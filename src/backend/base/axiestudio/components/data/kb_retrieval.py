import json
from pathlib import Path
from typing import Any

from cryptography.fernet import InvalidToken
from langchain_chroma import Chroma
from loguru import logger

from axiestudio.custom import Component
from axiestudio.io import BoolInput, DropdownInput, IntInput, MessageTextInput, Output, SecretStrInput
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.services.auth.utils import decrypt_api_key
from axiestudio.services.deps import get_settings_service

settings = get_settings_service().settings
knowledge_directory = settings.knowledge_bases_dir
if not knowledge_directory:
    msg = "Knowledge bases directory is not set in the settings."
    raise ValueError(msg)
KNOWLEDGE_BASES_ROOT_PATH = Path(knowledge_directory).expanduser()


class KBRetrievalComponent(Component):
    display_name = "Knowledge Retrieval"
    description = "Search and retrieve data from knowledge."
    icon = "database"
    name = "KBRetrieval"

    inputs = [
        DropdownInput(
            name="knowledge_base",
            display_name="Knowledge",
            info="Select the knowledge to load data from.",
            required=True,
            options=[
                str(d.name) for d in KNOWLEDGE_BASES_ROOT_PATH.iterdir() if not d.name.startswith(".") and d.is_dir()
            ]
            if KNOWLEDGE_BASES_ROOT_PATH.exists()
            else [],
            refresh_button=True,
            real_time_refresh=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="Embedding Provider API Key",
            info="API key for the embedding provider to generate embeddings.",
            advanced=True,
            required=False,
        ),
        MessageTextInput(
            name="search_query",
            display_name="Search Query",
            info="Optional search query to filter knowledge base data.",
        ),
        IntInput(
            name="top_k",
            display_name="Top K Results",
            info="Number of top results to return from the knowledge base.",
            value=5,
            advanced=True,
            required=False,
        ),
        BoolInput(
            name="include_metadata",
            display_name="Include Metadata",
            info="Whether to include all metadata and embeddings in the output. If false, only content is returned.",
            value=True,
            advanced=False,
        ),
    ]

    outputs = [
        Output(
            name="chroma_kb_data",
            display_name="Results",
            method="get_chroma_kb_data",
            info="Returns the data from the selected knowledge base.",
        ),
    ]

    def _get_knowledge_bases(self) -> list[str]:
        """Retrieve a list of available knowledge bases.

        Returns:
            A list of knowledge base names.
        """
        if not KNOWLEDGE_BASES_ROOT_PATH.exists():
            return []

        return [str(d.name) for d in KNOWLEDGE_BASES_ROOT_PATH.iterdir() if not d.name.startswith(".") and d.is_dir()]

    def update_build_config(self, build_config, field_value, field_name=None):  # noqa: ARG002
        if field_name == "knowledge_base":
            # Update the knowledge base options dynamically
            build_config["knowledge_base"]["options"] = self._get_knowledge_bases()

            # If the selected knowledge base is not available, reset it
            if build_config["knowledge_base"]["value"] not in build_config["knowledge_base"]["options"]:
                build_config["knowledge_base"]["value"] = None

        return build_config

    def _get_kb_metadata(self, kb_path: Path) -> dict[str, Any] | None:
        """Load knowledge base metadata from config file.

        Args:
            kb_path: Path to the knowledge base directory.

        Returns:
            Dictionary containing the knowledge base metadata, or None if not found.
        """
        config_file = kb_path / "config.json"
        if not config_file.exists():
            return None

        try:
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load KB metadata from {config_file}: {e}")
            return None

    def _build_embeddings(self, metadata: dict[str, Any]):
        """Build embedding function based on KB metadata.

        Args:
            metadata: Knowledge base metadata containing embedding configuration.

        Returns:
            Embedding function instance.
        """
        provider = metadata.get("embedding_provider", "OpenAI")
        model = metadata.get("embedding_model", "text-embedding-3-small")

        # Get API key (try provided key first, then encrypted key from metadata)
        api_key = self.api_key
        if not api_key and "encrypted_api_key" in metadata:
            try:
                api_key = decrypt_api_key(metadata["encrypted_api_key"], settings.secret_key)
            except (InvalidToken, Exception) as e:
                logger.warning(f"Failed to decrypt stored API key: {e}")

        if provider == "OpenAI":
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                model=model,
                api_key=api_key,
            )
        elif provider == "HuggingFace":
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=model)
        elif provider == "Cohere":
            from langchain_cohere import CohereEmbeddings
            return CohereEmbeddings(
                model=model,
                cohere_api_key=api_key,
            )
        else:
            msg = f"Unsupported embedding provider: {provider}"
            raise ValueError(msg)

    def get_chroma_kb_data(self) -> DataFrame:
        """Retrieve data from the selected knowledge base by reading the Chroma collection.

        Returns:
            A DataFrame containing the data rows from the knowledge base.
        """
        kb_path = KNOWLEDGE_BASES_ROOT_PATH / self.knowledge_base

        metadata = self._get_kb_metadata(kb_path)
        if not metadata:
            msg = f"Metadata not found for knowledge base: {self.knowledge_base}. Ensure it has been indexed."
            raise ValueError(msg)

        # Build the embedder for the knowledge base
        embedding_function = self._build_embeddings(metadata)

        # Load vector store
        chroma = Chroma(
            persist_directory=str(kb_path),
            embedding_function=embedding_function,
            collection_name=self.knowledge_base,
        )

        try:
            if self.search_query:
                # Perform similarity search
                results = chroma.similarity_search_with_score(
                    query=self.search_query,
                    k=self.top_k or 5,
                )
                
                # Convert results to DataFrame
                data_rows = []
                for doc, score in results:
                    row_data = {"content": doc.page_content, "similarity_score": score}
                    if self.include_metadata and doc.metadata:
                        row_data.update(doc.metadata)
                    data_rows.append(row_data)
                
            else:
                # Get all documents
                collection = chroma.get()
                
                # Convert to DataFrame
                data_rows = []
                documents = collection.get("documents", [])
                metadatas = collection.get("metadatas", [])
                
                for i, doc in enumerate(documents):
                    row_data = {"content": doc}
                    if self.include_metadata and i < len(metadatas) and metadatas[i]:
                        row_data.update(metadatas[i])
                    data_rows.append(row_data)
                
                # Limit results if top_k is specified
                if self.top_k and self.top_k > 0:
                    data_rows = data_rows[:self.top_k]

            # Set status message
            self.status = f"✅ Retrieved {len(data_rows)} documents from **{self.knowledge_base}**"
            
            return DataFrame(data_rows)

        except Exception as e:
            error_msg = f"Failed to retrieve data from knowledge base: {e}"
            self.status = f"❌ {error_msg}"
            logger.error(error_msg, exc_info=True)
            raise

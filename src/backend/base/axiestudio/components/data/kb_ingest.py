from __future__ import annotations

import hashlib
import json
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from cryptography.fernet import InvalidToken
from langchain_chroma import Chroma
from loguru import logger

from axiestudio.base.models.openai_constants import OPENAI_EMBEDDING_MODEL_NAMES
from axiestudio.custom import Component
from axiestudio.io import BoolInput, DataFrameInput, DropdownInput, IntInput, Output, SecretStrInput, StrInput, TableInput
from axiestudio.schema.data import Data
from axiestudio.schema.dotdict import dotdict  # noqa: TC001
from axiestudio.schema.table import EditMode
from axiestudio.services.auth.utils import decrypt_api_key, encrypt_api_key
from axiestudio.services.deps import get_settings_service

HUGGINGFACE_MODEL_NAMES = ["sentence-transformers/all-MiniLM-L6-v2", "sentence-transformers/all-mpnet-base-v2"]
COHERE_MODEL_NAMES = ["embed-english-v3.0", "embed-multilingual-v3.0"]

settings = get_settings_service().settings
knowledge_directory = settings.knowledge_bases_dir
if not knowledge_directory:
    msg = "Knowledge bases directory is not set in the settings."
    raise ValueError(msg)
KNOWLEDGE_BASES_ROOT_PATH = Path(knowledge_directory).expanduser()


class KBIngestionComponent(Component):
    """Create or append to Axie Studio Knowledge from a DataFrame."""

    # ------ UI metadata ---------------------------------------------------
    display_name = "Knowledge Ingestion"
    description = "Create or update knowledge in Axie Studio."
    icon = "database"
    name = "KBIngestion"

    @dataclass
    class NewKnowledgeBaseInput:
        functionality: str = "create"
        fields: dict[str, dict] = field(
            default_factory=lambda: {
                "knowledge_base": {
                    "type": "str",
                    "required": True,
                    "placeholder": "Enter knowledge base name",
                    "display_name": "Knowledge Base Name",
                    "info": "Name for the new knowledge base (alphanumeric, hyphens, underscores only).",
                }
            }
        )

    @dataclass
    class ColumnConfig:
        """Configuration for a single column in the knowledge base."""

        column_name: str
        vectorize: bool = True
        description: str = ""

    # ------ Inputs --------------------------------------------------------
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
            dialog_inputs=asdict(NewKnowledgeBaseInput()),
        ),
        DataFrameInput(
            name="input_df",
            display_name="Data",
            info="Table with all original columns (already chunked / processed).",
            required=True,
        ),
        DropdownInput(
            name="embedding_provider",
            display_name="Embedding Provider",
            info="Provider for generating embeddings.",
            options=["OpenAI", "HuggingFace", "Cohere"],
            value="OpenAI",
            required=True,
        ),
        DropdownInput(
            name="embedding_model",
            display_name="Embedding Model",
            info="Model to use for generating embeddings.",
            options=OPENAI_EMBEDDING_MODEL_NAMES,
            value="text-embedding-3-small",
            required=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="API key for the embedding provider.",
            required=False,
        ),
        TableInput(
            name="column_config",
            display_name="Column Configuration",
            info="Configure which columns to vectorize and their descriptions.",
            table_schema=[
                {"name": "column_name", "display_name": "Column", "type": "str", "readonly": True},
                {"name": "vectorize", "display_name": "Vectorize", "type": "bool"},
                {"name": "description", "display_name": "Description", "type": "str"},
            ],
            value=[],
            edit_mode=EditMode.EDITABLE,
        ),
        BoolInput(
            name="clear_existing",
            display_name="Clear Existing Data",
            info="Whether to clear existing data in the knowledge base before adding new data.",
            value=False,
            advanced=True,
        ),
        IntInput(
            name="chunk_size",
            display_name="Chunk Size",
            info="Number of documents to process in each batch.",
            value=100,
            advanced=True,
        ),
    ]

    outputs = [
        Output(
            name="kb_info",
            display_name="Knowledge Base Info",
            method="build_kb_info",
            info="Information about the created/updated knowledge base.",
        ),
    ]

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        """Update build configuration based on field changes."""
        if field_name == "input_df" and field_value is not None:
            # Auto-populate column configuration when DataFrame is provided
            try:
                df = field_value
                if hasattr(df, "columns"):
                    column_configs = []
                    for col in df.columns:
                        column_configs.append({
                            "column_name": str(col),
                            "vectorize": True,
                            "description": f"Content from {col} column",
                        })
                    build_config["column_config"]["value"] = column_configs
            except Exception as e:
                logger.warning(f"Failed to auto-populate column config: {e}")

        if field_name == "embedding_provider":
            # Update embedding model options based on provider
            if field_value == "OpenAI":
                build_config["embedding_model"]["options"] = OPENAI_EMBEDDING_MODEL_NAMES
                build_config["embedding_model"]["value"] = "text-embedding-3-small"
            elif field_value == "HuggingFace":
                build_config["embedding_model"]["options"] = HUGGINGFACE_MODEL_NAMES
                build_config["embedding_model"]["value"] = "sentence-transformers/all-MiniLM-L6-v2"
            elif field_value == "Cohere":
                build_config["embedding_model"]["options"] = COHERE_MODEL_NAMES
                build_config["embedding_model"]["value"] = "embed-english-v3.0"

        return build_config

    def _validate_column_config(self, df_source: pd.DataFrame) -> list[ColumnConfig]:
        """Validate and convert column configuration."""
        config_list = []
        
        if not self.column_config:
            # Default: vectorize all columns
            for col in df_source.columns:
                config_list.append(ColumnConfig(
                    column_name=str(col),
                    vectorize=True,
                    description=f"Content from {col} column"
                ))
        else:
            # Use provided configuration
            for config_row in self.column_config:
                if isinstance(config_row, dict):
                    config_list.append(ColumnConfig(
                        column_name=config_row.get("column_name", ""),
                        vectorize=config_row.get("vectorize", True),
                        description=config_row.get("description", "")
                    ))
        
        return config_list

    def _build_column_metadata(self, config_list: list[ColumnConfig], df_source: pd.DataFrame) -> dict[str, Any]:
        """Build metadata about columns."""
        return {
            "total_columns": len(df_source.columns),
            "vectorized_columns": len([c for c in config_list if c.vectorize]),
            "metadata_columns": len([c for c in config_list if not c.vectorize]),
            "column_details": [
                {
                    "name": config.column_name,
                    "vectorize": config.vectorize,
                    "description": config.description,
                    "data_type": str(df_source[config.column_name].dtype) if config.column_name in df_source.columns else "unknown"
                }
                for config in config_list
            ]
        }

    def _get_kb_root(self) -> Path:
        """Get the knowledge base root directory."""
        KNOWLEDGE_BASES_ROOT_PATH.mkdir(parents=True, exist_ok=True)
        return KNOWLEDGE_BASES_ROOT_PATH

    def _build_embeddings(self, embedding_model: str, api_key: str | None = None):
        """Build embedding function based on provider and model."""
        if self.embedding_provider == "OpenAI":
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                model=embedding_model,
                api_key=api_key,
            )
        elif self.embedding_provider == "HuggingFace":
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=embedding_model)
        elif self.embedding_provider == "Cohere":
            from langchain_cohere import CohereEmbeddings
            return CohereEmbeddings(
                model=embedding_model,
                cohere_api_key=api_key,
            )
        else:
            msg = f"Unsupported embedding provider: {self.embedding_provider}"
            raise ValueError(msg)

    def _create_vector_store(self, df_source: pd.DataFrame, config_list: list[ColumnConfig], embedding_model, api_key: str | None = None):
        """Create vector store from DataFrame."""
        # Get columns to vectorize
        content_cols = [config.column_name for config in config_list if config.vectorize and config.column_name in df_source.columns]
        
        if not content_cols:
            msg = "No columns selected for vectorization"
            raise ValueError(msg)

        # Build embedding function
        embedding_function = self._build_embeddings(embedding_model, api_key)
        
        # Prepare documents for vectorization
        documents = []
        metadatas = []
        
        # Convert each row to a document
        for _, row in df_source.iterrows():
            # Build content text from vectorized columns
            content_parts = [str(row[col]) for col in content_cols if col in row and pd.notna(row[col])]
            page_content = " ".join(content_parts)
            
            # Build metadata from NON-vectorized columns
            metadata = {}
            for col in df_source.columns:
                if col not in content_cols and col in row and pd.notna(row[col]):
                    metadata[col] = str(row[col])
            
            documents.append(page_content)
            metadatas.append(metadata)
        
        # Create or update Chroma collection
        kb_path = self._get_kb_root() / self.knowledge_base
        kb_path.mkdir(parents=True, exist_ok=True)
        
        chroma = Chroma(
            persist_directory=str(kb_path),
            embedding_function=embedding_function,
            collection_name=self.knowledge_base,
        )
        
        # Clear existing data if requested
        if self.clear_existing:
            chroma.delete_collection()
            chroma = Chroma(
                persist_directory=str(kb_path),
                embedding_function=embedding_function,
                collection_name=self.knowledge_base,
            )
        
        # Add documents in chunks
        chunk_size = self.chunk_size or 100
        for i in range(0, len(documents), chunk_size):
            chunk_docs = documents[i:i + chunk_size]
            chunk_metas = metadatas[i:i + chunk_size]
            chunk_ids = [f"{self.knowledge_base}_{i + j}" for j in range(len(chunk_docs))]
            
            chroma.add_texts(
                texts=chunk_docs,
                metadatas=chunk_metas,
                ids=chunk_ids,
            )
        
        return chroma

    def _save_kb_files(self, kb_path: Path, config_list: list[ColumnConfig]):
        """Save knowledge base configuration files."""
        # Save column configuration
        config_data = {
            "embedding_provider": self.embedding_provider,
            "embedding_model": self.embedding_model,
            "column_config": [
                {
                    "column_name": config.column_name,
                    "vectorize": config.vectorize,
                    "description": config.description,
                }
                for config in config_list
            ],
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        
        # Encrypt and save API key if provided
        if self.api_key:
            try:
                encrypted_key = encrypt_api_key(self.api_key, settings.secret_key)
                config_data["encrypted_api_key"] = encrypted_key
            except Exception as e:
                logger.warning(f"Failed to encrypt API key: {e}")
        
        config_file = kb_path / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)

    def _validate_kb_name(self, name: str) -> bool:
        """Validate knowledge base name."""
        if not name or len(name.strip()) == 0:
            return False
        
        # Check length (condition 1)
        if len(name) > 50:
            return False
        
        # Check for spaces (condition 2)
        if " " in name:
            return False
        
        # Check allowed characters (condition 3)
        return re.match(r"^[a-zA-Z0-9_-]+$", name) is not None

    # ---------------------------------------------------------------------
    #                         OUTPUT METHODS
    # ---------------------------------------------------------------------
    def build_kb_info(self) -> Data:
        """Main ingestion routine → returns a dict with KB metadata."""
        try:
            # Get source DataFrame
            df_source: pd.DataFrame = self.input_df
            
            # Validate column configuration
            config_list = self._validate_column_config(df_source)
            column_metadata = self._build_column_metadata(config_list, df_source)
            
            # Prepare KB folder
            kb_root = self._get_kb_root()
            kb_path = kb_root / self.knowledge_base
            
            # Validate knowledge base name
            if not self._validate_kb_name(self.knowledge_base):
                msg = "Invalid knowledge base name. Use only alphanumeric characters, hyphens, and underscores (max 50 chars, no spaces)."
                raise ValueError(msg)
            
            # Create vector store
            self._create_vector_store(df_source, config_list, embedding_model=self.embedding_model, api_key=self.api_key)
            
            # Save KB files
            self._save_kb_files(kb_path, config_list)
            
            # Build metadata response
            meta: dict[str, Any] = {
                "kb_id": str(uuid.uuid4()),
                "kb_name": self.knowledge_base,
                "rows": len(df_source),
                "column_metadata": column_metadata,
                "path": str(kb_path),
                "config_columns": len(config_list),
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            }
            
            # Set status message
            self.status = f"✅ KB **{self.knowledge_base}** saved · {len(df_source)} chunks."
            
            return Data(data=meta)
            
        except Exception as e:
            error_msg = f"Knowledge base ingestion failed: {e}"
            self.status = f"❌ {error_msg}"
            logger.error(error_msg, exc_info=True)
            raise

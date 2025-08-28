from langchain_openai import OpenAIEmbeddings

from axiestudio.base.embeddings.model import LCEmbeddingsModel
from axiestudio.base.models.openai_constants import OPENAI_EMBEDDING_MODEL_NAMES
from axiestudio.field_typing import Embeddings
from axiestudio.io import BoolInput, DictInput, DropdownInput, FloatInput, IntInput, MessageTextInput, SecretStrInput


class OpenAIEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "OpenAI-inbäddningar"
    description = "Generera embeddings med OpenAI-modeller."
    icon = "OpenAI"
    name = "OpenAIEmbeddings"

    inputs = [
        DictInput(
            name="default_headers",
            display_name="Standardhuvuden",
            advanced=True,
            info="Standardhuvuden att använda för API-förfrågan.",
        ),
        DictInput(
            name="default_query",
            display_name="Standardfråga",
            advanced=True,
            info="Standardfrågeparametrar att använda för API-förfrågan.",
        ),
        IntInput(name="chunk_size", display_name="Chunkstorlek", advanced=True, value=1000),
        MessageTextInput(name="client", display_name="Klient", advanced=True),
        MessageTextInput(name="deployment", display_name="Distribution", advanced=True),
        IntInput(name="embedding_ctx_length", display_name="Embedding-kontextlängd", advanced=True, value=1536),
        IntInput(name="max_retries", display_name="Max återförsök", value=3, advanced=True),
        DropdownInput(
            name="model",
            display_name="Modell",
            advanced=False,
            options=OPENAI_EMBEDDING_MODEL_NAMES,
            value="text-embedding-3-small",
        ),
        DictInput(name="model_kwargs", display_name="Modellargument", advanced=True),
        SecretStrInput(name="openai_api_key", display_name="OpenAI API-nyckel", value="OPENAI_API_KEY", required=True),
        MessageTextInput(name="openai_api_base", display_name="OpenAI API-bas", advanced=True),
        MessageTextInput(name="openai_api_type", display_name="OpenAI API-typ", advanced=True),
        MessageTextInput(name="openai_api_version", display_name="OpenAI API-version", advanced=True),
        MessageTextInput(
            name="openai_organization",
            display_name="OpenAI-organisation",
            advanced=True,
        ),
        MessageTextInput(name="openai_proxy", display_name="OpenAI Proxy", advanced=True),
        FloatInput(name="request_timeout", display_name="Timeout för förfrågan", advanced=True),
        BoolInput(name="show_progress_bar", display_name="Visa förloppsindikator", advanced=True),
        BoolInput(name="skip_empty", display_name="Hoppa över tomma", advanced=True),
        MessageTextInput(
            name="tiktoken_model_name",
            display_name="TikToken-modellnamn",
            advanced=True,
        ),
        BoolInput(
            name="tiktoken_enable",
            display_name="Aktivera TikToken",
            advanced=True,
            value=True,
            info="Om False måste du ha transformers installerat.",
        ),
        IntInput(
            name="dimensions",
            display_name="Dimensioner",
            info="Antalet dimensioner som de resulterande utmatningsembeddingarna ska ha. "
            "Stöds endast av vissa modeller.",
            advanced=True,
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        return OpenAIEmbeddings(
            client=self.client or None,
            model=self.model,
            dimensions=self.dimensions or None,
            deployment=self.deployment or None,
            api_version=self.openai_api_version or None,
            base_url=self.openai_api_base or None,
            openai_api_type=self.openai_api_type or None,
            openai_proxy=self.openai_proxy or None,
            embedding_ctx_length=self.embedding_ctx_length,
            api_key=self.openai_api_key or None,
            organization=self.openai_organization or None,
            allowed_special="all",
            disallowed_special="all",
            chunk_size=self.chunk_size,
            max_retries=self.max_retries,
            timeout=self.request_timeout or None,
            tiktoken_enabled=self.tiktoken_enable,
            tiktoken_model_name=self.tiktoken_model_name or None,
            show_progress_bar=self.show_progress_bar,
            model_kwargs=self.model_kwargs,
            skip_empty=self.skip_empty,
            default_headers=self.default_headers or None,
            default_query=self.default_query or None,
        )

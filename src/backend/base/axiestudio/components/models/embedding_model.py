from typing import Any

from langchain_openai import OpenAIEmbeddings

from axiestudio.base.embeddings.model import LCEmbeddingsModel
from axiestudio.base.models.openai_constants import OPENAI_EMBEDDING_MODEL_NAMES
from axiestudio.field_typing import Embeddings
from axiestudio.io import (
    BoolInput,
    DictInput,
    DropdownInput,
    FloatInput,
    IntInput,
    MessageTextInput,
    SecretStrInput,
)
from axiestudio.schema.dotdict import dotdict


class EmbeddingModelComponent(LCEmbeddingsModel):
    display_name = "Inbäddningsmodell"
    description = "Generera inbäddningar med en angiven leverantör."
    documentation: str = "https://docs.axiestudio.se/components-embedding-models"
    icon = "binary"
    name = "EmbeddingModel"
    category = "models"

    inputs = [
        DropdownInput(
            name="provider",
            display_name="Modellleverantör",
            options=["OpenAI"],
            value="OpenAI",
            info="Välj leverantör för inbäddningsmodell",
            real_time_refresh=True,
            options_metadata=[{"icon": "OpenAI"}],
        ),
        DropdownInput(
            name="model",
            display_name="Modellnamn",
            options=OPENAI_EMBEDDING_MODEL_NAMES,
            value=OPENAI_EMBEDDING_MODEL_NAMES[0],
            info="Välj inbäddningsmodell att använda",
        ),
        SecretStrInput(
            name="api_key",
            display_name="OpenAI API-nyckel",
            info="Modellleverantörens API-nyckel",
            required=True,
            show=True,
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="api_base",
            display_name="API-bas-URL",
            info="Bas-URL för API:et. Lämna tom för standard.",
            advanced=True,
        ),
        IntInput(
            name="dimensions",
            display_name="Dimensioner",
            info="Antalet dimensioner som de resulterande utmatningsinbäddningarna ska ha. "
            "Stöds endast av vissa modeller.",
            advanced=True,
        ),
        IntInput(name="chunk_size", display_name="Bitstorlek", advanced=True, value=1000),
        FloatInput(name="request_timeout", display_name="Timeout för förfrågan", advanced=True),
        IntInput(name="max_retries", display_name="Max återförsök", advanced=True, value=3),
        BoolInput(name="show_progress_bar", display_name="Visa förloppsindikator", advanced=True),
        DictInput(
            name="model_kwargs",
            display_name="Modellargument",
            advanced=True,
            info="Ytterligare nyckelordsargument att skicka till modellen.",
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        provider = self.provider
        model = self.model
        api_key = self.api_key
        api_base = self.api_base
        dimensions = self.dimensions
        chunk_size = self.chunk_size
        request_timeout = self.request_timeout
        max_retries = self.max_retries
        show_progress_bar = self.show_progress_bar
        model_kwargs = self.model_kwargs or {}

        if provider == "OpenAI":
            if not api_key:
                msg = "OpenAI API-nyckel krävs när OpenAI-leverantör används"
                raise ValueError(msg)
            return OpenAIEmbeddings(
                model=model,
                dimensions=dimensions or None,
                base_url=api_base or None,
                api_key=api_key,
                chunk_size=chunk_size,
                max_retries=max_retries,
                timeout=request_timeout or None,
                show_progress_bar=show_progress_bar,
                model_kwargs=model_kwargs,
            )
        msg = f"Okänd leverantör: {provider}"
        raise ValueError(msg)

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "provider" and field_value == "OpenAI":
            build_config["model"]["options"] = OPENAI_EMBEDDING_MODEL_NAMES
            build_config["model"]["value"] = OPENAI_EMBEDDING_MODEL_NAMES[0]
            build_config["api_key"]["display_name"] = "OpenAI API-nyckel"
            build_config["api_base"]["display_name"] = "OpenAI API-bas-URL"
        return build_config

from typing import Any

import cohere
from langchain_cohere import CohereEmbeddings

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import Embeddings
from axiestudio.io import DropdownInput, FloatInput, IntInput, MessageTextInput, Output, SecretStrInput

HTTP_STATUS_OK = 200


class CohereEmbeddingsComponent(LCModelComponent):
    display_name = "Cohere Inbäddningar"
    description = "Generera inbäddningar med Cohere-modeller."
    icon = "Cohere"
    name = "CohereEmbeddings"

    inputs = [
        SecretStrInput(name="api_key", display_name="Cohere API-nyckel", required=True, real_time_refresh=True),
        DropdownInput(
            name="model_name",
            display_name="Modell",
            advanced=False,
            options=[
                "embed-english-v2.0",
                "embed-multilingual-v2.0",
                "embed-english-light-v2.0",
                "embed-multilingual-light-v2.0",
            ],
            value="embed-english-v2.0",
            refresh_button=True,
            combobox=True,
        ),
        MessageTextInput(name="truncate", display_name="Trunkera", advanced=True),
        IntInput(name="max_retries", display_name="Max försök", value=3, advanced=True),
        MessageTextInput(name="user_agent", display_name="Användaragent", advanced=True, value="langchain"),
        FloatInput(name="request_timeout", display_name="Timeout för förfrågan", advanced=True),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def build_embeddings(self) -> Embeddings:
        data = None
        try:
            data = CohereEmbeddings(
                cohere_api_key=self.api_key,
                model=self.model_name,
                truncate=self.truncate,
                max_retries=self.max_retries,
                user_agent=self.user_agent,
                request_timeout=self.request_timeout or None,
            )
        except Exception as e:
            msg = (
                "Kunde inte skapa Cohere-inbäddningar. ",
                "Vänligen verifiera API-nyckeln och modellparametrarna, och försök igen.",
            )
            raise ValueError(msg) from e
        # added status if not the return data would be serialised to create the status
        return data

    def get_model(self):
        try:
            co = cohere.ClientV2(self.api_key)
            response = co.models.list(endpoint="embed")
            models = response.models
            return [model.name for model in models]
        except Exception as e:
            msg = f"Misslyckades med att hämta Cohere-modeller. Fel: {e}"
            raise ValueError(msg) from e

    async def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None):
        if field_name in {"model_name", "api_key"}:
            if build_config.get("api_key", {}).get("value", None):
                build_config["model_name"]["options"] = self.get_model()
        else:
            build_config["model_name"]["options"] = field_value
        return build_config

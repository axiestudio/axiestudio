from typing import Any
from urllib.parse import urljoin

import httpx

from axiestudio.base.embeddings.model import LCEmbeddingsModel
from axiestudio.field_typing import Embeddings
from axiestudio.inputs.inputs import DropdownInput, SecretStrInput
from axiestudio.io import FloatInput, MessageTextInput


class LMStudioEmbeddingsComponent(LCEmbeddingsModel):
    display_name: str = "LM Studio Inbäddningar"
    description: str = "Generera inbäddningar med LM Studio."
    icon = "LMStudio"

    async def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None):  # noqa: ARG002
        if field_name == "model":
            base_url_dict = build_config.get("base_url", {})
            base_url_load_from_db = base_url_dict.get("load_from_db", False)
            base_url_value = base_url_dict.get("value")
            if base_url_load_from_db:
                base_url_value = await self.get_variables(base_url_value, field_name)
            elif not base_url_value:
                base_url_value = "http://localhost:1234/v1"
            build_config["model"]["options"] = await self.get_model(base_url_value)

        return build_config

    @staticmethod
    async def get_model(base_url_value: str) -> list[str]:
        try:
            url = urljoin(base_url_value, "/v1/models")
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                return [model["id"] for model in data.get("data", [])]
        except Exception as e:
            msg = "Kunde inte hämta modeller. Vänligen säkerställ att LM Studio-servern körs."
            raise ValueError(msg) from e

    inputs = [
        DropdownInput(
            name="model",
            display_name="Modell",
            advanced=False,
            refresh_button=True,
            required=True,
        ),
        MessageTextInput(
            name="base_url",
            display_name="LM Studio bas-URL",
            refresh_button=True,
            value="http://localhost:1234/v1",
            required=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="LM Studio API-nyckel",
            advanced=True,
            value="LMSTUDIO_API_KEY",
        ),
        FloatInput(
            name="temperature",
            display_name="Modelltemperatur",
            value=0.1,
            advanced=True,
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        try:
            from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
        except ImportError as e:
            msg = "Vänligen installera langchain-nvidia-ai-endpoints för att använda LM Studio Inbäddningar."
            raise ImportError(msg) from e
        try:
            output = NVIDIAEmbeddings(
                model=self.model,
                base_url=self.base_url,
                temperature=self.temperature,
                nvidia_api_key=self.api_key,
            )
        except Exception as e:
            msg = f"Kunde inte ansluta till LM Studio API. Fel: {e}"
            raise ValueError(msg) from e
        return output

from collections import defaultdict
from typing import Any

import httpx
from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import (
    DropdownInput,
    IntInput,
    SecretStrInput,
    SliderInput,
    StrInput,
)


class OpenRouterComponent(LCModelComponent):
    """OpenRouter API component for language models."""

    display_name = "OpenRouter"
    description = (
        "OpenRouter ger enhetlig åtkomst till flera AI-modeller från olika leverantörer genom ett enda API."
    )
    icon = "OpenRouter"

    inputs = [
        *LCModelComponent._base_inputs,
        SecretStrInput(
            name="api_key", display_name="OpenRouter API-nyckel", required=True, info="Din OpenRouter API-nyckel"
        ),
        StrInput(
            name="site_url",
            display_name="Webbplats-URL",
            info="Din webbplats-URL för OpenRouter-rankningar",
            advanced=True,
        ),
        StrInput(
            name="app_name",
            display_name="Appnamn",
            info="Ditt appnamn för OpenRouter-rankningar",
            advanced=True,
        ),
        DropdownInput(
            name="provider",
            display_name="Leverantör",
            info="AI-modellleverantören",
            options=["Laddar leverantörer..."],
            value="Laddar leverantörer...",
            real_time_refresh=True,
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Modell",
            info="Modellen att använda för chattslutförande",
            options=["Välj en leverantör först"],
            value="Välj en leverantör först",
            real_time_refresh=True,
            required=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.7,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            info="Kontrollerar slumpmässighet. Lägre värden är mer deterministiska, högre värden är mer kreativa.",
            advanced=True,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            info="Maximalt antal tokens att generera",
            advanced=True,
        ),
    ]

    def fetch_models(self) -> dict[str, list]:
        """Fetch available models from OpenRouter API and organize them by provider."""
        url = "https://openrouter.ai/api/v1/models"

        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()

                models_data = response.json().get("data", [])
                provider_models = defaultdict(list)

                for model in models_data:
                    model_id = model.get("id", "")
                    if "/" in model_id:
                        provider = model_id.split("/")[0].title()
                        provider_models[provider].append(
                            {
                                "id": model_id,
                                "name": model.get("name", ""),
                                "description": model.get("description", ""),
                                "context_length": model.get("context_length", 0),
                            }
                        )

                return dict(provider_models)

        except httpx.HTTPError as e:
            self.log(f"Fel vid hämtning av modeller: {e!s}")
            return {"Error": [{"id": "error", "name": f"Fel vid hämtning av modeller: {e!s}"}]}

    def build_model(self) -> LanguageModel:
        """Build and return the OpenRouter language model."""
        model_not_selected = "Vänligen välj en modell"
        api_key_required = "API-nyckel krävs"

        if not self.model_name or self.model_name == "Välj en leverantör först":
            raise ValueError(model_not_selected)

        if not self.api_key:
            raise ValueError(api_key_required)

        api_key = SecretStr(self.api_key).get_secret_value()

        # Build base configuration
        kwargs: dict[str, Any] = {
            "model": self.model_name,
            "openai_api_key": api_key,
            "openai_api_base": "https://openrouter.ai/api/v1",
            "temperature": self.temperature if self.temperature is not None else 0.7,
        }

        # Add optional parameters
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        headers = {}
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.app_name:
            headers["X-Title"] = self.app_name

        if headers:
            kwargs["default_headers"] = headers

        try:
            return ChatOpenAI(**kwargs)
        except (ValueError, httpx.HTTPError) as err:
            error_msg = f"Misslyckades med att bygga modell: {err!s}"
            self.log(error_msg)
            raise ValueError(error_msg) from err

    def _get_exception_message(self, e: Exception) -> str | None:
        """Get a message from an OpenRouter exception.

        Args:
            e (Exception): The exception to get the message from.

        Returns:
            str | None: The message from the exception, or None if no specific message can be extracted.
        """
        try:
            from openai import BadRequestError

            if isinstance(e, BadRequestError):
                message = e.body.get("message")
                if message:
                    return message
        except ImportError:
            pass
        return None

    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None) -> dict:
        """Update build configuration based on field updates."""
        try:
            if field_name is None or field_name == "provider":
                provider_models = self.fetch_models()
                build_config["provider"]["options"] = sorted(provider_models.keys())
                if build_config["provider"]["value"] not in provider_models:
                    build_config["provider"]["value"] = build_config["provider"]["options"][0]

            if field_name == "provider" and field_value in self.fetch_models():
                provider_models = self.fetch_models()
                models = provider_models[field_value]

                build_config["model_name"]["options"] = [model["id"] for model in models]
                if models:
                    build_config["model_name"]["value"] = models[0]["id"]

                tooltips = {
                    model["id"]: (f"{model['name']}\nContext Length: {model['context_length']}\n{model['description']}")
                    for model in models
                }
                build_config["model_name"]["tooltips"] = tooltips

        except httpx.HTTPError as e:
            self.log(f"Error updating build config: {e!s}")
            build_config["provider"]["options"] = ["Error loading providers"]
            build_config["provider"]["value"] = "Error loading providers"
            build_config["model_name"]["options"] = ["Error loading models"]
            build_config["model_name"]["value"] = "Error loading models"

        return build_config

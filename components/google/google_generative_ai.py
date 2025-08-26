from typing import Any

import requests
from loguru import logger
from pydantic.v1 import SecretStr

from axiestudio.base.models.google_generative_ai_constants import GOOGLE_GENERATIVE_AI_MODELS
from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import (
    BoolInput,
    DropdownInput,
    FloatInput,
    IntInput,
    SecretStrInput,
    SliderInput,
)
from axiestudio.schema.dotdict import dotdict


class GoogleGenerativeAIComponent(LCModelComponent):
    display_name = "Google Generative AI"
    description = "Generera text med Google Generative AI."
    icon = "GoogleGenerativeAI"
    name = "GoogleGenerativeAIModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_output_tokens", display_name="Max utmatnings-tokens", info="Det maximala antalet tokens att generera."
        ),
        DropdownInput(
            name="model_name",
            display_name="Modell",
            info="Namnet på modellen att använda.",
            options=GOOGLE_GENERATIVE_AI_MODELS,
            value="gemini-1.5-pro",
            refresh_button=True,
            combobox=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="Google API-nyckel",
            info="Google API-nyckeln att använda för Google Generative AI.",
            required=True,
            real_time_refresh=True,
        ),
        FloatInput(
            name="top_p",
            display_name="Top P",
            info="Den maximala kumulativa sannolikheten för tokens att överväga vid sampling.",
            advanced=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            info="Kontrollerar slumpmässighet. Lägre värden är mer deterministiska, högre värden är mer kreativa.",
        ),
        IntInput(
            name="n",
            display_name="N",
            info="Antal chattavslutningar att generera för varje prompt. "
            "Observera att API:et kanske inte returnerar alla n avslutningar om dubbletter genereras.",
            advanced=True,
        ),
        IntInput(
            name="top_k",
            display_name="Top K",
            info="Avkoda med top-k sampling: överväg uppsättningen av de top_k mest sannolika tokens. Måste vara positivt.",
            advanced=True,
        ),
        BoolInput(
            name="tool_model_enabled",
            display_name="Verktygsmodell aktiverad",
            info="Om verktygsmodellen ska användas.",
            value=False,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as e:
            msg = "Paketet 'langchain_google_genai' krävs för att använda Google Generative AI-modellen."
            raise ImportError(msg) from e

        google_api_key = self.api_key
        model = self.model_name
        max_output_tokens = self.max_output_tokens
        temperature = self.temperature
        top_k = self.top_k
        top_p = self.top_p
        n = self.n

        return ChatGoogleGenerativeAI(
            model=model,
            max_output_tokens=max_output_tokens or None,
            temperature=temperature,
            top_k=top_k or None,
            top_p=top_p or None,
            n=n or 1,
            google_api_key=SecretStr(google_api_key).get_secret_value(),
        )

    def get_models(self, tool_model_enabled: bool | None = None) -> list[str]:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model_ids = [
                model.name.replace("models/", "")
                for model in genai.list_models()
                if "generateContent" in model.supported_generation_methods
            ]
            model_ids.sort(reverse=True)
        except (ImportError, ValueError) as e:
            logger.exception(f"Error getting model names: {e}")
            model_ids = GOOGLE_GENERATIVE_AI_MODELS
        if tool_model_enabled:
            try:
                from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
            except ImportError as e:
                msg = "langchain_google_genai is not installed."
                raise ImportError(msg) from e
            for model in model_ids:
                model_with_tool = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    google_api_key=self.api_key,
                )
                if not self.supports_tool_calling(model_with_tool):
                    model_ids.remove(model)
        return model_ids

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        if field_name in {"base_url", "model_name", "tool_model_enabled", "api_key"} and field_value:
            try:
                if len(self.api_key) == 0:
                    ids = GOOGLE_GENERATIVE_AI_MODELS
                else:
                    try:
                        ids = self.get_models(tool_model_enabled=self.tool_model_enabled)
                    except (ImportError, ValueError, requests.exceptions.RequestException) as e:
                        logger.exception(f"Error getting model names: {e}")
                        ids = GOOGLE_GENERATIVE_AI_MODELS
                build_config["model_name"]["options"] = ids
                build_config["model_name"]["value"] = ids[0]
            except Exception as e:
                msg = f"Error getting model names: {e}"
                raise ValueError(msg) from e
        return build_config

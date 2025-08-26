from langchain_mistralai import ChatMistralAI
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.io import BoolInput, DropdownInput, FloatInput, IntInput, SecretStrInput, StrInput


class MistralAIModelComponent(LCModelComponent):
    display_name = "MistralAI"
    description = "Genererar text med MistralAI LLM:er."
    icon = "MistralAI"
    name = "MistralModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            info="Det maximala antalet tokens att generera. Sätt till 0 för obegränsade tokens.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=[
                "open-mixtral-8x7b",
                "open-mixtral-8x22b",
                "mistral-small-latest",
                "mistral-medium-latest",
                "mistral-large-latest",
                "codestral-latest",
            ],
            value="codestral-latest",
        ),
        StrInput(
            name="mistral_api_base",
            display_name="Mistral API-bas",
            advanced=True,
            info="Bas-URL för Mistral API. Standard är https://api.mistral.ai/v1. "
            "Du kan ändra detta för att använda andra API:er som JinaChat, LocalAI och Prem.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="Mistral API-nyckel",
            info="Mistral API-nyckeln att använda för Mistral-modellen.",
            advanced=False,
            required=True,
            value="MISTRAL_API_KEY",
        ),
        FloatInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            advanced=True,
        ),
        IntInput(
            name="max_retries",
            display_name="Max återförsök",
            advanced=True,
            value=5,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            advanced=True,
            value=60,
        ),
        IntInput(
            name="max_concurrent_requests",
            display_name="Max samtidiga förfrågningar",
            advanced=True,
            value=3,
        ),
        FloatInput(
            name="top_p",
            display_name="Top P",
            advanced=True,
            value=1,
        ),
        IntInput(
            name="random_seed",
            display_name="Slumpmässigt frö",
            value=1,
            advanced=True,
        ),
        BoolInput(
            name="safe_mode",
            display_name="Säkert läge",
            advanced=True,
            value=False,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            return ChatMistralAI(
                model_name=self.model_name,
                mistral_api_key=SecretStr(self.api_key).get_secret_value() if self.api_key else None,
                endpoint=self.mistral_api_base or "https://api.mistral.ai/v1",
                max_tokens=self.max_tokens or None,
                temperature=self.temperature,
                max_retries=self.max_retries,
                timeout=self.timeout,
                max_concurrent_requests=self.max_concurrent_requests,
                top_p=self.top_p,
                random_seed=self.random_seed,
                safe_mode=self.safe_mode,
                streaming=self.stream,
            )
        except Exception as e:
            msg = "Could not connect to MistralAI API."
            raise ValueError(msg) from e

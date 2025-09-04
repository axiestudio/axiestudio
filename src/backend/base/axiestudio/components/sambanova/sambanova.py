from langchain_sambanova import ChatSambaNovaCloud
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.base.models.sambanova_constants import SAMBANOVA_MODEL_NAMES
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.io import DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput


class SambaNovaComponent(LCModelComponent):
    display_name = "SambaNova"
    description = "Generera text med Sambanova LLM:er."
    documentation = "https://cloud.sambanova.ai/"
    icon = "SambaNova"
    name = "SambaNovaModel"

    inputs = [
        *LCModelComponent._base_inputs,
        StrInput(
            name="base_url",
            display_name="SambaNova Cloud bas-URL",
            advanced=True,
            info="Bas-URL:en för Sambanova Cloud API. "
            "Standard är https://api.sambanova.ai/v1/chat/completions. "
            "Du kan ändra detta för att använda andra URL:er som Sambastudio",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=SAMBANOVA_MODEL_NAMES,
            value=SAMBANOVA_MODEL_NAMES[0],
        ),
        SecretStrInput(
            name="api_key",
            display_name="Sambanova API-nyckel",
            info="Sambanova API-nyckeln att använda för Sambanova-modellen.",
            advanced=False,
            value="SAMBANOVA_API_KEY",
            required=True,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            value=2048,
            info="Maximalt antal tokens att generera.",
        ),
        SliderInput(
            name="top_p",
            display_name="Top P",
            advanced=True,
            value=1.0,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            info="Modell top_p",
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        sambanova_url = self.base_url
        sambanova_api_key = self.api_key
        model_name = self.model_name
        max_tokens = self.max_tokens
        top_p = self.top_p
        temperature = self.temperature

        api_key = SecretStr(sambanova_api_key).get_secret_value() if sambanova_api_key else None

        return ChatSambaNovaCloud(
            model=model_name,
            max_tokens=max_tokens or 1024,
            temperature=temperature or 0.07,
            top_p=top_p,
            sambanova_url=sambanova_url,
            sambanova_api_key=api_key,
        )

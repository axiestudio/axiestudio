from langchain_community.chat_models import ChatMaritalk

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import DropdownInput, FloatInput, IntInput, SecretStrInput


class MaritalkModelComponent(LCModelComponent):
    display_name = "MariTalk"
    description = "Genererar text med MariTalk LLM:er."
    icon = "Maritalk"
    name = "Maritalk"
    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            value=512,
            info="Maximalt antal tokens att generera. Sätt till 0 för obegränsade tokens.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=["sabia-2-small", "sabia-2-medium"],
            value=["sabia-2-small"],
        ),
        SecretStrInput(
            name="api_key",
            display_name="MariTalk API-nyckel",
            info="MariTalk API-nyckeln att använda för autentisering.",
            advanced=False,
        ),
        FloatInput(name="temperature", display_name="Temperatur", value=0.1, range_spec=RangeSpec(min=0, max=1)),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        # self.output_schea is a list of dictionarie s
        # let's convert it to a dictionary
        api_key = self.api_key
        temperature = self.temperature
        model_name: str = self.model_name
        max_tokens = self.max_tokens

        return ChatMaritalk(
            max_tokens=max_tokens,
            model=model_name,
            api_key=api_key,
            temperature=temperature or 0.1,
        )

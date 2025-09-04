from langchain_cohere import ChatCohere
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.io import SecretStrInput, SliderInput


class CohereComponent(LCModelComponent):
    display_name = "Cohere Språkmodeller"
    description = "Generera text med Cohere LLM:er."
    documentation = "https://python.langchain.com/docs/modules/model_io/models/llms/integrations/cohere"
    icon = "Cohere"
    name = "CohereModel"

    inputs = [
        *LCModelComponent._base_inputs,
        SecretStrInput(
            name="cohere_api_key",
            display_name="Cohere API-nyckel",
            info="Cohere API-nyckeln som ska användas för Cohere-modellen.",
            advanced=False,
            value="COHERE_API_KEY",
            required=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.75,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            info="Styr slumpmässighet. Lägre värden är mer deterministiska, högre värden är mer kreativa.",
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        cohere_api_key = self.cohere_api_key
        temperature = self.temperature

        api_key = SecretStr(cohere_api_key).get_secret_value() if cohere_api_key else None

        return ChatCohere(
            temperature=temperature or 0.75,
            cohere_api_key=api_key,
        )

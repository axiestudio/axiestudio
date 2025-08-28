from langchain_community.chat_models import ChatPerplexity
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.io import DropdownInput, FloatInput, IntInput, SecretStrInput, SliderInput


class PerplexityComponent(LCModelComponent):
    display_name = "Perplexity"
    description = "Generera text med Perplexity LLM:er."
    documentation = "https://python.langchain.com/v0.2/docs/integrations/chat/perplexity/"
    icon = "Perplexity"
    name = "PerplexityModel"

    inputs = [
        *LCModelComponent._base_inputs,
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=[
                "llama-3.1-sonar-small-128k-online",
                "llama-3.1-sonar-large-128k-online",
                "llama-3.1-sonar-huge-128k-online",
                "llama-3.1-sonar-small-128k-chat",
                "llama-3.1-sonar-large-128k-chat",
                "llama-3.1-8b-instruct",
                "llama-3.1-70b-instruct",
            ],
            value="llama-3.1-sonar-small-128k-online",
        ),
        IntInput(
            name="max_output_tokens", display_name="Max utdata-tokens", info="Maximalt antal tokens att generera."
        ),
        SecretStrInput(
            name="api_key",
            display_name="Perplexity API-nyckel",
            info="Perplexity API-nyckeln att använda för Perplexity-modellen.",
            advanced=False,
            required=True,
        ),
        SliderInput(
            name="temperature", display_name="Temperatur", value=0.75, range_spec=RangeSpec(min=0, max=2, step=0.05)
        ),
        FloatInput(
            name="top_p",
            display_name="Top P",
            info="Den maximala kumulativa sannolikheten för tokens att överväga vid sampling.",
            advanced=True,
        ),
        IntInput(
            name="n",
            display_name="N",
            info="Antal chattslutföranden att generera för varje prompt. "
            "Observera att API:et kanske inte returnerar alla n slutföranden om dubbletter genereras.",
            advanced=True,
        ),
        IntInput(
            name="top_k",
            display_name="Top K",
            info="Avkoda med top-k-sampling: överväg uppsättningen av top_k mest sannolika tokens. Måste vara positiv.",
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        api_key = SecretStr(self.api_key).get_secret_value()
        temperature = self.temperature
        model = self.model_name
        max_output_tokens = self.max_output_tokens
        top_k = self.top_k
        top_p = self.top_p
        n = self.n

        return ChatPerplexity(
            model=model,
            temperature=temperature or 0.75,
            pplx_api_key=api_key,
            top_k=top_k or None,
            top_p=top_p or None,
            n=n or 1,
            max_output_tokens=max_output_tokens,
        )

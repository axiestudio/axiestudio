from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from axiestudio.base.models.anthropic_constants import ANTHROPIC_MODELS
from axiestudio.base.models.google_generative_ai_constants import GOOGLE_GENERATIVE_AI_MODELS
from axiestudio.base.models.model import LCModelComponent
from axiestudio.base.models.openai_constants import OPENAI_CHAT_MODEL_NAMES, OPENAI_REASONING_MODEL_NAMES
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import BoolInput
from axiestudio.io import DropdownInput, MessageInput, MultilineInput, SecretStrInput, SliderInput
from axiestudio.schema.dotdict import dotdict


class LanguageModelComponent(LCModelComponent):
    display_name = "Språkmodell"
    description = "Kör en språkmodell med en angiven leverantör."
    documentation: str = "https://docs.axiestudio.se/components-models"
    icon = "brain-circuit"
    category = "models"
    priority = 0  # Set priority to 0 to make it appear first

    inputs = [
        DropdownInput(
            name="provider",
            display_name="Modellleverantör",
            options=["OpenAI", "Anthropic", "Google"],
            value="OpenAI",
            info="Välj modellleverantören",
            real_time_refresh=True,
            options_metadata=[{"icon": "OpenAI"}, {"icon": "Anthropic"}, {"icon": "GoogleGenerativeAI"}],
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            options=OPENAI_CHAT_MODEL_NAMES + OPENAI_REASONING_MODEL_NAMES,
            value=OPENAI_CHAT_MODEL_NAMES[0],
            info="Välj modellen att använda",
            real_time_refresh=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="OpenAI API-nyckel",
            info="Modellleverantörens API-nyckel",
            required=False,
            show=True,
            real_time_refresh=True,
        ),
        MessageInput(
            name="input_value",
            display_name="Indata",
            info="Indatatexten att skicka till modellen",
        ),
        MultilineInput(
            name="system_message",
            display_name="Systemmeddelande",
            info="Ett systemmeddelande som hjälper till att ställa in assistentens beteende",
            advanced=False,
        ),
        BoolInput(
            name="stream",
            display_name="Stream",
            info="Om svaret ska strömmas",
            value=False,
            advanced=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            info="Kontrollerar slumpmässighet i svar",
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:
        provider = self.provider
        model_name = self.model_name
        temperature = self.temperature
        stream = self.stream

        if provider == "OpenAI":
            if not self.api_key:
                msg = "OpenAI API key is required when using OpenAI provider"
                raise ValueError(msg)

            if model_name in OPENAI_REASONING_MODEL_NAMES:
                # reasoning models do not support temperature (yet)
                temperature = None

            return ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                streaming=stream,
                openai_api_key=self.api_key,
            )
        if provider == "Anthropic":
            if not self.api_key:
                msg = "Anthropic API key is required when using Anthropic provider"
                raise ValueError(msg)
            return ChatAnthropic(
                model=model_name,
                temperature=temperature,
                streaming=stream,
                anthropic_api_key=self.api_key,
            )
        if provider == "Google":
            if not self.api_key:
                msg = "Google API key is required when using Google provider"
                raise ValueError(msg)
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                streaming=stream,
                google_api_key=self.api_key,
            )
        msg = f"Unknown provider: {provider}"
        raise ValueError(msg)

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "provider":
            if field_value == "OpenAI":
                build_config["model_name"]["options"] = OPENAI_CHAT_MODEL_NAMES + OPENAI_REASONING_MODEL_NAMES
                build_config["model_name"]["value"] = OPENAI_CHAT_MODEL_NAMES[0]
                build_config["api_key"]["display_name"] = "OpenAI API-nyckel"
            elif field_value == "Anthropic":
                build_config["model_name"]["options"] = ANTHROPIC_MODELS
                build_config["model_name"]["value"] = ANTHROPIC_MODELS[0]
                build_config["api_key"]["display_name"] = "Anthropic API-nyckel"
            elif field_value == "Google":
                build_config["model_name"]["options"] = GOOGLE_GENERATIVE_AI_MODELS
                build_config["model_name"]["value"] = GOOGLE_GENERATIVE_AI_MODELS[0]
                build_config["api_key"]["display_name"] = "Google API-nyckel"
        elif field_name == "model_name" and field_value.startswith("o1") and self.provider == "OpenAI":
            # Hide system_message for o1 models - currently unsupported
            if "system_message" in build_config:
                build_config["system_message"]["show"] = False
        elif field_name == "model_name" and not field_value.startswith("o1") and "system_message" in build_config:
            build_config["system_message"]["show"] = True
        return build_config

from typing import Any

from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.base.models.openai_constants import (
    OPENAI_CHAT_MODEL_NAMES,
    OPENAI_REASONING_MODEL_NAMES,
)
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import BoolInput, DictInput, DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput
from axiestudio.logging import logger


class OpenAIModelComponent(LCModelComponent):
    display_name = "OpenAI"
    description = "Genererar text med OpenAI LLM:er."
    icon = "OpenAI"
    name = "OpenAIModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            info="Maximalt antal tokens att generera. Sätt till 0 för obegränsade tokens.",
            range_spec=RangeSpec(min=0, max=128000),
        ),
        DictInput(
            name="model_kwargs",
            display_name="Modell-kwargs",
            advanced=True,
            info="Ytterligare nyckelordsargument att skicka till modellen.",
        ),
        BoolInput(
            name="json_mode",
            display_name="JSON-läge",
            advanced=True,
            info="Om True kommer det att mata ut JSON oavsett om ett schema skickas.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=OPENAI_CHAT_MODEL_NAMES + OPENAI_REASONING_MODEL_NAMES,
            value=OPENAI_CHAT_MODEL_NAMES[0],
            combobox=True,
            real_time_refresh=True,
        ),
        StrInput(
            name="openai_api_base",
            display_name="OpenAI API-bas",
            advanced=True,
            info="Bas-URL:en för OpenAI API. "
            "Standard är https://api.openai.com/v1. "
            "Du kan ändra detta för att använda andra API:er som JinaChat, LocalAI och Prem.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="OpenAI API-nyckel",
            info="OpenAI API-nyckeln att använda för OpenAI-modellen.",
            advanced=False,
            value="OPENAI_API_KEY",
            required=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            show=True,
        ),
        IntInput(
            name="seed",
            display_name="Frö",
            info="Fröet kontrollerar reproducerbarheten av jobbet.",
            advanced=True,
            value=1,
        ),
        IntInput(
            name="max_retries",
            display_name="Max återförsök",
            info="Maximalt antal återförsök att göra vid generering.",
            advanced=True,
            value=5,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            info="Timeout för förfrågningar till OpenAI completion API.",
            advanced=True,
            value=700,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        logger.debug(f"Kör förfrågan med modell: {self.model_name}")
        parameters = {
            "api_key": SecretStr(self.api_key).get_secret_value() if self.api_key else None,
            "model_name": self.model_name,
            "max_tokens": self.max_tokens or None,
            "model_kwargs": self.model_kwargs or {},
            "base_url": self.openai_api_base or "https://api.openai.com/v1",
            "max_retries": self.max_retries,
            "timeout": self.timeout,
        }

        # TODO: Återbesök om/när parametrar stöds för resonemangsmodeller
        unsupported_params_for_reasoning_models = ["temperature", "seed"]

        if self.model_name not in OPENAI_REASONING_MODEL_NAMES:
            parameters["temperature"] = self.temperature if self.temperature is not None else 0.1
            parameters["seed"] = self.seed
        else:
            params_str = ", ".join(unsupported_params_for_reasoning_models)
            logger.debug(f"{self.model_name} är en resonemangsmodell, {params_str} är inte konfigurerbara. Ignorerar.")

        output = ChatOpenAI(**parameters)
        if self.json_mode:
            output = output.bind(response_format={"type": "json_object"})

        return output

    def _get_exception_message(self, e: Exception):
        """Get a message from an OpenAI exception.

        Args:
            e (Exception): The exception to get the message from.

        Returns:
            str: The message from the exception.
        """
        try:
            from openai import BadRequestError
        except ImportError:
            return None
        if isinstance(e, BadRequestError):
            message = e.body.get("message")
            if message:
                return message
        return None

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        if field_name in {"base_url", "model_name", "api_key"} and field_value in OPENAI_REASONING_MODEL_NAMES:
            build_config["temperature"]["show"] = False
            build_config["seed"]["show"] = False
            # Hide system_message for o1 models - currently unsupported
            if field_value.startswith("o1") and "system_message" in build_config:
                build_config["system_message"]["show"] = False
        if field_name in {"base_url", "model_name", "api_key"} and field_value in OPENAI_CHAT_MODEL_NAMES:
            build_config["temperature"]["show"] = True
            build_config["seed"]["show"] = True
            if "system_message" in build_config:
                build_config["system_message"]["show"] = True
        return build_config

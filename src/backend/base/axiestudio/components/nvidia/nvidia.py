from typing import Any

from loguru import logger
from requests.exceptions import ConnectionError  # noqa: A004
from urllib3.exceptions import MaxRetryError, NameResolutionError

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import BoolInput, DropdownInput, IntInput, MessageTextInput, SecretStrInput, SliderInput
from axiestudio.schema.dotdict import dotdict


class NVIDIAModelComponent(LCModelComponent):
    display_name = "NVIDIA"
    description = "Genererar text med NVIDIA LLM:er."
    icon = "NVIDIA"

    try:
        import warnings

        # Suppresses repeated warnings about NIM key in langchain_nvidia_ai_endpoints==0.3.8
        warnings.filterwarnings("ignore", category=UserWarning, module="langchain_nvidia_ai_endpoints._common")
        from langchain_nvidia_ai_endpoints import ChatNVIDIA

        all_models = ChatNVIDIA().get_available_models()
    except ImportError as e:
        msg = "Please install langchain-nvidia-ai-endpoints to use the NVIDIA model."
        raise ImportError(msg) from e
    except (ConnectionError, MaxRetryError, NameResolutionError):
        logger.warning(
            "Failed to connect to NVIDIA API. Model list may be unavailable."
            " Please check your internet connection and API credentials."
        )
        all_models = []

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            info="Maximalt antal tokens att generera. Sätt till 0 för obegränsade tokens.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            info="Namnet på NVIDIA-modellen att använda.",
            advanced=False,
            value=None,
            options=[model.id for model in all_models],
            combobox=True,
            refresh_button=True,
        ),
        BoolInput(
            name="detailed_thinking",
            display_name="Detaljerat tänkande",
            info="Om sant kommer modellen att returnera en detaljerad tankeprocess. Stöds endast av resoneringsmodeller.",
            value=False,
            show=False,
        ),
        BoolInput(
            name="tool_model_enabled",
            display_name="Aktivera verktygsmodeller",
            info="Om aktiverad visas endast modeller som stöder verktygsanrop.",
            advanced=False,
            value=False,
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="base_url",
            display_name="NVIDIA bas-URL",
            value="https://integrate.api.nvidia.com/v1",
            info="Bas-URL:en för NVIDIA API. Standard är https://integrate.api.nvidia.com/v1.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="NVIDIA API-nyckel",
            info="NVIDIA API-nyckeln.",
            advanced=False,
            value="NVIDIA_API_KEY",
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            info="Kör inferens med denna temperatur.",
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
        IntInput(
            name="seed",
            display_name="Frö",
            info="Fröet kontrollerar reproducerbarheten av jobbet.",
            advanced=True,
            value=1,
        ),
    ]

    def get_models(self, tool_model_enabled: bool | None = None) -> list[str]:
        try:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
        except ImportError as e:
            msg = "Please install langchain-nvidia-ai-endpoints to use the NVIDIA model."
            raise ImportError(msg) from e

        # Note: don't include the previous model, as it may not exist in available models from the new base url
        model = ChatNVIDIA(base_url=self.base_url, api_key=self.api_key)
        if tool_model_enabled:
            tool_models = [m for m in model.get_available_models() if m.supports_tools]
            return [m.id for m in tool_models]
        return [m.id for m in model.available_models]

    def update_build_config(self, build_config: dotdict, _field_value: Any, field_name: str | None = None):
        if field_name in {"model_name", "tool_model_enabled", "base_url", "api_key"}:
            try:
                ids = self.get_models(self.tool_model_enabled)
                build_config["model_name"]["options"] = ids

                if "value" not in build_config["model_name"] or build_config["model_name"]["value"] is None:
                    build_config["model_name"]["value"] = ids[0]
                elif build_config["model_name"]["value"] not in ids:
                    build_config["model_name"]["value"] = None

                # TODO: use api to determine if model supports detailed thinking
                if build_config["model_name"]["value"] == "nemotron":
                    build_config["detailed_thinking"]["show"] = True
                else:
                    build_config["detailed_thinking"]["value"] = False
                    build_config["detailed_thinking"]["show"] = False
            except Exception as e:
                msg = f"Error getting model names: {e}"
                build_config["model_name"]["value"] = None
                build_config["model_name"]["options"] = []
                raise ValueError(msg) from e

        return build_config

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
        except ImportError as e:
            msg = "Please install langchain-nvidia-ai-endpoints to use the NVIDIA model."
            raise ImportError(msg) from e
        api_key = self.api_key
        temperature = self.temperature
        model_name: str = self.model_name
        max_tokens = self.max_tokens
        seed = self.seed
        return ChatNVIDIA(
            max_tokens=max_tokens or None,
            model=model_name,
            base_url=self.base_url,
            api_key=api_key,
            temperature=temperature or 0.1,
            seed=seed,
        )

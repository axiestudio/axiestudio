import json
from typing import Any

import requests
from langchain_ibm import ChatWatsonx
from loguru import logger
from pydantic.v1 import SecretStr

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import BoolInput, DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput
from axiestudio.schema.dotdict import dotdict


class WatsonxAIComponent(LCModelComponent):
    display_name = "IBM watsonx.ai"
    description = "Generera text med IBM watsonx.ai grundmodeller."
    icon = "WatsonxAI"
    name = "IBMwatsonxModel"
    beta = False

    _default_models = ["ibm/granite-3-2b-instruct", "ibm/granite-3-8b-instruct", "ibm/granite-13b-instruct-v2"]

    inputs = [
        *LCModelComponent._base_inputs,
        DropdownInput(
            name="url",
            display_name="watsonx API-endpoint",
            info="Bas-URL:en för API:et.",
            value=None,
            options=[
                "https://us-south.ml.cloud.ibm.com",
                "https://eu-de.ml.cloud.ibm.com",
                "https://eu-gb.ml.cloud.ibm.com",
                "https://au-syd.ml.cloud.ibm.com",
                "https://jp-tok.ml.cloud.ibm.com",
                "https://ca-tor.ml.cloud.ibm.com",
            ],
            real_time_refresh=True,
        ),
        StrInput(
            name="project_id",
            display_name="watsonx projekt-ID",
            required=True,
            info="Projekt-ID eller distributionsområdes-ID som är associerat med grundmodellen.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            info="API-nyckeln att använda för modellen.",
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            options=[],
            value=None,
            dynamic=True,
            required=True,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            info="Maximalt antal tokens att generera.",
            range_spec=RangeSpec(min=1, max=4096),
            value=1000,
        ),
        StrInput(
            name="stop_sequence",
            display_name="Stoppsekvens",
            advanced=True,
            info="Sekvens där generering ska stoppas.",
            field_type="str",
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            info="Styr slumpmässighet, högre värden ökar mångfalden.",
            value=0.1,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="top_p",
            display_name="Top P",
            info="Den kumulativa sannolikhetsgränsen för tokenval. "
            "Lägre värden betyder sampling från en mindre, mer toppviktad kärna.",
            value=0.9,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="frequency_penalty",
            display_name="Frekvensstraff",
            info="Straff för frekvens av tokenanvändning.",
            value=0.5,
            range_spec=RangeSpec(min=-2.0, max=2.0, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="presence_penalty",
            display_name="Närvarostraff",
            info="Straff för tokennärvaro i tidigare text.",
            value=0.3,
            range_spec=RangeSpec(min=-2.0, max=2.0, step=0.01),
            advanced=True,
        ),
        IntInput(
            name="seed",
            display_name="Slumpmässigt frö",
            advanced=True,
            info="Det slumpmässiga fröet för modellen.",
            value=8,
        ),
        BoolInput(
            name="logprobs",
            display_name="Logg-sannolikheter",
            advanced=True,
            info="Om logg-sannolikheter för utdata-tokens ska returneras.",
            value=True,
        ),
        IntInput(
            name="top_logprobs",
            display_name="Topp logg-sannolikheter",
            advanced=True,
            info="Antal mest sannolika tokens att returnera vid varje position.",
            value=3,
            range_spec=RangeSpec(min=1, max=20),
        ),
        StrInput(
            name="logit_bias",
            display_name="Logit-bias",
            advanced=True,
            info='JSON-sträng med token-ID:n att påverka eller undertrycka (t.ex. {"1003": -100, "1004": 100}).',
            field_type="str",
        ),
    ]

    @staticmethod
    def fetch_models(base_url: str) -> list[str]:
        """Fetch available models from the watsonx.ai API."""
        try:
            endpoint = f"{base_url}/ml/v1/foundation_model_specs"
            params = {"version": "2024-09-16", "filters": "function_text_chat,!lifecycle_withdrawn"}
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            models = [model["model_id"] for model in data.get("resources", [])]
            return sorted(models)
        except Exception:  # noqa: BLE001
            logger.exception("Error fetching models. Using default models.")
            return WatsonxAIComponent._default_models

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        """Update model options when URL or API key changes."""
        logger.info("Updating build config. Field name: %s, Field value: %s", field_name, field_value)

        if field_name == "url" and field_value:
            try:
                models = self.fetch_models(base_url=build_config.url.value)
                build_config.model_name.options = models
                if build_config.model_name.value:
                    build_config.model_name.value = models[0]
                info_message = f"Updated model options: {len(models)} models found in {build_config.url.value}"
                logger.info(info_message)
            except Exception:  # noqa: BLE001
                logger.exception("Error updating model options.")

    def build_model(self) -> LanguageModel:
        # Parse logit_bias from JSON string if provided
        logit_bias = None
        if hasattr(self, "logit_bias") and self.logit_bias:
            try:
                logit_bias = json.loads(self.logit_bias)
            except json.JSONDecodeError:
                logger.warning("Invalid logit_bias JSON format. Using default instead.")
                logit_bias = {"1003": -100, "1004": -100}

        chat_params = {
            "max_tokens": getattr(self, "max_tokens", None),
            "temperature": getattr(self, "temperature", None),
            "top_p": getattr(self, "top_p", None),
            "frequency_penalty": getattr(self, "frequency_penalty", None),
            "presence_penalty": getattr(self, "presence_penalty", None),
            "seed": getattr(self, "seed", None),
            "stop": [self.stop_sequence] if self.stop_sequence else [],
            "n": 1,
            "logprobs": getattr(self, "logprobs", True),
            "top_logprobs": getattr(self, "top_logprobs", None),
            "time_limit": 600000,
            "logit_bias": logit_bias,
        }

        return ChatWatsonx(
            apikey=SecretStr(self.api_key).get_secret_value(),
            url=self.url,
            project_id=self.project_id,
            model_id=self.model_name,
            params=chat_params,
            streaming=self.stream,
        )

import asyncio
from typing import Any
from urllib.parse import urljoin

import httpx
from langchain_ollama import ChatOllama

from axiestudio.base.models.model import LCModelComponent
from axiestudio.base.models.ollama_constants import URL_LIST
from axiestudio.field_typing import LanguageModel
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.io import BoolInput, DictInput, DropdownInput, FloatInput, IntInput, MessageTextInput, SliderInput
from axiestudio.logging import logger

HTTP_STATUS_OK = 200


class ChatOllamaComponent(LCModelComponent):
    display_name = "Ollama"
    description = "Generera text med Ollama lokala LLM:er."
    icon = "Ollama"
    name = "OllamaModel"

    # Define constants for JSON keys
    JSON_MODELS_KEY = "models"
    JSON_NAME_KEY = "name"
    JSON_CAPABILITIES_KEY = "capabilities"
    DESIRED_CAPABILITY = "completion"
    TOOL_CALLING_CAPABILITY = "tools"

    inputs = [
        MessageTextInput(
            name="base_url",
            display_name="Bas-URL",
            info="Endpoint för Ollama API.",
            value="",
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            options=[],
            info="Se https://ollama.com/library för fler modeller.",
            refresh_button=True,
            real_time_refresh=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperatur",
            value=0.1,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
        MessageTextInput(
            name="format", display_name="Format", info="Ange formatet för utdata (t.ex. json).", advanced=True
        ),
        DictInput(name="metadata", display_name="Metadata", info="Metadata att lägga till i körningsspåret.", advanced=True),
        DropdownInput(
            name="mirostat",
            display_name="Mirostat",
            options=["Disabled", "Mirostat", "Mirostat 2.0"],
            info="Aktivera/inaktivera Mirostat-sampling för att kontrollera perplexitet.",
            value="Disabled",
            advanced=True,
            real_time_refresh=True,
        ),
        FloatInput(
            name="mirostat_eta",
            display_name="Mirostat Eta",
            info="Inlärningshastighet för Mirostat-algoritm. (Standard: 0.1)",
            advanced=True,
        ),
        FloatInput(
            name="mirostat_tau",
            display_name="Mirostat Tau",
            info="Styr balansen mellan koherens och mångfald i utdata. (Standard: 5.0)",
            advanced=True,
        ),
        IntInput(
            name="num_ctx",
            display_name="Kontextfönsterstorlek",
            info="Storlek på kontextfönstret för att generera tokens. (Standard: 2048)",
            advanced=True,
        ),
        IntInput(
            name="num_gpu",
            display_name="Antal GPU:er",
            info="Antal GPU:er att använda för beräkning. (Standard: 1 på macOS, 0 för att inaktivera)",
            advanced=True,
        ),
        IntInput(
            name="num_thread",
            display_name="Antal trådar",
            info="Antal trådar att använda under beräkning. (Standard: detekterat för optimal prestanda)",
            advanced=True,
        ),
        IntInput(
            name="repeat_last_n",
            display_name="Upprepa senaste N",
            info="Hur långt tillbaka modellen tittar för att förhindra upprepning. (Standard: 64, 0 = inaktiverad, -1 = num_ctx)",
            advanced=True,
        ),
        FloatInput(
            name="repeat_penalty",
            display_name="Upprepningsstraff",
            info="Straff för upprepningar i genererad text. (Standard: 1.1)",
            advanced=True,
        ),
        FloatInput(name="tfs_z", display_name="TFS Z", info="Tail free sampling-värde. (Standard: 1)", advanced=True),
        IntInput(name="timeout", display_name="Timeout", info="Timeout för förfrågningsströmmen.", advanced=True),
        IntInput(
            name="top_k", display_name="Top K", info="Begränsar tokenval till topp K. (Standard: 40)", advanced=True
        ),
        FloatInput(name="top_p", display_name="Top P", info="Fungerar tillsammans med top-k. (Standard: 0.9)", advanced=True),
        BoolInput(name="verbose", display_name="Utförlig", info="Om svarstext ska skrivas ut.", advanced=True),
        MessageTextInput(
            name="tags",
            display_name="Taggar",
            info="Kommaseparerad lista med taggar att lägga till i körningsspåret.",
            advanced=True,
        ),
        MessageTextInput(
            name="stop_tokens",
            display_name="Stopp-tokens",
            info="Kommaseparerad lista med tokens för att signalera modellen att sluta generera text.",
            advanced=True,
        ),
        MessageTextInput(
            name="system", display_name="System", info="System att använda för att generera text.", advanced=True
        ),
        BoolInput(
            name="tool_model_enabled",
            display_name="Verktygsmodell aktiverad",
            info="Om verktygsanrop ska aktiveras i modellen.",
            value=True,
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="template", display_name="Mall", info="Mall att använda för att generera text.", advanced=True
        ),
        *LCModelComponent._base_inputs,
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        # Mapping mirostat settings to their corresponding values
        mirostat_options = {"Mirostat": 1, "Mirostat 2.0": 2}

        # Default to 0 for 'Disabled'
        mirostat_value = mirostat_options.get(self.mirostat, 0)

        # Set mirostat_eta and mirostat_tau to None if mirostat is disabled
        if mirostat_value == 0:
            mirostat_eta = None
            mirostat_tau = None
        else:
            mirostat_eta = self.mirostat_eta
            mirostat_tau = self.mirostat_tau

        # Mapping system settings to their corresponding values
        llm_params = {
            "base_url": self.base_url,
            "model": self.model_name,
            "mirostat": mirostat_value,
            "format": self.format,
            "metadata": self.metadata,
            "tags": self.tags.split(",") if self.tags else None,
            "mirostat_eta": mirostat_eta,
            "mirostat_tau": mirostat_tau,
            "num_ctx": self.num_ctx or None,
            "num_gpu": self.num_gpu or None,
            "num_thread": self.num_thread or None,
            "repeat_last_n": self.repeat_last_n or None,
            "repeat_penalty": self.repeat_penalty or None,
            "temperature": self.temperature or None,
            "stop": self.stop_tokens.split(",") if self.stop_tokens else None,
            "system": self.system,
            "tfs_z": self.tfs_z or None,
            "timeout": self.timeout or None,
            "top_k": self.top_k or None,
            "top_p": self.top_p or None,
            "verbose": self.verbose,
            "template": self.template,
        }

        # Remove parameters with None values
        llm_params = {k: v for k, v in llm_params.items() if v is not None}

        try:
            output = ChatOllama(**llm_params)
        except Exception as e:
            msg = (
                "Kunde inte ansluta till Ollama API. ",
                "Vänligen verifiera bas-URL:en, säkerställ att relevant Ollama-modell är hämtad, och försök igen.",
            )
            raise ValueError(msg) from e

        return output

    async def is_valid_ollama_url(self, url: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                return (await client.get(urljoin(url, "api/tags"))).status_code == HTTP_STATUS_OK
        except httpx.RequestError:
            return False

    async def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None):
        if field_name == "mirostat":
            if field_value == "Disabled":
                build_config["mirostat_eta"]["advanced"] = True
                build_config["mirostat_tau"]["advanced"] = True
                build_config["mirostat_eta"]["value"] = None
                build_config["mirostat_tau"]["value"] = None

            else:
                build_config["mirostat_eta"]["advanced"] = False
                build_config["mirostat_tau"]["advanced"] = False

                if field_value == "Mirostat 2.0":
                    build_config["mirostat_eta"]["value"] = 0.2
                    build_config["mirostat_tau"]["value"] = 10
                else:
                    build_config["mirostat_eta"]["value"] = 0.1
                    build_config["mirostat_tau"]["value"] = 5

        if field_name in {"base_url", "model_name"}:
            if build_config["base_url"].get("load_from_db", False):
                base_url_value = await self.get_variables(build_config["base_url"].get("value", ""), "base_url")
            else:
                base_url_value = build_config["base_url"].get("value", "")

            if not await self.is_valid_ollama_url(base_url_value):
                # Check if any URL in the list is valid
                valid_url = ""
                check_urls = URL_LIST
                if self.base_url:
                    check_urls = [self.base_url, *URL_LIST]
                for url in check_urls:
                    if await self.is_valid_ollama_url(url):
                        valid_url = url
                        break
                if valid_url != "":
                    build_config["base_url"]["value"] = valid_url
                else:
                    msg = "Ingen giltig Ollama-URL hittades."
                    raise ValueError(msg)
        if field_name in {"model_name", "base_url", "tool_model_enabled"}:
            if await self.is_valid_ollama_url(self.base_url):
                tool_model_enabled = build_config["tool_model_enabled"].get("value", False) or self.tool_model_enabled
                build_config["model_name"]["options"] = await self.get_models(self.base_url, tool_model_enabled)
            elif await self.is_valid_ollama_url(build_config["base_url"].get("value", "")):
                tool_model_enabled = build_config["tool_model_enabled"].get("value", False) or self.tool_model_enabled
                build_config["model_name"]["options"] = await self.get_models(
                    build_config["base_url"].get("value", ""), tool_model_enabled
                )
            else:
                build_config["model_name"]["options"] = []
        if field_name == "keep_alive_flag":
            if field_value == "Keep":
                build_config["keep_alive"]["value"] = "-1"
                build_config["keep_alive"]["advanced"] = True
            elif field_value == "Immediately":
                build_config["keep_alive"]["value"] = "0"
                build_config["keep_alive"]["advanced"] = True
            else:
                build_config["keep_alive"]["advanced"] = False

        return build_config

    async def get_models(self, base_url_value: str, tool_model_enabled: bool | None = None) -> list[str]:
        """Fetches a list of models from the Ollama API that do not have the "embedding" capability.

        Args:
            base_url_value (str): The base URL of the Ollama API.
            tool_model_enabled (bool | None, optional): If True, filters the models further to include
                only those that support tool calling. Defaults to None.

        Returns:
            list[str]: A list of model names that do not have the "embedding" capability. If
                `tool_model_enabled` is True, only models supporting tool calling are included.

        Raises:
            ValueError: If there is an issue with the API request or response, or if the model
                names cannot be retrieved.
        """
        try:
            # Normalize the base URL to avoid the repeated "/" at the end
            base_url = base_url_value.rstrip("/") + "/"

            # Ollama REST API to return models
            tags_url = urljoin(base_url, "api/tags")

            # Ollama REST API to return model capabilities
            show_url = urljoin(base_url, "api/show")

            async with httpx.AsyncClient() as client:
                # Fetch available models
                tags_response = await client.get(tags_url)
                tags_response.raise_for_status()
                models = tags_response.json()
                if asyncio.iscoroutine(models):
                    models = await models
                logger.debug(f"Available models: {models}")

                # Filter models that are NOT embedding models
                model_ids = []
                for model in models[self.JSON_MODELS_KEY]:
                    model_name = model[self.JSON_NAME_KEY]
                    logger.debug(f"Checking model: {model_name}")

                    payload = {"model": model_name}
                    show_response = await client.post(show_url, json=payload)
                    show_response.raise_for_status()
                    json_data = show_response.json()
                    if asyncio.iscoroutine(json_data):
                        json_data = await json_data
                    capabilities = json_data.get(self.JSON_CAPABILITIES_KEY, [])
                    logger.debug(f"Model: {model_name}, Capabilities: {capabilities}")

                    if self.DESIRED_CAPABILITY in capabilities and (
                        not tool_model_enabled or self.TOOL_CALLING_CAPABILITY in capabilities
                    ):
                        model_ids.append(model_name)

        except (httpx.RequestError, ValueError) as e:
            msg = "Kunde inte hämta modellnamn från Ollama."
            raise ValueError(msg) from e

        return model_ids

import httpx
from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.io import (
    BoolInput,
    DropdownInput,
    IntInput,
    MessageTextInput,
    MultilineInput,
    Output,
    SecretStrInput,
)
from axiestudio.schema.data import Data


class AgentQL(Component):
    display_name = "Extrahera webbdata"
    description = "Extraherar strukturerad data från en webbsida med en AgentQL-fråga eller en naturlig språkbeskrivning."
    documentation: str = "https://docs.agentql.com/rest-api/api-reference"
    icon = "AgentQL"
    name = "AgentQL"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            required=True,
            password=True,
            info="Din AgentQL API-nyckel från dev.agentql.com",
        ),
        MessageTextInput(
            name="url",
            display_name="URL",
            required=True,
            info="URL:en för den offentliga webbsidan du vill extrahera data från.",
            tool_mode=True,
        ),
        MultilineInput(
            name="query",
            display_name="AgentQL-fråga",
            required=False,
            info="AgentQL-frågan att utföra. Lär dig mer på https://docs.agentql.com/agentql-query eller använd en prompt.",
            tool_mode=True,
        ),
        MultilineInput(
            name="prompt",
            display_name="Prompt",
            required=False,
            info="En naturlig språkbeskrivning av datan att extrahera från sidan. Alternativ till AgentQL-fråga.",
            tool_mode=True,
        ),
        BoolInput(
            name="is_stealth_mode_enabled",
            display_name="Aktivera smygläge (Beta)",
            info="Aktivera experimentella anti-bot undvikningsstrategier. Kanske inte fungerar för alla webbplatser hela tiden.",
            value=False,
            advanced=True,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            info="Sekunder att vänta på en begäran.",
            value=900,
            advanced=True,
        ),
        DropdownInput(
            name="mode",
            display_name="Begäranläge",
            info="'standard' uses deep data analysis, while 'fast' trades some depth of analysis for speed.",
            options=["fast", "standard"],
            value="fast",
            advanced=True,
        ),
        IntInput(
            name="wait_for",
            display_name="Vänta på",
            info="Sekunder att vänta på att sidan ska laddas innan data extraheras.",
            value=0,
            range_spec=RangeSpec(min=0, max=10, step_type="int"),
            advanced=True,
        ),
        BoolInput(
            name="is_scroll_to_bottom_enabled",
            display_name="Aktivera rullning till botten",
            info="Rulla till botten av sidan innan data extraheras.",
            value=False,
            advanced=True,
        ),
        BoolInput(
            name="is_screenshot_enabled",
            display_name="Aktivera skärmdump",
            info="Ta en skärmdump innan data extraheras. Returneras i 'metadata' som en Base64-sträng.",
            value=False,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="build_output"),
    ]

    def build_output(self) -> Data:
        endpoint = "https://api.agentql.com/v1/query-data"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "X-TF-Request-Origin": "axiestudio",
        }

        payload = {
            "url": self.url,
            "query": self.query,
            "prompt": self.prompt,
            "params": {
                "mode": self.mode,
                "wait_for": self.wait_for,
                "is_scroll_to_bottom_enabled": self.is_scroll_to_bottom_enabled,
                "is_screenshot_enabled": self.is_screenshot_enabled,
            },
            "metadata": {
                "experimental_stealth_mode_enabled": self.is_stealth_mode_enabled,
            },
        }

        if not self.prompt and not self.query:
            self.status = "Either Query or Prompt must be provided."
            raise ValueError(self.status)
        if self.prompt and self.query:
            self.status = "Both Query and Prompt can't be provided at the same time."
            raise ValueError(self.status)

        try:
            response = httpx.post(endpoint, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()

            json = response.json()
            data = Data(result=json["data"], metadata=json["metadata"])

        except httpx.HTTPStatusError as e:
            response = e.response
            if response.status_code == httpx.codes.UNAUTHORIZED:
                self.status = "Please, provide a valid API Key. You can create one at https://dev.agentql.com."
            else:
                try:
                    error_json = response.json()
                    logger.error(
                        f"Failure response: '{response.status_code} {response.reason_phrase}' with body: {error_json}"
                    )
                    msg = error_json["error_info"] if "error_info" in error_json else error_json["detail"]
                except (ValueError, TypeError):
                    msg = f"HTTP {e}."
                self.status = msg
            raise ValueError(self.status) from e

        else:
            self.status = data
            return data

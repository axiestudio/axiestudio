from axiestudio.custom.custom_component.component import Component
from axiestudio.io import (
    MessageTextInput,
    Output,
    SecretStrInput,
)
from axiestudio.schema.data import Data


class ScrapeGraphSearchApi(Component):
    display_name: str = "ScrapeGraph Search API"
    description: str = "Givet en sökprompt returnerar den sökresultat med ScrapeGraphs sökfunktionalitet."
    name = "ScrapeGraphSearchApi"

    documentation: str = "https://docs.scrapegraphai.com/services/searchscraper"
    icon = "ScrapeGraph"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="ScrapeGraph API-nyckel",
            required=True,
            password=True,
            info="API-nyckeln för att använda ScrapeGraph API.",
        ),
        MessageTextInput(
            name="user_prompt",
            display_name="Sökprompt",
            tool_mode=True,
            info="Sökprompten att använda.",
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="search"),
    ]

    def search(self) -> list[Data]:
        try:
            from scrapegraph_py import Client
            from scrapegraph_py.logger import sgai_logger
        except ImportError as e:
            msg = "Could not import scrapegraph-py package. Please install it with `pip install scrapegraph-py`."
            raise ImportError(msg) from e

        # Set logging level
        sgai_logger.set_logging(level="INFO")

        # Initialize the client with API key
        sgai_client = Client(api_key=self.api_key)

        try:
            # SearchScraper request
            response = sgai_client.searchscraper(
                user_prompt=self.user_prompt,
            )

            # Close the client
            sgai_client.close()

            return Data(data=response)
        except Exception:
            sgai_client.close()
            raise

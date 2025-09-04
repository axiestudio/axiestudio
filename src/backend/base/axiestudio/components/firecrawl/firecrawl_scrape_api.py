from axiestudio.custom.custom_component.component import Component
from axiestudio.io import (
    DataInput,
    IntInput,
    MultilineInput,
    Output,
    SecretStrInput,
)
from axiestudio.schema.data import Data


class FirecrawlScrapeApi(Component):
    display_name: str = "Firecrawl Scrape API"
    description: str = "Skrapar en URL och returnerar resultaten."
    name = "FirecrawlScrapeApi"

    documentation: str = "https://docs.firecrawl.dev/api-reference/endpoint/scrape"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            required=True,
            password=True,
            info="API-nyckeln för att använda Firecrawl API.",
        ),
        MultilineInput(
            name="url",
            display_name="URL",
            required=True,
            info="URL:en att skrapa.",
            tool_mode=True,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            info="Timeout i millisekunder för begäran.",
        ),
        DataInput(
            name="scrapeOptions",
            display_name="Skrapningsalternativ",
            info="Sidalternativen att skicka med begäran.",
        ),
        DataInput(
            name="extractorOptions",
            display_name="Extraheringsalternativ",
            info="Extraheringsalternativen att skicka med begäran.",
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="scrape"),
    ]

    def scrape(self) -> Data:
        try:
            from firecrawl import FirecrawlApp
        except ImportError as e:
            msg = "Could not import firecrawl integration package. Please install it with `pip install firecrawl-py`."
            raise ImportError(msg) from e

        params = self.scrapeOptions.__dict__.get("data", {}) if self.scrapeOptions else {}
        extractor_options_dict = self.extractorOptions.__dict__.get("data", {}) if self.extractorOptions else {}
        if extractor_options_dict:
            params["extract"] = extractor_options_dict

        # Set default values for parameters
        params.setdefault("formats", ["markdown"])  # Default output format
        params.setdefault("onlyMainContent", True)  # Default to only main content

        app = FirecrawlApp(api_key=self.api_key)
        results = app.scrape_url(self.url, params=params)
        return Data(data=results)

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import (
    BoolInput,
    MultilineInput,
    Output,
    SecretStrInput,
)
from axiestudio.schema.data import Data


class FirecrawlMapApi(Component):
    display_name: str = "Firecrawl Map API"
    description: str = "Mappar en URL och returnerar resultaten."
    name = "FirecrawlMapApi"

    documentation: str = "https://docs.firecrawl.dev/api-reference/endpoint/map"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            required=True,
            password=True,
            info="API-nyckeln för att använda Firecrawl API.",
        ),
        MultilineInput(
            name="urls",
            display_name="URL:er",
            required=True,
            info="Lista över URL:er att skapa kartor från (separerade med komman eller nya rader).",
            tool_mode=True,
        ),
        BoolInput(
            name="ignore_sitemap",
            display_name="Ignorera sitemap",
            info="När sant kommer sitemap.xml-filen att ignoreras under crawling.",
        ),
        BoolInput(
            name="sitemap_only",
            display_name="Endast sitemap",
            info="När sant kommer endast länkar som finns i sitemapen att returneras.",
        ),
        BoolInput(
            name="include_subdomains",
            display_name="Inkludera subdomäner",
            info="När sant kommer även subdomäner för den angivna URL:en att skannas.",
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="map"),
    ]

    def map(self) -> Data:
        try:
            from firecrawl import FirecrawlApp
        except ImportError as e:
            msg = "Could not import firecrawl integration package. Please install it with `pip install firecrawl-py`."
            raise ImportError(msg) from e

        # Validate URLs
        if not self.urls:
            msg = "URLs are required"
            raise ValueError(msg)

        # Split and validate URLs (handle both commas and newlines)
        urls = [url.strip() for url in self.urls.replace("\n", ",").split(",") if url.strip()]
        if not urls:
            msg = "No valid URLs provided"
            raise ValueError(msg)

        params = {
            "ignoreSitemap": self.ignore_sitemap,
            "sitemapOnly": self.sitemap_only,
            "includeSubdomains": self.include_subdomains,
        }

        app = FirecrawlApp(api_key=self.api_key)

        # Map all provided URLs and combine results
        combined_links = []
        for url in urls:
            result = app.map_url(url, params=params)
            if isinstance(result, dict) and "links" in result:
                combined_links.extend(result["links"])

        map_result = {"success": True, "links": combined_links}

        return Data(data=map_result)

import pandas as pd
import requests
from bs4 import BeautifulSoup

from axiestudio.custom import Component
from axiestudio.io import IntInput, MessageTextInput, Output
from axiestudio.logging import logger
from axiestudio.schema import DataFrame


class RSSReaderComponent(Component):
    display_name = "RSS-läsare"
    description = "Hämtar och tolkar en RSS-feed."
    documentation: str = "https://docs.axiestudio.org/components-data#rss-reader"
    icon = "rss"
    name = "RSSReaderSimple"

    inputs = [
        MessageTextInput(
            name="rss_url",
            display_name="RSS-feed URL",
            info="URL för RSS-feeden att tolka.",
            tool_mode=True,
            required=True,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            info="Timeout för RSS-feed-förfrågan.",
            value=5,
            advanced=True,
        ),
    ]

    outputs = [Output(name="articles", display_name="Artiklar", method="read_rss")]

    def read_rss(self) -> DataFrame:
        try:
            response = requests.get(self.rss_url, timeout=self.timeout)
            response.raise_for_status()
            if not response.content.strip():
                msg = "Tomt svar mottaget"
                raise ValueError(msg)
            # Check if the response is valid XML
            try:
                BeautifulSoup(response.content, "xml")
            except Exception as e:
                msg = f"Ogiltigt XML-svar: {e}"
                raise ValueError(msg) from e
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
        except (requests.RequestException, ValueError) as e:
            self.status = f"Misslyckades att hämta RSS: {e}"
            return DataFrame(pd.DataFrame([{"title": "Fel", "link": "", "published": "", "summary": str(e)}]))

        articles = [
            {
                "title": item.title.text if item.title else "",
                "link": item.link.text if item.link else "",
                "published": item.pubDate.text if item.pubDate else "",
                "summary": item.description.text if item.description else "",
            }
            for item in items
        ]

        # Ensure the DataFrame has the correct columns even if empty
        df_articles = pd.DataFrame(articles, columns=["title", "link", "published", "summary"])
        logger.info(f"Hämtade {len(df_articles)} artiklar.")
        return DataFrame(df_articles)

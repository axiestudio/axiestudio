import re
from urllib.parse import parse_qs, unquote, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from axiestudio.custom import Component
from axiestudio.io import IntInput, MessageTextInput, Output
from axiestudio.schema import DataFrame
from axiestudio.services.deps import get_settings_service


class WebSearchComponent(Component):
    display_name = "Webbsökning"
    description = "Utför en grundläggande DuckDuckGo-sökning (HTML-skrapning). Kan vara föremål för hastighetsbegränsningar."
    documentation: str = "https://docs.axiestudio.org/components-data#web-search"
    icon = "search"
    name = "WebSearchNoAPI"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="Sökfråga",
            info="Nyckelord att söka efter.",
            tool_mode=True,
            required=True,
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            info="Timeout för webbsökningsförfrågan.",
            value=5,
            advanced=True,
        ),
    ]

    outputs = [Output(name="results", display_name="Sökresultat", method="perform_search")]

    def validate_url(self, string: str) -> bool:
        url_regex = re.compile(
            r"^(https?:\/\/)?" r"(www\.)?" r"([a-zA-Z0-9.-]+)" r"(\.[a-zA-Z]{2,})?" r"(:\d+)?" r"(\/[^\s]*)?$",
            re.IGNORECASE,
        )
        return bool(url_regex.match(string))

    def ensure_url(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if not self.validate_url(url):
            msg = f"Ogiltig URL: {url}"
            raise ValueError(msg)
        return url

    def _sanitize_query(self, query: str) -> str:
        """Sanitize search query."""
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\']', "", query.strip())

    def perform_search(self) -> DataFrame:
        query = self._sanitize_query(self.query)
        if not query:
            msg = "Tom sökfråga"
            raise ValueError(msg)
        headers = {"User-Agent": get_settings_service().settings.user_agent}
        params = {"q": query, "kl": "us-en"}
        url = "https://html.duckduckgo.com/html/"

        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            self.status = f"Misslyckad förfrågan: {e!s}"
            return DataFrame(pd.DataFrame([{"title": "Fel", "link": "", "snippet": str(e), "content": ""}]))

        if not response.text or "text/html" not in response.headers.get("content-type", "").lower():
            self.status = "Inga resultat hittades"
            return DataFrame(
                pd.DataFrame([{"title": "Fel", "link": "", "snippet": "Inga resultat hittades", "content": ""}])
            )
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select("div.result"):
            title_tag = result.select_one("a.result__a")
            snippet_tag = result.select_one("a.result__snippet")
            if title_tag:
                raw_link = title_tag.get("href", "")
                parsed = urlparse(raw_link)
                uddg = parse_qs(parsed.query).get("uddg", [""])[0]
                decoded_link = unquote(uddg) if uddg else raw_link

                try:
                    final_url = self.ensure_url(decoded_link)
                    page = requests.get(final_url, headers=headers, timeout=self.timeout)
                    page.raise_for_status()
                    content = BeautifulSoup(page.text, "lxml").get_text(separator=" ", strip=True)
                except requests.RequestException as e:
                    final_url = decoded_link
                    content = f"(Misslyckades att hämta: {e!s}"

                results.append(
                    {
                        "title": title_tag.get_text(strip=True),
                        "link": final_url,
                        "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
                        "content": content,
                    }
                )

        df_results = pd.DataFrame(results)
        return DataFrame(df_results)

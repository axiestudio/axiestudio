from langchain_core.tools import tool
from metaphor_python import Metaphor

from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing import Tool
from axiestudio.io import BoolInput, IntInput, Output, SecretStrInput


class ExaSearchToolkit(Component):
    display_name = "Exa-sökning"
    description = "Exa Search-verktygsuppsättning för sökning och innehållshämtning"
    documentation = "https://python.langchain.com/docs/integrations/tools/metaphor_search"
    beta = True
    name = "ExaSearch"
    icon = "ExaSearch"

    inputs = [
        SecretStrInput(
            name="metaphor_api_key",
            display_name="Exa Search API-nyckel",
            password=True,
        ),
        BoolInput(
            name="use_autoprompt",
            display_name="Använd automatisk prompt",
            value=True,
        ),
        IntInput(
            name="search_num_results",
            display_name="Antal sökresultat",
            value=5,
        ),
        IntInput(
            name="similar_num_results",
            display_name="Antal liknande resultat",
            value=5,
        ),
    ]

    outputs = [
        Output(name="tools", display_name="Verktyg", method="build_toolkit"),
    ]

    def build_toolkit(self) -> Tool:
        client = Metaphor(api_key=self.metaphor_api_key)

        @tool
        def search(query: str):
            """Anropa sökmotor med en fråga."""
            return client.search(query, use_autoprompt=self.use_autoprompt, num_results=self.search_num_results)

        @tool
        def get_contents(ids: list[str]):
            """Hämta innehåll från en webbsida.

            ID:na som skickas in ska vara en lista med ID:n som hämtats från `search`.
            """
            return client.get_contents(ids)

        @tool
        def find_similar(url: str):
            """Hämta sökresultat liknande en given URL.

            URL:en som skickas in ska vara en URL returnerad från `search`
            """
            return client.find_similar(url, num_results=self.similar_num_results)

        return [search, get_contents, find_similar]

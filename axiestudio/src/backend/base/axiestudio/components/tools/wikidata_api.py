from typing import Any

import httpx
from langchain_core.tools import StructuredTool, ToolException
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import MultilineInput
from axiestudio.schema.data import Data


class WikidataSearchSchema(BaseModel):
    query: str = Field(..., description="Sökfrågan för Wikidata")


class WikidataAPIWrapper(BaseModel):
    """Wrapper runt Wikidata API."""

    wikidata_api_url: str = "https://www.wikidata.org/w/api.php"

    def results(self, query: str) -> list[dict[str, Any]]:
        # Define request parameters for Wikidata API
        params = {
            "action": "wbsearchentities",
            "format": "json",
            "search": query,
            "language": "en",
        }

        # Send request to Wikidata API
        response = httpx.get(self.wikidata_api_url, params=params)
        response.raise_for_status()
        response_json = response.json()

        # Extract and return search results
        return response_json.get("search", [])

    def run(self, query: str) -> list[dict[str, Any]]:
        try:
            results = self.results(query)
            if results:
                return results

            error_message = "Inga sökresultat hittades för den angivna frågan."

            raise ToolException(error_message)

        except Exception as e:
            error_message = f"Fel i Wikidata Search API: {e!s}"

            raise ToolException(error_message) from e


class WikidataAPIComponent(LCToolComponent):
    display_name = "Wikidata API [Föråldrad]"
    description = "Utför en sökning med Wikidata API."
    name = "WikidataAPI"
    icon = "Wikipedia"
    legacy = True

    inputs = [
        MultilineInput(
            name="query",
            display_name="Fråga",
            info="Textfrågan för likhetssökning på Wikidata.",
            required=True,
        ),
    ]

    def build_tool(self) -> Tool:
        wrapper = WikidataAPIWrapper()

        # Define the tool using StructuredTool and wrapper's run method
        tool = StructuredTool.from_function(
            name="wikidata_search_api",
            description="Utför likhetssökning på Wikidata API",
            func=wrapper.run,
            args_schema=WikidataSearchSchema,
        )

        self.status = "Wikidata Search API-verktyg för Langchain"

        return tool

    def run_model(self) -> list[Data]:
        tool = self.build_tool()

        results = tool.run({"query": self.query})

        # Transform the API response into Data objects
        data = [
            Data(
                text=result["label"],
                metadata=result,
            )
            for result in results
        ]

        self.status = data  # type: ignore[assignment]

        return data

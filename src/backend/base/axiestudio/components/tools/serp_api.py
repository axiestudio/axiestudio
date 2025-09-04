from typing import Any

from langchain.tools import StructuredTool
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain_core.tools import ToolException
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import DictInput, IntInput, MultilineInput, SecretStrInput
from axiestudio.schema.data import Data


class SerpAPISchema(BaseModel):
    """Schema för SerpAPI sökparametrar."""

    query: str = Field(..., description="Sökfrågan")
    params: dict[str, Any] | None = Field(
        default={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        },
        description="Ytterligare sökparametrar",
    )
    max_results: int = Field(5, description="Maximalt antal resultat att returnera")
    max_snippet_length: int = Field(100, description="Maximal längd på varje resultatutdrag")


class SerpAPIComponent(LCToolComponent):
    display_name = "Serp Search API [FÖRÅLDRAD]"
    description = "Anropa Serp Search API med resultatbegränsning"
    name = "SerpAPI"
    icon = "SerpSearch"
    legacy = True

    inputs = [
        SecretStrInput(name="serpapi_api_key", display_name="SerpAPI API-nyckel", required=True),
        MultilineInput(
            name="input_value",
            display_name="Indata",
        ),
        DictInput(name="search_params", display_name="Parametrar", advanced=True, is_list=True),
        IntInput(name="max_results", display_name="Max resultat", value=5, advanced=True),
        IntInput(name="max_snippet_length", display_name="Max utdragslängd", value=100, advanced=True),
    ]

    def _build_wrapper(self, params: dict[str, Any] | None = None) -> SerpAPIWrapper:
        """Bygg en SerpAPIWrapper med de angivna parametrarna."""
        params = params or {}
        if params:
            return SerpAPIWrapper(
                serpapi_api_key=self.serpapi_api_key,
                params=params,
            )
        return SerpAPIWrapper(serpapi_api_key=self.serpapi_api_key)

    def build_tool(self) -> Tool:
        wrapper = self._build_wrapper(self.search_params)

        def search_func(
            query: str, params: dict[str, Any] | None = None, max_results: int = 5, max_snippet_length: int = 100
        ) -> list[dict[str, Any]]:
            try:
                local_wrapper = wrapper
                if params:
                    local_wrapper = self._build_wrapper(params)

                full_results = local_wrapper.results(query)
                organic_results = full_results.get("organic_results", [])[:max_results]

                limited_results = []
                for result in organic_results:
                    limited_result = {
                        "title": result.get("title", "")[:max_snippet_length],
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", "")[:max_snippet_length],
                    }
                    limited_results.append(limited_result)

            except Exception as e:
                error_message = f"Fel i SerpAPI-sökning: {e!s}"
                logger.debug(error_message)
                raise ToolException(error_message) from e
            return limited_results

        tool = StructuredTool.from_function(
            name="serp_search_api",
            description="Sök efter senaste resultat med SerpAPI med resultatbegränsning",
            func=search_func,
            args_schema=SerpAPISchema,
        )

        self.status = "SerpAPI-verktyg skapat"
        return tool

    def run_model(self) -> list[Data]:
        tool = self.build_tool()
        try:
            results = tool.run(
                {
                    "query": self.input_value,
                    "params": self.search_params or {},
                    "max_results": self.max_results,
                    "max_snippet_length": self.max_snippet_length,
                }
            )

            data_list = [Data(data=result, text=result.get("snippet", "")) for result in results]

        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Fel vid körning av SerpAPI")
            self.status = f"Fel: {e}"
            return [Data(data={"error": str(e)}, text=str(e))]

        self.status = data_list  # type: ignore[assignment]
        return data_list

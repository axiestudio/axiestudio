from typing import Any

from langchain.tools import StructuredTool
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import (
    DictInput,
    DropdownInput,
    IntInput,
    MultilineInput,
    SecretStrInput,
)
from axiestudio.schema.data import Data


class QuerySchema(BaseModel):
    query: str = Field(..., description="Frågan att söka efter.")
    query_type: str = Field(
        "search",
        description="Typen av sökning att utföra (t.ex. 'news' eller 'search').",
    )
    k: int = Field(4, description="Antalet resultat att returnera.")
    query_params: dict[str, Any] = Field({}, description="Ytterligare frågeparametrar att skicka till API:et.")


class GoogleSerperAPIComponent(LCToolComponent):
    display_name = "Google Serper API [FÖRÅLDRAD]"
    description = "Anropa Serper.dev Google Search API."
    name = "GoogleSerperAPI"
    icon = "Google"
    legacy = True
    inputs = [
        SecretStrInput(name="serper_api_key", display_name="Serper API-nyckel", required=True),
        MultilineInput(
            name="query",
            display_name="Fråga",
        ),
        IntInput(name="k", display_name="Antal resultat", value=4, required=True),
        DropdownInput(
            name="query_type",
            display_name="Frågetyp",
            required=False,
            options=["news", "search"],
            value="search",
        ),
        DictInput(
            name="query_params",
            display_name="Frågeparametrar",
            required=False,
            value={
                "gl": "us",
                "hl": "en",
            },
            list=True,
        ),
    ]

    def run_model(self) -> Data | list[Data]:
        wrapper = self._build_wrapper(self.k, self.query_type, self.query_params)
        results = wrapper.results(query=self.query)

        # Adjust the extraction based on the `type`
        if self.query_type == "search":
            list_results = results.get("organic", [])
        elif self.query_type == "news":
            list_results = results.get("news", [])
        else:
            list_results = []

        data_list = []
        for result in list_results:
            result["text"] = result.pop("snippet", "")
            data_list.append(Data(data=result))
        self.status = data_list
        return data_list

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="google_search",
            description="Sök på Google efter senaste resultat.",
            func=self._search,
            args_schema=self.QuerySchema,
        )

    def _build_wrapper(
        self,
        k: int = 5,
        query_type: str = "search",
        query_params: dict | None = None,
    ) -> GoogleSerperAPIWrapper:
        wrapper_args = {
            "serper_api_key": self.serper_api_key,
            "k": k,
            "type": query_type,
        }

        # Add query_params if provided
        if query_params:
            wrapper_args.update(query_params)  # Merge with additional query params

        # Dynamically pass parameters to the wrapper
        return GoogleSerperAPIWrapper(**wrapper_args)

    def _search(
        self,
        query: str,
        k: int = 5,
        query_type: str = "search",
        query_params: dict | None = None,
    ) -> dict:
        wrapper = self._build_wrapper(k, query_type, query_params)
        return wrapper.results(query=query)

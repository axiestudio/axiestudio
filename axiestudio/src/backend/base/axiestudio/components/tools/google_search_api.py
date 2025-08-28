from langchain_core.tools import Tool

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.inputs.inputs import IntInput, MultilineInput, SecretStrInput
from axiestudio.schema.data import Data


class GoogleSearchAPIComponent(LCToolComponent):
    display_name = "Google Search API [FÖRÅLDRAD]"
    description = "Anropa Google Search API."
    name = "GoogleSearchAPI"
    icon = "Google"
    legacy = True
    inputs = [
        SecretStrInput(name="google_api_key", display_name="Google API-nyckel", required=True),
        SecretStrInput(name="google_cse_id", display_name="Google CSE-ID", required=True),
        MultilineInput(
            name="input_value",
            display_name="Indata",
        ),
        IntInput(name="k", display_name="Antal resultat", value=4, required=True),
    ]

    def run_model(self) -> Data | list[Data]:
        wrapper = self._build_wrapper()
        results = wrapper.results(query=self.input_value, num_results=self.k)
        data = [Data(data=result, text=result["snippet"]) for result in results]
        self.status = data
        return data

    def build_tool(self) -> Tool:
        wrapper = self._build_wrapper()
        return Tool(
            name="google_search",
            description="Sök på Google efter senaste resultat.",
            func=wrapper.run,
        )

    def _build_wrapper(self):
        try:
            from langchain_google_community import GoogleSearchAPIWrapper
        except ImportError as e:
            msg = "Vänligen installera langchain-google-community för att använda GoogleSearchAPIWrapper."
            raise ImportError(msg) from e
        return GoogleSearchAPIWrapper(google_api_key=self.google_api_key, google_cse_id=self.google_cse_id, k=self.k)

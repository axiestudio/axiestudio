from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import MultilineInput, SecretStrInput
from axiestudio.io import Output
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame


class WolframAlphaAPIComponent(LCToolComponent):
    display_name = "WolframAlpha API"
    description = """Möjliggör frågor till WolframAlpha för beräkningsdata, fakta och beräkningar inom olika \
ämnen, levererar strukturerade svar."""
    name = "WolframAlphaAPI"

    outputs = [
        Output(display_name="DataFrame", name="dataframe", method="fetch_content_dataframe"),
    ]

    inputs = [
        MultilineInput(
            name="input_value", display_name="Inmatningsfråga", info="Exempelfråga: 'Vad är befolkningen i Frankrike?'"
        ),
        SecretStrInput(name="app_id", display_name="App-ID", required=True),
    ]

    icon = "WolframAlphaAPI"

    def run_model(self) -> DataFrame:
        return self.fetch_content_dataframe()

    def build_tool(self) -> Tool:
        wrapper = self._build_wrapper()
        return Tool(name="wolfram_alpha_api", description="Svarar på matematiska frågor.", func=wrapper.run)

    def _build_wrapper(self) -> WolframAlphaAPIWrapper:
        return WolframAlphaAPIWrapper(wolfram_alpha_appid=self.app_id)

    def fetch_content(self) -> list[Data]:
        wrapper = self._build_wrapper()
        result_str = wrapper.run(self.input_value)
        data = [Data(text=result_str)]
        self.status = data
        return data

    def fetch_content_dataframe(self) -> DataFrame:
        """Omvandla WolframAlpha-resultaten till en DataFrame.

        Returns:
            DataFrame: En DataFrame som innehåller frågeresultaten.
        """
        data = self.fetch_content()
        return DataFrame(data)

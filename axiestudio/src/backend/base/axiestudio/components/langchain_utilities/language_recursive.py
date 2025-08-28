from typing import Any

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter, TextSplitter

from axiestudio.base.textsplitters.model import LCTextSplitterComponent
from axiestudio.inputs.inputs import DataInput, DropdownInput, IntInput


class LanguageRecursiveTextSplitterComponent(LCTextSplitterComponent):
    display_name: str = "Språkrekursiv textdelare"
    description: str = "Dela upp text i delar av angiven längd baserat på språk."
    documentation: str = "https://docs.axiestudio.se/components"
    name = "LanguageRecursiveTextSplitter"
    icon = "LangChain"

    inputs = [
        IntInput(
            name="chunk_size",
            display_name="Chunk-storlek",
            info="Den maximala längden för varje chunk.",
            value=1000,
        ),
        IntInput(
            name="chunk_overlap",
            display_name="Chunk-överlappning",
            info="Mängden överlappning mellan chunks.",
            value=200,
        ),
        DataInput(
            name="data_input",
            display_name="Indata",
            info="Texterna att dela upp.",
            input_types=["Document", "Data"],
            required=True,
        ),
        DropdownInput(
            name="code_language", display_name="Kodspråk", options=[x.value for x in Language], value="python"
        ),
    ]

    def get_data_input(self) -> Any:
        return self.data_input

    def build_text_splitter(self) -> TextSplitter:
        return RecursiveCharacterTextSplitter.from_language(
            language=Language(self.code_language),
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

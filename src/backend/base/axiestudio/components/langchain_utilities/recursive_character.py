from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from axiestudio.base.textsplitters.model import LCTextSplitterComponent
from axiestudio.inputs.inputs import DataInput, IntInput, MessageTextInput
from axiestudio.utils.util import unescape_string


class RecursiveCharacterTextSplitterComponent(LCTextSplitterComponent):
    display_name: str = "Rekursiv tecken textdelare"
    description: str = "Dela upp text och försök hålla all relaterad text tillsammans."
    documentation: str = "https://docs.axiestudio.se/components"
    name = "RecursiveCharacterTextSplitter"
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
        MessageTextInput(
            name="separators",
            display_name="Avgränsare",
            info='Tecknen att dela på.\nOm lämnas tomt används standard ["\\n\\n", "\\n", " ", ""].',
            is_list=True,
        ),
    ]

    def get_data_input(self) -> Any:
        return self.data_input

    def build_text_splitter(self) -> TextSplitter:
        if not self.separators:
            separators: list[str] | None = None
        else:
            # check if the separators list has escaped characters
            # if there are escaped characters, unescape them
            separators = [unescape_string(x) for x in self.separators]

        return RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

from typing import Any

from langchain_text_splitters import CharacterTextSplitter, TextSplitter

from axiestudio.base.textsplitters.model import LCTextSplitterComponent
from axiestudio.inputs.inputs import DataInput, IntInput, MessageTextInput
from axiestudio.utils.util import unescape_string


class CharacterTextSplitterComponent(LCTextSplitterComponent):
    display_name = "Tecken textdelare"
    description = "Dela upp text efter antal tecken."
    documentation = "https://docs.axiestudio.org/components/text-splitters#charactertextsplitter"
    name = "CharacterTextSplitter"
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
            name="separator",
            display_name="Avgränsare",
            info='Tecknen att dela på.\nOm lämnas tomt används standard "\\n\\n".',
        ),
    ]

    def get_data_input(self) -> Any:
        return self.data_input

    def build_text_splitter(self) -> TextSplitter:
        separator = unescape_string(self.separator) if self.separator else "\n\n"
        return CharacterTextSplitter(
            chunk_overlap=self.chunk_overlap,
            chunk_size=self.chunk_size,
            separator=separator,
        )

from typing import Any

from langchain_text_splitters import NLTKTextSplitter, TextSplitter

from axiestudio.base.textsplitters.model import LCTextSplitterComponent
from axiestudio.inputs.inputs import DataInput, IntInput, MessageTextInput
from axiestudio.utils.util import unescape_string


class NaturalLanguageTextSplitterComponent(LCTextSplitterComponent):
    display_name = "Naturligt språk textdelare"
    description = "Dela upp text baserat på naturliga språkgränser, optimerad för ett specificerat språk."
    documentation = (
        "https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/split_by_token/#nltk"
    )
    name = "NaturalLanguageTextSplitter"
    icon = "LangChain"
    inputs = [
        IntInput(
            name="chunk_size",
            display_name="Chunk-storlek",
            info="Det maximala antalet tecken i varje chunk efter delning.",
            value=1000,
        ),
        IntInput(
            name="chunk_overlap",
            display_name="Chunk-överlappning",
            info="Antalet tecken som överlappar mellan efterföljande chunks.",
            value=200,
        ),
        DataInput(
            name="data_input",
            display_name="Indata",
            info="Textdata att dela upp.",
            input_types=["Document", "Data"],
            required=True,
        ),
        MessageTextInput(
            name="separator",
            display_name="Avgränsare",
            info='Tecknet (er) att använda som avgränsare vid delning av text.\nStandard är "\\n\\n" om lämnas tomt.',
        ),
        MessageTextInput(
            name="language",
            display_name="Språk",
            info='Språket för texten. Standard är "engelska". '
            "Stöder flera språk för bättre textgränsigenkänning.",
        ),
    ]

    def get_data_input(self) -> Any:
        return self.data_input

    def build_text_splitter(self) -> TextSplitter:
        separator = unescape_string(self.separator) if self.separator else "\n\n"
        return NLTKTextSplitter(
            language=self.language.lower() if self.language else "english",
            separator=separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

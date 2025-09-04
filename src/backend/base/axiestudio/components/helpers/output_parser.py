from langchain_core.output_parsers import CommaSeparatedListOutputParser

from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing.constants import OutputParser
from axiestudio.io import DropdownInput, Output
from axiestudio.schema.message import Message


class OutputParserComponent(Component):
    display_name = "Utdatatolk"
    description = "Transformerar utdatan från en LLM till ett specificerat format."
    icon = "type"
    name = "OutputParser"
    legacy = True

    inputs = [
        DropdownInput(
            name="parser_type",
            display_name="Tolk",
            options=["CSV"],
            value="CSV",
        ),
    ]

    outputs = [
        Output(
            display_name="Formatinstruktioner",
            name="format_instructions",
            info="Skicka till en promptmall för att inkludera formatinstruktioner för LLM-svar.",
            method="format_instructions",
        ),
        Output(display_name="Utdatatolk", name="output_parser", method="build_parser"),
    ]

    def build_parser(self) -> OutputParser:
        if self.parser_type == "CSV":
            return CommaSeparatedListOutputParser()
        msg = "Ej stödd eller saknad tolk"
        raise ValueError(msg)

    def format_instructions(self) -> Message:
        if self.parser_type == "CSV":
            return Message(text=CommaSeparatedListOutputParser().get_format_instructions())
        msg = "Ej stödd eller saknad tolk"
        raise ValueError(msg)

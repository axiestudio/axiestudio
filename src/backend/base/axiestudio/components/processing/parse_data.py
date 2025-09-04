from axiestudio.custom.custom_component.component import Component
from axiestudio.helpers.data import data_to_text, data_to_text_list
from axiestudio.io import DataInput, MultilineInput, Output, StrInput
from axiestudio.schema.data import Data
from axiestudio.schema.message import Message


class ParseDataComponent(Component):
    display_name = "Data till meddelande"
    description = "Konvertera Data-objekt till meddelanden med valfritt {field_name} från indata."
    icon = "message-square"
    name = "ParseData"
    legacy = True
    metadata = {
        "legacy_name": "Parse Data",
    }

    inputs = [
        DataInput(
            name="data",
            display_name="Data",
            info="Datan att konvertera till text.",
            is_list=True,
            required=True,
        ),
        MultilineInput(
            name="template",
            display_name="Mall",
            info="Mallen att använda för formatering av datan. "
            "Den kan innehålla nycklarna {text}, {data} eller någon annan nyckel i Data.",
            value="{text}",
            required=True,
        ),
        StrInput(name="sep", display_name="Avgränsare", advanced=True, value="\n"),
    ]

    outputs = [
        Output(
            display_name="Meddelande",
            name="text",
            info="Data som ett enda meddelande, med varje indata-Data separerad av avgränsare",
            method="parse_data",
        ),
        Output(
            display_name="Datalista",
            name="data_list",
            info="Data som en lista av ny Data, var och en med `text` formaterad av mall",
            method="parse_data_as_list",
        ),
    ]

    def _clean_args(self) -> tuple[list[Data], str, str]:
        data = self.data if isinstance(self.data, list) else [self.data]
        template = self.template
        sep = self.sep
        return data, template, sep

    def parse_data(self) -> Message:
        data, template, sep = self._clean_args()
        result_string = data_to_text(template, data, sep)
        self.status = result_string
        return Message(text=result_string)

    def parse_data_as_list(self) -> list[Data]:
        data, template, _ = self._clean_args()
        text_list, data_list = data_to_text_list(template, data)
        for item, text in zip(data_list, text_list, strict=True):
            item.set_text(text)
        self.status = data_list
        return data_list

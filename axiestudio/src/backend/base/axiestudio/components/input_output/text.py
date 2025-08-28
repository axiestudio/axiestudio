from axiestudio.base.io.text import TextComponent
from axiestudio.io import MultilineInput, Output
from axiestudio.schema.message import Message


class TextInputComponent(TextComponent):
    display_name = "Textinmatning"
    description = "Hämta användartextinmatningar."
    documentation: str = "https://docs.axiestudio.org/components-io#text-input"
    icon = "type"
    name = "TextInput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Text",
            info="Text som ska skickas som inmatning.",
        ),
    ]
    outputs = [
        Output(display_name="Utmatningstext", name="text", method="text_response"),
    ]

    def text_response(self) -> Message:
        return Message(
            text=self.input_value,
        )

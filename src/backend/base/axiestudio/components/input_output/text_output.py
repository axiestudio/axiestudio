from axiestudio.base.io.text import TextComponent
from axiestudio.io import MultilineInput, Output
from axiestudio.schema.message import Message


class TextOutputComponent(TextComponent):
    display_name = "Textutmatning"
    description = "Skickar textutmatning via API."
    documentation: str = "https://docs.axiestudio.org/components-io#text-output"
    icon = "type"
    name = "TextOutput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Inmatningar",
            info="Text som ska skickas som utmatning.",
        ),
    ]
    outputs = [
        Output(display_name="Utmatningstext", name="text", method="text_response"),
    ]

    def text_response(self) -> Message:
        message = Message(
            text=self.input_value,
        )
        self.status = self.input_value
        return message

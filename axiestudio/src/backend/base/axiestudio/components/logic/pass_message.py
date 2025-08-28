from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageInput
from axiestudio.schema.message import Message
from axiestudio.template.field.base import Output


class PassMessageComponent(Component):
    display_name = "Vidarebefordra"
    description = "Vidarebefordrar inmatningsmeddelandet, oförändrat."
    name = "Pass"
    icon = "arrow-right"
    legacy: bool = True

    inputs = [
        MessageInput(
            name="input_message",
            display_name="Inmatningsmeddelande",
            info="Meddelandet som ska vidarebefordras.",
            required=True,
        ),
        MessageInput(
            name="ignored_message",
            display_name="Ignorerat meddelande",
            info="Ett andra meddelande som ska ignoreras. Används som en lösning för kontinuitet.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Utmatningsmeddelande", name="output_message", method="pass_message"),
    ]

    def pass_message(self) -> Message:
        self.status = self.input_message
        return self.input_message

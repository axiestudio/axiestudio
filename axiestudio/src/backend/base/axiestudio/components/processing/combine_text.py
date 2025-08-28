from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema.message import Message


class CombineTextComponent(Component):
    display_name = "Kombinera text"
    description = "Sammanfoga två textkällor till en enda textbit med en angiven avgränsare."
    icon = "merge"
    name = "CombineText"
    legacy: bool = True

    inputs = [
        MessageTextInput(
            name="text1",
            display_name="Första texten",
            info="Den första textinmatningen att sammanfoga.",
        ),
        MessageTextInput(
            name="text2",
            display_name="Andra texten",
            info="Den andra textinmatningen att sammanfoga.",
        ),
        MessageTextInput(
            name="delimiter",
            display_name="Avgränsare",
            info="En sträng som används för att separera de två textinmatningarna. Standard är ett mellanslag.",
            value=" ",
        ),
    ]

    outputs = [
        Output(display_name="Kombinerad text", name="combined_text", method="combine_texts"),
    ]

    def combine_texts(self) -> Message:
        combined = self.delimiter.join([self.text1, self.text2])
        self.status = combined
        return Message(text=combined)

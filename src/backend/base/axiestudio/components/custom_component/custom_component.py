# from axiestudio.field_typing import Data
from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema.data import Data


class CustomComponent(Component):
    display_name = "Anpassad komponent"
    description = "Använd som mall för att skapa din egen komponent."
    documentation: str = "https://docs.axiestudio.org/components-custom-components"
    icon = "code"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="Inmatningsvärde",
            info="Detta är en anpassad komponentinmatning",
            value="Hello, World!",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Utmatning", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        data = Data(value=self.input_value)
        self.status = data
        return data

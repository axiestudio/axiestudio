import os

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import StrInput
from axiestudio.schema.message import Message
from axiestudio.template.field.base import Output


class GetEnvVar(Component):
    display_name = "Hämta miljövariabel"
    description = "Hämtar värdet av en miljövariabel från systemet."
    icon = "AstraDB"

    inputs = [
        StrInput(
            name="env_var_name",
            display_name="Miljövariabelnamn",
            info="Namnet på miljövariabeln att hämta",
        )
    ]

    outputs = [
        Output(display_name="Miljövariabelvärde", name="env_var_value", method="process_inputs"),
    ]

    def process_inputs(self) -> Message:
        if self.env_var_name not in os.environ:
            msg = f"Miljövariabel {self.env_var_name} är inte inställd"
            raise ValueError(msg)
        return Message(text=os.environ[self.env_var_name])

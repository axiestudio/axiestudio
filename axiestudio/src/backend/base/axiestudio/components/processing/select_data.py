from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing.range_spec import RangeSpec
from axiestudio.inputs.inputs import DataInput, IntInput
from axiestudio.io import Output
from axiestudio.schema.data import Data


class SelectDataComponent(Component):
    display_name: str = "Välj data"
    description: str = "Välj en enda data från en lista av data."
    name: str = "SelectData"
    icon = "prototypes"
    legacy = True

    inputs = [
        DataInput(
            name="data_list",
            display_name="Datalista",
            info="Lista av data att välja från.",
            is_list=True,  # Specify that this input takes a list of Data objects
        ),
        IntInput(
            name="data_index",
            display_name="Dataindex",
            info="Index för datan att välja.",
            value=0,  # Will be populated dynamically based on the length of data_list
            range_spec=RangeSpec(min=0, max=15, step=1, step_type="int"),
        ),
    ]

    outputs = [
        Output(display_name="Vald data", name="selected_data", method="select_data"),
    ]

    async def select_data(self) -> Data:
        # Retrieve the selected index from the dropdown
        selected_index = int(self.data_index)
        # Get the data list

        # Validate that the selected index is within bounds
        if selected_index < 0 or selected_index >= len(self.data_list):
            msg = f"Selected index {selected_index} is out of range."
            raise ValueError(msg)

        # Return the selected Data object
        selected_data = self.data_list[selected_index]
        self.status = selected_data  # Update the component status to reflect the selected data
        return selected_data

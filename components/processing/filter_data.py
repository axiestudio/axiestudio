from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataInput, MessageTextInput, Output
from axiestudio.schema.data import Data


class FilterDataComponent(Component):
    display_name = "Filtrera data"
    description = "Filtrerar ett dataobjekt baserat på en lista med nycklar."
    icon = "filter"
    beta = True
    name = "FilterData"
    legacy = True

    inputs = [
        DataInput(
            name="data",
            display_name="Data",
            info="Dataobjekt att filtrera.",
        ),
        MessageTextInput(
            name="filter_criteria",
            display_name="Filterkriterier",
            info="Lista med nycklar att filtrera efter.",
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="Filtrerad data", name="filtered_data", method="filter_data"),
    ]

    def filter_data(self) -> Data:
        filter_criteria: list[str] = self.filter_criteria
        data = self.data.data if isinstance(self.data, Data) else {}

        # Filter the data
        filtered = {key: value for key, value in data.items() if key in filter_criteria}

        # Create a new Data object with the filtered data
        filtered_data = Data(data=filtered)
        self.status = filtered_data
        return filtered_data

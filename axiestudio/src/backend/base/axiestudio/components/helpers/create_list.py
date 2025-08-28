from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import StrInput
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.template.field.base import Output


class CreateListComponent(Component):
    display_name = "Skapa lista"
    description = "Skapar en lista med texter."
    icon = "list"
    name = "CreateList"
    legacy = True

    inputs = [
        StrInput(
            name="texts",
            display_name="Texter",
            info="Ange en eller flera texter.",
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="Datalista", name="list", method="create_list"),
        Output(display_name="DataFrame", name="dataframe", method="as_dataframe"),
    ]

    def create_list(self) -> list[Data]:
        data = [Data(text=text) for text in self.texts]
        self.status = data
        return data

    def as_dataframe(self) -> DataFrame:
        """Convert the list of Data objects into a DataFrame.

        Returns:
            DataFrame: A DataFrame containing the list data.
        """
        return DataFrame(self.create_list())

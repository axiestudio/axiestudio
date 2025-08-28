from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataInput, Output
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame


class DataToDataFrameComponent(Component):
    display_name = "Data → DataFrame"
    description = (
        "Konverterar ett eller flera Data-objekt till en DataFrame. "
        "Varje Data-objekt motsvarar en rad. Fält från `.data` blir kolumner, "
        "och `.text` (om närvarande) placeras i en 'text'-kolumn."
    )
    icon = "table"
    name = "DataToDataFrame"
    legacy = True

    inputs = [
        DataInput(
            name="data_list",
            display_name="Data eller datalista",
            info="Ett eller flera Data-objekt att transformera till en DataFrame.",
            is_list=True,
        ),
    ]

    outputs = [
        Output(
            display_name="DataFrame",
            name="dataframe",
            method="build_dataframe",
            info="En DataFrame byggd från varje Data-objekts fält plus en 'text'-kolumn.",
        ),
    ]

    def build_dataframe(self) -> DataFrame:
        """Builds a DataFrame from Data objects by combining their fields.

        For each Data object:
          - Merge item.data (dictionary) as columns
          - If item.text is present, add 'text' column

        Returns a DataFrame with one row per Data object.
        """
        data_input = self.data_list

        # If user passed a single Data, it might come in as a single object rather than a list
        if not isinstance(data_input, list):
            data_input = [data_input]

        rows = []
        for item in data_input:
            if not isinstance(item, Data):
                msg = f"Förväntade Data-objekt, fick {type(item)} istället."
                raise TypeError(msg)

            # Start with a copy of item.data or an empty dict
            row_dict = dict(item.data) if item.data else {}

            # If the Data object has text, store it under 'text' col
            text_val = item.get_text()
            if text_val:
                row_dict["text"] = text_val

            rows.append(row_dict)

        # Build a DataFrame from these row dictionaries
        df_result = DataFrame(rows)
        self.status = df_result  # store in self.status for logs
        return df_result

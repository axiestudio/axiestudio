import csv
import io
from pathlib import Path

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import FileInput, MessageTextInput, MultilineInput, Output
from axiestudio.schema.data import Data


class CSVToDataComponent(Component):
    display_name = "Ladda CSV"
    description = "Ladda en CSV-fil, CSV från en filsökväg, eller en giltig CSV-sträng och konvertera den till en lista av Data"
    icon = "file-spreadsheet"
    name = "CSVtoData"
    legacy = True

    inputs = [
        FileInput(
            name="csv_file",
            display_name="CSV-fil",
            file_types=["csv"],
            info="Ladda upp en CSV-fil för att konvertera till en lista av Data-objekt",
        ),
        MessageTextInput(
            name="csv_path",
            display_name="CSV-filsökväg",
            info="Ange sökvägen till CSV-filen som ren text",
        ),
        MultilineInput(
            name="csv_string",
            display_name="CSV-sträng",
            info="Klistra in en CSV-sträng direkt för att konvertera till en lista av Data-objekt",
        ),
        MessageTextInput(
            name="text_key",
            display_name="Textnyckel",
            info="Nyckeln att använda för textkolumnen. Standard är 'text'.",
            value="text",
        ),
    ]

    outputs = [
        Output(name="data_list", display_name="Datalista", method="load_csv_to_data"),
    ]

    def load_csv_to_data(self) -> list[Data]:
        if sum(bool(field) for field in [self.csv_file, self.csv_path, self.csv_string]) != 1:
            msg = "Vänligen ange exakt en av: CSV-fil, filsökväg, eller CSV-sträng."
            raise ValueError(msg)

        csv_data = None
        try:
            if self.csv_file:
                resolved_path = self.resolve_path(self.csv_file)
                file_path = Path(resolved_path)
                if file_path.suffix.lower() != ".csv":
                    self.status = "Den angivna filen måste vara en CSV-fil."
                else:
                    with file_path.open(newline="", encoding="utf-8") as csvfile:
                        csv_data = csvfile.read()

            elif self.csv_path:
                file_path = Path(self.csv_path)
                if file_path.suffix.lower() != ".csv":
                    self.status = "Den angivna filen måste vara en CSV-fil."
                else:
                    with file_path.open(newline="", encoding="utf-8") as csvfile:
                        csv_data = csvfile.read()

            else:
                csv_data = self.csv_string

            if csv_data:
                csv_reader = csv.DictReader(io.StringIO(csv_data))
                result = [Data(data=row, text_key=self.text_key) for row in csv_reader]

                if not result:
                    self.status = "CSV-datan är tom."
                    return []

                self.status = result
                return result

        except csv.Error as e:
            error_message = f"CSV-tolkningsfel: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = f"Ett fel inträffade: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        # An error occurred
        raise ValueError(self.status)

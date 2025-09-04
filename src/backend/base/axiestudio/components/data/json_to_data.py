import json
from pathlib import Path

from json_repair import repair_json

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import FileInput, MessageTextInput, MultilineInput, Output
from axiestudio.schema.data import Data


class JSONToDataComponent(Component):
    display_name = "Ladda JSON"
    description = (
        "Konvertera en JSON-fil, JSON från en filsökväg, eller en JSON-sträng till ett Data-objekt eller en lista av Data-objekt"
    )
    icon = "braces"
    name = "JSONtoData"
    legacy = True

    inputs = [
        FileInput(
            name="json_file",
            display_name="JSON-fil",
            file_types=["json"],
            info="Ladda upp en JSON-fil för att konvertera till ett Data-objekt eller lista av Data-objekt",
        ),
        MessageTextInput(
            name="json_path",
            display_name="JSON-filsökväg",
            info="Ange sökvägen till JSON-filen som ren text",
        ),
        MultilineInput(
            name="json_string",
            display_name="JSON-sträng",
            info="Ange en giltig JSON-sträng (objekt eller array) för att konvertera till ett Data-objekt eller lista av Data-objekt",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Data", method="convert_json_to_data"),
    ]

    def convert_json_to_data(self) -> Data | list[Data]:
        if sum(bool(field) for field in [self.json_file, self.json_path, self.json_string]) != 1:
            msg = "Vänligen ange exakt en av: JSON-fil, filsökväg, eller JSON-sträng."
            self.status = msg
            raise ValueError(msg)

        json_data = None

        try:
            if self.json_file:
                resolved_path = self.resolve_path(self.json_file)
                file_path = Path(resolved_path)
                if file_path.suffix.lower() != ".json":
                    self.status = "Den angivna filen måste vara en JSON-fil."
                else:
                    json_data = file_path.read_text(encoding="utf-8")

            elif self.json_path:
                file_path = Path(self.json_path)
                if file_path.suffix.lower() != ".json":
                    self.status = "Den angivna filen måste vara en JSON-fil."
                else:
                    json_data = file_path.read_text(encoding="utf-8")

            else:
                json_data = self.json_string

            if json_data:
                # Try to parse the JSON string
                try:
                    parsed_data = json.loads(json_data)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to repair the JSON string
                    repaired_json_string = repair_json(json_data)
                    parsed_data = json.loads(repaired_json_string)

                # Check if the parsed data is a list
                if isinstance(parsed_data, list):
                    result = [Data(data=item) for item in parsed_data]
                else:
                    result = Data(data=parsed_data)
                self.status = result
                return result

        except (json.JSONDecodeError, SyntaxError, ValueError) as e:
            error_message = f"Ogiltig JSON eller Python-literal: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = f"Ett fel inträffade: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        # An error occurred
        raise ValueError(self.status)

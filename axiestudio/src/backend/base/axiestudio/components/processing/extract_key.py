from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataInput, Output, StrInput
from axiestudio.schema.data import Data


class ExtractDataKeyComponent(Component):
    display_name = "Extrahera nyckel"
    description = (
        "Extrahera en specifik nyckel från ett Data-objekt eller en lista av "
        "Data-objekt och returnera det extraherade värdet/värdena som Data-objekt."
    )
    icon = "key"
    name = "ExtractaKey"
    legacy = True

    inputs = [
        DataInput(
            name="data_input",
            display_name="Data-indata",
            info="Data-objektet eller listan av Data-objekt att extrahera nyckeln från.",
        ),
        StrInput(
            name="key",
            display_name="Nyckel att extrahera",
            info="Nyckeln i Data-objektet/objekten att extrahera.",
        ),
    ]

    outputs = [
        Output(display_name="Extraherad data", name="extracted_data", method="extract_key"),
    ]

    def extract_key(self) -> Data | list[Data]:
        key = self.key

        if isinstance(self.data_input, list):
            result = []
            for item in self.data_input:
                if isinstance(item, Data) and key in item.data:
                    extracted_value = item.data[key]
                    result.append(Data(data={key: extracted_value}))
            self.status = result
            return result
        if isinstance(self.data_input, Data):
            if key in self.data_input.data:
                extracted_value = self.data_input.data[key]
                result = Data(data={key: extracted_value})
                self.status = result
                return result
            self.status = f"Nyckel '{key}' hittades inte i Data-objekt."
            return Data(data={"error": f"Nyckel '{key}' hittades inte i Data-objekt."})
        self.status = "Ogiltig indata. Förväntade Data-objekt eller lista av Data-objekt."
        return Data(data={"error": "Ogiltig indata. Förväntade Data-objekt eller lista av Data-objekt."})

from docling_core.types.doc import DoclingDocument

from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame


def extract_docling_documents(data_inputs: Data | list[Data] | DataFrame, doc_key: str) -> list[DoclingDocument]:
    documents: list[DoclingDocument] = []
    if isinstance(data_inputs, DataFrame):
        if not len(data_inputs):
            msg = "DataFrame är tom"
            raise TypeError(msg)

        if doc_key not in data_inputs.columns:
            msg = f"Kolumnen '{doc_key}' hittades inte i DataFrame"
            raise TypeError(msg)
        try:
            documents = data_inputs[doc_key].tolist()
        except Exception as e:
            msg = f"Fel vid extrahering av DoclingDocument från DataFrame: {e}"
            raise TypeError(msg) from e
    else:
        if not data_inputs:
            msg = "Inga datainmatningar tillhandahållna"
            raise TypeError(msg)

        if isinstance(data_inputs, Data):
            if doc_key not in data_inputs.data:
                msg = (
                    f"'{doc_key}'-fältet är inte tillgängligt i indata. "
                    "Kontrollera att din indata är ett DoclingDocument. "
                    "Du kan använda Docling-komponenten för att konvertera din indata till ett DoclingDocument."
                )
                raise TypeError(msg)
            documents = [data_inputs.data[doc_key]]
        else:
            try:
                documents = [
                    input_.data[doc_key]
                    for input_ in data_inputs
                    if isinstance(input_, Data)
                    and doc_key in input_.data
                    and isinstance(input_.data[doc_key], DoclingDocument)
                ]
                if not documents:
                    msg = f"Inga giltiga datainmatningar hittades i {type(data_inputs)}"
                    raise TypeError(msg)
            except AttributeError as e:
                msg = f"Ogiltig indatatyp i samling: {e}"
                raise TypeError(msg) from e
    return documents

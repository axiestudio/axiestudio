from langchain.docstore.document import Document
from langchain_experimental.text_splitter import SemanticChunker

from axiestudio.base.textsplitters.model import LCTextSplitterComponent
from axiestudio.io import (
    DropdownInput,
    FloatInput,
    HandleInput,
    IntInput,
    MessageTextInput,
    Output,
)
from axiestudio.schema.data import Data


class SemanticTextSplitterComponent(LCTextSplitterComponent):
    """Split text into semantically meaningful chunks using semantic similarity."""

    display_name: str = "Semantisk textdelare"
    name: str = "SemanticTextSplitter"
    description: str = "Dela upp text i semantiskt meningsfulla delar med semantisk likhet."
    documentation = "https://python.langchain.com/docs/how_to/semantic-chunker/"
    beta = True  # this component is beta because it is imported from langchain_experimental
    icon = "LangChain"

    inputs = [
        HandleInput(
            name="data_inputs",
            display_name="Dataindata",
            info="Lista med Dataobjekt som innehåller text och metadata att dela upp.",
            input_types=["Data"],
            is_list=True,
            required=True,
        ),
        HandleInput(
            name="embeddings",
            display_name="Inbäddningar",
            info="Inbäddningsmodell att använda för semantisk likhet. Krävs.",
            input_types=["Embeddings"],
            is_list=False,
            required=True,
        ),
        DropdownInput(
            name="breakpoint_threshold_type",
            display_name="Brytpunktströskeltyp",
            info=(
                "Metod för att bestämma brytpunkter. Alternativ: 'percentile', "
                "'standard_deviation', 'interquartile'. Standardvärde är 'percentile'."
            ),
            value="percentile",
            options=["percentile", "standard_deviation", "interquartile"],
        ),
        FloatInput(
            name="breakpoint_threshold_amount",
            display_name="Brytpunkt tröskelbelopp",
            info="Numeriskt belopp för brytpunktströskeln.",
            value=0.5,
        ),
        IntInput(
            name="number_of_chunks",
            display_name="Antal chunks",
            info="Antal chunks att dela upp texten i.",
            value=5,
        ),
        MessageTextInput(
            name="sentence_split_regex",
            display_name="Meningsdelning regex",
            info="Reguljärt uttryck för att dela meningar. Valfritt.",
            value="",
            advanced=True,
        ),
        IntInput(
            name="buffer_size",
            display_name="Bufferstorlek",
            info="Storleken på bufferten.",
            value=0,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="split_text"),
    ]

    def _docs_to_data(self, docs: list[Document]) -> list[Data]:
        """Convert a list of Document objects to Data objects."""
        return [Data(text=doc.page_content, data=doc.metadata) for doc in docs]

    def split_text(self) -> list[Data]:
        """Split the input data into semantically meaningful chunks."""
        try:
            embeddings = getattr(self, "embeddings", None)
            if embeddings is None:
                error_msg = "An embeddings model is required for SemanticTextSplitter."
                raise ValueError(error_msg)

            if not self.data_inputs:
                error_msg = "Data inputs cannot be empty."
                raise ValueError(error_msg)

            documents = []
            for _input in self.data_inputs:
                if isinstance(_input, Data):
                    documents.append(_input.to_lc_document())
                else:
                    error_msg = f"Invalid data input type: {_input}"
                    raise TypeError(error_msg)

            if not documents:
                error_msg = "No valid Data objects found in data_inputs."
                raise ValueError(error_msg)

            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            splitter_params = {
                "embeddings": embeddings,
                "breakpoint_threshold_type": self.breakpoint_threshold_type or "percentile",
                "breakpoint_threshold_amount": self.breakpoint_threshold_amount,
                "number_of_chunks": self.number_of_chunks,
                "buffer_size": self.buffer_size,
            }

            if self.sentence_split_regex:
                splitter_params["sentence_split_regex"] = self.sentence_split_regex

            splitter = SemanticChunker(**splitter_params)
            docs = splitter.create_documents(texts, metadatas=metadatas)

            data = self._docs_to_data(docs)
            self.status = data

        except Exception as e:
            error_msg = f"Ett fel uppstod under semantisk uppdelning: {e}"
            raise RuntimeError(error_msg) from e

        else:
            return data

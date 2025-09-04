from langchain_community.embeddings import FakeEmbeddings

from axiestudio.base.embeddings.model import LCEmbeddingsModel
from axiestudio.field_typing import Embeddings
from axiestudio.io import IntInput


class FakeEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "Falska inbäddningar"
    description = "Generera falska inbäddningar, användbart för initial testning och anslutning av komponenter."
    icon = "LangChain"
    name = "LangChainFakeEmbeddings"

    inputs = [
        IntInput(
            name="dimensions",
            display_name="Dimensioner",
            info="Antalet dimensioner som de resulterande utdata-inbäddningarna ska ha.",
            value=5,
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        return FakeEmbeddings(
            size=self.dimensions or 5,
        )

from axiestudio.base.compressors.model import LCCompressorComponent
from axiestudio.field_typing import BaseDocumentCompressor
from axiestudio.inputs.inputs import SecretStrInput
from axiestudio.io import DropdownInput
from axiestudio.template.field.base import Output


class CohereRerankComponent(LCCompressorComponent):
    display_name = "Cohere Omrankning"
    description = "Omranka dokument med Cohere API."
    name = "CohereRerank"
    icon = "Cohere"

    inputs = [
        *LCCompressorComponent.inputs,
        SecretStrInput(
            name="api_key",
            display_name="Cohere API-nyckel",
        ),
        DropdownInput(
            name="model",
            display_name="Modell",
            options=[
                "rerank-english-v3.0",
                "rerank-multilingual-v3.0",
                "rerank-english-v2.0",
                "rerank-multilingual-v2.0",
            ],
            value="rerank-english-v3.0",
        ),
    ]

    outputs = [
        Output(
            display_name="Omrankade dokument",
            name="reranked_documents",
            method="compress_documents",
        ),
    ]

    def build_compressor(self) -> BaseDocumentCompressor:  # type: ignore[type-var]
        try:
            from langchain_cohere import CohereRerank
        except ImportError as e:
            msg = "Vänligen installera langchain-cohere för att använda Cohere-modellen."
            raise ImportError(msg) from e
        return CohereRerank(
            cohere_api_key=self.api_key,
            model=self.model,
            top_n=self.top_n,
        )

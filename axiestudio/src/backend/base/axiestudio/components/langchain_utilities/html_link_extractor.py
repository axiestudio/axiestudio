from typing import Any

from langchain_community.graph_vectorstores.extractors import HtmlLinkExtractor, LinkExtractorTransformer
from langchain_core.documents import BaseDocumentTransformer

from axiestudio.base.document_transformers.model import LCDocumentTransformerComponent
from axiestudio.inputs.inputs import BoolInput, DataInput, StrInput


class HtmlLinkExtractorComponent(LCDocumentTransformerComponent):
    display_name = "HTML-länkextraktor"
    description = "Extrahera hyperlänkar från HTML-innehåll."
    documentation = "https://python.langchain.com/v0.2/api_reference/community/graph_vectorstores/langchain_community.graph_vectorstores.extractors.html_link_extractor.HtmlLinkExtractor.html"
    name = "HtmlLinkExtractor"
    icon = "LangChain"

    inputs = [
        StrInput(name="kind", display_name="Typ av kant", value="hyperlink", required=False),
        BoolInput(name="drop_fragments", display_name="Ta bort URL-fragment", value=True, required=False),
        DataInput(
            name="data_input",
            display_name="Inmatning",
            info="Texterna från vilka länkar ska extraheras.",
            input_types=["Document", "Data"],
            required=True,
        ),
    ]

    def get_data_input(self) -> Any:
        return self.data_input

    def build_document_transformer(self) -> BaseDocumentTransformer:
        return LinkExtractorTransformer(
            [HtmlLinkExtractor(kind=self.kind, drop_fragments=self.drop_fragments).as_document_extractor()]
        )

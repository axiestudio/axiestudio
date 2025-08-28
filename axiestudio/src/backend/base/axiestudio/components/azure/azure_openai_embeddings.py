from langchain_openai import AzureOpenAIEmbeddings

from axiestudio.base.models.model import LCModelComponent
from axiestudio.base.models.openai_constants import OPENAI_EMBEDDING_MODEL_NAMES
from axiestudio.field_typing import Embeddings
from axiestudio.io import DropdownInput, IntInput, MessageTextInput, Output, SecretStrInput


class AzureOpenAIEmbeddingsComponent(LCModelComponent):
    display_name: str = "Azure OpenAI Inbäddningar"
    description: str = "Generera inbäddningar med Azure OpenAI-modeller."
    documentation: str = "https://python.langchain.com/docs/integrations/text_embedding/azureopenai"
    icon = "Azure"
    name = "AzureOpenAIEmbeddings"

    API_VERSION_OPTIONS = [
        "2022-12-01",
        "2023-03-15-preview",
        "2023-05-15",
        "2023-06-01-preview",
        "2023-07-01-preview",
        "2023-08-01-preview",
    ]

    inputs = [
        DropdownInput(
            name="model",
            display_name="Modell",
            advanced=False,
            options=OPENAI_EMBEDDING_MODEL_NAMES,
            value=OPENAI_EMBEDDING_MODEL_NAMES[0],
        ),
        MessageTextInput(
            name="azure_endpoint",
            display_name="Azure-endpoint",
            required=True,
            info="Din Azure-endpoint, inklusive resursen. Exempel: `https://example-resource.azure.openai.com/`",
        ),
        MessageTextInput(
            name="azure_deployment",
            display_name="Distributionsnamn",
            required=True,
        ),
        DropdownInput(
            name="api_version",
            display_name="API-version",
            options=API_VERSION_OPTIONS,
            value=API_VERSION_OPTIONS[-1],
            advanced=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            required=True,
        ),
        IntInput(
            name="dimensions",
            display_name="Dimensioner",
            info="Antalet dimensioner som de resulterande utdata-inbäddningarna ska ha. "
            "Stöds endast av vissa modeller.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def build_embeddings(self) -> Embeddings:
        try:
            embeddings = AzureOpenAIEmbeddings(
                model=self.model,
                azure_endpoint=self.azure_endpoint,
                azure_deployment=self.azure_deployment,
                api_version=self.api_version,
                api_key=self.api_key,
                dimensions=self.dimensions or None,
            )
        except Exception as e:
            msg = f"Kunde inte ansluta till AzureOpenAIEmbeddings API: {e}"
            raise ValueError(msg) from e

        return embeddings

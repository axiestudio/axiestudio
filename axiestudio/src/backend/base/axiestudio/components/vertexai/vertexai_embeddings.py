from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import Embeddings
from axiestudio.io import BoolInput, FileInput, FloatInput, IntInput, MessageTextInput, Output


class VertexAIEmbeddingsComponent(LCModelComponent):
    display_name = "Vertex AI Inbäddningar"
    description = "Generera inbäddningar med Google Cloud Vertex AI-modeller."
    icon = "VertexAI"
    name = "VertexAIEmbeddings"

    inputs = [
        FileInput(
            name="credentials",
            display_name="Autentiseringsuppgifter",
            info="JSON-fil med autentiseringsuppgifter. Lämna tom för att använda miljövariabler",
            value="",
            file_types=["json"],
            required=True,
        ),
        MessageTextInput(name="location", display_name="Plats", value="us-central1", advanced=True),
        MessageTextInput(name="project", display_name="Projekt", info="Projekt-ID.", advanced=True),
        IntInput(name="max_output_tokens", display_name="Max utdata-tokens", advanced=True),
        IntInput(name="max_retries", display_name="Max försök", value=1, advanced=True),
        MessageTextInput(name="model_name", display_name="Modellnamn", value="textembedding-gecko", required=True),
        IntInput(name="n", display_name="N", value=1, advanced=True),
        IntInput(name="request_parallelism", value=5, display_name="Förfrågningsparallellism", advanced=True),
        MessageTextInput(name="stop_sequences", display_name="Stopp", advanced=True, is_list=True),
        BoolInput(name="streaming", display_name="Strömning", value=False, advanced=True),
        FloatInput(name="temperature", value=0.0, display_name="Temperatur"),
        IntInput(name="top_k", display_name="Top K", advanced=True),
        FloatInput(name="top_p", display_name="Top P", value=0.95, advanced=True),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def build_embeddings(self) -> Embeddings:
        try:
            from langchain_google_vertexai import VertexAIEmbeddings
        except ImportError as e:
            msg = "Vänligen installera langchain-google-vertexai-paketet för att använda VertexAIEmbeddings-komponenten."
            raise ImportError(msg) from e

        from google.oauth2 import service_account

        if self.credentials:
            gcloud_credentials = service_account.Credentials.from_service_account_file(self.credentials)
        else:
            # will fallback to environment variable or inferred from gcloud CLI
            gcloud_credentials = None
        return VertexAIEmbeddings(
            credentials=gcloud_credentials,
            location=self.location,
            max_output_tokens=self.max_output_tokens or None,
            max_retries=self.max_retries,
            model_name=self.model_name,
            n=self.n,
            project=self.project,
            request_parallelism=self.request_parallelism,
            stop=self.stop_sequences or None,
            streaming=self.streaming,
            temperature=self.temperature,
            top_k=self.top_k or None,
            top_p=self.top_p,
        )

from typing import cast

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.inputs.inputs import MessageTextInput
from axiestudio.io import BoolInput, FileInput, FloatInput, IntInput, StrInput


class ChatVertexAIComponent(LCModelComponent):
    display_name = "Vertex AI"
    description = "Generera text med Vertex AI LLM:er."
    icon = "VertexAI"
    name = "VertexAiModel"

    inputs = [
        *LCModelComponent._base_inputs,
        FileInput(
            name="credentials",
            display_name="Autentiseringsuppgifter",
            info="JSON-fil med autentiseringsuppgifter. Lämna tom för att använda miljövariabler",
            file_types=["json"],
        ),
        MessageTextInput(name="model_name", display_name="Modellnamn", value="gemini-1.5-pro"),
        StrInput(name="project", display_name="Projekt", info="Projekt-ID.", advanced=True),
        StrInput(name="location", display_name="Plats", value="us-central1", advanced=True),
        IntInput(name="max_output_tokens", display_name="Max utdata-tokens", advanced=True),
        IntInput(name="max_retries", display_name="Max försök", value=1, advanced=True),
        FloatInput(name="temperature", value=0.0, display_name="Temperatur"),
        IntInput(name="top_k", display_name="Top K", advanced=True),
        FloatInput(name="top_p", display_name="Top P", value=0.95, advanced=True),
        BoolInput(name="verbose", display_name="Utförlig", value=False, advanced=True),
    ]

    def build_model(self) -> LanguageModel:
        try:
            from langchain_google_vertexai import ChatVertexAI
        except ImportError as e:
            msg = "Vänligen installera langchain-google-vertexai-paketet för att använda VertexAIEmbeddings-komponenten."
            raise ImportError(msg) from e
        location = self.location or None
        if self.credentials:
            from google.cloud import aiplatform
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(self.credentials)
            project = self.project or credentials.project_id
            # ChatVertexAI sometimes skip manual credentials initialization
            aiplatform.init(
                project=project,
                location=location,
                credentials=credentials,
            )
        else:
            project = self.project or None
            credentials = None

        return cast(
            "LanguageModel",
            ChatVertexAI(
                credentials=credentials,
                location=location,
                project=project,
                max_output_tokens=self.max_output_tokens or None,
                max_retries=self.max_retries,
                model_name=self.model_name,
                temperature=self.temperature,
                top_k=self.top_k or None,
                top_p=self.top_p,
                verbose=self.verbose,
            ),
        )

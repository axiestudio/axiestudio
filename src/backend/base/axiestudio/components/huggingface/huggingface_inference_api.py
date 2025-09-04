from urllib.parse import urlparse

import requests
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings

# Next update: use langchain_huggingface
from pydantic import SecretStr
from tenacity import retry, stop_after_attempt, wait_fixed

from axiestudio.base.embeddings.model import LCEmbeddingsModel
from axiestudio.field_typing import Embeddings
from axiestudio.io import MessageTextInput, Output, SecretStrInput


class HuggingFaceInferenceAPIEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "Hugging Face Inbäddningar Inferens"
    description = "Generera inbäddningar med Hugging Face Text Embeddings Inference (TEI)"
    documentation = "https://huggingface.co/docs/text-embeddings-inference/index"
    icon = "HuggingFace"
    name = "HuggingFaceInferenceAPIEmbeddings"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            advanced=False,
            info="Krävs för icke-lokala inferens-endpoints. Lokal inferens kräver inte en API-nyckel.",
        ),
        MessageTextInput(
            name="inference_endpoint",
            display_name="Inferens-endpoint",
            required=True,
            value="https://api-inference.huggingface.co/models/",
            info="Anpassad inferens-endpoint URL.",
        ),
        MessageTextInput(
            name="model_name",
            display_name="Modellnamn",
            value="BAAI/bge-large-en-v1.5",
            info="Namnet på modellen som ska användas för textinbäddningar.",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def validate_inference_endpoint(self, inference_endpoint: str) -> bool:
        parsed_url = urlparse(inference_endpoint)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            msg = (
                f"Ogiltigt inferens-endpoint format: '{self.inference_endpoint}'. "
                "Vänligen säkerställ att URL:en inkluderar både ett schema (t.ex. 'http://' eller 'https://') och ett domännamn. "
                "Exempel: 'http://localhost:8080' eller 'https://api.example.com'"
            )
            raise ValueError(msg)

        try:
            response = requests.get(f"{inference_endpoint}/health", timeout=5)
        except requests.RequestException as e:
            msg = (
                f"Inferens-endpoint '{inference_endpoint}' svarar inte. "
                "Vänligen säkerställ att URL:en är korrekt och att tjänsten körs."
            )
            raise ValueError(msg) from e

        if response.status_code != requests.codes.ok:
            msg = f"Hugging Face hälsokontroll misslyckades: {response.status_code}"
            raise ValueError(msg)
        # returning True to solve linting error
        return True

    def get_api_url(self) -> str:
        if "huggingface" in self.inference_endpoint.lower():
            return f"{self.inference_endpoint}"
        return self.inference_endpoint

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def create_huggingface_embeddings(
        self, api_key: SecretStr, api_url: str, model_name: str
    ) -> HuggingFaceInferenceAPIEmbeddings:
        return HuggingFaceInferenceAPIEmbeddings(api_key=api_key, api_url=api_url, model_name=model_name)

    def build_embeddings(self) -> Embeddings:
        api_url = self.get_api_url()

        is_local_url = (
            api_url.startswith(("http://localhost", "http://127.0.0.1", "http://0.0.0.0", "http://docker"))
            or "huggingface.co" not in api_url.lower()
        )

        if not self.api_key and is_local_url:
            self.validate_inference_endpoint(api_url)
            api_key = SecretStr("APIKeyForLocalDeployment")
        elif not self.api_key:
            msg = "API-nyckel krävs för icke-lokala inferens-endpoints"
            raise ValueError(msg)
        else:
            api_key = SecretStr(self.api_key).get_secret_value()

        try:
            return self.create_huggingface_embeddings(api_key, api_url, self.model_name)
        except Exception as e:
            msg = "Kunde inte ansluta till Hugging Face Inference API."
            raise ValueError(msg) from e

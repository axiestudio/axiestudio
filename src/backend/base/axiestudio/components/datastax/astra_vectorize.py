from typing import Any

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import DictInput, DropdownInput, MessageTextInput, SecretStrInput
from axiestudio.template.field.base import Output


class AstraVectorizeComponent(Component):
    display_name: str = "Astra Vectorize [FÖRÅLDRAD]"
    description: str = (
        "Konfigurationsalternativ för Astra Vectorize server-side embeddings. "
        "Denna komponent är föråldrad. Vänligen använd Astra DB-komponenten direkt."
    )
    documentation: str = "https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html"
    legacy = True
    icon = "AstraDB"
    name = "AstraVectorize"

    VECTORIZE_PROVIDERS_MAPPING = {
        "Azure OpenAI": ["azureOpenAI", ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]],
        "Hugging Face - Dedicated": ["huggingfaceDedicated", ["endpoint-defined-model"]],
        "Hugging Face - Serverless": [
            "huggingface",
            [
                "sentence-transformers/all-MiniLM-L6-v2",
                "intfloat/multilingual-e5-large",
                "intfloat/multilingual-e5-large-instruct",
                "BAAI/bge-small-en-v1.5",
                "BAAI/bge-base-en-v1.5",
                "BAAI/bge-large-en-v1.5",
            ],
        ],
        "Jina AI": [
            "jinaAI",
            [
                "jina-embeddings-v2-base-en",
                "jina-embeddings-v2-base-de",
                "jina-embeddings-v2-base-es",
                "jina-embeddings-v2-base-code",
                "jina-embeddings-v2-base-zh",
            ],
        ],
        "Mistral AI": ["mistral", ["mistral-embed"]],
        "NVIDIA": ["nvidia", ["NV-Embed-QA"]],
        "OpenAI": ["openai", ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]],
        "Upstage": ["upstageAI", ["solar-embedding-1-large"]],
        "Voyage AI": [
            "voyageAI",
            ["voyage-large-2-instruct", "voyage-law-2", "voyage-code-2", "voyage-large-2", "voyage-2"],
        ],
    }
    VECTORIZE_MODELS_STR = "\n\n".join(
        [provider + ": " + (", ".join(models[1])) for provider, models in VECTORIZE_PROVIDERS_MAPPING.items()]
    )

    inputs = [
        DropdownInput(
            name="provider",
            display_name="Leverantör",
            options=VECTORIZE_PROVIDERS_MAPPING.keys(),
            value="",
            required=True,
        ),
        MessageTextInput(
            name="model_name",
            display_name="Modellnamn",
            info="Embedding-modellen att använda för den valda leverantören. Varje leverantör har en annan uppsättning modeller "
            f"tillgängliga (fullständig lista på https://docs.datastax.com/en/astra-db-serverless/databases/embedding-generation.html):\n\n{VECTORIZE_MODELS_STR}",
            required=True,
        ),
        MessageTextInput(
            name="api_key_name",
            display_name="API-nyckelnamn",
            info="Namnet på embedding-leverantörens API-nyckel som lagras på Astra. "
            "Om den är inställd kommer den att åsidosätta 'ProviderKey' i autentiseringsparametrarna.",
        ),
        DictInput(
            name="authentication",
            display_name="Autentiseringsparametrar",
            is_list=True,
            advanced=True,
        ),
        SecretStrInput(
            name="provider_api_key",
            display_name="Leverantörs API-nyckel",
            info="Ett alternativ till Astra-autentiseringen som skickar en API-nyckel för leverantören med varje begäran "
            "till Astra DB. "
            "Detta kan användas när Vectorize är konfigurerat för samlingen, "
            "men ingen motsvarande leverantörshemlighet lagras inom Astras nyckelhanteringssystem.",
            advanced=True,
        ),
        DictInput(
            name="authentication",
            display_name="Autentiseringsparametrar",
            is_list=True,
            advanced=True,
        ),
        DictInput(
            name="model_parameters",
            display_name="Modellparametrar",
            advanced=True,
            is_list=True,
        ),
    ]
    outputs = [
        Output(display_name="Vectorize", name="config", method="build_options", types=["dict"]),
    ]

    def build_options(self) -> dict[str, Any]:
        provider_value = self.VECTORIZE_PROVIDERS_MAPPING[self.provider][0]
        authentication = {**(self.authentication or {})}
        api_key_name = self.api_key_name
        if api_key_name:
            authentication["providerKey"] = api_key_name
        return {
            # must match astrapy.info.VectorServiceOptions
            "collection_vector_service_options": {
                "provider": provider_value,
                "modelName": self.model_name,
                "authentication": authentication,
                "parameters": self.model_parameters or {},
            },
            "collection_embedding_api_key": self.provider_api_key,
        }

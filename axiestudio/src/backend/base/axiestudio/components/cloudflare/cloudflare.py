from langchain_community.embeddings.cloudflare_workersai import CloudflareWorkersAIEmbeddings

from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import Embeddings
from axiestudio.io import BoolInput, DictInput, IntInput, MessageTextInput, Output, SecretStrInput


class CloudflareWorkersAIEmbeddingsComponent(LCModelComponent):
    display_name: str = "Cloudflare Workers AI Inbäddningar"
    description: str = "Generera inbäddningar med Cloudflare Workers AI-modeller."
    documentation: str = "https://python.langchain.com/docs/integrations/text_embedding/cloudflare_workersai/"
    icon = "Cloudflare"
    name = "CloudflareWorkersAIEmbeddings"

    inputs = [
        MessageTextInput(
            name="account_id",
            display_name="Cloudflare konto-ID",
            info="Hitta ditt konto-ID https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/#find-account-id-workers-and-pages",
            required=True,
        ),
        SecretStrInput(
            name="api_token",
            display_name="Cloudflare API-token",
            info="Skapa en API-token https://developers.cloudflare.com/fundamentals/api/get-started/create-token/",
            required=True,
        ),
        MessageTextInput(
            name="model_name",
            display_name="Modellnamn",
            info="Lista över stödda modeller https://developers.cloudflare.com/workers-ai/models/#text-embeddings",
            required=True,
            value="@cf/baai/bge-base-en-v1.5",
        ),
        BoolInput(
            name="strip_new_lines",
            display_name="Ta bort nya rader",
            advanced=True,
            value=True,
        ),
        IntInput(
            name="batch_size",
            display_name="Batchstorlek",
            advanced=True,
            value=50,
        ),
        MessageTextInput(
            name="api_base_url",
            display_name="Cloudflare API bas-URL",
            advanced=True,
            value="https://api.cloudflare.com/client/v4/accounts",
        ),
        DictInput(
            name="headers",
            display_name="Rubriker",
            info="Ytterligare förfrågningsrubriker",
            is_list=True,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def build_embeddings(self) -> Embeddings:
        try:
            embeddings = CloudflareWorkersAIEmbeddings(
                account_id=self.account_id,
                api_base_url=self.api_base_url,
                api_token=self.api_token,
                batch_size=self.batch_size,
                headers=self.headers,
                model_name=self.model_name,
                strip_new_lines=self.strip_new_lines,
            )
        except Exception as e:
            msg = f"Kunde inte ansluta till CloudflareWorkersAIEmbeddings API: {e!s}"
            raise ValueError(msg) from e

        return embeddings

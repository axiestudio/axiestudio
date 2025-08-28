from axiestudio.base.models.aws_constants import AWS_EMBEDDING_MODEL_IDS, AWS_REGIONS
from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import Embeddings
from axiestudio.inputs.inputs import SecretStrInput
from axiestudio.io import DropdownInput, MessageTextInput, Output


class AmazonBedrockEmbeddingsComponent(LCModelComponent):
    display_name: str = "Amazon Bedrock Inbäddningar"
    description: str = "Generera inbäddningar med Amazon Bedrock-modeller."
    icon = "Amazon"
    name = "AmazonBedrockEmbeddings"

    inputs = [
        DropdownInput(
            name="model_id",
            display_name="Modell-ID",
            options=AWS_EMBEDDING_MODEL_IDS,
            value="amazon.titan-embed-text-v1",
        ),
        SecretStrInput(
            name="aws_access_key_id",
            display_name="AWS åtkomstnyckel-ID",
            info="Åtkomstnyckeln för ditt AWS-konto."
            "Vanligtvis satt i Python-kod som miljövariabeln 'AWS_ACCESS_KEY_ID'.",
            value="AWS_ACCESS_KEY_ID",
            required=True,
        ),
        SecretStrInput(
            name="aws_secret_access_key",
            display_name="AWS hemlig åtkomstnyckel",
            info="Den hemliga nyckeln för ditt AWS-konto. "
            "Vanligtvis satt i Python-kod som miljövariabeln 'AWS_SECRET_ACCESS_KEY'.",
            value="AWS_SECRET_ACCESS_KEY",
            required=True,
        ),
        SecretStrInput(
            name="aws_session_token",
            display_name="AWS sessionstoken",
            advanced=False,
            info="Sessionsnyckeln för ditt AWS-konto. "
            "Behövs endast för tillfälliga autentiseringsuppgifter. "
            "Vanligtvis satt i Python-kod som miljövariabeln 'AWS_SESSION_TOKEN'.",
            value="AWS_SESSION_TOKEN",
        ),
        SecretStrInput(
            name="credentials_profile_name",
            display_name="Autentiseringsprofilnamn",
            advanced=True,
            info="Namnet på profilen att använda från din "
            "~/.aws/credentials-fil. "
            "Om inte angiven kommer standardprofilen att användas.",
            value="AWS_CREDENTIALS_PROFILE_NAME",
        ),
        DropdownInput(
            name="region_name",
            display_name="Regionnamn",
            value="us-east-1",
            options=AWS_REGIONS,
            info="AWS-regionen där dina Bedrock-resurser finns.",
        ),
        MessageTextInput(
            name="endpoint_url",
            display_name="Endpoint-URL",
            advanced=True,
            info="URL:en för AWS Bedrock-endpointen att använda.",
        ),
    ]

    outputs = [
        Output(display_name="Inbäddningar", name="embeddings", method="build_embeddings"),
    ]

    def build_embeddings(self) -> Embeddings:
        try:
            from langchain_aws import BedrockEmbeddings
        except ImportError as e:
            msg = "langchain_aws är inte installerat. Vänligen installera det med `pip install langchain_aws`."
            raise ImportError(msg) from e
        try:
            import boto3
        except ImportError as e:
            msg = "boto3 är inte installerat. Vänligen installera det med `pip install boto3`."
            raise ImportError(msg) from e
        if self.aws_access_key_id or self.aws_secret_access_key:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
            )
        elif self.credentials_profile_name:
            session = boto3.Session(profile_name=self.credentials_profile_name)
        else:
            session = boto3.Session()

        client_params = {}
        if self.endpoint_url:
            client_params["endpoint_url"] = self.endpoint_url
        if self.region_name:
            client_params["region_name"] = self.region_name

        boto3_client = session.client("bedrock-runtime", **client_params)
        return BedrockEmbeddings(
            credentials_profile_name=self.credentials_profile_name,
            client=boto3_client,
            model_id=self.model_id,
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
        )

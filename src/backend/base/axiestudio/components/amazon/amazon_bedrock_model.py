from axiestudio.base.models.aws_constants import AWS_REGIONS, AWS_MODEL_IDs
from axiestudio.base.models.model import LCModelComponent
from axiestudio.field_typing import LanguageModel
from axiestudio.inputs.inputs import MessageTextInput, SecretStrInput
from axiestudio.io import DictInput, DropdownInput


class AmazonBedrockComponent(LCModelComponent):
    display_name: str = "Amazon Bedrock"
    description: str = "Generera text med Amazon Bedrock LLM:er."
    icon = "Amazon"
    name = "AmazonBedrockModel"

    inputs = [
        *LCModelComponent._base_inputs,
        DropdownInput(
            name="model_id",
            display_name="Modell-ID",
            options=AWS_MODEL_IDs,
            value="anthropic.claude-3-haiku-20240307-v1:0",
            info="Lista över tillgängliga modell-ID:n att välja från.",
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
            load_from_db=False,
        ),
        SecretStrInput(
            name="credentials_profile_name",
            display_name="Autentiseringsprofilnamn",
            advanced=True,
            info="Namnet på profilen att använda från din "
            "~/.aws/credentials-fil. "
            "Om inte angiven kommer standardprofilen att användas.",
            load_from_db=False,
        ),
        DropdownInput(
            name="region_name",
            display_name="Regionnamn",
            value="us-east-1",
            options=AWS_REGIONS,
            info="AWS-regionen där dina Bedrock-resurser finns.",
        ),
        DictInput(
            name="model_kwargs",
            display_name="Modell-kwargs",
            advanced=True,
            is_list=True,
            info="Ytterligare nyckelordsargument att skicka till modellen.",
        ),
        MessageTextInput(
            name="endpoint_url",
            display_name="Endpoint-URL",
            advanced=True,
            info="URL:en för Bedrock-endpointen att använda.",
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            from langchain_aws import ChatBedrock
        except ImportError as e:
            msg = "langchain_aws är inte installerat. Vänligen installera det med `pip install langchain_aws`."
            raise ImportError(msg) from e
        try:
            import boto3
        except ImportError as e:
            msg = "boto3 är inte installerat. Vänligen installera det med `pip install boto3`."
            raise ImportError(msg) from e
        if self.aws_access_key_id or self.aws_secret_access_key:
            try:
                session = boto3.Session(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    aws_session_token=self.aws_session_token,
                )
            except Exception as e:
                msg = "Kunde inte skapa en boto3-session."
                raise ValueError(msg) from e
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
        try:
            output = ChatBedrock(
                client=boto3_client,
                model_id=self.model_id,
                region_name=self.region_name,
                model_kwargs=self.model_kwargs,
                endpoint_url=self.endpoint_url,
                streaming=self.stream,
            )
        except Exception as e:
            msg = "Kunde inte ansluta till AmazonBedrock API."
            raise ValueError(msg) from e
        return output

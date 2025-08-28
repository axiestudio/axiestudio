import os

from astrapy.admin import parse_api_endpoint

from axiestudio.base.memory.model import LCChatMemoryComponent
from axiestudio.field_typing.constants import Memory
from axiestudio.inputs.inputs import MessageTextInput, SecretStrInput, StrInput


class AstraDBChatMemory(LCChatMemoryComponent):
    display_name = "Astra DB-chattminne"
    description = "Hämtar och lagrar chattmeddelanden från Astra DB."
    name = "AstraDBChatMemory"
    icon: str = "AstraDB"

    inputs = [
        SecretStrInput(
            name="token",
            display_name="Astra DB-applikationstoken",
            info="Autentiseringstoken för åtkomst till Astra DB.",
            value="ASTRA_DB_APPLICATION_TOKEN",
            required=True,
            advanced=os.getenv("ASTRA_ENHANCED", "false").lower() == "true",
        ),
        SecretStrInput(
            name="api_endpoint",
            display_name="API-slutpunkt",
            info="API-slutpunkts-URL för Astra DB-tjänsten.",
            value="ASTRA_DB_API_ENDPOINT",
            required=True,
        ),
        StrInput(
            name="collection_name",
            display_name="Samlingens namn",
            info="Namnet på samlingen inom Astra DB där vektorerna kommer att lagras.",
            required=True,
        ),
        StrInput(
            name="namespace",
            display_name="Namnrymd",
            info="Valfri namnrymd inom Astra DB att använda för samlingen.",
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="Sessions-ID",
            info="Sessions-ID för chatten. Om tom, kommer den aktuella sessions-ID-parametern att användas.",
            advanced=True,
        ),
    ]

    def build_message_history(self) -> Memory:
        try:
            from langchain_astradb.chat_message_histories import AstraDBChatMessageHistory
        except ImportError as e:
            msg = (
                "Det gick inte att importera langchain Astra DB-integreringspaketet. "
                "Installera det med `pip install langchain-astradb`."
            )
            raise ImportError(msg) from e

        return AstraDBChatMessageHistory(
            session_id=self.session_id,
            collection_name=self.collection_name,
            token=self.token,
            api_endpoint=self.api_endpoint,
            namespace=self.namespace or None,
            environment=parse_api_endpoint(self.api_endpoint).environment,
        )

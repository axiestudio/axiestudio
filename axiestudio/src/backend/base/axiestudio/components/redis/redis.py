from urllib import parse

from langchain_community.chat_message_histories.redis import RedisChatMessageHistory

from axiestudio.base.memory.model import LCChatMemoryComponent
from axiestudio.field_typing.constants import Memory
from axiestudio.inputs.inputs import IntInput, MessageTextInput, SecretStrInput, StrInput


class RedisIndexChatMemory(LCChatMemoryComponent):
    display_name = "Redis-chattminne"
    description = "Hämtar och lagrar chattmeddelanden från Redis."
    name = "RedisChatMemory"
    icon = "Redis"

    inputs = [
        StrInput(
            name="host", display_name="värdnamn", required=True, value="localhost", info="IP-adress eller värdnamn."
        ),
        IntInput(name="port", display_name="port", required=True, value=6379, info="Redis-portnummer."),
        StrInput(name="database", display_name="databas", required=True, value="0", info="Redis-databas."),
        MessageTextInput(
            name="username", display_name="Användarnamn", value="", info="Redis-användarnamnet.", advanced=True
        ),
        SecretStrInput(
            name="password", display_name="Lösenord", value="", info="Lösenordet för användarnamnet.", advanced=True
        ),
        StrInput(name="key_prefix", display_name="Nyckelprefix", info="Nyckelprefix.", advanced=True),
        MessageTextInput(
            name="session_id", display_name="Sessions-ID", info="Sessions-ID för meddelandet.", advanced=True
        ),
    ]

    def build_message_history(self) -> Memory:
        kwargs = {}
        password: str | None = self.password
        if self.key_prefix:
            kwargs["key_prefix"] = self.key_prefix
        if password:
            password = parse.quote_plus(password)

        url = f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        return RedisChatMessageHistory(session_id=self.session_id, url=url, **kwargs)

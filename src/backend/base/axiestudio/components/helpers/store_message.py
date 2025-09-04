from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import (
    HandleInput,
    MessageTextInput,
)
from axiestudio.memory import aget_messages, astore_message
from axiestudio.schema.message import Message
from axiestudio.template.field.base import Output
from axiestudio.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI


class MessageStoreComponent(Component):
    display_name = "Meddelandelagring"
    description = "Lagrar ett chattmeddelande eller text i Axie Studio-tabeller eller ett externt minne."
    icon = "message-square-text"
    name = "StoreMessage"
    legacy = True

    inputs = [
        MessageTextInput(
            name="message", display_name="Meddelande", info="Chattmeddelandet som ska lagras.", required=True, tool_mode=True
        ),
        HandleInput(
            name="memory",
            display_name="Externt minne",
            input_types=["Memory"],
            info="Det externa minnet för att lagra meddelandet. Om tomt kommer Axie Studio-tabellerna att användas.",
        ),
        MessageTextInput(
            name="sender",
            display_name="Avsändare",
            info="Avsändaren av meddelandet. Kan vara Maskin eller Användare. "
            "Om tomt kommer den aktuella avsändarparametern att användas.",
            advanced=True,
        ),
        MessageTextInput(
            name="sender_name",
            display_name="Avsändarnamn",
            info="Namnet på avsändaren. Kan vara AI eller Användare. Om tomt kommer den aktuella avsändarparametern att användas.",
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="Sessions-ID",
            info="Sessions-ID för chatten. Om tomt kommer den aktuella sessions-ID-parametern att användas.",
            value="",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Lagrade meddelanden", name="stored_messages", method="store_message", hidden=True),
    ]

    async def store_message(self) -> Message:
        message = Message(text=self.message) if isinstance(self.message, str) else self.message

        message.session_id = self.session_id or message.session_id
        message.sender = self.sender or message.sender or MESSAGE_SENDER_AI
        message.sender_name = self.sender_name or message.sender_name or MESSAGE_SENDER_NAME_AI

        stored_messages: list[Message] = []

        if self.memory:
            self.memory.session_id = message.session_id
            lc_message = message.to_lc_message()
            await self.memory.aadd_messages([lc_message])

            stored_messages = await self.memory.aget_messages() or []

            stored_messages = [Message.from_lc_message(m) for m in stored_messages] if stored_messages else []

            if message.sender:
                stored_messages = [m for m in stored_messages if m.sender == message.sender]
        else:
            await astore_message(message, flow_id=self.graph.flow_id)
            stored_messages = (
                await aget_messages(
                    session_id=message.session_id, sender_name=message.sender_name, sender=message.sender
                )
                or []
            )

        if not stored_messages:
            msg = "Inga meddelanden lagrades. Se till att sessions-ID och avsändare är korrekt inställda."
            raise ValueError(msg)

        stored_message = stored_messages[0]
        self.status = stored_message
        return stored_message

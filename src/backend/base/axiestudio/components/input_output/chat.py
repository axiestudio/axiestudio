from axiestudio.base.data.utils import IMG_FILE_TYPES, TEXT_FILE_TYPES
from axiestudio.base.io.chat import ChatComponent
from axiestudio.inputs.inputs import BoolInput
from axiestudio.io import (
    DropdownInput,
    FileInput,
    MessageTextInput,
    MultilineInput,
    Output,
)
from axiestudio.schema.message import Message
from axiestudio.utils.constants import (
    MESSAGE_SENDER_AI,
    MESSAGE_SENDER_NAME_USER,
    MESSAGE_SENDER_USER,
)


class ChatInput(ChatComponent):
    display_name = "Chattinmatning"
    description = "Hämta chattinmatningar från Playground."
    documentation: str = "https://docs.axiestudio.se/components-io#chat-input"
    icon = "MessagesSquare"
    name = "ChatInput"
    minimized = True

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Inmatningstext",
            value="",
            info="Meddelande som ska skickas som inmatning.",
            input_types=[],
        ),
        BoolInput(
            name="should_store_message",
            display_name="Lagra meddelanden",
            info="Lagra meddelandet i historiken.",
            value=True,
            advanced=True,
        ),
        DropdownInput(
            name="sender",
            display_name="Avsändartyp",
            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],
            value=MESSAGE_SENDER_USER,
            info="Typ av avsändare.",
            advanced=True,
        ),
        MessageTextInput(
            name="sender_name",
            display_name="Avsändarnamn",
            info="Namn på avsändaren.",
            value=MESSAGE_SENDER_NAME_USER,
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="Sessions-ID",
            info="Sessions-ID för chatten. Om tomt kommer den aktuella sessions-ID-parametern att användas.",
            advanced=True,
        ),
        FileInput(
            name="files",
            display_name="Filer",
            file_types=TEXT_FILE_TYPES + IMG_FILE_TYPES,
            info="Filer som ska skickas med meddelandet.",
            advanced=True,
            is_list=True,
            temp_file=True,
        ),
        MessageTextInput(
            name="background_color",
            display_name="Bakgrundsfärg",
            info="Bakgrundsfärgen för ikonen.",
            advanced=True,
        ),
        MessageTextInput(
            name="chat_icon",
            display_name="Ikon",
            info="Ikonen för meddelandet.",
            advanced=True,
        ),
        MessageTextInput(
            name="text_color",
            display_name="Textfärg",
            info="Textfärgen för namnet",
            advanced=True,
        ),
    ]
    outputs = [
        Output(display_name="Chattmeddelande", name="message", method="message_response"),
    ]

    async def message_response(self) -> Message:
        background_color = self.background_color
        text_color = self.text_color
        icon = self.chat_icon

        message = await Message.create(
            text=self.input_value,
            sender=self.sender,
            sender_name=self.sender_name,
            session_id=self.session_id,
            files=self.files,
            properties={
                "background_color": background_color,
                "text_color": text_color,
                "icon": icon,
            },
        )
        if self.session_id and isinstance(message, Message) and self.should_store_message:
            stored_message = await self.send_message(
                message,
            )
            self.message.value = stored_message
            message = stored_message

        self.status = message
        return message

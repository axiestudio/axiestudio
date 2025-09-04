from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageInput, Output
from axiestudio.schema.data import Data
from axiestudio.schema.message import Message


class MessageToDataComponent(Component):
    display_name = "Meddelande till data"
    description = "Konvertera ett meddelande-objekt till ett data-objekt"
    icon = "message-square-share"
    beta = True
    name = "MessagetoData"
    legacy = True

    inputs = [
        MessageInput(
            name="message",
            display_name="Meddelande",
            info="Meddelande-objektet att konvertera till ett data-objekt",
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="convert_message_to_data"),
    ]

    def convert_message_to_data(self) -> Data:
        if isinstance(self.message, Message):
            # Convert Message to Data
            return Data(data=self.message.data)

        msg = "Fel vid konvertering av meddelande till data: Indata måste vara ett meddelande-objekt"
        logger.opt(exception=True).debug(msg)
        self.status = msg
        return Data(data={"error": msg})

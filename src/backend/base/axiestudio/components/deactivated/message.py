from axiestudio.custom.custom_component.custom_component import CustomComponent
from axiestudio.schema.message import Message
from axiestudio.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_USER


class MessageComponent(CustomComponent):
    display_name = "Meddelande"
    description = "Skapar ett Message-objekt givet ett Sessions-ID."
    name = "Message"

    def build_config(self):
        return {
            "sender": {
                "options": [MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],
                "display_name": "Avsändartyp",
            },
            "sender_name": {"display_name": "Avsändarnamn"},
            "text": {"display_name": "Text"},
            "session_id": {
                "display_name": "Sessions-ID",
                "info": "Sessions-ID för chatthistoriken.",
                "input_types": ["Message"],
            },
        }

    def build(
        self,
        sender: str = MESSAGE_SENDER_USER,
        sender_name: str | None = None,
        session_id: str | None = None,
        text: str = "",
    ) -> Message:
        flow_id = self.graph.flow_id if hasattr(self, "graph") else None
        message = Message(text=text, sender=sender, sender_name=sender_name, flow_id=flow_id, session_id=session_id)

        self.status = message
        return message

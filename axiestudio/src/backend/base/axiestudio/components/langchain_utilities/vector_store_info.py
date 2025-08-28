from langchain.agents.agent_toolkits.vectorstore.toolkit import VectorStoreInfo

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import HandleInput, MessageTextInput, MultilineInput
from axiestudio.template.field.base import Output


class VectorStoreInfoComponent(Component):
    display_name = "VectorStore-info"
    description = "Information om en VectorStore"
    name = "VectorStoreInfo"
    legacy: bool = True
    icon = "LangChain"

    inputs = [
        MessageTextInput(
            name="vectorstore_name",
            display_name="Namn",
            info="Namn på VectorStore",
            required=True,
        ),
        MultilineInput(
            name="vectorstore_description",
            display_name="Beskrivning",
            info="Beskrivning av VectorStore",
            required=True,
        ),
        HandleInput(
            name="input_vectorstore",
            display_name="Vektorlager",
            input_types=["VectorStore"],
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Vektorlager-info", name="info", method="build_info"),
    ]

    def build_info(self) -> VectorStoreInfo:
        self.status = {
            "name": self.vectorstore_name,
            "description": self.vectorstore_description,
        }
        return VectorStoreInfo(
            vectorstore=self.input_vectorstore,
            description=self.vectorstore_description,
            name=self.vectorstore_name,
        )

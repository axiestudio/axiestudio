from langchain.chains import ConversationChain

from axiestudio.base.chains.model import LCChainComponent
from axiestudio.field_typing import Message
from axiestudio.inputs.inputs import HandleInput, MultilineInput


class ConversationChainComponent(LCChainComponent):
    display_name = "Konversationskedja"
    description = "Kedja för att ha en konversation och ladda kontext från minne."
    name = "ConversationChain"
    legacy: bool = True
    icon = "LangChain"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Indata",
            info="Indatavärdet att skicka till kedjan.",
            required=True,
        ),
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            input_types=["LanguageModel"],
            required=True,
        ),
        HandleInput(
            name="memory",
            display_name="Minne",
            input_types=["BaseChatMemory"],
        ),
    ]

    def invoke_chain(self) -> Message:
        if not self.memory:
            chain = ConversationChain(llm=self.llm)
        else:
            chain = ConversationChain(llm=self.llm, memory=self.memory)

        result = chain.invoke(
            {"input": self.input_value},
            config={"callbacks": self.get_langchain_callbacks()},
        )
        if isinstance(result, dict):
            result = result.get(chain.output_key, "")

        elif not isinstance(result, str):
            result = result.get("response")
        result = str(result)
        self.status = result
        return Message(text=result)

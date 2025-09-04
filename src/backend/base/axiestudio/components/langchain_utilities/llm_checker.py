from langchain.chains import LLMCheckerChain

from axiestudio.base.chains.model import LCChainComponent
from axiestudio.field_typing import Message
from axiestudio.inputs.inputs import HandleInput, MultilineInput


class LLMCheckerChainComponent(LCChainComponent):
    display_name = "LLM-kontrollkedja"
    description = "Kedja för frågor och svar med självverifiering."
    documentation = "https://python.langchain.com/docs/modules/chains/additional/llm_checker"
    name = "LLMCheckerChain"
    legacy: bool = True
    icon = "LangChain"
    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Inmatning",
            info="Inmatningsvärdet att skicka till kedjan.",
            required=True,
        ),
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            input_types=["LanguageModel"],
            required=True,
        ),
    ]

    def invoke_chain(self) -> Message:
        chain = LLMCheckerChain.from_llm(llm=self.llm)
        response = chain.invoke(
            {chain.input_key: self.input_value},
            config={"callbacks": self.get_langchain_callbacks()},
        )
        result = response.get(chain.output_key, "")
        result = str(result)
        self.status = result
        return Message(text=result)

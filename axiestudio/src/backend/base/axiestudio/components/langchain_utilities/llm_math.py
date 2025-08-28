from langchain.chains import LLMMathChain

from axiestudio.base.chains.model import LCChainComponent
from axiestudio.field_typing import Message
from axiestudio.inputs.inputs import HandleInput, MultilineInput
from axiestudio.template.field.base import Output


class LLMMathChainComponent(LCChainComponent):
    display_name = "LLM-matematikkedja"
    description = "Kedja som tolkar en prompt och kör Python-kod för att göra matematik."
    documentation = "https://python.langchain.com/docs/modules/chains/additional/llm_math"
    name = "LLMMathChain"
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
    ]

    outputs = [Output(display_name="Meddelande", name="text", method="invoke_chain")]

    def invoke_chain(self) -> Message:
        chain = LLMMathChain.from_llm(llm=self.llm)
        response = chain.invoke(
            {chain.input_key: self.input_value},
            config={"callbacks": self.get_langchain_callbacks()},
        )
        result = response.get(chain.output_key, "")
        result = str(result)
        self.status = result
        return Message(text=result)

from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from axiestudio.base.agents.agent import LCToolsAgentComponent
from axiestudio.inputs.inputs import (
    DataInput,
    HandleInput,
    MessageTextInput,
)
from axiestudio.schema.data import Data


class ToolCallingAgentComponent(LCToolsAgentComponent):
    display_name: str = "Verktygsanropande agent"
    description: str = "En agent designad för att använda olika verktyg sömlöst inom arbetsflöden."
    icon = "LangChain"
    name = "ToolCallingAgent"

    inputs = [
        *LCToolsAgentComponent._base_inputs,
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            input_types=["LanguageModel"],
            required=True,
            info="Språkmodell som agenten använder för att utföra uppgifter effektivt.",
        ),
        MessageTextInput(
            name="system_prompt",
            display_name="Systemprompt",
            info="Systemprompt för att vägleda agentens beteende.",
            value="Du är en hjälpsam assistent som kan använda verktyg för att svara på frågor och utföra uppgifter.",
        ),
        DataInput(
            name="chat_history",
            display_name="Chattminne",
            is_list=True,
            advanced=True,
            info="Denna inmatning lagrar chatthistoriken, vilket gör att agenten kan komma ihåg tidigare konversationer.",
        ),
    ]

    def get_chat_history_data(self) -> list[Data] | None:
        return self.chat_history

    def create_agent_runnable(self):
        messages = [
            ("system", "{system_prompt}"),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        self.validate_tool_names()
        try:
            return create_tool_calling_agent(self.llm, self.tools or [], prompt)
        except NotImplementedError as e:
            message = f"{self.display_name} stöder inte verktygsanrop. Vänligen försök använda en kompatibel modell."
            raise NotImplementedError(message) from e

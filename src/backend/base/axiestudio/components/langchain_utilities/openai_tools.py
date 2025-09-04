from langchain.agents import create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate

from axiestudio.base.agents.agent import LCToolsAgentComponent
from axiestudio.inputs.inputs import (
    DataInput,
    HandleInput,
    MultilineInput,
)
from axiestudio.schema.data import Data


class OpenAIToolsAgentComponent(LCToolsAgentComponent):
    display_name: str = "OpenAI-verktygsagent"
    description: str = "Agent som använder verktyg via openai-tools."
    icon = "LangChain"
    name = "OpenAIToolsAgent"

    inputs = [
        *LCToolsAgentComponent._base_inputs,
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            input_types=["LanguageModel", "ToolEnabledLanguageModel"],
            required=True,
        ),
        MultilineInput(
            name="system_prompt",
            display_name="Systemprompt",
            info="Systemprompt för agenten.",
            value="Du är en hjälpsam assistent",
        ),
        MultilineInput(
            name="user_prompt", display_name="Prompt", info="Denna prompt måste innehålla 'input'-nyckeln.", value="{input}"
        ),
        DataInput(name="chat_history", display_name="Chatthistorik", is_list=True, advanced=True),
    ]

    def get_chat_history_data(self) -> list[Data] | None:
        return self.chat_history

    def create_agent_runnable(self):
        if "input" not in self.user_prompt:
            msg = "Prompt måste innehålla 'input'-nyckel."
            raise ValueError(msg)
        messages = [
            ("system", self.system_prompt),
            ("placeholder", "{chat_history}"),
            HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=["input"], template=self.user_prompt)),
            ("placeholder", "{agent_scratchpad}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        return create_openai_tools_agent(self.llm, self.tools, prompt)

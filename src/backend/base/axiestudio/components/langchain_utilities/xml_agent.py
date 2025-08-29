from langchain.agents import create_xml_agent
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate

from axiestudio.base.agents.agent import LCToolsAgentComponent
from axiestudio.inputs.inputs import (
    DataInput,
    HandleInput,
    MultilineInput,
)
from axiestudio.schema.data import Data


class XMLAgentComponent(LCToolsAgentComponent):
    display_name: str = "XML-agent"
    description: str = "Agent som använder verktyg som formaterar instruktioner som xml till språkmodellen."
    icon = "LangChain"
    beta = True
    name = "XMLAgent"
    inputs = [
        *LCToolsAgentComponent._base_inputs,
        HandleInput(name="llm", display_name="Språkmodell", input_types=["LanguageModel"], required=True),
        DataInput(name="chat_history", display_name="Chatthistorik", is_list=True, advanced=True),
        MultilineInput(
            name="system_prompt",
            display_name="Systemprompt",
            info="Systemprompt för agenten.",
            value="""Du är en hjälpsam assistent. Hjälp användaren att svara på alla frågor.

Du har tillgång till följande verktyg:

{tools}

För att använda ett verktyg kan du använda <tool></tool> och <tool_input></tool_input> taggar. Du får sedan tillbaka ett svar i form av <observation></observation>

Till exempel, om du har ett verktyg som heter 'search' som kan köra en google-sökning, för att söka efter vädret i SF skulle du svara:

<tool>search</tool><tool_input>weather in SF</tool_input>

<observation>64 grader</observation>

När du är klar, svara med ett slutgiltigt svar mellan <final_answer></final_answer>. Till exempel:

<final_answer>Vädret i SF är 64 grader</final_answer>

Börja!

Fråga: {input}

{agent_scratchpad}
            """,  # noqa: E501
        ),
        MultilineInput(
            name="user_prompt", display_name="Prompt", info="Denna prompt måste innehålla 'input'-nyckeln.", value="{input}"
        ),
    ]

    def get_chat_history_data(self) -> list[Data] | None:
        return self.chat_history

    def create_agent_runnable(self):
        if "input" not in self.user_prompt:
            msg = "Prompt måste innehålla 'input'-nyckeln."
            raise ValueError(msg)
        messages = [
            ("system", self.system_prompt),
            ("placeholder", "{chat_history}"),
            HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=["input"], template=self.user_prompt)),
            ("ai", "{agent_scratchpad}"),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        return create_xml_agent(self.llm, self.tools, prompt)

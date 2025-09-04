from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent

from axiestudio.base.agents.agent import LCAgentComponent
from axiestudio.field_typing import AgentExecutor
from axiestudio.inputs.inputs import (
    DictInput,
    DropdownInput,
    FileInput,
    HandleInput,
    MessageTextInput,
)
from axiestudio.schema.message import Message
from axiestudio.template.field.base import Output


class CSVAgentComponent(LCAgentComponent):
    display_name = "CSV-agent"
    description = "Konstruera en CSV-agent från en CSV och verktyg."
    documentation = "https://python.langchain.com/docs/modules/agents/toolkits/csv"
    name = "CSVAgent"
    icon = "LangChain"

    inputs = [
        *LCAgentComponent._base_inputs,
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            input_types=["LanguageModel"],
            required=True,
            info="Ett LLM-modellobjekt (Det kan hittas i vilken LLM-komponent som helst).",
        ),
        FileInput(
            name="path",
            display_name="Filsökväg",
            file_types=["csv"],
            input_types=["str", "Message"],
            required=True,
            info="En CSV-fil eller filsökväg.",
        ),
        DropdownInput(
            name="agent_type",
            display_name="Agenttyp",
            advanced=True,
            options=["zero-shot-react-description", "openai-functions", "openai-tools"],
            value="openai-tools",
        ),
        MessageTextInput(
            name="input_value",
            display_name="Text",
            info="Text att skicka som indata och extrahera information från CSV-filen.",
            required=True,
        ),
        DictInput(
            name="pandas_kwargs",
            display_name="Pandas-argument",
            info="Pandas-argument att skicka till agenten.",
            advanced=True,
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="Svar", name="response", method="build_agent_response"),
        Output(display_name="Agent", name="agent", method="build_agent", hidden=True, tool_mode=False),
    ]

    def _path(self) -> str:
        if isinstance(self.path, Message) and isinstance(self.path.text, str):
            return self.path.text
        return self.path

    def build_agent_response(self) -> Message:
        agent_kwargs = {
            "verbose": self.verbose,
            "allow_dangerous_code": True,
        }

        agent_csv = create_csv_agent(
            llm=self.llm,
            path=self._path(),
            agent_type=self.agent_type,
            handle_parsing_errors=self.handle_parsing_errors,
            pandas_kwargs=self.pandas_kwargs,
            **agent_kwargs,
        )

        result = agent_csv.invoke({"input": self.input_value})
        return Message(text=str(result["output"]))

    def build_agent(self) -> AgentExecutor:
        agent_kwargs = {
            "verbose": self.verbose,
            "allow_dangerous_code": True,
        }

        agent_csv = create_csv_agent(
            llm=self.llm,
            path=self._path(),
            agent_type=self.agent_type,
            handle_parsing_errors=self.handle_parsing_errors,
            pandas_kwargs=self.pandas_kwargs,
            **agent_kwargs,
        )

        self.status = Message(text=str(agent_csv))

        return agent_csv

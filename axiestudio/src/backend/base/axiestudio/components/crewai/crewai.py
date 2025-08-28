from axiestudio.base.agents.crewai.crew import convert_llm, convert_tools
from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, DictInput, HandleInput, MultilineInput, Output


class CrewAIAgentComponent(Component):
    """Component for creating a CrewAI agent.

    This component allows you to create a CrewAI agent with the specified role, goal, backstory, tools,
    and language model.

    Args:
        Component (Component): Base class for all components.

    Returns:
        Agent: CrewAI agent.
    """

    display_name = "CrewAI-agent"
    description = "Representerar en agent från CrewAI."
    documentation: str = "https://docs.crewai.com/how-to/LLM-Connections/"
    icon = "CrewAI"
    legacy = True

    inputs = [
        MultilineInput(name="role", display_name="Roll", info="Agentens roll."),
        MultilineInput(name="goal", display_name="Mål", info="Agentens mål."),
        MultilineInput(name="backstory", display_name="Bakgrund", info="Agentens bakgrund."),
        HandleInput(
            name="tools",
            display_name="Verktyg",
            input_types=["Tool"],
            is_list=True,
            info="Verktyg som agenten har tillgång till",
            value=[],
        ),
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            info="Språkmodellen som kommer att köra agenten.",
            input_types=["LanguageModel"],
        ),
        BoolInput(
            name="memory",
            display_name="Memory",
            info="Whether the agent should have memory or not",
            advanced=True,
            value=True,
        ),
        BoolInput(
            name="verbose",
            display_name="Verbose",
            advanced=True,
            value=False,
        ),
        BoolInput(
            name="allow_delegation",
            display_name="Allow Delegation",
            info="Whether the agent is allowed to delegate tasks to other agents.",
            value=True,
        ),
        BoolInput(
            name="allow_code_execution",
            display_name="Allow Code Execution",
            info="Whether the agent is allowed to execute code.",
            value=False,
            advanced=True,
        ),
        DictInput(
            name="kwargs",
            display_name="kwargs",
            info="kwargs of agent.",
            is_list=True,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Agent", name="output", method="build_output"),
    ]

    def build_output(self):
        try:
            from crewai import Agent
        except ImportError as e:
            msg = "CrewAI is not installed. Please install it with `uv pip install crewai`."
            raise ImportError(msg) from e

        kwargs = self.kwargs or {}

        # Define the Agent
        agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            llm=convert_llm(self.llm),
            verbose=self.verbose,
            memory=self.memory,
            tools=convert_tools(self.tools),
            allow_delegation=self.allow_delegation,
            allow_code_execution=self.allow_code_execution,
            **kwargs,
        )

        self.status = repr(agent)

        return agent

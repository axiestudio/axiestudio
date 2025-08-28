from axiestudio.components.agents.agent import AgentComponent
from axiestudio.components.helpers.calculator_core import CalculatorComponent
from axiestudio.components.input_output import ChatInput, ChatOutput
from axiestudio.components.processing.python_repl_core import PythonREPLComponent
from axiestudio.graph import Graph


def simple_agent_graph():
    """Create a simple but powerful starter agent with calculator and Python REPL tools."""

    # Create input component
    chat_input = ChatInput()

    # Create tools
    calculator = CalculatorComponent()
    python_repl = PythonREPLComponent()

    # Create agent with tools
    agent = AgentComponent()
    agent.set(
        input_value=chat_input.message_response,
        tools=[calculator.component_as_tool, python_repl.component_as_tool],
        agent_llm="OpenAI",
        system_message="Du är en hjälpsam AI-assistent med tillgång till verktyg. Använd verktygen när det behövs för att hjälpa användaren.",
    )

    # Create output component
    chat_output = ChatOutput()
    chat_output.set(input_value=agent.response)

    return Graph(start=chat_input, end=chat_output)

from axiestudio.base.agents.crewai.crew import BaseCrewComponent
from axiestudio.io import HandleInput


class HierarchicalCrewComponent(BaseCrewComponent):
    display_name: str = "Hierarkisk besättning"
    description: str = (
        "Representerar en grupp agenter, definierar hur de ska samarbeta och vilka uppgifter de ska utföra."
    )
    documentation: str = "https://docs.crewai.com/how-to/Hierarchical/"
    icon = "CrewAI"
    legacy = True

    inputs = [
        *BaseCrewComponent._base_inputs,
        HandleInput(name="agents", display_name="Agenter", input_types=["Agent"], is_list=True),
        HandleInput(name="tasks", display_name="Uppgifter", input_types=["HierarchicalTask"], is_list=True),
        HandleInput(name="manager_llm", display_name="Chef-LLM", input_types=["LanguageModel"], required=False),
        HandleInput(name="manager_agent", display_name="Chefagent", input_types=["Agent"], required=False),
    ]

    def build_crew(self):
        try:
            from crewai import Crew, Process
        except ImportError as e:
            msg = "CrewAI is not installed. Please install it with `uv pip install crewai`."
            raise ImportError(msg) from e

        tasks, agents = self.get_tasks_and_agents()
        manager_llm = self.get_manager_llm()

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.hierarchical,
            verbose=self.verbose,
            memory=self.memory,
            cache=self.use_cache,
            max_rpm=self.max_rpm,
            share_crew=self.share_crew,
            function_calling_llm=self.function_calling_llm,
            manager_agent=self.manager_agent,
            manager_llm=manager_llm,
            step_callback=self.get_step_callback(),
            task_callback=self.get_task_callback(),
        )

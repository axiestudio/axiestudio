from axiestudio.base.agents.crewai.tasks import SequentialTask
from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, HandleInput, MultilineInput, Output


class SequentialTaskComponent(Component):
    display_name: str = "Sekventiell uppgift"
    description: str = "Varje uppgift måste ha en beskrivning, en förväntad utdata och en agent ansvarig för utförandet."
    icon = "CrewAI"
    legacy = True
    inputs = [
        MultilineInput(
            name="task_description",
            display_name="Beskrivning",
            info="Beskrivande text som detaljerar uppgiftens syfte och utförande.",
        ),
        MultilineInput(
            name="expected_output",
            display_name="Förväntad utdata",
            info="Tydlig definition av förväntat uppgiftsresultat.",
        ),
        HandleInput(
            name="tools",
            display_name="Verktyg",
            input_types=["Tool"],
            is_list=True,
            info="Lista över verktyg/resurser begränsade för uppgiftsutförande. Använder agentverktygen som standard.",
            required=False,
            advanced=True,
        ),
        HandleInput(
            name="agent",
            display_name="Agent",
            input_types=["Agent"],
            info="CrewAI-agent som kommer att utföra uppgiften",
            required=True,
        ),
        HandleInput(
            name="task",
            display_name="Uppgift",
            input_types=["SequentialTask"],
            info="CrewAI-uppgift som kommer att utföra uppgiften",
        ),
        BoolInput(
            name="async_execution",
            display_name="Asynkron utförande",
            value=True,
            advanced=True,
            info="Boolesk flagga som indikerar asynkront uppgiftsutförande.",
        ),
    ]

    outputs = [
        Output(display_name="Task", name="task_output", method="build_task"),
    ]

    def build_task(self) -> list[SequentialTask]:
        tasks: list[SequentialTask] = []
        task = SequentialTask(
            description=self.task_description,
            expected_output=self.expected_output,
            tools=self.agent.tools,
            async_execution=False,
            agent=self.agent,
        )
        tasks.append(task)
        self.status = task
        if self.task:
            if isinstance(self.task, list) and all(isinstance(task_item, SequentialTask) for task_item in self.task):
                tasks = self.task + tasks
            elif isinstance(self.task, SequentialTask):
                tasks = [self.task, *tasks]
        return tasks

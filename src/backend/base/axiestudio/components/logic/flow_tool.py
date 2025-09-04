from typing import Any

from loguru import logger
from typing_extensions import override

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.base.tools.flow_tool import FlowTool
from axiestudio.field_typing import Tool
from axiestudio.graph.graph.base import Graph
from axiestudio.helpers.flow import get_flow_inputs
from axiestudio.io import BoolInput, DropdownInput, Output, StrInput
from axiestudio.schema.data import Data
from axiestudio.schema.dotdict import dotdict


class FlowToolComponent(LCToolComponent):
    display_name = "Flöde som verktyg [Föråldrad]"
    description = "Konstruera ett verktyg från en funktion som kör det laddade flödet."
    field_order = ["flow_name", "name", "description", "return_direct"]
    trace_type = "tool"
    name = "FlowTool"
    legacy: bool = True
    icon = "hammer"

    async def get_flow_names(self) -> list[str]:
        flow_datas = await self.alist_flows()
        return [flow_data.data["name"] for flow_data in flow_datas]

    async def get_flow(self, flow_name: str) -> Data | None:
        """Retrieves a flow by its name.

        Args:
            flow_name (str): The name of the flow to retrieve.

        Returns:
            Optional[Text]: The flow record if found, None otherwise.
        """
        flow_datas = await self.alist_flows()
        for flow_data in flow_datas:
            if flow_data.data["name"] == flow_name:
                return flow_data
        return None

    @override
    async def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        if field_name == "flow_name":
            build_config["flow_name"]["options"] = self.get_flow_names()

        return build_config

    inputs = [
        DropdownInput(
            name="flow_name", display_name="Flödesnamn", info="Namnet på flödet att köra.", refresh_button=True
        ),
        StrInput(
            name="tool_name",
            display_name="Namn",
            info="Namnet på verktyget.",
        ),
        StrInput(
            name="tool_description",
            display_name="Beskrivning",
            info="Beskrivningen av verktyget; standardvärdet är flödets beskrivning.",
        ),
        BoolInput(
            name="return_direct",
            display_name="Returnera direkt",
            info="Returnera resultatet direkt från verktyget.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(name="api_build_tool", display_name="Verktyg", method="build_tool"),
    ]

    async def build_tool(self) -> Tool:
        FlowTool.model_rebuild()
        if "flow_name" not in self._attributes or not self._attributes["flow_name"]:
            msg = "Flödesnamn krävs"
            raise ValueError(msg)
        flow_name = self._attributes["flow_name"]
        flow_data = await self.get_flow(flow_name)
        if not flow_data:
            msg = "Flöde hittades inte."
            raise ValueError(msg)
        graph = Graph.from_payload(
            flow_data.data["data"],
            user_id=str(self.user_id),
        )
        try:
            graph.set_run_id(self.graph.run_id)
        except Exception:  # noqa: BLE001
            logger.opt(exception=True).warning("Misslyckades att sätta run_id")
        inputs = get_flow_inputs(graph)
        tool_description = self.tool_description.strip() or flow_data.description
        tool = FlowTool(
            name=self.tool_name,
            description=tool_description,
            graph=graph,
            return_direct=self.return_direct,
            inputs=inputs,
            flow_id=str(flow_data.id),
            user_id=str(self.user_id),
            session_id=self.graph.session_id if hasattr(self, "graph") else None,
        )
        description_repr = repr(tool.description).strip("'")
        args_str = "\n".join([f"- {arg_name}: {arg_data['description']}" for arg_name, arg_data in tool.args.items()])
        self.status = f"{description_repr}\nArgument:\n{args_str}"
        return tool

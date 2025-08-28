from axiestudio.custom.custom_component.custom_component import CustomComponent
from axiestudio.schema.data import Data


class ListFlowsComponent(CustomComponent):
    display_name = "Lista flöden"
    description = "En komponent för att lista alla tillgängliga flöden."
    icon = "ListFlows"
    beta: bool = True
    name = "ListFlows"

    def build_config(self):
        return {}

    async def build(
        self,
    ) -> list[Data]:
        flows = await self.alist_flows()
        self.status = flows
        return flows

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import HandleInput
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.template.field.base import Output


class LoopComponent(Component):
    display_name = "Slinga"
    description = (
        "Itererar över en lista med Data-objekt, matar ut ett objekt i taget och aggregerar resultat från slingans inmatningar."
    )
    documentation: str = "https://docs.axiestudio.se/components-logic#loop"
    icon = "infinity"

    inputs = [
        HandleInput(
            name="data",
            display_name="Inmatningar",
            info="Den initiala listan med Data-objekt eller DataFrame att iterera över.",
            input_types=["DataFrame"],
        ),
    ]

    outputs = [
        Output(display_name="Objekt", name="item", method="item_output", allows_loop=True, group_outputs=True),
        Output(display_name="Klar", name="done", method="done_output", group_outputs=True),
    ]

    def initialize_data(self) -> None:
        """Initialisera datalistan, kontextindex och aggregerad lista."""
        if self.ctx.get(f"{self._id}_initialized", False):
            return

        # Säkerställ att data är en lista med Data-objekt
        data_list = self._validate_data(self.data)

        # Lagra den initiala datan och kontextvariabler
        self.update_ctx(
            {
                f"{self._id}_data": data_list,
                f"{self._id}_index": 0,
                f"{self._id}_aggregated": [],
                f"{self._id}_initialized": True,
            }
        )

    def _validate_data(self, data):
        """Validera och returnera en lista med Data-objekt."""
        if isinstance(data, DataFrame):
            return data.to_data_list()
        if isinstance(data, Data):
            return [data]
        if isinstance(data, list) and all(isinstance(item, Data) for item in data):
            return data
        msg = "'data'-inmatningen måste vara en DataFrame, en lista med Data-objekt eller ett enskilt Data-objekt."
        raise TypeError(msg)

    def evaluate_stop_loop(self) -> bool:
        """Utvärdera om objekt- eller klar-utmatning ska stoppas."""
        current_index = self.ctx.get(f"{self._id}_index", 0)
        data_length = len(self.ctx.get(f"{self._id}_data", []))
        return current_index > data_length

    def item_output(self) -> Data:
        """Mata ut nästa objekt i listan eller stoppa om klar."""
        self.initialize_data()
        current_item = Data(text="")

        if self.evaluate_stop_loop():
            self.stop("item")
        else:
            # Hämta datalista och aktuellt index
            data_list, current_index = self.loop_variables()
            if current_index < len(data_list):
                # Mata ut aktuellt objekt och öka index
                try:
                    current_item = data_list[current_index]
                except IndexError:
                    current_item = Data(text="")
            self.aggregated_output()
            self.update_ctx({f"{self._id}_index": current_index + 1})

        # Nu behöver vi uppdatera beroenden för nästa körning
        self.update_dependency()
        return current_item

    def update_dependency(self):
        item_dependency_id = self.get_incoming_edge_by_target_param("item")
        if item_dependency_id not in self.graph.run_manager.run_predecessors[self._id]:
            self.graph.run_manager.run_predecessors[self._id].append(item_dependency_id)

    def done_output(self) -> DataFrame:
        """Utlös klar-utmatningen när iterationen är slutförd."""
        self.initialize_data()

        if self.evaluate_stop_loop():
            self.stop("item")
            self.start("done")

            aggregated = self.ctx.get(f"{self._id}_aggregated", [])

            return DataFrame(aggregated)
        self.stop("done")
        return DataFrame([])

    def loop_variables(self):
        """Hämta slingvariabler från kontext."""
        return (
            self.ctx.get(f"{self._id}_data", []),
            self.ctx.get(f"{self._id}_index", 0),
        )

    def aggregated_output(self) -> list[Data]:
        """Returnera den aggregerade listan när alla objekt är bearbetade."""
        self.initialize_data()

        # Hämta datalista och aggregerad lista
        data_list = self.ctx.get(f"{self._id}_data", [])
        aggregated = self.ctx.get(f"{self._id}_aggregated", [])
        loop_input = self.item
        if loop_input is not None and not isinstance(loop_input, str) and len(aggregated) <= len(data_list):
            aggregated.append(loop_input)
            self.update_ctx({f"{self._id}_aggregated": aggregated})
        return aggregated

from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing import Embeddings
from axiestudio.io import Output


class LCEmbeddingsModel(Component):
    trace_type = "embedding"

    outputs = [
        Output(display_name="Inbäddningsmodell", name="embeddings", method="build_embeddings"),
    ]

    def _validate_outputs(self) -> None:
        required_output_methods = ["build_embeddings"]
        output_names = [output.name for output in self.outputs]
        for method_name in required_output_methods:
            if method_name not in output_names:
                msg = f"Output med namnet '{method_name}' måste definieras."
                raise ValueError(msg)
            if not hasattr(self, method_name):
                msg = f"Metoden '{method_name}' måste definieras."
                raise ValueError(msg)

    def build_embeddings(self) -> Embeddings:
        msg = "Du måste implementera build_embeddings-metoden i din klass."
        raise NotImplementedError(msg)

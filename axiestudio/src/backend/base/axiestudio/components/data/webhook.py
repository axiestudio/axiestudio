import json

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MultilineInput, Output
from axiestudio.schema.data import Data


class WebhookComponent(Component):
    display_name = "Webhook"
    documentation: str = "https://docs.axiestudio.org/components-data#webhook"
    name = "Webhook"
    icon = "webhook"

    inputs = [
        MultilineInput(
            name="data",
            display_name="Nyttolast",
            info="Tar emot en nyttolast från externa system via HTTP POST.",
            advanced=True,
        ),
        MultilineInput(
            name="curl",
            display_name="cURL",
            value="CURL_WEBHOOK",
            advanced=True,
            input_types=[],
        ),
        MultilineInput(
            name="endpoint",
            display_name="Slutpunkt",
            value="BACKEND_URL",
            advanced=False,
            copy_field=True,
            input_types=[],
        ),
    ]
    outputs = [
        Output(display_name="Data", name="output_data", method="build_data"),
    ]

    def build_data(self) -> Data:
        message: str | Data = ""
        if not self.data:
            self.status = "Ingen data angiven."
            return Data(data={})
        try:
            my_data = self.data.replace('"\n"', '"\\n"')
            body = json.loads(my_data or "{}")
        except json.JSONDecodeError:
            body = {"payload": self.data}
            message = f"Ogiltig JSON-nyttolast. Vänligen kontrollera formatet.\n\n{self.data}"
        data = Data(data=body)
        if not message:
            message = data
        self.status = message
        return data

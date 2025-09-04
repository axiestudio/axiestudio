import requests
from requests.auth import HTTPBasicAuth

from axiestudio.base.models.openai_constants import OPENAI_CHAT_MODEL_NAMES
from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import DropdownInput, SecretStrInput, StrInput
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema.data import Data
from axiestudio.schema.message import Message


class CombinatorialReasonerComponent(Component):
    display_name = "Kombinatorisk resonerare"
    description = "Använder kombinatorisk optimering för att konstruera en optimal prompt med inbäddade skäl. Registrera dig här:\nhttps://forms.gle/oWNv2NKjBNaqqvCx6"
    icon = "Icosa"
    name = "Combinatorial Reasoner"

    inputs = [
        MessageTextInput(name="prompt", display_name="Prompt", required=True),
        SecretStrInput(
            name="openai_api_key",
            display_name="OpenAI API-nyckel",
            info="OpenAI API-nyckeln att använda för OpenAI-modellen.",
            advanced=False,
            value="OPENAI_API_KEY",
            required=True,
        ),
        StrInput(
            name="username",
            display_name="Användarnamn",
            info="Användarnamn för att autentisera åtkomst till Icosa CR API",
            advanced=False,
            required=True,
        ),
        SecretStrInput(
            name="password",
            display_name="Lösenord",
            info="Lösenord för att autentisera åtkomst till Icosa CR API.",
            advanced=False,
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Modellnamn",
            advanced=False,
            options=OPENAI_CHAT_MODEL_NAMES,
            value=OPENAI_CHAT_MODEL_NAMES[0],
        ),
    ]

    outputs = [
        Output(
            display_name="Optimerad prompt",
            name="optimized_prompt",
            method="build_prompt",
        ),
        Output(display_name="Valda skäl", name="reasons", method="build_reasons"),
    ]

    def build_prompt(self) -> Message:
        params = {
            "prompt": self.prompt,
            "apiKey": self.openai_api_key,
            "model": self.model_name,
        }

        creds = HTTPBasicAuth(self.username, password=self.password)
        response = requests.post(
            "https://cr-api.icosacomputing.com/cr/langflow",
            json=params,
            auth=creds,
            timeout=100,
        )
        response.raise_for_status()

        prompt = response.json()["prompt"]

        self.reasons = response.json()["finalReasons"]
        return prompt

    def build_reasons(self) -> Data:
        # list of selected reasons
        final_reasons = [reason[0] for reason in self.reasons]
        return Data(value=final_reasons)

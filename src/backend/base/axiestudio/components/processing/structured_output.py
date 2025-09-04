from pydantic import BaseModel, Field, create_model
from trustcall import create_extractor

from axiestudio.base.models.chat_result import get_chat_result
from axiestudio.custom.custom_component.component import Component
from axiestudio.helpers.base_model import build_model_from_schema
from axiestudio.io import (
    HandleInput,
    MessageTextInput,
    MultilineInput,
    Output,
    TableInput,
)
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.schema.table import EditMode


class StructuredOutputComponent(Component):
    display_name = "Strukturerad utdata"
    description = "Använder en LLM för att generera strukturerade data. Ideal för extrahering och konsekvens."
    documentation: str = "https://docs.axiestudio.se/components-processing#structured-output"
    name = "StructuredOutput"
    icon = "braces"

    inputs = [
        HandleInput(
            name="llm",
            display_name="Språkmodell",
            info="Språkmodellen att använda för att generera strukturerad utdata.",
            input_types=["LanguageModel"],
            required=True,
        ),
        MultilineInput(
            name="input_value",
            display_name="Indata",
            info="Indata till språkmodellen.",
            tool_mode=True,
            required=True,
        ),
        MultilineInput(
            name="system_prompt",
            display_name="Formateringsinstruktioner",
            info="Instruktioner till språkmodellen för att formatera utdata.",
            value=(
                "You are an AI that extracts structured JSON objects from unstructured text. "
                "Use a predefined schema with expected types (str, int, float, bool, dict). "
                "Extract ALL relevant instances that match the schema - if multiple patterns exist, capture them all. "
                "Fill missing or ambiguous values with defaults: null for missing values. "
                "Remove exact duplicates but keep variations that have different field values. "
                "Always return valid JSON in the expected format, never throw errors. "
                "If multiple objects can be extracted, return them all in the structured format."
            ),
            required=True,
            advanced=True,
        ),
        MessageTextInput(
            name="schema_name",
            display_name="Schemanamn",
            info="Ange ett namn för utdataschemat.",
            advanced=True,
        ),
        TableInput(
            name="output_schema",
            display_name="Utdataschema",
            info="Definiera strukturen och datatyperna för modellens utdata.",
            required=True,
            # TODO: remove deault value
            table_schema=[
                {
                    "name": "name",
                    "display_name": "Namn",
                    "type": "str",
                    "description": "Ange namnet på utdatafältet.",
                    "default": "field",
                    "edit_mode": EditMode.INLINE,
                },
                {
                    "name": "description",
                    "display_name": "Beskrivning",
                    "type": "str",
                    "description": "Beskriv syftet med utdatafältet.",
                    "default": "description of field",
                    "edit_mode": EditMode.POPOVER,
                },
                {
                    "name": "type",
                    "display_name": "Typ",
                    "type": "str",
                    "edit_mode": EditMode.INLINE,
                    "description": ("Ange datatypen för utdatafältet (t.ex. str, int, float, bool, dict)."),
                    "options": ["str", "int", "float", "bool", "dict"],
                    "default": "str",
                },
                {
                    "name": "multiple",
                    "display_name": "As List",
                    "type": "boolean",
                    "description": "Set to True if this output field should be a list of the specified type.",
                    "default": "False",
                    "edit_mode": EditMode.INLINE,
                },
            ],
            value=[
                {
                    "name": "field",
                    "description": "description of field",
                    "type": "str",
                    "multiple": "False",
                }
            ],
        ),
    ]

    outputs = [
        Output(
            name="structured_output",
            display_name="Strukturerad utdata",
            method="build_structured_output",
        ),
        Output(
            name="dataframe_output",
            display_name="Strukturerad utdata",
            method="build_structured_dataframe",
        ),
    ]

    def build_structured_output_base(self):
        schema_name = self.schema_name or "OutputModel"

        if not hasattr(self.llm, "with_structured_output"):
            msg = "Language model does not support structured output."
            raise TypeError(msg)
        if not self.output_schema:
            msg = "Output schema cannot be empty"
            raise ValueError(msg)

        output_model_ = build_model_from_schema(self.output_schema)

        output_model = create_model(
            schema_name,
            __doc__=f"A list of {schema_name}.",
            objects=(list[output_model_], Field(description=f"A list of {schema_name}.")),  # type: ignore[valid-type]
        )

        try:
            llm_with_structured_output = create_extractor(self.llm, tools=[output_model])
        except NotImplementedError as exc:
            msg = f"{self.llm.__class__.__name__} does not support structured output."
            raise TypeError(msg) from exc

        config_dict = {
            "run_name": self.display_name,
            "project_name": self.get_project_name(),
            "callbacks": self.get_langchain_callbacks(),
        }
        result = get_chat_result(
            runnable=llm_with_structured_output,
            system_message=self.system_prompt,
            input_value=self.input_value,
            config=config_dict,
        )

        # OPTIMIZATION NOTE: Simplified processing based on trustcall response structure
        # Handle non-dict responses (shouldn't happen with trustcall, but defensive)
        if not isinstance(result, dict):
            return result

        # Extract first response and convert BaseModel to dict
        responses = result.get("responses", [])
        if not responses:
            return result

        # Convert BaseModel to dict (creates the "objects" key)
        first_response = responses[0]
        structured_data = first_response.model_dump() if isinstance(first_response, BaseModel) else first_response

        # Extract the objects array (guaranteed to exist due to our Pydantic model structure)
        return structured_data.get("objects", structured_data)

    def build_structured_output(self) -> Data:
        output = self.build_structured_output_base()
        if not isinstance(output, list) or not output:
            # handle empty or unexpected type case
            msg = "No structured output returned"
            raise ValueError(msg)
        if len(output) == 1:
            return Data(data=output[0])
        if len(output) > 1:
            # Multiple outputs - wrap them in a results container
            return Data(data={"results": output})
        return Data()

    def build_structured_dataframe(self) -> DataFrame:
        output = self.build_structured_output_base()
        if not isinstance(output, list) or not output:
            # handle empty or unexpected type case
            msg = "No structured output returned"
            raise ValueError(msg)
        data_list = [Data(data=output[0])] if len(output) == 1 else [Data(data=item) for item in output]

        return DataFrame(data_list)

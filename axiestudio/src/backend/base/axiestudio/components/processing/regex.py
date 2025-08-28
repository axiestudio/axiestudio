import re

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema.data import Data
from axiestudio.schema.message import Message


class RegexExtractorComponent(Component):
    display_name = "Regex-extraktor"
    description = "Extrahera mönster från text med reguljära uttryck."
    icon = "regex"
    legacy = True

    inputs = [
        MessageTextInput(
            name="input_text",
            display_name="Inmatningstext",
            info="Texten att analysera",
            required=True,
        ),
        MessageTextInput(
            name="pattern",
            display_name="Regex-mönster",
            info="Det reguljära uttrycksmönstret att matcha",
            value=r"",
            required=True,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="extract_matches"),
        Output(display_name="Meddelande", name="text", method="get_matches_text"),
    ]

    def extract_matches(self) -> list[Data]:
        if not self.pattern or not self.input_text:
            self.status = []
            return []

        try:
            # Compile regex pattern
            pattern = re.compile(self.pattern)

            # Find all matches in the input text
            matches = pattern.findall(self.input_text)

            # Filter out empty matches
            filtered_matches = [match for match in matches if match]  # Remove empty matches

            # Return empty list for no matches, or list of matches if found
            result: list = [] if not filtered_matches else [Data(data={"match": match}) for match in filtered_matches]

        except re.error as e:
            error_message = f"Ogiltigt regex-mönster: {e!s}"
            result = [Data(data={"error": error_message})]
        except ValueError as e:
            error_message = f"Fel vid extrahering av matchningar: {e!s}"
            result = [Data(data={"error": error_message})]

        self.status = result
        return result

    def get_matches_text(self) -> Message:
        """Get matches as a formatted text message."""
        matches = self.extract_matches()

        if not matches:
            message = Message(text="Inga matchningar hittades")
            self.status = message
            return message

        if "error" in matches[0].data:
            message = Message(text=matches[0].data["error"])
            self.status = message
            return message

        result = "\n".join(match.data["match"] for match in matches)
        message = Message(text=result)
        self.status = message
        return message

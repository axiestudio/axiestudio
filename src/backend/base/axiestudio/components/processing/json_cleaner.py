import json
import unicodedata

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import BoolInput, MessageTextInput
from axiestudio.schema.message import Message
from axiestudio.template.field.base import Output


class JSONCleaner(Component):
    icon = "braces"
    display_name = "JSON-rensare"
    description = (
        "Rensar röriga och ibland felaktiga JSON-strängar som produceras av LLM:er "
        "så att de är fullt kompatibla med JSON-specifikationen."
    )
    legacy = True
    inputs = [
        MessageTextInput(
            name="json_str", display_name="JSON-sträng", info="JSON-strängen som ska rensas.", required=True
        ),
        BoolInput(
            name="remove_control_chars",
            display_name="Ta bort kontrolltecken",
            info="Ta bort kontrolltecken från JSON-strängen.",
            required=False,
        ),
        BoolInput(
            name="normalize_unicode",
            display_name="Normalisera Unicode",
            info="Normalisera Unicode-tecken i JSON-strängen.",
            required=False,
        ),
        BoolInput(
            name="validate_json",
            display_name="Validera JSON",
            info="Validera JSON-strängen för att säkerställa att den är välformad.",
            required=False,
        ),
    ]

    outputs = [
        Output(display_name="Rensad JSON-sträng", name="output", method="clean_json"),
    ]

    def clean_json(self) -> Message:
        try:
            from json_repair import repair_json
        except ImportError as e:
            msg = "Kunde inte importera json_repair-paketet. Vänligen installera det med `pip install json_repair`."
            raise ImportError(msg) from e

        """Clean the input JSON string based on provided options and return the cleaned JSON string."""
        json_str = self.json_str
        remove_control_chars = self.remove_control_chars
        normalize_unicode = self.normalize_unicode
        validate_json = self.validate_json

        start = json_str.find("{")
        end = json_str.rfind("}")
        if start == -1 or end == -1:
            msg = "Ogiltig JSON-sträng: Saknar '{' eller '}'"
            raise ValueError(msg)
        try:
            json_str = json_str[start : end + 1]

            if remove_control_chars:
                json_str = self._remove_control_characters(json_str)
            if normalize_unicode:
                json_str = self._normalize_unicode(json_str)
            if validate_json:
                json_str = self._validate_json(json_str)

            cleaned_json_str = repair_json(json_str)
            result = str(cleaned_json_str)

            self.status = result
            return Message(text=result)
        except Exception as e:
            msg = f"Fel vid rensning av JSON-sträng: {e}"
            raise ValueError(msg) from e

    def _remove_control_characters(self, s: str) -> str:
        """Remove control characters from the string."""
        return s.translate(self.translation_table)

    def _normalize_unicode(self, s: str) -> str:
        """Normalize Unicode characters in the string."""
        return unicodedata.normalize("NFC", s)

    def _validate_json(self, s: str) -> str:
        """Validate the JSON string."""
        try:
            json.loads(s)
        except json.JSONDecodeError as e:
            msg = f"Ogiltig JSON-sträng: {e}"
            raise ValueError(msg) from e
        return s

    def __init__(self, *args, **kwargs):
        # Create a translation table that maps control characters to None
        super().__init__(*args, **kwargs)
        self.translation_table = str.maketrans("", "", "".join(chr(i) for i in range(32)) + chr(127))

from pathlib import Path

import assemblyai as aai
from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, DropdownInput, FileInput, MessageTextInput, Output, SecretStrInput
from axiestudio.schema.data import Data


class AssemblyAITranscriptionJobCreator(Component):
    display_name = "AssemblyAI Starta transkription"
    description = "Skapa ett transkriptionsjobb för en ljudfil med AssemblyAI med avancerade alternativ"
    documentation = "https://www.assemblyai.com/docs"
    icon = "AssemblyAI"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="Assembly API-nyckel",
            info="Din AssemblyAI API-nyckel. Du kan få en från https://www.assemblyai.com/",
            required=True,
        ),
        FileInput(
            name="audio_file",
            display_name="Ljudfil",
            file_types=[
                "3ga",
                "8svx",
                "aac",
                "ac3",
                "aif",
                "aiff",
                "alac",
                "amr",
                "ape",
                "au",
                "dss",
                "flac",
                "flv",
                "m4a",
                "m4b",
                "m4p",
                "m4r",
                "mp3",
                "mpga",
                "ogg",
                "oga",
                "mogg",
                "opus",
                "qcp",
                "tta",
                "voc",
                "wav",
                "wma",
                "wv",
                "webm",
                "mts",
                "m2ts",
                "ts",
                "mov",
                "mp2",
                "mp4",
                "m4p",
                "m4v",
                "mxf",
            ],
            info="Ljudfilen att transkribera",
            required=True,
        ),
        MessageTextInput(
            name="audio_file_url",
            display_name="Ljudfil-URL",
            info="URL:en för ljudfilen att transkribera (Kan användas istället för en fil)",
            advanced=True,
        ),
        DropdownInput(
            name="speech_model",
            display_name="Talmodell",
            options=[
                "best",
                "nano",
            ],
            value="best",
            info="Talmodellen att använda för transkriptionen",
            advanced=True,
        ),
        BoolInput(
            name="language_detection",
            display_name="Automatisk språkdetektering",
            info="Aktivera automatisk språkdetektering",
            advanced=True,
        ),
        MessageTextInput(
            name="language_code",
            display_name="Språk",
            info=(
                """
            Språket för ljudfilen. Kan ställas in manuellt om automatisk språkdetektering är inaktiverad.
            Se https://www.assemblyai.com/docs/getting-started/supported-languages """
                "för en lista över språkkoder som stöds."
            ),
            advanced=True,
        ),
        BoolInput(
            name="speaker_labels",
            display_name="Aktivera talaretiketter",
            info="Aktivera talaridentifiering",
        ),
        MessageTextInput(
            name="speakers_expected",
            display_name="Förväntat antal talare",
            info="Ange förväntat antal talare (valfritt, ange ett nummer)",
            advanced=True,
        ),
        BoolInput(
            name="punctuate",
            display_name="Interpunktion",
            info="Aktivera automatisk interpunktion",
            advanced=True,
            value=True,
        ),
        BoolInput(
            name="format_text",
            display_name="Formatera text",
            info="Aktivera textformatering",
            advanced=True,
            value=True,
        ),
    ]

    outputs = [
        Output(display_name="Transkript-ID", name="transcript_id", method="create_transcription_job"),
    ]

    def create_transcription_job(self) -> Data:
        aai.settings.api_key = self.api_key

        # Convert speakers_expected to int if it's not empty
        speakers_expected = None
        if self.speakers_expected and self.speakers_expected.strip():
            try:
                speakers_expected = int(self.speakers_expected)
            except ValueError:
                self.status = "Error: Expected Number of Speakers must be a valid integer"
                return Data(data={"error": "Error: Expected Number of Speakers must be a valid integer"})

        language_code = self.language_code or None

        config = aai.TranscriptionConfig(
            speech_model=self.speech_model,
            language_detection=self.language_detection,
            language_code=language_code,
            speaker_labels=self.speaker_labels,
            speakers_expected=speakers_expected,
            punctuate=self.punctuate,
            format_text=self.format_text,
        )

        audio = None
        if self.audio_file:
            if self.audio_file_url:
                logger.warning("Both an audio file an audio URL were specified. The audio URL was ignored.")

            # Check if the file exists
            if not Path(self.audio_file).exists():
                self.status = "Error: Audio file not found"
                return Data(data={"error": "Error: Audio file not found"})
            audio = self.audio_file
        elif self.audio_file_url:
            audio = self.audio_file_url
        else:
            self.status = "Error: Either an audio file or an audio URL must be specified"
            return Data(data={"error": "Error: Either an audio file or an audio URL must be specified"})

        try:
            transcript = aai.Transcriber().submit(audio, config=config)
        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Error submitting transcription job")
            self.status = f"An error occurred: {e}"
            return Data(data={"error": f"An error occurred: {e}"})

        if transcript.error:
            self.status = transcript.error
            return Data(data={"error": transcript.error})
        result = Data(data={"transcript_id": transcript.id})
        self.status = result
        return result

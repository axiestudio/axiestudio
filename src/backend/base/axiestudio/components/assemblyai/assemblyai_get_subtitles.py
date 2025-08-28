import assemblyai as aai
from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataInput, DropdownInput, IntInput, Output, SecretStrInput
from axiestudio.schema.data import Data


class AssemblyAIGetSubtitles(Component):
    display_name = "AssemblyAI Hämta undertexter"
    description = "Exportera din transkription i SRT- eller VTT-format för undertexter och textning"
    documentation = "https://www.assemblyai.com/docs"
    icon = "AssemblyAI"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="Assembly API-nyckel",
            info="Din AssemblyAI API-nyckel. Du kan få en från https://www.assemblyai.com/",
            required=True,
        ),
        DataInput(
            name="transcription_result",
            display_name="Transkriptionsresultat",
            info="Transkriptionsresultatet från AssemblyAI",
            required=True,
        ),
        DropdownInput(
            name="subtitle_format",
            display_name="Undertextformat",
            options=["srt", "vtt"],
            value="srt",
            info="Formatet för textningen (SRT eller VTT)",
        ),
        IntInput(
            name="chars_per_caption",
            display_name="Tecken per textning",
            info="Maximalt antal tecken per textning (0 för ingen gräns)",
            value=0,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Undertexter", name="subtitles", method="get_subtitles"),
    ]

    def get_subtitles(self) -> Data:
        aai.settings.api_key = self.api_key

        # check if it's an error message from the previous step
        if self.transcription_result.data.get("error"):
            self.status = self.transcription_result.data["error"]
            return self.transcription_result

        try:
            transcript_id = self.transcription_result.data["id"]
            transcript = aai.Transcript.get_by_id(transcript_id)
        except Exception as e:  # noqa: BLE001
            error = f"Getting transcription failed: {e}"
            logger.opt(exception=True).debug(error)
            self.status = error
            return Data(data={"error": error})

        if transcript.status == aai.TranscriptStatus.completed:
            subtitles = None
            chars_per_caption = self.chars_per_caption if self.chars_per_caption > 0 else None
            if self.subtitle_format == "srt":
                subtitles = transcript.export_subtitles_srt(chars_per_caption)
            else:
                subtitles = transcript.export_subtitles_vtt(chars_per_caption)

            result = Data(
                subtitles=subtitles,
                format=self.subtitle_format,
                transcript_id=transcript_id,
                chars_per_caption=chars_per_caption,
            )

            self.status = result
            return result
        self.status = transcript.error
        return Data(data={"error": transcript.error})

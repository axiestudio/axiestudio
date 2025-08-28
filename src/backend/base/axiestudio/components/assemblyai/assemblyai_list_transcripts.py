import assemblyai as aai
from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, DropdownInput, IntInput, MessageTextInput, Output, SecretStrInput
from axiestudio.schema.data import Data


class AssemblyAIListTranscripts(Component):
    display_name = "AssemblyAI Lista transkriptioner"
    description = "Hämta en lista över transkriptioner från AssemblyAI med filtreringsalternativ"
    documentation = "https://www.assemblyai.com/docs"
    icon = "AssemblyAI"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="Assembly API-nyckel",
            info="Din AssemblyAI API-nyckel. Du kan få en från https://www.assemblyai.com/",
            required=True,
        ),
        IntInput(
            name="limit",
            display_name="Gräns",
            info="Maximalt antal transkriptioner att hämta (standard: 20, använd 0 för alla)",
            value=20,
        ),
        DropdownInput(
            name="status_filter",
            display_name="Statusfilter",
            options=["all", "queued", "processing", "completed", "error"],
            value="all",
            info="Filtrera efter transkriptionsstatus",
            advanced=True,
        ),
        MessageTextInput(
            name="created_on",
            display_name="Skapad den",
            info="Hämta endast transkriptioner skapade på detta datum (ÅÅÅÅ-MM-DD)",
            advanced=True,
        ),
        BoolInput(
            name="throttled_only",
            display_name="Endast begränsade",
            info="Hämta endast begränsade transkriptioner, åsidosätter statusfiltret",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Transkriptlista", name="transcript_list", method="list_transcripts"),
    ]

    def list_transcripts(self) -> list[Data]:
        aai.settings.api_key = self.api_key

        params = aai.ListTranscriptParameters()
        if self.limit:
            params.limit = self.limit
        if self.status_filter != "all":
            params.status = self.status_filter
        if self.created_on and self.created_on.text:
            params.created_on = self.created_on.text
        if self.throttled_only:
            params.throttled_only = True

        try:
            transcriber = aai.Transcriber()

            def convert_page_to_data_list(page):
                return [Data(**t.dict()) for t in page.transcripts]

            if self.limit == 0:
                # paginate over all pages
                params.limit = 100
                page = transcriber.list_transcripts(params)
                transcripts = convert_page_to_data_list(page)

                while page.page_details.before_id_of_prev_url is not None:
                    params.before_id = page.page_details.before_id_of_prev_url
                    page = transcriber.list_transcripts(params)
                    transcripts.extend(convert_page_to_data_list(page))
            else:
                # just one page
                page = transcriber.list_transcripts(params)
                transcripts = convert_page_to_data_list(page)

        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Error listing transcripts")
            error_data = Data(data={"error": f"Ett fel uppstod: {e}"})
            self.status = [error_data]
            return [error_data]

        self.status = transcripts
        return transcripts

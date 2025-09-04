import json
from typing import Any

from composio import Action

from axiestudio.base.composio.composio_base import ComposioBaseComponent
from axiestudio.inputs import BoolInput, FileInput, IntInput, MessageTextInput
from axiestudio.logging import logger


class ComposioOutlookAPIComponent(ComposioBaseComponent):
    display_name: str = "Outlook"
    description: str = "Outlook API"
    icon = "Outlook"
    documentation: str = "https://docs.composio.dev"
    app_name = "outlook"

    _actions_data: dict = {
        "OUTLOOK_OUTLOOK_REPLY_EMAIL": {
            "display_name": "Svara på e-post",
            "action_fields": [
                "OUTLOOK_OUTLOOK_REPLY_EMAIL_user_id",
                "OUTLOOK_OUTLOOK_REPLY_EMAIL_message_id",
                "OUTLOOK_OUTLOOK_REPLY_EMAIL_comment",
                "OUTLOOK_OUTLOOK_REPLY_EMAIL_cc_emails",
                "OUTLOOK_OUTLOOK_REPLY_EMAIL_bcc_emails",
            ],
            "get_result_field": False,
        },
        "OUTLOOK_OUTLOOK_GET_PROFILE": {
            "display_name": "Hämta profil",
            "action_fields": ["OUTLOOK_OUTLOOK_GET_PROFILE_user_id"],
            "get_result_field": True,
            "result_field": "response_data",
        },
        "OUTLOOK_OUTLOOK_SEND_EMAIL": {
            "display_name": "Skicka e-post",
            "action_fields": [
                "OUTLOOK_OUTLOOK_SEND_EMAIL_user_id",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_subject",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_body",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_to_email",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_to_name",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_cc_emails",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_bcc_emails",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_is_html",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_save_to_sent_items",
                "OUTLOOK_OUTLOOK_SEND_EMAIL_attachment",
            ],
            "get_result_field": False,
        },
        "OUTLOOK_OUTLOOK_LIST_MESSAGES": {
            "display_name": "Lista meddelanden",
            "action_fields": [
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_user_id",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_folder",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_top",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_skip",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_is_read",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_importance",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_subject",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_gt",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_startswith",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_endswith",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_contains",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_ge",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_lt",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_le",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_from_address",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_has_attachments",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_body_preview_contains",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_sent_date_time_gt",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_sent_date_time_lt",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_categories",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_select",
                "OUTLOOK_OUTLOOK_LIST_MESSAGES_orderby",
            ],
            "get_result_field": True,
            "result_field": "value",
        },
        "OUTLOOK_OUTLOOK_LIST_EVENTS": {
            "display_name": "Lista händelser",
            "action_fields": [
                "OUTLOOK_OUTLOOK_LIST_EVENTS_user_id",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_top",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_skip",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_filter",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_select",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_orderby",
                "OUTLOOK_OUTLOOK_LIST_EVENTS_timezone",
            ],
            "get_result_field": True,
            "result_field": "value",
        },
        "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT": {
            "display_name": "Skapa kalenderhändelse",
            "action_fields": [
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_user_id",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_subject",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_body",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_html",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_start_datetime",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_end_datetime",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_time_zone",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_online_meeting",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_online_meeting_provider",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_attendees_info",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_location",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_show_as",
                "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_categories",
            ],
            "get_result_field": True,
            "result_field": "response_data",
        },
        "OUTLOOK_OUTLOOK_GET_EVENT": {
            "display_name": "Hämta kalenderhändelse",
            "action_fields": ["OUTLOOK_OUTLOOK_GET_EVENT_user_id", "OUTLOOK_OUTLOOK_GET_EVENT_event_id"],
            "get_result_field": True,
            "result_field": "response_data",
        },
        "OUTLOOK_OUTLOOK_CREATE_DRAFT": {
            "display_name": "Skapa e-postutkast",
            "action_fields": [
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_subject",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_body",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_to_recipients",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_cc_recipients",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_bcc_recipients",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_is_html",
                "OUTLOOK_OUTLOOK_CREATE_DRAFT_attachment",
            ],
            "get_result_field": True,
            "result_field": "response_data",
        },
    }

    _all_fields = {field for action_data in _actions_data.values() for field in action_data["action_fields"]}

    _bool_variables = {
        "OUTLOOK_OUTLOOK_SEND_EMAIL_is_html",
        "OUTLOOK_OUTLOOK_SEND_EMAIL_save_to_sent_items",
        "OUTLOOK_OUTLOOK_CREATE_DRAFT_is_html",
        "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_html",
        "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_online_meeting",
        "OUTLOOK_OUTLOOK_LIST_MESSAGES_is_read",
        "OUTLOOK_OUTLOOK_LIST_MESSAGES_has_attachments",
    }

    _list_variables = {
        "OUTLOOK_OUTLOOK_LIST_EVENTS_select",
        "OUTLOOK_OUTLOOK_LIST_EVENTS_orderby",
        "OUTLOOK_OUTLOOK_SEND_EMAIL_cc_emails",
        "OUTLOOK_OUTLOOK_SEND_EMAIL_bcc_emails",
        "OUTLOOK_OUTLOOK_CREATE_DRAFT_to_recipients",
        "OUTLOOK_OUTLOOK_CREATE_DRAFT_cc_recipients",
        "OUTLOOK_OUTLOOK_CREATE_DRAFT_bcc_recipients",
        "OUTLOOK_OUTLOOK_REPLY_EMAIL_cc_emails",
        "OUTLOOK_OUTLOOK_REPLY_EMAIL_bcc_emails",
        "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_attendees_info",
        "OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_categories",
        "OUTLOOK_OUTLOOK_LIST_MESSAGES_categories",
        "OUTLOOK_OUTLOOK_LIST_MESSAGES_select",
        "OUTLOOK_OUTLOOK_LIST_MESSAGES_orderby",
    }

    inputs = [
        *ComposioBaseComponent._base_inputs,
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_user_id",
            display_name="Användar-ID",
            info="Målanvändarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
            advanced=True,
        ),
        IntInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_top",
            display_name="Max resultat",
            info="Maximalt antal händelser att returnera per begäran.",
            show=False,
            value=10,
        ),
        IntInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_skip",
            display_name="Hoppa över",
            info="Antal händelser att hoppa över innan insamling av resultat börjar.",
            show=False,
            value=0,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_filter",
            display_name="Filter",
            info="OData-frågesträng för att filtrera resultat. Exempel: start/dateTime ge '2024-01-01T00:00:00'",
            show=False,
            value="",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_select",
            display_name="Välj",
            info="Lista över egenskaper att inkludera i svaret, kommaseparerade.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_orderby",
            display_name="Sortera efter",
            info="Egenskaper att sortera resultat efter, kommaseparerade.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_EVENTS_timezone",
            display_name="Tidszon",
            info="Tidszonen för händelsernas start- och sluttider i svaret.",
            show=False,
            value="UTC",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_user_id",
            display_name="Användar-ID",
            info="Användarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_subject",
            display_name="Ämne",
            info="E-postens ämne",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_body",
            display_name="Brödtext",
            info="E-postens innehåll. Kan vara vanlig text eller HTML baserat på is_html-flaggan.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_to_email",
            display_name="Mottagarens e-post",
            info="Mottagarens e-postadress",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_to_name",
            display_name="Till namn",
            info="Mottagarens visningsnamn",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_cc_emails",
            display_name="CC",
            info="Lista över CC-mottagares e-postadresser, kommaseparerade",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_bcc_emails",
            display_name="BCC",
            info="Lista över BCC-mottagares e-postadresser, kommaseparerade",
            show=False,
            advanced=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_is_html",
            display_name="Är HTML",
            info="Sätt till True om brödtexten är HTML-formaterad",
            show=False,
            value=False,
            advanced=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_save_to_sent_items",
            display_name="Spara till skickade objekt",
            info="Om den skickade e-posten ska sparas i mappen Skickade objekt.",
            show=False,
            value=True,
            advanced=True,
        ),
        FileInput(
            name="OUTLOOK_OUTLOOK_SEND_EMAIL_attachment",
            display_name="Bilaga",
            file_types=[
                "csv",
                "txt",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "gif",
                "zip",
                "rar",
                "ppt",
                "pptx",
            ],
            info="Lägg till en bilaga",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_subject",
            display_name="Ämne",
            info="E-postens ämne",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_body",
            display_name="Brödtext",
            info="E-postens innehåll. Kan vara vanlig text eller HTML baserat på is_html-flaggan",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_to_recipients",
            display_name="Mottagarens e-post",
            info="Lista över mottagares e-postadresser, kommaseparerade",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_cc_recipients",
            display_name="CC-mottagare",
            info="Lista över CC-mottagares e-postadresser",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_bcc_recipients",
            display_name="BCC",
            info="Lista över BCC-mottagares e-postadresser, kommaseparerade",
            show=False,
            advanced=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_is_html",
            display_name="Är HTML",
            info="Sätt till True om brödtexten är HTML-formaterad",
            show=False,
            value=False,
            advanced=True,
        ),
        FileInput(
            name="OUTLOOK_OUTLOOK_CREATE_DRAFT_attachment",
            display_name="Bilaga",
            file_types=[
                "csv",
                "txt",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "gif",
                "zip",
                "rar",
                "ppt",
                "pptx",
            ],
            info="Lägg till en bilaga",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_GET_PROFILE_user_id",
            display_name="Användar-ID",
            info="Användarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_REPLY_EMAIL_user_id",
            display_name="Användar-ID",
            info="Användarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_REPLY_EMAIL_message_id",
            display_name="Meddelande-ID",
            info="ID för meddelandet att svara på. Kan erhållas från OUTLOOK_LIST_MESSAGES-åtgärden.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_REPLY_EMAIL_comment",
            display_name="Kommentar",
            info="Kommentar att inkludera i svaret. Måste vara vanlig text.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_REPLY_EMAIL_cc_emails",
            display_name="CC",
            info="Lista över CC-mottagares e-postadresser, kommaseparerade",
            show=False,
            value=[],
            is_list=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_REPLY_EMAIL_bcc_emails",
            display_name="BCC",
            info="Lista över BCC-mottagares e-postadresser, kommaseparerade",
            show=False,
            value=[],
            is_list=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_user_id",
            display_name="Användar-ID",
            info="Användarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_subject",
            display_name="Ämne",
            info="Händelsens ämne. Exempel: 'Teammöte'.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_body",
            display_name="Brödtext",
            info="Händelsens innehåll. Kan vara vanlig text eller HTML.",
            show=False,
            required=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_html",
            display_name="Är HTML",
            info="Sätt till True om brödtexten ska tolkas som HTML.",
            show=False,
            value=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_start_datetime",
            display_name="Starttid",
            info="Startdatum/tid (ISO 8601). Exempel: '2025-01-03T10:00:00Z'.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_end_datetime",
            display_name="Sluttid",
            info="Slutdatum/tid (ISO 8601). Exempel: '2025-01-03T11:00:00Z'.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_time_zone",
            display_name="Tidszon",
            info="Tidszon (t.ex. 'UTC' eller 'America/Los_Angeles').",
            show=False,
            required=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_is_online_meeting",
            display_name="Är onlinemöte",
            info="Sätt till True för att göra detta till ett onlinemöte och generera en Teams-URL.",
            show=False,
            value=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_online_meeting_provider",
            display_name="Onlinemötesleverantör",
            info="Leverantören av onlinemötestjänsten. Stöder för närvarande endast 'teamsForBusiness'.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_attendees_info",
            display_name="Deltagare",
            info="En lista med deltagarinformation. Endast e-post krävs för varje deltagare. Exempel: [{ 'email': 'team@example.com', 'name': 'Team', 'type': 'required' }, { 'email': 'other@example.com', 'type': 'optional' }, { 'email': 'other2@example.com' }]",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_location",
            display_name="Plats",
            info="Händelsens plats (t.ex. 'Konferensrum').",
            show=False,
            value="",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_show_as",
            display_name="Visa som",
            info="Händelsens status: 'free', 'tentative', 'busy' eller 'oof'.",
            show=False,
            value="busy",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_CALENDAR_CREATE_EVENT_categories",
            display_name="Kategorier",
            info="Lista över kategorier associerade med händelsen, kommaseparerade.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_GET_EVENT_user_id",
            display_name="Användar-ID",
            info="Användarens e-postadress eller 'me' för den autentiserade användaren.",
            show=False,
            value="me",
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_GET_EVENT_event_id",
            display_name="Händelse-ID",
            info="ID för kalenderhändelsen att hämta.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_user_id",
            display_name="Användar-ID",
            info="Målanvändarens e-postadress eller 'me' för den autentiserade användaren. För delegerade åtkomstscenarier ska detta vara e-postadressen för den delade brevlådan eller delegerade användaren.",  # noqa: E501
            show=False,
            value="me",
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_folder",
            display_name="Mapp",
            info="",
            show=False,
            value="inbox",
            advanced=True,
        ),
        IntInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_top",
            display_name="Max resultat",
            info="Maximalt antal meddelanden att returnera per begäran. Måste vara ett positivt heltal mellan 1 och 1000.",
            show=False,
            value=10,
        ),
        IntInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_skip",
            display_name="Hoppa över",
            info="Antal meddelanden att hoppa över innan insamling av resultat börjar. Används för paginerade svar.",
            show=False,
            value=0,
            advanced=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_is_read",
            display_name="Är läst",
            info="Filtrera meddelanden efter lässtatus. Om satt till False returneras endast olästa meddelanden.",
            show=False,
            value=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_importance",
            display_name="Viktighet",
            info="Filtrera meddelanden efter viktighet. Till exempel 'high', 'normal' eller 'low'.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_subject",
            display_name="Ämne",
            info="Filtrera meddelanden efter ämne (exakt matchning).",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_gt",
            display_name="Mottaget datum tid större än",
            info="Filtrera meddelanden med receivedDateTime större än det angivna värdet. Exempel: '2023-01-01T00:00:00Z'.",  # noqa: E501
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_startswith",
            display_name="Ämne börjar med",
            info="Filtrera meddelanden där ämnet börjar med den angivna strängen.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_endswith",
            display_name="Ämne slutar med",
            info="Filtrera meddelanden där ämnet slutar med den angivna strängen.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_subject_contains",
            display_name="Ämne innehåller",
            info="Filtrera meddelanden där ämnet innehåller den angivna delsträngen.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_ge",
            display_name="Mottaget datum tid större än eller lika med",
            info="Filtrera meddelanden med receivedDateTime större än eller lika med det angivna värdet.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_lt",
            display_name="Mottaget datum tid mindre än",
            info="Filtrera meddelanden med receivedDateTime mindre än det angivna värdet.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_received_date_time_le",
            display_name="Mottaget datum tid mindre än eller lika med",
            info="Filtrera meddelanden med receivedDateTime mindre än eller lika med det angivna värdet.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_from_address",
            display_name="Från-adress",
            info="Filtrera meddelanden efter avsändarens e-postadress. Använder likhetskontroll på from/emailAddress/address.",
            show=False,
            advanced=True,
        ),
        BoolInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_has_attachments",
            display_name="Har bilagor",
            info="Filtrera meddelanden efter om de har bilagor.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_body_preview_contains",
            display_name="Brödtextförhandsvisning innehåller",
            info="Filtrera meddelanden där bodyPreview innehåller den angivna delsträngen.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_sent_date_time_gt",
            display_name="Skickat datum tid större än",
            info="Filtrera meddelanden med sentDateTime större än det angivna värdet.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_sent_date_time_lt",
            display_name="Skickat datum tid mindre än",
            info="Filtrera meddelanden med sentDateTime mindre än det angivna värdet.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_categories",
            display_name="Kategorier",
            info="Filtrera meddelanden efter kategorier. Matchar om meddelandet innehåller någon av de angivna kategorierna.",
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_select",
            display_name="Välj",
            info="En lista över egenskaper att inkludera i svaret, kommaseparerade. Vanliga egenskaper: 'subject', 'from', 'toRecipients', 'receivedDateTime'.",  # noqa: E501
            show=False,
            advanced=True,
        ),
        MessageTextInput(
            name="OUTLOOK_OUTLOOK_LIST_MESSAGES_orderby",
            display_name="Sortera efter",
            info="Ange egenskaper att sortera resultat efter. Till exempel 'receivedDateTime desc' för nyaste meddelanden först.",  # noqa: E501
            show=False,
            advanced=True,
        ),
    ]

    def execute_action(self):
        """Execute action and return response as Message."""
        toolset = self._build_wrapper()

        try:
            self._build_action_maps()
            display_name = self.action[0]["name"] if isinstance(self.action, list) and self.action else self.action
            action_key = self._display_to_key_map.get(display_name)
            if not action_key:
                msg = f"Ogiltig åtgärd: {display_name}"
                raise ValueError(msg)

            enum_name = getattr(Action, action_key)
            params = {}
            if action_key in self._actions_data:
                for field in self._actions_data[action_key]["action_fields"]:
                    value = getattr(self, field)

                    if value is None or value == "":
                        continue

                    if field in self._list_variables and value:
                        value = [item.strip() for item in value.split(",")]

                    if field in self._bool_variables:
                        value = bool(value)

                    param_name = field.replace(action_key + "_", "")

                    params[param_name] = value

            result = toolset.execute_action(
                action=enum_name,
                params=params,
            )
            if not result.get("successful"):
                error_data = result.get("data", {})
                error_message = error_data.get("message", str(result.get("error", "Okänt fel")))

                if isinstance(error_message, str):
                    try:
                        error_obj = json.loads(error_message).get("error", {})
                        error_obj["status_code"] = error_data.get("status_code", 400)
                        return error_obj  # noqa: TRY300
                    except json.JSONDecodeError:
                        return {"error": error_message, "status_code": error_data.get("status_code", 400)}

                return error_message

            result_data = result.get("data", {})
            actions_data = self._actions_data.get(action_key, {})
            if actions_data.get("get_result_field") and actions_data.get("result_field"):
                response_data = result_data.get("response_data", {})
                if response_data and actions_data.get("result_field") in response_data:
                    result_data = response_data.get(actions_data.get("result_field"), result.get("data", []))
                else:
                    result_data = result_data.get(actions_data.get("result_field"), result.get("data", []))
            if len(result_data) != 1 and not actions_data.get("result_field") and actions_data.get("get_result_field"):
                msg = f"Förväntade en dict med en enda nyckel, fick {len(result_data)} nycklar: {result_data.keys()}"
                raise ValueError(msg)
            return result_data  # noqa: TRY300
        except Exception as e:
            logger.error(f"Fel vid körning av åtgärd: {e}")
            display_name = self.action[0]["name"] if isinstance(self.action, list) and self.action else str(self.action)
            msg = f"Misslyckades att köra {display_name}: {e!s}"
            raise ValueError(msg) from e

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        return super().update_build_config(build_config, field_value, field_name)

    def set_default_tools(self):
        self._default_tools = {
            self.sanitize_action_name("OUTLOOK_OUTLOOK_SEND_EMAIL").replace(" ", "-"),
            self.sanitize_action_name("OUTLOOK_OUTLOOK_LIST_MESSAGES").replace(" ", "-"),
        }

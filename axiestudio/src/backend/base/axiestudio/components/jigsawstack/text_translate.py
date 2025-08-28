from axiestudio.custom.custom_component.component import Component
from axiestudio.io import MessageTextInput, Output, SecretStrInput, StrInput
from axiestudio.schema.data import Data


class JigsawStackTextTranslateComponent(Component):
    display_name = "Textöversättning"
    description = "Översätt text från ett språk till ett annat med stöd för flera textformat."
    documentation = "https://jigsawstack.com/docs/api-reference/ai/translate"
    icon = "JigsawStack"
    name = "JigsawStackTextTranslate"
    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="JigsawStack API-nyckel",
            info="Din JigsawStack API-nyckel för autentisering",
            required=True,
        ),
        StrInput(
            name="target_language",
            display_name="Målspråk",
            info="Språkkoden för målspråket att översätta till. \
                Språkkod identifieras av en unik ISO 639-1 tvåbokstavskod",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="text",
            display_name="Text",
            info="Texten att översätta. Detta kan vara en enskild sträng eller en lista med strängar. \
                Om en lista tillhandahålls kommer varje sträng att översättas separat.",
            required=True,
            is_list=True,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Översättningsresultat", name="translation_results", method="translation"),
    ]

    def translation(self) -> Data:
        try:
            from jigsawstack import JigsawStack, JigsawStackError
        except ImportError as e:
            jigsawstack_import_error = (
                "JigsawStack-paketet hittades inte. Vänligen installera det med: pip install jigsawstack>=0.2.7"
            )
            raise ImportError(jigsawstack_import_error) from e

        try:
            client = JigsawStack(api_key=self.api_key)

            # build request object
            params = {}
            if self.target_language:
                params["target_language"] = self.target_language

            if self.text:
                if isinstance(self.text, list):
                    params["text"] = self.text
                else:
                    params["text"] = [self.text]

            # Call web scraping
            response = client.translate.text(params)

            if not response.get("success", False):
                failed_response_error = "JigsawStack API returnerade ett misslyckat svar"
                raise ValueError(failed_response_error)

            return Data(data=response)

        except JigsawStackError as e:
            error_data = {"error": str(e), "success": False}
            self.status = f"Fel: {e!s}"
            return Data(data=error_data)

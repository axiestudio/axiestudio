from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, DropdownInput, Output, QueryInput, SecretStrInput
from axiestudio.schema.data import Data
from axiestudio.schema.message import Message


class JigsawStackAIWebSearchComponent(Component):
    display_name = "AI-webbsökning"
    description = "Sök enkelt på webben och få tillgång till högkvalitativa resultat drivna av AI."
    documentation = "https://jigsawstack.com/docs/api-reference/web/ai-search"
    icon = "JigsawStack"
    name = "JigsawStackAISearch"
    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="JigsawStack API-nyckel",
            info="Din JigsawStack API-nyckel för autentisering",
            required=True,
        ),
        QueryInput(
            name="query",
            display_name="Sökfråga",
            info="Sökvärdet. Maximal längd på sökfrågan är 400 tecken",
            required=True,
            tool_mode=True,
        ),
        BoolInput(
            name="ai_overview",
            display_name="AI-översikt",
            info="Inkludera AI-driven översikt i sökresultaten",
            required=False,
            value=True,
        ),
        DropdownInput(
            name="safe_search",
            display_name="Säker sökning",
            info="Aktivera säker sökning för att filtrera bort vuxeninnehåll",
            required=False,
            options=["moderate", "strict", "off"],
            value="off",
        ),
        BoolInput(
            name="spell_check",
            display_name="Stavningskontroll",
            info="Stavningskontrollera sökfrågan",
            required=False,
            value=True,
        ),
    ]

    outputs = [
        Output(display_name="AI-sökresultat", name="search_results", method="search"),
        Output(display_name="Innehållstext", name="content_text", method="get_content_text"),
    ]

    def search(self) -> Data:
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
            search_params = {}
            if self.query:
                search_params["query"] = self.query
            if self.ai_overview is not None:
                search_params["ai_overview"] = self.ai_overview
            if self.safe_search:
                search_params["safe_search"] = self.safe_search
            if self.spell_check is not None:
                search_params["spell_check"] = self.spell_check

            # Call web scraping
            response = client.web.search(search_params)

            api_error_msg = "JigsawStack API returnerade ett misslyckat svar"
            if not response.get("success", False):
                raise ValueError(api_error_msg)

            # Create comprehensive data object
            result_data = {
                "query": self.query,
                "ai_overview": response.get("ai_overview", ""),
                "spell_fixed": response.get("spell_fixed", False),
                "is_safe": response.get("is_safe", True),
                "results": response.get("results", []),
                "success": True,
            }

            self.status = f"Sökning slutförd för: {response.get('query', '')}"

            return Data(data=result_data)

        except JigsawStackError as e:
            error_data = {"error": str(e), "success": False}
            self.status = f"Fel: {e!s}"
            return Data(data=error_data)

    def get_content_text(self) -> Message:
        try:
            from jigsawstack import JigsawStack, JigsawStackError
        except ImportError:
            return Message(text="Fel: JigsawStack-paketet hittades inte.")

        try:
            # Initialize JigsawStack client
            client = JigsawStack(api_key=self.api_key)
            search_params = {}
            if self.query:
                search_params["query"] = self.query
            if self.ai_overview is not None:
                search_params["ai_overview"] = self.ai_overview
            if self.safe_search:
                search_params["safe_search"] = self.safe_search
            if self.spell_check is not None:
                search_params["spell_check"] = self.spell_check

            # Call web scraping
            response = client.web.search(search_params)

            request_failed_msg = "Förfrågan misslyckades"
            if not response.get("success", False):
                raise JigsawStackError(request_failed_msg)

            # Return the content as text
            content = response.get("ai_overview", "")
            return Message(text=content)

        except JigsawStackError as e:
            return Message(text=f"Fel vid användning av AI-sökning: {e!s}")

import json
from typing import Any

import requests
from langchain.tools import StructuredTool
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import MultilineInput, SecretStrInput, StrInput
from axiestudio.schema.data import Data


class NotionListPages(LCToolComponent):
    display_name: str = "Lista sidor"
    description: str = (
        "Fråga en Notion-databas med filtrering och sortering. "
        "Indata ska vara en JSON-sträng som innehåller 'filter'- och 'sorts'-objekten. "
        "Exempel på indata:\n"
        '{"filter": {"property": "Status", "select": {"equals": "Done"}}, '
        '"sorts": [{"timestamp": "created_time", "direction": "descending"}]}'
    )
    documentation: str = "https://docs.axiestudio.se/integrations/notion/list-pages"
    icon = "NotionDirectoryLoader"

    inputs = [
        SecretStrInput(
            name="notion_secret",
            display_name="Notion-hemlighet",
            info="Notion-integrationstokenet.",
            required=True,
        ),
        StrInput(
            name="database_id",
            display_name="Databas-ID",
            info="ID:t för Notion-databasen att fråga.",
        ),
        MultilineInput(
            name="query_json",
            display_name="Databasfråga (JSON)",
            info="En JSON-sträng som innehåller filter och sorteringar som kommer att användas för att fråga databasen. "
            "Lämna tom för inga filter eller sorteringar.",
        ),
    ]

    class NotionListPagesSchema(BaseModel):
        database_id: str = Field(..., description="The ID of the Notion database to query.")
        query_json: str | None = Field(
            default="",
            description="A JSON string containing the filters and sorts for querying the database. "
            "Leave empty for no filters or sorts.",
        )

    def run_model(self) -> list[Data]:
        result = self._query_notion_database(self.database_id, self.query_json)

        if isinstance(result, str):
            # An error occurred, return it as a single record
            return [Data(text=result)]

        records = []
        combined_text = f"Pages found: {len(result)}\n\n"

        for page in result:
            page_data = {
                "id": page["id"],
                "url": page["url"],
                "created_time": page["created_time"],
                "last_edited_time": page["last_edited_time"],
                "properties": page["properties"],
            }

            text = (
                f"id: {page['id']}\n"
                f"url: {page['url']}\n"
                f"created_time: {page['created_time']}\n"
                f"last_edited_time: {page['last_edited_time']}\n"
                f"properties: {json.dumps(page['properties'], indent=2)}\n\n"
            )

            combined_text += text
            records.append(Data(text=text, **page_data))

        self.status = records
        return records

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="notion_list_pages",
            description=self.description,
            func=self._query_notion_database,
            args_schema=self.NotionListPagesSchema,
        )

    def _query_notion_database(self, database_id: str, query_json: str | None = None) -> list[dict[str, Any]] | str:
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.notion_secret}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        query_payload = {}
        if query_json and query_json.strip():
            try:
                query_payload = json.loads(query_json)
            except json.JSONDecodeError as e:
                return f"Invalid JSON format for query: {e}"

        try:
            response = requests.post(url, headers=headers, json=query_payload, timeout=10)
            response.raise_for_status()
            results = response.json()
            return results["results"]
        except requests.exceptions.RequestException as e:
            return f"Error querying Notion database: {e}"
        except KeyError:
            return "Unexpected response format from Notion API"
        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Error querying Notion database")
            return f"An unexpected error occurred: {e}"

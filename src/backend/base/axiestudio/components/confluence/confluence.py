from langchain_community.document_loaders import ConfluenceLoader
from langchain_community.document_loaders.confluence import ContentFormat

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, DropdownInput, IntInput, Output, SecretStrInput, StrInput
from axiestudio.schema.data import Data


class ConfluenceComponent(Component):
    display_name = "Confluence"
    description = "Confluence wiki-samarbetsplattform"
    documentation = "https://python.langchain.com/v0.2/docs/integrations/document_loaders/confluence/"
    trace_type = "tool"
    icon = "Confluence"
    name = "Confluence"

    inputs = [
        StrInput(
            name="url",
            display_name="Webbplats-URL",
            required=True,
            info="Bas-URL:en för Confluence-utrymmet. Exempel: https://<företag>.atlassian.net/wiki.",
        ),
        StrInput(
            name="username",
            display_name="Användarnamn",
            required=True,
            info="Atlassian-användarens e-post. Exempel: email@example.com",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API-nyckel",
            required=True,
            info="Atlassian-nyckel. Skapa på: https://id.atlassian.com/manage-profile/security/api-tokens",
        ),
        StrInput(name="space_key", display_name="Utrymmesnyckel", required=True),
        BoolInput(name="cloud", display_name="Använd moln?", required=True, value=True, advanced=True),
        DropdownInput(
            name="content_format",
            display_name="Innehållsformat",
            options=[
                ContentFormat.EDITOR.value,
                ContentFormat.EXPORT_VIEW.value,
                ContentFormat.ANONYMOUS_EXPORT_VIEW.value,
                ContentFormat.STORAGE.value,
                ContentFormat.VIEW.value,
            ],
            value=ContentFormat.STORAGE.value,
            required=True,
            advanced=True,
            info="Specify content format, defaults to ContentFormat.STORAGE",
        ),
        IntInput(
            name="max_pages",
            display_name="Max Pages",
            required=False,
            value=1000,
            advanced=True,
            info="Maximum number of pages to retrieve in total, defaults 1000",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Data", method="load_documents"),
    ]

    def build_confluence(self) -> ConfluenceLoader:
        content_format = ContentFormat(self.content_format)
        return ConfluenceLoader(
            url=self.url,
            username=self.username,
            api_key=self.api_key,
            cloud=self.cloud,
            space_key=self.space_key,
            content_format=content_format,
            max_pages=self.max_pages,
        )

    def load_documents(self) -> list[Data]:
        confluence = self.build_confluence()
        documents = confluence.load()
        data = [Data.from_document(doc) for doc in documents]  # Using the from_document method of Data
        self.status = data
        return data

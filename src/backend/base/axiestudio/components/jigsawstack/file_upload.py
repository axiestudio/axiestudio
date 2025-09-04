from pathlib import Path

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import BoolInput, FileInput, Output, SecretStrInput, StrInput
from axiestudio.schema.data import Data


class JigsawStackFileUploadComponent(Component):
    display_name = "Filuppladdning"
    description = "Lagra vilken fil som helst sömlöst på JigsawStack fillagring och använd den i dina AI-applikationer. \
        Stöder olika filtyper inklusive bilder, dokument och mer."
    documentation = "https://jigsawstack.com/docs/api-reference/store/file/add"
    icon = "JigsawStack"
    name = "JigsawStackFileUpload"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="JigsawStack API-nyckel",
            info="Din JigsawStack API-nyckel för autentisering",
            required=True,
        ),
        FileInput(
            name="file",
            display_name="Fil",
            info="Ladda upp fil som ska lagras på JigsawStack fillagring.",
            required=True,
            file_types=["pdf", "png", "jpg", "jpeg", "mp4", "mp3", "txt", "docx", "xlsx"],
        ),
        StrInput(
            name="key",
            display_name="Nyckel",
            info="Nyckeln som används för att lagra filen på JigsawStack fillagring. \
                Om den inte anges kommer en unik nyckel att genereras.",
            required=False,
            tool_mode=True,
        ),
        BoolInput(
            name="overwrite",
            display_name="Skriv över befintlig fil",
            info="Om sant, kommer att skriva över den befintliga filen med samma nyckel. \
                Om falskt, kommer att returnera ett fel om filen redan finns.",
            required=False,
            value=True,
        ),
        BoolInput(
            name="temp_public_url",
            display_name="Returnera tillfällig offentlig URL",
            info="Om sant, kommer att returnera en tillfällig offentlig URL som varar en begränsad tid. \
                Om falskt, kommer att returnera fillagringsnyckel som endast kan nås av ägaren.",
            required=False,
            value=False,
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="File Store Result", name="file_upload_result", method="upload_file"),
    ]

    def upload_file(self) -> Data:
        try:
            from jigsawstack import JigsawStack, JigsawStackError
        except ImportError as e:
            jigsawstack_import_error = (
                "JigsawStack package not found. Please install it using: pip install jigsawstack>=0.2.7"
            )
            raise ImportError(jigsawstack_import_error) from e

        try:
            client = JigsawStack(api_key=self.api_key)

            file_path = Path(self.file)
            with Path.open(file_path, "rb") as f:
                file_content = f.read()
            params = {}

            if self.key:
                # if key is provided, use it as the file store key
                params["key"] = self.key
            if self.overwrite is not None:
                # if overwrite is provided, use it to determine if the file should be overwritten
                params["overwrite"] = self.overwrite
            if self.temp_public_url is not None:
                # if temp_public_url is provided, use it to determine if a temporary public URL should
                params["temp_public_url"] = self.temp_public_url

            response = client.store.upload(file_content, params)
            return Data(data=response)

        except JigsawStackError as e:
            error_data = {"error": str(e), "success": False}
            self.status = f"Error: {e!s}"
            return Data(data=error_data)

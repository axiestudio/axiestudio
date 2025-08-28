from axiestudio.custom.custom_component.component import Component
from axiestudio.io import Output, SecretStrInput, StrInput
from axiestudio.schema.data import Data


class JigsawStackNSFWComponent(Component):
    display_name = "NSFW-detektering"
    description = "Upptäck om bild/video innehåller NSFW-innehåll"
    documentation = "https://jigsawstack.com/docs/api-reference/ai/nsfw"
    icon = "JigsawStack"
    name = "JigsawStackNSFW"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="JigsawStack API-nyckel",
            info="Din JigsawStack API-nyckel för autentisering",
            required=True,
        ),
        StrInput(
            name="url",
            display_name="URL",
            info="URL för bilden eller videon att analysera",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="NSFW-analys", name="nsfw_result", method="detect_nsfw"),
    ]

    def detect_nsfw(self) -> Data:
        try:
            from jigsawstack import JigsawStack, JigsawStackError
        except ImportError as e:
            jigsawstack_import_error = (
                "JigsawStack package not found. Please install it using: pip install jigsawstack>=0.2.7"
            )
            raise ImportError(jigsawstack_import_error) from e

        try:
            client = JigsawStack(api_key=self.api_key)

            # Build request parameters
            params = {"url": self.url}

            response = client.validate.nsfw(params)

            api_error_msg = "JigsawStack API returned unsuccessful response"
            if not response.get("success", False):
                raise ValueError(api_error_msg)

            return Data(data=response)

        except ValueError:
            raise
        except JigsawStackError as e:
            error_data = {"error": str(e), "success": False}
            self.status = f"Error: {e!s}"
            return Data(data=error_data)

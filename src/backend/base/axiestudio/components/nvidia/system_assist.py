import asyncio

from axiestudio.custom.custom_component.component_with_cache import ComponentWithCache
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema import Message
from axiestudio.services.cache.utils import CacheMiss

RISE_INITIALIZED_KEY = "rise_initialized"


class NvidiaSystemAssistComponent(ComponentWithCache):
    display_name = "NVIDIA System-Assist"
    description = (
        "(Endast Windows) Uppmanar NVIDIA System-Assist att interagera med NVIDIA GPU-drivrutinen. "
        "Användaren kan fråga om GPU-specifikationer, tillstånd och be NV-API att utföra "
        "flera GPU-redigeringsåtgärder. Prompten måste vara på mänskligt läsbart språk."
    )
    documentation = "https://docs.axiestudio.org/components-custom-components"
    icon = "NVIDIA"
    rise_initialized = False

    inputs = [
        MessageTextInput(
            name="prompt",
            display_name="System-Assist-prompt",
            info="Ange en prompt för NVIDIA System-Assist att bearbeta. Exempel: 'Vad är min GPU?'",
            value="",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Svar", name="response", method="sys_assist_prompt"),
    ]

    def maybe_register_rise_client(self):
        try:
            from gassist.rise import register_rise_client

            rise_initialized = self._shared_component_cache.get(RISE_INITIALIZED_KEY)
            if not isinstance(rise_initialized, CacheMiss) and rise_initialized:
                return
            self.log("Initializing Rise Client")

            register_rise_client()
            self._shared_component_cache.set(key=RISE_INITIALIZED_KEY, value=True)
        except ImportError as e:
            msg = "NVIDIA System-Assist is Windows only and not supported on this platform"
            raise ValueError(msg) from e
        except Exception as e:
            msg = f"An error occurred initializing NVIDIA System-Assist: {e}"
            raise ValueError(msg) from e

    async def sys_assist_prompt(self) -> Message:
        try:
            from gassist.rise import send_rise_command
        except ImportError as e:
            msg = "NVIDIA System-Assist is Windows only and not supported on this platform"
            raise ValueError(msg) from e

        self.maybe_register_rise_client()

        response = await asyncio.to_thread(send_rise_command, self.prompt)

        return Message(text=response["completed_response"]) if response is not None else Message(text=None)

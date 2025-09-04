from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from loguru import logger

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DropdownInput, Output
from axiestudio.schema.message import Message


class CurrentDateComponent(Component):
    display_name = "Aktuellt datum"
    description = "Returnerar aktuellt datum och tid i den valda tidszonen."
    documentation: str = "https://docs.axiestudio.org/components-helpers#current-date"
    icon = "clock"
    name = "CurrentDate"

    inputs = [
        DropdownInput(
            name="timezone",
            display_name="Tidszon",
            options=list(available_timezones()),
            value="UTC",
            info="Välj tidszonen för aktuellt datum och tid.",
            tool_mode=True,
        ),
    ]
    outputs = [
        Output(display_name="Aktuellt datum", name="current_date", method="get_current_date"),
    ]

    def get_current_date(self) -> Message:
        try:
            tz = ZoneInfo(self.timezone)
            current_date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            result = f"Aktuellt datum och tid i {self.timezone}: {current_date}"
            self.status = result
            return Message(text=result)
        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Fel vid hämtning av aktuellt datum")
            error_message = f"Fel: {e}"
            self.status = error_message
            return Message(text=error_message)

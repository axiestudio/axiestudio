from axiestudio.custom.custom_component.component import Component


class TextComponent(Component):
    display_name = "Textkomponent"
    description = "Används för att skicka text till nästa komponent."

    def build_config(self):
        return {
            "input_value": {
                "display_name": "Värde",
                "input_types": ["Message", "Data"],
                "info": "Text eller data att skickas.",
            },
            "data_template": {
                "display_name": "Datamall",
                "multiline": True,
                "info": "Mall för att konvertera data till text. "
                "Om den lämnas tom kommer den att dynamiskt sättas till datans textnyckel.",
                "advanced": True,
            },
        }

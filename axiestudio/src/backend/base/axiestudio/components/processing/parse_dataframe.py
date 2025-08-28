from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataFrameInput, MultilineInput, Output, StrInput
from axiestudio.schema.message import Message


class ParseDataFrameComponent(Component):
    display_name = "Tolka DataFrame"
    description = (
        "Konvertera en DataFrame till vanlig text enligt en angiven mall. "
        "Varje kolumn i DataFrame behandlas som en möjlig mallnyckel, t.ex. {col_name}."
    )
    icon = "braces"
    name = "ParseDataFrame"
    legacy = True

    inputs = [
        DataFrameInput(name="df", display_name="DataFrame", info="DataFrame att konvertera till textrader."),
        MultilineInput(
            name="template",
            display_name="Mall",
            info=(
                "Mallen för formatering av varje rad. "
                "Använd platshållare som matchar kolumnnamn i DataFrame, till exempel '{col1}', '{col2}'."
            ),
            value="{text}",
        ),
        StrInput(
            name="sep",
            display_name="Avgränsare",
            advanced=True,
            value="\n",
            info="Sträng som förenar alla radtexter när den enda textutdatan byggs.",
        ),
    ]

    outputs = [
        Output(
            display_name="Text",
            name="text",
            info="Alla rader kombinerade till en enda text, varje rad formaterad av mallen och separerad av `sep`.",
            method="parse_data",
        ),
    ]

    def _clean_args(self):
        dataframe = self.df
        template = self.template or "{text}"
        sep = self.sep or "\n"
        return dataframe, template, sep

    def parse_data(self) -> Message:
        """Converts each row of the DataFrame into a formatted string using the template.

        then joins them with `sep`. Returns a single combined string as a Message.
        """
        dataframe, template, sep = self._clean_args()

        lines = []
        # For each row in the DataFrame, build a dict and format
        for _, row in dataframe.iterrows():
            row_dict = row.to_dict()
            text_line = template.format(**row_dict)  # e.g. template="{text}", row_dict={"text": "Hello"}
            lines.append(text_line)

        # Join all lines with the provided separator
        result_string = sep.join(lines)
        self.status = result_string  # store in self.status for UI logs
        return Message(text=result_string)

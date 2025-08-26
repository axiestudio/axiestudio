from langchain_text_splitters import CharacterTextSplitter

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DropdownInput, HandleInput, IntInput, MessageTextInput, Output
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.schema.message import Message
from axiestudio.utils.util import unescape_string


class SplitTextComponent(Component):
    display_name: str = "Dela text"
    description: str = "Dela text i bitar baserat på specificerade kriterier."
    documentation: str = "https://docs.axiestudio.org/components-processing#split-text"
    icon = "scissors-line-dashed"
    name = "SplitText"

    inputs = [
        HandleInput(
            name="data_inputs",
            display_name="Inmatning",
            info="Data med texter att dela i bitar.",
            input_types=["Data", "DataFrame", "Message"],
            required=True,
        ),
        IntInput(
            name="chunk_overlap",
            display_name="Bitöverlappning",
            info="Antal tecken att överlappa mellan bitar.",
            value=200,
        ),
        IntInput(
            name="chunk_size",
            display_name="Bitstorlek",
            info=(
                "Den maximala längden för varje bit. Text delas först av separator, "
                "sedan slås bitar samman upp till denna storlek. "
                "Enskilda delningar större än detta kommer inte att delas ytterligare."
            ),
            value=1000,
        ),
        MessageTextInput(
            name="separator",
            display_name="Separator",
            info=(
                "Tecknet att dela på. Använd \\n för ny rad. "
                "Exempel: \\n\\n för stycken, \\n för rader, . för meningar"
            ),
            value="\n",
        ),
        MessageTextInput(
            name="text_key",
            display_name="Textnyckel",
            info="Nyckeln att använda för textkolumnen.",
            value="text",
            advanced=True,
        ),
        DropdownInput(
            name="keep_separator",
            display_name="Behåll separator",
            info="Om separatorn ska behållas i utmatningsbitarna och var den ska placeras.",
            options=["False", "True", "Start", "End"],
            value="False",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Bitar", name="dataframe", method="split_text"),
    ]

    def _docs_to_data(self, docs) -> list[Data]:
        return [Data(text=doc.page_content, data=doc.metadata) for doc in docs]

    def _fix_separator(self, separator: str) -> str:
        """Fix common separator issues and convert to proper format."""
        if separator == "/n":
            return "\n"
        if separator == "/t":
            return "\t"
        return separator

    def split_text_base(self):
        separator = self._fix_separator(self.separator)
        separator = unescape_string(separator)

        if isinstance(self.data_inputs, DataFrame):
            if not len(self.data_inputs):
                msg = "DataFrame is empty"
                raise TypeError(msg)

            self.data_inputs.text_key = self.text_key
            try:
                documents = self.data_inputs.to_lc_documents()
            except Exception as e:
                msg = f"Error converting DataFrame to documents: {e}"
                raise TypeError(msg) from e
        elif isinstance(self.data_inputs, Message):
            self.data_inputs = [self.data_inputs.to_data()]
            return self.split_text_base()
        else:
            if not self.data_inputs:
                msg = "No data inputs provided"
                raise TypeError(msg)

            documents = []
            if isinstance(self.data_inputs, Data):
                self.data_inputs.text_key = self.text_key
                documents = [self.data_inputs.to_lc_document()]
            else:
                try:
                    documents = [input_.to_lc_document() for input_ in self.data_inputs if isinstance(input_, Data)]
                    if not documents:
                        msg = f"No valid Data inputs found in {type(self.data_inputs)}"
                        raise TypeError(msg)
                except AttributeError as e:
                    msg = f"Invalid input type in collection: {e}"
                    raise TypeError(msg) from e
        try:
            # Convert string 'False'/'True' to boolean
            keep_sep = self.keep_separator
            if isinstance(keep_sep, str):
                if keep_sep.lower() == "false":
                    keep_sep = False
                elif keep_sep.lower() == "true":
                    keep_sep = True
                # 'start' and 'end' are kept as strings

            splitter = CharacterTextSplitter(
                chunk_overlap=self.chunk_overlap,
                chunk_size=self.chunk_size,
                separator=separator,
                keep_separator=keep_sep,
            )
            return splitter.split_documents(documents)
        except Exception as e:
            msg = f"Error splitting text: {e}"
            raise TypeError(msg) from e

    def split_text(self) -> DataFrame:
        return DataFrame(self._docs_to_data(self.split_text_base()))

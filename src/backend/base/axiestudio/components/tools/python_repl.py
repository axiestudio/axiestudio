import importlib

from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from langchain_experimental.utilities import PythonREPL
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import StrInput
from axiestudio.schema.data import Data


class PythonREPLToolComponent(LCToolComponent):
    display_name = "Python REPL [FÖRÅLDRAD]"
    description = "Ett verktyg för att köra Python-kod i en REPL-miljö."
    name = "PythonREPLTool"
    icon = "Python"
    legacy = True

    inputs = [
        StrInput(
            name="name",
            display_name="Verktygsnamn",
            info="Namnet på verktyget.",
            value="python_repl",
        ),
        StrInput(
            name="description",
            display_name="Verktygsbeskrivning",
            info="En beskrivning av verktyget.",
            value="Ett Python-skal. Använd detta för att köra python-kommandon. "
            "Inmatning ska vara ett giltigt python-kommando. "
            "Om du vill se utmatningen av ett värde ska du skriva ut det med `print(...)`.",
        ),
        StrInput(
            name="global_imports",
            display_name="Globala importer",
            info="En kommaseparerad lista med moduler att importera globalt, t.ex. 'math,numpy'.",
            value="math",
        ),
        StrInput(
            name="code",
            display_name="Python-kod",
            info="Python-koden att köra.",
            value="print('Hello, World!')",
        ),
    ]

    class PythonREPLSchema(BaseModel):
        code: str = Field(..., description="Python-koden att köra.")

    def get_globals(self, global_imports: str | list[str]) -> dict:
        global_dict = {}
        if isinstance(global_imports, str):
            modules = [module.strip() for module in global_imports.split(",")]
        elif isinstance(global_imports, list):
            modules = global_imports
        else:
            msg = "global_imports måste vara antingen en sträng eller en lista"
            raise TypeError(msg)

        for module in modules:
            try:
                imported_module = importlib.import_module(module)
                global_dict[imported_module.__name__] = imported_module
            except ImportError as e:
                msg = f"Kunde inte importera modul {module}"
                raise ImportError(msg) from e
        return global_dict

    def build_tool(self) -> Tool:
        globals_ = self.get_globals(self.global_imports)
        python_repl = PythonREPL(_globals=globals_)

        def run_python_code(code: str) -> str:
            try:
                return python_repl.run(code)
            except Exception as e:
                logger.opt(exception=True).debug("Fel vid körning av Python-kod")
                raise ToolException(str(e)) from e

        tool = StructuredTool.from_function(
            name=self.name,
            description=self.description,
            func=run_python_code,
            args_schema=self.PythonREPLSchema,
        )

        self.status = f"Python REPL-verktyg skapat med globala importer: {self.global_imports}"
        return tool

    def run_model(self) -> list[Data]:
        tool = self.build_tool()
        result = tool.run(self.code)
        return [Data(data={"result": result})]

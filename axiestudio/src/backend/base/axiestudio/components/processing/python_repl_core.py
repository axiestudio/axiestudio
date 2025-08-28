import importlib

from langchain_experimental.utilities import PythonREPL

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import CodeInput, Output, StrInput
from axiestudio.schema.data import Data


class PythonREPLComponent(Component):
    display_name = "Python-tolk"
    description = "Kör Python-kod med valfria importer. Använd print() för att se utdata."
    documentation: str = "https://docs.axiestudio.se/components-processing#python-interpreter"
    icon = "square-terminal"

    inputs = [
        StrInput(
            name="global_imports",
            display_name="Globala importer",
            info="En kommaseparerad lista med moduler att importera globalt, t.ex. 'math,numpy,pandas'.",
            value="math,pandas",
            required=True,
        ),
        CodeInput(
            name="python_code",
            display_name="Python-kod",
            info="Python-koden att köra. Endast moduler specificerade i Globala importer kan användas.",
            value="print('Hej, världen!')",
            input_types=["Message"],
            tool_mode=True,
            required=True,
        ),
    ]

    outputs = [
        Output(
            display_name="Resultat",
            name="results",
            type_=Data,
            method="run_python_repl",
        ),
    ]

    def get_globals(self, global_imports: str | list[str]) -> dict:
        """Skapa en globala dictionary med endast de importer som anges."""
        global_dict = {}

        try:
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
                    msg = f"Kunde inte importera modul {module}: {e!s}"
                    raise ImportError(msg) from e

        except Exception as e:
            self.log(f"Fel i globala importer: {e!s}")
            raise
        else:
            self.log(f"Importerade moduler framgångsrikt: {list(global_dict.keys())}")
            return global_dict

    def run_python_repl(self) -> Data:
        try:
            globals_ = self.get_globals(self.global_imports)
            python_repl = PythonREPL(_globals=globals_)
            result = python_repl.run(self.python_code)
            result = result.strip() if result else ""

            self.log("Kodkörning slutfördes framgångsrikt")
            return Data(data={"result": result})

        except ImportError as e:
            error_message = f"Importfel: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

        except SyntaxError as e:
            error_message = f"Syntaxfel: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

        except (NameError, TypeError, ValueError) as e:
            error_message = f"Fel under körning: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

    def build(self):
        return self.run_python_repl

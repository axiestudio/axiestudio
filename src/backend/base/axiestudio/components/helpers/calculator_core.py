import ast
import operator
from collections.abc import Callable

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import MessageTextInput
from axiestudio.io import Output
from axiestudio.schema.data import Data


class CalculatorComponent(Component):
    display_name = "Kalkylator"
    description = "Utför grundläggande aritmetiska operationer på ett givet uttryck."
    documentation: str = "https://docs.axiestudio.se/components-helpers#calculator"
    icon = "calculator"

    # Cachea operatörsordbok som klassvariabel
    OPERATORS: dict[type[ast.operator], Callable] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    inputs = [
        MessageTextInput(
            name="expression",
            display_name="Uttryck",
            info="Det aritmetiska uttrycket att utvärdera (t.ex. '4*4*(33/22)+12-20').",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Data", name="result", type_=Data, method="evaluate_expression"),
    ]

    def _eval_expr(self, node: ast.AST) -> float:
        """Utvärdera en AST-nod rekursivt."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int | float):
                return float(node.value)
            error_msg = f"Konstant typ som inte stöds: {type(node.value).__name__}"
            raise TypeError(error_msg)
        if isinstance(node, ast.Num):  # För bakåtkompatibilitet
            if isinstance(node.n, int | float):
                return float(node.n)
            error_msg = f"Taltyp som inte stöds: {type(node.n).__name__}"
            raise TypeError(error_msg)

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.OPERATORS:
                error_msg = f"Binär operator som inte stöds: {op_type.__name__}"
                raise TypeError(error_msg)

            left = self._eval_expr(node.left)
            right = self._eval_expr(node.right)
            return self.OPERATORS[op_type](left, right)

        error_msg = f"Operation eller uttryckstyp som inte stöds: {type(node).__name__}"
        raise TypeError(error_msg)

    def evaluate_expression(self) -> Data:
        """Utvärdera det matematiska uttrycket och returnera resultatet."""
        try:
            tree = ast.parse(self.expression, mode="eval")
            result = self._eval_expr(tree.body)

            formatted_result = f"{float(result):.6f}".rstrip("0").rstrip(".")
            self.log(f"Beräkningsresultat: {formatted_result}")

            self.status = formatted_result
            return Data(data={"result": formatted_result})

        except ZeroDivisionError:
            error_message = "Fel: Division med noll"
            self.status = error_message
            return Data(data={"error": error_message, "input": self.expression})

        except (SyntaxError, TypeError, KeyError, ValueError, AttributeError, OverflowError) as e:
            error_message = f"Ogiltigt uttryck: {e!s}"
            self.status = error_message
            return Data(data={"error": error_message, "input": self.expression})

    def build(self):
        """Returnera huvudutvärderingsfunktionen."""
        return self.evaluate_expression

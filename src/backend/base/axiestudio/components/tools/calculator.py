import ast
import operator

from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import MessageTextInput
from axiestudio.schema.data import Data


class CalculatorToolComponent(LCToolComponent):
    display_name = "Kalkylator [FÖRÅLDRAD]"
    description = "Utför grundläggande aritmetiska operationer på ett givet uttryck."
    icon = "calculator"
    name = "CalculatorTool"
    legacy = True

    inputs = [
        MessageTextInput(
            name="expression",
            display_name="Uttryck",
            info="Det aritmetiska uttrycket att utvärdera (t.ex. '4*4*(33/22)+12-20').",
        ),
    ]

    class CalculatorToolSchema(BaseModel):
        expression: str = Field(..., description="Det aritmetiska uttrycket att utvärdera.")

    def run_model(self) -> list[Data]:
        return self._evaluate_expression(self.expression)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="calculator",
            description="Utvärdera grundläggande aritmetiska uttryck. Indata ska vara en sträng som innehåller uttrycket.",
            func=self._eval_expr_with_error,
            args_schema=self.CalculatorToolSchema,
        )

    def _eval_expr(self, node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            left_val = self._eval_expr(node.left)
            right_val = self._eval_expr(node.right)
            return self.operators[type(node.op)](left_val, right_val)
        if isinstance(node, ast.UnaryOp):
            operand_val = self._eval_expr(node.operand)
            return self.operators[type(node.op)](operand_val)
        if isinstance(node, ast.Call):
            msg = (
                "Funktionsanrop som sqrt(), sin(), cos() etc. stöds inte. "
                "Endast grundläggande aritmetiska operationer (+, -, *, /, **) är tillåtna."
            )
            raise TypeError(msg)
        msg = f"Operation eller uttryckstyp som inte stöds: {type(node).__name__}"
        raise TypeError(msg)

    def _eval_expr_with_error(self, expression: str) -> list[Data]:
        try:
            return self._evaluate_expression(expression)
        except Exception as e:
            raise ToolException(str(e)) from e

    def _evaluate_expression(self, expression: str) -> list[Data]:
        try:
            # Parse the expression and evaluate it
            tree = ast.parse(expression, mode="eval")
            result = self._eval_expr(tree.body)

            # Format the result to a reasonable number of decimal places
            formatted_result = f"{result:.6f}".rstrip("0").rstrip(".")

            self.status = formatted_result
            return [Data(data={"result": formatted_result})]

        except (SyntaxError, TypeError, KeyError) as e:
            error_message = f"Ogiltigt uttryck: {e}"
            self.status = error_message
            return [Data(data={"error": error_message, "input": expression})]
        except ZeroDivisionError:
            error_message = "Fel: Division med noll"
            self.status = error_message
            return [Data(data={"error": error_message, "input": expression})]
        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Fel vid utvärdering av uttryck")
            error_message = f"Fel: {e}"
            self.status = error_message
            return [Data(data={"error": error_message, "input": expression})]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }

﻿"""Processing components for AxieStudio."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from axi.components._importing import import_mod

if TYPE_CHECKING:
    from axi.components.processing.alter_metadata import AlterMetadataComponent
    from axi.components.processing.batch_run import BatchRunComponent
    from axi.components.processing.combine_text import CombineTextComponent
    from axi.components.processing.converter import TypeConverterComponent
    from axi.components.processing.create_data import CreateDataComponent
    from axi.components.processing.data_operations import DataOperationsComponent
    from axi.components.processing.data_to_dataframe import DataToDataFrameComponent
    from axi.components.processing.dataframe_operations import DataFrameOperationsComponent
    from axi.components.processing.extract_key import ExtractDataKeyComponent
    from axi.components.processing.filter_data import FilterDataComponent
    from axi.components.processing.filter_data_values import DataFilterComponent
    from axi.components.processing.json_cleaner import JSONCleaner
    from axi.components.processing.lambda_filter import LambdaFilterComponent
    from axi.components.processing.llm_router import LLMRouterComponent
    from axi.components.processing.merge_data import MergeDataComponent
    from axi.components.processing.message_to_data import MessageToDataComponent
    from axi.components.processing.parse_data import ParseDataComponent
    from axi.components.processing.parse_dataframe import ParseDataFrameComponent
    from axi.components.processing.parse_json_data import ParseJSONDataComponent
    from axi.components.processing.parser import ParserComponent
    from axi.components.processing.prompt import PromptComponent
    from axi.components.processing.python_repl_core import PythonREPLComponent
    from axi.components.processing.regex import RegexExtractorComponent
    from axi.components.processing.save_file import SaveToFileComponent
    from axi.components.processing.select_data import SelectDataComponent
    from axi.components.processing.split_text import SplitTextComponent
    from axi.components.processing.structured_output import StructuredOutputComponent
    from axi.components.processing.update_data import UpdateDataComponent

_dynamic_imports = {
    "AlterMetadataComponent": "alter_metadata",
    "BatchRunComponent": "batch_run",
    "CombineTextComponent": "combine_text",
    "TypeConverterComponent": "converter",
    "CreateDataComponent": "create_data",
    "DataOperationsComponent": "data_operations",
    "DataToDataFrameComponent": "data_to_dataframe",
    "DataFrameOperationsComponent": "dataframe_operations",
    "ExtractDataKeyComponent": "extract_key",
    "FilterDataComponent": "filter_data",
    "DataFilterComponent": "filter_data_values",
    "JSONCleaner": "json_cleaner",
    "LambdaFilterComponent": "lambda_filter",
    "LLMRouterComponent": "llm_router",
    "MergeDataComponent": "merge_data",
    "MessageToDataComponent": "message_to_data",
    "ParseDataComponent": "parse_data",
    "ParseDataFrameComponent": "parse_dataframe",
    "ParseJSONDataComponent": "parse_json_data",
    "ParserComponent": "parser",
    "PromptComponent": "prompt",
    "PythonREPLComponent": "python_repl_core",
    "RegexExtractorComponent": "regex",
    "SaveToFileComponent": "save_file",
    "SelectDataComponent": "select_data",
    "SplitTextComponent": "split_text",
    "StructuredOutputComponent": "structured_output",
    "UpdateDataComponent": "update_data",
}

__all__ = [
    "AlterMetadataComponent",
    "BatchRunComponent",
    "CombineTextComponent",
    "CreateDataComponent",
    "DataFilterComponent",
    "DataFrameOperationsComponent",
    "DataOperationsComponent",
    "DataToDataFrameComponent",
    "ExtractDataKeyComponent",
    "FilterDataComponent",
    "JSONCleaner",
    "LLMRouterComponent",
    "LambdaFilterComponent",
    "MergeDataComponent",
    "MessageToDataComponent",
    "ParseDataComponent",
    "ParseDataFrameComponent",
    "ParseJSONDataComponent",
    "ParserComponent",
    "PromptComponent",
    "PythonREPLComponent",
    "RegexExtractorComponent",
    "SaveToFileComponent",
    "SelectDataComponent",
    "SplitTextComponent",
    "StructuredOutputComponent",
    "TypeConverterComponent",
    "UpdateDataComponent",
]


def __getattr__(attr_name: str) -> Any:
    """Lazily import processing components on attribute access."""
    if attr_name not in _dynamic_imports:
        msg = f"module '{__name__}' has no attribute '{attr_name}'"
        raise AttributeError(msg)
    try:
        result = import_mod(attr_name, _dynamic_imports[attr_name], __spec__.parent)
    except (ModuleNotFoundError, ImportError, AttributeError) as e:
        msg = f"Could not import '{attr_name}' from '{__name__}': {e}"
        raise AttributeError(msg) from e
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)

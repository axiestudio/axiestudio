import ast
import pprint
from enum import Enum

import yfinance as yf
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import DropdownInput, IntInput, MessageTextInput
from axiestudio.schema.data import Data


class YahooFinanceMethod(Enum):
    GET_INFO = "get_info"
    GET_NEWS = "get_news"
    GET_ACTIONS = "get_actions"
    GET_ANALYSIS = "get_analysis"
    GET_BALANCE_SHEET = "get_balance_sheet"
    GET_CALENDAR = "get_calendar"
    GET_CASHFLOW = "get_cashflow"
    GET_INSTITUTIONAL_HOLDERS = "get_institutional_holders"
    GET_RECOMMENDATIONS = "get_recommendations"
    GET_SUSTAINABILITY = "get_sustainability"
    GET_MAJOR_HOLDERS = "get_major_holders"
    GET_MUTUALFUND_HOLDERS = "get_mutualfund_holders"
    GET_INSIDER_PURCHASES = "get_insider_purchases"
    GET_INSIDER_TRANSACTIONS = "get_insider_transactions"
    GET_INSIDER_ROSTER_HOLDERS = "get_insider_roster_holders"
    GET_DIVIDENDS = "get_dividends"
    GET_CAPITAL_GAINS = "get_capital_gains"
    GET_SPLITS = "get_splits"
    GET_SHARES = "get_shares"
    GET_FAST_INFO = "get_fast_info"
    GET_SEC_FILINGS = "get_sec_filings"
    GET_RECOMMENDATIONS_SUMMARY = "get_recommendations_summary"
    GET_UPGRADES_DOWNGRADES = "get_upgrades_downgrades"
    GET_EARNINGS = "get_earnings"
    GET_INCOME_STMT = "get_income_stmt"


class YahooFinanceSchema(BaseModel):
    symbol: str = Field(..., description="Aktiesymbolen att hämta data för.")
    method: YahooFinanceMethod = Field(YahooFinanceMethod.GET_INFO, description="Typen av data att hämta.")
    num_news: int | None = Field(5, description="Antalet nyhetsartiklar att hämta.")


class YfinanceToolComponent(LCToolComponent):
    display_name = "Yahoo! Finance [FÖRÅLDRAD]"
    description = """Använder [yfinance](https://pypi.org/project/yfinance/) (inofficiellt paket) \
för att komma åt finansiell data och marknadsinformation från Yahoo! Finance."""
    icon = "trending-up"
    name = "YahooFinanceTool"
    legacy = True

    inputs = [
        MessageTextInput(
            name="symbol",
            display_name="Aktiesymbol",
            info="Aktiesymbolen att hämta data för (t.ex. AAPL, GOOG).",
        ),
        DropdownInput(
            name="method",
            display_name="Datametod",
            info="Typen av data att hämta.",
            options=list(YahooFinanceMethod),
            value="get_news",
        ),
        IntInput(
            name="num_news",
            display_name="Antal nyheter",
            info="Antalet nyhetsartiklar att hämta (gäller endast för get_news).",
            value=5,
        ),
    ]

    def run_model(self) -> list[Data]:
        return self._yahoo_finance_tool(
            self.symbol,
            self.method,
            self.num_news,
        )

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="yahoo_finance",
            description="Komma åt finansiell data och marknadsinformation från Yahoo! Finance.",
            func=self._yahoo_finance_tool,
            args_schema=YahooFinanceSchema,
        )

    def _yahoo_finance_tool(
        self,
        symbol: str,
        method: YahooFinanceMethod,
        num_news: int | None = 5,
    ) -> list[Data]:
        ticker = yf.Ticker(symbol)

        try:
            if method == YahooFinanceMethod.GET_INFO:
                result = ticker.info
            elif method == YahooFinanceMethod.GET_NEWS:
                result = ticker.news[:num_news]
            else:
                result = getattr(ticker, method.value)()

            result = pprint.pformat(result)

            if method == YahooFinanceMethod.GET_NEWS:
                data_list = [Data(data=article) for article in ast.literal_eval(result)]
            else:
                data_list = [Data(data={"result": result})]

        except Exception as e:
            error_message = f"Fel vid hämtning av data: {e}"
            logger.debug(error_message)
            self.status = error_message
            raise ToolException(error_message) from e

        return data_list

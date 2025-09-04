from enum import Enum

import httpx
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException
from loguru import logger
from pydantic import BaseModel, Field

from axiestudio.base.langchain_utilities.model import LCToolComponent
from axiestudio.field_typing import Tool
from axiestudio.inputs.inputs import BoolInput, DropdownInput, IntInput, MessageTextInput, SecretStrInput
from axiestudio.schema.data import Data

# Add at the top with other constants
MAX_CHUNKS_PER_SOURCE = 3


class TavilySearchDepth(Enum):
    BASIC = "basic"
    ADVANCED = "advanced"


class TavilySearchTopic(Enum):
    GENERAL = "general"
    NEWS = "news"


class TavilySearchTimeRange(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class TavilySearchSchema(BaseModel):
    query: str = Field(..., description="Sökfrågan du vill utföra med Tavily.")
    search_depth: TavilySearchDepth = Field(TavilySearchDepth.BASIC, description="Djupet på sökningen.")
    topic: TavilySearchTopic = Field(TavilySearchTopic.GENERAL, description="Kategorin för sökningen.")
    max_results: int = Field(5, description="Maximalt antal sökresultat att returnera.")
    include_images: bool = Field(default=False, description="Inkludera en lista med frågerelaterade bilder i svaret.")
    include_answer: bool = Field(default=False, description="Inkludera ett kort svar på den ursprungliga frågan.")
    chunks_per_source: int = Field(
        default=MAX_CHUNKS_PER_SOURCE,
        description=(
            "Antal innehållsdelar att hämta från varje källa (max 500 tecken vardera). Endast för avancerad sökning."
        ),
        ge=1,
        le=MAX_CHUNKS_PER_SOURCE,
    )
    include_domains: list[str] = Field(
        default=[],
        description="En lista över domäner att specifikt inkludera i sökresultaten.",
    )
    exclude_domains: list[str] = Field(
        default=[],
        description="En lista över domäner att specifikt exkludera från sökresultaten.",
    )
    include_raw_content: bool = Field(
        default=False,
        description="Inkludera det rensade och tolkade HTML-innehållet från varje sökresultat.",
    )
    days: int = Field(
        default=7,
        description="Antal dagar bakåt från aktuellt datum att inkludera. Endast tillgängligt om ämnet är nyheter.",
        ge=1,
    )
    time_range: TavilySearchTimeRange | None = Field(
        default=None,
        description="Tidsintervallet bakåt från aktuellt datum för att filtrera resultat.",
    )


class TavilySearchToolComponent(LCToolComponent):
    display_name = "Tavily Search API"
    description = """**Tavily Search API** är en sökmotor optimerad för LLM:er och RAG, \
        inriktad på effektiva, snabba och beständiga sökresultat. Den kan användas självständigt eller som ett agentverktyg.

Obs: Markera 'Avancerat' för alla alternativ.
"""
    icon = "TavilyIcon"
    name = "TavilyAISearch"
    documentation = "https://docs.tavily.com/"
    legacy = True

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="Tavily API-nyckel",
            required=True,
            info="Din Tavily API-nyckel.",
        ),
        MessageTextInput(
            name="query",
            display_name="Sökfråga",
            info="Sökfrågan du vill utföra med Tavily.",
        ),
        DropdownInput(
            name="search_depth",
            display_name="Sökdjup",
            info="Djupet på sökningen.",
            options=list(TavilySearchDepth),
            value=TavilySearchDepth.ADVANCED,
            advanced=True,
        ),
        IntInput(
            name="chunks_per_source",
            display_name="Delar per källa",
            info=("Antal innehållsdelar att hämta från varje källa (1-3). Fungerar endast med avancerad sökning."),
            value=MAX_CHUNKS_PER_SOURCE,
            advanced=True,
        ),
        DropdownInput(
            name="topic",
            display_name="Sökämne",
            info="Kategorin för sökningen.",
            options=list(TavilySearchTopic),
            value=TavilySearchTopic.GENERAL,
            advanced=True,
        ),
        IntInput(
            name="days",
            display_name="Dagar",
            info="Antal dagar bakåt från aktuellt datum att inkludera. Endast tillgängligt med nyhetsämne.",
            value=7,
            advanced=True,
        ),
        IntInput(
            name="max_results",
            display_name="Max resultat",
            info="Maximalt antal sökresultat att returnera.",
            value=5,
            advanced=True,
        ),
        BoolInput(
            name="include_answer",
            display_name="Inkludera svar",
            info="Inkludera ett kort svar på den ursprungliga frågan.",
            value=True,
            advanced=True,
        ),
        DropdownInput(
            name="time_range",
            display_name="Tidsintervall",
            info="Tidsintervallet bakåt från aktuellt datum för att filtrera resultat.",
            options=list(TavilySearchTimeRange),
            value=None,
            advanced=True,
        ),
        BoolInput(
            name="include_images",
            display_name="Inkludera bilder",
            info="Inkludera en lista med frågrelaterade bilder i svaret.",
            value=True,
            advanced=True,
        ),
        MessageTextInput(
            name="include_domains",
            display_name="Inkludera domäner",
            info="Kommaseparerad lista med domäner att inkludera i sökresultaten.",
            advanced=True,
        ),
        MessageTextInput(
            name="exclude_domains",
            display_name="Exkludera domäner",
            info="Kommaseparerad lista med domäner att exkludera från sökresultaten.",
            advanced=True,
        ),
        BoolInput(
            name="include_raw_content",
            display_name="Inkludera råinnehåll",
            info="Inkludera det rensade och tolkade HTML-innehållet för varje sökresultat.",
            value=False,
            advanced=True,
        ),
    ]

    def run_model(self) -> list[Data]:
        # Convert string values to enum instances with validation
        try:
            search_depth_enum = (
                self.search_depth
                if isinstance(self.search_depth, TavilySearchDepth)
                else TavilySearchDepth(str(self.search_depth).lower())
            )
        except ValueError as e:
            error_message = f"Invalid search depth value: {e!s}"
            self.status = error_message
            return [Data(data={"error": error_message})]

        try:
            topic_enum = (
                self.topic if isinstance(self.topic, TavilySearchTopic) else TavilySearchTopic(str(self.topic).lower())
            )
        except ValueError as e:
            error_message = f"Invalid topic value: {e!s}"
            self.status = error_message
            return [Data(data={"error": error_message})]

        try:
            time_range_enum = (
                self.time_range
                if isinstance(self.time_range, TavilySearchTimeRange)
                else TavilySearchTimeRange(str(self.time_range).lower())
                if self.time_range
                else None
            )
        except ValueError as e:
            error_message = f"Invalid time range value: {e!s}"
            self.status = error_message
            return [Data(data={"error": error_message})]

        # Initialize domain variables as None
        include_domains = None
        exclude_domains = None

        # Only process domains if they're provided
        if self.include_domains:
            include_domains = [domain.strip() for domain in self.include_domains.split(",") if domain.strip()]

        if self.exclude_domains:
            exclude_domains = [domain.strip() for domain in self.exclude_domains.split(",") if domain.strip()]

        return self._tavily_search(
            self.query,
            search_depth=search_depth_enum,
            topic=topic_enum,
            max_results=self.max_results,
            include_images=self.include_images,
            include_answer=self.include_answer,
            chunks_per_source=self.chunks_per_source,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_raw_content=self.include_raw_content,
            days=self.days,
            time_range=time_range_enum,
        )

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="tavily_search",
            description="Perform a web search using the Tavily API.",
            func=self._tavily_search,
            args_schema=TavilySearchSchema,
        )

    def _tavily_search(
        self,
        query: str,
        *,
        search_depth: TavilySearchDepth = TavilySearchDepth.BASIC,
        topic: TavilySearchTopic = TavilySearchTopic.GENERAL,
        max_results: int = 5,
        include_images: bool = False,
        include_answer: bool = False,
        chunks_per_source: int = MAX_CHUNKS_PER_SOURCE,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_raw_content: bool = False,
        days: int = 7,
        time_range: TavilySearchTimeRange | None = None,
    ) -> list[Data]:
        # Validate enum values
        if not isinstance(search_depth, TavilySearchDepth):
            msg = f"Invalid search_depth value: {search_depth}"
            raise TypeError(msg)
        if not isinstance(topic, TavilySearchTopic):
            msg = f"Invalid topic value: {topic}"
            raise TypeError(msg)

        # Validate chunks_per_source range
        if not 1 <= chunks_per_source <= MAX_CHUNKS_PER_SOURCE:
            msg = f"chunks_per_source must be between 1 and {MAX_CHUNKS_PER_SOURCE}, got {chunks_per_source}"
            raise ValueError(msg)

        # Validate days is positive
        if days < 1:
            msg = f"days must be greater than or equal to 1, got {days}"
            raise ValueError(msg)

        try:
            url = "https://api.tavily.com/search"
            headers = {
                "content-type": "application/json",
                "accept": "application/json",
            }
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": search_depth.value,
                "topic": topic.value,
                "max_results": max_results,
                "include_images": include_images,
                "include_answer": include_answer,
                "chunks_per_source": chunks_per_source if search_depth == TavilySearchDepth.ADVANCED else None,
                "include_domains": include_domains if include_domains else None,
                "exclude_domains": exclude_domains if exclude_domains else None,
                "include_raw_content": include_raw_content,
                "days": days if topic == TavilySearchTopic.NEWS else None,
                "time_range": time_range.value if time_range else None,
            }

            with httpx.Client(timeout=90.0) as client:
                response = client.post(url, json=payload, headers=headers)

            response.raise_for_status()
            search_results = response.json()

            data_results = [
                Data(
                    data={
                        "title": result.get("title"),
                        "url": result.get("url"),
                        "content": result.get("content"),
                        "score": result.get("score"),
                        "raw_content": result.get("raw_content") if include_raw_content else None,
                    }
                )
                for result in search_results.get("results", [])
            ]

            if include_answer and search_results.get("answer"):
                data_results.insert(0, Data(data={"answer": search_results["answer"]}))

            if include_images and search_results.get("images"):
                data_results.append(Data(data={"images": search_results["images"]}))

            self.status = data_results  # type: ignore[assignment]

        except httpx.TimeoutException as e:
            error_message = "Request timed out (90s). Please try again or adjust parameters."
            logger.error(f"Timeout error: {e}")
            self.status = error_message
            raise ToolException(error_message) from e
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP error: {e.response.status_code} - {e.response.text}"
            logger.debug(error_message)
            self.status = error_message
            raise ToolException(error_message) from e
        except Exception as e:
            error_message = f"Unexpected error: {e}"
            logger.opt(exception=True).debug("Error running Tavily Search")
            self.status = error_message
            raise ToolException(error_message) from e
        return data_results

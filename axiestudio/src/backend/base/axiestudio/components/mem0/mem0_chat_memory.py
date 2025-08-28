import os

from loguru import logger
from mem0 import Memory, MemoryClient

from axiestudio.base.memory.model import LCChatMemoryComponent
from axiestudio.inputs.inputs import (
    DictInput,
    HandleInput,
    MessageTextInput,
    NestedDictInput,
    SecretStrInput,
)
from axiestudio.io import Output
from axiestudio.schema.data import Data


class Mem0MemoryComponent(LCChatMemoryComponent):
    display_name = "Mem0-chattminne"
    description = "Hämtar och lagrar chattmeddelanden med Mem0-minneslagring."
    name = "mem0_chat_memory"
    icon: str = "Mem0"
    inputs = [
        NestedDictInput(
            name="mem0_config",
            display_name="Mem0-konfiguration",
            info="""Konfigurationsordbok för att initialisera Mem0-minnesinstans.
                    Exempel:
                    {
                        "graph_store": {
                            "provider": "neo4j",
                            "config": {
                                "url": "neo4j+s://your-neo4j-url",
                                "username": "neo4j",
                                "password": "your-password"
                            }
                        },
                        "version": "v1.1"
                    }""",
            input_types=["Data"],
        ),
        MessageTextInput(
            name="ingest_message",
            display_name="Meddelande att mata in",
            info="Meddelandeinnehållet som ska matas in i Mem0-minnet.",
        ),
        HandleInput(
            name="existing_memory",
            display_name="Befintlig minnesinstans",
            input_types=["Memory"],
            info="Valfri befintlig Mem0-minnesinstans. Om inte angiven kommer en ny instans att skapas.",
        ),
        MessageTextInput(
            name="user_id", display_name="Användar-ID", info="Identifierare för användaren associerad med meddelandena."
        ),
        MessageTextInput(
            name="search_query", display_name="Sökfråga", info="Inmatningstext för att söka relaterade minnen i Mem0."
        ),
        SecretStrInput(
            name="mem0_api_key",
            display_name="Mem0 API-nyckel",
            info="API-nyckel för Mem0-plattformen. Lämna tom för att använda den lokala versionen.",
        ),
        DictInput(
            name="metadata",
            display_name="Metadata",
            info="Ytterligare metadata att associera med det inmatade meddelandet.",
            advanced=True,
        ),
        SecretStrInput(
            name="openai_api_key",
            display_name="OpenAI API-nyckel",
            required=False,
            info="API-nyckel för OpenAI. Krävs om du använder OpenAI-inbäddningar utan en angiven konfiguration.",
        ),
    ]

    outputs = [
        Output(name="memory", display_name="Mem0-minne", method="ingest_data"),
        Output(
            name="search_results",
            display_name="Sökresultat",
            method="build_search_results",
        ),
    ]

    def build_mem0(self) -> Memory:
        """Initializes a Mem0 memory instance based on provided configuration and API keys."""
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key

        try:
            if not self.mem0_api_key:
                return Memory.from_config(config_dict=dict(self.mem0_config)) if self.mem0_config else Memory()
            if self.mem0_config:
                return MemoryClient.from_config(api_key=self.mem0_api_key, config_dict=dict(self.mem0_config))
            return MemoryClient(api_key=self.mem0_api_key)
        except ImportError as e:
            msg = "Mem0 is not properly installed. Please install it with 'pip install -U mem0ai'."
            raise ImportError(msg) from e

    def ingest_data(self) -> Memory:
        """Ingests a new message into Mem0 memory and returns the updated memory instance."""
        mem0_memory = self.existing_memory or self.build_mem0()

        if not self.ingest_message or not self.user_id:
            logger.warning("Saknar 'ingest_message' eller 'user_id'; kan inte mata in data.")
            return mem0_memory

        metadata = self.metadata or {}

        logger.info("Matar in meddelande för user_id: %s", self.user_id)

        try:
            mem0_memory.add(self.ingest_message, user_id=self.user_id, metadata=metadata)
        except Exception:
            logger.exception("Misslyckades med att lägga till meddelande i Mem0-minnet.")
            raise

        return mem0_memory

    def build_search_results(self) -> Data:
        """Searches the Mem0 memory for related messages based on the search query and returns the results."""
        mem0_memory = self.ingest_data()
        search_query = self.search_query
        user_id = self.user_id

        logger.info("Search query: %s", search_query)

        try:
            if search_query:
                logger.info("Performing search with query.")
                related_memories = mem0_memory.search(query=search_query, user_id=user_id)
            else:
                logger.info("Retrieving all memories for user_id: %s", user_id)
                related_memories = mem0_memory.get_all(user_id=user_id)
        except Exception:
            logger.exception("Failed to retrieve related memories from Mem0.")
            raise

        logger.info("Related memories retrieved: %s", related_memories)
        return related_memories

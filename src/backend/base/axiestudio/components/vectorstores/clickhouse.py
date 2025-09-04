from langchain_community.vectorstores import Clickhouse, ClickhouseSettings

from axiestudio.base.vectorstores.model import LCVectorStoreComponent, check_cached_vector_store
from axiestudio.helpers.data import docs_to_data
from axiestudio.inputs.inputs import BoolInput, FloatInput
from axiestudio.io import (
    DictInput,
    DropdownInput,
    HandleInput,
    IntInput,
    SecretStrInput,
    StrInput,
)
from axiestudio.schema.data import Data


class ClickhouseVectorStoreComponent(LCVectorStoreComponent):
    display_name = "Clickhouse"
    description = "Clickhouse Vektorlager med sökmöjligheter"
    name = "Clickhouse"
    icon = "Clickhouse"

    inputs = [
        StrInput(name="host", display_name="Värdnamn", required=True, value="localhost"),
        IntInput(name="port", display_name="Port", required=True, value=8123),
        StrInput(name="database", display_name="Databas", required=True),
        StrInput(name="table", display_name="Tabellnamn", required=True),
        StrInput(name="username", display_name="ClickHouse användarnamn", required=True),
        SecretStrInput(name="password", display_name="Lösenord för användaren", required=True),
        DropdownInput(
            name="index_type",
            display_name="Indextyp",
            options=["annoy", "vector_similarity"],
            info="Typ av index.",
            value="annoy",
            advanced=True,
        ),
        DropdownInput(
            name="metric",
            display_name="Mätmetod",
            options=["angular", "euclidean", "manhattan", "hamming", "dot"],
            info="Mätmetod för att beräkna avstånd.",
            value="angular",
            advanced=True,
        ),
        BoolInput(
            name="secure",
            display_name="Använd https/TLS. Detta åsidosätter härledda värden från gränssnitt eller portargument.",
            value=False,
            advanced=True,
        ),
        StrInput(name="index_param", display_name="Indexparameter", value="100,'L2Distance'", advanced=True),
        DictInput(name="index_query_params", display_name="Indexfrågeparametrar", advanced=True),
        *LCVectorStoreComponent.inputs,
        HandleInput(name="embedding", display_name="Inbäddning", input_types=["Embeddings"]),
        IntInput(
            name="number_of_results",
            display_name="Antal resultat",
            info="Antal resultat att returnera.",
            value=4,
            advanced=True,
        ),
        FloatInput(name="score_threshold", display_name="Poängtröskel", advanced=True),
    ]

    @check_cached_vector_store
    def build_vector_store(self) -> Clickhouse:
        try:
            import clickhouse_connect
        except ImportError as e:
            msg = (
                "Misslyckades med att importera Clickhouse-beroenden. "
                "Installera det med `uv pip install axiestudio[clickhouse-connect] --pre`"
            )
            raise ImportError(msg) from e

        try:
            client = clickhouse_connect.get_client(
                host=self.host, port=self.port, username=self.username, password=self.password
            )
            client.command("SELECT 1")
        except Exception as e:
            msg = f"Misslyckades med att ansluta till Clickhouse: {e}"
            raise ValueError(msg) from e

        # Convert DataFrame to Data if needed using parent's method
        self.ingest_data = self._prepare_ingest_data()

        documents = []
        for _input in self.ingest_data or []:
            if isinstance(_input, Data):
                documents.append(_input.to_lc_document())
            else:
                documents.append(_input)

        kwargs = {}
        if self.index_param:
            kwargs["index_param"] = self.index_param.split(",")
        if self.index_query_params:
            kwargs["index_query_params"] = self.index_query_params

        settings = ClickhouseSettings(
            table=self.table,
            database=self.database,
            host=self.host,
            index_type=self.index_type,
            metric=self.metric,
            password=self.password,
            port=self.port,
            secure=self.secure,
            username=self.username,
            **kwargs,
        )
        if documents:
            clickhouse_vs = Clickhouse.from_documents(documents=documents, embedding=self.embedding, config=settings)

        else:
            clickhouse_vs = Clickhouse(embedding=self.embedding, config=settings)

        return clickhouse_vs

    def search_documents(self) -> list[Data]:
        vector_store = self.build_vector_store()

        if self.search_query and isinstance(self.search_query, str) and self.search_query.strip():
            kwargs = {}
            if self.score_threshold:
                kwargs["score_threshold"] = self.score_threshold

            docs = vector_store.similarity_search(query=self.search_query, k=self.number_of_results, **kwargs)

            data = docs_to_data(docs)
            self.status = data
            return data
        return []

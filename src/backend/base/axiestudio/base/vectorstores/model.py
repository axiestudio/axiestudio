from abc import abstractmethod
from functools import wraps
from typing import TYPE_CHECKING, Any

from axiestudio.custom.custom_component.component import Component
from axiestudio.field_typing import Text, VectorStore
from axiestudio.helpers.data import docs_to_data
from axiestudio.inputs.inputs import BoolInput
from axiestudio.io import HandleInput, Output, QueryInput
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame

if TYPE_CHECKING:
    from langchain_core.documents import Document


def check_cached_vector_store(f):
    """Decorator to check for cached vector stores, and returns them if they exist.

    Note: caching only occurs during the execution of a component - they do not persist
    across separate invocations of the component. This method exists so that components with
    multiple output methods share the same vector store during the same invocation of the
    component.
    """

    @wraps(f)
    def check_cached(self, *args, **kwargs):
        should_cache = getattr(self, "should_cache_vector_store", True)

        if should_cache and self._cached_vector_store is not None:
            return self._cached_vector_store

        result = f(self, *args, **kwargs)
        self._cached_vector_store = result
        return result

    check_cached.is_cached_vector_store_checked = True
    return check_cached


class LCVectorStoreComponent(Component):
    # Used to ensure a single vector store is built for each run of the flow
    _cached_vector_store: VectorStore | None = None

    def __init_subclass__(cls, **kwargs):
        """Enforces the check cached decorator on all subclasses."""
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "build_vector_store"):
            method = cls.build_vector_store
            if not hasattr(method, "is_cached_vector_store_checked"):
                msg = (
                    f"Metoden 'build_vector_store' i klass {cls.__name__} "
                    "måste dekoreras med @check_cached_vector_store"
                )
                raise TypeError(msg)

    trace_type = "retriever"

    inputs = [
        HandleInput(
            name="ingest_data",
            display_name="Mata in data",
            input_types=["Data", "DataFrame"],
            is_list=True,
        ),
        QueryInput(
            name="search_query",
            display_name="Sökfråga",
            info="Ange en fråga för att köra en likhetsökning.",
            placeholder="Ange en fråga...",
            tool_mode=True,
        ),
        BoolInput(
            name="should_cache_vector_store",
            display_name="Cacha vektorlager",
            value=True,
            advanced=True,
            info="Om True kommer vektorlagret att cachas för den aktuella byggnationen av komponenten. "
            "Detta är användbart för komponenter som har flera utdatametoder och vill dela samma vektorlager.",
        ),
    ]

    outputs = [
        Output(
            display_name="Sökresultat",
            name="search_results",
            method="search_documents",
        ),
        Output(display_name="DataFrame", name="dataframe", method="as_dataframe"),
    ]

    def _validate_outputs(self) -> None:
        # At least these three outputs must be defined
        required_output_methods = [
            "search_documents",
            "build_vector_store",
        ]
        output_names = [output.name for output in self.outputs]
        for method_name in required_output_methods:
            if method_name not in output_names:
                msg = f"Output med namnet '{method_name}' måste definieras."
                raise ValueError(msg)
            if not hasattr(self, method_name):
                msg = f"Metoden '{method_name}' måste definieras."
                raise ValueError(msg)

    def _prepare_ingest_data(self) -> list[Any]:
        """Prepares ingest_data by converting DataFrame to Data if needed."""
        ingest_data: list | Data | DataFrame = self.ingest_data
        if not ingest_data:
            return []

        if not isinstance(ingest_data, list):
            ingest_data = [ingest_data]

        result = []

        for _input in ingest_data:
            if isinstance(_input, DataFrame):
                result.extend(_input.to_data_list())
            else:
                result.append(_input)
        return result

    def search_with_vector_store(
        self,
        input_value: Text,
        search_type: str,
        vector_store: VectorStore,
        k=10,
        **kwargs,
    ) -> list[Data]:
        """Search for data in the vector store based on the input value and search type.

        Args:
            input_value (Text): The input value to search for.
            search_type (str): The type of search to perform.
            vector_store (VectorStore): The vector store to search in.
            k (int): The number of results to return.
            **kwargs: Additional keyword arguments to pass to the vector store search method.

        Returns:
            List[Data]: A list of data matching the search criteria.

        Raises:
            ValueError: If invalid inputs are provided.
        """
        docs: list[Document] = []
        if input_value and isinstance(input_value, str) and hasattr(vector_store, "search"):
            docs = vector_store.search(query=input_value, search_type=search_type.lower(), k=k, **kwargs)
        else:
            msg = "Invalid inputs provided."
            raise ValueError(msg)
        data = docs_to_data(docs)
        self.status = data
        return data

    def search_documents(self) -> list[Data]:
        """Search for documents in the vector store."""
        if self._cached_vector_store is not None:
            vector_store = self._cached_vector_store
        else:
            vector_store = self.build_vector_store()
            self._cached_vector_store = vector_store

        search_query: str = self.search_query
        if not search_query:
            self.status = ""
            return []

        self.log(f"Search input: {search_query}")
        self.log(f"Search type: {self.search_type}")
        self.log(f"Number of results: {self.number_of_results}")

        search_results = self.search_with_vector_store(
            search_query, self.search_type, vector_store, k=self.number_of_results
        )
        self.status = search_results
        return search_results

    def as_dataframe(self) -> DataFrame:
        return DataFrame(self.search_documents())

    def get_retriever_kwargs(self):
        """Get the retriever kwargs. Implementations can override this method to provide custom retriever kwargs."""
        return {}

    @abstractmethod
    @check_cached_vector_store
    def build_vector_store(self) -> VectorStore:
        """Builds the Vector Store object."""
        msg = "build_vector_store-metoden måste implementeras."
        raise NotImplementedError(msg)

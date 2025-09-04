from typing import Any

import numpy as np

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import DataInput, DropdownInput, Output
from axiestudio.schema.data import Data


class EmbeddingSimilarityComponent(Component):
    display_name: str = "Inbäddningslikhet"
    description: str = "Beräkna vald form av likhet mellan två inbäddningsvektorer."
    icon = "equal"
    legacy: bool = True

    inputs = [
        DataInput(
            name="embedding_vectors",
            display_name="Inbäddningsvektorer",
            info="En lista som innehåller exakt två dataobjekt med inbäddningsvektorer att jämföra.",
            is_list=True,
            required=True,
        ),
        DropdownInput(
            name="similarity_metric",
            display_name="Likhetsmått",
            info="Välj likhetsmåttet att använda.",
            options=["Cosine Similarity", "Euclidean Distance", "Manhattan Distance"],
            value="Cosine Similarity",
        ),
    ]

    outputs = [
        Output(display_name="Likhetsdata", name="similarity_data", method="compute_similarity"),
    ]

    def compute_similarity(self) -> Data:
        embedding_vectors: list[Data] = self.embedding_vectors

        # Assert that the list contains exactly two Data objects
        if len(embedding_vectors) != 2:  # noqa: PLR2004
            msg = "Exakt två inbäddningsvektorer krävs."
            raise ValueError(msg)

        embedding_1 = np.array(embedding_vectors[0].data["embeddings"])
        embedding_2 = np.array(embedding_vectors[1].data["embeddings"])

        if embedding_1.shape != embedding_2.shape:
            similarity_score: dict[str, Any] = {"error": "Inbäddningar måste ha samma dimensioner."}
        else:
            similarity_metric = self.similarity_metric

            if similarity_metric == "Cosine Similarity":
                score = np.dot(embedding_1, embedding_2) / (np.linalg.norm(embedding_1) * np.linalg.norm(embedding_2))
                similarity_score = {"cosine_similarity": score}

            elif similarity_metric == "Euclidean Distance":
                score = np.linalg.norm(embedding_1 - embedding_2)
                similarity_score = {"euclidean_distance": score}

            elif similarity_metric == "Manhattan Distance":
                score = np.sum(np.abs(embedding_1 - embedding_2))
                similarity_score = {"manhattan_distance": score}

        # Create a Data object to encapsulate the similarity score and additional information
        similarity_data = Data(
            data={
                "embedding_1": embedding_vectors[0].data["embeddings"],
                "embedding_2": embedding_vectors[1].data["embeddings"],
                "similarity_score": similarity_score,
            },
            text_key="similarity_score",
        )

        self.status = similarity_data
        return similarity_data

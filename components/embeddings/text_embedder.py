import logging
from typing import TYPE_CHECKING

from axiestudio.custom.custom_component.component import Component
from axiestudio.io import HandleInput, MessageInput, Output
from axiestudio.schema.data import Data

if TYPE_CHECKING:
    from axiestudio.field_typing import Embeddings
    from axiestudio.schema.message import Message


class TextEmbedderComponent(Component):
    display_name: str = "Text Embedder"
    description: str = "Generera embeddings för ett givet meddelande med den angivna embedding-modellen."
    icon = "binary"
    legacy: bool = True
    inputs = [
        HandleInput(
            name="embedding_model",
            display_name="Embedding-modell",
            info="Embedding-modellen att använda för att generera embeddings.",
            input_types=["Embeddings"],
            required=True,
        ),
        MessageInput(
            name="message",
            display_name="Meddelande",
            info="Meddelandet att generera embeddings för.",
            required=True,
        ),
    ]
    outputs = [
        Output(display_name="Embedding-data", name="embeddings", method="generate_embeddings"),
    ]

    def generate_embeddings(self) -> Data:
        try:
            embedding_model: Embeddings = self.embedding_model
            message: Message = self.message

            # Combine validation checks to reduce nesting
            if not embedding_model or not hasattr(embedding_model, "embed_documents"):
                msg = "Invalid or incompatible embedding model"
                raise ValueError(msg)

            text_content = message.text if message and message.text else ""
            if not text_content:
                msg = "No text content found in message"
                raise ValueError(msg)

            embeddings = embedding_model.embed_documents([text_content])
            if not embeddings or not isinstance(embeddings, list):
                msg = "Invalid embeddings generated"
                raise ValueError(msg)

            embedding_vector = embeddings[0]
            self.status = {"text": text_content, "embeddings": embedding_vector}
            return Data(data={"text": text_content, "embeddings": embedding_vector})
        except Exception as e:
            logging.exception("Error generating embeddings")
            error_data = Data(data={"text": "", "embeddings": [], "error": str(e)})
            self.status = {"error": str(e)}
            return error_data

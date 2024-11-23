from uuid import uuid4

import qdrant_client
from pydantic import BaseModel
from qdrant_client.http import models

from llm_in_cb.config import QDRANT_URL, EMBED_SIZE, COLLECTION_NAME


class Item(BaseModel):
    embeddings: list
    payload: dict


class Database:
    def __init__(self) -> None:
        self.collection_name = COLLECTION_NAME
        self.client = qdrant_client.QdrantClient(
            QDRANT_URL
        )
        if not self.client.collection_exists(
                collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=EMBED_SIZE,
                    distance=models.Distance.COSINE,
                ),
            )

    def insert(self, items: list[Item]):
        vectors = [item.embeddings for item in items]
        payloads = [item.payload for item in items]
        point_ids = [uuid4().hex for _ in range(len(items))]
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=point_ids,
                payloads=payloads,
                vectors=vectors,
            ),
            wait=True,
        )

    def search(self, item: Item):
        embeddings = item.embeddings
        payload = item.payload
        filters = models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(
                        value=payload["category"],
                    ),
                ),

            ],
        )

        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=embeddings,
            query_filter=filters,
            limit=5,
        )
        if len(response) == 0:
            response = self.client.search(
                collection_name=self.collection_name,
                query_vector=embeddings,
                limit=5,
            )

        return [response[i].payload["content"] for i in
                range(len(response))]

    def delete_points(self, data: dict):
        document_id = data["document_id"]
        return self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id),
                        ),
                    ],
                ),
            ),
        )

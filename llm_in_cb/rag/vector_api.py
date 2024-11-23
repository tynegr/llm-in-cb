import uvicorn
from fastapi import FastAPI

from llm_in_cb.config import VECTOR_PORT
from llm_in_cb.rag.vector_database import Database, Item

database = Database()
app = FastAPI()


@app.post("/add", status_code=200)
async def add(data: dict):
    embeddings = data["embeddings"]
    content = data["content"]
    category = data["category"]
    items = [
        Item(
            embeddings=embeddings,
            payload={
                "category": category,
                "content": content,
            },
        )
    ]
    database.insert(items)


@app.post("/search")
async def search(data: dict) -> list:
    embeddings = data["embeddings"]
    category = data["category"]
    item = Item(
        embeddings=embeddings,
        payload={

            "category": category,
        },
    )
    return database.search(item)


if __name__ == "__main__":
    uvicorn.run(app, port=VECTOR_PORT)

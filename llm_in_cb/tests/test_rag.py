import requests

from llm_in_cb.config import VECTOR_PORT, EMBED_PORT

VECTOR_API_URL = f"http://127.0.0.1:{VECTOR_PORT}"

EMBEDDING_API_URL = f"http://127.0.0.1:{EMBED_PORT}"

texts_to_embed = {
    "text": "Hello, this is a test."
}

response = requests.post(f"{EMBEDDING_API_URL}/embed", json=texts_to_embed)

if response.status_code == 200:
    embeddings = response.json()["embeddings"]
    print("Embeddings successfully generated:", len(embeddings))
else:
    print("Failed to generate embeddings:", response.json())

data_to_add = {
    "embeddings": embeddings,
    "content": "Hello, this is a test.",
    "category": "test_category",
}

response_add = requests.post(f"{VECTOR_API_URL}/add", json=data_to_add)

if response_add.status_code == 200:
    print("Data added successfully.")
else:
    print("Failed to add data:", response_add.json())

data_to_search = {
    "embeddings": embeddings,
    "content": "Hello, this is a test.",
    "category": "test_category",
}

response_search = requests.post(f"{VECTOR_API_URL}/search",
                                json=data_to_search)

if response_search.status_code == 200:
    print("Search results:", response_search.json())
else:
    print("Search failed:", response_search.json())

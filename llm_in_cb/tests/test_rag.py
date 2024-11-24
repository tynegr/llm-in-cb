import requests

VECTOR_API_URL = "http://localhost:5555"
EMBEDDING_API_URL = "http://localhost:6666"

texts_to_embed = {
    "text": "Hello, this is a test."
}

print("Generating embeddings...")
response = requests.post(f"{EMBEDDING_API_URL}/embed", json=texts_to_embed)

if response.status_code == 200:
    embeddings = response.json().get("embeddings", [])
    print(f"Embeddings successfully generated: {len(embeddings)}")
else:
    print("Failed to generate embeddings:", response.json())
    exit(1)

data_to_add = {
    "embeddings": embeddings,
    "content": "Hello, this is a test.",
    "category": "test_category",
}

print("Adding data to vector store...")
response_add = requests.post(f"{VECTOR_API_URL}/add", json=data_to_add)

if response_add.status_code == 200:
    print("Data added successfully.")
else:
    print("Failed to add data:", response_add.json())
    exit(1)

data_to_search = {
    "embeddings": embeddings,
    "content": "Hello, this is a test.",
    "category": "test_category",
}

print("Searching for similar data in vector store...")
response_search = requests.post(f"{VECTOR_API_URL}/search", json=data_to_search)

if response_search.status_code == 200:
    search_results = response_search.json()
    print("Search results:", search_results)
else:
    print("Search failed:", response_search.json())
    exit(1)

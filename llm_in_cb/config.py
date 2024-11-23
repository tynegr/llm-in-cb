import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_PORT = int(os.getenv("EMBED_PORT", "6666"))
VECTOR_PORT = int(os.getenv("EMBED_PORT", "5555"))
EMBED_SIZE = int(os.getenv("EMBED_SIZE", "384"))
MODEL_NAME = os.getenv("MODEL_NAME", 'intfloat/multilingual-e5-small')
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "llm_in_cb_test_2")

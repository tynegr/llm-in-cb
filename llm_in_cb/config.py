import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_PORT = int(os.getenv("EMBED_PORT", "6666"))
VECTOR_PORT = int(os.getenv("EMBED_PORT", "5555"))
EMBED_SIZE = int(os.getenv("EMBED_SIZE", "384"))
MODEL_NAME = os.getenv("MODEL_NAME", 'intfloat/multilingual-e5-small')
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "llm_in_cb_test_2")
CONFIG_PATH = os.getenv("CONFIG_PATH", "llm_in_cb/bot/config_api.json")
VECTOR_DB_API_URL = os.getenv("VECTOR_DB_API_URL", "http://localhost:5555")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "http://localhost:6666")
LLM_API_URL = os.getenv("LLM_API_URL", "http://llama_cpp:1349/completion")
LLM_API_URL_NEW = os.getenv("LLM_API_URL_NEW", "http://llama_cpp_new:1348/completion")
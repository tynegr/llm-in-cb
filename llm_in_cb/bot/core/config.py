import os
import json

CONFIG_PATH = "llm_in_cb/bot/config_api.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()
TGBOT_API = config["telegram_bot"]["token"]
# URLs сервисов из переменных окружения
LLM_API_URL = os.getenv("LLM_API_URL", "http://ollama:11434/v1/completions")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "http://embedding_api:6666")
VECTOR_DB_API_URL = os.getenv("VECTOR_DB_API_URL", "http://vector_api:5555")

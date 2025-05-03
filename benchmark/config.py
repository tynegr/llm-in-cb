import os

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral-large-latest")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

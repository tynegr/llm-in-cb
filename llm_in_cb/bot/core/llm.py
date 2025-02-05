import requests

from llm_in_cb.bot.core.config import LLM_API_URL, EMBEDDING_API_URL, VECTOR_DB_API_URL


def query_llm(prompt, model):
    try:
        data = {"model": model, "prompt": prompt, "max_tokens": 200}
        headers = {"Content-Type": "application/json"}
        response = requests.post(LLM_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("text", "Ошибка: пустой ответ").strip()
    except requests.RequestException as e:
        return f"Ошибка запроса к LLM: {str(e)}"

def get_embeddings(text):
    try:
        response = requests.post(f"{EMBEDDING_API_URL}/embed", json={"text": text})
        response.raise_for_status()
        embeddings = response.json().get("embeddings")
        if not embeddings:
            raise ValueError("Пустой ответ от сервиса эмбеддингов")
        return embeddings
    except requests.RequestException as e:
        return {"error": f"Ошибка получения эмбеддингов: {str(e)}"}
    except ValueError as e:
        return {"error": f"Ошибка обработки эмбеддингов: {str(e)}"}

def search_vector_database(embeddings, category):
    try:
        response = requests.post(
            f"{VECTOR_DB_API_URL}/search", json={"embeddings": embeddings, "category": category}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Ошибка поиска в базе: {str(e)}"}

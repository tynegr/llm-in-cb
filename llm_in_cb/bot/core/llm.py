import requests

from llm_in_cb.bot.core.config import LLM_API_URL, EMBEDDING_API_URL, VECTOR_DB_API_URL


def query_llm(prompt, model):
    print(f"[LLM] Вызов query_llm с prompt:\n{prompt}\nи model: {model}", flush=True)
    try:
        data = {"model": model, "prompt": prompt, "max_tokens": 200, "stream": False}
        print(f"[LLM] Payload запроса: {data}", flush=True)
        headers = {"Content-Type": "application/json"}
        print(f"[LLM] URL: {LLM_API_URL}", flush=True)

        response = requests.post(LLM_API_URL, headers=headers, json=data)
        print(f"[LLM] Status code: {response.status_code}", flush=True)
        print(f"[LLM] Raw response text: {response.text}", flush=True)

        response.raise_for_status()
        response_json = response.json()
        print(f"[LLM] JSON-ответ: {response_json}", flush=True)

        result = response_json.get("response", "Ошибка: пустой ответ")
        print(f"[LLM] Итоговый ответ: {result}", flush=True)
        return result.strip()
    except requests.RequestException as e:
        print(f"[LLM] Ошибка запроса к LLM: {str(e)}", flush=True)
        return f"Ошибка запроса к LLM: {str(e)}"
    except Exception as e:
        print(f"[LLM] Общая ошибка в query_llm: {str(e)}", flush=True)
        return f"Ошибка в query_llm: {str(e)}"



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

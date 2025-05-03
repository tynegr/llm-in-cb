from config import TAVILY_API_KEY
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str) -> str:
    search_response = tavily_client.search(query)
    return "\n".join([site.get("title") + '\n\n' + site.get("content") for site in search_response.get("results")])


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Поиск в интеренете",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Твой запрос в интернет",
                    }
                },
                "required": ["query"],
            },
        },
    },
]

names_to_functions = {
    'search_web': search_web
}

import json
from loguru import logger
from config import LLM_API_KEY, MODEL_NAME
from tools import TOOLS, names_to_functions
from mistralai import Mistral

client = Mistral(api_key=LLM_API_KEY)


def ask_question(question):
    messages = [{"role": "user", "content": question}]
    try:
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="any",
            max_tokens=1000,
            temperature=0.05,
        )
        return messages, response
    except Exception as e:
        logger.error(f"Error: {e}")
        return messages, None


def handle_tool_call(messages, response):
    if not response or not response.choices:
        logger.warning("LLM is not responding")
        return None

    choice = response.choices[0].message
    messages.append(choice)

    if not choice.tool_calls:
        logger.info("No tool calls somehow ...")
        return choice.content

    tool_call = choice.tool_calls[0]
    function_name = tool_call.function.name
    try:
        function_params = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError as e:
        logger.error(f"Error: {e}")
        return None

    if function_name not in names_to_functions:
        logger.error(f"Unexpected function: {function_name}")
        return None

    try:
        function_result = names_to_functions[function_name](**function_params)
    except Exception as e:
        logger.error(f"Error in  '{function_name}': {e}")
        function_result = str(e)

    messages.append({
        "role": "tool",
        "name": function_name,
        "content": function_result,
        "tool_call_id": tool_call.id,
    })

    return get_final_response(messages)


def get_final_response(messages):
    try:
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=1000,
            temperature=0.05,
        )
        return response.choices[0].message.content[0].text
    except Exception as e:
        logger.error(f"Error: {e}")
        return None


def main():
    question = input()
    messages, initial_response = ask_question(question)
    final_answer = handle_tool_call(messages, initial_response)
    if final_answer:
        print(final_answer)
    else:
        print("Error")


if __name__ == "__main__":
    main()

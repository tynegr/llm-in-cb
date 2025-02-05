from mistralai import Mistral

MAIN_SYSTEM_PROMPT= """Используя характеристики товара, которые я предоставлю тебе ниже,
напиши
красивое
описание
товара
для
интернет
магазина.
ОБЯЗАТЕЛЬНО
НА
РУССКОМ
ЯЗЫКЕ!"""



MAIN_CONTEXT_PROMPT= """Характеристики:

\"\"\"
{text}
\"\"\"
"""

client = Mistral(api_key="kGKt4ZgoNAS0U1Nw2FOeZii5Qy4GlGRB")


async def make_llm_request(text):
    llm_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": MAIN_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": MAIN_CONTEXT_PROMPT.format(text=text),
            },
        ],
    )
    return llm_response.choices[0].message.content



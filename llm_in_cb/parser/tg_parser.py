import snscrape.modules.telegram as sntelegram
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import requests
from llm_in_cb.config import VECTOR_DB_API_URL, EMBEDDING_API_URL

posts_per_channel = 5000 # выбрать нужное колеичество постов для формирвоания контекстов

with open("llm_in_cb/parser/tg_channels.txt", "r") as file:
    lines = file.readlines()

channels = [line.strip() for line in lines]

all_posts = ''

for channel in channels:
    for i, mydata in enumerate(sntelegram.TelegramChannelScraper(f'{channel}').get_items()):
        if i > posts_per_channel:
            break
        if mydata.content:
            all_posts += mydata.content.strip() + " \n "

text_splitter = RecursiveCharacterTextSplitter()

chunks = text_splitter.create_documents([all_posts])

with open("llm_in_cb/parser/combined_chunks.json", "w", encoding="utf-8") as json_file:
    json.dump([{'text': chunk.page_content} for chunk in chunks], json_file, ensure_ascii=False, indent=4)


with open("llm_in_cb/parser/combined_chunks.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

for key, text in data.items():
    response = requests.post(f"{EMBEDDING_API_URL}/embed", json=data[key])

    if response.status_code == 200:
        embeddings = response.json().get("embeddings", [])
    else:
        print("Failed to generate embeddings:", response.json())
        exit(1)

    data[key] = {
        "embeddings": embeddings,
        "content": text,
        "category": "context_5000_posts_per_channel",
    }

    print("Adding data to vector store...")
    response_add = requests.post(f"{VECTOR_DB_API_URL}/add", json=data[key])

    if response_add.status_code != 200:
        print("Failed to add data:", response_add.json())
        exit(1)
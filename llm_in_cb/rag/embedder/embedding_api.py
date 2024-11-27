import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModel

from llm_in_cb.config import EMBED_PORT
from llm_in_cb.models import EmbeddingResponse, TextRequest

app = FastAPI(title="Multilingual-E5-small API",
              description="API to serve Multilingual-E5-small model for text embeddings")

MODEL_NAME = "intfloat/multilingual-e5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)


@app.post("/embed", response_model=EmbeddingResponse)
async def get_embedding(request: TextRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True,
                           padding=True)

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].squeeze().tolist()

        return EmbeddingResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, port=EMBED_PORT)

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


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
    return sum_embeddings / sum_mask

def get_embeddings(texts: list[str]) -> list[list[float]]:
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = mean_pooling(outputs, inputs['attention_mask'])
    return embeddings.tolist()




@app.post("/embed", response_model=EmbeddingResponse)
async def generate_embeddings(request: TextRequest):
    texts = request.texts
    if not texts:
        raise HTTPException(status_code=400,
                            detail="Input texts cannot be empty.")
    try:
        embeddings = get_embeddings(texts)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, port=EMBED_PORT)

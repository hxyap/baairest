import os
from sentence_transformers import SentenceTransformer
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    embedding: list

keyword_encoder = None

@app.on_event("startup")
async def load_model():
    global keyword_encoder
    model_name = os.getenv("MODEL_NAME", "BAAI/bge-base-en-v1.5")
    keyword_encoder = SentenceTransformer(model_name)

def encode(query: str) -> list:
    try:
        text_emb = keyword_encoder.encode(query, normalize_embeddings=True)
        return text_emb.ravel().tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during encoding: {str(e)}")

@app.post("/get-text-embeddings", response_model=Response)
async def predict_api(request: Request) -> Response:
    embedding = encode(request.question)
    return Response(embedding=embedding)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

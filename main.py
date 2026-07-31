from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="GuardRAG")

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(q: Query):
    return run_agent(q.question)

@app.get("/")
def health():
    return {"status": "GuardRAG is running"}

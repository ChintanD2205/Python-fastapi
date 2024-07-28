from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import RAG, Classification

app = FastAPI()

rag_model = RAG()
classification_model = Classification("data/dataset.csv")

class QueryRequest(BaseModel):
    query: str

@app.post("/rag")
async def rag_endpoint(query_request: QueryRequest):
    try:
        user_query = query_request.query
        response = await rag_model.process_user_query(user_query)  
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/classification")
async def classification_endpoint(query_request: QueryRequest):
    try:
        text = query_request.query
        response = await classification_model.classify_text(text) 
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

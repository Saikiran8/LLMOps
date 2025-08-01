from fastapi import FastAPI, Request
from mcp import MCPRequest, inject_mcp
from rag_engine import RAGEngine
from kafka_producer import send_mcp_event

app = FastAPI()
rag = RAGEngine()

@app.middleware("http")
async def inject_mcp_middleware(request: Request, call_next):
    request.state.mcp = inject_mcp(request)
    response = await call_next(request)
    return response

@app.post("/query")
async def query_route(mcp: MCPRequest, request: Request):
    answer, trace = rag.answer(mcp.query, mcp.metadata)
    response = {
        "request_id": mcp.request_id,
        "answer": answer,
        "model_trace": trace
    }
    send_mcp_event(mcp, trace)
    return response

from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

class MCPMetadata(BaseModel):
    retriever: str = "chroma"
    model_version: str = "gpt-4"
    prompt_id: str = "default"
    doc_ids: list[str] = []

class MCPRequest(BaseModel):
    request_id: str
    user_id: str
    timestamp: str
    query: str
    conversation_id: str
    metadata: MCPMetadata

def inject_mcp(request) -> MCPRequest:
    return MCPRequest(
        request_id=str(uuid4()),
        user_id="anonymous",
        timestamp=datetime.utcnow().isoformat(),
        query=request.query_params.get("query", ""),
        conversation_id="conv-000",
        metadata=MCPMetadata()
    )

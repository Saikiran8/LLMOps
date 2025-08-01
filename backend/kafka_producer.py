from kafka import KafkaProducer
import json
from mcp import MCPRequest

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_mcp_event(mcp: MCPRequest, trace: dict):
    message = {
        "request_id": mcp.request_id,
        "timestamp": mcp.timestamp,
        "user_id": mcp.user_id,
        "query": mcp.query,
        "metadata": mcp.metadata.dict(),
        "trace": trace
    }
    producer.send("query-events", message)

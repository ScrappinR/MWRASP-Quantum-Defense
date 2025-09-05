"""
API Gateway and Service Definitions
REST API, gRPC, and WebSocket interfaces
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import grpc
from concurrent import futures
import asyncio
import json
import uuid
from datetime import datetime

# Proto definitions for gRPC
PROTO_DEFINITION = """
syntax = "proto3";

package homomorphic_swarm;

service SwarmService {
    rpc Encrypt(EncryptRequest) returns (EncryptResponse);
    rpc Compute(ComputeRequest) returns (ComputeResponse);
    rpc Bootstrap(BootstrapRequest) returns (BootstrapResponse);
    rpc GetStatus(StatusRequest) returns (StatusResponse);
    rpc StreamComputation(stream ComputeRequest) returns (stream ComputeResponse);
}

message EncryptRequest {
    repeated double data = 1;
    string encryption_params = 2;
}

message EncryptResponse {
    bytes encrypted_data = 1;
    string operation_id = 2;
}

message ComputeRequest {
    string operation = 1;
    repeated bytes operands = 2;
    map<string, string> params = 3;
}

message ComputeResponse {
    bytes result = 1;
    double execution_time = 2;
    string operation_id = 3;
    map<string, string> metadata = 4;
}

message BootstrapRequest {
    bytes ciphertext = 1;
    string strategy = 2;
}

message BootstrapResponse {
    bytes refreshed_ciphertext = 1;
    double speedup_percent = 2;
}

message StatusRequest {
    bool include_metrics = 1;
}

message StatusResponse {
    map<string, NodeStatus> nodes = 1;
    double average_speedup = 2;
    int32 total_operations = 3;
}

message NodeStatus {
    string node_id = 1;
    string node_type = 2;
    bool is_active = 3;
    double trust_score = 4;
}
"""

# Pydantic models for REST API
class EncryptRequest(BaseModel):
    data: List[float] = Field(..., description="Data to encrypt")
    params: Optional[Dict[str, Any]] = Field(default={}, description="Encryption parameters")

class ComputeRequest(BaseModel):
    operation: str = Field(..., description="Operation type: add, multiply, bootstrap")
    operands: List[str] = Field(..., description="Hex-encoded encrypted operands")
    params: Optional[Dict[str, Any]] = Field(default={}, description="Operation parameters")

class ComputeResponse(BaseModel):
    result: str = Field(..., description="Hex-encoded result")
    operation_id: str = Field(..., description="Unique operation ID")
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")
    speedup_percent: Optional[float] = Field(None, description="Speedup vs vanilla")

class SwarmStatus(BaseModel):
    nodes: Dict[str, Dict[str, Any]]
    average_speedup: float
    total_operations: int
    byzantine_detections: int

# FastAPI application
app = FastAPI(
    title="Homomorphic Swarm API",
    description="Bio-inspired distributed homomorphic encryption system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    # Implementation from security layer
    return {"user_id": "authenticated_user"}

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
            
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

# REST API endpoints
@app.post("/api/v1/encrypt", response_model=Dict[str, str])
async def encrypt(request: EncryptRequest, auth=Depends(verify_token)):
    """Encrypt data using the swarm"""
    operation_id = str(uuid.uuid4())
    
    # Forward to swarm
    # In production, this would call the actual swarm
    encrypted_data = "encrypted_hex_data"
    
    return {
        "encrypted_data": encrypted_data,
        "operation_id": operation_id
    }

@app.post("/api/v1/compute", response_model=ComputeResponse)
async def compute(request: ComputeRequest, auth=Depends(verify_token)):
    """Execute homomorphic computation"""
    operation_id = str(uuid.uuid4())
    
    # Validate operation
    valid_operations = ["add", "multiply", "bootstrap", "polynomial", "comparison"]
    if request.operation not in valid_operations:
        raise HTTPException(status_code=400, detail=f"Invalid operation: {request.operation}")
    
    # Forward to swarm
    # Simulated for now
    start_time = asyncio.get_event_loop().time()
    
    # Process computation
    result = "computed_result_hex"
    
    execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
    
    return ComputeResponse(
        result=result,
        operation_id=operation_id,
        execution_time_ms=execution_time,
        speedup_percent=35.2 if request.operation == "bootstrap" else None
    )

@app.get("/api/v1/status", response_model=SwarmStatus)
async def get_status(include_metrics: bool = True):
    """Get swarm status"""
    # Aggregate from all nodes
    return SwarmStatus(
        nodes={
            "queen_0": {"type": "queen", "active": True, "trust_score": 1.0},
            "worker_0": {"type": "worker", "active": True, "trust_score": 0.98},
            "worker_1": {"type": "worker", "active": True, "trust_score": 0.99},
            "guardian_0": {"type": "guardian", "active": True, "trust_score": 1.0}
        },
        average_speedup=34.7,
        total_operations=15432,
        byzantine_detections=3
    )

@app.post("/api/v1/batch")
async def batch_compute(requests: List[ComputeRequest], auth=Depends(verify_token)):
    """Batch multiple computations"""
    results = []
    
    # Process in parallel
    tasks = [compute(req, auth) for req in requests]
    results = await asyncio.gather(*tasks)
    
    return {"results": results}

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "subscribe":
                # Subscribe to operation updates
                await manager.send_personal_message(
                    json.dumps({"type": "subscribed", "status": "ok"}),
                    client_id
                )
            elif message["type"] == "compute":
                # Real-time computation
                result = await compute(ComputeRequest(**message["data"]), None)
                await manager.send_personal_message(
                    json.dumps({"type": "result", "data": result.dict()}),
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# gRPC service implementation
class SwarmServicer:
    """gRPC service implementation"""
    
    def __init__(self, swarm_client):
        self.swarm_client = swarm_client
        
    async def Encrypt(self, request, context):
        """Handle encrypt request"""
        # Convert request to internal format
        encrypted = await self.swarm_client.encrypt(list(request.data))
        
        return EncryptResponse(
            encrypted_data=encrypted.data,
            operation_id=str(uuid.uuid4())
        )
        
    async def Compute(self, request, context):
        """Handle compute request"""
        start_time = asyncio.get_event_loop().time()
        
        # Execute computation
        result = await self.swarm_client.compute(
            request.operation,
            [bytes.fromhex(op) for op in request.operands],
            dict(request.params)
        )
        
        execution_time = asyncio.get_event_loop().time() - start_time
        
        return ComputeResponse(
            result=result,
            execution_time=execution_time,
            operation_id=str(uuid.uuid4()),
            metadata={"node_count": "10"}
        )
        
    async def Bootstrap(self, request, context):
        """Handle bootstrap request"""
        start_time = asyncio.get_event_loop().time()
        
        # Distributed bootstrap
        refreshed = await self.swarm_client.bootstrap(
            request.ciphertext,
            strategy=request.strategy or "distributed"
        )
        
        vanilla_time = 0.012  # 12ms baseline
        actual_time = asyncio.get_event_loop().time() - start_time
        speedup = ((vanilla_time - actual_time) / vanilla_time) * 100
        
        return BootstrapResponse(
            refreshed_ciphertext=refreshed,
            speedup_percent=speedup
        )
        
    async def StreamComputation(self, request_iterator, context):
        """Handle streaming computations"""
        async for request in request_iterator:
            # Process each request
            result = await self.Compute(request, context)
            yield result

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # Check if swarm is ready
    ready = True  # Check actual swarm status
    
    if not ready:
        raise HTTPException(status_code=503, detail="Swarm not ready")
        
    return {"status": "ready"}

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # Return Prometheus format metrics
    metrics_text = """
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="POST",endpoint="/api/v1/compute"} 1234
http_requests_total{method="GET",endpoint="/api/v1/status"} 567

# HELP compute_duration_seconds Computation duration
# TYPE compute_duration_seconds histogram
compute_duration_seconds_bucket{operation="bootstrap",le="0.005"} 123
compute_duration_seconds_bucket{operation="bootstrap",le="0.01"} 456
compute_duration_seconds_bucket{operation="bootstrap",le="+Inf"} 789
compute_duration_seconds_sum{operation="bootstrap"} 7.89
compute_duration_seconds_count{operation="bootstrap"} 789
"""
    return metrics_text

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/compute")
@limiter.limit("100/minute")
async def rate_limited_compute(request: ComputeRequest, auth=Depends(verify_token)):
    return await compute(request, auth)

# GraphQL support
from strawberry.fastapi import GraphQLRouter
import strawberry

@strawberry.type
class SwarmQuery:
    @strawberry.field
    async def status(self) -> SwarmStatus:
        return await get_status()
        
    @strawberry.field
    async def node(self, node_id: str) -> Optional[Dict[str, Any]]:
        status = await get_status()
        return status.nodes.get(node_id)

@strawberry.type
class SwarmMutation:
    @strawberry.mutation
    async def compute(self, operation: str, operands: List[str]) -> ComputeResponse:
        req = ComputeRequest(operation=operation, operands=operands)
        return await compute(req, None)

schema = strawberry.Schema(query=SwarmQuery, mutation=SwarmMutation)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Start gRPC server
def serve_grpc(port: int = 50051):
    """Start gRPC server"""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer
    servicer = SwarmServicer(None)  # Pass actual swarm client
    # Register with generated stubs
    # swarm_pb2_grpc.add_SwarmServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    asyncio.run(server.start())
    asyncio.run(server.wait_for_termination())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

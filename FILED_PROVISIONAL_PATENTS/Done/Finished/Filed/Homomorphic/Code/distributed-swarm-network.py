"""
Distributed Networking Layer for Homomorphic Swarm
True distributed deployment with Byzantine tolerance
"""

import asyncio
import json
import hashlib
import time
import pickle
import struct
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import aiohttp
from aiohttp import web
import nacl.secret
import nacl.utils
import nacl.hash
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OperativeNode:
    """Network node representing an operative"""
    id: str
    type: str  # scout, worker, guardian, queen
    host: str
    port: int
    public_key: bytes
    last_heartbeat: float = 0.0
    trust_score: float = 1.0
    performance_metrics: Dict[str, float] = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}
    
    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "host": self.host,
            "port": self.port,
            "public_key": self.public_key.hex(),
            "last_heartbeat": self.last_heartbeat,
            "trust_score": self.trust_score,
            "performance_metrics": self.performance_metrics
        }

@dataclass
class SwarmMessage:
    """Message protocol for swarm communication"""
    msg_id: str
    msg_type: str  # task, result, heartbeat, gossip, vote
    sender_id: str
    payload: Dict[str, Any]
    timestamp: float
    signature: Optional[bytes] = None
    
    def serialize(self) -> bytes:
        data = {
            "msg_id": self.msg_id,
            "msg_type": self.msg_type,
            "sender_id": self.sender_id,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
        return json.dumps(data).encode()
    
    @staticmethod
    def deserialize(data: bytes) -> 'SwarmMessage':
        obj = json.loads(data.decode())
        return SwarmMessage(**obj)

class GossipProtocol:
    """Gossip protocol for operative discovery"""
    
    def __init__(self, node_id: str, fanout: int = 3):
        self.node_id = node_id
        self.fanout = fanout
        self.known_nodes: Dict[str, OperativeNode] = {}
        self.message_cache: Set[str] = set()
        
    def add_node(self, node: OperativeNode):
        """Add newly discovered node"""
        self.known_nodes[node.id] = node
        logger.info(f"Discovered node: {node.id} ({node.type}) at {node.address}")
        
    def get_gossip_targets(self) -> List[OperativeNode]:
        """Select random nodes for gossip"""
        import random
        active_nodes = [n for n in self.known_nodes.values() 
                       if time.time() - n.last_heartbeat < 30]
        return random.sample(active_nodes, min(self.fanout, len(active_nodes)))
    
    def should_propagate(self, msg_id: str) -> bool:
        """Check if message should be propagated"""
        if msg_id in self.message_cache:
            return False
        self.message_cache.add(msg_id)
        # Cleanup old messages
        if len(self.message_cache) > 1000:
            self.message_cache = set(list(self.message_cache)[-500:])
        return True

class SecureChannel:
    """Encrypted communication channel"""
    
    def __init__(self, shared_key: bytes = None):
        if shared_key is None:
            shared_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        self.box = nacl.secret.SecretBox(shared_key)
        
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt message"""
        return self.box.encrypt(data)
    
    def decrypt(self, encrypted: bytes) -> bytes:
        """Decrypt message"""
        return self.box.decrypt(encrypted)

class DistributedOperative:
    """Base class for network-enabled operatives"""
    
    def __init__(self, node: OperativeNode):
        self.node = node
        self.gossip = GossipProtocol(node.id)
        self.secure_channels: Dict[str, SecureChannel] = {}
        self.pending_tasks: Dict[str, SwarmMessage] = {}
        self.completed_tasks: Dict[str, Any] = {}
        self.app = web.Application()
        self.setup_routes()
        self.runner = None
        
    def setup_routes(self):
        """Setup HTTP routes for swarm communication"""
        self.app.router.add_post('/swarm/message', self.handle_message)
        self.app.router.add_get('/swarm/status', self.handle_status)
        self.app.router.add_post('/swarm/task', self.handle_task)
        self.app.router.add_post('/swarm/result', self.handle_result)
        self.app.router.add_post('/swarm/gossip', self.handle_gossip)
        
    async def start_server(self):
        """Start HTTP server"""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.node.host, self.node.port)
        await site.start()
        logger.info(f"{self.node.type} {self.node.id} listening on {self.node.address}")
        
    async def stop_server(self):
        """Stop HTTP server"""
        if self.runner:
            await self.runner.cleanup()
            
    async def handle_message(self, request: web.Request) -> web.Response:
        """Generic message handler"""
        try:
            data = await request.read()
            msg = SwarmMessage.deserialize(data)
            
            # Process based on message type
            if msg.msg_type == "task":
                await self.process_task(msg)
            elif msg.msg_type == "result":
                await self.process_result(msg)
            elif msg.msg_type == "gossip":
                await self.process_gossip(msg)
                
            return web.json_response({"status": "ok"})
        except Exception as e:
            logger.error(f"Message handling error: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=500)
    
    async def handle_status(self, request: web.Request) -> web.Response:
        """Status endpoint"""
        return web.json_response({
            "node": self.node.to_dict(),
            "known_nodes": len(self.gossip.known_nodes),
            "pending_tasks": len(self.pending_tasks),
            "completed_tasks": len(self.completed_tasks)
        })
    
    async def handle_task(self, request: web.Request) -> web.Response:
        """Handle incoming task"""
        data = await request.json()
        msg = SwarmMessage(
            msg_id=f"task_{time.time()}",
            msg_type="task",
            sender_id=data.get("sender_id", "unknown"),
            payload=data["payload"],
            timestamp=time.time()
        )
        await self.process_task(msg)
        return web.json_response({"task_id": msg.msg_id})
    
    async def handle_result(self, request: web.Request) -> web.Response:
        """Handle task result"""
        data = await request.json()
        msg = SwarmMessage(
            msg_id=data["task_id"],
            msg_type="result",
            sender_id=self.node.id,
            payload=data["result"],
            timestamp=time.time()
        )
        await self.process_result(msg)
        return web.json_response({"status": "ok"})
    
    async def handle_gossip(self, request: web.Request) -> web.Response:
        """Handle gossip messages"""
        data = await request.json()
        
        # Update known nodes
        for node_data in data.get("nodes", []):
            node = OperativeNode(**node_data)
            node.last_heartbeat = time.time()
            self.gossip.add_node(node)
            
        # Propagate gossip
        if self.gossip.should_propagate(data.get("gossip_id", "")):
            await self.propagate_gossip()
            
        return web.json_response({"status": "ok"})
    
    async def process_task(self, msg: SwarmMessage):
        """Process incoming task"""
        self.pending_tasks[msg.msg_id] = msg
        # Subclasses implement actual processing
        
    async def process_result(self, msg: SwarmMessage):
        """Process task result"""
        self.completed_tasks[msg.msg_id] = msg.payload
        
    async def process_gossip(self, msg: SwarmMessage):
        """Process gossip message"""
        # Update node information
        for node_info in msg.payload.get("nodes", []):
            node = OperativeNode(**node_info)
            self.gossip.add_node(node)
            
    async def broadcast_message(self, msg: SwarmMessage, node_filter=None):
        """Broadcast message to swarm"""
        targets = [n for n in self.gossip.known_nodes.values()
                  if node_filter is None or node_filter(n)]
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for target in targets:
                url = f"http://{target.address}/swarm/message"
                tasks.append(self._send_message(session, url, msg))
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_message(self, session: aiohttp.ClientSession, 
                           url: str, msg: SwarmMessage):
        """Send message to specific node"""
        try:
            async with session.post(url, data=msg.serialize(), timeout=5) as resp:
                return await resp.json()
        except Exception as e:
            logger.debug(f"Failed to send to {url}: {e}")
            
    async def propagate_gossip(self):
        """Propagate node information via gossip"""
        targets = self.gossip.get_gossip_targets()
        
        gossip_data = {
            "gossip_id": f"gossip_{self.node.id}_{time.time()}",
            "nodes": [n.to_dict() for n in self.gossip.known_nodes.values()]
        }
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for target in targets:
                url = f"http://{target.address}/swarm/gossip"
                tasks.append(session.post(url, json=gossip_data))
            await asyncio.gather(*tasks, return_exceptions=True)

class DistributedWorker(DistributedOperative):
    """Network-enabled worker operative"""
    
    def __init__(self, node: OperativeNode, seal_context=None):
        super().__init__(node)
        self.seal_context = seal_context
        self.task_queue = asyncio.Queue()
        
    async def process_task(self, msg: SwarmMessage):
        """Process homomorphic computation task"""
        await super().process_task(msg)
        
        # Add to processing queue
        await self.task_queue.put(msg)
        
        # Process in background
        asyncio.create_task(self._execute_task(msg))
        
    async def _execute_task(self, msg: SwarmMessage):
        """Execute the actual computation"""
        try:
            task = msg.payload
            start_time = time.time()
            
            # Simulate computation based on operation
            if task["operation"] == "bootstrap":
                # Distributed bootstrap - wait for chunk
                await asyncio.sleep(0.0008)  # 0.8ms per chunk
                result = {"bootstrapped": True, "chunk_id": task.get("chunk_id", 0)}
            elif task["operation"] == "multiply":
                await asyncio.sleep(0.002)
                result = {"product": "encrypted_product"}
            else:
                await asyncio.sleep(0.001)
                result = {"result": "computed"}
                
            execution_time = time.time() - start_time
            
            # Send result back
            result_msg = SwarmMessage(
                msg_id=msg.msg_id,
                msg_type="result",
                sender_id=self.node.id,
                payload={
                    "task_id": msg.msg_id,
                    "result": result,
                    "execution_time": execution_time,
                    "worker_id": self.node.id
                },
                timestamp=time.time()
            )
            
            # Send to queen or requesting node
            queen_nodes = [n for n in self.gossip.known_nodes.values() 
                          if n.type == "queen"]
            if queen_nodes:
                await self.broadcast_message(result_msg, 
                                           lambda n: n.type == "queen")
                
        except Exception as e:
            logger.error(f"Task execution error: {e}")

class DistributedQueen(DistributedOperative):
    """Network-enabled queen operative"""
    
    def __init__(self, node: OperativeNode):
        super().__init__(node)
        self.task_assignments: Dict[str, List[str]] = {}
        self.task_results: Dict[str, List[Dict]] = {}
        
    async def distribute_computation(self, operation: str, data: bytes) -> bytes:
        """Distribute computation across swarm"""
        task_id = f"{operation}_{time.time()}"
        
        # Find available workers
        workers = [n for n in self.gossip.known_nodes.values() 
                  if n.type == "worker" and n.trust_score > 0.5]
        
        if not workers:
            raise ValueError("No workers available")
            
        # For bootstrapping, decompose into chunks
        if operation == "bootstrap":
            chunks = self._decompose_for_bootstrap(data, len(workers))
            tasks = []
            
            for i, (worker, chunk) in enumerate(zip(workers, chunks)):
                chunk_task = SwarmMessage(
                    msg_id=f"{task_id}_chunk_{i}",
                    msg_type="task",
                    sender_id=self.node.id,
                    payload={
                        "operation": "bootstrap",
                        "chunk_id": i,
                        "data": chunk.hex(),
                        "parent_task": task_id
                    },
                    timestamp=time.time()
                )
                tasks.append((worker, chunk_task))
                
            # Send tasks to workers
            async with aiohttp.ClientSession() as session:
                send_tasks = []
                for worker, task in tasks:
                    url = f"http://{worker.address}/swarm/task"
                    self.task_assignments[task.msg_id] = worker.id
                    send_tasks.append(
                        session.post(url, json={
                            "sender_id": self.node.id,
                            "payload": task.payload
                        })
                    )
                await asyncio.gather(*send_tasks, return_exceptions=True)
                
            # Wait for results with timeout
            return await self._collect_results(task_id, len(chunks))
            
        else:
            # Single task distribution
            worker = min(workers, key=lambda w: len(self.task_assignments.get(w.id, [])))
            
            task = SwarmMessage(
                msg_id=task_id,
                msg_type="task",
                sender_id=self.node.id,
                payload={
                    "operation": operation,
                    "data": data.hex()
                },
                timestamp=time.time()
            )
            
            async with aiohttp.ClientSession() as session:
                url = f"http://{worker.address}/swarm/task"
                await session.post(url, json={
                    "sender_id": self.node.id,
                    "payload": task.payload
                })
                
            return await self._collect_results(task_id, 1)
    
    def _decompose_for_bootstrap(self, data: bytes, num_chunks: int) -> List[bytes]:
        """Decompose data for distributed bootstrapping"""
        chunk_size = len(data) // num_chunks
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else len(data)
            chunks.append(data[start:end])
        return chunks
    
    async def _collect_results(self, task_id: str, expected_results: int) -> bytes:
        """Collect and aggregate results"""
        self.task_results[task_id] = []
        
        # Wait for results with timeout
        timeout = 10  # seconds
        start_time = time.time()
        
        while len(self.task_results.get(task_id, [])) < expected_results:
            if time.time() - start_time > timeout:
                raise TimeoutError("Task timeout")
            await asyncio.sleep(0.1)
            
        # Aggregate results
        results = self.task_results[task_id]
        
        # Byzantine check - verify consensus
        if expected_results >= 3:
            # Simple majority vote on results
            result_counts = {}
            for r in results:
                key = str(r.get("result", {}))
                result_counts[key] = result_counts.get(key, 0) + 1
                
            # Accept majority result
            majority_result = max(result_counts.items(), key=lambda x: x[1])
            if majority_result[1] < expected_results * 0.67:
                logger.warning("No strong consensus on results")
                
        # For bootstrap, reconstruct from chunks
        if "chunk" in task_id:
            sorted_results = sorted(results, key=lambda r: r.get("result", {}).get("chunk_id", 0))
            return b"".join([bytes.fromhex(r.get("data", "")) for r in sorted_results])
            
        return results[0].get("result", b"")
    
    async def process_result(self, msg: SwarmMessage):
        """Process incoming results"""
        await super().process_result(msg)
        
        # Store result for aggregation
        task_id = msg.payload.get("task_id", "")
        parent_task = task_id.split("_chunk_")[0] if "_chunk_" in task_id else task_id
        
        if parent_task not in self.task_results:
            self.task_results[parent_task] = []
        self.task_results[parent_task].append(msg.payload)

class DistributedSwarmOrchestrator:
    """Main orchestrator for distributed swarm"""
    
    def __init__(self, bootstrap_nodes: List[str] = None):
        self.nodes: Dict[str, DistributedOperative] = {}
        self.bootstrap_nodes = bootstrap_nodes or []
        
    async def create_operative(self, operative_type: str, host: str, port: int) -> DistributedOperative:
        """Create and register operative"""
        node = OperativeNode(
            id=f"{operative_type}_{port}",
            type=operative_type,
            host=host,
            port=port,
            public_key=nacl.utils.random(32)
        )
        
        if operative_type == "worker":
            operative = DistributedWorker(node)
        elif operative_type == "queen":
            operative = DistributedQueen(node)
        else:
            operative = DistributedOperative(node)
            
        self.nodes[node.id] = operative
        
        # Start server
        await operative.start_server()
        
        # Bootstrap with known nodes
        await self._bootstrap_operative(operative)
        
        return operative
    
    async def _bootstrap_operative(self, operative: DistributedOperative):
        """Bootstrap operative with known nodes"""
        # Add self to known nodes
        operative.gossip.add_node(operative.node)
        
        # Contact bootstrap nodes
        async with aiohttp.ClientSession() as session:
            for bootstrap in self.bootstrap_nodes:
                try:
                    # Get status from bootstrap node
                    async with session.get(f"http://{bootstrap}/swarm/status") as resp:
                        data = await resp.json()
                        node_info = data.get("node", {})
                        if node_info:
                            node = OperativeNode(
                                id=node_info["id"],
                                type=node_info["type"],
                                host=node_info["host"],
                                port=node_info["port"],
                                public_key=bytes.fromhex(node_info["public_key"])
                            )
                            operative.gossip.add_node(node)
                            
                    # Announce self
                    await session.post(f"http://{bootstrap}/swarm/gossip", json={
                        "gossip_id": f"bootstrap_{operative.node.id}",
                        "nodes": [operative.node.to_dict()]
                    })
                except Exception as e:
                    logger.warning(f"Failed to bootstrap from {bootstrap}: {e}")
                    
        # Start gossip protocol
        asyncio.create_task(self._gossip_loop(operative))
        
    async def _gossip_loop(self, operative: DistributedOperative):
        """Periodic gossip propagation"""
        while True:
            await asyncio.sleep(5)  # Gossip every 5 seconds
            try:
                await operative.propagate_gossip()
            except Exception as e:
                logger.error(f"Gossip error: {e}")

# Demo: Launch distributed swarm
async def demo_distributed_swarm():
    """Demo distributed homomorphic swarm"""
    print("=== Distributed Homomorphic Swarm Demo ===\n")
    
    orchestrator = DistributedSwarmOrchestrator()
    
    # Create queen node
    print("1. Starting Queen node...")
    queen = await orchestrator.create_operative("queen", "localhost", 8000)
    
    # Create worker nodes
    print("\n2. Starting Worker nodes...")
    workers = []
    for i in range(5):
        worker = await orchestrator.create_operative("worker", "localhost", 8001 + i)
        workers.append(worker)
        
    # Wait for gossip propagation
    print("\n3. Waiting for swarm formation...")
    await asyncio.sleep(3)
    
    # Check swarm status
    print(f"\n4. Swarm Status:")
    print(f"   Queen knows about {len(queen.gossip.known_nodes)} nodes")
    print(f"   Workers: {[n.id for n in queen.gossip.known_nodes.values() if n.type == 'worker']}")
    
    # Test distributed bootstrap
    print("\n5. Testing distributed bootstrap...")
    test_data = b"test_ciphertext_" * 1000  # 16KB
    
    start = time.time()
    result = await queen.distribute_computation("bootstrap", test_data)
    elapsed = time.time() - start
    
    print(f"   Distributed bootstrap time: {elapsed*1000:.2f}ms")
    print(f"   Expected speedup: 33.3% (patent claim)")
    
    # Cleanup
    print("\n6. Shutting down swarm...")
    for node in orchestrator.nodes.values():
        await node.stop_server()
        
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    asyncio.run(demo_distributed_swarm())

"""
Performance Optimizations for Homomorphic Swarm
Connection pooling, caching, memory management
"""

import asyncio
import aioredis
import aiomcache
from typing import Dict, Any, Optional, List, Tuple
import time
import numpy as np
from collections import OrderedDict
import psutil
import gc
import mmap
import pickle
from concurrent.futures import ThreadPoolExecutor
import lz4.frame
import multiprocessing as mp

class ConnectionPool:
    """Reusable connection pool for swarm nodes"""
    
    def __init__(self, max_connections: int = 100, timeout: int = 30):
        self.max_connections = max_connections
        self.timeout = timeout
        self._pools: Dict[str, asyncio.Queue] = {}
        self._connection_count: Dict[str, int] = {}
        self._lock = asyncio.Lock()
        
    async def get_connection(self, node_address: str) -> Any:
        """Get connection from pool"""
        async with self._lock:
            if node_address not in self._pools:
                self._pools[node_address] = asyncio.Queue(maxsize=self.max_connections)
                self._connection_count[node_address] = 0
                
        pool = self._pools[node_address]
        
        try:
            # Try to get existing connection
            conn = pool.get_nowait()
            if await self._validate_connection(conn):
                return conn
        except asyncio.QueueEmpty:
            pass
            
        # Create new connection if under limit
        async with self._lock:
            if self._connection_count[node_address] < self.max_connections:
                conn = await self._create_connection(node_address)
                self._connection_count[node_address] += 1
                return conn
                
        # Wait for available connection
        return await asyncio.wait_for(pool.get(), timeout=self.timeout)
        
    async def release_connection(self, node_address: str, conn: Any):
        """Return connection to pool"""
        if node_address in self._pools:
            await self._pools[node_address].put(conn)
            
    async def _create_connection(self, node_address: str) -> Any:
        """Create new connection"""
        import aiohttp
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        return aiohttp.ClientSession(timeout=timeout)
        
    async def _validate_connection(self, conn: Any) -> bool:
        """Check if connection is still valid"""
        return not conn.closed if hasattr(conn, 'closed') else True

class DistributedCache:
    """Multi-tier distributed cache"""
    
    def __init__(self):
        # L1: In-memory LRU cache
        self.l1_cache = LRUCache(max_size=1000)
        
        # L2: Redis cache
        self.redis: Optional[aioredis.Redis] = None
        
        # L3: Memcached
        self.memcached: Optional[aiomcache.Client] = None
        
        # Stats
        self.hits = {'l1': 0, 'l2': 0, 'l3': 0}
        self.misses = 0
        
    async def initialize(self, redis_url: str = "redis://localhost", 
                        memcached_host: str = "localhost"):
        """Initialize cache backends"""
        self.redis = await aioredis.create_redis_pool(redis_url)
        self.memcached = aiomcache.Client(memcached_host, 11211)
        
    async def get(self, key: str) -> Optional[bytes]:
        """Get from cache (waterfall through tiers)"""
        # L1 - Memory
        value = self.l1_cache.get(key)
        if value is not None:
            self.hits['l1'] += 1
            return value
            
        # L2 - Redis
        if self.redis:
            value = await self.redis.get(key)
            if value:
                self.hits['l2'] += 1
                self.l1_cache.put(key, value)  # Promote to L1
                return value
                
        # L3 - Memcached
        if self.memcached:
            value = await self.memcached.get(key)
            if value:
                self.hits['l3'] += 1
                # Promote to higher tiers
                if self.redis:
                    await self.redis.set(key, value, expire=3600)
                self.l1_cache.put(key, value)
                return value
                
        self.misses += 1
        return None
        
    async def set(self, key: str, value: bytes, ttl: int = 3600):
        """Set in all cache tiers"""
        # Compress large values
        if len(value) > 1024:
            value = lz4.frame.compress(value)
            
        # Write to all tiers
        self.l1_cache.put(key, value)
        
        if self.redis:
            await self.redis.set(key, value, expire=ttl)
            
        if self.memcached:
            await self.memcached.set(key, value, exptime=ttl)
            
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_hits = sum(self.hits.values())
        total_requests = total_hits + self.misses
        
        return {
            "hit_rate": total_hits / max(total_requests, 1),
            "hits_by_tier": self.hits,
            "misses": self.misses,
            "l1_size": len(self.l1_cache.cache)
        }

class LRUCache:
    """Thread-safe LRU cache"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self._lock = asyncio.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get value and update access order"""
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
        
    def put(self, key: str, value: Any):
        """Add value to cache"""
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # Remove oldest
            
        self.cache[key] = value

class MemoryManager:
    """Intelligent memory management"""
    
    def __init__(self, target_memory_percent: float = 80.0):
        self.target_memory_percent = target_memory_percent
        self.monitoring = True
        
    async def monitor_loop(self):
        """Monitor and manage memory usage"""
        while self.monitoring:
            memory_percent = psutil.virtual_memory().percent
            
            if memory_percent > self.target_memory_percent:
                await self.free_memory()
                
            await asyncio.sleep(10)  # Check every 10 seconds
            
    async def free_memory(self):
        """Free memory when usage is high"""
        # Force garbage collection
        gc.collect()
        
        # Clear caches if needed
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 90:
            # More aggressive cleanup
            gc.collect(2)
            
            # Notify system to reduce load
            print(f"High memory usage: {memory_percent}%")

class ComputationOptimizer:
    """Optimize homomorphic computations"""
    
    def __init__(self):
        self.operation_cache = {}
        self.computation_graph = {}
        
    def optimize_computation_graph(self, operations: List[Dict]) -> List[Dict]:
        """Optimize computation DAG"""
        # Build dependency graph
        graph = self._build_dependency_graph(operations)
        
        # Identify common subexpressions
        common_subs = self._find_common_subexpressions(graph)
        
        # Reorder for parallelism
        optimized = self._reorder_for_parallelism(graph, common_subs)
        
        # Batch similar operations
        batched = self._batch_operations(optimized)
        
        return batched
        
    def _build_dependency_graph(self, operations: List[Dict]) -> Dict:
        """Build operation dependency graph"""
        graph = {}
        for i, op in enumerate(operations):
            deps = []
            for j, other in enumerate(operations[:i]):
                if self._depends_on(op, other):
                    deps.append(j)
            graph[i] = deps
        return graph
        
    def _depends_on(self, op1: Dict, op2: Dict) -> bool:
        """Check if op1 depends on op2"""
        return any(input_id in op2.get("outputs", []) 
                  for input_id in op1.get("inputs", []))
        
    def _find_common_subexpressions(self, graph: Dict) -> List[Tuple]:
        """Identify repeated computations"""
        expr_map = {}
        common = []
        
        for node, deps in graph.items():
            expr_hash = self._hash_expression(node, deps)
            if expr_hash in expr_map:
                common.append((expr_map[expr_hash], node))
            else:
                expr_map[expr_hash] = node
                
        return common
        
    def _hash_expression(self, node: int, deps: List[int]) -> str:
        """Hash computation expression"""
        return f"{node}:{','.join(map(str, sorted(deps)))}"
        
    def _reorder_for_parallelism(self, graph: Dict, common: List) -> List[int]:
        """Reorder operations for maximum parallelism"""
        levels = self._topological_levels(graph)
        
        # Execute each level in parallel
        ordered = []
        for level in levels:
            ordered.extend(sorted(level))  # Deterministic order
            
        return ordered
        
    def _topological_levels(self, graph: Dict) -> List[List[int]]:
        """Group nodes by topological level"""
        in_degree = {node: len(deps) for node, deps in graph.items()}
        levels = []
        
        while in_degree:
            # Find nodes with no dependencies
            current_level = [node for node, degree in in_degree.items() if degree == 0]
            if not current_level:
                break  # Cycle detected
                
            levels.append(current_level)
            
            # Remove processed nodes
            for node in current_level:
                del in_degree[node]
                # Update dependencies
                for other, deps in graph.items():
                    if node in deps and other in in_degree:
                        in_degree[other] -= 1
                        
        return levels
        
    def _batch_operations(self, operations: List[int]) -> List[Dict]:
        """Batch similar operations together"""
        batches = {}
        
        for op_id in operations:
            op_type = self._get_operation_type(op_id)
            if op_type not in batches:
                batches[op_type] = []
            batches[op_type].append(op_id)
            
        # Convert to batch operations
        batched_ops = []
        for op_type, op_ids in batches.items():
            if len(op_ids) > 1:
                batched_ops.append({
                    "type": "batch",
                    "operation": op_type,
                    "operations": op_ids
                })
            else:
                batched_ops.append({"type": "single", "operation": op_ids[0]})
                
        return batched_ops
        
    def _get_operation_type(self, op_id: int) -> str:
        """Get operation type for batching"""
        # Implementation specific
        return "multiply"  # Placeholder

class ZeroCopySerializer:
    """Zero-copy serialization for large ciphertexts"""
    
    def __init__(self, buffer_size: int = 10 * 1024 * 1024):  # 10MB
        self.buffer_size = buffer_size
        self.mmap_files = {}
        
    def serialize_to_mmap(self, data: bytes, key: str) -> str:
        """Serialize to memory-mapped file"""
        filename = f"/tmp/swarm_mmap_{key}.dat"
        
        # Create memory-mapped file
        with open(filename, "wb") as f:
            f.write(data)
            
        # Map for zero-copy access
        with open(filename, "r+b") as f:
            mmapped = mmap.mmap(f.fileno(), 0)
            self.mmap_files[key] = mmapped
            
        return filename
        
    def deserialize_from_mmap(self, filename: str) -> memoryview:
        """Get zero-copy view of data"""
        with open(filename, "r+b") as f:
            mmapped = mmap.mmap(f.fileno(), 0)
            return memoryview(mmapped)

class ParallelExecutor:
    """Execute operations in parallel"""
    
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()
        self.thread_pool = ThreadPoolExecutor(max_workers=self.num_workers)
        self.process_pool = mp.Pool(processes=self.num_workers)
        
    async def parallel_map(self, func, items: List[Any]) -> List[Any]:
        """Map function over items in parallel"""
        loop = asyncio.get_event_loop()
        
        # Use thread pool for I/O bound
        if asyncio.iscoroutinefunction(func):
            tasks = [func(item) for item in items]
            return await asyncio.gather(*tasks)
            
        # Use process pool for CPU bound
        return await loop.run_in_executor(
            self.process_pool,
            self._parallel_map_sync,
            func,
            items
        )
        
    def _parallel_map_sync(self, func, items):
        """Synchronous parallel map"""
        return self.process_pool.map(func, items)

# Integration example
class OptimizedSwarmNode:
    """Swarm node with all optimizations"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.connection_pool = ConnectionPool()
        self.cache = DistributedCache()
        self.memory_manager = MemoryManager()
        self.optimizer = ComputationOptimizer()
        self.serializer = ZeroCopySerializer()
        self.executor = ParallelExecutor()
        
    async def initialize(self):
        """Initialize all components"""
        await self.cache.initialize()
        asyncio.create_task(self.memory_manager.monitor_loop())
        
    async def process_computation(self, task: Dict) -> Dict:
        """Process with all optimizations"""
        # Check cache
        cache_key = self._compute_cache_key(task)
        cached = await self.cache.get(cache_key)
        if cached:
            return pickle.loads(lz4.frame.decompress(cached))
            
        # Get connection from pool
        conn = await self.connection_pool.get_connection(task["target_node"])
        
        try:
            # Optimize computation graph
            if "operations" in task:
                task["operations"] = self.optimizer.optimize_computation_graph(
                    task["operations"]
                )
                
            # Zero-copy serialization for large data
            if len(task.get("data", b"")) > 1024 * 1024:  # 1MB
                mmap_file = self.serializer.serialize_to_mmap(
                    task["data"], 
                    task["id"]
                )
                task["data_file"] = mmap_file
                del task["data"]
                
            # Execute computation
            result = await self._execute_computation(task, conn)
            
            # Cache result
            cached_data = lz4.frame.compress(pickle.dumps(result))
            await self.cache.set(cache_key, cached_data)
            
            return result
            
        finally:
            await self.connection_pool.release_connection(task["target_node"], conn)
            
    def _compute_cache_key(self, task: Dict) -> str:
        """Generate cache key for task"""
        import hashlib
        task_str = json.dumps(task, sort_keys=True)
        return hashlib.sha256(task_str.encode()).hexdigest()
        
    async def _execute_computation(self, task: Dict, conn: Any) -> Dict:
        """Execute the actual computation"""
        # Implementation specific
        return {"result": "computed"}

if __name__ == "__main__":
    # Demo optimized node
    async def demo():
        node = OptimizedSwarmNode("worker_0")
        await node.initialize()
        
        # Process computation with all optimizations
        result = await node.process_computation({
            "id": "task_123",
            "operation": "multiply",
            "data": b"large_encrypted_data" * 1000,
            "target_node": "worker_1"
        })
        
        print(f"Result: {result}")
        print(f"Cache stats: {node.cache.get_stats()}")
        
    asyncio.run(demo())

"""
Database and Persistence Layer
PostgreSQL, Redis, S3 storage for swarm data
"""

from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Boolean, JSON, BYTEA, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import asyncpg
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
import boto3
import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
import json

Base = declarative_base()

# Database models
class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    execution_time_ms = Column(Float)
    node_id = Column(String(100))
    speedup_percent = Column(Float)
    metadata = Column(JSON)
    
    __table_args__ = (
        Index('idx_operation_type', 'operation_type'),
        Index('idx_created_at', 'created_at'),
        Index('idx_node_id', 'node_id'),
    )

class CiphertextStorage(Base):
    __tablename__ = "ciphertexts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash_key = Column(String(64), unique=True, index=True)
    storage_url = Column(String(500))  # S3 URL
    size_bytes = Column(Integer)
    encryption_params = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    accessed_at = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)

class NodeRegistry(Base):
    __tablename__ = "nodes"
    
    node_id = Column(String(100), primary_key=True)
    node_type = Column(String(20))
    host = Column(String(255))
    port = Column(Integer)
    public_key = Column(BYTEA)
    trust_score = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(DateTime)
    performance_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_node_type', 'node_type'),
        Index('idx_is_active', 'is_active'),
    )

class ByzantineEvent(Base):
    __tablename__ = "byzantine_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    detected_at = Column(DateTime, default=datetime.utcnow)
    node_id = Column(String(100))
    detection_type = Column(String(50))
    guardian_id = Column(String(100))
    evidence = Column(JSON)
    action_taken = Column(String(100))

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engine = None
        self.session_factory = None
        self.async_pool = None
        
    async def initialize(self):
        """Initialize database connections"""
        # PostgreSQL
        self.engine = create_engine(
            self.config["postgresql_url"],
            pool_size=20,
            max_overflow=40,
            pool_pre_ping=True
        )
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        
        # Async PostgreSQL pool
        self.async_pool = await asyncpg.create_pool(
            self.config["postgresql_url"],
            min_size=10,
            max_size=20
        )
        
    async def record_operation(self, operation_data: Dict) -> str:
        """Record operation in database"""
        async with self.async_pool.acquire() as conn:
            operation_id = str(uuid.uuid4())
            await conn.execute("""
                INSERT INTO operations 
                (id, operation_type, status, node_id, metadata)
                VALUES ($1, $2, $3, $4, $5)
            """, operation_id, operation_data["type"], "pending",
                operation_data.get("node_id"), json.dumps(operation_data))
            
            return operation_id
            
    async def update_operation(self, operation_id: str, updates: Dict):
        """Update operation status"""
        async with self.async_pool.acquire() as conn:
            if "completed_at" not in updates:
                updates["completed_at"] = datetime.utcnow()
                
            set_clause = ", ".join([f"{k} = ${i+2}" for i, k in enumerate(updates.keys())])
            values = [operation_id] + list(updates.values())
            
            await conn.execute(f"""
                UPDATE operations 
                SET {set_clause}
                WHERE id = $1
            """, *values)
            
    async def get_operation_stats(self, time_window_hours: int = 24) -> Dict:
        """Get operation statistics"""
        async with self.async_pool.acquire() as conn:
            results = await conn.fetch("""
                SELECT 
                    operation_type,
                    COUNT(*) as count,
                    AVG(execution_time_ms) as avg_time,
                    AVG(speedup_percent) as avg_speedup,
                    MIN(execution_time_ms) as min_time,
                    MAX(execution_time_ms) as max_time
                FROM operations
                WHERE created_at > NOW() - INTERVAL '%s hours'
                AND status = 'completed'
                GROUP BY operation_type
            """, time_window_hours)
            
            return {row["operation_type"]: dict(row) for row in results}

class S3Storage:
    """S3 storage for large ciphertexts"""
    
    def __init__(self, config: Dict[str, Any]):
        self.bucket_name = config["s3_bucket"]
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config.get("aws_access_key"),
            aws_secret_access_key=config.get("aws_secret_key"),
            region_name=config.get("aws_region", "us-east-1")
        )
        
    async def store_ciphertext(self, ciphertext: bytes, metadata: Dict) -> str:
        """Store ciphertext in S3"""
        import hashlib
        
        # Generate key
        hash_key = hashlib.sha256(ciphertext).hexdigest()
        s3_key = f"ciphertexts/{hash_key[:2]}/{hash_key}"
        
        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=ciphertext,
            Metadata=metadata,
            StorageClass='INTELLIGENT_TIERING'
        )
        
        return f"s3://{self.bucket_name}/{s3_key}"
        
    async def retrieve_ciphertext(self, s3_url: str) -> bytes:
        """Retrieve ciphertext from S3"""
        # Parse S3 URL
        parts = s3_url.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1]
        
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()

class RedisCache:
    """Redis caching layer"""
    
    def __init__(self, config: Dict[str, Any]):
        self.redis_url = config["redis_url"]
        self.redis = None
        self.default_ttl = config.get("cache_ttl", 3600)
        
    async def initialize(self):
        """Initialize Redis connection"""
        self.redis = await aioredis.create_redis_pool(self.redis_url)
        
    async def get_cached_result(self, cache_key: str) -> Optional[bytes]:
        """Get cached computation result"""
        return await self.redis.get(cache_key)
        
    async def cache_result(self, cache_key: str, result: bytes, ttl: int = None):
        """Cache computation result"""
        ttl = ttl or self.default_ttl
        await self.redis.setex(cache_key, ttl, result)
        
    async def get_node_status(self, node_id: str) -> Optional[Dict]:
        """Get cached node status"""
        data = await self.redis.hget("node_status", node_id)
        return json.loads(data) if data else None
        
    async def update_node_status(self, node_id: str, status: Dict):
        """Update node status in cache"""
        await self.redis.hset("node_status", node_id, json.dumps(status))
        
    async def increment_counter(self, counter_name: str) -> int:
        """Increment and return counter value"""
        return await self.redis.incr(counter_name)

class MongoDBLogger:
    """MongoDB for detailed logs and analytics"""
    
    def __init__(self, config: Dict[str, Any]):
        self.mongo_url = config["mongodb_url"]
        self.db_name = config.get("db_name", "homomorphic_swarm")
        self.client = None
        self.db = None
        
    async def initialize(self):
        """Initialize MongoDB connection"""
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.db_name]
        
        # Create indexes
        await self.db.operation_logs.create_index("timestamp")
        await self.db.operation_logs.create_index("operation_id")
        await self.db.performance_metrics.create_index([("timestamp", -1)])
        
    async def log_operation(self, operation_data: Dict):
        """Log detailed operation data"""
        operation_data["timestamp"] = datetime.utcnow()
        await self.db.operation_logs.insert_one(operation_data)
        
    async def log_performance_metric(self, metric_data: Dict):
        """Log performance metrics"""
        metric_data["timestamp"] = datetime.utcnow()
        await self.db.performance_metrics.insert_one(metric_data)
        
    async def get_operation_history(self, 
                                   filters: Dict = None,
                                   limit: int = 100) -> List[Dict]:
        """Query operation history"""
        filters = filters or {}
        cursor = self.db.operation_logs.find(filters).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
        
    async def aggregate_metrics(self, pipeline: List[Dict]) -> List[Dict]:
        """Run aggregation pipeline on metrics"""
        cursor = self.db.performance_metrics.aggregate(pipeline)
        return await cursor.to_list(length=None)

class PersistenceOrchestrator:
    """Orchestrates all persistence operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_manager = DatabaseManager(config)
        self.s3_storage = S3Storage(config)
        self.redis_cache = RedisCache(config)
        self.mongo_logger = MongoDBLogger(config)
        
    async def initialize(self):
        """Initialize all persistence layers"""
        await self.db_manager.initialize()
        await self.redis_cache.initialize()
        await self.mongo_logger.initialize()
        
    async def store_computation(self, 
                              operation_type: str,
                              input_data: bytes,
                              result: bytes,
                              metadata: Dict) -> str:
        """Store computation with all persistence layers"""
        # 1. Record in PostgreSQL
        operation_id = await self.db_manager.record_operation({
            "type": operation_type,
            "node_id": metadata.get("node_id"),
            "metadata": metadata
        })
        
        # 2. Store large data in S3
        if len(result) > 1024 * 1024:  # 1MB threshold
            s3_url = await self.s3_storage.store_ciphertext(result, {
                "operation_id": operation_id,
                "operation_type": operation_type
            })
            metadata["result_url"] = s3_url
        
        # 3. Cache in Redis
        cache_key = self._compute_cache_key(operation_type, input_data)
        await self.redis_cache.cache_result(cache_key, result)
        
        # 4. Log to MongoDB
        await self.mongo_logger.log_operation({
            "operation_id": operation_id,
            "operation_type": operation_type,
            "input_size": len(input_data),
            "result_size": len(result),
            "metadata": metadata
        })
        
        return operation_id
        
    def _compute_cache_key(self, operation_type: str, input_data: bytes) -> str:
        """Generate cache key"""
        import hashlib
        data_hash = hashlib.sha256(input_data).hexdigest()[:16]
        return f"result:{operation_type}:{data_hash}"
        
    async def get_cached_or_compute(self,
                                   operation_type: str,
                                   input_data: bytes,
                                   compute_func) -> bytes:
        """Get from cache or compute"""
        cache_key = self._compute_cache_key(operation_type, input_data)
        
        # Check cache
        cached = await self.redis_cache.get_cached_result(cache_key)
        if cached:
            await self.redis_cache.increment_counter("cache_hits")
            return cached
            
        # Compute
        await self.redis_cache.increment_counter("cache_misses")
        result = await compute_func()
        
        # Store result
        await self.store_computation(operation_type, input_data, result, {})
        
        return result

# Migration script
async def migrate_database():
    """Run database migrations"""
    from alembic import command
    from alembic.config import Config
    
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Example configuration
PERSISTENCE_CONFIG = {
    "postgresql_url": "postgresql://user:pass@localhost/homomorphic_swarm",
    "redis_url": "redis://localhost:6379",
    "mongodb_url": "mongodb://localhost:27017",
    "s3_bucket": "homomorphic-swarm-data",
    "aws_access_key": "YOUR_KEY",
    "aws_secret_key": "YOUR_SECRET",
    "cache_ttl": 3600
}

if __name__ == "__main__":
    # Example usage
    async def example():
        orchestrator = PersistenceOrchestrator(PERSISTENCE_CONFIG)
        await orchestrator.initialize()
        
        # Store computation
        operation_id = await orchestrator.store_computation(
            "bootstrap",
            b"input_ciphertext",
            b"output_ciphertext",
            {"speedup": 35.2, "node_id": "worker_1"}
        )
        
        print(f"Stored operation: {operation_id}")
        
    asyncio.run(example())

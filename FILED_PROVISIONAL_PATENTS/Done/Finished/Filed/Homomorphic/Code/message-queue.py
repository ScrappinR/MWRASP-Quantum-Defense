"""
Message Queue Integration
Kafka, RabbitMQ, and event-driven architecture
"""

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import aio_pika
from typing import Dict, List, Any, Callable, Optional
import json
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Swarm event types"""
    OPERATION_REQUESTED = "operation.requested"
    OPERATION_STARTED = "operation.started"
    OPERATION_COMPLETED = "operation.completed"
    OPERATION_FAILED = "operation.failed"
    
    BOOTSTRAP_INITIATED = "bootstrap.initiated"
    BOOTSTRAP_COMPLETED = "bootstrap.completed"
    
    NODE_JOINED = "node.joined"
    NODE_LEFT = "node.left"
    NODE_FAILED = "node.failed"
    
    BYZANTINE_DETECTED = "byzantine.detected"
    BYZANTINE_RESOLVED = "byzantine.resolved"
    
    PERFORMANCE_ALERT = "performance.alert"
    SPEEDUP_ACHIEVED = "speedup.achieved"

@dataclass
class SwarmEvent:
    """Base event structure"""
    event_id: str
    event_type: EventType
    timestamp: datetime
    node_id: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    
    def to_json(self) -> str:
        data = asdict(self)
        data["event_type"] = self.event_type.value
        data["timestamp"] = self.timestamp.isoformat()
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, data: str) -> 'SwarmEvent':
        obj = json.loads(data)
        obj["event_type"] = EventType(obj["event_type"])
        obj["timestamp"] = datetime.fromisoformat(obj["timestamp"])
        return cls(**obj)

class KafkaEventBus:
    """Kafka-based event bus for high throughput"""
    
    def __init__(self, config: Dict[str, Any]):
        self.bootstrap_servers = config["bootstrap_servers"]
        self.producer = None
        self.consumers: Dict[str, AIOKafkaConsumer] = {}
        self.handlers: Dict[EventType, List[Callable]] = {}
        
    async def initialize(self):
        """Initialize Kafka connections"""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: v.encode('utf-8'),
            compression_type='lz4'
        )
        await self.producer.start()
        
    async def publish(self, event: SwarmEvent, topic: str = "swarm-events"):
        """Publish event to Kafka"""
        try:
            # Add partitioning key based on node_id for ordering
            key = event.node_id.encode('utf-8')
            
            await self.producer.send(
                topic,
                value=event.to_json(),
                key=key,
                headers=[
                    ("event_type", event.event_type.value.encode()),
                    ("correlation_id", (event.correlation_id or "").encode())
                ]
            )
            
            logger.debug(f"Published event {event.event_id} to {topic}")
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
            
    async def subscribe(self, 
                       topics: List[str],
                       group_id: str,
                       handler: Callable[[SwarmEvent], None]):
        """Subscribe to Kafka topics"""
        consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: v.decode('utf-8'),
            enable_auto_commit=True,
            auto_offset_reset='latest'
        )
        
        await consumer.start()
        self.consumers[group_id] = consumer
        
        # Start consumer loop
        asyncio.create_task(self._consume_loop(consumer, handler))
        
    async def _consume_loop(self, consumer: AIOKafkaConsumer, handler: Callable):
        """Consume messages in a loop"""
        try:
            async for msg in consumer:
                try:
                    event = SwarmEvent.from_json(msg.value)
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            await consumer.stop()
            
    async def close(self):
        """Close all connections"""
        if self.producer:
            await self.producer.stop()
            
        for consumer in self.consumers.values():
            await consumer.stop()

class RabbitMQEventBus:
    """RabbitMQ for reliable message delivery"""
    
    def __init__(self, config: Dict[str, Any]):
        self.amqp_url = config["amqp_url"]
        self.connection = None
        self.channel = None
        self.exchange_name = "swarm_events"
        
    async def initialize(self):
        """Initialize RabbitMQ connection"""
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        
        # Declare exchange
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        
    async def publish(self, event: SwarmEvent, routing_key: str = None):
        """Publish event to RabbitMQ"""
        routing_key = routing_key or f"{event.event_type.value}"
        
        message = aio_pika.Message(
            body=event.to_json().encode(),
            message_id=event.event_id,
            timestamp=event.timestamp,
            headers={
                "event_type": event.event_type.value,
                "node_id": event.node_id,
                "correlation_id": event.correlation_id
            },
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self.exchange.publish(message, routing_key=routing_key)
        
    async def subscribe(self,
                       routing_patterns: List[str],
                       queue_name: str,
                       handler: Callable[[SwarmEvent], None]):
        """Subscribe to events"""
        # Declare queue
        queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                "x-message-ttl": 3600000,  # 1 hour TTL
                "x-max-length": 10000       # Max 10k messages
            }
        )
        
        # Bind to routing patterns
        for pattern in routing_patterns:
            await queue.bind(self.exchange, routing_key=pattern)
            
        # Start consuming
        await queue.consume(self._handle_message(handler))
        
    def _handle_message(self, handler: Callable):
        """Create message handler"""
        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    event = SwarmEvent.from_json(message.body.decode())
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    # Message will be requeued
                    raise
                    
        return process_message
        
    async def close(self):
        """Close connections"""
        if self.connection:
            await self.connection.close()

class EventOrchestrator:
    """Orchestrates events across different message systems"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.kafka_bus = KafkaEventBus(config["kafka"]) if "kafka" in config else None
        self.rabbitmq_bus = RabbitMQEventBus(config["rabbitmq"]) if "rabbitmq" in config else None
        self.local_handlers: Dict[EventType, List[Callable]] = {}
        
    async def initialize(self):
        """Initialize all event buses"""
        if self.kafka_bus:
            await self.kafka_bus.initialize()
        if self.rabbitmq_bus:
            await self.rabbitmq_bus.initialize()
            
    def register_handler(self, event_type: EventType, handler: Callable):
        """Register local event handler"""
        if event_type not in self.local_handlers:
            self.local_handlers[event_type] = []
        self.local_handlers[event_type].append(handler)
        
    async def publish(self, event: SwarmEvent, reliable: bool = False):
        """Publish event to appropriate bus"""
        # Local handlers first
        if event.event_type in self.local_handlers:
            for handler in self.local_handlers[event.event_type]:
                await handler(event)
                
        # Use RabbitMQ for reliable delivery
        if reliable and self.rabbitmq_bus:
            await self.rabbitmq_bus.publish(event)
        # Use Kafka for high throughput
        elif self.kafka_bus:
            await self.kafka_bus.publish(event)
            
    async def create_and_publish(self,
                               event_type: EventType,
                               node_id: str,
                               payload: Dict[str, Any],
                               correlation_id: str = None,
                               reliable: bool = False):
        """Helper to create and publish event"""
        event = SwarmEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.utcnow(),
            node_id=node_id,
            payload=payload,
            correlation_id=correlation_id
        )
        
        await self.publish(event, reliable=reliable)
        return event

class EventDrivenWorker:
    """Worker that processes events"""
    
    def __init__(self, node_id: str, event_orchestrator: EventOrchestrator):
        self.node_id = node_id
        self.events = event_orchestrator
        self.processing_queue = asyncio.Queue()
        
    async def start(self):
        """Start processing events"""
        # Register handlers
        self.events.register_handler(
            EventType.OPERATION_REQUESTED,
            self.handle_operation_request
        )
        
        # Subscribe to Kafka for high-throughput operations
        if self.events.kafka_bus:
            await self.events.kafka_bus.subscribe(
                ["operation-requests"],
                f"worker-{self.node_id}",
                self.handle_kafka_event
            )
            
        # Process queue
        asyncio.create_task(self._process_loop())
        
    async def handle_operation_request(self, event: SwarmEvent):
        """Handle operation request"""
        await self.processing_queue.put(event)
        
    async def handle_kafka_event(self, event: SwarmEvent):
        """Handle event from Kafka"""
        if event.event_type == EventType.OPERATION_REQUESTED:
            await self.processing_queue.put(event)
            
    async def _process_loop(self):
        """Process events from queue"""
        while True:
            event = await self.processing_queue.get()
            
            try:
                # Notify start
                await self.events.create_and_publish(
                    EventType.OPERATION_STARTED,
                    self.node_id,
                    {"operation_id": event.payload["operation_id"]},
                    correlation_id=event.event_id
                )
                
                # Process operation
                result = await self._process_operation(event.payload)
                
                # Notify completion
                await self.events.create_and_publish(
                    EventType.OPERATION_COMPLETED,
                    self.node_id,
                    {
                        "operation_id": event.payload["operation_id"],
                        "result": result,
                        "execution_time_ms": result.get("execution_time_ms")
                    },
                    correlation_id=event.event_id,
                    reliable=True  # Ensure delivery
                )
                
                # Check for speedup achievement
                if result.get("speedup_percent", 0) >= 33.3:
                    await self.events.create_and_publish(
                        EventType.SPEEDUP_ACHIEVED,
                        self.node_id,
                        {"speedup_percent": result["speedup_percent"]},
                        correlation_id=event.event_id
                    )
                    
            except Exception as e:
                logger.error(f"Operation failed: {e}")
                await self.events.create_and_publish(
                    EventType.OPERATION_FAILED,
                    self.node_id,
                    {
                        "operation_id": event.payload["operation_id"],
                        "error": str(e)
                    },
                    correlation_id=event.event_id,
                    reliable=True
                )
                
    async def _process_operation(self, operation: Dict) -> Dict:
        """Process the actual operation"""
        # Simulate processing
        await asyncio.sleep(0.01)
        return {
            "result": "processed",
            "execution_time_ms": 8.5,
            "speedup_percent": 35.2
        }

class EventMonitor:
    """Monitor and analyze events"""
    
    def __init__(self, event_orchestrator: EventOrchestrator):
        self.events = event_orchestrator
        self.metrics = {
            "events_processed": 0,
            "events_by_type": {},
            "average_processing_time": {}
        }
        
    async def start(self):
        """Start monitoring"""
        # Subscribe to all events
        for event_type in EventType:
            self.events.register_handler(event_type, self.analyze_event)
            
    async def analyze_event(self, event: SwarmEvent):
        """Analyze event for metrics"""
        self.metrics["events_processed"] += 1
        
        # Count by type
        event_type_str = event.event_type.value
        if event_type_str not in self.metrics["events_by_type"]:
            self.metrics["events_by_type"][event_type_str] = 0
        self.metrics["events_by_type"][event_type_str] += 1
        
        # Track processing times
        if event.event_type == EventType.OPERATION_COMPLETED:
            exec_time = event.payload.get("execution_time_ms", 0)
            op_type = event.payload.get("operation_type", "unknown")
            
            if op_type not in self.metrics["average_processing_time"]:
                self.metrics["average_processing_time"][op_type] = []
            self.metrics["average_processing_time"][op_type].append(exec_time)
            
        # Detect anomalies
        if event.event_type == EventType.BYZANTINE_DETECTED:
            logger.warning(f"Byzantine behavior detected: {event.payload}")
            
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        # Calculate averages
        avg_times = {}
        for op_type, times in self.metrics["average_processing_time"].items():
            if times:
                avg_times[op_type] = sum(times) / len(times)
                
        return {
            **self.metrics,
            "average_processing_time": avg_times
        }

# Configuration
EVENT_CONFIG = {
    "kafka": {
        "bootstrap_servers": "localhost:9092"
    },
    "rabbitmq": {
        "amqp_url": "amqp://guest:guest@localhost/"
    }
}

if __name__ == "__main__":
    # Example usage
    async def example():
        orchestrator = EventOrchestrator(EVENT_CONFIG)
        await orchestrator.initialize()
        
        # Create worker
        worker = EventDrivenWorker("worker_1", orchestrator)
        await worker.start()
        
        # Create monitor
        monitor = EventMonitor(orchestrator)
        await monitor.start()
        
        # Publish test event
        await orchestrator.create_and_publish(
            EventType.OPERATION_REQUESTED,
            "queen_0",
            {
                "operation_id": str(uuid.uuid4()),
                "operation_type": "bootstrap",
                "data": "encrypted_data"
            }
        )
        
        # Wait and check metrics
        await asyncio.sleep(1)
        print(f"Metrics: {monitor.get_metrics()}")
        
    asyncio.run(example())

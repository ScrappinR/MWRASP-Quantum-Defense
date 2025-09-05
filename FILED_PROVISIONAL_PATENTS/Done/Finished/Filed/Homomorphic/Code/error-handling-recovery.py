"""
Error Handling and Recovery Mechanisms
Circuit breakers, retry logic, and self-healing
"""

from typing import Dict, List, Any, Optional, Callable, Type
import asyncio
import time
from dataclasses import dataclass
from enum import Enum
import logging
from collections import deque
import traceback
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Categorized error types"""
    NETWORK_ERROR = "network_error"
    COMPUTATION_ERROR = "computation_error"
    BYZANTINE_ERROR = "byzantine_error"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    TIMEOUT_ERROR = "timeout_error"
    ENCRYPTION_ERROR = "encryption_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class ErrorContext:
    """Context for error handling"""
    error_type: ErrorType
    error: Exception
    timestamp: datetime
    node_id: str
    operation_id: Optional[str] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = None
    traceback: str = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.traceback is None:
            self.traceback = traceback.format_exc()

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    class State(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 expected_exception: Type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = self.State.CLOSED
        self._lock = asyncio.Lock()
        
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        async with self._lock:
            if self.state == self.State.OPEN:
                if self._should_attempt_reset():
                    self.state = self.State.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")
                    
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise
            
    async def _on_success(self):
        """Handle successful call"""
        async with self._lock:
            self.failure_count = 0
            if self.state == self.State.HALF_OPEN:
                self.state = self.State.CLOSED
                logger.info("Circuit breaker reset to CLOSED")
                
    async def _on_failure(self):
        """Handle failed call"""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = self.State.OPEN
                logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
                
    def _should_attempt_reset(self) -> bool:
        """Check if we should try to reset"""
        return (self.last_failure_time and 
                time.time() - self.last_failure_time >= self.recovery_timeout)

class RetryPolicy:
    """Configurable retry policy"""
    
    def __init__(self,
                 max_retries: int = 3,
                 initial_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        
    def get_delay(self, retry_count: int) -> float:
        """Calculate delay for retry attempt"""
        delay = min(
            self.initial_delay * (self.exponential_base ** retry_count),
            self.max_delay
        )
        
        if self.jitter:
            import random
            delay *= (0.5 + random.random())
            
        return delay

class ErrorHandler:
    """Centralized error handling"""
    
    def __init__(self):
        self.handlers: Dict[ErrorType, List[Callable]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_policies: Dict[str, RetryPolicy] = {}
        self.error_history = deque(maxlen=1000)
        
    def register_handler(self, error_type: ErrorType, handler: Callable):
        """Register error handler"""
        if error_type not in self.handlers:
            self.handlers[error_type] = []
        self.handlers[error_type].append(handler)
        
    async def handle_error(self, context: ErrorContext) -> bool:
        """Handle error with registered handlers"""
        self.error_history.append(context)
        
        handlers = self.handlers.get(context.error_type, [])
        handlers.extend(self.handlers.get(ErrorType.UNKNOWN_ERROR, []))
        
        handled = False
        for handler in handlers:
            try:
                if await handler(context):
                    handled = True
                    break
            except Exception as e:
                logger.error(f"Error in error handler: {e}")
                
        return handled
        
    def get_circuit_breaker(self, service: str) -> CircuitBreaker:
        """Get or create circuit breaker for service"""
        if service not in self.circuit_breakers:
            self.circuit_breakers[service] = CircuitBreaker()
        return self.circuit_breakers[service]
        
    def get_retry_policy(self, operation: str) -> RetryPolicy:
        """Get retry policy for operation"""
        if operation not in self.retry_policies:
            # Default policies by operation type
            if "bootstrap" in operation:
                self.retry_policies[operation] = RetryPolicy(max_retries=5)
            elif "byzantine" in operation:
                self.retry_policies[operation] = RetryPolicy(max_retries=1)
            else:
                self.retry_policies[operation] = RetryPolicy()
                
        return self.retry_policies[operation]

class ResilienceManager:
    """Manages system resilience and recovery"""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.recovery_strategies: Dict[ErrorType, Callable] = {}
        self._setup_default_strategies()
        
    def _setup_default_strategies(self):
        """Setup default recovery strategies"""
        self.recovery_strategies[ErrorType.NETWORK_ERROR] = self._recover_network
        self.recovery_strategies[ErrorType.COMPUTATION_ERROR] = self._recover_computation
        self.recovery_strategies[ErrorType.BYZANTINE_ERROR] = self._recover_byzantine
        self.recovery_strategies[ErrorType.RESOURCE_EXHAUSTION] = self._recover_resources
        
    async def with_resilience(self, 
                            func: Callable,
                            operation_name: str,
                            node_id: str,
                            *args, **kwargs):
        """Execute function with full resilience"""
        retry_policy = self.error_handler.get_retry_policy(operation_name)
        circuit_breaker = self.error_handler.get_circuit_breaker(node_id)
        
        for retry_count in range(retry_policy.max_retries + 1):
            try:
                # Execute with circuit breaker
                result = await circuit_breaker.call(func, *args, **kwargs)
                return result
                
            except Exception as e:
                # Classify error
                error_type = self._classify_error(e)
                
                # Create context
                context = ErrorContext(
                    error_type=error_type,
                    error=e,
                    timestamp=datetime.utcnow(),
                    node_id=node_id,
                    operation_id=operation_name,
                    retry_count=retry_count
                )
                
                # Handle error
                handled = await self.error_handler.handle_error(context)
                
                # Apply recovery strategy
                if error_type in self.recovery_strategies:
                    recovered = await self.recovery_strategies[error_type](context)
                    if recovered:
                        continue
                        
                # Check if we should retry
                if retry_count < retry_policy.max_retries:
                    delay = retry_policy.get_delay(retry_count)
                    logger.warning(f"Retrying after {delay}s (attempt {retry_count + 1})")
                    await asyncio.sleep(delay)
                else:
                    raise
                    
    def _classify_error(self, error: Exception) -> ErrorType:
        """Classify error type"""
        error_str = str(error).lower()
        
        if any(keyword in error_str for keyword in ["network", "connection", "timeout"]):
            return ErrorType.NETWORK_ERROR
        elif any(keyword in error_str for keyword in ["byzantine", "malicious", "corrupt"]):
            return ErrorType.BYZANTINE_ERROR
        elif any(keyword in error_str for keyword in ["memory", "cpu", "resource"]):
            return ErrorType.RESOURCE_EXHAUSTION
        elif any(keyword in error_str for keyword in ["encrypt", "decrypt", "seal"]):
            return ErrorType.ENCRYPTION_ERROR
        else:
            return ErrorType.UNKNOWN_ERROR
            
    async def _recover_network(self, context: ErrorContext) -> bool:
        """Recover from network errors"""
        logger.info(f"Attempting network recovery for {context.node_id}")
        
        # Try alternative endpoints
        # Refresh DNS
        # Reset connections
        
        return True
        
    async def _recover_computation(self, context: ErrorContext) -> bool:
        """Recover from computation errors"""
        # Try different parameters
        # Reduce computation size
        # Switch to different algorithm
        
        return False
        
    async def _recover_byzantine(self, context: ErrorContext) -> bool:
        """Recover from Byzantine errors"""
        # Exclude malicious node
        # Increase replication
        # Switch to verified nodes only
        
        from message_queue import EventType, SwarmEvent
        event = SwarmEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.BYZANTINE_DETECTED,
            timestamp=datetime.utcnow(),
            node_id=context.node_id,
            payload={"error": str(context.error)}
        )
        # Publish event
        
        return False
        
    async def _recover_resources(self, context: ErrorContext) -> bool:
        """Recover from resource exhaustion"""
        # Free memory
        import gc
        gc.collect()
        
        # Reduce batch sizes
        # Queue operations
        
        return True

class SelfHealingSystem:
    """Self-healing mechanisms"""
    
    def __init__(self, resilience_manager: ResilienceManager):
        self.resilience_manager = resilience_manager
        self.health_checks: Dict[str, Callable] = {}
        self.healing_actions: Dict[str, Callable] = {}
        self.monitoring_interval = 30  # seconds
        
    def register_health_check(self, component: str, check: Callable):
        """Register health check"""
        self.health_checks[component] = check
        
    def register_healing_action(self, component: str, action: Callable):
        """Register healing action"""
        self.healing_actions[component] = action
        
    async def start_monitoring(self):
        """Start self-healing monitor"""
        while True:
            await self._check_and_heal()
            await asyncio.sleep(self.monitoring_interval)
            
    async def _check_and_heal(self):
        """Check health and heal if needed"""
        for component, check in self.health_checks.items():
            try:
                healthy = await check()
                if not healthy:
                    logger.warning(f"Component {component} unhealthy")
                    if component in self.healing_actions:
                        await self.healing_actions[component]()
                        logger.info(f"Healing action applied to {component}")
            except Exception as e:
                logger.error(f"Health check failed for {component}: {e}")

# Decorators for easy use
def with_retry(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retry logic"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    await asyncio.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

def with_circuit_breaker(failure_threshold: int = 5):
    """Decorator for circuit breaker"""
    circuit_breaker = CircuitBreaker(failure_threshold=failure_threshold)
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await circuit_breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator

def with_timeout(seconds: float):
    """Decorator for timeout"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
        return wrapper
    return decorator

# Error recovery for specific swarm operations
class SwarmErrorRecovery:
    """Swarm-specific error recovery"""
    
    def __init__(self):
        self.fallback_nodes: List[str] = []
        self.operation_cache = {}
        
    async def recover_failed_bootstrap(self, 
                                     ciphertext: bytes,
                                     failed_nodes: List[str]) -> bytes:
        """Recover from failed bootstrap"""
        # Try fallback nodes
        for node in self.fallback_nodes:
            if node not in failed_nodes:
                try:
                    # Attempt bootstrap on fallback node
                    result = await self._bootstrap_on_node(ciphertext, node)
                    return result
                except Exception:
                    continue
                    
        # If all fail, use cached result if available
        cache_key = hashlib.sha256(ciphertext).hexdigest()[:16]
        if cache_key in self.operation_cache:
            logger.warning("Using cached bootstrap result")
            return self.operation_cache[cache_key]
            
        raise Exception("Bootstrap recovery failed")
        
    async def _bootstrap_on_node(self, ciphertext: bytes, node_id: str) -> bytes:
        """Bootstrap on specific node"""
        # Implementation
        return ciphertext

# Example usage
async def example_resilient_operation():
    """Example of resilient operation"""
    # Setup
    error_handler = ErrorHandler()
    resilience_manager = ResilienceManager(error_handler)
    
    # Register custom error handler
    async def handle_byzantine(context: ErrorContext) -> bool:
        logger.error(f"Byzantine behavior from {context.node_id}")
        # Exclude node from future operations
        return True
        
    error_handler.register_handler(ErrorType.BYZANTINE_ERROR, handle_byzantine)
    
    # Execute with resilience
    @with_timeout(30.0)
    @with_retry(max_retries=3)
    async def risky_operation():
        # Simulate operation that might fail
        import random
        if random.random() < 0.5:
            raise Exception("Operation failed")
        return "Success"
        
    try:
        result = await resilience_manager.with_resilience(
            risky_operation,
            "test_operation",
            "node_1"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after all retries: {e}")

if __name__ == "__main__":
    asyncio.run(example_resilient_operation())

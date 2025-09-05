"""
Centralized Logging and Observability System
ELK stack integration, distributed tracing, and log analysis
"""

import logging
import json
import time
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import structlog
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.aiohttp import AioHttpClientInstrumentor
from elasticsearch import AsyncElasticsearch
import aiologger
from pythonjsonlogger import jsonlogger

# Resource information
resource = Resource.create({
    "service.name": "homomorphic-swarm",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# OTLP exporters
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Metrics
metric_exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

# Structured logging setup
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            parameters=[structlog.processors.CallsiteParameter.FILENAME,
                       structlog.processors.CallsiteParameter.LINENO,
                       structlog.processors.CallsiteParameter.FUNC_NAME]
        ),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: str
    message: str
    node_id: str
    operation_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def to_elasticsearch(self) -> Dict:
        """Convert to Elasticsearch document"""
        doc = asdict(self)
        doc["timestamp"] = self.timestamp.isoformat()
        doc["@timestamp"] = self.timestamp  # For Kibana
        return doc

class SwarmLogger:
    """Enhanced logger for swarm operations"""
    
    def __init__(self, node_id: str, node_type: str):
        self.node_id = node_id
        self.node_type = node_type
        self.logger = structlog.get_logger()
        self.es_client = None
        self.metrics = self._setup_metrics()
        
    def _setup_metrics(self):
        """Setup custom metrics"""
        return {
            "log_messages": meter.create_counter(
                "swarm_log_messages_total",
                description="Total log messages",
                unit="1"
            ),
            "errors": meter.create_counter(
                "swarm_errors_total",
                description="Total errors logged",
                unit="1"
            ),
            "operation_duration": meter.create_histogram(
                "swarm_operation_duration_seconds",
                description="Operation duration",
                unit="s"
            )
        }
        
    async def initialize(self, elasticsearch_url: str = None):
        """Initialize logger connections"""
        if elasticsearch_url:
            self.es_client = AsyncElasticsearch([elasticsearch_url])
            
    def _add_context(self, **kwargs) -> Dict:
        """Add swarm context to logs"""
        ctx = trace.get_current_span().get_span_context()
        
        context = {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "trace_id": format(ctx.trace_id, '032x') if ctx.trace_id else None,
            "span_id": format(ctx.span_id, '016x') if ctx.span_id else None,
            "environment": os.getenv("ENVIRONMENT", "development"),
            **kwargs
        }
        
        return context
        
    async def log(self, level: str, message: str, **kwargs):
        """Log with context"""
        context = self._add_context(**kwargs)
        
        # Update metrics
        self.metrics["log_messages"].add(1, {"level": level, "node_type": self.node_type})
        if level == "error":
            self.metrics["errors"].add(1, {"node_type": self.node_type})
            
        # Log via structlog
        getattr(self.logger, level)(message, **context)
        
        # Send to Elasticsearch
        if self.es_client:
            await self._send_to_elasticsearch(level, message, context)
            
    async def _send_to_elasticsearch(self, level: str, message: str, context: Dict):
        """Send log to Elasticsearch"""
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            level=level,
            message=message,
            node_id=self.node_id,
            operation_id=context.get("operation_id"),
            trace_id=context.get("trace_id"),
            span_id=context.get("span_id"),
            metadata=context
        )
        
        try:
            await self.es_client.index(
                index=f"swarm-logs-{datetime.utcnow().strftime('%Y.%m.%d')}",
                body=entry.to_elasticsearch()
            )
        except Exception as e:
            # Fallback to local logging
            self.logger.error(f"Failed to send to Elasticsearch: {e}")
            
    async def operation(self, operation_name: str, operation_id: str = None):
        """Log operation with tracing"""
        return OperationLogger(self, operation_name, operation_id)

class OperationLogger:
    """Context manager for operation logging"""
    
    def __init__(self, logger: SwarmLogger, operation_name: str, operation_id: str = None):
        self.logger = logger
        self.operation_name = operation_name
        self.operation_id = operation_id or str(uuid.uuid4())
        self.start_time = None
        self.span = None
        
    async def __aenter__(self):
        self.start_time = time.time()
        self.span = tracer.start_span(self.operation_name)
        self.span.set_attribute("operation.id", self.operation_id)
        self.span.set_attribute("node.id", self.logger.node_id)
        
        await self.logger.log(
            "info",
            f"Operation started: {self.operation_name}",
            operation_id=self.operation_id,
            operation_name=self.operation_name
        )
        
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        if exc_val:
            self.span.record_exception(exc_val)
            self.span.set_status(trace.Status(trace.StatusCode.ERROR))
            
            await self.logger.log(
                "error",
                f"Operation failed: {self.operation_name}",
                operation_id=self.operation_id,
                operation_name=self.operation_name,
                duration_seconds=duration,
                error=str(exc_val),
                traceback=traceback.format_exc()
            )
        else:
            self.span.set_status(trace.Status(trace.StatusCode.OK))
            
            await self.logger.log(
                "info",
                f"Operation completed: {self.operation_name}",
                operation_id=self.operation_id,
                operation_name=self.operation_name,
                duration_seconds=duration
            )
            
        self.span.end()
        
        # Record metric
        self.logger.metrics["operation_duration"].record(
            duration,
            {"operation": self.operation_name, "status": "error" if exc_val else "success"}
        )

class DistributedTracer:
    """Distributed tracing for swarm operations"""
    
    def __init__(self):
        self.tracer = tracer
        
    def trace_computation(self, operation_type: str):
        """Decorator for tracing computations"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                with self.tracer.start_as_current_span(
                    f"computation.{operation_type}",
                    kind=trace.SpanKind.INTERNAL
                ) as span:
                    span.set_attribute("operation.type", operation_type)
                    span.set_attribute("input.size", len(str(args)))
                    
                    try:
                        result = await func(*args, **kwargs)
                        span.set_attribute("output.size", len(str(result)))
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.Status(trace.StatusCode.ERROR))
                        raise
                        
            return wrapper
        return decorator
        
    def trace_network_call(self, target_node: str):
        """Trace network calls between nodes"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                with self.tracer.start_as_current_span(
                    f"network.call",
                    kind=trace.SpanKind.CLIENT
                ) as span:
                    span.set_attribute("target.node", target_node)
                    span.set_attribute("network.protocol", "http")
                    
                    return await func(*args, **kwargs)
                    
            return wrapper
        return decorator

class LogAggregator:
    """Aggregate and analyze logs"""
    
    def __init__(self, elasticsearch_url: str):
        self.es_client = AsyncElasticsearch([elasticsearch_url])
        
    async def search_logs(self, 
                         query: Dict,
                         start_time: datetime,
                         end_time: datetime,
                         size: int = 100) -> List[Dict]:
        """Search logs in Elasticsearch"""
        body = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {
                            "@timestamp": {
                                "gte": start_time.isoformat(),
                                "lte": end_time.isoformat()
                            }
                        }},
                        query
                    ]
                }
            },
            "size": size,
            "sort": [{"@timestamp": {"order": "desc"}}]
        }
        
        result = await self.es_client.search(
            index="swarm-logs-*",
            body=body
        )
        
        return [hit["_source"] for hit in result["hits"]["hits"]]
        
    async def analyze_errors(self, time_window_hours: int = 24) -> Dict:
        """Analyze error patterns"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=time_window_hours)
        
        # Aggregate errors by type
        body = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"level": "error"}},
                        {"range": {
                            "@timestamp": {
                                "gte": start_time.isoformat(),
                                "lte": end_time.isoformat()
                            }
                        }}
                    ]
                }
            },
            "aggs": {
                "error_types": {
                    "terms": {"field": "error_type.keyword", "size": 20}
                },
                "nodes": {
                    "terms": {"field": "node_id.keyword", "size": 50}
                },
                "timeline": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "1h"
                    }
                }
            }
        }
        
        result = await self.es_client.search(
            index="swarm-logs-*",
            body=body
        )
        
        return {
            "total_errors": result["hits"]["total"]["value"],
            "error_types": result["aggregations"]["error_types"]["buckets"],
            "affected_nodes": result["aggregations"]["nodes"]["buckets"],
            "timeline": result["aggregations"]["timeline"]["buckets"]
        }
        
    async def get_operation_traces(self, operation_id: str) -> List[Dict]:
        """Get all logs for an operation"""
        logs = await self.search_logs(
            {"term": {"operation_id.keyword": operation_id}},
            datetime.utcnow() - timedelta(hours=24),
            datetime.utcnow(),
            size=1000
        )
        
        # Sort by timestamp
        return sorted(logs, key=lambda x: x["timestamp"])

class PerformanceAnalyzer:
    """Analyze performance from logs and traces"""
    
    def __init__(self, log_aggregator: LogAggregator):
        self.aggregator = log_aggregator
        
    async def analyze_bootstrap_performance(self, hours: int = 24) -> Dict:
        """Analyze bootstrap performance"""
        query = {
            "bool": {
                "must": [
                    {"term": {"operation_name.keyword": "bootstrap"}},
                    {"exists": {"field": "duration_seconds"}}
                ]
            }
        }
        
        logs = await self.aggregator.search_logs(
            query,
            datetime.utcnow() - timedelta(hours=hours),
            datetime.utcnow(),
            size=10000
        )
        
        if not logs:
            return {"error": "No bootstrap operations found"}
            
        durations = [log["duration_seconds"] * 1000 for log in logs]  # Convert to ms
        
        return {
            "count": len(durations),
            "average_ms": np.mean(durations),
            "median_ms": np.median(durations),
            "p95_ms": np.percentile(durations, 95),
            "p99_ms": np.percentile(durations, 99),
            "min_ms": min(durations),
            "max_ms": max(durations),
            "speedup_percent": ((12.0 - np.mean(durations)) / 12.0) * 100  # vs 12ms baseline
        }

# Fluentd configuration for log shipping
FLUENTD_CONFIG = """
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match swarm.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix swarm-logs
  
  <buffer>
    @type file
    path /var/log/fluentd-buffers/swarm.buffer
    flush_mode interval
    flush_interval 10s
  </buffer>
</match>

<filter swarm.**>
  @type record_transformer
  enable_ruby
  <record>
    cluster ${ENV['CLUSTER_NAME']}
    environment ${ENV['ENVIRONMENT']}
  </record>
</filter>
"""

# Filebeat configuration
FILEBEAT_CONFIG = """
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'
  processors:
    - add_kubernetes_metadata:
        host: ${NODE_NAME}
        matchers:
        - logs_path:
            logs_path: "/var/lib/docker/containers/"

output.elasticsearch:
  hosts: ['elasticsearch:9200']
  pipeline: swarm_pipeline
  index: "swarm-logs-%{+yyyy.MM.dd}"

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~
"""

# Logstash pipeline
LOGSTASH_PIPELINE = """
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }
  
  date {
    match => [ "timestamp", "ISO8601" ]
  }
  
  mutate {
    add_field => { 
      "[@metadata][index_name]" => "swarm-logs-%{+YYYY.MM.dd}"
    }
  }
  
  if [level] == "error" {
    mutate {
      add_tag => [ "error", "alert" ]
    }
  }
  
  # Extract operation metrics
  if [operation_name] and [duration_seconds] {
    ruby {
      code => "
        duration_ms = event.get('duration_seconds') * 1000
        event.set('duration_ms', duration_ms)
        
        if event.get('operation_name') == 'bootstrap'
          speedup = ((12.0 - duration_ms) / 12.0) * 100
          event.set('speedup_percent', speedup)
        end
      "
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index_name]}"
  }
  
  if "alert" in [tags] {
    email {
      to => 'ops@example.com'
      subject => 'Swarm Error Alert'
      body => "Error in %{node_id}: %{message}"
    }
  }
}
"""

if __name__ == "__main__":
    # Example usage
    async def demo():
        # Initialize logger
        logger = SwarmLogger("worker_1", "worker")
        await logger.initialize("http://localhost:9200")
        
        # Log operation
        async with logger.operation("bootstrap", "op_123") as op:
            await logger.log("info", "Starting bootstrap process")
            await asyncio.sleep(0.008)  # Simulate work
            await logger.log("info", "Bootstrap completed successfully")
            
        # Analyze logs
        aggregator = LogAggregator("http://localhost:9200")
        errors = await aggregator.analyze_errors()
        print(f"Error analysis: {errors}")
        
        # Performance analysis
        analyzer = PerformanceAnalyzer(aggregator)
        perf = await analyzer.analyze_bootstrap_performance()
        print(f"Bootstrap performance: {perf}")
        
    asyncio.run(demo())

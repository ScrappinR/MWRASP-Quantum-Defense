"""
Production Monitoring with Prometheus/Grafana
Real metrics export from swarm nodes
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from aiohttp import web
import time
import asyncio
from typing import Dict, Optional

# Prometheus metrics
registry = CollectorRegistry()

# Operation metrics
operation_counter = Counter(
    'homomorphic_operations_total',
    'Total homomorphic operations performed',
    ['operation_type', 'node_id', 'node_type'],
    registry=registry
)

operation_duration = Histogram(
    'homomorphic_operation_duration_seconds',
    'Duration of homomorphic operations',
    ['operation_type', 'node_id'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
    registry=registry
)

bootstrap_duration = Histogram(
    'homomorphic_bootstrap_duration_seconds',
    'Bootstrap operation duration',
    ['node_id'],
    buckets=[0.005, 0.008, 0.01, 0.012, 0.015, 0.02, 0.05],
    registry=registry
)

# Node metrics
active_nodes = Gauge(
    'swarm_active_nodes',
    'Number of active nodes in swarm',
    ['node_type'],
    registry=registry
)

node_trust_score = Gauge(
    'swarm_node_trust_score',
    'Trust score of swarm nodes',
    ['node_id', 'node_type'],
    registry=registry
)

# Byzantine metrics
byzantine_detections = Counter(
    'byzantine_detections_total',
    'Total Byzantine failures detected',
    ['detection_type', 'guardian_id'],
    registry=registry
)

# Performance metrics
speedup_gauge = Gauge(
    'homomorphic_speedup_percent',
    'Current speedup percentage vs vanilla',
    registry=registry
)

noise_budget = Gauge(
    'homomorphic_noise_budget',
    'Current noise budget level',
    ['operation_id'],
    registry=registry
)

# Task queue metrics
pending_tasks = Gauge(
    'swarm_pending_tasks',
    'Number of pending tasks',
    ['node_id'],
    registry=registry
)

class PrometheusExporter:
    """Prometheus metrics exporter mixin for swarm nodes"""
    
    def __init__(self):
        self.metrics_registry = registry
        self._setup_metrics_endpoint()
        
    def _setup_metrics_endpoint(self):
        """Add Prometheus metrics endpoint"""
        if hasattr(self, 'app'):
            self.app.router.add_get('/metrics', self.handle_metrics)
            
    async def handle_metrics(self, request):
        """Prometheus metrics endpoint"""
        metrics = generate_latest(self.metrics_registry)
        return web.Response(text=metrics.decode('utf-8'), content_type='text/plain')
    
    def record_operation(self, operation_type: str, duration: float, node_id: str, node_type: str):
        """Record operation metrics"""
        operation_counter.labels(
            operation_type=operation_type,
            node_id=node_id,
            node_type=node_type
        ).inc()
        
        operation_duration.labels(
            operation_type=operation_type,
            node_id=node_id
        ).observe(duration)
        
        if operation_type == "bootstrap":
            bootstrap_duration.labels(node_id=node_id).observe(duration)
            
    def update_node_metrics(self, node_id: str, node_type: str, trust: float):
        """Update node status metrics"""
        node_trust_score.labels(
            node_id=node_id,
            node_type=node_type
        ).set(trust)
        
    def record_byzantine_detection(self, detection_type: str, guardian_id: str):
        """Record Byzantine detection"""
        byzantine_detections.labels(
            detection_type=detection_type,
            guardian_id=guardian_id
        ).inc()
        
    def update_speedup(self, speedup_percent: float):
        """Update speedup gauge"""
        speedup_gauge.set(speedup_percent)

# Enhanced Worker with Prometheus
class MonitoredWorkerOperative:
    """Worker operative with Prometheus metrics"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.node_type = "worker"
        self.exporter = PrometheusExporter()
        
    async def execute_task(self, task: Dict) -> Dict:
        """Execute task with metrics recording"""
        start_time = time.time()
        
        try:
            # Simulate task execution
            if task["operation"] == "bootstrap":
                await asyncio.sleep(0.008)  # 8ms
            else:
                await asyncio.sleep(0.002)
                
            duration = time.time() - start_time
            
            # Record metrics
            self.exporter.record_operation(
                operation_type=task["operation"],
                duration=duration,
                node_id=self.node_id,
                node_type=self.node_type
            )
            
            # Update noise budget
            noise_budget.labels(operation_id=task.get("id", "unknown")).set(
                task.get("noise_remaining", 50.0)
            )
            
            return {
                "success": True,
                "duration": duration,
                "result": "computed"
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.exporter.record_operation(
                operation_type=f"{task['operation']}_failed",
                duration=duration,
                node_id=self.node_id,
                node_type=self.node_type
            )
            raise

# Prometheus configuration
PROMETHEUS_CONFIG = """
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'homomorphic-swarm'
    static_configs:
      # Queen
      - targets: ['localhost:8000']
        labels:
          node_type: 'queen'
      # Workers
      - targets: ['localhost:8001', 'localhost:8002', 'localhost:8003', 'localhost:8004', 'localhost:8005']
        labels:
          node_type: 'worker'
      # Guardians
      - targets: ['localhost:8006', 'localhost:8007', 'localhost:8008']
        labels:
          node_type: 'guardian'

rule_files:
  - 'alerts.yml'
"""

# Alert rules
ALERT_RULES = """
groups:
  - name: swarm_alerts
    interval: 30s
    rules:
      - alert: LowSpeedupAlert
        expr: homomorphic_speedup_percent < 30
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Speedup below patent claim threshold"
          description: "Current speedup {{ $value }}% is below 33.3% claim"
          
      - alert: ByzantineAttackDetected
        expr: rate(byzantine_detections_total[5m]) > 0.1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High rate of Byzantine failures"
          description: "{{ $value }} Byzantine failures per second detected"
          
      - alert: NodeDown
        expr: up == 0
        for: 30s
        labels:
          severity: error
        annotations:
          summary: "Swarm node is down"
          description: "Node {{ $labels.instance }} is not responding"
          
      - alert: HighOperationLatency
        expr: histogram_quantile(0.95, rate(homomorphic_operation_duration_seconds_bucket[5m])) > 0.02
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High operation latency"
          description: "95th percentile latency is {{ $value }}s"
"""

# Grafana dashboard configuration
GRAFANA_DASHBOARD = {
    "dashboard": {
        "title": "Homomorphic Swarm Monitor",
        "panels": [
            {
                "title": "Bootstrap Performance",
                "targets": [{
                    "expr": "histogram_quantile(0.5, rate(homomorphic_bootstrap_duration_seconds_bucket[5m]))",
                    "legendFormat": "p50"
                }, {
                    "expr": "histogram_quantile(0.95, rate(homomorphic_bootstrap_duration_seconds_bucket[5m]))",
                    "legendFormat": "p95"
                }, {
                    "expr": "histogram_quantile(0.99, rate(homomorphic_bootstrap_duration_seconds_bucket[5m]))",
                    "legendFormat": "p99"
                }],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
            },
            {
                "title": "Current Speedup %",
                "targets": [{
                    "expr": "homomorphic_speedup_percent"
                }],
                "type": "stat",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
            },
            {
                "title": "Operations Per Second",
                "targets": [{
                    "expr": "sum(rate(homomorphic_operations_total[1m])) by (operation_type)",
                    "legendFormat": "{{ operation_type }}"
                }],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
            },
            {
                "title": "Active Nodes by Type",
                "targets": [{
                    "expr": "count(up == 1) by (node_type)",
                    "legendFormat": "{{ node_type }}"
                }],
                "type": "bargauge",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
            },
            {
                "title": "Byzantine Detections",
                "targets": [{
                    "expr": "rate(byzantine_detections_total[5m])",
                    "legendFormat": "{{ detection_type }}"
                }],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
            },
            {
                "title": "Node Trust Scores",
                "targets": [{
                    "expr": "swarm_node_trust_score",
                    "legendFormat": "{{ node_id }}"
                }],
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
            }
        ]
    }
}

# Docker Compose configuration
DOCKER_COMPOSE = """
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - "9090:9090"
    networks:
      - swarm-net

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - swarm-net
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    ports:
      - "9093:9093"
    networks:
      - swarm-net

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  swarm-net:
    driver: bridge
"""

# Setup script
def setup_monitoring():
    """Create monitoring configuration files"""
    import os
    
    # Create directories
    os.makedirs("monitoring/grafana/dashboards", exist_ok=True)
    os.makedirs("monitoring/grafana/datasources", exist_ok=True)
    
    # Write Prometheus config
    with open("monitoring/prometheus.yml", "w") as f:
        f.write(PROMETHEUS_CONFIG)
    
    # Write alert rules
    with open("monitoring/alerts.yml", "w") as f:
        f.write(ALERT_RULES)
    
    # Write Grafana dashboard
    with open("monitoring/grafana/dashboards/swarm.json", "w") as f:
        json.dump(GRAFANA_DASHBOARD, f, indent=2)
    
    # Write Grafana datasource
    datasource = {
        "apiVersion": 1,
        "datasources": [{
            "name": "Prometheus",
            "type": "prometheus",
            "access": "proxy",
            "url": "http://prometheus:9090",
            "isDefault": True
        }]
    }
    with open("monitoring/grafana/datasources/prometheus.yml", "w") as f:
        json.dump(datasource, f, indent=2)
    
    # Write docker-compose
    with open("monitoring/docker-compose.yml", "w") as f:
        f.write(DOCKER_COMPOSE)
    
    print("Monitoring setup complete!")
    print("\nTo start:")
    print("cd monitoring && docker-compose up -d")
    print("\nAccess:")
    print("- Prometheus: http://localhost:9090")
    print("- Grafana: http://localhost:3000 (admin/admin)")
    print("- Alertmanager: http://localhost:9093")

if __name__ == "__main__":
    setup_monitoring()

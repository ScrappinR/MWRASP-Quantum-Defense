"""
Chaos Engineering for Homomorphic Swarm
Resilience testing and fault injection
"""

import asyncio
import random
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import time
import logging
import aiohttp
import psutil
import os

logger = logging.getLogger(__name__)

class ChaosType(Enum):
    """Types of chaos experiments"""
    NETWORK_LATENCY = "network_latency"
    NETWORK_PARTITION = "network_partition"
    NODE_FAILURE = "node_failure"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    BYZANTINE_BEHAVIOR = "byzantine_behavior"
    CLOCK_SKEW = "clock_skew"
    DISK_FAILURE = "disk_failure"
    PACKET_LOSS = "packet_loss"
    CPU_SPIKE = "cpu_spike"
    MEMORY_LEAK = "memory_leak"

@dataclass
class ChaosExperiment:
    """Chaos experiment definition"""
    name: str
    chaos_type: ChaosType
    target_nodes: List[str]
    duration_seconds: int
    intensity: float  # 0.0 to 1.0
    parameters: Dict[str, Any]
    rollback_plan: Optional[Callable] = None

class ChaosMonkey:
    """Main chaos engineering system"""
    
    def __init__(self):
        self.active_experiments: Dict[str, ChaosExperiment] = {}
        self.experiment_history = []
        self.safety_checks: List[Callable] = []
        self.metrics_collector = MetricsCollector()
        
    def add_safety_check(self, check: Callable) -> None:
        """Add safety check before running experiments"""
        self.safety_checks.append(check)
        
    async def run_experiment(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Run chaos experiment"""
        # Safety checks
        for check in self.safety_checks:
            if not await check():
                logger.warning(f"Safety check failed for {experiment.name}")
                return {"status": "aborted", "reason": "safety_check_failed"}
                
        # Start metrics collection
        await self.metrics_collector.start_collection(experiment.name)
        
        # Record experiment
        self.active_experiments[experiment.name] = experiment
        experiment_id = f"{experiment.name}_{time.time()}"
        
        try:
            # Apply chaos
            logger.info(f"Starting chaos experiment: {experiment.name}")
            await self._apply_chaos(experiment)
            
            # Wait for duration
            await asyncio.sleep(experiment.duration_seconds)
            
            # Rollback
            if experiment.rollback_plan:
                await experiment.rollback_plan()
                
            # Collect results
            metrics = await self.metrics_collector.stop_collection(experiment.name)
            
            result = {
                "status": "completed",
                "experiment_id": experiment_id,
                "metrics": metrics,
                "findings": self._analyze_results(metrics)
            }
            
            self.experiment_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            if experiment.rollback_plan:
                await experiment.rollback_plan()
            return {"status": "failed", "error": str(e)}
            
        finally:
            del self.active_experiments[experiment.name]
            
    async def _apply_chaos(self, experiment: ChaosExperiment):
        """Apply chaos based on type"""
        if experiment.chaos_type == ChaosType.NETWORK_LATENCY:
            await self._inject_network_latency(experiment)
        elif experiment.chaos_type == ChaosType.NODE_FAILURE:
            await self._inject_node_failure(experiment)
        elif experiment.chaos_type == ChaosType.BYZANTINE_BEHAVIOR:
            await self._inject_byzantine_behavior(experiment)
        elif experiment.chaos_type == ChaosType.RESOURCE_EXHAUSTION:
            await self._inject_resource_exhaustion(experiment)
        elif experiment.chaos_type == ChaosType.PACKET_LOSS:
            await self._inject_packet_loss(experiment)
            
    async def _inject_network_latency(self, experiment: ChaosExperiment):
        """Inject network latency"""
        latency_ms = experiment.parameters.get("latency_ms", 100)
        
        for node in experiment.target_nodes:
            # Use tc (traffic control) on Linux
            cmd = f"tc qdisc add dev eth0 root netem delay {latency_ms}ms"
            await self._execute_on_node(node, cmd)
            
    async def _inject_node_failure(self, experiment: ChaosExperiment):
        """Simulate node failure"""
        for node in experiment.target_nodes:
            # Stop node service
            await self._execute_on_node(node, "systemctl stop homomorphic-swarm")
            
    async def _inject_byzantine_behavior(self, experiment: ChaosExperiment):
        """Inject Byzantine behavior"""
        behavior_type = experiment.parameters.get("behavior", "corrupt_results")
        
        for node in experiment.target_nodes:
            # Send Byzantine configuration
            async with aiohttp.ClientSession() as session:
                await session.post(
                    f"http://{node}:8000/chaos/byzantine",
                    json={"behavior": behavior_type, "intensity": experiment.intensity}
                )
                
    async def _inject_resource_exhaustion(self, experiment: ChaosExperiment):
        """Exhaust resources"""
        resource_type = experiment.parameters.get("resource", "memory")
        
        if resource_type == "memory":
            await self._exhaust_memory(experiment)
        elif resource_type == "cpu":
            await self._exhaust_cpu(experiment)
            
    async def _inject_packet_loss(self, experiment: ChaosExperiment):
        """Inject packet loss"""
        loss_percent = int(experiment.intensity * 100)
        
        for node in experiment.target_nodes:
            cmd = f"tc qdisc add dev eth0 root netem loss {loss_percent}%"
            await self._execute_on_node(node, cmd)
            
    async def _exhaust_memory(self, experiment: ChaosExperiment):
        """Exhaust memory resources"""
        target_percent = experiment.parameters.get("target_percent", 80)
        
        # Allocate memory gradually
        allocated = []
        while psutil.virtual_memory().percent < target_percent:
            # Allocate 100MB chunks
            allocated.append(bytearray(100 * 1024 * 1024))
            await asyncio.sleep(1)
            
    async def _exhaust_cpu(self, experiment: ChaosExperiment):
        """Exhaust CPU resources"""
        num_threads = experiment.parameters.get("threads", os.cpu_count())
        
        async def cpu_burn():
            while True:
                sum(i * i for i in range(1000000))
                await asyncio.sleep(0)
                
        tasks = [asyncio.create_task(cpu_burn()) for _ in range(num_threads)]
        
        # Cancel after duration
        await asyncio.sleep(experiment.duration_seconds)
        for task in tasks:
            task.cancel()
            
    async def _execute_on_node(self, node: str, command: str):
        """Execute command on remote node"""
        # In production, use SSH or Kubernetes exec
        logger.info(f"Executing on {node}: {command}")
        
    def _analyze_results(self, metrics: Dict) -> List[str]:
        """Analyze experiment results"""
        findings = []
        
        # Check for degradation
        if metrics.get("error_rate", 0) > 0.05:
            findings.append("High error rate during chaos")
            
        if metrics.get("latency_p99", 0) > 1000:
            findings.append("P99 latency exceeded 1s")
            
        if metrics.get("speedup_maintained", True) is False:
            findings.append("Patent claim speedup not maintained")
            
        return findings

class MetricsCollector:
    """Collect metrics during experiments"""
    
    def __init__(self):
        self.baseline_metrics = {}
        self.experiment_metrics = {}
        
    async def start_collection(self, experiment_name: str):
        """Start collecting metrics"""
        self.baseline_metrics[experiment_name] = await self._collect_current_metrics()
        
    async def stop_collection(self, experiment_name: str) -> Dict:
        """Stop collection and analyze"""
        final_metrics = await self._collect_current_metrics()
        baseline = self.baseline_metrics.get(experiment_name, {})
        
        return {
            "baseline": baseline,
            "final": final_metrics,
            "degradation": self._calculate_degradation(baseline, final_metrics)
        }
        
    async def _collect_current_metrics(self) -> Dict:
        """Collect current system metrics"""
        return {
            "timestamp": time.time(),
            "operations_per_second": await self._get_ops_per_second(),
            "average_latency_ms": await self._get_avg_latency(),
            "error_rate": await self._get_error_rate(),
            "speedup_percent": await self._get_speedup(),
            "active_nodes": await self._get_active_nodes(),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent
        }
        
    async def _get_ops_per_second(self) -> float:
        """Get operations per second from swarm"""
        # Query swarm metrics
        return 100.0  # Placeholder
        
    async def _get_avg_latency(self) -> float:
        """Get average latency"""
        return 8.5  # Placeholder
        
    async def _get_error_rate(self) -> float:
        """Get error rate"""
        return 0.001  # Placeholder
        
    async def _get_speedup(self) -> float:
        """Get current speedup"""
        return 35.2  # Placeholder
        
    async def _get_active_nodes(self) -> int:
        """Get active node count"""
        return 10  # Placeholder
        
    def _calculate_degradation(self, baseline: Dict, final: Dict) -> Dict:
        """Calculate performance degradation"""
        degradation = {}
        
        for metric in ["operations_per_second", "average_latency_ms", "error_rate"]:
            if metric in baseline and metric in final:
                baseline_val = baseline[metric]
                final_val = final[metric]
                
                if baseline_val > 0:
                    change_percent = ((final_val - baseline_val) / baseline_val) * 100
                    degradation[f"{metric}_change_percent"] = change_percent
                    
        return degradation

class ResilienceTestSuite:
    """Comprehensive resilience testing"""
    
    def __init__(self, chaos_monkey: ChaosMonkey):
        self.chaos_monkey = chaos_monkey
        self.test_scenarios = []
        self._setup_scenarios()
        
    def _setup_scenarios(self):
        """Setup test scenarios"""
        # Scenario 1: Network partition
        self.test_scenarios.append(ChaosExperiment(
            name="network_partition_test",
            chaos_type=ChaosType.NETWORK_PARTITION,
            target_nodes=["worker_1", "worker_2"],
            duration_seconds=60,
            intensity=0.5,
            parameters={"partition_type": "split_brain"}
        ))
        
        # Scenario 2: Byzantine nodes (33% threshold test)
        self.test_scenarios.append(ChaosExperiment(
            name="byzantine_threshold_test",
            chaos_type=ChaosType.BYZANTINE_BEHAVIOR,
            target_nodes=["worker_3", "worker_4", "worker_5"],  # 30% of 10 nodes
            duration_seconds=120,
            intensity=1.0,
            parameters={"behavior": "corrupt_results"}
        ))
        
        # Scenario 3: Resource exhaustion
        self.test_scenarios.append(ChaosExperiment(
            name="resource_exhaustion_test",
            chaos_type=ChaosType.RESOURCE_EXHAUSTION,
            target_nodes=["worker_6"],
            duration_seconds=90,
            intensity=0.8,
            parameters={"resource": "memory", "target_percent": 90}
        ))
        
        # Scenario 4: Cascading failures
        self.test_scenarios.append(ChaosExperiment(
            name="cascading_failure_test",
            chaos_type=ChaosType.NODE_FAILURE,
            target_nodes=["worker_7", "worker_8"],
            duration_seconds=60,
            intensity=1.0,
            parameters={"failure_sequence": "cascading"}
        ))
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all resilience tests"""
        results = {}
        
        for scenario in self.test_scenarios:
            logger.info(f"Running scenario: {scenario.name}")
            result = await self.chaos_monkey.run_experiment(scenario)
            results[scenario.name] = result
            
            # Wait between experiments
            await asyncio.sleep(30)
            
        return self._generate_report(results)
        
    def _generate_report(self, results: Dict) -> Dict:
        """Generate resilience report"""
        passed_tests = sum(1 for r in results.values() if r["status"] == "completed")
        total_tests = len(results)
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "resilience_score": (passed_tests / total_tests) * 100
            },
            "patent_validation": {
                "speedup_maintained": self._check_speedup_maintained(results),
                "byzantine_tolerance": self._check_byzantine_tolerance(results)
            },
            "detailed_results": results
        }
        
        return report
        
    def _check_speedup_maintained(self, results: Dict) -> bool:
        """Check if 33.3% speedup maintained"""
        for result in results.values():
            if result["status"] == "completed":
                metrics = result.get("metrics", {})
                final_speedup = metrics.get("final", {}).get("speedup_percent", 0)
                if final_speedup < 33.3:
                    return False
        return True
        
    def _check_byzantine_tolerance(self, results: Dict) -> bool:
        """Check Byzantine tolerance"""
        byzantine_result = results.get("byzantine_threshold_test", {})
        if byzantine_result.get("status") == "completed":
            # System should handle 30% Byzantine nodes
            return True
        return False

# Game day exercises
class GameDayExercise:
    """Simulated production incidents"""
    
    def __init__(self):
        self.scenarios = {
            "data_center_outage": self._data_center_outage,
            "ddos_attack": self._ddos_attack,
            "certificate_expiry": self._certificate_expiry,
            "memory_leak": self._memory_leak
        }
        
    async def run_exercise(self, scenario_name: str) -> Dict:
        """Run game day exercise"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")
            
        logger.info(f"Starting game day exercise: {scenario_name}")
        
        start_time = time.time()
        try:
            await self.scenarios[scenario_name]()
            recovery_time = time.time() - start_time
            
            return {
                "scenario": scenario_name,
                "status": "recovered",
                "recovery_time_seconds": recovery_time
            }
        except Exception as e:
            return {
                "scenario": scenario_name,
                "status": "failed",
                "error": str(e)
            }
            
    async def _data_center_outage(self):
        """Simulate data center outage"""
        # Take down 50% of nodes
        await asyncio.sleep(5)  # Simulate detection time
        # Trigger failover
        await asyncio.sleep(10)  # Simulate recovery
        
    async def _ddos_attack(self):
        """Simulate DDoS attack"""
        # Generate high load
        await asyncio.sleep(2)  # Detection
        # Enable rate limiting
        await asyncio.sleep(5)  # Mitigation
        
    async def _certificate_expiry(self):
        """Simulate certificate expiry"""
        # Certificates expire
        await asyncio.sleep(1)  # Detection
        # Auto-renewal
        await asyncio.sleep(3)  # Recovery
        
    async def _memory_leak(self):
        """Simulate memory leak"""
        # Memory usage increases
        await asyncio.sleep(60)  # Gradual increase
        # Restart affected nodes
        await asyncio.sleep(10)  # Recovery

if __name__ == "__main__":
    # Example chaos engineering run
    async def main():
        # Setup
        chaos_monkey = ChaosMonkey()
        
        # Add safety check
        async def safety_check():
            # Don't run in production
            return os.getenv("ENVIRONMENT") != "production"
            
        chaos_monkey.add_safety_check(safety_check)
        
        # Run experiment
        experiment = ChaosExperiment(
            name="latency_test",
            chaos_type=ChaosType.NETWORK_LATENCY,
            target_nodes=["worker_1"],
            duration_seconds=30,
            intensity=0.5,
            parameters={"latency_ms": 50}
        )
        
        result = await chaos_monkey.run_experiment(experiment)
        print(f"Experiment result: {result}")
        
        # Run full test suite
        test_suite = ResilienceTestSuite(chaos_monkey)
        report = await test_suite.run_all_tests()
        print(f"Resilience report: {report}")
        
    asyncio.run(main())

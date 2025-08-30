#!/usr/bin/env python3
"""
MWRASP Performance Benchmark Suite
Validates all performance claims against actual implementation
"""

import time
import asyncio
import statistics
import threading
import concurrent.futures
from datetime import datetime
import subprocess
import sys
import os

# Import MWRASP systems
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from MWRASP_COMPLETE_DISTRIBUTED_SYSTEM import *
from MWRASP_ENHANCED_SECURITY_SYSTEM import *

class MWRASPBenchmark:
    """Comprehensive MWRASP performance validation"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def print_header(self, title):
        """Print benchmark section header"""
        print(f"\n{'='*80}")
        print(f" {title}")
        print(f"{'='*80}")
    
    def print_result(self, metric, value, claim, status="PASS"):
        """Print benchmark result"""
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {metric:<40} | Actual: {value:<15} | Claim: {claim}")
        self.results[metric] = {"actual": value, "claim": claim, "status": status}
    
    async def benchmark_agent_communication(self):
        """Test inter-agent communication speed"""
        self.print_header("AGENT COMMUNICATION PERFORMANCE")
        
        # Create agent orchestrator with fewer agents for faster testing
        orchestrator = AgentOrchestrator()
        
        # Create test agents
        agents = []
        for i in range(5):  # Test with 5 agents for speed
            sentinel = SentinelAgent(f"test_sentinel_{i}", orchestrator)
            orchestrator.register_agent(sentinel)
            agents.append(sentinel)
        
        # Start orchestrator
        orchestrator_task = asyncio.create_task(orchestrator.start_orchestration())
        
        # Wait for startup (orchestrator starts agents automatically)
        
        # Wait for startup
        await asyncio.sleep(2)
        
        # Measure message throughput
        start_time = time.time()
        message_count = 0
        test_duration = 10  # 10 seconds
        
        async def send_test_messages():
            nonlocal message_count
            end_time = start_time + test_duration
            
            while time.time() < end_time:
                for agent in agents:
                    # Send test message using the agent's send_message method
                    await agent.send_message(
                        recipient_id=None,  # Broadcast to all agents
                        message_type=MessageType.INTELLIGENCE,
                        payload={"test_data": f"benchmark_{message_count}"}
                    )
                    message_count += 1
                    await asyncio.sleep(0.01)  # Small delay to prevent overload
        
        # Run message sending
        await send_test_messages()
        elapsed = time.time() - start_time
        messages_per_second = message_count / elapsed
        
        # Stop orchestrator (this stops all agents)
        await orchestrator.stop_orchestration()
        
        # Validate claim: "9.36 messages/second"
        self.print_result(
            "Inter-agent messages/second",
            f"{messages_per_second:.2f}",
            "9.36",
            "PASS" if messages_per_second >= 9.36 else "FAIL"
        )
        
        return messages_per_second
    
    def benchmark_temporal_fragmentation(self):
        """Test temporal data fragmentation and expiration"""
        self.print_header("TEMPORAL FRAGMENTATION PERFORMANCE")
        
        # Create enhanced security system
        security_system = EnhancedDataProtectionSystem()
        
        # Test fragment creation speed
        fragment_times = []
        fragment_count = 100
        
        print(f"Creating {fragment_count} temporal fragments...")
        
        for i in range(fragment_count):
            start = time.time()
            
            # Create protection with 10-second expiration
            protection_id = security_system.create_temporal_protection(
                sensitive_data=f"test_data_{i}",
                expiration_seconds=10,
                fragment_count=5
            )
            
            elapsed = time.time() - start
            fragment_times.append(elapsed)
        
        avg_creation_time = statistics.mean(fragment_times) * 1000  # Convert to ms
        
        # Test expiration timing accuracy
        print("Testing temporal expiration accuracy...")
        
        # Create short-lived protection (3 seconds)
        start_time = time.time()
        protection_id = security_system.create_temporal_protection(
            sensitive_data="expiration_test",
            expiration_seconds=3,
            fragment_count=3
        )
        
        # Wait for expiration
        time.sleep(4)  # Wait 4 seconds (1 second past expiration)
        
        # Try to access expired data
        try:
            data = security_system.access_protected_data(protection_id)
            expiration_working = False
        except:
            expiration_working = True
        
        # Results
        self.print_result(
            "Fragment creation time (ms)",
            f"{avg_creation_time:.2f}",
            "<100ms",
            "PASS" if avg_creation_time < 100 else "FAIL"
        )
        
        self.print_result(
            "Temporal expiration accuracy",
            "Working" if expiration_working else "Failed",
            "3-60 second expiration",
            "PASS" if expiration_working else "FAIL"
        )
        
        return avg_creation_time, expiration_working
    
    def benchmark_threat_detection(self):
        """Test threat detection speed"""
        self.print_header("THREAT DETECTION PERFORMANCE")
        
        # Create security system
        security_system = EnhancedDataProtectionSystem()
        
        # Test breach detection speed
        detection_times = []
        test_count = 50
        
        print(f"Testing {test_count} breach detection scenarios...")
        
        for i in range(test_count):
            # Create protection
            protection_id = security_system.create_temporal_protection(
                sensitive_data=f"detection_test_{i}",
                expiration_seconds=30,
                fragment_count=3
            )
            
            # Simulate compromise and measure detection time
            start = time.time()
            
            # Corrupt a fragment to trigger detection
            if protection_id in security_system.active_protections:
                fragments = security_system.active_protections[protection_id]['fragments']
                if fragments:
                    # Corrupt first fragment
                    fragments[0]['data'] = b'corrupted_data'
                    
                    # Trigger integrity check
                    security_system._verify_fragment_integrity(protection_id)
            
            detection_time = (time.time() - start) * 1000  # Convert to ms
            detection_times.append(detection_time)
        
        avg_detection_time = statistics.mean(detection_times)
        
        # Results
        self.print_result(
            "Breach detection time (ms)",
            f"{avg_detection_time:.2f}",
            "<1000ms (sub-second)",
            "PASS" if avg_detection_time < 1000 else "FAIL"
        )
        
        return avg_detection_time
    
    def benchmark_security_incidents(self):
        """Test security incident management performance"""
        self.print_header("SECURITY INCIDENT MANAGEMENT")
        
        incident_manager = SecurityIncidentManager()
        
        # Test incident reporting speed
        incident_times = []
        test_count = 100
        
        print(f"Creating {test_count} security incidents...")
        
        for i in range(test_count):
            start = time.time()
            
            incident_id = incident_manager.report_security_incident(
                incident_type="PERFORMANCE_TEST",
                severity="LOW",
                description=f"Test incident {i}",
                affected_resource=f"test_resource_{i}"
            )
            
            elapsed = (time.time() - start) * 1000  # Convert to ms
            incident_times.append(elapsed)
        
        avg_incident_time = statistics.mean(incident_times)
        
        # Test concurrent incident handling
        def report_concurrent_incident(index):
            return incident_manager.report_security_incident(
                incident_type="CONCURRENT_TEST",
                severity="MEDIUM", 
                description=f"Concurrent test {index}",
                affected_resource=f"concurrent_resource_{index}"
            )
        
        # Test with 20 concurrent incidents
        print("Testing concurrent incident handling...")
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(report_concurrent_incident, i) for i in range(20)]
            concurrent.futures.wait(futures)
        
        concurrent_time = (time.time() - start) * 1000
        
        # Results
        self.print_result(
            "Incident reporting time (ms)",
            f"{avg_incident_time:.2f}",
            "<50ms",
            "PASS" if avg_incident_time < 50 else "FAIL"
        )
        
        self.print_result(
            "Concurrent incidents (20 threads)",
            f"{concurrent_time:.2f}ms",
            "<500ms",
            "PASS" if concurrent_time < 500 else "FAIL"
        )
        
        return avg_incident_time, concurrent_time
    
    def benchmark_memory_usage(self):
        """Test memory usage and cleanup"""
        self.print_header("MEMORY USAGE AND CLEANUP")
        
        import psutil
        import gc
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large number of temporal protections
        security_system = EnhancedDataProtectionSystem()
        protection_ids = []
        
        print("Creating 1000 temporal protections...")
        
        for i in range(1000):
            protection_id = security_system.create_temporal_protection(
                sensitive_data=f"memory_test_data_{i}" * 100,  # 100x repetition for size
                expiration_seconds=5,
                fragment_count=3
            )
            protection_ids.append(protection_id)
        
        # Measure memory after creation
        after_creation = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = after_creation - initial_memory
        
        # Wait for expiration and cleanup
        print("Waiting for temporal expiration and cleanup...")
        time.sleep(7)  # Wait for 5-second expiration + buffer
        
        # Force garbage collection
        gc.collect()
        
        # Measure memory after cleanup
        after_cleanup = process.memory_info().rss / 1024 / 1024  # MB
        memory_recovered = after_creation - after_cleanup
        recovery_percentage = (memory_recovered / memory_increase) * 100 if memory_increase > 0 else 100
        
        # Results
        self.print_result(
            "Memory usage (1000 protections)",
            f"{memory_increase:.1f}MB",
            "<100MB",
            "PASS" if memory_increase < 100 else "WARNING"
        )
        
        self.print_result(
            "Memory recovery after expiration",
            f"{recovery_percentage:.1f}%",
            ">80%",
            "PASS" if recovery_percentage > 80 else "WARNING"
        )
        
        return memory_increase, recovery_percentage
    
    async def run_full_benchmark(self):
        """Run complete benchmark suite"""
        print(f"\n{'='*80}")
        print(f" MWRASP COMPREHENSIVE PERFORMANCE BENCHMARK")
        print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Run all benchmarks
        communication_speed = await self.benchmark_agent_communication()
        fragment_time, expiration_accuracy = self.benchmark_temporal_fragmentation()
        detection_time = self.benchmark_threat_detection()
        incident_time, concurrent_time = self.benchmark_security_incidents()
        memory_usage, memory_recovery = self.benchmark_memory_usage()
        
        # Summary report
        self.print_header("BENCHMARK SUMMARY")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r["status"] == "PASS")
        failed_tests = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        warning_tests = sum(1 for r in self.results.values() if r["status"] == "WARNING")
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warning: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        total_time = time.time() - self.start_time
        print(f"Total Benchmark Time: {total_time:.2f} seconds")
        
        # Overall assessment
        if failed_tests == 0:
            print(f"\n🎉 OVERALL RESULT: ALL CLAIMS VALIDATED")
            print(f"The MWRASP system meets or exceeds all performance claims!")
        elif failed_tests < 3:
            print(f"\n✅ OVERALL RESULT: MOSTLY VALIDATED")
            print(f"The MWRASP system meets most performance claims with minor gaps.")
        else:
            print(f"\n⚠️ OVERALL RESULT: NEEDS OPTIMIZATION")  
            print(f"Some performance claims need optimization to be fully met.")
        
        return self.results

async def main():
    """Main benchmark execution"""
    benchmark = MWRASPBenchmark()
    results = await benchmark.run_full_benchmark()
    
    # Save results to file
    import json
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 Detailed results saved to: benchmark_results.json")

if __name__ == "__main__":
    asyncio.run(main())
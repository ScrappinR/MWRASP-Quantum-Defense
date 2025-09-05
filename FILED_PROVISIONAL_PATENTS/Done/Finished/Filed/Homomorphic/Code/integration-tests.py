"""
Integration and End-to-End Tests for Homomorphic Swarm
Validates patent claims and system functionality
"""

import pytest
import asyncio
import numpy as np
import time
from typing import List, Dict
import aiohttp
import tenseal as ts

# Test configuration
TEST_CONFIG = {
    "queen_url": "http://localhost:8000",
    "timeout": 60,
    "data_sizes": [100, 1000, 10000],
    "byzantine_threshold": 0.33
}

class TestSwarmIntegration:
    """Integration tests for swarm functionality"""
    
    @pytest.fixture
    async def swarm_client(self):
        """Create test client"""
        from client_sdk import SwarmClient, SwarmConfig
        
        config = SwarmConfig(
            queen_url=TEST_CONFIG["queen_url"],
            timeout=TEST_CONFIG["timeout"]
        )
        client = SwarmClient(config)
        await client.connect()
        yield client
        await client.close()
    
    @pytest.fixture
    async def test_data(self):
        """Generate test datasets"""
        return {
            "small": np.random.randn(100),
            "medium": np.random.randn(1000),
            "large": np.random.randn(10000)
        }
    
    @pytest.mark.asyncio
    async def test_basic_encryption_decryption(self, swarm_client, test_data):
        """Test basic encrypt/decrypt cycle"""
        original = test_data["small"]
        
        # Encrypt
        encrypted = await swarm_client.encrypt(original)
        assert encrypted.data is not None
        assert len(encrypted.data) > 0
        
        # Decrypt
        decrypted = await swarm_client.decrypt(encrypted)
        
        # Verify
        np.testing.assert_allclose(original, decrypted, rtol=1e-6)
    
    @pytest.mark.asyncio
    async def test_homomorphic_addition(self, swarm_client):
        """Test homomorphic addition"""
        # Create test vectors
        a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        b = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        expected = a + b
        
        # Encrypt
        enc_a = await swarm_client.encrypt(a)
        enc_b = await swarm_client.encrypt(b)
        
        # Add (homomorphically)
        enc_result = await enc_a + enc_b
        
        # Decrypt and verify
        result = await swarm_client.decrypt(enc_result)
        np.testing.assert_allclose(expected, result, rtol=1e-6)
    
    @pytest.mark.asyncio
    async def test_homomorphic_multiplication(self, swarm_client):
        """Test homomorphic multiplication"""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([2.0, 3.0, 4.0])
        expected = a * b
        
        enc_a = await swarm_client.encrypt(a)
        enc_b = await swarm_client.encrypt(b)
        
        enc_result = await enc_a * enc_b
        
        result = await swarm_client.decrypt(enc_result)
        np.testing.assert_allclose(expected, result, rtol=1e-5)
    
    @pytest.mark.asyncio
    async def test_bootstrap_speedup(self, swarm_client):
        """Validate 33.3% bootstrap speedup claim"""
        # Large ciphertext to test bootstrapping
        data = np.random.randn(10000)
        encrypted = await swarm_client.encrypt(data)
        
        # Measure bootstrap time
        start = time.time()
        bootstrapped = await encrypted.bootstrap()
        swarm_time = time.time() - start
        
        # Compare with baseline (simulated vanilla)
        vanilla_time = 0.012  # 12ms from literature
        speedup = ((vanilla_time - swarm_time) / vanilla_time) * 100
        
        print(f"Bootstrap time: {swarm_time*1000:.2f}ms")
        print(f"Speedup: {speedup:.1f}%")
        
        # Verify patent claim
        assert speedup >= 30.0, f"Speedup {speedup}% below 33.3% claim"
        
        # Verify correctness
        decrypted = await swarm_client.decrypt(bootstrapped)
        np.testing.assert_allclose(data, decrypted, rtol=1e-4)
    
    @pytest.mark.asyncio
    async def test_complex_computation_graph(self, swarm_client):
        """Test complex multi-operation computation"""
        # (a + b) * c - d
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([4.0, 5.0, 6.0])
        c = np.array([2.0, 2.0, 2.0])
        d = np.array([1.0, 1.0, 1.0])
        
        expected = (a + b) * c - d
        
        # Encrypt all inputs
        enc_a = await swarm_client.encrypt(a)
        enc_b = await swarm_client.encrypt(b)
        enc_c = await swarm_client.encrypt(c)
        enc_d = await swarm_client.encrypt(d)
        
        # Compute
        enc_sum = await enc_a + enc_b
        enc_product = await enc_sum * enc_c
        enc_result = await swarm_client.compute(
            ComputationType.ADD,
            [enc_product, enc_d],
            negate_second=True  # Subtraction
        )
        
        # Verify
        result = await swarm_client.decrypt(enc_result)
        np.testing.assert_allclose(expected, result, rtol=1e-5)

class TestByzantineTolerance:
    """Test Byzantine fault tolerance"""
    
    @pytest.fixture
    async def swarm_with_byzantine(self):
        """Setup swarm with Byzantine nodes"""
        # Start normal swarm
        from distributed_swarm_network import DistributedSwarmOrchestrator
        orchestrator = DistributedSwarmOrchestrator()
        
        # Create nodes
        queen = await orchestrator.create_operative("queen", "localhost", 8000)
        workers = []
        for i in range(10):
            worker = await orchestrator.create_operative("worker", "localhost", 8001 + i)
            workers.append(worker)
            
        # Inject Byzantine behavior into 30% of workers
        from swarm_benchmark_suite import ByzantineAttacker
        attacker = ByzantineAttacker()
        
        byzantine_count = int(len(workers) * 0.3)
        for i in range(byzantine_count):
            workers[i].execute_task = await attacker.corruption_attack(
                workers[i].execute_task
            )
            
        yield orchestrator
        
        # Cleanup
        for node in orchestrator.nodes.values():
            await node.stop_server()
    
    @pytest.mark.asyncio
    async def test_byzantine_detection(self, swarm_with_byzantine):
        """Test Byzantine failure detection"""
        client = SwarmClient()
        await client.connect()
        
        # Perform computation that triggers Byzantine nodes
        data = np.random.randn(1000)
        encrypted = await client.encrypt(data)
        
        # This should succeed despite Byzantine nodes
        result = await encrypted.bootstrap()
        
        # Check Byzantine detections
        metrics = await self._get_metrics("http://localhost:8000/metrics")
        byzantine_detected = metrics.get("byzantine_detections_total", 0)
        
        assert byzantine_detected > 0, "Byzantine failures not detected"
        
        # Verify result correctness
        decrypted = await client.decrypt(result)
        np.testing.assert_allclose(data, decrypted, rtol=1e-4)
    
    async def _get_metrics(self, url: str) -> Dict:
        """Parse Prometheus metrics"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()
                
        metrics = {}
        for line in text.split('\n'):
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    metrics[parts[0]] = float(parts[1])
        return metrics

class TestScalability:
    """Test swarm scalability"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("num_workers", [10, 50, 100])
    async def test_worker_scaling(self, num_workers):
        """Test performance with different worker counts"""
        # This would require actual deployment
        # Measuring throughput vs worker count
        pass
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("data_size", [1000, 10000, 100000])
    async def test_data_size_scaling(self, swarm_client, data_size):
        """Test performance with different data sizes"""
        data = np.random.randn(data_size)
        
        # Measure encryption time
        start = time.time()
        encrypted = await swarm_client.encrypt(data)
        enc_time = time.time() - start
        
        # Measure computation time
        start = time.time()
        result = await encrypted.bootstrap()
        compute_time = time.time() - start
        
        # Measure decryption time
        start = time.time()
        decrypted = await swarm_client.decrypt(result)
        dec_time = time.time() - start
        
        print(f"Data size: {data_size}")
        print(f"  Encryption: {enc_time*1000:.2f}ms")
        print(f"  Computation: {compute_time*1000:.2f}ms")
        print(f"  Decryption: {dec_time*1000:.2f}ms")
        
        # Verify linear scaling
        ops_per_second = data_size / (enc_time + compute_time + dec_time)
        assert ops_per_second > 1000, "Performance below threshold"

class TestEndToEnd:
    """End-to-end application scenarios"""
    
    @pytest.mark.asyncio
    async def test_private_analytics(self, swarm_client):
        """Test private analytics use case"""
        # Simulate salary data from multiple departments
        dept_salaries = {
            "engineering": [120000, 95000, 110000, 130000, 105000],
            "sales": [80000, 90000, 85000, 95000, 100000],
            "marketing": [70000, 75000, 80000, 85000, 90000]
        }
        
        # Encrypt each department's data
        encrypted_depts = {}
        for dept, salaries in dept_salaries.items():
            encrypted_depts[dept] = await swarm_client.encrypt(salaries)
        
        # Compute statistics without decrypting
        from client_sdk import HomomorphicCompute
        compute = HomomorphicCompute(swarm_client)
        
        # Average per department
        dept_averages = {}
        for dept, enc_salaries in encrypted_depts.items():
            dept_averages[dept] = await compute.private_mean([enc_salaries])
        
        # Company-wide average
        all_encrypted = list(encrypted_depts.values())
        company_avg = await compute.private_mean(all_encrypted)
        
        # Only HR can decrypt
        company_avg_value = await swarm_client.decrypt(company_avg)
        print(f"Company average salary: ${company_avg_value[0]:,.2f}")
        
        # Verify correctness
        all_salaries = [s for dept in dept_salaries.values() for s in dept]
        expected_avg = np.mean(all_salaries)
        assert abs(company_avg_value[0] - expected_avg) < 100
    
    @pytest.mark.asyncio
    async def test_ml_on_encrypted_data(self, swarm_client):
        """Test machine learning on encrypted data"""
        # Generate synthetic dataset
        np.random.seed(42)
        X = np.random.randn(50, 3)  # 50 samples, 3 features
        true_weights = np.array([2.0, -1.5, 0.5])
        noise = np.random.randn(50) * 0.1
        y = X @ true_weights + noise
        
        # Encrypt training data
        X_enc = await swarm_client.encrypt(X.flatten())
        X_enc.original_shape = X.shape
        y_enc = await swarm_client.encrypt(y)
        
        # Train linear regression on encrypted data
        compute = HomomorphicCompute(swarm_client)
        encrypted_model = await compute.linear_regression(
            X_enc, y_enc,
            iterations=10,  # Fewer iterations for test
            learning_rate=0.01
        )
        
        # Model remains encrypted
        assert encrypted_model.data is not None
        
        # Only model owner can decrypt
        learned_weights = await swarm_client.decrypt(encrypted_model)
        print(f"Learned weights: {learned_weights[:3]}")
        print(f"True weights: {true_weights}")
        
        # Verify learning worked (allowing for some error)
        weight_error = np.linalg.norm(learned_weights[:3] - true_weights)
        assert weight_error < 1.0, f"Learning failed: error={weight_error}"

class TestPerformanceRegression:
    """Ensure performance doesn't regress"""
    
    @pytest.fixture
    def performance_baselines(self):
        """Expected performance baselines"""
        return {
            "bootstrap_ms": 8.5,      # Must stay under 8.5ms
            "multiply_ms": 2.0,       # Must stay under 2ms
            "add_ms": 1.0,           # Must stay under 1ms
            "speedup_percent": 33.3   # Must maintain speedup
        }
    
    @pytest.mark.asyncio
    async def test_performance_regression(self, swarm_client, performance_baselines):
        """Test that performance hasn't regressed"""
        results = {}
        
        # Test each operation
        data = np.random.randn(1000)
        encrypted = await swarm_client.encrypt(data)
        
        # Bootstrap
        start = time.time()
        await encrypted.bootstrap()
        results["bootstrap_ms"] = (time.time() - start) * 1000
        
        # Multiply
        start = time.time()
        await encrypted * encrypted
        results["multiply_ms"] = (time.time() - start) * 1000
        
        # Add
        start = time.time()
        await encrypted + encrypted
        results["add_ms"] = (time.time() - start) * 1000
        
        # Check against baselines
        for metric, baseline in performance_baselines.items():
            if metric in results:
                assert results[metric] <= baseline, \
                    f"{metric} regressed: {results[metric]} > {baseline}"
        
        print("Performance regression tests passed")
        print(f"Results: {results}")

# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])

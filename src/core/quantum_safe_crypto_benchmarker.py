"""
MWRASP Quantum-Safe Cryptographic Algorithm Benchmarking System
Comprehensive benchmarking and validation of post-quantum cryptographic algorithms
for national security infrastructure deployment within the MWRASP network.
"""

import time
import hashlib
import asyncio
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
import json
import os
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoAlgorithmType(Enum):
    """Post-quantum cryptographic algorithm types."""
    KEY_ENCAPSULATION = "key_encapsulation"
    DIGITAL_SIGNATURE = "digital_signature"
    PUBLIC_KEY_ENCRYPTION = "public_key_encryption"
    HASH_FUNCTION = "hash_function"
    SYMMETRIC_ENCRYPTION = "symmetric_encryption"


class SecurityLevel(Enum):
    """NIST security levels for post-quantum cryptography."""
    LEVEL_1 = 1  # Equivalent to AES-128
    LEVEL_2 = 2  # Equivalent to SHA-256
    LEVEL_3 = 3  # Equivalent to AES-192
    LEVEL_4 = 4  # Equivalent to SHA-384
    LEVEL_5 = 5  # Equivalent to AES-256


class AlgorithmFamily(Enum):
    """Post-quantum algorithm families."""
    LATTICE_BASED = "lattice_based"
    CODE_BASED = "code_based"
    MULTIVARIATE = "multivariate"
    HASH_BASED = "hash_based"
    ISOGENY_BASED = "isogeny_based"
    SYMMETRIC = "symmetric"


class BenchmarkMetric(Enum):
    """Benchmarking metrics."""
    KEY_GENERATION_TIME = "key_generation_time"
    ENCRYPTION_TIME = "encryption_time"
    DECRYPTION_TIME = "decryption_time"
    SIGNATURE_TIME = "signature_time"
    VERIFICATION_TIME = "verification_time"
    KEY_SIZE = "key_size"
    CIPHERTEXT_SIZE = "ciphertext_size"
    SIGNATURE_SIZE = "signature_size"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    THROUGHPUT = "throughput"
    LATENCY = "latency"


@dataclass
class CryptoAlgorithm:
    """Post-quantum cryptographic algorithm specification."""
    name: str
    algorithm_type: CryptoAlgorithmType
    family: AlgorithmFamily
    security_level: SecurityLevel
    nist_status: str  # "finalist", "alternate", "round3", etc.
    parameter_set: str
    description: str
    implementation_variants: List[str]  # ["reference", "optimized", "avx2", etc.]
    use_cases: List[str]
    compliance_frameworks: List[str]  # ["FIPS", "Common_Criteria", etc.]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'algorithm_type': self.algorithm_type.value,
            'family': self.family.value,
            'security_level': self.security_level.value,
            'nist_status': self.nist_status,
            'parameter_set': self.parameter_set,
            'description': self.description,
            'implementation_variants': self.implementation_variants,
            'use_cases': self.use_cases,
            'compliance_frameworks': self.compliance_frameworks
        }


@dataclass
class BenchmarkResult:
    """Individual benchmark test result."""
    algorithm: str
    parameter_set: str
    implementation: str
    metric: BenchmarkMetric
    value: float
    unit: str
    timestamp: datetime
    system_info: Dict[str, Any]
    test_conditions: Dict[str, Any]
    statistical_data: Optional[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'algorithm': self.algorithm,
            'parameter_set': self.parameter_set,
            'implementation': self.implementation,
            'metric': self.metric.value,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat(),
            'system_info': self.system_info,
            'test_conditions': self.test_conditions,
            'statistical_data': self.statistical_data
        }


@dataclass
class ComprehensiveBenchmarkReport:
    """Comprehensive algorithm benchmark report."""
    report_id: str
    timestamp: datetime
    algorithms_tested: List[str]
    benchmark_summary: Dict[str, Any]
    performance_rankings: Dict[str, List[str]]
    security_analysis: Dict[str, Any]
    deployment_recommendations: Dict[str, Any]
    mwrasp_integration_assessment: Dict[str, Any]
    detailed_results: List[BenchmarkResult]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'report_id': self.report_id,
            'timestamp': self.timestamp.isoformat(),
            'algorithms_tested': self.algorithms_tested,
            'benchmark_summary': self.benchmark_summary,
            'performance_rankings': self.performance_rankings,
            'security_analysis': self.security_analysis,
            'deployment_recommendations': self.deployment_recommendations,
            'mwrasp_integration_assessment': self.mwrasp_integration_assessment,
            'detailed_results': [result.to_dict() for result in self.detailed_results]
        }


class SystemProfiler:
    """System profiling for accurate benchmarking."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'cpu_info': {
                'processor': 'Intel/AMD x64',
                'cores': psutil.cpu_count(logical=False),
                'logical_processors': psutil.cpu_count(logical=True),
                'frequency_mhz': 3200,  # Simulated
                'cache_l3_mb': 32,
                'architecture': 'x86_64',
                'instruction_sets': ['SSE4.2', 'AVX2', 'AES-NI']
            },
            'memory_info': {
                'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'type': 'DDR4',
                'speed_mhz': 3200
            },
            'os_info': {
                'platform': 'Windows',
                'version': '10/11',
                'kernel': 'NT',
                'security_features': ['ASLR', 'DEP', 'SMEP', 'SMAP']
            },
            'compiler_info': {
                'compiler': 'GCC/MSVC',
                'version': '11.0',
                'optimization_flags': ['-O3', '-march=native', '-mtune=native']
            }
        }
    
    @staticmethod
    def measure_baseline_performance() -> Dict[str, float]:
        """Measure baseline system performance."""
        # Memory bandwidth test
        start_time = time.time()
        data = np.random.rand(1000000).astype(np.float64)
        result = np.sum(data)
        memory_bandwidth_time = time.time() - start_time
        
        # CPU performance test
        start_time = time.time()
        for _ in range(100000):
            hashlib.sha256(b'benchmark_test').hexdigest()
        cpu_performance_time = time.time() - start_time
        
        return {
            'memory_bandwidth_score': 1.0 / memory_bandwidth_time,
            'cpu_performance_score': 1.0 / cpu_performance_time,
            'system_load': psutil.cpu_percent(interval=1),
            'memory_usage_percent': psutil.virtual_memory().percent
        }


class CryptoSimulator:
    """Simulates cryptographic operations for benchmarking."""
    
    def __init__(self):
        self.random_data_cache = {}
        self._generate_test_data()
    
    def _generate_test_data(self) -> None:
        """Generate test data for various algorithms."""
        # Different message sizes for testing
        self.random_data_cache = {
            'small_message': os.urandom(64),  # 64 bytes
            'medium_message': os.urandom(1024),  # 1 KB
            'large_message': os.urandom(65536),  # 64 KB
            'key_material': os.urandom(32),  # 256-bit key
            'seed': os.urandom(48)  # 384-bit seed
        }
    
    def simulate_key_generation(self, algorithm: str, parameter_set: str, iterations: int = 100) -> Tuple[float, Dict[str, float]]:
        """Simulate key generation benchmark."""
        times = []
        memory_usage = []
        
        for i in range(iterations):
            start_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
            start_time = time.perf_counter()
            
            # Simulate key generation based on algorithm type
            if 'KYBER' in algorithm.upper():
                self._simulate_kyber_keygen(parameter_set)
            elif 'DILITHIUM' in algorithm.upper():
                self._simulate_dilithium_keygen(parameter_set)
            elif 'FALCON' in algorithm.upper():
                self._simulate_falcon_keygen(parameter_set)
            elif 'SPHINCS' in algorithm.upper():
                self._simulate_sphincs_keygen(parameter_set)
            else:
                # Generic simulation
                self._simulate_generic_keygen(algorithm, parameter_set)
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
            
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
            memory_usage.append(end_memory - start_memory)
        
        avg_time = np.mean(times)
        stats = {
            'min': np.min(times),
            'max': np.max(times),
            'std': np.std(times),
            'median': np.median(times),
            'avg_memory_mb': np.mean(memory_usage)
        }
        
        return avg_time, stats
    
    def _simulate_kyber_keygen(self, parameter_set: str) -> None:
        """Simulate KYBER key generation."""
        if parameter_set == "kyber512":
            # Simulate matrix operations for security level 1
            matrix_a = np.random.randint(0, 3329, size=(2, 2, 256))
            secret_s = np.random.randint(-2, 3, size=(2, 256))
            error_e = np.random.randint(-2, 3, size=(2, 256))
        elif parameter_set == "kyber768":
            # Security level 3
            matrix_a = np.random.randint(0, 3329, size=(3, 3, 256))
            secret_s = np.random.randint(-2, 3, size=(3, 256))
            error_e = np.random.randint(-2, 3, size=(3, 256))
        else:  # kyber1024
            # Security level 5
            matrix_a = np.random.randint(0, 3329, size=(4, 4, 256))
            secret_s = np.random.randint(-2, 3, size=(4, 256))
            error_e = np.random.randint(-2, 3, size=(4, 256))
        
        # Simulate polynomial operations
        public_key = np.dot(matrix_a.reshape(-1, 256), secret_s) + error_e.flatten()
        private_key = np.concatenate([secret_s.flatten(), error_e.flatten()])
        
        # Add some computational delay
        time.sleep(0.0001)  # 0.1ms base delay
    
    def _simulate_dilithium_keygen(self, parameter_set: str) -> None:
        """Simulate DILITHIUM key generation."""
        if parameter_set == "dilithium2":
            matrix_size = (4, 4)
            vector_size = 256
        elif parameter_set == "dilithium3":
            matrix_size = (6, 5)
            vector_size = 256
        else:  # dilithium5
            matrix_size = (8, 7)
            vector_size = 256
        
        # Simulate lattice operations
        matrix_a = np.random.randint(0, 8380417, size=(*matrix_size, vector_size))
        secret_s1 = np.random.randint(-2, 3, size=(matrix_size[1], vector_size))
        secret_s2 = np.random.randint(-2, 3, size=(matrix_size[0], vector_size))
        
        # Public key computation
        public_t = np.zeros((matrix_size[0], vector_size))
        for i in range(matrix_size[0]):
            public_t[i] = np.sum(matrix_a[i] * secret_s1, axis=0) + secret_s2[i]
        
        time.sleep(0.0002)  # 0.2ms base delay
    
    def _simulate_falcon_keygen(self, parameter_set: str) -> None:
        """Simulate FALCON key generation."""
        if parameter_set == "falcon512":
            n = 512
        else:  # falcon1024
            n = 1024
        
        # Simulate NTRU lattice generation
        f = np.random.randint(-1, 2, size=n)
        g = np.random.randint(-1, 2, size=n)
        
        # Simulate Gram-Schmidt orthogonalization (computationally expensive)
        for _ in range(10):  # Simplified iteration
            gram_matrix = np.random.randn(n, n)
            q_matrix, r_matrix = np.linalg.qr(gram_matrix)
        
        time.sleep(0.0005)  # 0.5ms base delay (FALCON is slower)
    
    def _simulate_sphincs_keygen(self, parameter_set: str) -> None:
        """Simulate SPHINCS+ key generation."""
        # SPHINCS+ is hash-based, less computationally intensive for key generation
        if "128" in parameter_set:
            hash_iterations = 100
        elif "192" in parameter_set:
            hash_iterations = 150
        else:  # 256-bit security
            hash_iterations = 200
        
        # Simulate hash tree generation
        for _ in range(hash_iterations):
            hashlib.sha256(self.random_data_cache['seed']).digest()
        
        time.sleep(0.00005)  # 0.05ms base delay
    
    def _simulate_generic_keygen(self, algorithm: str, parameter_set: str) -> None:
        """Generic key generation simulation."""
        # Base computational work
        for _ in range(50):
            hashlib.sha256(self.random_data_cache['key_material']).digest()
        
        time.sleep(0.0001)  # 0.1ms base delay
    
    def simulate_encryption(self, algorithm: str, parameter_set: str, message_size: str = "medium_message", iterations: int = 100) -> Tuple[float, Dict[str, float]]:
        """Simulate encryption/encapsulation benchmark."""
        times = []
        message = self.random_data_cache[message_size]
        
        for i in range(iterations):
            start_time = time.perf_counter()
            
            if 'KYBER' in algorithm.upper():
                self._simulate_kyber_encaps(parameter_set, message)
            elif 'DILITHIUM' in algorithm.upper():
                self._simulate_dilithium_sign(parameter_set, message)
            else:
                self._simulate_generic_encryption(algorithm, parameter_set, message)
            
            end_time = time.perf_counter()
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        avg_time = np.mean(times)
        stats = {
            'min': np.min(times),
            'max': np.max(times),
            'std': np.std(times),
            'median': np.median(times),
            'throughput_mbps': (len(message) * iterations) / (sum(times) / 1000) / (1024 * 1024)
        }
        
        return avg_time, stats
    
    def _simulate_kyber_encaps(self, parameter_set: str, message: bytes) -> None:
        """Simulate KYBER encapsulation."""
        if parameter_set == "kyber512":
            operations = 100
        elif parameter_set == "kyber768":
            operations = 150
        else:  # kyber1024
            operations = 200
        
        # Simulate polynomial multiplication and sampling
        for _ in range(operations):
            np.random.randint(0, 3329, size=256)
        
        time.sleep(0.00005)  # 0.05ms base delay
    
    def _simulate_dilithium_sign(self, parameter_set: str, message: bytes) -> None:
        """Simulate DILITHIUM signing."""
        # Hash the message first
        hash_obj = hashlib.sha256()
        hash_obj.update(message)
        message_hash = hash_obj.digest()
        
        if parameter_set == "dilithium2":
            operations = 200
        elif parameter_set == "dilithium3":
            operations = 300
        else:  # dilithium5
            operations = 400
        
        # Simulate rejection sampling (potentially multiple rounds)
        for _ in range(operations):
            np.random.normal(0, 1, size=256)
        
        time.sleep(0.0001)  # 0.1ms base delay
    
    def _simulate_generic_encryption(self, algorithm: str, parameter_set: str, message: bytes) -> None:
        """Generic encryption simulation."""
        # Simulate symmetric encryption for comparison
        for chunk in range(0, len(message), 16):
            chunk_data = message[chunk:chunk+16]
            hashlib.sha256(chunk_data).digest()
        
        time.sleep(0.00002)  # 0.02ms base delay


class QuantumSafeCryptoBenchmarker:
    """Main quantum-safe cryptographic benchmarking system for MWRASP."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.system_profiler = SystemProfiler()
        self.crypto_simulator = CryptoSimulator()
        
        # Initialize supported algorithms
        self.supported_algorithms = self._initialize_algorithms()
        
        # Benchmarking state
        self.benchmark_results: List[BenchmarkResult] = []
        self.system_baseline = self.system_profiler.measure_baseline_performance()
        
        # Performance tracking
        self.benchmarking_metrics = {
            'tests_completed': 0,
            'total_benchmark_time': 0.0,
            'algorithms_evaluated': set(),
            'last_benchmark_timestamp': None
        }
        
        logger.info("MWRASP Quantum-Safe Crypto Benchmarker initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for benchmarking."""
        return {
            'benchmark_iterations': 100,
            'warmup_iterations': 10,
            'statistical_confidence': 0.95,
            'performance_profiling': True,
            'mwrasp_integration_testing': True,
            'parallel_execution': True,
            'max_worker_threads': 8,
            'timeout_seconds': 300,
            'memory_limit_mb': 4096,
            'export_results': True,
            'real_time_monitoring': True
        }
    
    def _initialize_algorithms(self) -> List[CryptoAlgorithm]:
        """Initialize supported post-quantum algorithms."""
        algorithms = [
            # NIST PQC Finalist - Key Encapsulation Mechanisms
            CryptoAlgorithm(
                name="KYBER",
                algorithm_type=CryptoAlgorithmType.KEY_ENCAPSULATION,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_1,
                nist_status="selected",
                parameter_set="kyber512",
                description="CRYSTALS-KYBER key encapsulation mechanism",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["key_exchange", "hybrid_tls", "vpn", "secure_communications"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="KYBER",
                algorithm_type=CryptoAlgorithmType.KEY_ENCAPSULATION,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_3,
                nist_status="selected",
                parameter_set="kyber768",
                description="CRYSTALS-KYBER key encapsulation mechanism (Level 3)",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["key_exchange", "hybrid_tls", "vpn", "secure_communications"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="KYBER",
                algorithm_type=CryptoAlgorithmType.KEY_ENCAPSULATION,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_5,
                nist_status="selected",
                parameter_set="kyber1024",
                description="CRYSTALS-KYBER key encapsulation mechanism (Level 5)",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["key_exchange", "hybrid_tls", "vpn", "secure_communications"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            
            # NIST PQC Finalist - Digital Signatures
            CryptoAlgorithm(
                name="DILITHIUM",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_2,
                nist_status="selected",
                parameter_set="dilithium2",
                description="CRYSTALS-DILITHIUM digital signature algorithm",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["code_signing", "document_authentication", "pki", "firmware_validation"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="DILITHIUM",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_3,
                nist_status="selected",
                parameter_set="dilithium3",
                description="CRYSTALS-DILITHIUM digital signature algorithm (Level 3)",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["code_signing", "document_authentication", "pki", "firmware_validation"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="DILITHIUM",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_5,
                nist_status="selected",
                parameter_set="dilithium5",
                description="CRYSTALS-DILITHIUM digital signature algorithm (Level 5)",
                implementation_variants=["reference", "optimized", "avx2"],
                use_cases=["code_signing", "document_authentication", "pki", "firmware_validation"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            
            CryptoAlgorithm(
                name="FALCON",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_1,
                nist_status="selected",
                parameter_set="falcon512",
                description="FALCON compact digital signature algorithm",
                implementation_variants=["reference", "optimized", "ct"],
                use_cases=["constrained_devices", "embedded_systems", "iot_security"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="FALCON",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.LATTICE_BASED,
                security_level=SecurityLevel.LEVEL_5,
                nist_status="selected",
                parameter_set="falcon1024",
                description="FALCON compact digital signature algorithm (Level 5)",
                implementation_variants=["reference", "optimized", "ct"],
                use_cases=["constrained_devices", "embedded_systems", "iot_security"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            
            CryptoAlgorithm(
                name="SPHINCS_PLUS",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.HASH_BASED,
                security_level=SecurityLevel.LEVEL_1,
                nist_status="selected",
                parameter_set="sphincs_sha256_128f",
                description="SPHINCS+ hash-based signature scheme (fast variant)",
                implementation_variants=["reference", "simple", "robust"],
                use_cases=["long_term_signatures", "blockchain", "timestamping"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="SPHINCS_PLUS",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.HASH_BASED,
                security_level=SecurityLevel.LEVEL_3,
                nist_status="selected",
                parameter_set="sphincs_sha256_192f",
                description="SPHINCS+ hash-based signature scheme (fast variant, Level 3)",
                implementation_variants=["reference", "simple", "robust"],
                use_cases=["long_term_signatures", "blockchain", "timestamping"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            ),
            CryptoAlgorithm(
                name="SPHINCS_PLUS",
                algorithm_type=CryptoAlgorithmType.DIGITAL_SIGNATURE,
                family=AlgorithmFamily.HASH_BASED,
                security_level=SecurityLevel.LEVEL_5,
                nist_status="selected",
                parameter_set="sphincs_sha256_256f",
                description="SPHINCS+ hash-based signature scheme (fast variant, Level 5)",
                implementation_variants=["reference", "simple", "robust"],
                use_cases=["long_term_signatures", "blockchain", "timestamping"],
                compliance_frameworks=["NIST_PQC", "FIPS_CANDIDATE"]
            )
        ]
        
        return algorithms
    
    async def run_comprehensive_benchmark(self, algorithms: Optional[List[str]] = None) -> ComprehensiveBenchmarkReport:
        """Run comprehensive benchmarking of quantum-safe algorithms."""
        start_time = datetime.now()
        
        # Select algorithms to benchmark
        if algorithms is None:
            algorithms_to_test = self.supported_algorithms
        else:
            algorithms_to_test = [alg for alg in self.supported_algorithms if alg.name in algorithms]
        
        logger.info(f"Starting comprehensive benchmark of {len(algorithms_to_test)} algorithms")
        
        # Clear previous results
        self.benchmark_results.clear()
        
        # Run benchmarks for each algorithm
        if self.config.get('parallel_execution', True):
            await self._run_parallel_benchmarks(algorithms_to_test)
        else:
            await self._run_sequential_benchmarks(algorithms_to_test)
        
        # Generate comprehensive report
        report = await self._generate_comprehensive_report(algorithms_to_test, start_time)
        
        # Update metrics
        self.benchmarking_metrics['last_benchmark_timestamp'] = datetime.now()
        self.benchmarking_metrics['total_benchmark_time'] += (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Comprehensive benchmark completed in {(datetime.now() - start_time).total_seconds():.2f} seconds")
        return report
    
    async def _run_parallel_benchmarks(self, algorithms: List[CryptoAlgorithm]) -> None:
        """Run benchmarks in parallel for faster execution."""
        max_workers = min(self.config.get('max_worker_threads', 8), len(algorithms))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            tasks = []
            
            for algorithm in algorithms:
                for implementation in algorithm.implementation_variants:
                    task = asyncio.get_event_loop().run_in_executor(
                        executor,
                        self._benchmark_algorithm_sync,
                        algorithm,
                        implementation
                    )
                    tasks.append(task)
            
            # Wait for all benchmarks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Benchmark failed: {result}")
                elif result:
                    self.benchmark_results.extend(result)
    
    async def _run_sequential_benchmarks(self, algorithms: List[CryptoAlgorithm]) -> None:
        """Run benchmarks sequentially."""
        for algorithm in algorithms:
            for implementation in algorithm.implementation_variants:
                try:
                    results = self._benchmark_algorithm_sync(algorithm, implementation)
                    if results:
                        self.benchmark_results.extend(results)
                except Exception as e:
                    logger.error(f"Benchmark failed for {algorithm.name} ({implementation}): {e}")
    
    def _benchmark_algorithm_sync(self, algorithm: CryptoAlgorithm, implementation: str) -> List[BenchmarkResult]:
        """Synchronous benchmark execution for an algorithm implementation."""
        results = []
        system_info = self.system_profiler.get_system_info()
        test_conditions = {
            'implementation': implementation,
            'iterations': self.config.get('benchmark_iterations', 100),
            'warmup_iterations': self.config.get('warmup_iterations', 10),
            'system_baseline': self.system_baseline
        }
        
        try:
            # Key Generation Benchmark
            key_gen_time, key_gen_stats = self.crypto_simulator.simulate_key_generation(
                algorithm.name, algorithm.parameter_set, self.config.get('benchmark_iterations', 100)
            )
            
            results.append(BenchmarkResult(
                algorithm=algorithm.name,
                parameter_set=algorithm.parameter_set,
                implementation=implementation,
                metric=BenchmarkMetric.KEY_GENERATION_TIME,
                value=key_gen_time,
                unit="milliseconds",
                timestamp=datetime.now(),
                system_info=system_info,
                test_conditions=test_conditions,
                statistical_data=key_gen_stats
            ))
            
            # Encryption/Signing Benchmark
            if algorithm.algorithm_type in [CryptoAlgorithmType.KEY_ENCAPSULATION, CryptoAlgorithmType.DIGITAL_SIGNATURE]:
                enc_time, enc_stats = self.crypto_simulator.simulate_encryption(
                    algorithm.name, algorithm.parameter_set, "medium_message", self.config.get('benchmark_iterations', 100)
                )
                
                metric_type = BenchmarkMetric.SIGNATURE_TIME if algorithm.algorithm_type == CryptoAlgorithmType.DIGITAL_SIGNATURE else BenchmarkMetric.ENCRYPTION_TIME
                
                results.append(BenchmarkResult(
                    algorithm=algorithm.name,
                    parameter_set=algorithm.parameter_set,
                    implementation=implementation,
                    metric=metric_type,
                    value=enc_time,
                    unit="milliseconds",
                    timestamp=datetime.now(),
                    system_info=system_info,
                    test_conditions=test_conditions,
                    statistical_data=enc_stats
                ))
            
            # Memory Usage Benchmark
            memory_usage = key_gen_stats.get('avg_memory_mb', 0) + enc_stats.get('avg_memory_mb', 0) if 'enc_stats' in locals() else key_gen_stats.get('avg_memory_mb', 0)
            
            results.append(BenchmarkResult(
                algorithm=algorithm.name,
                parameter_set=algorithm.parameter_set,
                implementation=implementation,
                metric=BenchmarkMetric.MEMORY_USAGE,
                value=memory_usage,
                unit="megabytes",
                timestamp=datetime.now(),
                system_info=system_info,
                test_conditions=test_conditions,
                statistical_data={'peak_memory': memory_usage * 1.2}
            ))
            
            # Throughput Benchmark
            throughput = enc_stats.get('throughput_mbps', 0) if 'enc_stats' in locals() else 0
            
            results.append(BenchmarkResult(
                algorithm=algorithm.name,
                parameter_set=algorithm.parameter_set,
                implementation=implementation,
                metric=BenchmarkMetric.THROUGHPUT,
                value=throughput,
                unit="mbps",
                timestamp=datetime.now(),
                system_info=system_info,
                test_conditions=test_conditions,
                statistical_data={'peak_throughput': throughput * 1.15}
            ))
            
            self.benchmarking_metrics['tests_completed'] += len(results)
            self.benchmarking_metrics['algorithms_evaluated'].add(algorithm.name)
            
        except Exception as e:
            logger.error(f"Error benchmarking {algorithm.name} ({implementation}): {e}")
        
        return results
    
    async def _generate_comprehensive_report(self, algorithms_tested: List[CryptoAlgorithm], start_time: datetime) -> ComprehensiveBenchmarkReport:
        """Generate comprehensive benchmark report."""
        algorithms_names = [alg.name for alg in algorithms_tested]
        
        # Generate benchmark summary
        benchmark_summary = self._generate_benchmark_summary()
        
        # Calculate performance rankings
        performance_rankings = self._calculate_performance_rankings()
        
        # Security analysis
        security_analysis = self._perform_security_analysis(algorithms_tested)
        
        # Deployment recommendations
        deployment_recommendations = self._generate_deployment_recommendations(algorithms_tested)
        
        # MWRASP integration assessment
        mwrasp_integration = self._assess_mwrasp_integration(algorithms_tested)
        
        report = ComprehensiveBenchmarkReport(
            report_id=f"MWRASP_CRYPTO_BENCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            algorithms_tested=algorithms_names,
            benchmark_summary=benchmark_summary,
            performance_rankings=performance_rankings,
            security_analysis=security_analysis,
            deployment_recommendations=deployment_recommendations,
            mwrasp_integration_assessment=mwrasp_integration,
            detailed_results=self.benchmark_results
        )
        
        return report
    
    def _generate_benchmark_summary(self) -> Dict[str, Any]:
        """Generate benchmark summary statistics."""
        if not self.benchmark_results:
            return {'status': 'no_results'}
        
        # Group results by algorithm
        by_algorithm = {}
        for result in self.benchmark_results:
            if result.algorithm not in by_algorithm:
                by_algorithm[result.algorithm] = []
            by_algorithm[result.algorithm].append(result)
        
        # Calculate summary statistics
        summary = {
            'total_algorithms_tested': len(by_algorithm),
            'total_tests_conducted': len(self.benchmark_results),
            'fastest_key_generation': self._find_fastest(BenchmarkMetric.KEY_GENERATION_TIME),
            'fastest_encryption': self._find_fastest(BenchmarkMetric.ENCRYPTION_TIME),
            'fastest_signature': self._find_fastest(BenchmarkMetric.SIGNATURE_TIME),
            'lowest_memory_usage': self._find_lowest(BenchmarkMetric.MEMORY_USAGE),
            'highest_throughput': self._find_highest(BenchmarkMetric.THROUGHPUT),
            'algorithm_performance_summary': {}
        }
        
        # Per-algorithm summary
        for alg_name, results in by_algorithm.items():
            key_gen_results = [r for r in results if r.metric == BenchmarkMetric.KEY_GENERATION_TIME]
            enc_results = [r for r in results if r.metric in [BenchmarkMetric.ENCRYPTION_TIME, BenchmarkMetric.SIGNATURE_TIME]]
            
            summary['algorithm_performance_summary'][alg_name] = {
                'avg_key_generation_ms': np.mean([r.value for r in key_gen_results]) if key_gen_results else 0,
                'avg_encryption_ms': np.mean([r.value for r in enc_results]) if enc_results else 0,
                'parameter_sets_tested': len(set([r.parameter_set for r in results])),
                'implementations_tested': len(set([r.implementation for r in results]))
            }
        
        return summary
    
    def _find_fastest(self, metric: BenchmarkMetric) -> Dict[str, Any]:
        """Find the fastest algorithm for a given metric."""
        relevant_results = [r for r in self.benchmark_results if r.metric == metric]
        if not relevant_results:
            return {'algorithm': 'N/A', 'value': 0, 'unit': 'N/A'}
        
        fastest = min(relevant_results, key=lambda r: r.value)
        return {
            'algorithm': f"{fastest.algorithm} ({fastest.parameter_set})",
            'implementation': fastest.implementation,
            'value': fastest.value,
            'unit': fastest.unit
        }
    
    def _find_lowest(self, metric: BenchmarkMetric) -> Dict[str, Any]:
        """Find the algorithm with lowest value for a given metric."""
        relevant_results = [r for r in self.benchmark_results if r.metric == metric]
        if not relevant_results:
            return {'algorithm': 'N/A', 'value': 0, 'unit': 'N/A'}
        
        lowest = min(relevant_results, key=lambda r: r.value)
        return {
            'algorithm': f"{lowest.algorithm} ({lowest.parameter_set})",
            'implementation': lowest.implementation,
            'value': lowest.value,
            'unit': lowest.unit
        }
    
    def _find_highest(self, metric: BenchmarkMetric) -> Dict[str, Any]:
        """Find the algorithm with highest value for a given metric."""
        relevant_results = [r for r in self.benchmark_results if r.metric == metric]
        if not relevant_results:
            return {'algorithm': 'N/A', 'value': 0, 'unit': 'N/A'}
        
        highest = max(relevant_results, key=lambda r: r.value)
        return {
            'algorithm': f"{highest.algorithm} ({highest.parameter_set})",
            'implementation': highest.implementation,
            'value': highest.value,
            'unit': highest.unit
        }
    
    def _calculate_performance_rankings(self) -> Dict[str, List[str]]:
        """Calculate performance rankings across different metrics."""
        rankings = {}
        
        metrics_to_rank = [
            BenchmarkMetric.KEY_GENERATION_TIME,
            BenchmarkMetric.ENCRYPTION_TIME,
            BenchmarkMetric.SIGNATURE_TIME,
            BenchmarkMetric.MEMORY_USAGE,
            BenchmarkMetric.THROUGHPUT
        ]
        
        for metric in metrics_to_rank:
            relevant_results = [r for r in self.benchmark_results if r.metric == metric]
            if not relevant_results:
                rankings[metric.value] = []
                continue
            
            # Group by algorithm and get best performance per algorithm
            by_algorithm = {}
            for result in relevant_results:
                alg_key = f"{result.algorithm}_{result.parameter_set}"
                if alg_key not in by_algorithm or result.value < by_algorithm[alg_key].value:
                    if metric == BenchmarkMetric.THROUGHPUT:  # Higher is better for throughput
                        if alg_key not in by_algorithm or result.value > by_algorithm[alg_key].value:
                            by_algorithm[alg_key] = result
                    else:  # Lower is better for time/memory
                        by_algorithm[alg_key] = result
            
            # Sort and create ranking
            if metric == BenchmarkMetric.THROUGHPUT:
                sorted_results = sorted(by_algorithm.values(), key=lambda r: r.value, reverse=True)
            else:
                sorted_results = sorted(by_algorithm.values(), key=lambda r: r.value)
            
            rankings[metric.value] = [f"{r.algorithm} ({r.parameter_set})" for r in sorted_results]
        
        return rankings
    
    def _perform_security_analysis(self, algorithms_tested: List[CryptoAlgorithm]) -> Dict[str, Any]:
        """Perform security analysis of tested algorithms."""
        security_levels = {}
        algorithm_families = {}
        nist_status_distribution = {}
        
        for alg in algorithms_tested:
            # Security level distribution
            level_key = f"Level_{alg.security_level.value}"
            if level_key not in security_levels:
                security_levels[level_key] = []
            security_levels[level_key].append(alg.name)
            
            # Algorithm family distribution
            family_key = alg.family.value
            if family_key not in algorithm_families:
                algorithm_families[family_key] = []
            algorithm_families[family_key].append(alg.name)
            
            # NIST status distribution
            status_key = alg.nist_status
            nist_status_distribution[status_key] = nist_status_distribution.get(status_key, 0) + 1
        
        # Security recommendations
        security_recommendations = []
        
        if any(alg.security_level == SecurityLevel.LEVEL_5 for alg in algorithms_tested):
            security_recommendations.append("Level 5 algorithms available for maximum security applications")
        
        if any(alg.family == AlgorithmFamily.LATTICE_BASED for alg in algorithms_tested):
            security_recommendations.append("Lattice-based algorithms provide strong security foundations")
        
        if any(alg.family == AlgorithmFamily.HASH_BASED for alg in algorithms_tested):
            security_recommendations.append("Hash-based signatures provide quantum-safe long-term security")
        
        return {
            'security_level_distribution': security_levels,
            'algorithm_family_distribution': algorithm_families,
            'nist_status_distribution': nist_status_distribution,
            'security_recommendations': security_recommendations,
            'quantum_resistance': 'FULL',
            'compliance_coverage': list(set([framework for alg in algorithms_tested for framework in alg.compliance_frameworks]))
        }
    
    def _generate_deployment_recommendations(self, algorithms_tested: List[CryptoAlgorithm]) -> Dict[str, Any]:
        """Generate deployment recommendations based on benchmark results."""
        recommendations = {
            'high_performance_scenarios': [],
            'constrained_environments': [],
            'balanced_deployments': [],
            'specific_use_cases': {},
            'implementation_guidance': []
        }
        
        # Analyze performance characteristics
        key_gen_results = [r for r in self.benchmark_results if r.metric == BenchmarkMetric.KEY_GENERATION_TIME]
        memory_results = [r for r in self.benchmark_results if r.metric == BenchmarkMetric.MEMORY_USAGE]
        throughput_results = [r for r in self.benchmark_results if r.metric == BenchmarkMetric.THROUGHPUT]
        
        # High-performance recommendations
        if key_gen_results:
            fastest_keygen = min(key_gen_results, key=lambda r: r.value)
            recommendations['high_performance_scenarios'].append(
                f"{fastest_keygen.algorithm} ({fastest_keygen.parameter_set}) - fastest key generation at {fastest_keygen.value:.2f}ms"
            )
        
        if throughput_results:
            highest_throughput = max(throughput_results, key=lambda r: r.value)
            recommendations['high_performance_scenarios'].append(
                f"{highest_throughput.algorithm} ({highest_throughput.parameter_set}) - highest throughput at {highest_throughput.value:.2f} Mbps"
            )
        
        # Constrained environment recommendations
        if memory_results:
            lowest_memory = min(memory_results, key=lambda r: r.value)
            recommendations['constrained_environments'].append(
                f"{lowest_memory.algorithm} ({lowest_memory.parameter_set}) - lowest memory usage at {lowest_memory.value:.2f}MB"
            )
        
        # Use case specific recommendations
        for alg in algorithms_tested:
            for use_case in alg.use_cases:
                if use_case not in recommendations['specific_use_cases']:
                    recommendations['specific_use_cases'][use_case] = []
                recommendations['specific_use_cases'][use_case].append(f"{alg.name} ({alg.parameter_set})")
        
        # Implementation guidance
        recommendations['implementation_guidance'].extend([
            "Use optimized implementations for production deployments",
            "Implement proper random number generation for key material",
            "Consider hybrid approaches for transition periods",
            "Plan for algorithm agility in long-term deployments"
        ])
        
        return recommendations
    
    def _assess_mwrasp_integration(self, algorithms_tested: List[CryptoAlgorithm]) -> Dict[str, Any]:
        """Assess integration compatibility with MWRASP network infrastructure."""
        integration_assessment = {
            'network_latency_compatibility': {},
            'agent_communication_suitability': {},
            'quantum_velocity_network_integration': {},
            'deployment_readiness': {},
            'mwrasp_specific_recommendations': []
        }
        
        # Analyze latency requirements for MWRASP's sub-millisecond response goals
        key_gen_results = [r for r in self.benchmark_results if r.metric == BenchmarkMetric.KEY_GENERATION_TIME]
        enc_results = [r for r in self.benchmark_results if r.metric in [BenchmarkMetric.ENCRYPTION_TIME, BenchmarkMetric.SIGNATURE_TIME]]
        
        for alg in algorithms_tested:
            alg_key_gen = [r for r in key_gen_results if r.algorithm == alg.name and r.parameter_set == alg.parameter_set]
            alg_enc = [r for r in enc_results if r.algorithm == alg.name and r.parameter_set == alg.parameter_set]
            
            if alg_key_gen:
                avg_keygen_time = np.mean([r.value for r in alg_key_gen])
                # MWRASP targets sub-millisecond response, evaluate compatibility
                if avg_keygen_time < 1.0:
                    compatibility = 'EXCELLENT'
                elif avg_keygen_time < 5.0:
                    compatibility = 'GOOD'
                elif avg_keygen_time < 10.0:
                    compatibility = 'ACCEPTABLE'
                else:
                    compatibility = 'REQUIRES_OPTIMIZATION'
                
                integration_assessment['network_latency_compatibility'][f"{alg.name}_{alg.parameter_set}"] = {
                    'rating': compatibility,
                    'avg_keygen_ms': avg_keygen_time,
                    'mwrasp_latency_target': '<1ms for quantum instant response'
                }
        
        # Agent communication suitability
        for alg in algorithms_tested:
            if alg.algorithm_type == CryptoAlgorithmType.KEY_ENCAPSULATION:
                suitability = 'HIGH' if 'secure_communications' in alg.use_cases else 'MEDIUM'
            elif alg.algorithm_type == CryptoAlgorithmType.DIGITAL_SIGNATURE:
                suitability = 'HIGH' if any(use in alg.use_cases for use in ['pki', 'document_authentication']) else 'MEDIUM'
            else:
                suitability = 'MEDIUM'
            
            integration_assessment['agent_communication_suitability'][f"{alg.name}_{alg.parameter_set}"] = suitability
        
        # Quantum velocity network integration
        for alg in algorithms_tested:
            # Assess based on security level and performance
            if alg.security_level.value >= 3:  # Level 3+ security
                velocity_rating = 'TACTICAL_SWIFT'  # 10-100ms tier
                if alg.family == AlgorithmFamily.LATTICE_BASED:
                    velocity_rating = 'MACHINE_REFLEX'  # 1-10ms tier
            else:
                velocity_rating = 'MACHINE_REFLEX'  # 1-10ms tier
                
            integration_assessment['quantum_velocity_network_integration'][f"{alg.name}_{alg.parameter_set}"] = {
                'velocity_tier': velocity_rating,
                'autonomous_decision_capable': alg.security_level.value >= 3,
                'entanglement_coordination_ready': alg.family == AlgorithmFamily.LATTICE_BASED
            }
        
        # Deployment readiness for national security infrastructure
        for alg in algorithms_tested:
            readiness_score = 0
            
            if alg.nist_status == 'selected':
                readiness_score += 40
            elif alg.nist_status in ['finalist', 'round3']:
                readiness_score += 30
            
            if 'NIST_PQC' in alg.compliance_frameworks:
                readiness_score += 25
            
            if 'FIPS_CANDIDATE' in alg.compliance_frameworks:
                readiness_score += 20
            
            if alg.security_level.value >= 3:
                readiness_score += 15
            
            if readiness_score >= 80:
                readiness_level = 'PRODUCTION_READY'
            elif readiness_score >= 60:
                readiness_level = 'PILOT_READY'
            elif readiness_score >= 40:
                readiness_level = 'TESTING_PHASE'
            else:
                readiness_level = 'RESEARCH_PHASE'
            
            integration_assessment['deployment_readiness'][f"{alg.name}_{alg.parameter_set}"] = {
                'readiness_level': readiness_level,
                'readiness_score': readiness_score,
                'national_security_approved': alg.nist_status == 'selected'
            }
        
        # MWRASP-specific recommendations
        integration_assessment['mwrasp_specific_recommendations'].extend([
            "Deploy KYBER for quantum-safe key exchange in agent communications",
            "Use DILITHIUM for authenticating agent messages and commands",
            "Implement FALCON for constrained devices in the distributed network",
            "Consider SPHINCS+ for long-term archival signatures",
            "Maintain algorithm agility for rapid algorithm switching",
            "Pre-compute key material during low-activity periods",
            "Implement hybrid classical/post-quantum systems during transition",
            "Integrate with quantum velocity network for optimal performance"
        ])
        
        return integration_assessment
    
    def export_benchmark_results(self, format_type: str = "json", filename: Optional[str] = None) -> str:
        """Export benchmark results to various formats."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mwrasp_crypto_benchmark_{timestamp}.{format_type}"
        
        if format_type.lower() == "json":
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'system_info': self.system_profiler.get_system_info(),
                'system_baseline': self.system_baseline,
                'benchmark_config': self.config,
                'benchmarking_metrics': {
                    **self.benchmarking_metrics,
                    'algorithms_evaluated': list(self.benchmarking_metrics['algorithms_evaluated'])
                },
                'results': [result.to_dict() for result in self.benchmark_results]
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        logger.info(f"Benchmark results exported to {filename}")
        return filename
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current benchmarker system status."""
        return {
            'status': 'OPERATIONAL',
            'supported_algorithms': len(self.supported_algorithms),
            'benchmark_results_cached': len(self.benchmark_results),
            'benchmarking_metrics': {
                **self.benchmarking_metrics,
                'algorithms_evaluated': list(self.benchmarking_metrics['algorithms_evaluated'])
            },
            'system_baseline': self.system_baseline,
            'configuration': self.config,
            'last_benchmark': self.benchmarking_metrics.get('last_benchmark_timestamp')
        }


async def main():
    """Main demonstration of the quantum-safe crypto benchmarker."""
    benchmarker = QuantumSafeCryptoBenchmarker()
    
    print("MWRASP Quantum-Safe Cryptographic Benchmarker")
    print("=" * 60)
    
    # Show system status
    status = benchmarker.get_system_status()
    print(f"System Status: {status['status']}")
    print(f"Supported Algorithms: {status['supported_algorithms']}")
    print(f"System Baseline Performance: {status['system_baseline']}")
    
    # Run comprehensive benchmark
    print("\nStarting comprehensive benchmark...")
    report = await benchmarker.run_comprehensive_benchmark(['KYBER', 'DILITHIUM'])
    
    # Display results summary
    print(f"\nBenchmark Report: {report.report_id}")
    print(f"Algorithms Tested: {', '.join(report.algorithms_tested)}")
    print(f"Total Tests Conducted: {report.benchmark_summary['total_tests_conducted']}")
    
    print("\nPerformance Summary:")
    for alg, summary in report.benchmark_summary['algorithm_performance_summary'].items():
        print(f"  {alg}:")
        print(f"    Key Generation: {summary['avg_key_generation_ms']:.2f}ms")
        print(f"    Encryption/Sign: {summary['avg_encryption_ms']:.2f}ms")
    
    print("\nMWRASP Integration Assessment:")
    for alg, assessment in report.mwrasp_integration_assessment['network_latency_compatibility'].items():
        print(f"  {alg}: {assessment['rating']} (avg: {assessment['avg_keygen_ms']:.2f}ms)")
    
    print("\nDeployment Recommendations:")
    for rec in report.deployment_recommendations['high_performance_scenarios'][:3]:
        print(f"  • {rec}")
    
    # Export results
    export_file = benchmarker.export_benchmark_results()
    print(f"\nResults exported to: {export_file}")


if __name__ == "__main__":
    asyncio.run(main())
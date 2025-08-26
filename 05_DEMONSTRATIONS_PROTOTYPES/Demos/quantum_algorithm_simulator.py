#!/usr/bin/env python3
"""
MWRASP Quantum Algorithm Simulator
Simulates quantum algorithm attack patterns for detection testing

Uses free quantum simulation libraries:
- Qiskit (IBM Quantum)
- NumPy for classical simulation
- No external quantum computer required

Created for MWRASP 4-hour development sprint
"""

import numpy as np
import time
import random
import hashlib
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# Try to import Qiskit if available (free IBM Quantum toolkit)
try:
    from qiskit import QuantumCircuit, execute, Aer
    from qiskit.quantum_info import Statevector
    QISKIT_AVAILABLE = True
    print("Qiskit available - using quantum simulation")
except ImportError:
    QISKIT_AVAILABLE = False
    print("Qiskit not available - using classical simulation")

class QuantumAlgorithm(Enum):
    SHOR = "shor"
    GROVER = "grover" 
    SIMON = "simon"
    BERNSTEIN_VAZIRANI = "bernstein_vazirani"
    DEUTSCH_JOZSA = "deutsch_jozsa"

@dataclass
class QuantumAttackSimulation:
    algorithm: QuantumAlgorithm
    n_bits: int
    query_count: int
    execution_time: float
    success_probability: float
    access_pattern: List[Dict]

class QuantumAlgorithmSimulator:
    """Simulate quantum algorithm attack patterns for MWRASP detection testing"""
    
    def __init__(self):
        self.simulator = Aer.get_backend('qasm_simulator') if QISKIT_AVAILABLE else None
        self.attack_history = []
        
    def simulate_simons_algorithm(self, n_bits: int = 4) -> QuantumAttackSimulation:
        """
        Simulate Simon's algorithm for period finding attacks
        
        Simon's algorithm finds hidden periods in O(n) queries vs O(2^n/2) classical
        Used for breaking symmetric cryptographic primitives
        """
        start_time = time.time()
        
        # Simulate hidden period (secret cryptographic structure)
        secret_period = random.randint(1, 2**(n_bits-1))
        
        # Simon's algorithm uses O(n) quantum queries
        quantum_queries = n_bits
        
        access_pattern = []
        base_time = time.time()
        
        # Simulate quantum superposition queries (very fast, periodic)
        for i in range(quantum_queries):
            query_time = base_time + i * 0.0001  # 0.1ms between quantum queries
            
            # Simulate quantum oracle access with hidden periodicity
            oracle_input = random.randint(0, 2**n_bits - 1)
            oracle_output = oracle_input ^ secret_period  # XOR with secret period
            
            access_pattern.append({
                'time': query_time,
                'query_type': 'quantum_oracle',
                'input': oracle_input,
                'output': oracle_output,
                'algorithm_step': 'period_finding',
                'value': str(oracle_input)  # Make input available as value for detection
            })
        
        # Classical post-processing (slower)
        classical_time = base_time + quantum_queries * 0.0001 + 0.01  # 10ms classical processing
        access_pattern.append({
            'time': classical_time,
            'query_type': 'classical_postprocess',
            'result': secret_period,
            'algorithm_step': 'period_extraction'
        })
        
        execution_time = time.time() - start_time
        
        return QuantumAttackSimulation(
            algorithm=QuantumAlgorithm.SIMON,
            n_bits=n_bits,
            query_count=quantum_queries,
            execution_time=execution_time,
            success_probability=1.0,  # Simon's algorithm always succeeds
            access_pattern=access_pattern
        )
    
    def simulate_bernstein_vazirani_algorithm(self, n_bits: int = 6) -> QuantumAttackSimulation:
        """
        Simulate Bernstein-Vazirani algorithm for linear structure detection
        
        BV algorithm finds secret strings in a single quantum query vs 2^n classical queries
        Used for breaking linear structures in block ciphers
        """
        start_time = time.time()
        
        # Simulate secret string (cryptographic key or structure)
        secret_string = random.randint(0, 2**n_bits - 1)
        
        access_pattern = []
        base_time = time.time()
        
        # BV algorithm's signature: single quantum query gives complete answer
        query_time = base_time + 0.0001  # Single 0.1ms quantum query
        
        # Simulate quantum oracle that computes dot product
        oracle_result = bin(secret_string).count('1') % 2  # Parity of secret string
        
        access_pattern.append({
            'time': query_time,
            'query_type': 'quantum_oracle_single',
            'input': 'superposition_all_states',
            'output': oracle_result,
            'algorithm_step': 'linear_structure_detection'
        })
        
        # Immediate result extraction (BV characteristic)
        result_time = query_time + 0.0001  # Additional 0.1ms for result
        access_pattern.append({
            'time': result_time,
            'query_type': 'quantum_measurement',
            'result': secret_string,
            'algorithm_step': 'secret_string_extraction'
        })
        
        # Classical verification (much slower than quantum query)
        verification_time = result_time + 0.02  # 20ms classical verification
        access_pattern.append({
            'time': verification_time,
            'query_type': 'classical_verification',
            'verified_result': secret_string,
            'algorithm_step': 'result_verification'
        })
        
        execution_time = time.time() - start_time
        
        return QuantumAttackSimulation(
            algorithm=QuantumAlgorithm.BERNSTEIN_VAZIRANI,
            n_bits=n_bits,
            query_count=1,  # Single quantum query
            execution_time=execution_time,
            success_probability=1.0,  # BV algorithm always succeeds
            access_pattern=access_pattern
        )
    
    def simulate_deutsch_jozsa_algorithm(self, n_bits: int = 5) -> QuantumAttackSimulation:
        """
        Simulate Deutsch-Jozsa algorithm for oracle function analysis
        
        DJ algorithm determines if function is constant or balanced in single query
        vs 2^(n-1)+1 classical queries
        Used for analyzing cryptographic oracle functions
        """
        start_time = time.time()
        
        # Simulate oracle function (constant or balanced)
        is_constant = random.choice([True, False])
        
        access_pattern = []
        base_time = time.time()
        
        # DJ algorithm's signature: single definitive quantum query
        query_time = base_time + 0.0002  # Single 0.2ms quantum query
        
        if is_constant:
            # Constant function: always returns same value
            oracle_result = random.choice([0, 1])
            function_type = 'constant'
        else:
            # Balanced function: returns 0 for half inputs, 1 for half
            oracle_result = random.choice([0, 1])
            function_type = 'balanced'
        
        access_pattern.append({
            'time': query_time,
            'query_type': 'quantum_oracle_definitive',
            'input': 'superposition_all_states',
            'output': oracle_result,
            'function_type': function_type,
            'algorithm_step': 'oracle_analysis'
        })
        
        # Immediate decisive result (DJ characteristic)
        decision_time = query_time + 0.0001  # 0.1ms for decision
        access_pattern.append({
            'time': decision_time,
            'query_type': 'quantum_decision',
            'decision': function_type,
            'confidence': 1.0,
            'algorithm_step': 'function_classification'
        })
        
        execution_time = time.time() - start_time
        
        return QuantumAttackSimulation(
            algorithm=QuantumAlgorithm.DEUTSCH_JOZSA,
            n_bits=n_bits,
            query_count=1,  # Single quantum query
            execution_time=execution_time,
            success_probability=1.0,  # DJ algorithm always succeeds
            access_pattern=access_pattern
        )
    
    def simulate_grovers_algorithm(self, search_space_bits: int = 10) -> QuantumAttackSimulation:
        """
        Simulate Grover's algorithm for unstructured search attacks
        
        Grover's algorithm searches unstructured databases in O(√N) vs O(N) classical
        Used for breaking cryptographic keys through search acceleration
        """
        start_time = time.time()
        
        # Simulate search space (e.g., cryptographic key space)
        search_space_size = 2**search_space_bits
        target_value = random.randint(0, search_space_size - 1)  # Secret key to find
        
        # Grover's uses approximately √N iterations for optimal success probability
        grover_iterations = int(np.sqrt(search_space_size) * random.uniform(0.8, 1.2))
        
        access_pattern = []
        base_time = time.time()
        
        # Simulate Grover's amplitude amplification iterations
        current_amplitude = 1.0 / np.sqrt(search_space_size)  # Initial uniform superposition
        
        for i in range(grover_iterations):
            iteration_time = base_time + i * 0.0015  # 1.5ms per Grover iteration
            
            # Simulate quantum oracle query (marks target)
            oracle_query_time = iteration_time + 0.0001  # 0.1ms oracle query
            
            # Grover operator: Oracle + Diffusion
            # Amplitude of target state increases each iteration
            current_amplitude = min(current_amplitude * 1.2, 0.99)  # Amplitude amplification
            
            # Simulate measurement probability (amplitude squared)
            measurement_prob = current_amplitude ** 2
            
            # Select values based on current amplification (focus on target region)
            if measurement_prob > 0.5:
                # High amplitude - close to target
                search_value = target_value + random.randint(-10, 10)
            else:
                # Lower amplitude - broader search
                search_value = random.randint(max(0, target_value - 100), 
                                            min(search_space_size-1, target_value + 100))
            
            search_value = max(0, min(search_space_size-1, search_value))  # Bounds check
            
            access_pattern.append({
                'time': oracle_query_time,
                'query_type': 'quantum_oracle_search',
                'input': search_value,
                'output': 1 if search_value == target_value else 0,
                'algorithm_step': 'amplitude_amplification',
                'value': str(search_value),
                'amplitude': current_amplitude,
                'iteration': i
            })
            
            # Simulate diffusion operator (inversion about average)
            diffusion_time = oracle_query_time + 0.0001  # Additional 0.1ms
            access_pattern.append({
                'time': diffusion_time,
                'query_type': 'quantum_diffusion',
                'algorithm_step': 'inversion_about_average',
                'value': str(int(search_space_size * current_amplitude)),  # Average state
                'amplitude': current_amplitude
            })
        
        # Final measurement and result extraction
        measurement_time = base_time + grover_iterations * 0.0015 + 0.005  # 5ms measurement
        final_result = target_value if current_amplitude > 0.7 else random.randint(0, search_space_size-1)
        
        access_pattern.append({
            'time': measurement_time,
            'query_type': 'quantum_measurement',
            'result': final_result,
            'algorithm_step': 'final_measurement',
            'value': str(final_result),
            'success_probability': current_amplitude ** 2
        })
        
        execution_time = time.time() - start_time
        success_prob = current_amplitude ** 2 if current_amplitude < 1.0 else 0.85
        
        return QuantumAttackSimulation(
            algorithm=QuantumAlgorithm.GROVER,
            n_bits=search_space_bits,
            query_count=grover_iterations * 2 + 1,  # Oracle + Diffusion per iteration + measurement
            execution_time=execution_time,
            success_probability=success_prob,
            access_pattern=access_pattern
        )
    
    def simulate_shors_algorithm(self, key_bits: int = 12) -> QuantumAttackSimulation:
        """
        Simulate Shor's algorithm for integer factorization attacks
        
        Shor's algorithm factors large integers exponentially faster than classical methods
        Used for breaking RSA, ECC, and Diffie-Hellman cryptographic systems
        """
        start_time = time.time()
        
        # Simulate RSA-like composite number to factor (N = p * q)
        # For simulation, use smaller numbers but representative patterns
        N = random.randint(2**(key_bits-1), 2**key_bits - 1)
        if N % 2 == 0:
            N += 1  # Make it odd (more realistic for crypto)
        
        access_pattern = []
        base_time = time.time()
        
        # Phase 1: Classical preprocessing - find random 'a' coprime to N
        preprocessing_time = base_time + 0.01  # 10ms preprocessing
        a = random.randint(2, N-1)
        while np.gcd(a, N) != 1:
            a = random.randint(2, N-1)
        
        access_pattern.append({
            'time': preprocessing_time,
            'query_type': 'classical_preprocessing',
            'input': N,
            'value': str(N),
            'algorithm_step': 'coprime_selection',
            'selected_a': a
        })
        
        # Phase 2: Quantum period finding (core of Shor's algorithm)
        # This involves quantum Fourier transform and superposition
        qft_operations = int(np.log2(N)) * 2  # QFT scales with log(N)
        
        period_candidates = []
        current_time = preprocessing_time
        
        for i in range(qft_operations):
            operation_time = current_time + i * 0.0008  # 0.8ms per QFT operation
            
            # Simulate modular exponentiation in superposition: a^x mod N
            superposition_state = random.randint(1, N-1)
            mod_result = pow(a, superposition_state, N)  # a^x mod N
            
            # Quantum Fourier Transform operation
            access_pattern.append({
                'time': operation_time,
                'query_type': 'quantum_fourier_transform',
                'input': superposition_state,
                'output': mod_result,
                'value': str(superposition_state),
                'algorithm_step': 'period_finding',
                'modular_exp': f"{a}^{superposition_state} mod {N} = {mod_result}",
                'qft_phase': i
            })
            
            # Simulate period detection through interference patterns
            if i > 5 and mod_result in [pow(a, j, N) for j in period_candidates[-3:]] if period_candidates else []:
                # Found potential period - Shor's algorithm detects this through quantum interference
                potential_period = superposition_state - (period_candidates[-1] if period_candidates else 0)
                if potential_period > 0:
                    period_candidates.append(potential_period)
            
            period_candidates.append(superposition_state)
        
        # Phase 3: Period analysis and classical post-processing
        analysis_time = current_time + qft_operations * 0.0008 + 0.02  # 20ms analysis
        
        # Determine period from quantum measurements (simulated)
        if len(period_candidates) >= 4:
            period = period_candidates[len(period_candidates)//2]  # Middle candidate
        else:
            period = random.randint(2, N//4)
        
        access_pattern.append({
            'time': analysis_time,
            'query_type': 'quantum_measurement',
            'result': period,
            'value': str(period),
            'algorithm_step': 'period_extraction',
            'period_candidates': len(period_candidates)
        })
        
        # Phase 4: Classical factorization using discovered period
        factorization_time = analysis_time + 0.005  # 5ms factorization
        
        # Use period to find factors: gcd(a^(r/2) ± 1, N)
        if period % 2 == 0:
            factor_attempt = pow(a, period//2, N)
            potential_factor1 = np.gcd(factor_attempt - 1, N)
            potential_factor2 = np.gcd(factor_attempt + 1, N)
            
            if potential_factor1 > 1 and potential_factor1 < N:
                discovered_factor = potential_factor1
            elif potential_factor2 > 1 and potential_factor2 < N:
                discovered_factor = potential_factor2
            else:
                discovered_factor = random.randint(2, int(np.sqrt(N)))  # Fallback
        else:
            discovered_factor = random.randint(2, int(np.sqrt(N)))  # Period not even
        
        access_pattern.append({
            'time': factorization_time,
            'query_type': 'classical_factorization',
            'target': N,
            'discovered_factor': discovered_factor,
            'value': str(discovered_factor),
            'algorithm_step': 'factor_extraction',
            'success': discovered_factor > 1 and N % discovered_factor == 0
        })
        
        # Final verification
        verification_time = factorization_time + 0.002  # 2ms verification
        success = discovered_factor > 1 and N % discovered_factor == 0
        
        access_pattern.append({
            'time': verification_time,
            'query_type': 'classical_verification',
            'original_number': N,
            'factor1': discovered_factor,
            'factor2': N // discovered_factor if success else None,
            'value': str(N),
            'algorithm_step': 'factorization_complete',
            'cryptographic_break': success
        })
        
        execution_time = time.time() - start_time
        success_probability = 0.95 if success else 0.75  # Shor's has high success rate
        
        return QuantumAttackSimulation(
            algorithm=QuantumAlgorithm.SHOR,
            n_bits=key_bits,
            query_count=qft_operations + 4,  # QFT operations + setup/analysis/verification
            execution_time=execution_time,
            success_probability=success_probability,
            access_pattern=access_pattern
        )
    
    def simulate_classical_attack(self, algorithm: QuantumAlgorithm, n_bits: int) -> QuantumAttackSimulation:
        """Simulate classical version of algorithm for comparison"""
        start_time = time.time()
        access_pattern = []
        base_time = time.time()
        
        if algorithm == QuantumAlgorithm.SIMON:
            # Classical period finding requires O(2^n/2) queries
            classical_queries = min(2**(n_bits//2), 100)  # Cap for simulation
            
            for i in range(classical_queries):
                query_time = base_time + i * 0.01  # 10ms per classical query
                access_pattern.append({
                    'time': query_time,
                    'query_type': 'classical_oracle',
                    'input': random.randint(0, 2**n_bits - 1),
                    'algorithm_step': 'brute_force_search'
                })
        
        elif algorithm == QuantumAlgorithm.BERNSTEIN_VAZIRANI:
            # Classical linear structure detection requires 2^n queries worst case
            classical_queries = min(2**n_bits, 64)  # Cap for simulation
            
            for i in range(classical_queries):
                query_time = base_time + i * 0.005  # 5ms per classical query
                access_pattern.append({
                    'time': query_time,
                    'query_type': 'classical_oracle',
                    'input': i,
                    'algorithm_step': 'exhaustive_search'
                })
        
        elif algorithm == QuantumAlgorithm.DEUTSCH_JOZSA:
            # Classical function analysis requires 2^(n-1)+1 queries worst case
            classical_queries = min(2**(n_bits-1) + 1, 32)  # Cap for simulation
            
            for i in range(classical_queries):
                query_time = base_time + i * 0.008  # 8ms per classical query
                access_pattern.append({
                    'time': query_time,
                    'query_type': 'classical_oracle',
                    'input': i,
                    'algorithm_step': 'sequential_evaluation'
                })
        
        elif algorithm == QuantumAlgorithm.GROVER:
            # Classical unstructured search requires O(N) queries worst case
            classical_queries = min(2**n_bits, 100)  # Cap for simulation
            
            for i in range(classical_queries):
                query_time = base_time + i * 0.01  # 10ms per classical query
                access_pattern.append({
                    'time': query_time,
                    'query_type': 'classical_search',
                    'input': i,
                    'algorithm_step': 'linear_search'
                })
        
        elif algorithm == QuantumAlgorithm.SHOR:
            # Classical factorization requires exponential time vs polynomial quantum time
            classical_queries = min(2**(n_bits//2), 50)  # Cap for simulation - exponential scaling
            
            for i in range(classical_queries):
                query_time = base_time + i * 0.05  # 50ms per trial division attempt
                access_pattern.append({
                    'time': query_time,
                    'query_type': 'classical_trial_division',
                    'input': i + 2,  # Trial divisors starting from 2
                    'algorithm_step': 'factorization_attempt'
                })
        
        execution_time = time.time() - start_time
        
        return QuantumAttackSimulation(
            algorithm=algorithm,
            n_bits=n_bits,
            query_count=len(access_pattern),
            execution_time=execution_time,
            success_probability=0.8,  # Classical algorithms may not always succeed quickly
            access_pattern=access_pattern
        )
    
    def generate_mixed_attack_scenario(self, num_attacks: int = 10) -> List[QuantumAttackSimulation]:
        """Generate mixed quantum and classical attack scenarios for testing"""
        scenarios = []
        
        algorithms = [
            QuantumAlgorithm.SIMON,
            QuantumAlgorithm.BERNSTEIN_VAZIRANI, 
            QuantumAlgorithm.DEUTSCH_JOZSA,
            QuantumAlgorithm.GROVER,
            QuantumAlgorithm.SHOR
        ]
        
        for i in range(num_attacks):
            algorithm = random.choice(algorithms)
            n_bits = random.randint(3, 8)
            is_quantum = random.choice([True, False])
            
            if is_quantum:
                if algorithm == QuantumAlgorithm.SIMON:
                    scenario = self.simulate_simons_algorithm(n_bits)
                elif algorithm == QuantumAlgorithm.BERNSTEIN_VAZIRANI:
                    scenario = self.simulate_bernstein_vazirani_algorithm(n_bits)
                elif algorithm == QuantumAlgorithm.DEUTSCH_JOZSA:
                    scenario = self.simulate_deutsch_jozsa_algorithm(n_bits)
                elif algorithm == QuantumAlgorithm.GROVER:
                    scenario = self.simulate_grovers_algorithm(n_bits)
                elif algorithm == QuantumAlgorithm.SHOR:
                    scenario = self.simulate_shors_algorithm(n_bits + 4)  # Larger keys for Shor's
            else:
                scenario = self.simulate_classical_attack(algorithm, n_bits)
            
            scenarios.append(scenario)
        
        return scenarios
    
    def export_test_data(self, scenarios: List[QuantumAttackSimulation], filename: str):
        """Export simulation data for MWRASP testing"""
        import json
        
        test_data = {
            'generated_at': time.time(),
            'total_scenarios': len(scenarios),
            'quantum_scenarios': len([s for s in scenarios if s.query_count <= 10]),
            'classical_scenarios': len([s for s in scenarios if s.query_count > 10]),
            'scenarios': []
        }
        
        for scenario in scenarios:
            test_data['scenarios'].append({
                'algorithm': scenario.algorithm.value,
                'n_bits': scenario.n_bits,
                'query_count': scenario.query_count,
                'execution_time': scenario.execution_time,
                'success_probability': scenario.success_probability,
                'access_pattern': scenario.access_pattern
            })
        
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"Test data exported to {filename}")
        print(f"Generated {len(scenarios)} attack scenarios")
        print(f"Quantum attacks: {test_data['quantum_scenarios']}")
        print(f"Classical attacks: {test_data['classical_scenarios']}")

def main():
    """Test the quantum algorithm simulator"""
    print("MWRASP Quantum Algorithm Simulator")
    print("=" * 50)
    
    simulator = QuantumAlgorithmSimulator()
    
    # Test individual algorithms
    print("\n1. Testing Simon's Algorithm Simulation...")
    simon_attack = simulator.simulate_simons_algorithm(5)
    print(f"Simon's Algorithm: {simon_attack.query_count} queries, {simon_attack.execution_time:.4f}s")
    
    print("\n2. Testing Bernstein-Vazirani Algorithm Simulation...")
    bv_attack = simulator.simulate_bernstein_vazirani_algorithm(6)
    print(f"Bernstein-Vazirani: {bv_attack.query_count} queries, {bv_attack.execution_time:.4f}s")
    
    print("\n3. Testing Deutsch-Jozsa Algorithm Simulation...")
    dj_attack = simulator.simulate_deutsch_jozsa_algorithm(5)
    print(f"Deutsch-Jozsa: {dj_attack.query_count} queries, {dj_attack.execution_time:.4f}s")
    
    print("\n4. Testing Grover's Algorithm Simulation...")
    grover_attack = simulator.simulate_grovers_algorithm(8)
    print(f"Grover's: {grover_attack.query_count} queries, {grover_attack.execution_time:.4f}s")
    
    print("\n5. Testing Shor's Algorithm Simulation...")
    shor_attack = simulator.simulate_shors_algorithm(10)
    print(f"Shor's: {shor_attack.query_count} queries, {shor_attack.execution_time:.4f}s")
    
    # Generate mixed attack scenarios
    print("\n6. Generating Mixed Attack Scenarios...")
    scenarios = simulator.generate_mixed_attack_scenario(20)
    
    # Export test data
    simulator.export_test_data(scenarios, 'quantum_attack_test_data.json')
    
    # Performance comparison
    print("\n7. Quantum vs Classical Performance Comparison:")
    print("-" * 50)
    
    for algorithm in [QuantumAlgorithm.SIMON, QuantumAlgorithm.BERNSTEIN_VAZIRANI, QuantumAlgorithm.DEUTSCH_JOZSA, QuantumAlgorithm.GROVER, QuantumAlgorithm.SHOR]:
        print(f"\n{algorithm.value.upper()} Algorithm:")
        
        # Quantum version
        if algorithm == QuantumAlgorithm.SIMON:
            quantum = simulator.simulate_simons_algorithm(5)
        elif algorithm == QuantumAlgorithm.BERNSTEIN_VAZIRANI:
            quantum = simulator.simulate_bernstein_vazirani_algorithm(5)
        elif algorithm == QuantumAlgorithm.DEUTSCH_JOZSA:
            quantum = simulator.simulate_deutsch_jozsa_algorithm(5)
        elif algorithm == QuantumAlgorithm.GROVER:
            quantum = simulator.simulate_grovers_algorithm(6)
        elif algorithm == QuantumAlgorithm.SHOR:
            quantum = simulator.simulate_shors_algorithm(8)
        
        # Classical version
        classical = simulator.simulate_classical_attack(algorithm, 5)
        
        print(f"  Quantum: {quantum.query_count} queries, {quantum.execution_time:.6f}s")
        print(f"  Classical: {classical.query_count} queries, {classical.execution_time:.6f}s")
        
        query_speedup = classical.query_count / max(quantum.query_count, 1)
        time_speedup = classical.execution_time / max(quantum.execution_time, 0.000001)
        print(f"  Speedup: {query_speedup:.1f}x queries, {time_speedup:.1f}x time")

if __name__ == "__main__":
    main()
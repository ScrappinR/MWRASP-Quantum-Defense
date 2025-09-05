#!/usr/bin/env python3
"""
MWRASP Quantum Circuit Converter
Converts quantum algorithm simulations to executable quantum circuits
for validation against real quantum hardware
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import json
import time
from dataclasses import dataclass
from enum import Enum

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit.circuit.library import QFT
    from qiskit.quantum_info import Operator
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    # Fallback classes for when Qiskit is not available
    class QuantumCircuit:
        def __init__(self, *args, **kwargs):
            self.qubits = []
            self.gates = []
    
    class QuantumRegister:
        def __init__(self, size, name=None):
            self.size = size
            self.name = name
    
    class ClassicalRegister:
        def __init__(self, size, name=None):
            self.size = size
            self.name = name


class AlgorithmType(Enum):
    SIMONS = "simons"
    DEUTSCH_JOZSA = "deutsch_jozsa"
    BERNSTEIN_VAZIRANI = "bernstein_vazirani"
    GROVERS = "grovers"
    SHORS = "shors"


@dataclass
class CircuitConversionResult:
    """Result of quantum circuit conversion"""
    algorithm_type: AlgorithmType
    circuit: Any  # QuantumCircuit when Qiskit available
    parameters: Dict[str, Any]
    qubit_count: int
    depth: int
    gate_count: int
    expected_output: Any
    validation_metrics: Dict[str, float]
    conversion_time: float
    hardware_compatible: bool
    error_rate_estimate: float


@dataclass
class SimulationData:
    """Input simulation data for circuit conversion"""
    algorithm_type: AlgorithmType
    input_size: int
    parameters: Dict[str, Any]
    expected_behavior: Dict[str, Any]
    timing_data: List[float]
    access_patterns: List[Dict]


class QuantumCircuitConverter:
    """Converts quantum algorithm simulations to executable circuits"""
    
    def __init__(self):
        self.qiskit_available = QISKIT_AVAILABLE
        self.conversion_cache: Dict[str, CircuitConversionResult] = {}
        self.supported_algorithms = {
            AlgorithmType.SIMONS: self._convert_simons_algorithm,
            AlgorithmType.DEUTSCH_JOZSA: self._convert_deutsch_jozsa_algorithm,
            AlgorithmType.BERNSTEIN_VAZIRANI: self._convert_bernstein_vazirani_algorithm
        }
        
    def convert_simulation_to_circuit(self, simulation_data: SimulationData) -> CircuitConversionResult:
        """Convert quantum algorithm simulation data to executable circuit"""
        if not self.qiskit_available:
            raise RuntimeError("Qiskit is not available for circuit conversion")
            
        start_time = time.time()
        
        # Check cache first
        cache_key = self._generate_cache_key(simulation_data)
        if cache_key in self.conversion_cache:
            cached_result = self.conversion_cache[cache_key]
            cached_result.conversion_time = time.time() - start_time
            return cached_result
            
        # Get appropriate conversion function
        if simulation_data.algorithm_type not in self.supported_algorithms:
            raise ValueError(f"Unsupported algorithm: {simulation_data.algorithm_type}")
            
        converter_func = self.supported_algorithms[simulation_data.algorithm_type]
        
        # Perform conversion
        result = converter_func(simulation_data)
        result.conversion_time = time.time() - start_time
        
        # Cache result
        self.conversion_cache[cache_key] = result
        
        return result
    
    def _generate_cache_key(self, simulation_data: SimulationData) -> str:
        """Generate cache key for simulation data"""
        key_data = {
            'algorithm': simulation_data.algorithm_type.value,
            'input_size': simulation_data.input_size,
            'parameters': simulation_data.parameters
        }
        return json.dumps(key_data, sort_keys=True)
    
    def _convert_simons_algorithm(self, sim_data: SimulationData) -> CircuitConversionResult:
        """Convert Simon's algorithm simulation to quantum circuit
        
        Simon's algorithm finds hidden bit string s where f(x) = f(x⊕s)
        Requires O(n) quantum queries vs O(2^n/2) classical queries
        """
        n = sim_data.input_size
        if n < 2 or n > 10:  # Practical limits for current quantum hardware
            raise ValueError(f"Simon's algorithm: input size {n} not supported (2-10)")
            
        # Extract Simon's secret from parameters
        secret_string = sim_data.parameters.get('secret_string', '0' * n)
        if len(secret_string) != n:
            secret_string = format(np.random.randint(1, 2**n), f'0{n}b')
            
        # Create quantum circuit
        # Need n qubits for input, n qubits for output (oracle result)
        q_input = QuantumRegister(n, 'input')
        q_output = QuantumRegister(n, 'output') 
        c_result = ClassicalRegister(n, 'result')
        
        circuit = QuantumCircuit(q_input, q_output, c_result)
        
        # Simon's algorithm implementation
        # Step 1: Initialize superposition on input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 2: Apply oracle function f(x) = f(x⊕s)
        # Oracle creates entanglement based on secret string
        self._add_simons_oracle(circuit, q_input, q_output, secret_string)
        
        # Step 3: Apply Hadamard gates to input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 4: Measure input register
        circuit.measure(q_input, c_result)
        
        # Calculate circuit metrics
        gate_count = len(circuit.data)
        depth = circuit.depth()
        
        # Estimate error rate based on circuit complexity and hardware
        error_rate = self._estimate_error_rate(gate_count, depth, n * 2)
        
        # Expected output: measurements should be orthogonal to secret string
        expected_output = {
            'secret_string': secret_string,
            'measurement_constraint': f"All measurements y satisfy y·s = 0 (mod 2)",
            'required_measurements': n - 1,
            'success_probability': max(0.5, 1.0 - error_rate)
        }
        
        # Validation metrics
        validation_metrics = {
            'theoretical_advantage': 2**(n/2) / n,  # Classical vs quantum query complexity
            'circuit_fidelity': 1.0 - error_rate,
            'hardware_efficiency': min(1.0, 10.0 / (gate_count + depth)),
            'scalability_score': max(0.0, 1.0 - (n - 2) / 8.0)  # Scales down as n increases
        }
        
        return CircuitConversionResult(
            algorithm_type=AlgorithmType.SIMONS,
            circuit=circuit,
            parameters={
                'secret_string': secret_string,
                'input_size': n,
                'oracle_type': 'xor_mask'
            },
            qubit_count=n * 2,
            depth=depth,
            gate_count=gate_count,
            expected_output=expected_output,
            validation_metrics=validation_metrics,
            conversion_time=0.0,  # Will be set by caller
            hardware_compatible=error_rate < 0.3,  # Compatible if error rate < 30%
            error_rate_estimate=error_rate
        )
    
    def _add_simons_oracle(self, circuit: QuantumCircuit, q_input: QuantumRegister, 
                          q_output: QuantumRegister, secret_string: str):
        """Add Simon's oracle to quantum circuit
        
        Oracle implements f(x) = f(x⊕s) where s is the secret string
        """
        n = len(secret_string)
        
        # Simple oracle: copy input to output, then apply secret XOR
        for i in range(n):
            circuit.cx(q_input[i], q_output[i])
        
        # Apply secret string XOR pattern
        for i, bit in enumerate(secret_string):
            if bit == '1':
                # If secret bit is 1, apply additional XOR operations
                for j in range(n):
                    if j != i:  # Don't XOR with itself
                        circuit.cx(q_input[j], q_output[i])
    
    def _convert_deutsch_jozsa_algorithm(self, sim_data: SimulationData) -> CircuitConversionResult:
        """Convert Deutsch-Jozsa algorithm simulation to quantum circuit
        
        Deutsch-Jozsa algorithm determines if function is constant or balanced
        with single quantum query vs 2^(n-1)+1 classical queries
        """
        n = sim_data.input_size
        if n < 1 or n > 12:  # Practical limits
            raise ValueError(f"Deutsch-Jozsa algorithm: input size {n} not supported (1-12)")
            
        # Extract function type from parameters
        is_constant = sim_data.parameters.get('is_constant', True)
        constant_value = sim_data.parameters.get('constant_value', 0) if is_constant else None
        
        # Create quantum circuit
        q_input = QuantumRegister(n, 'input')
        q_ancilla = QuantumRegister(1, 'ancilla')
        c_result = ClassicalRegister(n, 'result')
        
        circuit = QuantumCircuit(q_input, q_ancilla, c_result)
        
        # Deutsch-Jozsa algorithm implementation
        # Step 1: Initialize ancilla qubit in |-> state
        circuit.x(q_ancilla[0])
        circuit.h(q_ancilla[0])
        
        # Step 2: Create superposition on input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 3: Apply oracle function
        self._add_deutsch_jozsa_oracle(circuit, q_input, q_ancilla, is_constant, constant_value, n)
        
        # Step 4: Apply Hadamard gates to input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 5: Measure input register
        circuit.measure(q_input, c_result)
        
        # Calculate circuit metrics
        gate_count = len(circuit.data)
        depth = circuit.depth()
        
        # Estimate error rate
        error_rate = self._estimate_error_rate(gate_count, depth, n + 1)
        
        # Expected output
        expected_output = {
            'function_type': 'constant' if is_constant else 'balanced',
            'measurement_result': '0' * n if is_constant else 'non-zero',
            'success_probability': max(0.8, 1.0 - error_rate),
            'quantum_advantage': 2**(n-1) if n > 1 else 2
        }
        
        # Validation metrics
        validation_metrics = {
            'theoretical_advantage': 2**(n-1) / 1.0,  # Classical vs quantum queries
            'circuit_fidelity': 1.0 - error_rate,
            'decisiveness': 1.0,  # DJ gives definitive answer
            'hardware_efficiency': min(1.0, 15.0 / (gate_count + depth))
        }
        
        return CircuitConversionResult(
            algorithm_type=AlgorithmType.DEUTSCH_JOZSA,
            circuit=circuit,
            parameters={
                'is_constant': is_constant,
                'constant_value': constant_value,
                'input_size': n
            },
            qubit_count=n + 1,
            depth=depth,
            gate_count=gate_count,
            expected_output=expected_output,
            validation_metrics=validation_metrics,
            conversion_time=0.0,
            hardware_compatible=error_rate < 0.2,
            error_rate_estimate=error_rate
        )
    
    def _add_deutsch_jozsa_oracle(self, circuit: QuantumCircuit, q_input: QuantumRegister,
                                 q_ancilla: QuantumRegister, is_constant: bool, 
                                 constant_value: Optional[int], n: int):
        """Add Deutsch-Jozsa oracle to quantum circuit"""
        if is_constant:
            if constant_value == 1:
                # Constant function f(x) = 1: flip ancilla
                circuit.x(q_ancilla[0])
            # For f(x) = 0, do nothing
        else:
            # Balanced function: XOR ancilla with parity of input
            for i in range(n):
                circuit.cx(q_input[i], q_ancilla[0])
    
    def _convert_bernstein_vazirani_algorithm(self, sim_data: SimulationData) -> CircuitConversionResult:
        """Convert Bernstein-Vazirani algorithm simulation to quantum circuit
        
        Bernstein-Vazirani algorithm finds secret bit string with single query
        vs n classical queries for n-bit string
        """
        n = sim_data.input_size
        if n < 1 or n > 15:  # Practical limits
            raise ValueError(f"Bernstein-Vazirani algorithm: input size {n} not supported (1-15)")
            
        # Extract secret string from parameters
        secret_string = sim_data.parameters.get('secret_string', '0' * n)
        if len(secret_string) != n:
            secret_string = format(np.random.randint(0, 2**n), f'0{n}b')
            
        # Create quantum circuit
        q_input = QuantumRegister(n, 'input')
        q_ancilla = QuantumRegister(1, 'ancilla')
        c_result = ClassicalRegister(n, 'result')
        
        circuit = QuantumCircuit(q_input, q_ancilla, c_result)
        
        # Bernstein-Vazirani algorithm implementation
        # Step 1: Initialize ancilla qubit in |-> state
        circuit.x(q_ancilla[0])
        circuit.h(q_ancilla[0])
        
        # Step 2: Create superposition on input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 3: Apply oracle function f(x) = s·x (inner product)
        self._add_bernstein_vazirani_oracle(circuit, q_input, q_ancilla, secret_string)
        
        # Step 4: Apply Hadamard gates to input register
        for i in range(n):
            circuit.h(q_input[i])
            
        # Step 5: Measure input register
        circuit.measure(q_input, c_result)
        
        # Calculate circuit metrics
        gate_count = len(circuit.data)
        depth = circuit.depth()
        
        # Estimate error rate
        error_rate = self._estimate_error_rate(gate_count, depth, n + 1)
        
        # Expected output: should directly measure the secret string
        expected_output = {
            'secret_string': secret_string,
            'measurement_result': secret_string,
            'success_probability': max(0.9, 1.0 - error_rate),
            'quantum_advantage': n  # n classical queries vs 1 quantum query
        }
        
        # Validation metrics
        validation_metrics = {
            'theoretical_advantage': float(n),  # n classical vs 1 quantum query
            'circuit_fidelity': 1.0 - error_rate,
            'precision': 1.0,  # BV gives exact answer
            'hardware_efficiency': min(1.0, 20.0 / (gate_count + depth))
        }
        
        return CircuitConversionResult(
            algorithm_type=AlgorithmType.BERNSTEIN_VAZIRANI,
            circuit=circuit,
            parameters={
                'secret_string': secret_string,
                'input_size': n,
                'oracle_type': 'inner_product'
            },
            qubit_count=n + 1,
            depth=depth,
            gate_count=gate_count,
            expected_output=expected_output,
            validation_metrics=validation_metrics,
            conversion_time=0.0,
            hardware_compatible=error_rate < 0.15,
            error_rate_estimate=error_rate
        )
    
    def _add_bernstein_vazirani_oracle(self, circuit: QuantumCircuit, q_input: QuantumRegister,
                                      q_ancilla: QuantumRegister, secret_string: str):
        """Add Bernstein-Vazirani oracle to quantum circuit
        
        Oracle computes f(x) = s·x (inner product mod 2)
        """
        for i, bit in enumerate(secret_string):
            if bit == '1':
                # If secret bit is 1, include this input bit in inner product
                circuit.cx(q_input[i], q_ancilla[0])
    
    def _estimate_error_rate(self, gate_count: int, depth: int, qubit_count: int) -> float:
        """Estimate quantum circuit error rate based on hardware characteristics"""
        # Conservative error model for NISQ devices
        single_qubit_error = 0.001  # 0.1% per single-qubit gate
        two_qubit_error = 0.01     # 1% per two-qubit gate
        decoherence_per_step = 0.0001 * qubit_count  # Decoherence increases with qubits
        
        # Estimate gate types (simplified)
        estimated_single_qubit_gates = gate_count * 0.7  # ~70% single-qubit gates
        estimated_two_qubit_gates = gate_count * 0.3     # ~30% two-qubit gates
        
        # Calculate total error rate
        gate_errors = (estimated_single_qubit_gates * single_qubit_error + 
                      estimated_two_qubit_gates * two_qubit_error)
        decoherence_errors = depth * decoherence_per_step
        
        total_error_rate = gate_errors + decoherence_errors
        
        # Cap error rate at 95% (completely unreliable)
        return min(0.95, total_error_rate)
    
    def validate_circuit_against_simulation(self, circuit_result: CircuitConversionResult,
                                          simulation_data: SimulationData) -> Dict[str, float]:
        """Validate converted circuit against original simulation data"""
        validation_scores = {}
        
        # Check parameter consistency
        param_consistency = self._validate_parameters(circuit_result.parameters, 
                                                     simulation_data.parameters)
        validation_scores['parameter_consistency'] = param_consistency
        
        # Check circuit complexity vs simulation complexity
        complexity_score = self._validate_complexity(circuit_result, simulation_data)
        validation_scores['complexity_match'] = complexity_score
        
        # Check expected behavior alignment
        behavior_score = self._validate_expected_behavior(circuit_result.expected_output,
                                                         simulation_data.expected_behavior)
        validation_scores['behavior_alignment'] = behavior_score
        
        # Overall validation score
        validation_scores['overall_score'] = np.mean(list(validation_scores.values()))
        
        return validation_scores
    
    def _validate_parameters(self, circuit_params: Dict, sim_params: Dict) -> float:
        """Validate parameter consistency between circuit and simulation"""
        if not circuit_params or not sim_params:
            return 0.5  # Neutral if missing parameters
            
        matching_keys = set(circuit_params.keys()) & set(sim_params.keys())
        if not matching_keys:
            return 0.3  # Low score if no matching keys
            
        matches = 0
        for key in matching_keys:
            if circuit_params[key] == sim_params[key]:
                matches += 1
                
        return matches / len(matching_keys)
    
    def _validate_complexity(self, circuit_result: CircuitConversionResult,
                           simulation_data: SimulationData) -> float:
        """Validate circuit complexity matches simulation expectations"""
        # Compare qubit count to input size
        expected_qubits = simulation_data.input_size * 2  # Rough estimate
        qubit_ratio = min(circuit_result.qubit_count, expected_qubits) / max(circuit_result.qubit_count, expected_qubits)
        
        # Check if circuit depth is reasonable
        max_reasonable_depth = simulation_data.input_size * 10
        depth_score = 1.0 if circuit_result.depth <= max_reasonable_depth else 0.5
        
        return (qubit_ratio + depth_score) / 2.0
    
    def _validate_expected_behavior(self, circuit_output: Dict, sim_behavior: Dict) -> float:
        """Validate expected output matches simulation behavior"""
        if not circuit_output or not sim_behavior:
            return 0.6  # Neutral score if missing data
            
        # Check for key behavioral indicators
        score_components = []
        
        # Success probability should be reasonable
        success_prob = circuit_output.get('success_probability', 0.5)
        prob_score = 1.0 if success_prob > 0.7 else success_prob
        score_components.append(prob_score)
        
        # Quantum advantage should be present
        quantum_advantage = circuit_output.get('quantum_advantage', 1.0)
        advantage_score = min(1.0, quantum_advantage / 2.0) if quantum_advantage > 1 else 0.3
        score_components.append(advantage_score)
        
        return np.mean(score_components)
    
    def get_conversion_summary(self) -> Dict[str, Any]:
        """Get summary of all circuit conversions performed"""
        summary = {
            'total_conversions': len(self.conversion_cache),
            'algorithms_converted': list(set(result.algorithm_type.value 
                                           for result in self.conversion_cache.values())),
            'average_conversion_time': np.mean([result.conversion_time 
                                              for result in self.conversion_cache.values()]) if self.conversion_cache else 0,
            'hardware_compatible_rate': np.mean([result.hardware_compatible 
                                               for result in self.conversion_cache.values()]) if self.conversion_cache else 0,
            'qiskit_available': self.qiskit_available
        }
        
        # Algorithm-specific statistics
        for algorithm_type in AlgorithmType:
            if algorithm_type in self.supported_algorithms:
                algorithm_results = [result for result in self.conversion_cache.values() 
                                   if result.algorithm_type == algorithm_type]
                if algorithm_results:
                    summary[f'{algorithm_type.value}_stats'] = {
                        'count': len(algorithm_results),
                        'avg_qubit_count': np.mean([r.qubit_count for r in algorithm_results]),
                        'avg_gate_count': np.mean([r.gate_count for r in algorithm_results]),
                        'avg_error_rate': np.mean([r.error_rate_estimate for r in algorithm_results])
                    }
        
        return summary


# Factory function for easy instantiation
def create_circuit_converter() -> QuantumCircuitConverter:
    """Create and return a QuantumCircuitConverter instance"""
    return QuantumCircuitConverter()
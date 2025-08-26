"""
Quantum Error Correction Pattern Analysis System
Detection and analysis of fault-tolerant quantum computing attacks
"""

import time
import hashlib
import secrets
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json


class QuantumErrorCorrectionCode(Enum):
    SURFACE_CODE = "surface_code"
    STEANE_CODE = "steane_code"
    SHOR_CODE = "shor_code"
    CSS_CODE = "css_code"
    TORIC_CODE = "toric_code"
    COLOR_CODE = "color_code"
    BACON_SHOR_CODE = "bacon_shor_code"
    QUANTUM_LDPC = "quantum_ldpc"
    CONCATENATED_CODE = "concatenated_code"
    TOPOLOGICAL_CODE = "topological_code"
    STABILIZER_CODE = "stabilizer_code"
    SUBSYSTEM_CODE = "subsystem_code"


class ErrorType(Enum):
    BIT_FLIP_X = "bit_flip_x"
    PHASE_FLIP_Z = "phase_flip_z"
    COMBINED_Y = "combined_y"
    DEPOLARIZING = "depolarizing"
    AMPLITUDE_DAMPING = "amplitude_damping"
    PHASE_DAMPING = "phase_damping"
    THERMAL_NOISE = "thermal_noise"
    CROSSTALK = "crosstalk"
    MEASUREMENT_ERROR = "measurement_error"
    GATE_ERROR = "gate_error"
    COHERENT_ERROR = "coherent_error"


class LogicalOperation(Enum):
    LOGICAL_X = "logical_x"
    LOGICAL_Z = "logical_z"
    LOGICAL_Y = "logical_y"
    LOGICAL_H = "logical_h"
    LOGICAL_CNOT = "logical_cnot"
    LOGICAL_T = "logical_t"
    LOGICAL_S = "logical_s"
    LOGICAL_MEASUREMENT = "logical_measurement"
    MAGIC_STATE_INJECTION = "magic_state_injection"
    CODE_SWITCHING = "code_switching"


@dataclass
class ErrorSyndrome:
    syndrome_id: str
    error_pattern: List[int]  # Binary pattern indicating error locations
    syndrome_measurement: List[int]  # Stabilizer measurement outcomes
    error_type: ErrorType
    correction_applied: List[int]  # Correction operations applied
    success_probability: float
    measurement_round: int
    timestamp: float
    logical_qubits_affected: Set[int]
    
    def get_syndrome_weight(self) -> int:
        """Calculate Hamming weight of error syndrome"""
        return sum(self.syndrome_measurement)
    
    def is_correctable(self, code: QuantumErrorCorrectionCode) -> bool:
        """Check if error syndrome is correctable by given code"""
        syndrome_weight = self.get_syndrome_weight()
        
        # Different codes have different correction capabilities
        if code == QuantumErrorCorrectionCode.SURFACE_CODE:
            return syndrome_weight <= 2  # Can correct up to t=2 errors
        elif code == QuantumErrorCorrectionCode.STEANE_CODE:
            return syndrome_weight <= 1  # [[7,1,3]] code corrects 1 error
        elif code == QuantumErrorCorrectionCode.SHOR_CODE:
            return syndrome_weight <= 1  # [[9,1,3]] code corrects 1 error
        else:
            return syndrome_weight <= 1  # Conservative estimate


@dataclass
class FaultTolerantPattern:
    pattern_id: str
    code_type: QuantumErrorCorrectionCode
    logical_qubit_count: int
    physical_qubit_count: int
    error_syndromes: List[ErrorSyndrome]
    logical_operations: List[LogicalOperation]
    threshold_estimate: float  # Error threshold for this pattern
    fidelity_estimate: float
    correction_rounds: int
    detection_timestamp: float
    attack_indicators: List[str] = field(default_factory=list)
    
    def calculate_logical_error_rate(self) -> float:
        """Calculate estimated logical error rate"""
        if not self.error_syndromes:
            return 0.0
        
        failed_corrections = sum(
            1 for syndrome in self.error_syndromes
            if syndrome.success_probability < 0.9
        )
        
        return failed_corrections / len(self.error_syndromes)
    
    def get_code_distance(self) -> int:
        """Estimate code distance from pattern"""
        if self.code_type == QuantumErrorCorrectionCode.SURFACE_CODE:
            # Surface code distance roughly sqrt(physical_qubits)
            return int(np.sqrt(self.physical_qubit_count))
        elif self.code_type == QuantumErrorCorrectionCode.STEANE_CODE:
            return 3  # [[7,1,3]] code
        elif self.code_type == QuantumErrorCorrectionCode.SHOR_CODE:
            return 3  # [[9,1,3]] code
        else:
            return max(1, int(np.log2(self.physical_qubit_count / self.logical_qubit_count)))


@dataclass
class MagicStatePattern:
    state_type: str  # T, CCZ, etc.
    distillation_rounds: int
    input_fidelity: float
    output_fidelity: float
    resource_overhead: float
    injection_success_rate: float
    detection_timestamp: float
    
    def is_high_quality(self) -> bool:
        """Check if magic state meets quality threshold"""
        return (self.output_fidelity > 0.9999 and 
                self.injection_success_rate > 0.95)


class QuantumErrorCorrectionAnalyzer:
    def __init__(self):
        self.error_correction_patterns: Dict[str, FaultTolerantPattern] = {}
        self.syndrome_history: Dict[str, List[ErrorSyndrome]] = defaultdict(list)
        self.magic_state_tracking: Dict[str, List[MagicStatePattern]] = defaultdict(list)
        self.attack_signatures: Dict[str, List[str]] = defaultdict(list)
        
        # Analysis parameters
        self.syndrome_analysis_window = 60.0  # 1 minute window
        self.threshold_detector_sensitivity = 0.001  # Error rate threshold
        self.logical_error_threshold = 1e-15  # Target logical error rate
        
        # Code-specific parameters
        self.code_parameters = self._initialize_code_parameters()
        
        # Detection statistics
        self.detection_stats: Dict[str, int] = defaultdict(int)
        
    def _initialize_code_parameters(self) -> Dict[QuantumErrorCorrectionCode, Dict[str, Any]]:
        """Initialize parameters for different quantum error correction codes"""
        return {
            QuantumErrorCorrectionCode.SURFACE_CODE: {
                'threshold': 0.0057,  # Surface code threshold ~0.57%
                'overhead': lambda d: d**2,  # Quadratic overhead
                'min_distance': 3,
                'max_distance': 100,
                'logical_gate_overhead': {
                    LogicalOperation.LOGICAL_X: 1,
                    LogicalOperation.LOGICAL_Z: 1,
                    LogicalOperation.LOGICAL_CNOT: 4,
                    LogicalOperation.LOGICAL_T: 1000  # Magic state injection
                },
                'stabilizer_count': lambda d: 2 * (d**2 - 1),
                'measurement_rounds': lambda d: d
            },
            QuantumErrorCorrectionCode.STEANE_CODE: {
                'threshold': 0.001,  # Lower threshold for CSS codes
                'overhead': lambda d: 7,  # Fixed [[7,1,3]] encoding
                'min_distance': 3,
                'max_distance': 3,
                'logical_gate_overhead': {
                    LogicalOperation.LOGICAL_X: 1,
                    LogicalOperation.LOGICAL_Z: 1,
                    LogicalOperation.LOGICAL_H: 1,
                    LogicalOperation.LOGICAL_CNOT: 2,
                    LogicalOperation.LOGICAL_T: 15  # Transversal implementation
                },
                'stabilizer_count': lambda d: 6,
                'measurement_rounds': lambda d: 3
            },
            QuantumErrorCorrectionCode.SHOR_CODE: {
                'threshold': 0.0001,  # Very low threshold
                'overhead': lambda d: 9,  # Fixed [[9,1,3]] encoding
                'min_distance': 3,
                'max_distance': 3,
                'logical_gate_overhead': {
                    LogicalOperation.LOGICAL_X: 3,
                    LogicalOperation.LOGICAL_Z: 3,
                    LogicalOperation.LOGICAL_CNOT: 9,
                },
                'stabilizer_count': lambda d: 8,
                'measurement_rounds': lambda d: 2
            },
            QuantumErrorCorrectionCode.COLOR_CODE: {
                'threshold': 0.0025,  # Color code threshold
                'overhead': lambda d: 2 * d**2 - 2 * d + 1,
                'min_distance': 3,
                'max_distance': 50,
                'logical_gate_overhead': {
                    LogicalOperation.LOGICAL_X: 1,
                    LogicalOperation.LOGICAL_Z: 1,
                    LogicalOperation.LOGICAL_H: 1,
                    LogicalOperation.LOGICAL_S: 1,  # Transversal S gate
                    LogicalOperation.LOGICAL_CNOT: 2,
                    LogicalOperation.LOGICAL_T: 100
                },
                'stabilizer_count': lambda d: d**2 - 1,
                'measurement_rounds': lambda d: d
            }
        }
    
    def analyze_error_correction_pattern(
        self,
        access_patterns: List[Dict],
        source_identifier: str
    ) -> Optional[FaultTolerantPattern]:
        """Analyze access patterns for quantum error correction signatures"""
        
        if len(access_patterns) < 10:
            return None
        
        current_time = time.time()
        
        # Extract error correction characteristics
        code_type = self._identify_error_correction_code(access_patterns)
        error_syndromes = self._extract_error_syndromes(access_patterns)
        logical_operations = self._identify_logical_operations(access_patterns)
        
        # Estimate system parameters
        logical_qubits = self._estimate_logical_qubit_count(access_patterns, code_type)
        physical_qubits = self._estimate_physical_qubit_count(access_patterns, code_type, logical_qubits)
        
        # Calculate quality metrics
        threshold_estimate = self._estimate_error_threshold(error_syndromes, code_type)
        fidelity_estimate = self._estimate_logical_fidelity(error_syndromes)
        correction_rounds = self._count_correction_rounds(access_patterns)
        
        # Create pattern
        pattern = FaultTolerantPattern(
            pattern_id=f"ftqc_{secrets.token_hex(8)}_{int(current_time)}",
            code_type=code_type,
            logical_qubit_count=logical_qubits,
            physical_qubit_count=physical_qubits,
            error_syndromes=error_syndromes,
            logical_operations=logical_operations,
            threshold_estimate=threshold_estimate,
            fidelity_estimate=fidelity_estimate,
            correction_rounds=correction_rounds,
            detection_timestamp=current_time
        )
        
        # Analyze for attack indicators
        self._analyze_attack_indicators(pattern, access_patterns)
        
        self.error_correction_patterns[pattern.pattern_id] = pattern
        
        # Update syndrome history
        for syndrome in error_syndromes:
            self.syndrome_history[source_identifier].append(syndrome)
        
        # Check for suspicious patterns
        self._check_fault_injection_attacks(pattern, source_identifier)
        
        return pattern
    
    def _identify_error_correction_code(self, access_patterns: List[Dict]) -> QuantumErrorCorrectionCode:
        """Identify quantum error correction code from access patterns"""
        
        # Look for stabilizer measurement patterns
        measurement_patterns = []
        syndrome_patterns = []
        
        for access in access_patterns:
            query_type = access.get('query_type', '').lower()
            value = str(access.get('value', '')).lower()
            
            if 'stabilizer' in query_type or 'syndrome' in query_type:
                syndrome_patterns.append(access)
            elif 'measurement' in query_type:
                measurement_patterns.append(access)
        
        # Analyze patterns to identify code type
        if len(syndrome_patterns) >= 6:
            # Check for surface code signatures (2D grid of stabilizers)
            grid_indicators = sum(1 for p in syndrome_patterns if 'grid' in str(p) or 'surface' in str(p))
            if grid_indicators > 0 or len(syndrome_patterns) > 20:
                return QuantumErrorCorrectionCode.SURFACE_CODE
            
            # Check for Steane code (7 qubits, 6 stabilizers)
            if 6 <= len(syndrome_patterns) <= 8:
                return QuantumErrorCorrectionCode.STEANE_CODE
            
            # Check for Shor code (9 qubits, 8 stabilizers)
            if 8 <= len(syndrome_patterns) <= 10:
                return QuantumErrorCorrectionCode.SHOR_CODE
            
            # Check for color code indicators
            color_indicators = sum(1 for p in syndrome_patterns if 'color' in str(p))
            if color_indicators > 0:
                return QuantumErrorCorrectionCode.COLOR_CODE
        
        # Default to stabilizer code
        return QuantumErrorCorrectionCode.STABILIZER_CODE
    
    def _extract_error_syndromes(self, access_patterns: List[Dict]) -> List[ErrorSyndrome]:
        """Extract error syndromes from access patterns"""
        syndromes = []
        current_time = time.time()
        
        # Group patterns by measurement rounds
        measurement_rounds = defaultdict(list)
        
        for i, access in enumerate(access_patterns):
            round_id = i // 10  # Assume 10 measurements per round
            measurement_rounds[round_id].append(access)
        
        for round_id, round_accesses in measurement_rounds.items():
            if len(round_accesses) >= 4:  # Need sufficient measurements
                
                # Extract syndrome measurements
                syndrome_measurements = []
                error_pattern = []
                
                for access in round_accesses:
                    # Extract binary measurements from access patterns
                    output_val = access.get('output', 0)
                    if isinstance(output_val, int):
                        syndrome_measurements.append(output_val % 2)  # Convert to binary
                        error_pattern.append((output_val // 2) % 2)
                
                if syndrome_measurements and len(syndrome_measurements) >= 3:
                    # Determine error type based on syndrome pattern
                    syndrome_weight = sum(syndrome_measurements)
                    if syndrome_weight == 1:
                        error_type = ErrorType.BIT_FLIP_X
                    elif syndrome_weight == 2:
                        error_type = ErrorType.PHASE_FLIP_Z
                    elif syndrome_weight >= 3:
                        error_type = ErrorType.DEPOLARIZING
                    else:
                        error_type = ErrorType.MEASUREMENT_ERROR
                    
                    # Estimate correction success probability
                    correction_applied = [s for s in syndrome_measurements if s == 1]
                    success_prob = max(0.5, 1.0 - (syndrome_weight * 0.1))
                    
                    syndrome = ErrorSyndrome(
                        syndrome_id=f"syndrome_{round_id}_{secrets.token_hex(4)}",
                        error_pattern=error_pattern[:len(syndrome_measurements)],
                        syndrome_measurement=syndrome_measurements,
                        error_type=error_type,
                        correction_applied=correction_applied,
                        success_probability=success_prob,
                        measurement_round=round_id,
                        timestamp=current_time - (len(measurement_rounds) - round_id) * 0.1,
                        logical_qubits_affected={0}  # Simplified
                    )
                    
                    syndromes.append(syndrome)
        
        return syndromes
    
    def _identify_logical_operations(self, access_patterns: List[Dict]) -> List[LogicalOperation]:
        """Identify logical quantum operations from access patterns"""
        logical_ops = []
        
        for access in access_patterns:
            query_type = access.get('query_type', '').lower()
            algorithm_step = access.get('algorithm_step', '').lower()
            value = str(access.get('value', '')).lower()
            
            # Look for logical operation indicators
            if 'logical' in query_type:
                if 'x' in value or 'pauli_x' in algorithm_step:
                    logical_ops.append(LogicalOperation.LOGICAL_X)
                elif 'z' in value or 'pauli_z' in algorithm_step:
                    logical_ops.append(LogicalOperation.LOGICAL_Z)
                elif 'y' in value or 'pauli_y' in algorithm_step:
                    logical_ops.append(LogicalOperation.LOGICAL_Y)
                elif 'hadamard' in algorithm_step or 'h_gate' in value:
                    logical_ops.append(LogicalOperation.LOGICAL_H)
                elif 'cnot' in algorithm_step or 'cx' in value:
                    logical_ops.append(LogicalOperation.LOGICAL_CNOT)
                elif 't_gate' in algorithm_step or 't' in value:
                    logical_ops.append(LogicalOperation.LOGICAL_T)
            
            elif 'magic' in query_type or 'magic_state' in algorithm_step:
                logical_ops.append(LogicalOperation.MAGIC_STATE_INJECTION)
            
            elif 'measurement' in query_type and 'logical' in algorithm_step:
                logical_ops.append(LogicalOperation.LOGICAL_MEASUREMENT)
        
        return logical_ops
    
    def _estimate_logical_qubit_count(self, access_patterns: List[Dict], code_type: QuantumErrorCorrectionCode) -> int:
        """Estimate number of logical qubits"""
        
        # Look for logical operation patterns
        logical_indicators = []
        for access in access_patterns:
            if 'logical' in str(access).lower():
                logical_indicators.append(access)
        
        if logical_indicators:
            # Estimate based on unique logical qubit references
            unique_qubits = set()
            for access in logical_indicators:
                # Extract qubit indices from access patterns
                input_val = access.get('input', 0)
                if isinstance(input_val, int) and input_val < 100:
                    unique_qubits.add(input_val % 20)  # Assume max 20 logical qubits
            
            return max(1, len(unique_qubits))
        else:
            # Conservative estimate based on pattern complexity
            return max(1, len(access_patterns) // 50)
    
    def _estimate_physical_qubit_count(
        self, 
        access_patterns: List[Dict], 
        code_type: QuantumErrorCorrectionCode, 
        logical_qubits: int
    ) -> int:
        """Estimate number of physical qubits"""
        
        code_params = self.code_parameters.get(code_type)
        if code_params:
            if code_type == QuantumErrorCorrectionCode.SURFACE_CODE:
                # Surface code needs d^2 physical qubits per logical qubit
                distance = max(3, int(np.sqrt(len(access_patterns) / 10)))  # Rough estimate
                return logical_qubits * distance**2
            elif code_type == QuantumErrorCorrectionCode.STEANE_CODE:
                return logical_qubits * 7  # [[7,1,3]] code
            elif code_type == QuantumErrorCorrectionCode.SHOR_CODE:
                return logical_qubits * 9  # [[9,1,3]] code
            else:
                # General estimate
                return logical_qubits * max(7, len(access_patterns) // 20)
        else:
            return logical_qubits * 10  # Conservative estimate
    
    def _estimate_error_threshold(self, error_syndromes: List[ErrorSyndrome], code_type: QuantumErrorCorrectionCode) -> float:
        """Estimate error threshold from observed syndromes"""
        
        if not error_syndromes:
            return 0.001  # Default threshold
        
        # Calculate observed error rate
        total_errors = sum(syndrome.get_syndrome_weight() for syndrome in error_syndromes)
        total_measurements = sum(len(syndrome.syndrome_measurement) for syndrome in error_syndromes)
        
        if total_measurements == 0:
            return 0.001
        
        observed_error_rate = total_errors / total_measurements
        
        # Compare to theoretical thresholds
        code_params = self.code_parameters.get(code_type)
        if code_params:
            theoretical_threshold = code_params['threshold']
            # Return estimated threshold based on performance
            return min(theoretical_threshold, observed_error_rate * 2)
        else:
            return observed_error_rate * 1.5
    
    def _estimate_logical_fidelity(self, error_syndromes: List[ErrorSyndrome]) -> float:
        """Estimate logical gate fidelity"""
        
        if not error_syndromes:
            return 0.99  # Default high fidelity
        
        # Calculate average success probability
        success_probs = [syndrome.success_probability for syndrome in error_syndromes]
        avg_success = np.mean(success_probs)
        
        # Convert to logical fidelity (higher is better)
        logical_fidelity = 0.95 + avg_success * 0.05  # Scale between 0.95-1.0
        
        return min(0.9999, logical_fidelity)
    
    def _count_correction_rounds(self, access_patterns: List[Dict]) -> int:
        """Count error correction rounds"""
        
        correction_indicators = []
        for access in access_patterns:
            if ('correction' in str(access).lower() or 
                'syndrome' in str(access).lower() or
                'stabilizer' in str(access).lower()):
                correction_indicators.append(access)
        
        # Estimate rounds based on temporal grouping
        if correction_indicators:
            times = [access.get('time', 0) for access in correction_indicators]
            time_diffs = np.diff(sorted(times))
            
            # Count significant time gaps as round boundaries
            round_boundaries = sum(1 for diff in time_diffs if diff > 0.01)  # 10ms threshold
            return max(1, round_boundaries + 1)
        else:
            return 1
    
    def _analyze_attack_indicators(self, pattern: FaultTolerantPattern, access_patterns: List[Dict]):
        """Analyze pattern for potential attack indicators"""
        
        attack_indicators = []
        
        # Check for abnormally high error rates
        logical_error_rate = pattern.calculate_logical_error_rate()
        if logical_error_rate > 0.1:  # 10% logical error rate is suspiciously high
            attack_indicators.append(f"high_logical_error_rate_{logical_error_rate:.3f}")
        
        # Check for threshold violations
        if pattern.threshold_estimate > 0.01:  # Above typical thresholds
            attack_indicators.append(f"threshold_violation_{pattern.threshold_estimate:.4f}")
        
        # Check for unusual syndrome patterns
        if pattern.error_syndromes:
            high_weight_syndromes = sum(
                1 for syndrome in pattern.error_syndromes
                if syndrome.get_syndrome_weight() > 5
            )
            if high_weight_syndromes > len(pattern.error_syndromes) * 0.3:
                attack_indicators.append("high_weight_syndromes")
        
        # Check for magic state distillation attacks
        logical_t_count = sum(1 for op in pattern.logical_operations if op == LogicalOperation.LOGICAL_T)
        if logical_t_count > len(pattern.logical_operations) * 0.5:
            attack_indicators.append("excessive_t_gates")
        
        # Check for code switching attacks
        code_switching_count = sum(1 for op in pattern.logical_operations if op == LogicalOperation.CODE_SWITCHING)
        if code_switching_count > 0:
            attack_indicators.append("code_switching_detected")
        
        pattern.attack_indicators = attack_indicators
    
    def _check_fault_injection_attacks(self, pattern: FaultTolerantPattern, source_identifier: str):
        """Check for fault injection attack patterns"""
        
        # Analyze error syndrome patterns for injection signatures
        if pattern.error_syndromes:
            # Check for correlated errors (signature of fault injection)
            correlated_errors = 0
            for i, syndrome1 in enumerate(pattern.error_syndromes):
                for j, syndrome2 in enumerate(pattern.error_syndromes[i+1:], i+1):
                    # Check for spatial or temporal correlation
                    if (abs(syndrome1.timestamp - syndrome2.timestamp) < 0.001 and  # Same time
                        syndrome1.error_type == syndrome2.error_type):  # Same error type
                        correlated_errors += 1
            
            correlation_ratio = correlated_errors / len(pattern.error_syndromes)
            if correlation_ratio > 0.3:  # High correlation suggests injection
                pattern.attack_indicators.append("fault_injection_correlation")
                self.attack_signatures["fault_injection"].append(pattern.pattern_id)
                
                print(f"FAULT INJECTION ATTACK DETECTED: {pattern.code_type.value}")
                print(f"Pattern: {pattern.pattern_id}")
                print(f"Correlation ratio: {correlation_ratio:.3f}")
                print(f"Logical error rate: {pattern.calculate_logical_error_rate():.3f}")
                
                self.detection_stats["fault_injection"] += 1
        
        # Check for threshold manipulation attacks
        if pattern.threshold_estimate > 0.005:  # Above surface code threshold
            pattern.attack_indicators.append("threshold_manipulation")
            self.attack_signatures["threshold_attack"].append(pattern.pattern_id)
            
            print(f"THRESHOLD MANIPULATION DETECTED: {pattern.code_type.value}")
            print(f"Estimated threshold: {pattern.threshold_estimate:.4f}")
            
            self.detection_stats["threshold_attack"] += 1
    
    def analyze_magic_state_distillation(
        self, 
        access_patterns: List[Dict], 
        source_identifier: str
    ) -> Optional[MagicStatePattern]:
        """Analyze magic state distillation patterns"""
        
        magic_indicators = [
            access for access in access_patterns
            if ('magic' in str(access).lower() or 
                't_gate' in str(access).lower() or
                'distillation' in str(access).lower())
        ]
        
        if len(magic_indicators) < 3:
            return None
        
        current_time = time.time()
        
        # Estimate distillation parameters
        distillation_rounds = self._count_distillation_rounds(magic_indicators)
        input_fidelity = self._estimate_input_fidelity(magic_indicators)
        output_fidelity = self._estimate_output_fidelity(magic_indicators, input_fidelity, distillation_rounds)
        resource_overhead = self._calculate_resource_overhead(magic_indicators, distillation_rounds)
        injection_success_rate = self._estimate_injection_success_rate(magic_indicators)
        
        pattern = MagicStatePattern(
            state_type="T_state",  # Most common magic state
            distillation_rounds=distillation_rounds,
            input_fidelity=input_fidelity,
            output_fidelity=output_fidelity,
            resource_overhead=resource_overhead,
            injection_success_rate=injection_success_rate,
            detection_timestamp=current_time
        )
        
        self.magic_state_tracking[source_identifier].append(pattern)
        
        # Check for magic state attacks
        if not pattern.is_high_quality():
            print(f"MAGIC STATE ATTACK DETECTED: Low quality magic states")
            print(f"Output fidelity: {output_fidelity:.4f}")
            print(f"Injection success rate: {injection_success_rate:.3f}")
            
            self.detection_stats["magic_state_attack"] += 1
        
        return pattern
    
    def _count_distillation_rounds(self, magic_indicators: List[Dict]) -> int:
        """Count magic state distillation rounds"""
        # Look for repeated distillation patterns
        distillation_times = [access.get('time', 0) for access in magic_indicators]
        time_gaps = np.diff(sorted(distillation_times))
        
        # Count significant gaps as round separators
        rounds = sum(1 for gap in time_gaps if gap > 0.1) + 1  # 100ms threshold
        return max(1, min(rounds, 10))  # Cap at 10 rounds
    
    def _estimate_input_fidelity(self, magic_indicators: List[Dict]) -> float:
        """Estimate input magic state fidelity"""
        # Analyze access patterns for fidelity indicators
        error_indicators = sum(
            1 for access in magic_indicators
            if 'error' in str(access).lower()
        )
        
        # High error indicators suggest low input fidelity
        error_rate = error_indicators / len(magic_indicators)
        return max(0.5, 1.0 - error_rate)
    
    def _estimate_output_fidelity(self, magic_indicators: List[Dict], input_fidelity: float, rounds: int) -> float:
        """Estimate output magic state fidelity after distillation"""
        # Distillation improves fidelity exponentially with rounds
        improvement_factor = 1 - (1 - input_fidelity) ** (2 ** rounds)
        output_fidelity = input_fidelity + improvement_factor * (0.9999 - input_fidelity)
        
        return min(0.9999, output_fidelity)
    
    def _calculate_resource_overhead(self, magic_indicators: List[Dict], rounds: int) -> float:
        """Calculate resource overhead for magic state distillation"""
        # Resource overhead grows exponentially with distillation rounds
        base_overhead = len(magic_indicators) * 15  # T gates are expensive
        distillation_overhead = 2 ** rounds  # Exponential resource cost
        
        return base_overhead * distillation_overhead
    
    def _estimate_injection_success_rate(self, magic_indicators: List[Dict]) -> float:
        """Estimate magic state injection success rate"""
        # Look for injection success/failure patterns
        success_indicators = sum(
            1 for access in magic_indicators
            if ('success' in str(access).lower() or 
                access.get('output', 0) == access.get('input', 1))
        )
        
        return success_indicators / len(magic_indicators)
    
    def get_error_correction_analysis(self) -> Dict[str, Any]:
        """Get comprehensive error correction analysis"""
        current_time = time.time()
        
        analysis = {
            'fault_tolerant_patterns_detected': len(self.error_correction_patterns),
            'error_correction_codes_identified': {},
            'attack_detection_statistics': dict(self.detection_stats),
            'syndrome_analysis': {},
            'magic_state_analysis': {},
            'threshold_analysis': {},
            'recent_patterns': [],
            'code_performance_metrics': {}
        }
        
        # Analyze code distribution
        code_distribution = defaultdict(int)
        threshold_estimates = defaultdict(list)
        fidelity_estimates = defaultdict(list)
        
        for pattern in self.error_correction_patterns.values():
            code_distribution[pattern.code_type.value] += 1
            threshold_estimates[pattern.code_type.value].append(pattern.threshold_estimate)
            fidelity_estimates[pattern.code_type.value].append(pattern.fidelity_estimate)
        
        analysis['error_correction_codes_identified'] = dict(code_distribution)
        
        # Syndrome analysis
        total_syndromes = sum(len(syndromes) for syndromes in self.syndrome_history.values())
        if total_syndromes > 0:
            all_syndromes = []
            for syndromes in self.syndrome_history.values():
                all_syndromes.extend(syndromes)
            
            syndrome_weights = [s.get_syndrome_weight() for s in all_syndromes]
            error_types = [s.error_type.value for s in all_syndromes]
            
            analysis['syndrome_analysis'] = {
                'total_syndromes': total_syndromes,
                'average_syndrome_weight': np.mean(syndrome_weights),
                'max_syndrome_weight': np.max(syndrome_weights),
                'error_type_distribution': {
                    error_type: error_types.count(error_type)
                    for error_type in set(error_types)
                },
                'high_weight_syndrome_percentage': sum(1 for w in syndrome_weights if w > 3) / len(syndrome_weights)
            }
        
        # Magic state analysis
        total_magic_states = sum(len(patterns) for patterns in self.magic_state_tracking.values())
        if total_magic_states > 0:
            all_magic_patterns = []
            for patterns in self.magic_state_tracking.values():
                all_magic_patterns.extend(patterns)
            
            analysis['magic_state_analysis'] = {
                'total_magic_state_patterns': total_magic_states,
                'average_distillation_rounds': np.mean([p.distillation_rounds for p in all_magic_patterns]),
                'average_output_fidelity': np.mean([p.output_fidelity for p in all_magic_patterns]),
                'average_resource_overhead': np.mean([p.resource_overhead for p in all_magic_patterns]),
                'high_quality_state_percentage': sum(1 for p in all_magic_patterns if p.is_high_quality()) / len(all_magic_patterns)
            }
        
        # Threshold analysis
        for code_type, thresholds in threshold_estimates.items():
            if thresholds:
                analysis['threshold_analysis'][code_type] = {
                    'average_threshold': np.mean(thresholds),
                    'min_threshold': np.min(thresholds),
                    'max_threshold': np.max(thresholds),
                    'above_theoretical_count': sum(1 for t in thresholds if t > 0.005)
                }
        
        # Code performance metrics
        for code_type, fidelities in fidelity_estimates.items():
            if fidelities:
                analysis['code_performance_metrics'][code_type] = {
                    'average_fidelity': np.mean(fidelities),
                    'min_fidelity': np.min(fidelities),
                    'max_fidelity': np.max(fidelities),
                    'high_fidelity_count': sum(1 for f in fidelities if f > 0.99)
                }
        
        # Recent patterns (last 5 minutes)
        recent_patterns = [
            pattern for pattern in self.error_correction_patterns.values()
            if current_time - pattern.detection_timestamp < 300.0
        ]
        
        analysis['recent_patterns'] = [
            {
                'pattern_id': pattern.pattern_id,
                'code_type': pattern.code_type.value,
                'logical_qubits': pattern.logical_qubit_count,
                'physical_qubits': pattern.physical_qubit_count,
                'threshold_estimate': pattern.threshold_estimate,
                'fidelity_estimate': pattern.fidelity_estimate,
                'attack_indicators': pattern.attack_indicators,
                'detection_time': pattern.detection_timestamp
            }
            for pattern in recent_patterns
        ]
        
        return analysis
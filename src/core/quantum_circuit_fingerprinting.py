"""
Quantum Circuit Fingerprinting System
Hardware-specific quantum computer attack detection through circuit analysis
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


class QuantumHardwareType(Enum):
    IBM_QUANTUM = "ibm_quantum"
    GOOGLE_QUANTUM = "google_quantum"
    RIGETTI_QUANTUM = "rigetti_quantum"
    IONQ_TRAPPED_ION = "ionq_trapped_ion"
    DWAVE_ANNEALING = "dwave_annealing"
    XANADU_PHOTONIC = "xanadu_photonic"
    ATOM_COMPUTING = "atom_computing"
    PASQAL_NEUTRAL_ATOM = "pasqal_neutral_atom"
    QUANTINUUM_TRAPPED_ION = "quantinuum_trapped_ion"
    UNKNOWN_HARDWARE = "unknown_hardware"


class QuantumGateType(Enum):
    # Single-qubit gates
    PAULI_X = "pauli_x"
    PAULI_Y = "pauli_y"
    PAULI_Z = "pauli_z"
    HADAMARD = "hadamard"
    PHASE = "phase"
    T_GATE = "t_gate"
    S_GATE = "s_gate"
    RX_ROTATION = "rx_rotation"
    RY_ROTATION = "ry_rotation"
    RZ_ROTATION = "rz_rotation"
    
    # Two-qubit gates
    CNOT = "cnot"
    CZ_GATE = "cz_gate"
    SWAP = "swap"
    ISWAP = "iswap"
    
    # Multi-qubit gates
    TOFFOLI = "toffoli"
    FREDKIN = "fredkin"
    
    # Measurement and initialization
    MEASUREMENT = "measurement"
    RESET = "reset"
    
    # Hardware-specific gates
    MOLMER_SORENSEN = "molmer_sorensen"  # Trapped ion
    NATIVE_GATE = "native_gate"
    
    # Error correction
    STABILIZER_CHECK = "stabilizer_check"
    ERROR_SYNDROME = "error_syndrome"


@dataclass
class QuantumCircuitPattern:
    pattern_id: str
    hardware_type: QuantumHardwareType
    gate_sequence: List[QuantumGateType]
    qubit_connectivity: Dict[int, Set[int]]
    gate_fidelities: Dict[QuantumGateType, float]
    coherence_times: Dict[int, float]  # T1, T2 times per qubit
    gate_times: Dict[QuantumGateType, float]  # Execution times in microseconds
    error_rates: Dict[QuantumGateType, float]
    native_gate_set: Set[QuantumGateType]
    pattern_confidence: float
    detection_timestamp: float
    circuit_depth: int
    qubit_count: int
    
    def get_hardware_signature(self) -> str:
        """Generate unique hardware signature from circuit characteristics"""
        signature_data = {
            'hardware_type': self.hardware_type.value,
            'native_gates': sorted([gate.value for gate in self.native_gate_set]),
            'connectivity_hash': self._hash_connectivity(),
            'fidelity_profile': self._get_fidelity_profile(),
            'timing_profile': self._get_timing_profile()
        }
        
        signature_str = json.dumps(signature_data, sort_keys=True)
        return hashlib.sha256(signature_str.encode()).hexdigest()[:32]
    
    def _hash_connectivity(self) -> str:
        """Create hash of qubit connectivity topology"""
        connectivity_str = ''.join([
            f"{qubit}:{sorted(list(neighbors))}"
            for qubit, neighbors in sorted(self.qubit_connectivity.items())
        ])
        return hashlib.md5(connectivity_str.encode()).hexdigest()[:16]
    
    def _get_fidelity_profile(self) -> List[float]:
        """Get sorted fidelity profile for hardware identification"""
        return sorted([fidelity for fidelity in self.gate_fidelities.values()], reverse=True)
    
    def _get_timing_profile(self) -> List[float]:
        """Get sorted timing profile for hardware identification"""
        return sorted([timing for timing in self.gate_times.values()])


@dataclass
class HardwareFingerprint:
    fingerprint_id: str
    hardware_type: QuantumHardwareType
    vendor_signature: str
    architecture_characteristics: Dict[str, Any]
    noise_profile: Dict[str, float]
    calibration_timestamp: float
    confidence_score: float
    detection_history: List[float] = field(default_factory=list)
    
    def matches_pattern(self, pattern: QuantumCircuitPattern, threshold: float = 0.85) -> bool:
        """Check if a circuit pattern matches this hardware fingerprint"""
        if pattern.hardware_type != self.hardware_type:
            return False
        
        # Compare architecture characteristics
        similarity_score = self._calculate_similarity(pattern)
        return similarity_score >= threshold
    
    def _calculate_similarity(self, pattern: QuantumCircuitPattern) -> float:
        """Calculate similarity score between pattern and fingerprint"""
        scores = []
        
        # Gate set similarity
        expected_gates = self.architecture_characteristics.get('native_gate_set', set())
        pattern_gates = pattern.native_gate_set
        if expected_gates and pattern_gates:
            gate_overlap = len(expected_gates & pattern_gates) / len(expected_gates | pattern_gates)
            scores.append(gate_overlap)
        
        # Fidelity profile similarity
        expected_fidelities = self.architecture_characteristics.get('fidelity_profile', [])
        if expected_fidelities and pattern.gate_fidelities:
            pattern_fidelities = pattern._get_fidelity_profile()
            fidelity_similarity = self._vector_similarity(expected_fidelities, pattern_fidelities)
            scores.append(fidelity_similarity)
        
        # Timing profile similarity
        expected_timings = self.architecture_characteristics.get('timing_profile', [])
        if expected_timings and pattern.gate_times:
            pattern_timings = pattern._get_timing_profile()
            timing_similarity = self._vector_similarity(expected_timings, pattern_timings)
            scores.append(timing_similarity)
        
        return np.mean(scores) if scores else 0.0
    
    def _vector_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not vec1 or not vec2:
            return 0.0
        
        # Pad shorter vector with zeros
        max_len = max(len(vec1), len(vec2))
        vec1_padded = vec1 + [0.0] * (max_len - len(vec1))
        vec2_padded = vec2 + [0.0] * (max_len - len(vec2))
        
        # Cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1_padded, vec2_padded))
        magnitude1 = sum(a * a for a in vec1_padded) ** 0.5
        magnitude2 = sum(a * a for a in vec2_padded) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


class QuantumCircuitFingerprintEngine:
    def __init__(self):
        self.circuit_patterns: Dict[str, QuantumCircuitPattern] = {}
        self.hardware_fingerprints: Dict[str, HardwareFingerprint] = {}
        self.attack_signatures: Dict[str, List[str]] = defaultdict(list)  # hardware -> pattern_ids
        self.real_time_analysis: Dict[str, Any] = {}
        
        # Initialize known hardware fingerprints
        self._initialize_hardware_fingerprints()
        
        # Monitoring
        self.monitoring_active = False
        self.detection_statistics: Dict[str, int] = defaultdict(int)
    
    def _initialize_hardware_fingerprints(self):
        """Initialize known quantum hardware fingerprints"""
        
        # IBM Quantum (superconducting qubits)
        ibm_fingerprint = HardwareFingerprint(
            fingerprint_id="ibm_quantum_main",
            hardware_type=QuantumHardwareType.IBM_QUANTUM,
            vendor_signature="ibm_quantum_network",
            architecture_characteristics={
                'native_gate_set': {
                    QuantumGateType.RZ_ROTATION, QuantumGateType.RX_ROTATION,
                    QuantumGateType.CNOT, QuantumGateType.MEASUREMENT
                },
                'fidelity_profile': [0.999, 0.995, 0.990, 0.980],  # Single-qubit, two-qubit gates
                'timing_profile': [0.04, 0.2, 0.5, 1.0],  # Gate times in microseconds
                'topology': 'heavy_hex',
                'coherence_t1': 150.0,  # microseconds
                'coherence_t2': 200.0,
                'max_qubits': 127,
                'calibration_frequency': 'daily'
            },
            noise_profile={
                'readout_error': 0.02,
                'gate_error_1q': 0.001,
                'gate_error_2q': 0.01,
                'thermal_noise': 0.0001,
                'crosstalk': 0.005
            },
            calibration_timestamp=time.time(),
            confidence_score=0.95
        )
        self.hardware_fingerprints["ibm_quantum_main"] = ibm_fingerprint
        
        # Google Quantum (Sycamore processor)
        google_fingerprint = HardwareFingerprint(
            fingerprint_id="google_sycamore",
            hardware_type=QuantumHardwareType.GOOGLE_QUANTUM,
            vendor_signature="google_quantum_ai",
            architecture_characteristics={
                'native_gate_set': {
                    QuantumGateType.RZ_ROTATION, QuantumGateType.RY_ROTATION,
                    QuantumGateType.CZ_GATE, QuantumGateType.MEASUREMENT
                },
                'fidelity_profile': [0.9995, 0.993, 0.985, 0.975],
                'timing_profile': [0.02, 0.15, 0.3, 0.8],
                'topology': 'grid_2d',
                'coherence_t1': 80.0,
                'coherence_t2': 120.0,
                'max_qubits': 70,
                'calibration_frequency': 'continuous'
            },
            noise_profile={
                'readout_error': 0.015,
                'gate_error_1q': 0.0005,
                'gate_error_2q': 0.007,
                'thermal_noise': 0.00005,
                'crosstalk': 0.003
            },
            calibration_timestamp=time.time(),
            confidence_score=0.98
        )
        self.hardware_fingerprints["google_sycamore"] = google_fingerprint
        
        # IonQ (trapped ion)
        ionq_fingerprint = HardwareFingerprint(
            fingerprint_id="ionq_trapped_ion",
            hardware_type=QuantumHardwareType.IONQ_TRAPPED_ION,
            vendor_signature="ionq_systems",
            architecture_characteristics={
                'native_gate_set': {
                    QuantumGateType.RX_ROTATION, QuantumGateType.RY_ROTATION,
                    QuantumGateType.RZ_ROTATION, QuantumGateType.MOLMER_SORENSEN,
                    QuantumGateType.MEASUREMENT
                },
                'fidelity_profile': [0.9999, 0.995, 0.990, 0.985],
                'timing_profile': [10.0, 50.0, 100.0, 200.0],  # Much slower but higher fidelity
                'topology': 'all_to_all',  # Can perform operations between any qubits
                'coherence_t1': 10000.0,  # Much longer coherence
                'coherence_t2': 5000.0,
                'max_qubits': 32,
                'calibration_frequency': 'weekly'
            },
            noise_profile={
                'readout_error': 0.001,
                'gate_error_1q': 0.0001,
                'gate_error_2q': 0.005,
                'thermal_noise': 0.000001,
                'crosstalk': 0.0001
            },
            calibration_timestamp=time.time(),
            confidence_score=0.92
        )
        self.hardware_fingerprints["ionq_trapped_ion"] = ionq_fingerprint
        
        # D-Wave (quantum annealing)
        dwave_fingerprint = HardwareFingerprint(
            fingerprint_id="dwave_advantage",
            hardware_type=QuantumHardwareType.DWAVE_ANNEALING,
            vendor_signature="dwave_systems",
            architecture_characteristics={
                'native_gate_set': {
                    QuantumGateType.NATIVE_GATE  # Ising model operations
                },
                'fidelity_profile': [0.99, 0.95, 0.90],  # Annealing fidelity
                'timing_profile': [20000.0],  # 20ms annealing time
                'topology': 'chimera_pegasus',
                'coherence_t1': 50.0,
                'coherence_t2': 25.0,
                'max_qubits': 5760,
                'calibration_frequency': 'continuous'
            },
            noise_profile={
                'readout_error': 0.05,
                'annealing_error': 0.01,
                'thermal_noise': 0.001,
                'programming_error': 0.02,
                'crosstalk': 0.01
            },
            calibration_timestamp=time.time(),
            confidence_score=0.88
        )
        self.hardware_fingerprints["dwave_advantage"] = dwave_fingerprint
    
    def analyze_quantum_circuit_signature(
        self,
        access_pattern: List[Dict],
        source_identifier: str
    ) -> Optional[QuantumCircuitPattern]:
        """Analyze access patterns to identify quantum circuit signatures"""
        
        if len(access_pattern) < 5:
            return None
        
        current_time = time.time()
        
        # Extract circuit characteristics from access patterns
        gate_sequence = self._extract_gate_sequence(access_pattern)
        qubit_connectivity = self._analyze_connectivity(access_pattern)
        gate_timings = self._extract_gate_timings(access_pattern)
        error_characteristics = self._analyze_error_patterns(access_pattern)
        
        # Identify hardware type based on patterns
        hardware_type = self._classify_hardware_type(
            gate_sequence, qubit_connectivity, gate_timings, error_characteristics
        )
        
        # Create circuit pattern
        pattern = QuantumCircuitPattern(
            pattern_id=f"circuit_{secrets.token_hex(8)}_{int(current_time)}",
            hardware_type=hardware_type,
            gate_sequence=gate_sequence,
            qubit_connectivity=qubit_connectivity,
            gate_fidelities=self._estimate_gate_fidelities(access_pattern),
            coherence_times=self._estimate_coherence_times(access_pattern),
            gate_times=gate_timings,
            error_rates=error_characteristics,
            native_gate_set=self._identify_native_gates(gate_sequence, hardware_type),
            pattern_confidence=self._calculate_pattern_confidence(access_pattern),
            detection_timestamp=current_time,
            circuit_depth=self._calculate_circuit_depth(gate_sequence),
            qubit_count=len(qubit_connectivity)
        )
        
        self.circuit_patterns[pattern.pattern_id] = pattern
        
        # Check for attack signatures
        self._check_attack_signatures(pattern, source_identifier)
        
        return pattern
    
    def _extract_gate_sequence(self, access_pattern: List[Dict]) -> List[QuantumGateType]:
        """Extract quantum gate sequence from access patterns"""
        gate_sequence = []
        
        for access in access_pattern:
            # Analyze access timing and values to infer gate types
            access_time_delta = access.get('time_delta', 0.0)
            query_type = access.get('query_type', '')
            value_pattern = access.get('value', '')
            
            # Single-qubit gate patterns (fast, localized)
            if access_time_delta < 0.1 and 'single' in query_type.lower():
                if 'hadamard' in value_pattern.lower():
                    gate_sequence.append(QuantumGateType.HADAMARD)
                elif 'rotation' in value_pattern.lower():
                    if 'x' in value_pattern.lower():
                        gate_sequence.append(QuantumGateType.RX_ROTATION)
                    elif 'y' in value_pattern.lower():
                        gate_sequence.append(QuantumGateType.RY_ROTATION)
                    elif 'z' in value_pattern.lower():
                        gate_sequence.append(QuantumGateType.RZ_ROTATION)
                elif 'pauli' in value_pattern.lower():
                    gate_sequence.append(QuantumGateType.PAULI_X)
            
            # Two-qubit gate patterns (slower, involves pairs)
            elif 0.1 <= access_time_delta < 1.0:
                if 'cnot' in value_pattern.lower() or 'cx' in value_pattern.lower():
                    gate_sequence.append(QuantumGateType.CNOT)
                elif 'cz' in value_pattern.lower():
                    gate_sequence.append(QuantumGateType.CZ_GATE)
                elif 'swap' in value_pattern.lower():
                    gate_sequence.append(QuantumGateType.SWAP)
            
            # Measurement patterns (distinctive readout signatures)
            elif 'measure' in query_type.lower() or 'readout' in query_type.lower():
                gate_sequence.append(QuantumGateType.MEASUREMENT)
            
            # Hardware-specific patterns
            elif access_time_delta > 10.0:  # Very slow operations
                if 'ion' in query_type.lower():
                    gate_sequence.append(QuantumGateType.MOLMER_SORENSEN)
                else:
                    gate_sequence.append(QuantumGateType.NATIVE_GATE)
        
        return gate_sequence
    
    def _analyze_connectivity(self, access_pattern: List[Dict]) -> Dict[int, Set[int]]:
        """Analyze qubit connectivity topology from access patterns"""
        connectivity = defaultdict(set)
        
        for access in access_pattern:
            # Extract qubit indices from access patterns
            input_val = access.get('input', 0)
            output_val = access.get('output', 0)
            
            # Infer qubit indices from numerical patterns
            if isinstance(input_val, int) and isinstance(output_val, int):
                qubit1 = input_val % 100  # Assume qubit indices are encoded
                qubit2 = output_val % 100
                
                if qubit1 != qubit2 and 0 <= qubit1 < 200 and 0 <= qubit2 < 200:
                    connectivity[qubit1].add(qubit2)
                    connectivity[qubit2].add(qubit1)
        
        # Convert to regular dict
        return {qubit: neighbors for qubit, neighbors in connectivity.items()}
    
    def _extract_gate_timings(self, access_pattern: List[Dict]) -> Dict[QuantumGateType, float]:
        """Extract gate execution timings"""
        gate_timings = {}
        
        # Analyze timing patterns to estimate gate execution times
        timing_samples = [access.get('time_delta', 0.0) for access in access_pattern]
        
        if timing_samples:
            # Typical timings for different gate types
            min_time = min(t for t in timing_samples if t > 0)
            max_time = max(timing_samples)
            avg_time = np.mean([t for t in timing_samples if t > 0])
            
            # Estimate gate timings based on observed patterns
            gate_timings[QuantumGateType.RZ_ROTATION] = min_time
            gate_timings[QuantumGateType.RX_ROTATION] = min_time * 1.2
            gate_timings[QuantumGateType.HADAMARD] = min_time * 1.1
            gate_timings[QuantumGateType.CNOT] = avg_time
            gate_timings[QuantumGateType.MEASUREMENT] = max_time * 0.8
        
        return gate_timings
    
    def _analyze_error_patterns(self, access_pattern: List[Dict]) -> Dict[QuantumGateType, float]:
        """Analyze error characteristics from access patterns"""
        error_rates = {}
        
        # Look for error indicators in access patterns
        error_indicators = []
        for access in access_pattern:
            # Check for inconsistencies that might indicate errors
            if 'error' in str(access).lower():
                error_indicators.append(1)
            else:
                error_indicators.append(0)
        
        if error_indicators:
            overall_error_rate = np.mean(error_indicators)
            
            # Estimate error rates for different gate types
            error_rates[QuantumGateType.RZ_ROTATION] = overall_error_rate * 0.1
            error_rates[QuantumGateType.CNOT] = overall_error_rate * 1.0
            error_rates[QuantumGateType.MEASUREMENT] = overall_error_rate * 2.0
        
        return error_rates
    
    def _classify_hardware_type(
        self,
        gate_sequence: List[QuantumGateType],
        connectivity: Dict[int, Set[int]],
        timings: Dict[QuantumGateType, float],
        errors: Dict[QuantumGateType, float]
    ) -> QuantumHardwareType:
        """Classify quantum hardware type based on circuit characteristics"""
        
        # Check for D-Wave annealing signatures
        if QuantumGateType.NATIVE_GATE in gate_sequence and len(connectivity) > 1000:
            return QuantumHardwareType.DWAVE_ANNEALING
        
        # Check for trapped ion signatures (slow but high fidelity)
        if timings and max(timings.values()) > 10.0:  # Very slow gates
            if QuantumGateType.MOLMER_SORENSEN in gate_sequence:
                return QuantumHardwareType.IONQ_TRAPPED_ION
        
        # Check for superconducting qubit signatures
        if QuantumGateType.CNOT in gate_sequence and QuantumGateType.RZ_ROTATION in gate_sequence:
            # Distinguish IBM vs Google based on specific patterns
            if QuantumGateType.CZ_GATE in gate_sequence:
                return QuantumHardwareType.GOOGLE_QUANTUM
            else:
                return QuantumHardwareType.IBM_QUANTUM
        
        # Default to unknown
        return QuantumHardwareType.UNKNOWN_HARDWARE
    
    def _estimate_gate_fidelities(self, access_pattern: List[Dict]) -> Dict[QuantumGateType, float]:
        """Estimate gate fidelities from access patterns"""
        fidelities = {}
        
        # Analyze pattern consistency to estimate fidelities
        consistency_score = self._calculate_pattern_consistency(access_pattern)
        base_fidelity = 0.95 + consistency_score * 0.05  # Scale between 0.95-1.0
        
        # Different gate types have different fidelity characteristics
        fidelities[QuantumGateType.RZ_ROTATION] = min(0.9999, base_fidelity * 1.01)
        fidelities[QuantumGateType.HADAMARD] = min(0.999, base_fidelity * 1.005)
        fidelities[QuantumGateType.CNOT] = min(0.99, base_fidelity * 0.98)
        fidelities[QuantumGateType.MEASUREMENT] = min(0.98, base_fidelity * 0.95)
        
        return fidelities
    
    def _estimate_coherence_times(self, access_pattern: List[Dict]) -> Dict[int, float]:
        """Estimate qubit coherence times"""
        coherence_times = {}
        
        # Analyze timing patterns to estimate coherence
        max_time = max([access.get('time_delta', 0.0) for access in access_pattern])
        
        # Estimate T1 and T2 times based on observed operation durations
        estimated_t1 = max_time * 100  # Rough estimate
        estimated_t2 = estimated_t1 * 0.8
        
        # Apply to observed qubits
        for i in range(min(10, len(access_pattern))):  # Limit to reasonable number
            coherence_times[i] = estimated_t1
        
        return coherence_times
    
    def _identify_native_gates(
        self,
        gate_sequence: List[QuantumGateType],
        hardware_type: QuantumHardwareType
    ) -> Set[QuantumGateType]:
        """Identify native gate set for hardware type"""
        
        if hardware_type == QuantumHardwareType.IBM_QUANTUM:
            return {QuantumGateType.RZ_ROTATION, QuantumGateType.RX_ROTATION, QuantumGateType.CNOT}
        elif hardware_type == QuantumHardwareType.GOOGLE_QUANTUM:
            return {QuantumGateType.RZ_ROTATION, QuantumGateType.RY_ROTATION, QuantumGateType.CZ_GATE}
        elif hardware_type == QuantumHardwareType.IONQ_TRAPPED_ION:
            return {QuantumGateType.RX_ROTATION, QuantumGateType.RY_ROTATION, QuantumGateType.RZ_ROTATION, QuantumGateType.MOLMER_SORENSEN}
        elif hardware_type == QuantumHardwareType.DWAVE_ANNEALING:
            return {QuantumGateType.NATIVE_GATE}
        else:
            # Extract from observed gate sequence
            return set(gate_sequence)
    
    def _calculate_pattern_confidence(self, access_pattern: List[Dict]) -> float:
        """Calculate confidence score for pattern recognition"""
        confidence_factors = []
        
        # Pattern length factor
        length_factor = min(1.0, len(access_pattern) / 20.0)
        confidence_factors.append(length_factor)
        
        # Timing consistency factor
        timing_consistency = self._calculate_timing_consistency(access_pattern)
        confidence_factors.append(timing_consistency)
        
        # Value pattern consistency
        pattern_consistency = self._calculate_pattern_consistency(access_pattern)
        confidence_factors.append(pattern_consistency)
        
        return np.mean(confidence_factors)
    
    def _calculate_timing_consistency(self, access_pattern: List[Dict]) -> float:
        """Calculate timing consistency score"""
        timings = [access.get('time_delta', 0.0) for access in access_pattern]
        timings = [t for t in timings if t > 0]
        
        if len(timings) < 3:
            return 0.5
        
        # Calculate coefficient of variation
        mean_timing = np.mean(timings)
        std_timing = np.std(timings)
        
        if mean_timing == 0:
            return 0.0
        
        cv = std_timing / mean_timing
        # Convert to consistency score (lower variation = higher consistency)
        return max(0.0, 1.0 - cv)
    
    def _calculate_pattern_consistency(self, access_pattern: List[Dict]) -> float:
        """Calculate pattern consistency score"""
        if len(access_pattern) < 2:
            return 0.0
        
        # Look for recurring patterns in values
        values = [str(access.get('value', '')) for access in access_pattern]
        unique_values = len(set(values))
        total_values = len(values)
        
        # Higher repetition suggests more consistent patterns
        repetition_score = 1.0 - (unique_values / total_values)
        
        return max(0.0, min(1.0, repetition_score))
    
    def _calculate_circuit_depth(self, gate_sequence: List[QuantumGateType]) -> int:
        """Calculate circuit depth (number of time steps)"""
        # Simplified calculation - assumes sequential execution
        return len([gate for gate in gate_sequence if gate != QuantumGateType.MEASUREMENT])
    
    def _check_attack_signatures(self, pattern: QuantumCircuitPattern, source_identifier: str):
        """Check if pattern matches known attack signatures"""
        
        # Check against known hardware fingerprints
        for fingerprint_id, fingerprint in self.hardware_fingerprints.items():
            if fingerprint.matches_pattern(pattern):
                self.attack_signatures[fingerprint.hardware_type.value].append(pattern.pattern_id)
                
                # Log potential attack
                print(f"QUANTUM HARDWARE ATTACK DETECTED: {fingerprint.hardware_type.value}")
                print(f"Pattern: {pattern.pattern_id}")
                print(f"Source: {source_identifier}")
                print(f"Confidence: {pattern.pattern_confidence:.3f}")
                
                self.detection_statistics[fingerprint.hardware_type.value] += 1
    
    def get_hardware_detection_statistics(self) -> Dict[str, Any]:
        """Get comprehensive hardware detection statistics"""
        current_time = time.time()
        
        stats = {
            'total_patterns_analyzed': len(self.circuit_patterns),
            'hardware_types_detected': dict(self.detection_statistics),
            'known_hardware_fingerprints': len(self.hardware_fingerprints),
            'attack_signatures_found': sum(len(sigs) for sigs in self.attack_signatures.values()),
            'hardware_fingerprint_details': {},
            'recent_detections': [],
            'confidence_distribution': []
        }
        
        # Add fingerprint details
        for fp_id, fingerprint in self.hardware_fingerprints.items():
            stats['hardware_fingerprint_details'][fp_id] = {
                'hardware_type': fingerprint.hardware_type.value,
                'confidence': fingerprint.confidence_score,
                'max_qubits': fingerprint.architecture_characteristics.get('max_qubits', 0),
                'topology': fingerprint.architecture_characteristics.get('topology', 'unknown'),
                'native_gates': len(fingerprint.architecture_characteristics.get('native_gate_set', set()))
            }
        
        # Recent detections (last 5 minutes)
        recent_patterns = [
            pattern for pattern in self.circuit_patterns.values()
            if current_time - pattern.detection_timestamp < 300.0
        ]
        
        stats['recent_detections'] = [
            {
                'pattern_id': pattern.pattern_id,
                'hardware_type': pattern.hardware_type.value,
                'confidence': pattern.pattern_confidence,
                'qubit_count': pattern.qubit_count,
                'circuit_depth': pattern.circuit_depth,
                'detection_time': pattern.detection_timestamp
            }
            for pattern in recent_patterns
        ]
        
        # Confidence distribution
        if self.circuit_patterns:
            confidences = [p.pattern_confidence for p in self.circuit_patterns.values()]
            stats['confidence_distribution'] = {
                'mean': np.mean(confidences),
                'std': np.std(confidences),
                'min': np.min(confidences),
                'max': np.max(confidences),
                'high_confidence_count': sum(1 for c in confidences if c > 0.8)
            }
        
        return stats
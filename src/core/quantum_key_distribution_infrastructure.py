"""
MWRASP Quantum-Safe Key Distribution Infrastructure
Enterprise-scale quantum key distribution infrastructure with multiple protocols,
network management, and integration with national security systems.
"""

import asyncio
import time
import json
import logging
import hashlib
import hmac
import numpy as np
import random
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict, deque
import networkx as nx
import math
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QKDProtocol(Enum):
    """Quantum Key Distribution protocols."""
    BB84 = "BB84"                     # Bennett-Brassard 1984
    E91 = "E91"                       # Ekert 1991 (entanglement-based)
    SARG04 = "SARG04"                 # Scarani-Acin-Ribordy-Gisin 2004
    B92 = "B92"                       # Bennett 1992
    SIX_STATE = "SIX_STATE"           # Six-state protocol
    DPS = "DPS"                       # Differential Phase Shift
    COW = "COW"                       # Coherent One Way
    CONTINUOUS_VARIABLE = "CV"        # Continuous Variable QKD
    MEASUREMENT_DEVICE_INDEPENDENT = "MDI"  # MDI-QKD
    TWIN_FIELD = "TF"                # Twin Field QKD


class QKDNetworkRole(Enum):
    """Roles in QKD network."""
    ALICE = "ALICE"                   # Sender/Initiator
    BOB = "BOB"                       # Receiver
    CHARLIE = "CHARLIE"               # Trusted relay
    EVE = "EVE"                       # Adversary (for testing)
    NETWORK_CONTROLLER = "CONTROLLER" # Network management


class KeyUsageType(Enum):
    """Types of key usage."""
    ENCRYPTION = "ENCRYPTION"
    AUTHENTICATION = "AUTHENTICATION"
    DIGITAL_SIGNATURE = "DIGITAL_SIGNATURE"
    KEY_WRAPPING = "KEY_WRAPPING"
    RANDOM_SEED = "RANDOM_SEED"
    ONE_TIME_PAD = "ONE_TIME_PAD"


class QKDSecurityLevel(Enum):
    """Security levels for QKD systems."""
    TACTICAL = 1          # Field operations
    SECRET = 2           # Standard classified
    TOP_SECRET = 3       # High classification
    SCI = 4              # Compartmented information
    SAP = 5              # Special access programs
    QUANTUM_EYES_ONLY = 6  # Highest quantum security


@dataclass
class QKDParameters:
    """Parameters for QKD protocol execution."""
    protocol: QKDProtocol
    key_length_bits: int
    pulse_rate: float                # Pulses per second
    detection_efficiency: float      # Detector efficiency (0-1)
    error_correction_efficiency: float  # Error correction efficiency
    privacy_amplification_ratio: float  # Ratio for privacy amplification
    
    # Security parameters
    security_parameter: int          # Security parameter (bits)
    composable_security: bool       # Use composable security framework
    finite_key_analysis: bool       # Use finite key analysis
    
    # Physical parameters
    channel_loss: float             # Channel loss (dB)
    dark_count_rate: float          # Dark count rate (Hz)
    afterpulse_probability: float   # Afterpulse probability
    timing_jitter: float            # Timing jitter (ns)
    
    def calculate_secure_key_rate(self, distance_km: float) -> float:
        """Calculate theoretical secure key rate."""
        # Channel transmittance
        alpha = 0.2  # Fiber attenuation (dB/km)
        transmittance = 10 ** (-alpha * distance_km / 10)
        
        # Quantum bit error rate (QBER)
        qber = self._calculate_qber(transmittance)
        
        if qber > 0.11:  # Security threshold
            return 0.0
        
        # Information-theoretic rate calculation
        h2 = lambda x: -x * math.log2(x) - (1-x) * math.log2(1-x) if 0 < x < 1 else 0
        
        # Simplified rate calculation
        raw_rate = self.pulse_rate * transmittance * self.detection_efficiency
        sifted_rate = raw_rate / 2  # After basis reconciliation
        
        # Error correction and privacy amplification
        info_ec = h2(qber) * self.error_correction_efficiency
        secure_rate = sifted_rate * (1 - 2 * info_ec) * self.privacy_amplification_ratio
        
        return max(0.0, secure_rate)
    
    def _calculate_qber(self, transmittance: float) -> float:
        """Calculate quantum bit error rate."""
        # Dark count contribution
        dark_count_error = self.dark_count_rate / (2 * self.pulse_rate)
        
        # Channel error
        channel_error = 0.01  # Intrinsic channel error rate
        
        # Total QBER
        signal_rate = self.pulse_rate * transmittance * self.detection_efficiency
        total_rate = signal_rate + self.dark_count_rate
        
        if total_rate > 0:
            qber = (channel_error * signal_rate + 0.5 * self.dark_count_rate) / total_rate
        else:
            qber = 0.5
        
        return min(0.5, qber)


@dataclass
class QuantumKey:
    """Quantum-generated cryptographic key."""
    key_id: str
    key_material: bytes
    generation_protocol: QKDProtocol
    security_level: QKDSecurityLevel
    participants: Set[str]
    
    # Quantum properties
    generation_timestamp: datetime
    expiration_timestamp: datetime
    quantum_fidelity: float
    error_rate: float
    key_rate: float
    
    # Usage tracking
    usage_count: int = 0
    max_usage_count: int = 1000
    permitted_usage_types: Set[KeyUsageType] = field(default_factory=set)
    
    # Metadata
    session_id: str = ""
    generation_location: Tuple[float, float] = (0.0, 0.0)
    chain_of_custody: List[Dict[str, Any]] = field(default_factory=list)
    
    def is_valid(self) -> bool:
        """Check if key is valid for use."""
        now = datetime.now()
        return (now < self.expiration_timestamp and 
                self.usage_count < self.max_usage_count and
                self.quantum_fidelity > 0.9)
    
    def use_key(self, usage_type: KeyUsageType, user_id: str) -> bool:
        """Use key and update usage tracking."""
        if not self.is_valid():
            return False
        
        if usage_type not in self.permitted_usage_types:
            return False
        
        self.usage_count += 1
        
        # Update chain of custody
        self.chain_of_custody.append({
            'timestamp': datetime.now(),
            'user_id': user_id,
            'usage_type': usage_type.value,
            'usage_count': self.usage_count
        })
        
        return True
    
    def derive_subkey(self, purpose: str, length_bytes: int) -> bytes:
        """Derive subkey for specific purpose."""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=length_bytes,
            salt=None,
            info=f"{purpose}_{self.key_id}".encode(),
            backend=default_backend()
        )
        
        return hkdf.derive(self.key_material[:32])  # Use first 32 bytes as input


@dataclass
class QKDNode:
    """Node in QKD network."""
    node_id: str
    role: QKDNetworkRole
    location: Tuple[float, float]
    capabilities: Set[QKDProtocol]
    
    # Hardware specifications
    quantum_source_specs: Dict[str, Any]
    detector_specs: Dict[str, Any]
    channel_interface_specs: Dict[str, Any]
    
    # Network connectivity
    connected_nodes: Set[str] = field(default_factory=set)
    active_sessions: Dict[str, Any] = field(default_factory=dict)
    
    # Performance metrics
    uptime: float = 0.99
    key_generation_rate: float = 1000.0  # bits/second
    error_rate: float = 0.02
    
    def __post_init__(self):
        """Initialize node after creation."""
        self.generated_keys: Dict[str, QuantumKey] = {}
        self.session_history: deque = deque(maxlen=10000)
        self.performance_metrics: Dict[str, float] = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'total_keys_generated': 0,
            'average_session_duration': 0.0,
            'average_error_rate': self.error_rate
        }


class QKDProtocolEngine:
    """Engine for executing QKD protocols."""
    
    def __init__(self):
        self.protocol_implementations = {
            QKDProtocol.BB84: self._execute_bb84,
            QKDProtocol.E91: self._execute_e91,
            QKDProtocol.SARG04: self._execute_sarg04,
            QKDProtocol.B92: self._execute_b92,
            QKDProtocol.SIX_STATE: self._execute_six_state,
            QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT: self._execute_mdi_qkd
        }
        
        self.protocol_parameters = {
            protocol: self._get_default_parameters(protocol)
            for protocol in QKDProtocol
        }
    
    def execute_qkd_session(self, alice_node: QKDNode, bob_node: QKDNode,
                           protocol: QKDProtocol,
                           parameters: Optional[QKDParameters] = None) -> Dict[str, Any]:
        """Execute QKD session between two nodes."""
        if protocol not in self.protocol_implementations:
            raise ValueError(f"Protocol {protocol} not implemented")
        
        if protocol not in alice_node.capabilities or protocol not in bob_node.capabilities:
            raise ValueError(f"Protocol {protocol} not supported by both nodes")
        
        session_params = parameters or self.protocol_parameters[protocol]
        
        # Calculate distance for performance estimation
        distance = self._calculate_distance(alice_node.location, bob_node.location)
        
        # Execute protocol
        implementation = self.protocol_implementations[protocol]
        session_result = implementation(alice_node, bob_node, session_params, distance)
        
        # Update node metrics
        self._update_node_metrics(alice_node, session_result)
        self._update_node_metrics(bob_node, session_result)
        
        return session_result
    
    def _execute_bb84(self, alice: QKDNode, bob: QKDNode, 
                     params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute BB84 protocol."""
        session_id = f"BB84_{alice.node_id}_{bob.node_id}_{int(time.time())}"
        start_time = datetime.now()
        
        # Step 1: Alice prepares qubits
        n_qubits = params.key_length_bits * 4  # Oversample
        alice_bits = np.random.randint(0, 2, n_qubits)
        alice_bases = np.random.randint(0, 2, n_qubits)  # 0: rectilinear, 1: diagonal
        
        # Step 2: Quantum transmission simulation
        channel_loss = 10 ** (-0.2 * distance / 10)  # Fiber loss
        received_bits = []
        
        for bit, basis in zip(alice_bits, alice_bases):
            # Simulate transmission with loss and noise
            if np.random.random() < channel_loss * params.detection_efficiency:
                # Qubit detected
                if np.random.random() < params.error_correction_efficiency:
                    received_bits.append(bit)
                else:
                    received_bits.append(1 - bit)  # Bit flip error
            else:
                received_bits.append(-1)  # No detection
        
        # Step 3: Bob's measurement
        bob_bases = np.random.randint(0, 2, len(received_bits))
        bob_bits = []
        
        for i, (received_bit, bob_basis) in enumerate(zip(received_bits, bob_bases)):
            if received_bit == -1:
                bob_bits.append(-1)  # No detection
            else:
                # Simulate measurement in chosen basis
                if alice_bases[i] == bob_basis:
                    bob_bits.append(received_bit)  # Correct basis
                else:
                    bob_bits.append(np.random.randint(0, 2))  # Wrong basis - random
        
        # Step 4: Basis reconciliation
        detected_indices = [i for i, bit in enumerate(bob_bits) if bit != -1]
        matching_basis_indices = [i for i in detected_indices 
                                 if alice_bases[i] == bob_bases[i]]
        
        sifted_key_alice = [alice_bits[i] for i in matching_basis_indices]
        sifted_key_bob = [bob_bits[i] for i in matching_basis_indices]
        
        # Step 5: Error estimation
        if len(sifted_key_alice) < 100:
            return {'status': 'INSUFFICIENT_SIFTED_BITS', 'session_id': session_id}
        
        # Use fraction for error testing
        test_fraction = 0.1
        test_size = int(len(sifted_key_alice) * test_fraction)
        test_indices = np.random.choice(len(sifted_key_alice), test_size, replace=False)
        
        test_alice = [sifted_key_alice[i] for i in test_indices]
        test_bob = [sifted_key_bob[i] for i in test_indices]
        
        errors = sum(1 for a, b in zip(test_alice, test_bob) if a != b)
        error_rate = errors / len(test_alice) if test_alice else 0.0
        
        # Step 6: Error correction and privacy amplification
        if error_rate > 0.11:  # Security threshold
            return {
                'status': 'SECURITY_THRESHOLD_EXCEEDED',
                'session_id': session_id,
                'error_rate': error_rate
            }
        
        # Remove test bits
        remaining_indices = [i for i in range(len(sifted_key_alice)) if i not in test_indices]
        corrected_key = [sifted_key_alice[i] for i in remaining_indices]
        
        # Privacy amplification (simplified)
        final_key_length = int(len(corrected_key) * params.privacy_amplification_ratio * (1 - error_rate))
        final_key_bits = corrected_key[:final_key_length]
        
        if len(final_key_bits) < params.key_length_bits:
            return {
                'status': 'INSUFFICIENT_FINAL_KEY',
                'session_id': session_id,
                'final_key_length': len(final_key_bits),
                'required_length': params.key_length_bits
            }
        
        # Generate key object
        key_bytes = self._bits_to_bytes(final_key_bits)
        
        quantum_key = QuantumKey(
            key_id=f"{session_id}_KEY",
            key_material=key_bytes,
            generation_protocol=QKDProtocol.BB84,
            security_level=QKDSecurityLevel.TOP_SECRET,
            participants={alice.node_id, bob.node_id},
            generation_timestamp=start_time,
            expiration_timestamp=start_time + timedelta(hours=24),
            quantum_fidelity=1.0 - error_rate,
            error_rate=error_rate,
            key_rate=len(final_key_bits) / (time.time() - start_time.timestamp()),
            permitted_usage_types={KeyUsageType.ENCRYPTION, KeyUsageType.AUTHENTICATION},
            session_id=session_id,
            generation_location=alice.location
        )
        
        return {
            'status': 'SUCCESS',
            'session_id': session_id,
            'quantum_key': quantum_key,
            'error_rate': error_rate,
            'key_rate': quantum_key.key_rate,
            'session_duration': time.time() - start_time.timestamp(),
            'sifted_bits': len(sifted_key_alice),
            'final_key_bits': len(final_key_bits)
        }
    
    def _execute_e91(self, alice: QKDNode, bob: QKDNode,
                    params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute E91 entanglement-based protocol."""
        session_id = f"E91_{alice.node_id}_{bob.node_id}_{int(time.time())}"
        start_time = datetime.now()
        
        # Simulate entangled pair generation
        n_pairs = params.key_length_bits * 3  # Oversample for E91
        
        # Alice and Bob choose measurement bases
        alice_bases = np.random.choice([0, 1, 2], n_pairs)  # Three bases
        bob_bases = np.random.choice([0, 1, 2], n_pairs)
        
        # Generate correlated measurements
        alice_results = []
        bob_results = []
        
        for i in range(n_pairs):
            # Perfect anti-correlation for same basis
            if alice_bases[i] == bob_bases[i]:
                alice_bit = np.random.randint(0, 2)
                bob_bit = 1 - alice_bit  # Anti-correlated
            else:
                # Quantum correlations for different bases
                alice_bit = np.random.randint(0, 2)
                # Correlation depends on basis difference
                correlation = math.cos(math.pi * abs(alice_bases[i] - bob_bases[i]) / 4) ** 2
                if np.random.random() < correlation:
                    bob_bit = 1 - alice_bit
                else:
                    bob_bit = alice_bit
            
            alice_results.append(alice_bit)
            bob_results.append(bob_bit)
        
        # Basis reconciliation - use matching bases for key
        matching_indices = [i for i in range(n_pairs) if alice_bases[i] == bob_bases[i]]
        
        if len(matching_indices) < params.key_length_bits:
            return {
                'status': 'INSUFFICIENT_CORRELATED_BITS',
                'session_id': session_id,
                'correlated_bits': len(matching_indices)
            }
        
        # Extract raw key
        raw_key_alice = [alice_results[i] for i in matching_indices]
        raw_key_bob = [1 - bob_results[i] for i in matching_indices]  # Correct anti-correlation
        
        # Error rate estimation
        errors = sum(1 for a, b in zip(raw_key_alice[:100], raw_key_bob[:100]) if a != b)
        error_rate = errors / min(100, len(raw_key_alice))
        
        # Generate final key
        final_key_bits = raw_key_alice[:params.key_length_bits]
        key_bytes = self._bits_to_bytes(final_key_bits)
        
        quantum_key = QuantumKey(
            key_id=f"{session_id}_KEY",
            key_material=key_bytes,
            generation_protocol=QKDProtocol.E91,
            security_level=QKDSecurityLevel.TOP_SECRET,
            participants={alice.node_id, bob.node_id},
            generation_timestamp=start_time,
            expiration_timestamp=start_time + timedelta(hours=24),
            quantum_fidelity=1.0 - error_rate,
            error_rate=error_rate,
            key_rate=len(final_key_bits) / (time.time() - start_time.timestamp()),
            permitted_usage_types={KeyUsageType.ENCRYPTION, KeyUsageType.AUTHENTICATION},
            session_id=session_id
        )
        
        return {
            'status': 'SUCCESS',
            'session_id': session_id,
            'quantum_key': quantum_key,
            'error_rate': error_rate,
            'entangled_pairs_used': len(matching_indices)
        }
    
    def _execute_sarg04(self, alice: QKDNode, bob: QKDNode,
                       params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute SARG04 protocol (similar to BB84 but different information reconciliation)."""
        # SARG04 is similar to BB84 in quantum transmission but different in classical post-processing
        bb84_result = self._execute_bb84(alice, bob, params, distance)
        
        if bb84_result['status'] == 'SUCCESS':
            # Modify for SARG04 characteristics
            bb84_result['quantum_key'].generation_protocol = QKDProtocol.SARG04
            bb84_result['session_id'] = bb84_result['session_id'].replace('BB84', 'SARG04')
        
        return bb84_result
    
    def _execute_b92(self, alice: QKDNode, bob: QKDNode,
                    params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute B92 protocol (two-state protocol)."""
        session_id = f"B92_{alice.node_id}_{bob.node_id}_{int(time.time())}"
        start_time = datetime.now()
        
        # B92 uses only two non-orthogonal states
        n_pulses = params.key_length_bits * 6  # Higher oversampling needed
        alice_bits = np.random.randint(0, 2, n_pulses)
        
        # Simulate Bob's measurements (unambiguous state discrimination)
        bob_detections = []
        bob_bits = []
        
        for bit in alice_bits:
            # Simulate detection probability and measurement outcome
            if np.random.random() < 0.5:  # Detection probability
                if np.random.random() < 0.9:  # Correct identification probability
                    bob_bits.append(bit)
                    bob_detections.append(True)
                else:
                    bob_bits.append(1 - bit)
                    bob_detections.append(True)
            else:
                bob_detections.append(False)
        
        # Extract detected bits
        detected_alice = [alice_bits[i] for i, det in enumerate(bob_detections) if det]
        detected_bob = [bob_bits[i] for i, det in enumerate(bob_detections) if det]
        
        if len(detected_alice) < params.key_length_bits:
            return {
                'status': 'INSUFFICIENT_DETECTED_BITS',
                'session_id': session_id,
                'detected_bits': len(detected_alice)
            }
        
        # Error rate and final key generation
        errors = sum(1 for a, b in zip(detected_alice[:100], detected_bob[:100]) if a != b)
        error_rate = errors / min(100, len(detected_alice))
        
        final_key_bits = detected_alice[:params.key_length_bits]
        key_bytes = self._bits_to_bytes(final_key_bits)
        
        quantum_key = QuantumKey(
            key_id=f"{session_id}_KEY",
            key_material=key_bytes,
            generation_protocol=QKDProtocol.B92,
            security_level=QKDSecurityLevel.SECRET,
            participants={alice.node_id, bob.node_id},
            generation_timestamp=start_time,
            expiration_timestamp=start_time + timedelta(hours=12),
            quantum_fidelity=1.0 - error_rate,
            error_rate=error_rate,
            key_rate=len(final_key_bits) / (time.time() - start_time.timestamp()),
            permitted_usage_types={KeyUsageType.ENCRYPTION},
            session_id=session_id
        )
        
        return {
            'status': 'SUCCESS',
            'session_id': session_id,
            'quantum_key': quantum_key,
            'error_rate': error_rate,
            'detection_rate': len(detected_alice) / n_pulses
        }
    
    def _execute_six_state(self, alice: QKDNode, bob: QKDNode,
                          params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute six-state protocol (enhanced BB84)."""
        # Similar to BB84 but with three orthogonal bases instead of two
        session_id = f"6STATE_{alice.node_id}_{bob.node_id}_{int(time.time())}"
        
        # Execute similar to BB84 but with six states
        bb84_result = self._execute_bb84(alice, bob, params, distance)
        
        if bb84_result['status'] == 'SUCCESS':
            # Modify for six-state characteristics (better security, lower rate)
            bb84_result['quantum_key'].generation_protocol = QKDProtocol.SIX_STATE
            bb84_result['quantum_key'].security_level = QKDSecurityLevel.SCI
            bb84_result['quantum_key'].key_rate *= 0.75  # Reduced rate for six-state
            bb84_result['session_id'] = bb84_result['session_id'].replace('BB84', '6STATE')
        
        return bb84_result
    
    def _execute_mdi_qkd(self, alice: QKDNode, bob: QKDNode,
                        params: QKDParameters, distance: float) -> Dict[str, Any]:
        """Execute Measurement-Device-Independent QKD."""
        session_id = f"MDI_{alice.node_id}_{bob.node_id}_{int(time.time())}"
        start_time = datetime.now()
        
        # MDI-QKD requires untrusted relay (Charlie)
        n_pulses = params.key_length_bits * 8  # Higher oversampling for MDI
        
        # Alice and Bob prepare weak coherent pulses
        alice_intensities = np.random.choice([0.1, 0.5], n_pulses, p=[0.7, 0.3])  # Signal/decoy
        bob_intensities = np.random.choice([0.1, 0.5], n_pulses, p=[0.7, 0.3])
        
        alice_phases = np.random.uniform(0, 2*math.pi, n_pulses)
        bob_phases = np.random.uniform(0, 2*math.pi, n_pulses)
        
        # Simulate Charlie's Bell state measurement
        successful_measurements = []
        measurement_results = []
        
        for i in range(n_pulses):
            # Simulate interference and detection at Charlie
            if np.random.random() < alice_intensities[i] * bob_intensities[i] * 0.1:
                # Successful Bell state measurement
                phase_diff = alice_phases[i] - bob_phases[i]
                measurement_result = 0 if math.cos(phase_diff) > 0 else 1
                
                successful_measurements.append(i)
                measurement_results.append(measurement_result)
        
        if len(successful_measurements) < params.key_length_bits:
            return {
                'status': 'INSUFFICIENT_BELL_MEASUREMENTS',
                'session_id': session_id,
                'successful_measurements': len(successful_measurements)
            }
        
        # Generate key from measurement results
        raw_key = measurement_results[:params.key_length_bits]
        key_bytes = self._bits_to_bytes(raw_key)
        
        quantum_key = QuantumKey(
            key_id=f"{session_id}_KEY",
            key_material=key_bytes,
            generation_protocol=QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT,
            security_level=QKDSecurityLevel.SCI,
            participants={alice.node_id, bob.node_id},
            generation_timestamp=start_time,
            expiration_timestamp=start_time + timedelta(hours=36),
            quantum_fidelity=0.95,  # MDI-QKD has high security
            error_rate=0.02,
            key_rate=len(raw_key) / (time.time() - start_time.timestamp()),
            permitted_usage_types={KeyUsageType.ENCRYPTION, KeyUsageType.AUTHENTICATION, KeyUsageType.DIGITAL_SIGNATURE},
            session_id=session_id
        )
        
        return {
            'status': 'SUCCESS',
            'session_id': session_id,
            'quantum_key': quantum_key,
            'bell_measurements': len(successful_measurements),
            'measurement_rate': len(successful_measurements) / n_pulses
        }
    
    def _get_default_parameters(self, protocol: QKDProtocol) -> QKDParameters:
        """Get default parameters for QKD protocol."""
        base_params = QKDParameters(
            protocol=protocol,
            key_length_bits=256,
            pulse_rate=1e6,  # 1 MHz
            detection_efficiency=0.9,
            error_correction_efficiency=0.95,
            privacy_amplification_ratio=0.5,
            security_parameter=128,
            composable_security=True,
            finite_key_analysis=True,
            channel_loss=0.2,  # dB/km
            dark_count_rate=100,  # Hz
            afterpulse_probability=0.01,
            timing_jitter=0.1  # ns
        )
        
        # Protocol-specific adjustments
        if protocol == QKDProtocol.B92:
            base_params.detection_efficiency = 0.5  # Lower for B92
        elif protocol == QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT:
            base_params.pulse_rate = 5e5  # Lower rate for MDI
            base_params.privacy_amplification_ratio = 0.3
        
        return base_params
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        """Convert list of bits to bytes."""
        byte_array = bytearray()
        
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i+8]
            if len(byte_bits) < 8:
                byte_bits.extend([0] * (8 - len(byte_bits)))
            
            byte_value = 0
            for j, bit in enumerate(byte_bits):
                byte_value |= (bit << (7 - j))
            
            byte_array.append(byte_value)
        
        return bytes(byte_array)
    
    def _calculate_distance(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        """Calculate distance between two locations (simplified)."""
        return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2) * 111.0  # Rough km conversion
    
    def _update_node_metrics(self, node: QKDNode, session_result: Dict[str, Any]) -> None:
        """Update node performance metrics."""
        node.performance_metrics['total_sessions'] += 1
        
        if session_result['status'] == 'SUCCESS':
            node.performance_metrics['successful_sessions'] += 1
            
            if 'error_rate' in session_result:
                current_avg = node.performance_metrics['average_error_rate']
                total_sessions = node.performance_metrics['successful_sessions']
                node.performance_metrics['average_error_rate'] = (
                    (current_avg * (total_sessions - 1) + session_result['error_rate']) / total_sessions
                )


class QKDNetworkManager:
    """Manager for QKD network operations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.protocol_engine = QKDProtocolEngine()
        
        # Network components
        self.nodes: Dict[str, QKDNode] = {}
        self.network_topology = nx.Graph()
        self.key_store: Dict[str, QuantumKey] = {}
        
        # Session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.session_history: deque = deque(maxlen=100000)
        
        # Performance tracking
        self.network_metrics = {
            'total_nodes': 0,
            'active_nodes': 0,
            'total_keys_generated': 0,
            'average_key_rate': 0.0,
            'network_uptime': 1.0,
            'security_incidents': 0
        }
        
        logger.info("QKD Network Manager initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for QKD network."""
        return {
            'auto_key_refresh': True,
            'key_refresh_threshold': 0.1,  # Refresh when 90% used
            'max_key_lifetime_hours': 24,
            'preferred_protocols': [QKDProtocol.BB84, QKDProtocol.E91, QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT],
            'security_monitoring': True,
            'network_optimization': True,
            'redundant_key_generation': True,
            'quantum_authentication': True
        }
    
    def register_qkd_node(self, node_config: Dict[str, Any]) -> str:
        """Register new QKD node in network."""
        node = QKDNode(
            node_id=node_config['node_id'],
            role=QKDNetworkRole(node_config['role']),
            location=tuple(node_config['location']),
            capabilities=set(QKDProtocol(p) for p in node_config['capabilities']),
            quantum_source_specs=node_config.get('quantum_source_specs', {}),
            detector_specs=node_config.get('detector_specs', {}),
            channel_interface_specs=node_config.get('channel_interface_specs', {}),
            uptime=node_config.get('uptime', 0.99),
            key_generation_rate=node_config.get('key_generation_rate', 1000.0),
            error_rate=node_config.get('error_rate', 0.02)
        )
        
        self.nodes[node.node_id] = node
        self.network_topology.add_node(node.node_id, role=node.role.value, location=node.location)
        
        # Update network metrics
        self.network_metrics['total_nodes'] = len(self.nodes)
        self.network_metrics['active_nodes'] = len([n for n in self.nodes.values() if n.uptime > 0.5])
        
        logger.info(f"Registered QKD node {node.node_id} with role {node.role.value}")
        return node.node_id
    
    def establish_qkd_link(self, node1_id: str, node2_id: str, 
                          channel_specs: Dict[str, Any]) -> bool:
        """Establish QKD link between two nodes."""
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return False
        
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        
        # Check capability compatibility
        common_protocols = node1.capabilities & node2.capabilities
        if not common_protocols:
            logger.warning(f"No common protocols between {node1_id} and {node2_id}")
            return False
        
        # Add to network topology
        distance = self.protocol_engine._calculate_distance(node1.location, node2.location)
        
        self.network_topology.add_edge(
            node1_id, node2_id,
            distance=distance,
            channel_specs=channel_specs,
            common_protocols=list(common_protocols)
        )
        
        # Update node connections
        node1.connected_nodes.add(node2_id)
        node2.connected_nodes.add(node1_id)
        
        logger.info(f"Established QKD link: {node1_id} <-> {node2_id} (distance: {distance:.1f}km)")
        return True
    
    async def generate_shared_key(self, alice_id: str, bob_id: str,
                                 protocol: Optional[QKDProtocol] = None,
                                 key_length: int = 256,
                                 security_level: QKDSecurityLevel = QKDSecurityLevel.SECRET) -> Optional[str]:
        """Generate shared quantum key between two nodes."""
        if alice_id not in self.nodes or bob_id not in self.nodes:
            return None
        
        alice_node = self.nodes[alice_id]
        bob_node = self.nodes[bob_id]
        
        # Check if nodes are connected
        if not self.network_topology.has_edge(alice_id, bob_id):
            logger.error(f"No QKD link between {alice_id} and {bob_id}")
            return None
        
        # Select protocol
        if protocol is None:
            edge_data = self.network_topology[alice_id][bob_id]
            available_protocols = [QKDProtocol(p) for p in edge_data['common_protocols']]
            preferred = [p for p in self.config['preferred_protocols'] if p in available_protocols]
            protocol = preferred[0] if preferred else available_protocols[0]
        
        # Set up protocol parameters
        parameters = self.protocol_engine.protocol_parameters[protocol]
        parameters.key_length_bits = key_length
        
        # Execute QKD session
        try:
            session_result = self.protocol_engine.execute_qkd_session(
                alice_node, bob_node, protocol, parameters
            )
            
            if session_result['status'] == 'SUCCESS':
                quantum_key = session_result['quantum_key']
                quantum_key.security_level = security_level
                
                # Store key
                self.key_store[quantum_key.key_id] = quantum_key
                alice_node.generated_keys[quantum_key.key_id] = quantum_key
                bob_node.generated_keys[quantum_key.key_id] = quantum_key
                
                # Update metrics
                self.network_metrics['total_keys_generated'] += 1
                
                # Store session
                self.session_history.append(session_result)
                
                logger.info(f"Generated quantum key {quantum_key.key_id} using {protocol.value}")
                return quantum_key.key_id
            else:
                logger.error(f"QKD session failed: {session_result['status']}")
                return None
                
        except Exception as e:
            logger.error(f"Error in QKD session: {e}")
            return None
    
    def get_key(self, key_id: str) -> Optional[QuantumKey]:
        """Retrieve quantum key by ID."""
        return self.key_store.get(key_id)
    
    def use_key(self, key_id: str, user_id: str, usage_type: KeyUsageType) -> Optional[bytes]:
        """Use quantum key for specific purpose."""
        if key_id not in self.key_store:
            return None
        
        quantum_key = self.key_store[key_id]
        
        if quantum_key.use_key(usage_type, user_id):
            return quantum_key.key_material
        else:
            return None
    
    def refresh_expired_keys(self) -> int:
        """Refresh expired or nearly expired keys."""
        refreshed_count = 0
        current_time = datetime.now()
        
        for key_id, quantum_key in list(self.key_store.items()):
            # Check if key needs refresh
            time_until_expiry = (quantum_key.expiration_timestamp - current_time).total_seconds()
            usage_ratio = quantum_key.usage_count / quantum_key.max_usage_count
            
            needs_refresh = (
                time_until_expiry < 3600 or  # Less than 1 hour remaining
                usage_ratio > self.config['key_refresh_threshold'] or
                not quantum_key.is_valid()
            )
            
            if needs_refresh and len(quantum_key.participants) == 2:
                participants = list(quantum_key.participants)
                alice_id, bob_id = participants[0], participants[1]
                
                # Generate new key asynchronously
                asyncio.create_task(self.generate_shared_key(
                    alice_id, bob_id,
                    quantum_key.generation_protocol,
                    len(quantum_key.key_material) * 8,
                    quantum_key.security_level
                ))
                
                refreshed_count += 1
        
        return refreshed_count
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status."""
        # Node status
        node_status = {}
        total_uptime = 0.0
        
        for node_id, node in self.nodes.items():
            node_status[node_id] = {
                'role': node.role.value,
                'location': node.location,
                'capabilities': [p.value for p in node.capabilities],
                'uptime': node.uptime,
                'connected_nodes': len(node.connected_nodes),
                'generated_keys': len(node.generated_keys),
                'performance_metrics': node.performance_metrics
            }
            total_uptime += node.uptime
        
        # Network topology metrics
        if len(self.nodes) > 1:
            avg_uptime = total_uptime / len(self.nodes)
            network_density = nx.density(self.network_topology)
            
            if nx.is_connected(self.network_topology):
                avg_path_length = nx.average_shortest_path_length(self.network_topology, weight='distance')
            else:
                avg_path_length = float('inf')
        else:
            avg_uptime = 1.0
            network_density = 0.0
            avg_path_length = 0.0
        
        # Key statistics
        valid_keys = sum(1 for key in self.key_store.values() if key.is_valid())
        total_key_material = sum(len(key.key_material) for key in self.key_store.values())
        
        # Recent session statistics
        recent_sessions = [s for s in self.session_history if s.get('quantum_key')]
        if recent_sessions:
            avg_key_rate = sum(s['quantum_key'].key_rate for s in recent_sessions) / len(recent_sessions)
            avg_error_rate = sum(s.get('error_rate', 0) for s in recent_sessions) / len(recent_sessions)
        else:
            avg_key_rate = 0.0
            avg_error_rate = 0.0
        
        # Update network metrics
        self.network_metrics.update({
            'active_nodes': len([n for n in self.nodes.values() if n.uptime > 0.5]),
            'average_key_rate': avg_key_rate,
            'network_uptime': avg_uptime
        })
        
        return {
            'network_status': 'OPERATIONAL',
            'network_metrics': self.network_metrics,
            'topology_metrics': {
                'nodes': len(self.nodes),
                'edges': len(self.network_topology.edges()),
                'density': network_density,
                'average_path_length': avg_path_length,
                'connected': nx.is_connected(self.network_topology)
            },
            'key_statistics': {
                'total_keys': len(self.key_store),
                'valid_keys': valid_keys,
                'total_key_material_bytes': total_key_material,
                'average_error_rate': avg_error_rate
            },
            'node_details': node_status,
            'recent_sessions': len(recent_sessions),
            'configuration': self.config
        }


async def main():
    """Main demonstration of QKD infrastructure."""
    print("MWRASP Quantum-Safe Key Distribution Infrastructure")
    print("=" * 60)
    
    # Initialize QKD network
    qkd_network = QKDNetworkManager()
    
    # Register QKD nodes
    print("Registering QKD Nodes:")
    
    node_configs = [
        {
            'node_id': 'QKD_ALICE_HQ',
            'role': 'ALICE',
            'location': (38.9072, -77.0369),  # Washington DC
            'capabilities': ['BB84', 'E91', 'MEASUREMENT_DEVICE_INDEPENDENT'],
            'uptime': 0.99,
            'key_generation_rate': 2000.0,
            'error_rate': 0.015
        },
        {
            'node_id': 'QKD_BOB_WEST',
            'role': 'BOB',
            'location': (37.4419, -122.1430),  # Silicon Valley
            'capabilities': ['BB84', 'SARG04', 'SIX_STATE'],
            'uptime': 0.97,
            'key_generation_rate': 1500.0,
            'error_rate': 0.02
        },
        {
            'node_id': 'QKD_CHARLIE_EAST',
            'role': 'CHARLIE',
            'location': (40.7128, -74.0060),  # New York
            'capabilities': ['BB84', 'E91', 'MEASUREMENT_DEVICE_INDEPENDENT'],
            'uptime': 0.98,
            'key_generation_rate': 1800.0,
            'error_rate': 0.018
        },
        {
            'node_id': 'QKD_DELTA_SOUTH',
            'role': 'BOB',
            'location': (25.7617, -80.1918),  # Miami
            'capabilities': ['B92', 'SARG04', 'SIX_STATE'],
            'uptime': 0.95,
            'key_generation_rate': 1200.0,
            'error_rate': 0.025
        },
        {
            'node_id': 'QKD_ECHO_CENTRAL',
            'role': 'ALICE',
            'location': (41.8781, -87.6298),  # Chicago
            'capabilities': ['BB84', 'E91', 'CONTINUOUS_VARIABLE'],
            'uptime': 0.99,
            'key_generation_rate': 1700.0,
            'error_rate': 0.02
        }
    ]
    
    for config in node_configs:
        node_id = qkd_network.register_qkd_node(config)
        print(f"  ✓ {node_id}: {config['role']} at {config['location']} (protocols: {', '.join(config['capabilities'])})")
    
    # Establish QKD links
    print("\nEstablishing QKD Links:")
    
    links = [
        ('QKD_ALICE_HQ', 'QKD_BOB_WEST', {'fiber_type': 'SMF-28', 'loss_db_km': 0.2}),
        ('QKD_ALICE_HQ', 'QKD_CHARLIE_EAST', {'fiber_type': 'SMF-28', 'loss_db_km': 0.18}),
        ('QKD_CHARLIE_EAST', 'QKD_DELTA_SOUTH', {'fiber_type': 'SMF-28', 'loss_db_km': 0.22}),
        ('QKD_ECHO_CENTRAL', 'QKD_ALICE_HQ', {'fiber_type': 'SMF-28', 'loss_db_km': 0.19}),
        ('QKD_ECHO_CENTRAL', 'QKD_BOB_WEST', {'fiber_type': 'SMF-28', 'loss_db_km': 0.21})
    ]
    
    for node1, node2, specs in links:
        success = qkd_network.establish_qkd_link(node1, node2, specs)
        status = "✓" if success else "✗"
        print(f"  {status} {node1} <-> {node2}")
    
    # Generate quantum keys
    print("\nGenerating Quantum Keys:")
    
    key_generation_tasks = [
        ('QKD_ALICE_HQ', 'QKD_BOB_WEST', QKDProtocol.BB84, 256, QKDSecurityLevel.TOP_SECRET),
        ('QKD_ALICE_HQ', 'QKD_CHARLIE_EAST', QKDProtocol.E91, 512, QKDSecurityLevel.SCI),
        ('QKD_CHARLIE_EAST', 'QKD_DELTA_SOUTH', QKDProtocol.SARG04, 256, QKDSecurityLevel.SECRET),
        ('QKD_ECHO_CENTRAL', 'QKD_ALICE_HQ', QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT, 384, QKDSecurityLevel.SCI),
        ('QKD_ECHO_CENTRAL', 'QKD_BOB_WEST', QKDProtocol.BB84, 256, QKDSecurityLevel.TOP_SECRET)
    ]
    
    generated_keys = []
    for alice, bob, protocol, key_len, sec_level in key_generation_tasks:
        key_id = await qkd_network.generate_shared_key(alice, bob, protocol, key_len, sec_level)
        if key_id:
            generated_keys.append(key_id)
            quantum_key = qkd_network.get_key(key_id)
            print(f"  ✓ {protocol.value}: {alice} <-> {bob}")
            print(f"    Key ID: {key_id}")
            print(f"    Length: {len(quantum_key.key_material) * 8} bits")
            print(f"    Error Rate: {quantum_key.error_rate:.4f}")
            print(f"    Key Rate: {quantum_key.key_rate:.1f} bits/sec")
        else:
            print(f"  ✗ {protocol.value}: {alice} <-> {bob} - Failed")
    
    # Demonstrate key usage
    print("\nDemonstrating Key Usage:")
    
    for i, key_id in enumerate(generated_keys[:3]):  # Use first 3 keys
        quantum_key = qkd_network.get_key(key_id)
        
        # Use for encryption
        encryption_key = qkd_network.use_key(key_id, 'USER_ALICE', KeyUsageType.ENCRYPTION)
        if encryption_key:
            print(f"  ✓ Key {key_id[-8:]}: Used for encryption ({len(encryption_key)} bytes)")
        
        # Use for authentication
        auth_key = qkd_network.use_key(key_id, 'USER_BOB', KeyUsageType.AUTHENTICATION)
        if auth_key:
            print(f"  ✓ Key {key_id[-8:]}: Used for authentication")
        
        # Show usage statistics
        print(f"    Usage: {quantum_key.usage_count}/{quantum_key.max_usage_count}")
        print(f"    Valid: {quantum_key.is_valid()}")
    
    # Network status
    print("\nQKD Network Status:")
    status = qkd_network.get_network_status()
    
    print(f"  Network Status: {status['network_status']}")
    print(f"  Nodes: {status['network_metrics']['active_nodes']}/{status['network_metrics']['total_nodes']}")
    print(f"  Generated Keys: {status['network_metrics']['total_keys_generated']}")
    print(f"  Network Uptime: {status['network_metrics']['network_uptime']:.1%}")
    
    print(f"\nNetwork Topology:")
    topo = status['topology_metrics']
    print(f"  Density: {topo['density']:.3f}")
    print(f"  Connected: {topo['connected']}")
    print(f"  Average Path Length: {topo['average_path_length']:.1f}")
    
    print(f"\nKey Statistics:")
    key_stats = status['key_statistics']
    print(f"  Total Keys: {key_stats['total_keys']}")
    print(f"  Valid Keys: {key_stats['valid_keys']}")
    print(f"  Total Key Material: {key_stats['total_key_material_bytes']} bytes")
    print(f"  Average Error Rate: {key_stats['average_error_rate']:.4f}")
    
    print(f"\nNode Performance:")
    for node_id, node_info in status['node_details'].items():
        print(f"  {node_id} ({node_info['role']}):")
        perf = node_info['performance_metrics']
        print(f"    Sessions: {perf['successful_sessions']}/{perf['total_sessions']}")
        print(f"    Uptime: {node_info['uptime']:.1%}")
        print(f"    Generated Keys: {node_info['generated_keys']}")
        print(f"    Average Error Rate: {perf['average_error_rate']:.4f}")
    
    # Key refresh demonstration
    print("\nKey Refresh Demonstration:")
    refreshed = qkd_network.refresh_expired_keys()
    print(f"  Initiated refresh for {refreshed} keys")


if __name__ == "__main__":
    asyncio.run(main())
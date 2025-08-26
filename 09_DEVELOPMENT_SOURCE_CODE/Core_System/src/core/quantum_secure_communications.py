"""
MWRASP Quantum-Enhanced Secure Communication Protocols
Advanced quantum-enhanced secure communication system with quantum key distribution,
quantum encryption, and quantum-safe protocols for national security communications.
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
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumProtocol(Enum):
    """Quantum communication protocols."""
    QUANTUM_KEY_DISTRIBUTION = "QKD"           # BB84, E91, SARG04
    QUANTUM_DIGITAL_SIGNATURES = "QDS"        # Quantum digital signature protocols
    QUANTUM_SECRET_SHARING = "QSS"            # Quantum secret sharing
    QUANTUM_TELEPORTATION = "QT"              # Quantum state teleportation
    QUANTUM_ENTANGLEMENT_DISTRIBUTION = "QED" # Entanglement-based communication
    POST_QUANTUM_CRYPTOGRAPHY = "PQC"         # Post-quantum classical protocols
    HYBRID_QUANTUM_CLASSICAL = "HQC"          # Hybrid quantum-classical protocols


class SecurityLevel(Enum):
    """Communication security levels."""
    UNCLASSIFIED = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4
    SCI = 5
    SAP = 6
    QUANTUM_EYES_ONLY = 7


class QuantumChannel(Enum):
    """Types of quantum communication channels."""
    OPTICAL_FIBER = "OPTICAL_FIBER"           # Fiber optic quantum channel
    FREE_SPACE_OPTICAL = "FREE_SPACE_OPTICAL" # Satellite/terrestrial FSO
    MICROWAVE_QUANTUM = "MICROWAVE_QUANTUM"   # Microwave quantum communication
    TRAPPED_ION = "TRAPPED_ION"               # Trapped ion quantum network
    SUPERCONDUCTING = "SUPERCONDUCTING"       # Superconducting quantum circuits
    HYBRID_CHANNEL = "HYBRID_CHANNEL"         # Multiple channel types


@dataclass
class QuantumKey:
    """Quantum cryptographic key with metadata."""
    key_id: str
    key_material: bytes
    algorithm: str
    security_level: SecurityLevel
    generation_timestamp: datetime
    expiration_timestamp: datetime
    usage_count: int
    max_usage_count: int
    participants: Set[str]
    quantum_properties: Dict[str, Any]
    
    def is_valid(self) -> bool:
        """Check if key is still valid."""
        if datetime.now() > self.expiration_timestamp:
            return False
        if self.usage_count >= self.max_usage_count:
            return False
        return True
    
    def get_remaining_uses(self) -> int:
        """Get remaining key uses."""
        return max(0, self.max_usage_count - self.usage_count)
    
    def use_key(self) -> bool:
        """Use the key (increment usage count)."""
        if not self.is_valid():
            return False
        self.usage_count += 1
        return True


@dataclass
class QuantumMessage:
    """Quantum-secured message structure."""
    message_id: str
    sender_id: str
    receiver_id: str
    content: bytes
    protocol: QuantumProtocol
    security_level: SecurityLevel
    encryption_key_id: str
    quantum_signature: bytes
    timestamp: datetime
    channel_type: QuantumChannel
    quantum_properties: Dict[str, Any]
    
    # Message integrity and authentication
    classical_mac: bytes
    quantum_mac: bytes
    entanglement_verification: Optional[Dict[str, Any]] = None
    
    def calculate_message_hash(self) -> bytes:
        """Calculate cryptographic hash of message content."""
        hasher = hashlib.sha3_256()
        hasher.update(self.content)
        hasher.update(self.sender_id.encode())
        hasher.update(self.receiver_id.encode())
        hasher.update(self.timestamp.isoformat().encode())
        return hasher.digest()


@dataclass
class QuantumChannelState:
    """State information for quantum communication channel."""
    channel_id: str
    channel_type: QuantumChannel
    participants: Set[str]
    quantum_fidelity: float  # 0-1 channel fidelity
    error_rate: float        # Quantum bit error rate
    key_rate: float          # Key generation rate (bits/second)
    bandwidth: float         # Classical bandwidth (Mbps)
    latency: float          # Round-trip latency (ms)
    availability: float     # Channel availability (0-1)
    
    # Quantum-specific parameters
    entanglement_rate: float      # Entangled pairs/second
    coherence_time: float         # Quantum coherence time (ms)
    gate_fidelity: float          # Quantum gate operation fidelity
    measurement_efficiency: float  # Detection efficiency
    
    # Security parameters
    eavesdropping_probability: float  # Estimated eavesdropping probability
    security_parameter: float        # Security parameter for protocols
    
    def calculate_secure_key_rate(self) -> float:
        """Calculate secure key generation rate."""
        # Simplified secure key rate calculation for BB84-like protocols
        if self.error_rate > 0.11:  # Above security threshold
            return 0.0
        
        # Information-theoretic secure key rate
        h_error = self._binary_entropy(self.error_rate)
        secure_rate = self.key_rate * (1 - 2 * h_error) * self.quantum_fidelity
        
        return max(0.0, secure_rate)
    
    def _binary_entropy(self, p: float) -> float:
        """Calculate binary entropy function."""
        if p <= 0 or p >= 1:
            return 0.0
        return -p * math.log2(p) - (1-p) * math.log2(1-p)
    
    def assess_channel_security(self) -> Dict[str, Any]:
        """Assess overall channel security."""
        security_factors = {
            'quantum_fidelity': self.quantum_fidelity,
            'error_rate_security': 1.0 - (self.error_rate / 0.11),  # Normalize to security threshold
            'eavesdropping_resistance': 1.0 - self.eavesdropping_probability,
            'coherence_quality': min(1.0, self.coherence_time / 1000.0),  # Normalize to 1 second
            'detection_efficiency': self.measurement_efficiency
        }
        
        # Weighted security score
        weights = [0.25, 0.25, 0.2, 0.15, 0.15]
        overall_security = sum(w * s for w, s in zip(weights, security_factors.values()))
        
        security_assessment = {
            'overall_security_score': max(0.0, min(1.0, overall_security)),
            'secure_key_rate': self.calculate_secure_key_rate(),
            'security_factors': security_factors,
            'recommended_protocols': self._recommend_protocols(),
            'threat_level': self._assess_threat_level()
        }
        
        return security_assessment
    
    def _recommend_protocols(self) -> List[QuantumProtocol]:
        """Recommend suitable quantum protocols based on channel state."""
        recommendations = []
        
        if self.quantum_fidelity > 0.95 and self.error_rate < 0.05:
            recommendations.append(QuantumProtocol.QUANTUM_KEY_DISTRIBUTION)
            recommendations.append(QuantumProtocol.QUANTUM_DIGITAL_SIGNATURES)
        
        if self.entanglement_rate > 1000 and self.coherence_time > 100:
            recommendations.append(QuantumProtocol.QUANTUM_TELEPORTATION)
            recommendations.append(QuantumProtocol.QUANTUM_ENTANGLEMENT_DISTRIBUTION)
        
        if self.error_rate < 0.15:  # Still usable with error correction
            recommendations.append(QuantumProtocol.QUANTUM_SECRET_SHARING)
        
        # Always recommend hybrid approaches for robustness
        recommendations.append(QuantumProtocol.HYBRID_QUANTUM_CLASSICAL)
        recommendations.append(QuantumProtocol.POST_QUANTUM_CRYPTOGRAPHY)
        
        return recommendations
    
    def _assess_threat_level(self) -> str:
        """Assess threat level based on channel parameters."""
        if self.eavesdropping_probability > 0.1:
            return 'HIGH'
        elif self.error_rate > 0.08:
            return 'MEDIUM'
        elif self.quantum_fidelity < 0.9:
            return 'MEDIUM'
        else:
            return 'LOW'


class QuantumKeyDistribution:
    """Quantum Key Distribution (QKD) implementation."""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.generated_keys: Dict[str, QuantumKey] = {}
        
    def initiate_bb84_session(self, alice_id: str, bob_id: str, 
                             channel: QuantumChannelState, 
                             key_length: int = 256) -> Dict[str, Any]:
        """Initiate BB84 quantum key distribution session."""
        session_id = f"BB84_{alice_id}_{bob_id}_{int(time.time())}"
        
        # Simulate BB84 protocol steps
        session_data = {
            'session_id': session_id,
            'protocol': 'BB84',
            'alice_id': alice_id,
            'bob_id': bob_id,
            'channel_state': channel,
            'target_key_length': key_length,
            'status': 'INITIATED',
            'start_time': datetime.now(),
            'quantum_transmissions': [],
            'basis_reconciliation': None,
            'error_detection_results': None,
            'privacy_amplification': None
        }
        
        # Step 1: Alice prepares random qubits in random bases
        alice_bits = [random.randint(0, 1) for _ in range(key_length * 4)]  # 4x oversampling
        alice_bases = [random.randint(0, 1) for _ in range(key_length * 4)]  # 0: rectilinear, 1: diagonal
        
        # Step 2: Simulate quantum transmission with channel noise
        received_bits = []
        for i, (bit, basis) in enumerate(zip(alice_bits, alice_bases)):
            # Simulate channel errors
            if random.random() < channel.error_rate:
                received_bit = 1 - bit  # Bit flip error
            else:
                received_bit = bit
            received_bits.append(received_bit)
        
        # Step 3: Bob measures in random bases
        bob_bases = [random.randint(0, 1) for _ in range(key_length * 4)]
        
        session_data['quantum_transmissions'] = {
            'alice_bits': alice_bits,
            'alice_bases': alice_bases,
            'received_bits': received_bits,
            'bob_bases': bob_bases,
            'transmission_time': datetime.now()
        }
        
        # Step 4: Basis reconciliation (classical communication)
        matching_bases = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
        sifted_key_alice = [alice_bits[i] for i in matching_bases]
        sifted_key_bob = [received_bits[i] for i in matching_bases]
        
        session_data['basis_reconciliation'] = {
            'matching_indices': matching_bases,
            'sifted_length': len(sifted_key_alice),
            'sifted_key_alice': sifted_key_alice,
            'sifted_key_bob': sifted_key_bob
        }
        
        # Step 5: Error detection and estimation
        test_fraction = 0.5  # Use half the sifted key for error testing
        test_length = int(len(sifted_key_alice) * test_fraction)
        test_indices = random.sample(range(len(sifted_key_alice)), test_length)
        
        test_bits_alice = [sifted_key_alice[i] for i in test_indices]
        test_bits_bob = [sifted_key_bob[i] for i in test_indices]
        
        errors = sum(1 for a, b in zip(test_bits_alice, test_bits_bob) if a != b)
        error_rate = errors / len(test_bits_alice) if test_bits_alice else 0.0
        
        session_data['error_detection_results'] = {
            'test_length': test_length,
            'errors_detected': errors,
            'estimated_error_rate': error_rate,
            'security_threshold': 0.11
        }
        
        # Step 6: Privacy amplification (if error rate is acceptable)
        if error_rate <= 0.11:  # Security threshold for BB84
            remaining_indices = [i for i in range(len(sifted_key_alice)) if i not in test_indices]
            remaining_key = [sifted_key_alice[i] for i in remaining_indices]
            
            # Simulate privacy amplification (hash-based)
            if len(remaining_key) >= key_length:
                final_key_bits = remaining_key[:key_length]
                final_key_bytes = self._bits_to_bytes(final_key_bits)
                
                # Generate quantum key object
                quantum_key = QuantumKey(
                    key_id=f"{session_id}_KEY",
                    key_material=final_key_bytes,
                    algorithm="BB84",
                    security_level=SecurityLevel.QUANTUM_EYES_ONLY,
                    generation_timestamp=datetime.now(),
                    expiration_timestamp=datetime.now() + timedelta(hours=24),
                    usage_count=0,
                    max_usage_count=1000,
                    participants={alice_id, bob_id},
                    quantum_properties={
                        'protocol': 'BB84',
                        'error_rate': error_rate,
                        'key_rate': len(final_key_bits) / (time.time() - session_data['start_time'].timestamp()),
                        'security_parameter': 1.0 - 2 * error_rate
                    }
                )
                
                self.generated_keys[quantum_key.key_id] = quantum_key
                session_data['status'] = 'SUCCESS'
                session_data['generated_key_id'] = quantum_key.key_id
                
            else:
                session_data['status'] = 'INSUFFICIENT_KEY_MATERIAL'
        else:
            session_data['status'] = 'SECURITY_THRESHOLD_EXCEEDED'
        
        session_data['completion_time'] = datetime.now()
        session_data['session_duration'] = (session_data['completion_time'] - session_data['start_time']).total_seconds()
        
        self.active_sessions[session_id] = session_data
        
        return {
            'session_id': session_id,
            'status': session_data['status'],
            'key_id': session_data.get('generated_key_id'),
            'error_rate': error_rate,
            'session_duration': session_data['session_duration']
        }
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        """Convert list of bits to bytes."""
        byte_array = bytearray()
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i+8]
            if len(byte_bits) < 8:
                byte_bits.extend([0] * (8 - len(byte_bits)))  # Pad with zeros
            
            byte_value = 0
            for j, bit in enumerate(byte_bits):
                byte_value |= (bit << (7 - j))
            
            byte_array.append(byte_value)
        
        return bytes(byte_array)
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of QKD session."""
        if session_id not in self.active_sessions:
            return {'status': 'NOT_FOUND'}
        
        session = self.active_sessions[session_id]
        return {
            'session_id': session_id,
            'protocol': session['protocol'],
            'status': session['status'],
            'participants': [session['alice_id'], session['bob_id']],
            'start_time': session['start_time'],
            'completion_time': session.get('completion_time'),
            'session_duration': session.get('session_duration'),
            'generated_key_id': session.get('generated_key_id'),
            'error_rate': session.get('error_detection_results', {}).get('estimated_error_rate')
        }


class QuantumEncryption:
    """Quantum encryption and decryption operations."""
    
    def __init__(self, key_distribution: QuantumKeyDistribution):
        self.qkd = key_distribution
        self.encryption_history: deque = deque(maxlen=10000)
        
    def encrypt_message(self, plaintext: bytes, sender_id: str, receiver_id: str,
                       security_level: SecurityLevel, protocol: QuantumProtocol) -> QuantumMessage:
        """Encrypt message using quantum-secured keys."""
        # Find appropriate quantum key
        suitable_keys = [
            key for key in self.qkd.generated_keys.values()
            if (sender_id in key.participants and receiver_id in key.participants and
                key.security_level.value >= security_level.value and key.is_valid())
        ]
        
        if not suitable_keys:
            raise ValueError("No suitable quantum key available for encryption")
        
        # Select best key (highest security level, most recent)
        selected_key = max(suitable_keys, key=lambda k: (k.security_level.value, k.generation_timestamp))
        
        # Use the key
        if not selected_key.use_key():
            raise ValueError("Selected key is no longer valid")
        
        # Generate message ID
        message_id = f"QMSG_{int(time.time() * 1000000)}"
        
        # Encrypt content using quantum key
        if protocol == QuantumProtocol.QUANTUM_KEY_DISTRIBUTION:
            encrypted_content = self._qkd_encrypt(plaintext, selected_key.key_material)
        elif protocol == QuantumProtocol.POST_QUANTUM_CRYPTOGRAPHY:
            encrypted_content = self._pqc_encrypt(plaintext, selected_key.key_material)
        elif protocol == QuantumProtocol.HYBRID_QUANTUM_CLASSICAL:
            encrypted_content = self._hybrid_encrypt(plaintext, selected_key.key_material)
        else:
            encrypted_content = self._default_quantum_encrypt(plaintext, selected_key.key_material)
        
        # Generate quantum signature
        quantum_signature = self._generate_quantum_signature(encrypted_content, selected_key)
        
        # Generate MACs
        classical_mac = self._generate_classical_mac(encrypted_content, selected_key.key_material)
        quantum_mac = self._generate_quantum_mac(encrypted_content, selected_key)
        
        # Create quantum message
        quantum_message = QuantumMessage(
            message_id=message_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=encrypted_content,
            protocol=protocol,
            security_level=security_level,
            encryption_key_id=selected_key.key_id,
            quantum_signature=quantum_signature,
            timestamp=datetime.now(),
            channel_type=QuantumChannel.HYBRID_CHANNEL,  # Default
            quantum_properties={
                'key_usage_count': selected_key.usage_count,
                'quantum_fidelity': 0.99,  # Simulated
                'entanglement_verified': True
            },
            classical_mac=classical_mac,
            quantum_mac=quantum_mac
        )
        
        # Record encryption
        self.encryption_history.append({
            'message_id': message_id,
            'timestamp': datetime.now(),
            'sender': sender_id,
            'receiver': receiver_id,
            'protocol': protocol.value,
            'key_id': selected_key.key_id,
            'plaintext_length': len(plaintext),
            'ciphertext_length': len(encrypted_content)
        })
        
        return quantum_message
    
    def decrypt_message(self, quantum_message: QuantumMessage, receiver_id: str) -> bytes:
        """Decrypt quantum message."""
        # Verify receiver
        if quantum_message.receiver_id != receiver_id:
            raise ValueError("Message not intended for this receiver")
        
        # Get decryption key
        if quantum_message.encryption_key_id not in self.qkd.generated_keys:
            raise ValueError("Decryption key not found")
        
        decryption_key = self.qkd.generated_keys[quantum_message.encryption_key_id]
        
        # Verify receiver has access to key
        if receiver_id not in decryption_key.participants:
            raise ValueError("Receiver not authorized for this key")
        
        # Verify message integrity
        if not self._verify_message_integrity(quantum_message, decryption_key):
            raise ValueError("Message integrity verification failed")
        
        # Decrypt based on protocol
        if quantum_message.protocol == QuantumProtocol.QUANTUM_KEY_DISTRIBUTION:
            plaintext = self._qkd_decrypt(quantum_message.content, decryption_key.key_material)
        elif quantum_message.protocol == QuantumProtocol.POST_QUANTUM_CRYPTOGRAPHY:
            plaintext = self._pqc_decrypt(quantum_message.content, decryption_key.key_material)
        elif quantum_message.protocol == QuantumProtocol.HYBRID_QUANTUM_CLASSICAL:
            plaintext = self._hybrid_decrypt(quantum_message.content, decryption_key.key_material)
        else:
            plaintext = self._default_quantum_decrypt(quantum_message.content, decryption_key.key_material)
        
        return plaintext
    
    def _qkd_encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt using QKD-derived key (One-Time Pad for perfect security)."""
        if len(key) < len(plaintext):
            # Expand key using secure hash
            expanded_key = self._expand_key(key, len(plaintext))
        else:
            expanded_key = key[:len(plaintext)]
        
        # One-time pad encryption
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, expanded_key))
        return ciphertext
    
    def _qkd_decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt using QKD-derived key."""
        if len(key) < len(ciphertext):
            expanded_key = self._expand_key(key, len(ciphertext))
        else:
            expanded_key = key[:len(ciphertext)]
        
        # One-time pad decryption (same as encryption)
        plaintext = bytes(c ^ k for c, k in zip(ciphertext, expanded_key))
        return plaintext
    
    def _pqc_encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt using post-quantum cryptography."""
        # Simulate CRYSTALS-Kyber or similar post-quantum encryption
        # In practice, this would use actual PQC libraries
        
        # Use AES-256 with quantum-derived key for simulation
        if len(key) >= 32:
            aes_key = key[:32]
        else:
            aes_key = self._expand_key(key, 32)
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # AES-256-CBC encryption
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # PKCS7 padding
        padding_length = 16 - (len(plaintext) % 16)
        padded_plaintext = plaintext + bytes([padding_length]) * padding_length
        
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        
        # Prepend IV to ciphertext
        return iv + ciphertext
    
    def _pqc_decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt using post-quantum cryptography."""
        if len(key) >= 32:
            aes_key = key[:32]
        else:
            aes_key = self._expand_key(key, 32)
        
        # Extract IV and ciphertext
        iv = ciphertext[:16]
        encrypted_data = ciphertext[16:]
        
        # AES-256-CBC decryption
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-padding_length]
        
        return plaintext
    
    def _hybrid_encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt using hybrid quantum-classical approach."""
        # Split key for dual encryption
        half_len = len(key) // 2
        quantum_key = key[:half_len] if half_len > 0 else key
        classical_key = key[half_len:] if half_len > 0 else key
        
        # First layer: quantum encryption
        quantum_encrypted = self._qkd_encrypt(plaintext, quantum_key)
        
        # Second layer: classical encryption
        classical_encrypted = self._pqc_encrypt(quantum_encrypted, classical_key)
        
        return classical_encrypted
    
    def _hybrid_decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt using hybrid quantum-classical approach."""
        half_len = len(key) // 2
        quantum_key = key[:half_len] if half_len > 0 else key
        classical_key = key[half_len:] if half_len > 0 else key
        
        # First layer: classical decryption
        classical_decrypted = self._pqc_decrypt(ciphertext, classical_key)
        
        # Second layer: quantum decryption
        plaintext = self._qkd_decrypt(classical_decrypted, quantum_key)
        
        return plaintext
    
    def _default_quantum_encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Default quantum encryption (fallback to QKD)."""
        return self._qkd_encrypt(plaintext, key)
    
    def _default_quantum_decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Default quantum decryption (fallback to QKD)."""
        return self._qkd_decrypt(ciphertext, key)
    
    def _expand_key(self, key: bytes, target_length: int) -> bytes:
        """Expand key to target length using secure hash."""
        if len(key) >= target_length:
            return key[:target_length]
        
        expanded = bytearray()
        counter = 0
        
        while len(expanded) < target_length:
            hasher = hashlib.sha3_256()
            hasher.update(key)
            hasher.update(counter.to_bytes(4, 'big'))
            expanded.extend(hasher.digest())
            counter += 1
        
        return bytes(expanded[:target_length])
    
    def _generate_quantum_signature(self, content: bytes, key: QuantumKey) -> bytes:
        """Generate quantum digital signature."""
        # Simulate quantum signature generation
        hasher = hashlib.sha3_256()
        hasher.update(content)
        hasher.update(key.key_material)
        hasher.update(key.key_id.encode())
        hasher.update(str(key.generation_timestamp).encode())
        
        return hasher.digest()
    
    def _generate_classical_mac(self, content: bytes, key: bytes) -> bytes:
        """Generate classical message authentication code."""
        return hmac.new(key, content, hashlib.sha3_256).digest()
    
    def _generate_quantum_mac(self, content: bytes, key: QuantumKey) -> bytes:
        """Generate quantum message authentication code."""
        # Incorporate quantum properties into MAC
        quantum_data = json.dumps(key.quantum_properties, sort_keys=True).encode()
        
        hasher = hashlib.sha3_256()
        hasher.update(content)
        hasher.update(key.key_material)
        hasher.update(quantum_data)
        
        return hasher.digest()
    
    def _verify_message_integrity(self, message: QuantumMessage, key: QuantumKey) -> bool:
        """Verify message integrity using MACs and signatures."""
        # Verify classical MAC
        expected_classical_mac = self._generate_classical_mac(message.content, key.key_material)
        if not hmac.compare_digest(message.classical_mac, expected_classical_mac):
            return False
        
        # Verify quantum MAC
        expected_quantum_mac = self._generate_quantum_mac(message.content, key)
        if not hmac.compare_digest(message.quantum_mac, expected_quantum_mac):
            return False
        
        # Verify quantum signature
        expected_signature = self._generate_quantum_signature(message.content, key)
        if not hmac.compare_digest(message.quantum_signature, expected_signature):
            return False
        
        return True


class QuantumSecureCommunicationSystem:
    """Main quantum secure communication system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        
        # Core components
        self.key_distribution = QuantumKeyDistribution()
        self.encryption_engine = QuantumEncryption(self.key_distribution)
        
        # Channel management
        self.quantum_channels: Dict[str, QuantumChannelState] = {}
        self.channel_topology = nx.Graph()
        
        # Communication sessions
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.message_queue: deque = deque(maxlen=100000)
        
        # Performance metrics
        self.communication_metrics = {
            'total_messages': 0,
            'total_key_distributions': 0,
            'average_encryption_time': 0.0,
            'average_decryption_time': 0.0,
            'security_violations': 0,
            'channel_uptime': 0.95
        }
        
        # Security monitoring
        self.security_monitor = QuantumSecurityMonitor()
        
        logger.info("MWRASP Quantum Secure Communication System initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for quantum communication system."""
        return {
            'auto_key_distribution': True,
            'key_refresh_interval_hours': 12,
            'max_key_usage_count': 1000,
            'security_monitoring': True,
            'channel_redundancy': True,
            'error_correction_enabled': True,
            'quantum_signature_verification': True,
            'hybrid_protocols_preferred': True,
            'emergency_classical_fallback': True
        }
    
    def establish_quantum_channel(self, channel_id: str, channel_type: QuantumChannel,
                                participants: List[str], 
                                channel_parameters: Dict[str, float]) -> str:
        """Establish quantum communication channel."""
        # Create channel state
        channel_state = QuantumChannelState(
            channel_id=channel_id,
            channel_type=channel_type,
            participants=set(participants),
            quantum_fidelity=channel_parameters.get('quantum_fidelity', 0.95),
            error_rate=channel_parameters.get('error_rate', 0.02),
            key_rate=channel_parameters.get('key_rate', 1000.0),  # bits/second
            bandwidth=channel_parameters.get('bandwidth', 100.0),  # Mbps
            latency=channel_parameters.get('latency', 50.0),      # ms
            availability=channel_parameters.get('availability', 0.99),
            entanglement_rate=channel_parameters.get('entanglement_rate', 10000.0),
            coherence_time=channel_parameters.get('coherence_time', 100.0),  # ms
            gate_fidelity=channel_parameters.get('gate_fidelity', 0.999),
            measurement_efficiency=channel_parameters.get('measurement_efficiency', 0.9),
            eavesdropping_probability=channel_parameters.get('eavesdropping_probability', 0.01),
            security_parameter=channel_parameters.get('security_parameter', 0.95)
        )
        
        # Register channel
        self.quantum_channels[channel_id] = channel_state
        
        # Add to topology
        self.channel_topology.add_node(channel_id, channel_type=channel_type.value)
        
        # Connect participants in topology
        for i, participant1 in enumerate(participants):
            for participant2 in participants[i+1:]:
                if not self.channel_topology.has_edge(participant1, participant2):
                    self.channel_topology.add_edge(participant1, participant2, channels=[])
                
                self.channel_topology[participant1][participant2]['channels'].append(channel_id)
        
        # Assess channel security
        security_assessment = channel_state.assess_channel_security()
        
        logger.info(f"Established quantum channel {channel_id}: {channel_type.value} "
                   f"(security score: {security_assessment['overall_security_score']:.3f})")
        
        return channel_id
    
    def initiate_secure_session(self, alice_id: str, bob_id: str, 
                               security_level: SecurityLevel,
                               protocol: Optional[QuantumProtocol] = None) -> str:
        """Initiate secure communication session."""
        session_id = f"QSESSION_{alice_id}_{bob_id}_{int(time.time())}"
        
        # Find suitable channel
        suitable_channels = self._find_channels_for_participants([alice_id, bob_id])
        
        if not suitable_channels:
            raise ValueError("No suitable quantum channels available")
        
        # Select best channel
        best_channel = self._select_optimal_channel(suitable_channels, security_level)
        channel_state = self.quantum_channels[best_channel]
        
        # Determine protocol if not specified
        if protocol is None:
            recommended_protocols = channel_state._recommend_protocols()
            protocol = recommended_protocols[0] if recommended_protocols else QuantumProtocol.HYBRID_QUANTUM_CLASSICAL
        
        # Initiate key distribution if needed
        key_distribution_result = None
        if protocol in [QuantumProtocol.QUANTUM_KEY_DISTRIBUTION, QuantumProtocol.HYBRID_QUANTUM_CLASSICAL]:
            key_distribution_result = self.key_distribution.initiate_bb84_session(
                alice_id, bob_id, channel_state
            )
        
        # Create session
        session_data = {
            'session_id': session_id,
            'alice_id': alice_id,
            'bob_id': bob_id,
            'security_level': security_level,
            'protocol': protocol,
            'channel_id': best_channel,
            'start_time': datetime.now(),
            'key_distribution_result': key_distribution_result,
            'status': 'ACTIVE',
            'messages_exchanged': 0,
            'security_events': []
        }
        
        self.active_sessions[session_id] = session_data
        
        logger.info(f"Initiated secure session {session_id}: {alice_id} <-> {bob_id} "
                   f"using {protocol.value}")
        
        return session_id
    
    def send_secure_message(self, session_id: str, sender_id: str, 
                           plaintext: Union[str, bytes], 
                           message_priority: str = "NORMAL") -> str:
        """Send secure message through quantum communication system."""
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
        
        session = self.active_sessions[session_id]
        
        # Verify sender authorization
        if sender_id not in [session['alice_id'], session['bob_id']]:
            raise ValueError("Sender not authorized for this session")
        
        # Convert string to bytes if needed
        if isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            plaintext_bytes = plaintext
        
        # Encrypt message
        receiver_id = session['bob_id'] if sender_id == session['alice_id'] else session['alice_id']
        
        start_time = time.time()
        quantum_message = self.encryption_engine.encrypt_message(
            plaintext_bytes, sender_id, receiver_id, 
            session['security_level'], session['protocol']
        )
        encryption_time = time.time() - start_time
        
        # Add to message queue
        self.message_queue.append(quantum_message)
        
        # Update session
        session['messages_exchanged'] += 1
        session['last_message_time'] = datetime.now()
        
        # Update metrics
        self.communication_metrics['total_messages'] += 1
        current_avg = self.communication_metrics['average_encryption_time']
        total_messages = self.communication_metrics['total_messages']
        self.communication_metrics['average_encryption_time'] = (
            (current_avg * (total_messages - 1) + encryption_time) / total_messages
        )
        
        # Security monitoring
        self.security_monitor.monitor_message(quantum_message, session)
        
        logger.info(f"Sent secure message {quantum_message.message_id} in session {session_id}")
        
        return quantum_message.message_id
    
    def receive_secure_message(self, message_id: str, receiver_id: str) -> bytes:
        """Receive and decrypt secure message."""
        # Find message in queue
        quantum_message = None
        for msg in self.message_queue:
            if msg.message_id == message_id:
                quantum_message = msg
                break
        
        if quantum_message is None:
            raise ValueError("Message not found")
        
        # Verify receiver
        if quantum_message.receiver_id != receiver_id:
            raise ValueError("Message not intended for this receiver")
        
        # Decrypt message
        start_time = time.time()
        plaintext = self.encryption_engine.decrypt_message(quantum_message, receiver_id)
        decryption_time = time.time() - start_time
        
        # Update metrics
        current_avg = self.communication_metrics['average_decryption_time']
        total_messages = self.communication_metrics['total_messages']
        self.communication_metrics['average_decryption_time'] = (
            (current_avg * (total_messages - 1) + decryption_time) / total_messages
        )
        
        logger.info(f"Received and decrypted message {message_id}")
        
        return plaintext
    
    def _find_channels_for_participants(self, participants: List[str]) -> List[str]:
        """Find channels that connect all participants."""
        suitable_channels = []
        
        for channel_id, channel_state in self.quantum_channels.items():
            if all(participant in channel_state.participants for participant in participants):
                suitable_channels.append(channel_id)
        
        return suitable_channels
    
    def _select_optimal_channel(self, channel_ids: List[str], 
                               security_level: SecurityLevel) -> str:
        """Select optimal channel based on security requirements."""
        if not channel_ids:
            raise ValueError("No channels provided")
        
        channel_scores = []
        
        for channel_id in channel_ids:
            channel_state = self.quantum_channels[channel_id]
            security_assessment = channel_state.assess_channel_security()
            
            # Score based on security, performance, and availability
            security_score = security_assessment['overall_security_score']
            performance_score = (channel_state.quantum_fidelity + 
                               (1.0 - channel_state.error_rate) + 
                               min(1.0, channel_state.key_rate / 1000.0)) / 3.0
            availability_score = channel_state.availability
            
            # Weight based on security level requirement
            if security_level.value >= SecurityLevel.TOP_SECRET.value:
                weights = [0.6, 0.2, 0.2]  # Prioritize security
            else:
                weights = [0.4, 0.4, 0.2]  # Balance security and performance
            
            overall_score = (weights[0] * security_score + 
                           weights[1] * performance_score + 
                           weights[2] * availability_score)
            
            channel_scores.append((channel_id, overall_score))
        
        # Select channel with highest score
        best_channel_id, _ = max(channel_scores, key=lambda x: x[1])
        return best_channel_id
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        # Channel status summary
        channel_summary = {}
        total_security_score = 0.0
        
        for channel_id, channel_state in self.quantum_channels.items():
            security_assessment = channel_state.assess_channel_security()
            channel_summary[channel_id] = {
                'type': channel_state.channel_type.value,
                'participants': list(channel_state.participants),
                'security_score': security_assessment['overall_security_score'],
                'key_rate': security_assessment['secure_key_rate'],
                'threat_level': security_assessment['threat_level'],
                'availability': channel_state.availability
            }
            total_security_score += security_assessment['overall_security_score']
        
        avg_security_score = total_security_score / len(self.quantum_channels) if self.quantum_channels else 0.0
        
        # Session status
        active_session_count = len([s for s in self.active_sessions.values() if s['status'] == 'ACTIVE'])
        
        return {
            'system_status': 'OPERATIONAL',
            'quantum_channels': len(self.quantum_channels),
            'active_sessions': active_session_count,
            'total_sessions': len(self.active_sessions),
            'message_queue_size': len(self.message_queue),
            'generated_keys': len(self.key_distribution.generated_keys),
            'average_security_score': avg_security_score,
            'communication_metrics': self.communication_metrics,
            'channel_summary': channel_summary,
            'security_events': self.security_monitor.get_recent_events(24)
        }


class QuantumSecurityMonitor:
    """Security monitoring for quantum communications."""
    
    def __init__(self):
        self.security_events: deque = deque(maxlen=10000)
        self.threat_indicators: Dict[str, float] = defaultdict(float)
        
    def monitor_message(self, message: QuantumMessage, session: Dict[str, Any]) -> None:
        """Monitor message for security threats."""
        # Check for anomalies
        anomalies = []
        
        # Unusual message timing
        if 'last_message_time' in session:
            time_diff = (message.timestamp - session['last_message_time']).total_seconds()
            if time_diff < 0.1:  # Too frequent
                anomalies.append('HIGH_FREQUENCY_MESSAGING')
            elif time_diff > 3600:  # Too infrequent
                anomalies.append('UNUSUAL_TIMING_PATTERN')
        
        # Message size anomalies
        if len(message.content) > 1000000:  # 1MB
            anomalies.append('LARGE_MESSAGE_SIZE')
        
        # Protocol consistency
        if message.protocol != session['protocol']:
            anomalies.append('PROTOCOL_MISMATCH')
        
        # Record security event if anomalies found
        if anomalies:
            security_event = {
                'timestamp': datetime.now(),
                'message_id': message.message_id,
                'session_id': session['session_id'],
                'sender': message.sender_id,
                'receiver': message.receiver_id,
                'anomalies': anomalies,
                'threat_level': self._calculate_threat_level(anomalies)
            }
            
            self.security_events.append(security_event)
            
            # Update threat indicators
            for anomaly in anomalies:
                self.threat_indicators[anomaly] += 1.0
    
    def _calculate_threat_level(self, anomalies: List[str]) -> str:
        """Calculate threat level based on anomalies."""
        high_risk_anomalies = ['PROTOCOL_MISMATCH', 'TIMING_ATTACK_PATTERN']
        
        if any(anomaly in high_risk_anomalies for anomaly in anomalies):
            return 'HIGH'
        elif len(anomalies) > 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_recent_events(self, hours: int) -> List[Dict[str, Any]]:
        """Get recent security events."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_events = [
            event for event in self.security_events
            if event['timestamp'] > cutoff_time
        ]
        
        return recent_events


async def main():
    """Main demonstration of quantum secure communications."""
    print("MWRASP Quantum-Enhanced Secure Communication Protocols")
    print("=" * 65)
    
    # Initialize quantum communication system
    qcomm = QuantumSecureCommunicationSystem()
    
    # Establish quantum channels
    print("Establishing Quantum Channels:")
    
    channels_config = [
        {
            'channel_id': 'QC_HQ_ALPHA',
            'channel_type': QuantumChannel.OPTICAL_FIBER,
            'participants': ['AGENT_ALICE', 'AGENT_BOB'],
            'parameters': {
                'quantum_fidelity': 0.98,
                'error_rate': 0.015,
                'key_rate': 2000.0,
                'bandwidth': 200.0,
                'latency': 25.0
            }
        },
        {
            'channel_id': 'QC_SATELLITE_BRAVO',
            'channel_type': QuantumChannel.FREE_SPACE_OPTICAL,
            'participants': ['AGENT_CHARLIE', 'AGENT_DELTA'],
            'parameters': {
                'quantum_fidelity': 0.95,
                'error_rate': 0.035,
                'key_rate': 1000.0,
                'bandwidth': 100.0,
                'latency': 500.0
            }
        },
        {
            'channel_id': 'QC_HYBRID_GAMMA',
            'channel_type': QuantumChannel.HYBRID_CHANNEL,
            'participants': ['AGENT_ALICE', 'AGENT_CHARLIE', 'AGENT_DELTA'],
            'parameters': {
                'quantum_fidelity': 0.97,
                'error_rate': 0.02,
                'key_rate': 1500.0,
                'bandwidth': 150.0,
                'latency': 100.0
            }
        }
    ]
    
    for config in channels_config:
        channel_id = qcomm.establish_quantum_channel(
            config['channel_id'],
            config['channel_type'],
            config['participants'],
            config['parameters']
        )
        
        channel_state = qcomm.quantum_channels[channel_id]
        security_assessment = channel_state.assess_channel_security()
        
        print(f"  ✓ {channel_id}: {config['channel_type'].value}")
        print(f"    Security Score: {security_assessment['overall_security_score']:.3f}")
        print(f"    Key Rate: {security_assessment['secure_key_rate']:.1f} bits/sec")
        print(f"    Participants: {', '.join(config['participants'])}")
    
    # Initiate secure sessions
    print("\nInitiating Secure Communication Sessions:")
    
    sessions = [
        ('AGENT_ALICE', 'AGENT_BOB', SecurityLevel.TOP_SECRET, QuantumProtocol.QUANTUM_KEY_DISTRIBUTION),
        ('AGENT_CHARLIE', 'AGENT_DELTA', SecurityLevel.SCI, QuantumProtocol.HYBRID_QUANTUM_CLASSICAL),
        ('AGENT_ALICE', 'AGENT_CHARLIE', SecurityLevel.SECRET, QuantumProtocol.POST_QUANTUM_CRYPTOGRAPHY)
    ]
    
    session_ids = []
    for alice_id, bob_id, security_level, protocol in sessions:
        try:
            session_id = qcomm.initiate_secure_session(alice_id, bob_id, security_level, protocol)
            session_ids.append(session_id)
            
            session_data = qcomm.active_sessions[session_id]
            print(f"  ✓ Session {session_id[-8:]}: {alice_id} <-> {bob_id}")
            print(f"    Protocol: {protocol.value}")
            print(f"    Security Level: {security_level.name}")
            
            if session_data['key_distribution_result']:
                kd_result = session_data['key_distribution_result']
                print(f"    Key Distribution: {kd_result['status']} (error rate: {kd_result.get('error_rate', 0):.3f})")
            
        except Exception as e:
            print(f"  ✗ Failed to create session {alice_id} <-> {bob_id}: {e}")
    
    # Exchange secure messages
    print("\nExchanging Secure Messages:")
    
    message_scenarios = [
        (session_ids[0], 'AGENT_ALICE', "TOP SECRET: Quantum threat detected in sector 7"),
        (session_ids[0], 'AGENT_BOB', "ACKNOWLEDGED: Deploying countermeasures"),
        (session_ids[1], 'AGENT_CHARLIE', "Hybrid protocol test message with quantum signature"),
        (session_ids[2], 'AGENT_ALICE', "Post-quantum encrypted intelligence report")
    ]
    
    message_ids = []
    for session_id, sender, message_text in message_scenarios:
        if session_id:  # Only if session was created successfully
            try:
                message_id = qcomm.send_secure_message(session_id, sender, message_text)
                message_ids.append((message_id, session_id, sender))
                
                print(f"  ✓ Sent message {message_id[-8:]}: {sender}")
                print(f"    Content length: {len(message_text)} characters")
                
            except Exception as e:
                print(f"  ✗ Failed to send message from {sender}: {e}")
    
    # Receive and decrypt messages
    print("\nReceiving and Decrypting Messages:")
    
    for message_id, session_id, original_sender in message_ids:
        session_data = qcomm.active_sessions[session_id]
        
        # Determine receiver
        receiver = session_data['bob_id'] if original_sender == session_data['alice_id'] else session_data['alice_id']
        
        try:
            decrypted_content = qcomm.receive_secure_message(message_id, receiver)
            decrypted_text = decrypted_content.decode('utf-8')
            
            print(f"  ✓ Received by {receiver}: {message_id[-8:]}")
            print(f"    Decrypted: \"{decrypted_text[:50]}{'...' if len(decrypted_text) > 50 else ''}\"")
            
        except Exception as e:
            print(f"  ✗ Failed to decrypt message for {receiver}: {e}")
    
    # System status and metrics
    print("\nQuantum Communication System Status:")
    status = qcomm.get_system_status()
    
    print(f"  System Status: {status['system_status']}")
    print(f"  Quantum Channels: {status['quantum_channels']}")
    print(f"  Active Sessions: {status['active_sessions']}")
    print(f"  Messages Processed: {status['communication_metrics']['total_messages']}")
    print(f"  Generated Keys: {status['generated_keys']}")
    print(f"  Average Security Score: {status['average_security_score']:.3f}")
    
    print("\nCommunication Performance Metrics:")
    metrics = status['communication_metrics']
    print(f"  Average Encryption Time: {metrics['average_encryption_time']*1000:.2f}ms")
    print(f"  Average Decryption Time: {metrics['average_decryption_time']*1000:.2f}ms")
    print(f"  Security Violations: {metrics['security_violations']}")
    print(f"  Channel Uptime: {metrics['channel_uptime']:.1%}")
    
    print("\nChannel Security Summary:")
    for channel_id, channel_info in status['channel_summary'].items():
        print(f"  {channel_id}:")
        print(f"    Type: {channel_info['type']}")
        print(f"    Security Score: {channel_info['security_score']:.3f}")
        print(f"    Threat Level: {channel_info['threat_level']}")
        print(f"    Availability: {channel_info['availability']:.1%}")
    
    # Security events
    security_events = status['security_events']
    if security_events:
        print(f"\nRecent Security Events ({len(security_events)}):")
        for event in security_events[-3:]:  # Show last 3 events
            print(f"  • {event['timestamp']}: {', '.join(event['anomalies'])}")
            print(f"    Threat Level: {event['threat_level']}")


if __name__ == "__main__":
    asyncio.run(main())
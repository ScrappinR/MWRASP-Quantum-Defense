"""
Quantum Key Distribution (QKD) Attack Detection System
Detection and analysis of attacks on quantum communication protocols
"""

import time
import hashlib
import secrets
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
import base64


class QKDProtocol(Enum):
    BB84 = "bb84"
    E91 = "e91"
    SARG04 = "sarg04"
    B92 = "b92"
    SIX_STATE = "six_state"
    DECOY_STATE = "decoy_state"
    DIFFERENTIAL_PHASE_SHIFT = "differential_phase_shift"
    COHERENT_ONE_WAY = "coherent_one_way"
    TWIN_FIELD = "twin_field"
    MEASUREMENT_DEVICE_INDEPENDENT = "measurement_device_independent"
    DEVICE_INDEPENDENT = "device_independent"


class QKDAttackType(Enum):
    PHOTON_NUMBER_SPLITTING = "photon_number_splitting"
    INTERCEPT_RESEND = "intercept_resend"
    BEAM_SPLITTING = "beam_splitting"
    TROJAN_HORSE = "trojan_horse"
    BLINDING_ATTACK = "blinding_attack"
    TIME_SHIFT_ATTACK = "time_shift_attack"
    WAVELENGTH_ATTACK = "wavelength_attack"
    PHASE_REMAPPING = "phase_remapping"
    DETECTOR_CONTROL = "detector_control"
    QUANTUM_HACKING = "quantum_hacking"
    SIDE_CHANNEL = "side_channel"
    MAN_IN_THE_MIDDLE = "man_in_the_middle"
    DENIAL_OF_SERVICE = "denial_of_service"
    IMPERSONATION = "impersonation"
    KEY_CORRELATION = "key_correlation"


class PhotonState(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"
    ANTI_DIAGONAL = "anti_diagonal"
    RIGHT_CIRCULAR = "right_circular"
    LEFT_CIRCULAR = "left_circular"
    COHERENT_STATE = "coherent_state"
    VACUUM = "vacuum"
    MULTI_PHOTON = "multi_photon"


class MeasurementBasis(Enum):
    RECTILINEAR = "rectilinear"  # H/V
    DIAGONAL = "diagonal"        # +/- 45°
    CIRCULAR = "circular"        # L/R circular
    BELL_STATE = "bell_state"    # Entangled measurements
    RANDOM = "random"


@dataclass
class QKDTransaction:
    transaction_id: str
    protocol: QKDProtocol
    alice_state: PhotonState
    alice_basis: MeasurementBasis
    bob_basis: MeasurementBasis
    bob_measurement: int  # 0 or 1
    transmission_time: float
    detection_efficiency: float
    error_rate: float
    intensity: float  # Photon intensity (for coherent states)
    wavelength: float
    timing_window: float
    basis_match: bool
    key_bit_used: bool
    
    def is_valid_measurement(self) -> bool:
        """Check if measurement is valid (bases match)"""
        return self.basis_match
    
    def calculate_qber(self, expected_bit: int) -> float:
        """Calculate quantum bit error rate for this measurement"""
        if not self.basis_match:
            return 0.5  # Random result when bases don't match
        
        return 1.0 if self.bob_measurement != expected_bit else 0.0


@dataclass
class QKDSession:
    session_id: str
    protocol: QKDProtocol
    alice_id: str
    bob_id: str
    transactions: List[QKDTransaction] = field(default_factory=list)
    raw_key_bits: List[int] = field(default_factory=list)
    sifted_key_bits: List[int] = field(default_factory=list)
    final_key_bits: List[int] = field(default_factory=list)
    session_start_time: float = 0.0
    session_end_time: float = 0.0
    quantum_bit_error_rate: float = 0.0
    key_generation_rate: float = 0.0
    security_parameter: float = 0.0
    privacy_amplification_ratio: float = 0.0
    
    def calculate_qber(self) -> float:
        """Calculate overall quantum bit error rate"""
        if not self.sifted_key_bits:
            return 0.0
        
        # Compare a sample of bits to estimate error rate
        sample_size = min(100, len(self.sifted_key_bits) // 4)  # Use 25% for error estimation
        if sample_size < 10:
            return 0.0
        
        # Simulate error checking on sample bits
        errors = 0
        for i in range(sample_size):
            # In real QKD, Alice and Bob would compare random bits
            # Here we simulate by checking for consistency
            if i + sample_size < len(self.sifted_key_bits):
                expected_correlation = self.sifted_key_bits[i] ^ self.sifted_key_bits[i + sample_size]
                # High correlation suggests low error rate
                if expected_correlation != 0:  # Simplified error simulation
                    errors += 1
        
        self.quantum_bit_error_rate = errors / sample_size
        return self.quantum_bit_error_rate
    
    def get_session_duration(self) -> float:
        """Get total session duration"""
        return self.session_end_time - self.session_start_time
    
    def is_secure_session(self, qber_threshold: float = 0.11) -> bool:
        """Check if session is secure based on QBER threshold"""
        return self.quantum_bit_error_rate < qber_threshold


@dataclass
class QKDAttackSignature:
    signature_id: str
    attack_type: QKDAttackType
    protocol_targeted: QKDProtocol
    detection_indicators: List[str]
    statistical_anomalies: Dict[str, float]
    confidence_score: float
    detection_timestamp: float
    affected_transactions: List[str]
    mitigation_suggestions: List[str] = field(default_factory=list)


class QuantumKeyDistributionDetector:
    def __init__(self):
        self.qkd_sessions: Dict[str, QKDSession] = {}
        self.attack_signatures: Dict[str, QKDAttackSignature] = {}
        self.protocol_statistics: Dict[QKDProtocol, Dict[str, Any]] = defaultdict(dict)
        
        # Detection parameters
        self.qber_threshold = 0.11  # Standard QKD security threshold
        self.intensity_variance_threshold = 0.15
        self.timing_anomaly_threshold = 0.05  # 50ms
        self.detection_efficiency_threshold = 0.8
        
        # Attack pattern databases
        self.known_attack_patterns = self._initialize_attack_patterns()
        self.statistical_baselines = self._initialize_statistical_baselines()
        
        # Real-time monitoring
        self.transaction_buffer = deque(maxlen=10000)
        self.detection_statistics: Dict[QKDAttackType, int] = defaultdict(int)
        
    def _initialize_attack_patterns(self) -> Dict[QKDAttackType, Dict[str, Any]]:
        """Initialize known QKD attack patterns"""
        return {
            QKDAttackType.PHOTON_NUMBER_SPLITTING: {
                'indicators': [
                    'multi_photon_detection',
                    'intensity_correlation',
                    'basis_correlation_anomaly'
                ],
                'statistical_signatures': {
                    'intensity_variance': {'min': 0.2, 'max': 0.8},
                    'multi_photon_probability': {'min': 0.1, 'max': 1.0},
                    'qber_increase': {'min': 0.02, 'max': 0.15}
                },
                'targeted_protocols': [QKDProtocol.BB84, QKDProtocol.SARG04],
                'countermeasures': ['decoy_states', 'intensity_monitoring']
            },
            
            QKDAttackType.INTERCEPT_RESEND: {
                'indicators': [
                    'increased_qber',
                    'timing_irregularities',
                    'intensity_fluctuations'
                ],
                'statistical_signatures': {
                    'qber_increase': {'min': 0.25, 'max': 0.5},
                    'timing_variance': {'min': 0.001, 'max': 0.01},
                    'detection_efficiency_drop': {'min': 0.1, 'max': 0.3}
                },
                'targeted_protocols': [QKDProtocol.BB84, QKDProtocol.B92],
                'countermeasures': ['authentication', 'statistical_monitoring']
            },
            
            QKDAttackType.BLINDING_ATTACK: {
                'indicators': [
                    'detector_saturation',
                    'detection_efficiency_anomaly',
                    'wavelength_shift'
                ],
                'statistical_signatures': {
                    'detection_efficiency': {'min': 0.0, 'max': 0.1},
                    'intensity_spike': {'min': 10.0, 'max': 1000.0},
                    'basis_bias': {'min': 0.6, 'max': 1.0}
                },
                'targeted_protocols': [QKDProtocol.BB84, QKDProtocol.SARG04],
                'countermeasures': ['detector_monitoring', 'intensity_limits']
            },
            
            QKDAttackType.TIME_SHIFT_ATTACK: {
                'indicators': [
                    'timing_window_manipulation',
                    'detection_time_correlation',
                    'basis_prediction_success'
                ],
                'statistical_signatures': {
                    'timing_shift': {'min': 0.001, 'max': 0.1},
                    'correlation_increase': {'min': 0.1, 'max': 0.3},
                    'basis_guess_accuracy': {'min': 0.6, 'max': 0.9}
                },
                'targeted_protocols': [QKDProtocol.BB84, QKDProtocol.E91],
                'countermeasures': ['random_timing', 'timing_verification']
            },
            
            QKDAttackType.DETECTOR_CONTROL: {
                'indicators': [
                    'detector_response_manipulation',
                    'controlled_detection_pattern',
                    'selective_measurement_success'
                ],
                'statistical_signatures': {
                    'detection_pattern_regularity': {'min': 0.8, 'max': 1.0},
                    'controlled_error_rate': {'min': 0.0, 'max': 0.05},
                    'measurement_bias': {'min': 0.3, 'max': 0.7}
                },
                'targeted_protocols': [QKDProtocol.BB84, QKDProtocol.MEASUREMENT_DEVICE_INDEPENDENT],
                'countermeasures': ['detector_characterization', 'randomness_testing']
            }
        }
    
    def _initialize_statistical_baselines(self) -> Dict[QKDProtocol, Dict[str, Any]]:
        """Initialize statistical baselines for normal QKD operation"""
        return {
            QKDProtocol.BB84: {
                'expected_qber': {'mean': 0.02, 'std': 0.01, 'max_acceptable': 0.11},
                'basis_match_rate': {'mean': 0.5, 'std': 0.05},
                'detection_efficiency': {'mean': 0.85, 'std': 0.05, 'min_acceptable': 0.7},
                'key_generation_rate': {'mean': 1000.0, 'std': 100.0},  # bits/second
                'intensity_variation': {'mean': 0.05, 'std': 0.02}
            },
            
            QKDProtocol.E91: {
                'expected_qber': {'mean': 0.015, 'std': 0.008, 'max_acceptable': 0.09},
                'bell_violation': {'mean': 2.4, 'std': 0.1, 'min_acceptable': 2.0},
                'detection_efficiency': {'mean': 0.8, 'std': 0.06, 'min_acceptable': 0.65},
                'entanglement_fidelity': {'mean': 0.95, 'std': 0.03, 'min_acceptable': 0.85}
            },
            
            QKDProtocol.DECOY_STATE: {
                'expected_qber': {'mean': 0.01, 'std': 0.005, 'max_acceptable': 0.08},
                'decoy_intensity_ratio': {'mean': 0.1, 'std': 0.02},
                'gain_ratio': {'mean': 0.3, 'std': 0.05},
                'security_parameter': {'mean': 1e-6, 'std': 1e-7}
            }
        }
    
    def analyze_qkd_session(
        self,
        access_patterns: List[Dict],
        source_identifier: str,
        session_context: Dict[str, Any] = None
    ) -> Optional[QKDSession]:
        """Analyze access patterns for QKD protocol signatures"""
        
        if len(access_patterns) < 10:
            return None
        
        current_time = time.time()
        
        # Identify QKD protocol from access patterns
        protocol = self._identify_qkd_protocol(access_patterns)
        if protocol is None:
            return None
        
        # Extract QKD transactions
        transactions = self._extract_qkd_transactions(access_patterns, protocol)
        if not transactions:
            return None
        
        # Create QKD session
        session = QKDSession(
            session_id=f"qkd_{secrets.token_hex(8)}_{int(current_time)}",
            protocol=protocol,
            alice_id=session_context.get('alice_id', 'alice') if session_context else 'alice',
            bob_id=session_context.get('bob_id', 'bob') if session_context else 'bob',
            transactions=transactions,
            session_start_time=min(t.transmission_time for t in transactions),
            session_end_time=max(t.transmission_time for t in transactions)
        )
        
        # Process key generation phases
        self._process_key_generation(session)
        
        # Calculate session metrics
        session.calculate_qber()
        session.key_generation_rate = len(session.final_key_bits) / max(session.get_session_duration(), 1.0)
        
        # Store session
        self.qkd_sessions[session.session_id] = session
        
        # Analyze for attacks
        self._analyze_qkd_attacks(session, source_identifier)
        
        return session
    
    def _identify_qkd_protocol(self, access_patterns: List[Dict]) -> Optional[QKDProtocol]:
        """Identify QKD protocol from access patterns"""
        
        protocol_indicators = defaultdict(int)
        
        for access in access_patterns:
            query_type = access.get('query_type', '').lower()
            algorithm_step = access.get('algorithm_step', '').lower()
            value = str(access.get('value', '')).lower()
            
            # BB84 indicators
            if ('bb84' in query_type or 'four_state' in algorithm_step or
                ('rectilinear' in value and 'diagonal' in value)):
                protocol_indicators[QKDProtocol.BB84] += 1
            
            # E91 indicators
            elif ('e91' in query_type or 'bell' in algorithm_step or 'entangle' in value):
                protocol_indicators[QKDProtocol.E91] += 1
            
            # Decoy state indicators
            elif ('decoy' in query_type or 'intensity' in algorithm_step):
                protocol_indicators[QKDProtocol.DECOY_STATE] += 1
            
            # SARG04 indicators
            elif 'sarg' in query_type or 'four_state_unambiguous' in algorithm_step:
                protocol_indicators[QKDProtocol.SARG04] += 1
            
            # Six-state indicators
            elif 'six_state' in query_type or 'circular' in value:
                protocol_indicators[QKDProtocol.SIX_STATE] += 1
            
            # Generic QKD indicators
            elif ('photon' in query_type or 'quantum_key' in algorithm_step or
                  'basis' in value or 'measurement' in algorithm_step):
                # Could be any protocol, add to most common
                if protocol_indicators:
                    max_protocol = max(protocol_indicators, key=protocol_indicators.get)
                    protocol_indicators[max_protocol] += 0.5
                else:
                    protocol_indicators[QKDProtocol.BB84] += 0.5  # Default to BB84
        
        if not protocol_indicators:
            return None
        
        # Return protocol with highest score
        best_protocol = max(protocol_indicators.items(), key=lambda x: x[1])
        return best_protocol[0] if best_protocol[1] >= 3 else None
    
    def _extract_qkd_transactions(self, access_patterns: List[Dict], protocol: QKDProtocol) -> List[QKDTransaction]:
        """Extract QKD transactions from access patterns"""
        transactions = []
        current_time = time.time()
        
        # Group access patterns into transactions
        transaction_groups = self._group_qkd_accesses(access_patterns)
        
        for i, group in enumerate(transaction_groups):
            if len(group) < 2:  # Need at least Alice's send and Bob's receive
                continue
            
            # Extract transaction parameters
            alice_state, alice_basis = self._extract_alice_state(group, protocol)
            bob_basis = self._extract_bob_basis(group, protocol)
            bob_measurement = self._extract_bob_measurement(group)
            
            # Calculate transaction metrics
            transmission_time = min(access.get('time', current_time) for access in group)
            detection_efficiency = self._calculate_detection_efficiency(group)
            error_rate = self._estimate_error_rate(group)
            intensity = self._extract_photon_intensity(group)
            wavelength = self._extract_wavelength(group)
            timing_window = max(access.get('time', 0) for access in group) - transmission_time
            basis_match = self._check_basis_match(alice_basis, bob_basis, protocol)
            
            transaction = QKDTransaction(
                transaction_id=f"qkd_tx_{i}_{secrets.token_hex(4)}",
                protocol=protocol,
                alice_state=alice_state,
                alice_basis=alice_basis,
                bob_basis=bob_basis,
                bob_measurement=bob_measurement,
                transmission_time=transmission_time,
                detection_efficiency=detection_efficiency,
                error_rate=error_rate,
                intensity=intensity,
                wavelength=wavelength,
                timing_window=timing_window,
                basis_match=basis_match,
                key_bit_used=basis_match  # Only matching bases contribute to key
            )
            
            transactions.append(transaction)
            self.transaction_buffer.append(transaction)
        
        return transactions
    
    def _group_qkd_accesses(self, access_patterns: List[Dict]) -> List[List[Dict]]:
        """Group access patterns into QKD transactions"""
        groups = []
        current_group = []
        
        for i, access in enumerate(access_patterns):
            current_group.append(access)
            
            # Start new group if time gap is large or we have enough accesses
            if (len(current_group) >= 4 or 
                (i < len(access_patterns) - 1 and 
                 access_patterns[i+1].get('time', 0) - access.get('time', 0) > 0.01)):
                
                if len(current_group) >= 2:
                    groups.append(current_group)
                current_group = []
        
        # Add final group
        if len(current_group) >= 2:
            groups.append(current_group)
        
        return groups
    
    def _extract_alice_state(self, group: List[Dict], protocol: QKDProtocol) -> Tuple[PhotonState, MeasurementBasis]:
        """Extract Alice's photon state and basis choice"""
        
        # Look for state and basis indicators
        for access in group:
            value = str(access.get('value', '')).lower()
            algorithm_step = access.get('algorithm_step', '').lower()
            
            # Photon state indicators
            if 'horizontal' in value or 'h_state' in algorithm_step:
                state = PhotonState.HORIZONTAL
            elif 'vertical' in value or 'v_state' in algorithm_step:
                state = PhotonState.VERTICAL
            elif 'diagonal' in value and '+' in value:
                state = PhotonState.DIAGONAL
            elif 'diagonal' in value and '-' in value:
                state = PhotonState.ANTI_DIAGONAL
            elif 'coherent' in value:
                state = PhotonState.COHERENT_STATE
            else:
                # Default based on protocol
                state = PhotonState.HORIZONTAL if protocol == QKDProtocol.BB84 else PhotonState.COHERENT_STATE
            
            # Basis indicators
            if 'rectilinear' in value or 'hv_basis' in algorithm_step:
                basis = MeasurementBasis.RECTILINEAR
            elif 'diagonal' in value or 'diag_basis' in algorithm_step:
                basis = MeasurementBasis.DIAGONAL
            elif 'circular' in value:
                basis = MeasurementBasis.CIRCULAR
            elif 'bell' in algorithm_step:
                basis = MeasurementBasis.BELL_STATE
            else:
                # Default basis
                basis = MeasurementBasis.RECTILINEAR
            
            return state, basis
        
        # Fallback defaults
        return PhotonState.HORIZONTAL, MeasurementBasis.RECTILINEAR
    
    def _extract_bob_basis(self, group: List[Dict], protocol: QKDProtocol) -> MeasurementBasis:
        """Extract Bob's measurement basis choice"""
        
        for access in group:
            value = str(access.get('value', '')).lower()
            algorithm_step = access.get('algorithm_step', '').lower()
            
            if 'bob' in algorithm_step or 'receive' in algorithm_step:
                if 'rectilinear' in value:
                    return MeasurementBasis.RECTILINEAR
                elif 'diagonal' in value:
                    return MeasurementBasis.DIAGONAL
                elif 'circular' in value:
                    return MeasurementBasis.CIRCULAR
                elif 'bell' in value:
                    return MeasurementBasis.BELL_STATE
        
        # Random basis selection (typical for QKD)
        return MeasurementBasis.RANDOM
    
    def _extract_bob_measurement(self, group: List[Dict]) -> int:
        """Extract Bob's measurement result"""
        
        for access in group:
            output = access.get('output', 0)
            if isinstance(output, int):
                return output % 2  # Convert to bit
        
        # Random measurement result
        return secrets.randbelow(2)
    
    def _calculate_detection_efficiency(self, group: List[Dict]) -> float:
        """Calculate detection efficiency for this transaction"""
        
        detection_indicators = 0
        total_attempts = len(group)
        
        for access in group:
            if (access.get('output') is not None or 
                'detection' in str(access).lower() or
                'measurement' in str(access).lower()):
                detection_indicators += 1
        
        return detection_indicators / max(total_attempts, 1)
    
    def _estimate_error_rate(self, group: List[Dict]) -> float:
        """Estimate error rate for this transaction"""
        
        error_indicators = sum(
            1 for access in group
            if 'error' in str(access).lower()
        )
        
        return min(0.5, error_indicators / len(group))
    
    def _extract_photon_intensity(self, group: List[Dict]) -> float:
        """Extract photon intensity information"""
        
        for access in group:
            # Look for intensity indicators
            if 'intensity' in str(access).lower():
                try:
                    value = access.get('value', '')
                    if isinstance(value, (int, float)):
                        return float(value)
                    elif isinstance(value, str) and value.replace('.', '').isdigit():
                        return float(value)
                except:
                    pass
        
        # Default intensity (weak coherent pulses)
        return 0.1 + secrets.randbelow(50) / 1000.0
    
    def _extract_wavelength(self, group: List[Dict]) -> float:
        """Extract wavelength information"""
        
        # Look for wavelength indicators
        for access in group:
            if 'wavelength' in str(access).lower() or 'lambda' in str(access).lower():
                try:
                    value = access.get('value', '')
                    if isinstance(value, (int, float)):
                        return float(value)
                except:
                    pass
        
        # Standard telecom wavelengths (1550nm typical)
        return 1550.0 + secrets.randbelow(100)  # 1550-1650 nm range
    
    def _check_basis_match(self, alice_basis: MeasurementBasis, bob_basis: MeasurementBasis, protocol: QKDProtocol) -> bool:
        """Check if Alice and Bob used compatible bases"""
        
        if bob_basis == MeasurementBasis.RANDOM:
            # Random basis selection - 50% chance of match for BB84
            return secrets.randbelow(2) == 0
        
        # Exact basis matching
        if alice_basis == bob_basis:
            return True
        
        # Protocol-specific compatibility
        if protocol == QKDProtocol.E91:
            # E91 uses correlated measurements, not basis matching
            return True  # Entangled pairs always compatible
        
        return False
    
    def _process_key_generation(self, session: QKDSession):
        """Process key generation phases: sifting, error correction, privacy amplification"""
        
        # Phase 1: Raw key (all measurements)
        session.raw_key_bits = [tx.bob_measurement for tx in session.transactions]
        
        # Phase 2: Sifting (keep only matching bases)
        session.sifted_key_bits = [
            tx.bob_measurement for tx in session.transactions
            if tx.basis_match
        ]
        
        # Phase 3: Error correction and privacy amplification
        if session.sifted_key_bits:
            # Simulate error correction (removes some bits)
            error_correction_loss = 0.1  # 10% overhead
            corrected_length = int(len(session.sifted_key_bits) * (1 - error_correction_loss))
            
            # Simulate privacy amplification (removes more bits for security)
            privacy_amplification_loss = 0.2  # 20% for privacy
            final_length = int(corrected_length * (1 - privacy_amplification_loss))
            
            # Generate final key bits (simplified)
            session.final_key_bits = session.sifted_key_bits[:final_length]
            session.privacy_amplification_ratio = privacy_amplification_loss
    
    def _analyze_qkd_attacks(self, session: QKDSession, source_identifier: str):
        """Analyze QKD session for potential attacks"""
        
        detected_attacks = []
        
        # Check each known attack type
        for attack_type, attack_pattern in self.known_attack_patterns.items():
            if session.protocol not in attack_pattern.get('targeted_protocols', []):
                continue
            
            attack_confidence = self._detect_specific_attack(session, attack_type, attack_pattern)
            
            if attack_confidence > 0.7:  # High confidence threshold
                signature = QKDAttackSignature(
                    signature_id=f"qkd_attack_{secrets.token_hex(6)}",
                    attack_type=attack_type,
                    protocol_targeted=session.protocol,
                    detection_indicators=self._get_attack_indicators(session, attack_pattern),
                    statistical_anomalies=self._calculate_statistical_anomalies(session, attack_pattern),
                    confidence_score=attack_confidence,
                    detection_timestamp=time.time(),
                    affected_transactions=[tx.transaction_id for tx in session.transactions],
                    mitigation_suggestions=attack_pattern.get('countermeasures', [])
                )
                
                self.attack_signatures[signature.signature_id] = signature
                detected_attacks.append(signature)
                
                # Log attack detection
                print(f"QKD ATTACK DETECTED: {attack_type.value}")
                print(f"Protocol: {session.protocol.value}")
                print(f"Confidence: {attack_confidence:.3f}")
                print(f"QBER: {session.quantum_bit_error_rate:.4f}")
                print(f"Session: {session.session_id}")
                
                self.detection_statistics[attack_type] += 1
        
        return detected_attacks
    
    def _detect_specific_attack(self, session: QKDSession, attack_type: QKDAttackType, attack_pattern: Dict) -> float:
        """Detect specific attack type with confidence score"""
        
        confidence_scores = []
        statistical_signatures = attack_pattern.get('statistical_signatures', {})
        
        # Check QBER anomalies
        if 'qber_increase' in statistical_signatures:
            qber_range = statistical_signatures['qber_increase']
            if qber_range['min'] <= session.quantum_bit_error_rate <= qber_range['max']:
                confidence_scores.append(0.8)
        
        # Check timing anomalies
        if session.transactions:
            timing_variance = np.var([tx.timing_window for tx in session.transactions])
            
            if 'timing_variance' in statistical_signatures:
                timing_range = statistical_signatures['timing_variance']
                if timing_range['min'] <= timing_variance <= timing_range['max']:
                    confidence_scores.append(0.7)
        
        # Check detection efficiency anomalies
        avg_detection_efficiency = np.mean([tx.detection_efficiency for tx in session.transactions])
        
        if 'detection_efficiency' in statistical_signatures:
            det_eff_range = statistical_signatures['detection_efficiency']
            if det_eff_range['min'] <= avg_detection_efficiency <= det_eff_range['max']:
                confidence_scores.append(0.6)
        
        # Check intensity anomalies
        if session.transactions:
            intensities = [tx.intensity for tx in session.transactions]
            intensity_variance = np.var(intensities)
            
            if 'intensity_variance' in statistical_signatures:
                intensity_range = statistical_signatures['intensity_variance']
                if intensity_range['min'] <= intensity_variance <= intensity_range['max']:
                    confidence_scores.append(0.5)
        
        # Specific attack patterns
        if attack_type == QKDAttackType.PHOTON_NUMBER_SPLITTING:
            # Check for multi-photon signatures
            multi_photon_count = sum(
                1 for tx in session.transactions 
                if tx.intensity > 0.5  # High intensity suggests multi-photon
            )
            if multi_photon_count > len(session.transactions) * 0.2:
                confidence_scores.append(0.9)
        
        elif attack_type == QKDAttackType.INTERCEPT_RESEND:
            # Check for increased error rate and timing irregularities
            if session.quantum_bit_error_rate > 0.25:  # High QBER
                confidence_scores.append(0.8)
            
            # Check for timing patterns
            timing_windows = [tx.timing_window for tx in session.transactions]
            if timing_windows and np.std(timing_windows) > 0.005:  # High timing variance
                confidence_scores.append(0.6)
        
        elif attack_type == QKDAttackType.BLINDING_ATTACK:
            # Check for detection efficiency drops
            if avg_detection_efficiency < 0.1:  # Very low detection
                confidence_scores.append(0.95)
            
            # Check for intensity spikes
            max_intensity = max(tx.intensity for tx in session.transactions) if session.transactions else 0
            if max_intensity > 10.0:  # Very high intensity
                confidence_scores.append(0.8)
        
        # Return average confidence
        return np.mean(confidence_scores) if confidence_scores else 0.0
    
    def _get_attack_indicators(self, session: QKDSession, attack_pattern: Dict) -> List[str]:
        """Get list of attack indicators found in session"""
        
        indicators = []
        pattern_indicators = attack_pattern.get('indicators', [])
        
        # Check for each indicator
        for indicator in pattern_indicators:
            if indicator == 'increased_qber' and session.quantum_bit_error_rate > 0.15:
                indicators.append(f"High QBER: {session.quantum_bit_error_rate:.4f}")
            
            elif indicator == 'multi_photon_detection':
                high_intensity_count = sum(1 for tx in session.transactions if tx.intensity > 0.5)
                if high_intensity_count > 0:
                    indicators.append(f"Multi-photon events: {high_intensity_count}")
            
            elif indicator == 'detector_saturation':
                low_efficiency_count = sum(1 for tx in session.transactions if tx.detection_efficiency < 0.1)
                if low_efficiency_count > 0:
                    indicators.append(f"Detector saturation events: {low_efficiency_count}")
            
            elif indicator == 'timing_irregularities':
                timing_windows = [tx.timing_window for tx in session.transactions]
                if timing_windows and np.std(timing_windows) > 0.01:
                    indicators.append(f"Timing variance: {np.std(timing_windows):.6f}")
        
        return indicators
    
    def _calculate_statistical_anomalies(self, session: QKDSession, attack_pattern: Dict) -> Dict[str, float]:
        """Calculate statistical anomalies for the session"""
        
        anomalies = {}
        baseline = self.statistical_baselines.get(session.protocol, {})
        
        # QBER anomaly
        expected_qber = baseline.get('expected_qber', {})
        if expected_qber:
            qber_z_score = abs(session.quantum_bit_error_rate - expected_qber.get('mean', 0.02)) / expected_qber.get('std', 0.01)
            anomalies['qber_z_score'] = qber_z_score
        
        # Detection efficiency anomaly
        if session.transactions:
            avg_det_eff = np.mean([tx.detection_efficiency for tx in session.transactions])
            expected_det_eff = baseline.get('detection_efficiency', {})
            if expected_det_eff:
                det_eff_z_score = abs(avg_det_eff - expected_det_eff.get('mean', 0.8)) / expected_det_eff.get('std', 0.05)
                anomalies['detection_efficiency_z_score'] = det_eff_z_score
        
        # Intensity variation anomaly
        if session.transactions:
            intensities = [tx.intensity for tx in session.transactions]
            intensity_cv = np.std(intensities) / max(np.mean(intensities), 0.01)  # Coefficient of variation
            expected_intensity_var = baseline.get('intensity_variation', {})
            if expected_intensity_var:
                intensity_anomaly = abs(intensity_cv - expected_intensity_var.get('mean', 0.05)) / expected_intensity_var.get('std', 0.02)
                anomalies['intensity_variation_anomaly'] = intensity_anomaly
        
        # Key generation rate anomaly
        expected_key_rate = baseline.get('key_generation_rate', {})
        if expected_key_rate:
            key_rate_z_score = abs(session.key_generation_rate - expected_key_rate.get('mean', 1000)) / expected_key_rate.get('std', 100)
            anomalies['key_generation_rate_z_score'] = key_rate_z_score
        
        return anomalies
    
    def get_qkd_security_analysis(self) -> Dict[str, Any]:
        """Get comprehensive QKD security analysis"""
        current_time = time.time()
        
        analysis = {
            'total_sessions_analyzed': len(self.qkd_sessions),
            'protocols_detected': {},
            'attack_detection_statistics': dict(self.detection_statistics),
            'security_metrics': {},
            'recent_sessions': [],
            'attack_signatures': len(self.attack_signatures),
            'protocol_security_assessment': {},
            'transaction_buffer_size': len(self.transaction_buffer)
        }
        
        # Protocol distribution
        protocol_distribution = defaultdict(int)
        qber_by_protocol = defaultdict(list)
        key_rates_by_protocol = defaultdict(list)
        
        for session in self.qkd_sessions.values():
            protocol_distribution[session.protocol.value] += 1
            qber_by_protocol[session.protocol.value].append(session.quantum_bit_error_rate)
            key_rates_by_protocol[session.protocol.value].append(session.key_generation_rate)
        
        analysis['protocols_detected'] = dict(protocol_distribution)
        
        # Security metrics
        all_qbers = []
        secure_sessions = 0
        
        for session in self.qkd_sessions.values():
            all_qbers.append(session.quantum_bit_error_rate)
            if session.is_secure_session(self.qber_threshold):
                secure_sessions += 1
        
        if all_qbers:
            analysis['security_metrics'] = {
                'overall_qber_mean': np.mean(all_qbers),
                'overall_qber_std': np.std(all_qbers),
                'secure_sessions_percentage': secure_sessions / len(self.qkd_sessions),
                'sessions_above_threshold': sum(1 for q in all_qbers if q > self.qber_threshold),
                'max_qber_detected': max(all_qbers),
                'min_qber_detected': min(all_qbers)
            }
        
        # Recent sessions (last 5 minutes)
        recent_sessions = [
            session for session in self.qkd_sessions.values()
            if current_time - session.session_end_time < 300.0
        ]
        
        analysis['recent_sessions'] = [
            {
                'session_id': session.session_id,
                'protocol': session.protocol.value,
                'qber': session.quantum_bit_error_rate,
                'key_generation_rate': session.key_generation_rate,
                'transaction_count': len(session.transactions),
                'duration': session.get_session_duration(),
                'secure': session.is_secure_session(),
                'final_key_length': len(session.final_key_bits)
            }
            for session in recent_sessions[-10:]  # Last 10 recent sessions
        ]
        
        # Protocol security assessment
        for protocol, qbers in qber_by_protocol.items():
            if qbers:
                key_rates = key_rates_by_protocol[protocol]
                analysis['protocol_security_assessment'][protocol] = {
                    'session_count': len(qbers),
                    'average_qber': np.mean(qbers),
                    'qber_stability': 1.0 / (1.0 + np.std(qbers)),  # Higher is more stable
                    'average_key_rate': np.mean(key_rates),
                    'security_violations': sum(1 for q in qbers if q > self.qber_threshold),
                    'recommended_threshold': min(0.11, np.mean(qbers) + 2 * np.std(qbers))
                }
        
        return analysis
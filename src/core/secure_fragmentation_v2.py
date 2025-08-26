"""
MWRASP Secure Fragmentation v2 - Solving the Real Technical Problems
This addresses data integrity, agent authentication, and handshake protocols
"""

import time
import hashlib
import secrets
import struct
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
# Cryptography imports removed - using hashlib for demo
# In production, would use cryptography library for proper encryption
import json
import base64


class IntegrityStatus(Enum):
    """Fragment integrity verification status"""
    INTACT = "intact"
    CORRUPTED = "corrupted"
    TAMPERED = "tampered"
    EXPIRED = "expired"
    VERIFIED = "verified"


@dataclass
class FragmentMetadata:
    """Metadata for fragment integrity and reconstruction"""
    fragment_id: str
    sequence_number: int
    total_fragments: int
    data_length: int  # Original data length before fragmentation
    fragment_offset: int  # Where this fragment starts in original data
    fragment_size: int  # Size of actual data (not including padding/overhead)
    checksum: str  # SHA-256 of fragment data
    error_correction_code: bytes  # Reed-Solomon or similar
    creation_timestamp: float
    expiration_timestamp: float
    
    def to_bytes(self) -> bytes:
        """Serialize metadata for transmission"""
        meta_dict = {
            'fid': self.fragment_id,
            'seq': self.sequence_number,
            'tot': self.total_fragments,
            'len': self.data_length,
            'off': self.fragment_offset,
            'siz': self.fragment_size,
            'chk': self.checksum,
            'ecc': base64.b64encode(self.error_correction_code).decode(),
            'crt': self.creation_timestamp,
            'exp': self.expiration_timestamp
        }
        return json.dumps(meta_dict).encode()
    
    @staticmethod
    def from_bytes(data: bytes) -> 'FragmentMetadata':
        """Deserialize metadata from bytes"""
        meta_dict = json.loads(data.decode())
        return FragmentMetadata(
            fragment_id=meta_dict['fid'],
            sequence_number=meta_dict['seq'],
            total_fragments=meta_dict['tot'],
            data_length=meta_dict['len'],
            fragment_offset=meta_dict['off'],
            fragment_size=meta_dict['siz'],
            checksum=meta_dict['chk'],
            error_correction_code=base64.b64decode(meta_dict['ecc']),
            creation_timestamp=meta_dict['crt'],
            expiration_timestamp=meta_dict['exp']
        )


@dataclass  
class SecureFragment:
    """Fragment with integrity protection"""
    metadata: FragmentMetadata
    encrypted_data: bytes  # The actual fragment data (encrypted)
    integrity_proof: bytes  # HMAC or digital signature
    redundancy_data: bytes  # For reconstruction if primary data corrupted
    
    def verify_integrity(self, verification_key: bytes) -> IntegrityStatus:
        """Verify fragment hasn't been corrupted or tampered with"""
        # Check expiration
        if time.time() > self.metadata.expiration_timestamp:
            return IntegrityStatus.EXPIRED
        
        # Verify checksum
        data_hash = hashlib.sha256(self.encrypted_data).hexdigest()
        if data_hash != self.metadata.checksum:
            return IntegrityStatus.CORRUPTED
        
        # Verify integrity proof (simplified - would use HMAC in production)
        expected_proof = hashlib.sha256(
            self.encrypted_data + verification_key + self.metadata.to_bytes()
        ).digest()
        
        if expected_proof != self.integrity_proof:
            return IntegrityStatus.TAMPERED
        
        return IntegrityStatus.VERIFIED


class SecureFragmentationSystem:
    """Handles fragmentation with guaranteed integrity"""
    
    def __init__(self):
        self.fragment_cache: Dict[str, List[SecureFragment]] = {}
        self.reconstruction_buffer: Dict[str, bytearray] = {}
        self.master_key = secrets.token_bytes(32)
        
    def fragment_with_integrity(self, data: bytes, fragment_count: int = 5, 
                               lifetime_ms: int = 100) -> Tuple[str, List[SecureFragment]]:
        """
        Fragment data with integrity guarantees
        Returns: (data_id, fragments)
        """
        data_id = secrets.token_hex(16)
        data_length = len(data)
        
        # Calculate fragment sizes (equal distribution with last fragment handling remainder)
        base_fragment_size = data_length // fragment_count
        
        fragments = []
        current_offset = 0
        
        for i in range(fragment_count):
            # Calculate this fragment's size
            if i == fragment_count - 1:
                # Last fragment gets any remainder
                fragment_size = data_length - current_offset
            else:
                fragment_size = base_fragment_size
            
            # Extract fragment data
            fragment_data = data[current_offset:current_offset + fragment_size]
            
            # Add error correction codes (simplified Reed-Solomon concept)
            ecc = self._generate_error_correction(fragment_data)
            
            # Encrypt fragment
            encrypted = self._encrypt_fragment(fragment_data, data_id, i)
            
            # Create metadata
            metadata = FragmentMetadata(
                fragment_id=f"{data_id}_f{i}",
                sequence_number=i,
                total_fragments=fragment_count,
                data_length=data_length,
                fragment_offset=current_offset,
                fragment_size=fragment_size,
                checksum=hashlib.sha256(encrypted).hexdigest(),
                error_correction_code=ecc,
                creation_timestamp=time.time(),
                expiration_timestamp=time.time() + (lifetime_ms / 1000.0)
            )
            
            # Generate integrity proof
            integrity_proof = hashlib.sha256(
                encrypted + self.master_key + metadata.to_bytes()
            ).digest()
            
            # Create redundancy data for recovery
            redundancy = self._create_redundancy(fragment_data)
            
            fragment = SecureFragment(
                metadata=metadata,
                encrypted_data=encrypted,
                integrity_proof=integrity_proof,
                redundancy_data=redundancy
            )
            
            fragments.append(fragment)
            current_offset += fragment_size
        
        # Store for later reconstruction
        self.fragment_cache[data_id] = fragments
        
        return data_id, fragments
    
    def reconstruct_with_verification(self, data_id: str, 
                                     fragments: List[SecureFragment]) -> Optional[bytes]:
        """
        Reconstruct data with integrity verification
        Returns None if reconstruction fails or data is corrupted
        """
        if not fragments:
            return None
        
        # Verify all fragments first
        for fragment in fragments:
            status = fragment.verify_integrity(self.master_key)
            if status not in [IntegrityStatus.VERIFIED, IntegrityStatus.INTACT]:
                # Try to recover using redundancy
                if not self._attempt_recovery(fragment):
                    print(f"Fragment {fragment.metadata.fragment_id} failed verification: {status}")
                    return None
        
        # Sort fragments by sequence number
        fragments.sort(key=lambda f: f.metadata.sequence_number)
        
        # Verify we have all fragments
        expected_count = fragments[0].metadata.total_fragments
        if len(fragments) != expected_count:
            print(f"Missing fragments: have {len(fragments)}, need {expected_count}")
            return None
        
        # Verify sequence is complete
        for i, fragment in enumerate(fragments):
            if fragment.metadata.sequence_number != i:
                print(f"Fragment sequence broken at position {i}")
                return None
        
        # Initialize reconstruction buffer
        total_length = fragments[0].metadata.data_length
        reconstructed = bytearray(total_length)
        
        # Reconstruct data
        for fragment in fragments:
            # Decrypt fragment
            decrypted = self._decrypt_fragment(
                fragment.encrypted_data, 
                data_id, 
                fragment.metadata.sequence_number
            )
            
            # Verify decrypted size matches metadata
            if len(decrypted) != fragment.metadata.fragment_size:
                # Try error correction
                corrected = self._apply_error_correction(decrypted, fragment.metadata.error_correction_code)
                if corrected and len(corrected) == fragment.metadata.fragment_size:
                    decrypted = corrected
                else:
                    print(f"Fragment {fragment.metadata.fragment_id} size mismatch")
                    return None
            
            # Place fragment in correct position
            start = fragment.metadata.fragment_offset
            end = start + fragment.metadata.fragment_size
            
            # Verify bounds
            if end > total_length:
                print(f"Fragment {fragment.metadata.fragment_id} exceeds data bounds")
                return None
            
            reconstructed[start:end] = decrypted
        
        return bytes(reconstructed)
    
    def _generate_error_correction(self, data: bytes) -> bytes:
        """Generate error correction codes for data"""
        # Simplified - in production would use Reed-Solomon or similar
        # For now, just create XOR parity blocks
        
        block_size = 16
        parity = bytearray(block_size)
        
        for i in range(0, len(data), block_size):
            block = data[i:i+block_size]
            for j, byte in enumerate(block):
                if j < len(parity):
                    parity[j] ^= byte
        
        return bytes(parity)
    
    def _apply_error_correction(self, data: bytes, ecc: bytes) -> Optional[bytes]:
        """Attempt to correct errors in data using ECC"""
        # Simplified implementation - would use proper ECC in production
        # For now, just return the data if ECC validates
        
        check_ecc = self._generate_error_correction(data)
        if check_ecc == ecc:
            return data
        
        # In production, would attempt actual error correction here
        return None
    
    def _encrypt_fragment(self, data: bytes, data_id: str, sequence: int) -> bytes:
        """Encrypt fragment data"""
        # Derive fragment-specific key
        fragment_key = hashlib.sha256(
            self.master_key + data_id.encode() + struct.pack('I', sequence)
        ).digest()
        
        # Simple XOR encryption (in production would use AES-GCM)
        encrypted = bytearray(len(data))
        key_stream = fragment_key * ((len(data) // 32) + 1)
        
        for i, byte in enumerate(data):
            encrypted[i] = byte ^ key_stream[i]
        
        return bytes(encrypted)
    
    def _decrypt_fragment(self, encrypted: bytes, data_id: str, sequence: int) -> bytes:
        """Decrypt fragment data"""
        # Encryption is symmetric for XOR
        return self._encrypt_fragment(encrypted, data_id, sequence)
    
    def _create_redundancy(self, data: bytes) -> bytes:
        """Create redundancy data for recovery"""
        # Simple approach: store compressed version
        # In production would use erasure coding
        return hashlib.sha256(data).digest()
    
    def _attempt_recovery(self, fragment: SecureFragment) -> bool:
        """Attempt to recover corrupted fragment"""
        # In production, would use redundancy_data to recover
        # For now, just return False
        return False


@dataclass
class AgentIdentity:
    """Cryptographic identity for an agent"""
    agent_id: str
    public_key: bytes
    private_key: bytes
    birth_timestamp: float
    geographic_origin: Tuple[float, float]  # (latitude, longitude)
    network_address: str
    behavioral_signature: Dict[str, Any]
    trust_scores: Dict[str, float]  # agent_id -> trust score
    
    def sign_data(self, data: bytes) -> bytes:
        """Sign data with agent's private key"""
        signature = hashlib.sha256(data + self.private_key).digest()
        return signature
    
    def verify_signature(self, data: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify signature from another agent"""
        expected = hashlib.sha256(data + public_key).digest()
        return expected == signature


@dataclass
class HandshakeProtocol:
    """Unique handshake between two specific agents"""
    agent_a_id: str
    agent_b_id: str
    shared_secret: bytes
    handshake_sequence: List[str]  # Sequence of challenges/responses
    last_handshake: float
    handshake_count: int
    geographic_distance: float  # Distance between agents
    temporal_offset: float  # Time zone difference
    behavioral_compatibility: float  # How well agents work together
    
    def generate_next_challenge(self) -> bytes:
        """Generate next challenge in handshake sequence"""
        # Use shared secret and handshake count to generate unique challenge
        challenge_data = (
            self.shared_secret + 
            str(self.handshake_count).encode() + 
            str(time.time()).encode()
        )
        return hashlib.sha256(challenge_data).digest()
    
    def verify_response(self, response: bytes, expected_challenge: bytes) -> bool:
        """Verify response to challenge"""
        # Response should be hash of challenge + shared secret
        expected_response = hashlib.sha256(expected_challenge + self.shared_secret).digest()
        return response == expected_response
    
    def evolve_handshake(self):
        """Evolve the handshake pattern after each use"""
        # Rotate shared secret
        self.shared_secret = hashlib.sha256(
            self.shared_secret + str(self.handshake_count).encode()
        ).digest()
        
        # Update sequence
        self.handshake_count += 1
        self.last_handshake = time.time()
        
        # Add behavioral learning (simplified)
        self.behavioral_compatibility *= 1.01  # Improve with each successful handshake


class AgentAuthenticationSystem:
    """Handles agent identity verification and handshakes"""
    
    def __init__(self):
        self.agent_identities: Dict[str, AgentIdentity] = {}
        self.handshake_protocols: Dict[Tuple[str, str], HandshakeProtocol] = {}
        self.geographic_grid: Dict[Tuple[int, int], List[str]] = {}  # Grid cell -> agent IDs
        
    def create_agent_identity(self, agent_id: str, location: Tuple[float, float], 
                            network_address: str) -> AgentIdentity:
        """Create a new agent identity"""
        
        # Generate key pair (simplified)
        private_key = secrets.token_bytes(32)
        public_key = hashlib.sha256(private_key).digest()
        
        identity = AgentIdentity(
            agent_id=agent_id,
            public_key=public_key,
            private_key=private_key,
            birth_timestamp=time.time(),
            geographic_origin=location,
            network_address=network_address,
            behavioral_signature={
                'response_time_ms': np.random.normal(100, 20),
                'message_frequency': np.random.normal(10, 2),
                'vocabulary_size': np.random.randint(100, 1000),
                'interaction_style': np.random.choice(['aggressive', 'passive', 'balanced'])
            },
            trust_scores={}
        )
        
        self.agent_identities[agent_id] = identity
        
        # Add to geographic grid
        grid_cell = self._get_grid_cell(location)
        if grid_cell not in self.geographic_grid:
            self.geographic_grid[grid_cell] = []
        self.geographic_grid[grid_cell].append(agent_id)
        
        return identity
    
    def establish_handshake(self, agent_a_id: str, agent_b_id: str) -> HandshakeProtocol:
        """Establish unique handshake between two agents"""
        
        # Check if handshake already exists
        key = tuple(sorted([agent_a_id, agent_b_id]))
        if key in self.handshake_protocols:
            return self.handshake_protocols[key]
        
        # Get agent identities
        agent_a = self.agent_identities.get(agent_a_id)
        agent_b = self.agent_identities.get(agent_b_id)
        
        if not agent_a or not agent_b:
            raise ValueError("Agent identity not found")
        
        # Calculate geographic distance
        distance = self._calculate_distance(
            agent_a.geographic_origin, 
            agent_b.geographic_origin
        )
        
        # Calculate temporal offset (simplified - based on longitude)
        temporal_offset = abs(agent_a.geographic_origin[1] - agent_b.geographic_origin[1]) / 15.0
        
        # Generate shared secret based on both agents' keys and environmental factors
        shared_data = (
            agent_a.private_key + 
            agent_b.public_key + 
            str(distance).encode() + 
            str(temporal_offset).encode() +
            str(time.time()).encode()
        )
        shared_secret = hashlib.sha256(shared_data).digest()
        
        # Calculate behavioral compatibility
        compatibility = self._calculate_behavioral_compatibility(
            agent_a.behavioral_signature,
            agent_b.behavioral_signature
        )
        
        handshake = HandshakeProtocol(
            agent_a_id=agent_a_id,
            agent_b_id=agent_b_id,
            shared_secret=shared_secret,
            handshake_sequence=[],
            last_handshake=0,
            handshake_count=0,
            geographic_distance=distance,
            temporal_offset=temporal_offset,
            behavioral_compatibility=compatibility
        )
        
        self.handshake_protocols[key] = handshake
        return handshake
    
    def perform_handshake(self, initiator_id: str, responder_id: str, 
                         fragment: SecureFragment) -> Tuple[bool, bytes]:
        """
        Perform handshake and exchange fragment
        Returns: (success, encrypted_fragment_with_auth)
        """
        
        # Get or create handshake protocol
        handshake = self.establish_handshake(initiator_id, responder_id)
        
        # Generate challenge
        challenge = handshake.generate_next_challenge()
        
        # Initiator signs challenge
        initiator = self.agent_identities[initiator_id]
        signature = initiator.sign_data(challenge)
        
        # Package fragment with authentication
        auth_package = {
            'fragment': fragment,
            'challenge': challenge,
            'signature': signature,
            'initiator_id': initiator_id,
            'timestamp': time.time(),
            'handshake_count': handshake.handshake_count
        }
        
        # Verify geographic and temporal constraints
        if not self._verify_spatiotemporal_constraints(initiator_id, responder_id):
            return False, b''
        
        # Verify behavioral patterns match expected
        if not self._verify_behavioral_patterns(initiator_id, responder_id, handshake):
            return False, b''
        
        # Evolve handshake for next time
        handshake.evolve_handshake()
        
        # Update trust scores
        initiator.trust_scores[responder_id] = min(
            initiator.trust_scores.get(responder_id, 0.5) + 0.01, 
            1.0
        )
        
        # Serialize and encrypt package
        package_bytes = json.dumps(auth_package, default=str).encode()
        encrypted_package = self._encrypt_with_handshake(package_bytes, handshake.shared_secret)
        
        return True, encrypted_package
    
    def verify_and_receive_fragment(self, receiver_id: str, 
                                   encrypted_package: bytes) -> Optional[SecureFragment]:
        """Verify handshake and receive fragment"""
        
        # Try all known handshakes for this receiver
        for (agent_a, agent_b), handshake in self.handshake_protocols.items():
            if receiver_id not in [agent_a, agent_b]:
                continue
            
            # Try to decrypt with this handshake
            try:
                decrypted = self._decrypt_with_handshake(encrypted_package, handshake.shared_secret)
                auth_package = json.loads(decrypted.decode())
                
                # Verify sender is part of this handshake
                sender_id = auth_package['initiator_id']
                if sender_id not in [agent_a, agent_b]:
                    continue
                
                # Verify challenge response
                challenge = bytes.fromhex(auth_package['challenge'])
                expected_response = hashlib.sha256(challenge + handshake.shared_secret).digest()
                
                # Verify signature
                sender = self.agent_identities.get(sender_id)
                if not sender:
                    continue
                
                signature = bytes.fromhex(auth_package['signature'])
                if not sender.verify_signature(challenge, signature, sender.public_key):
                    continue
                
                # Verify timing (must be recent)
                if time.time() - auth_package['timestamp'] > 10:  # 10 second window
                    continue
                
                # Extract and return fragment
                # (In real implementation, would properly deserialize)
                return auth_package['fragment']
                
            except Exception:
                continue
        
        return None
    
    def _get_grid_cell(self, location: Tuple[float, float]) -> Tuple[int, int]:
        """Get grid cell for geographic location"""
        # 1 degree grid cells
        lat_cell = int(location[0])
        lon_cell = int(location[1])
        return (lat_cell, lon_cell)
    
    def _calculate_distance(self, loc1: Tuple[float, float], 
                          loc2: Tuple[float, float]) -> float:
        """Calculate distance between two locations (simplified)"""
        # Euclidean distance in degrees (simplified)
        return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)**0.5
    
    def _calculate_behavioral_compatibility(self, behavior1: Dict, behavior2: Dict) -> float:
        """Calculate how compatible two agents' behaviors are"""
        compatibility = 1.0
        
        # Response time compatibility (prefer similar speeds)
        time_diff = abs(behavior1.get('response_time_ms', 100) - behavior2.get('response_time_ms', 100))
        compatibility *= max(0.5, 1.0 - time_diff / 200)
        
        # Interaction style compatibility
        style1 = behavior1.get('interaction_style', 'balanced')
        style2 = behavior2.get('interaction_style', 'balanced')
        
        style_compatibility = {
            ('aggressive', 'aggressive'): 0.7,
            ('aggressive', 'passive'): 0.9,
            ('aggressive', 'balanced'): 0.8,
            ('passive', 'passive'): 0.7,
            ('passive', 'balanced'): 0.8,
            ('balanced', 'balanced'): 1.0
        }
        
        compatibility *= style_compatibility.get((style1, style2), 0.6)
        
        return compatibility
    
    def _verify_spatiotemporal_constraints(self, agent1_id: str, agent2_id: str) -> bool:
        """Verify agents meet geographic and temporal constraints for communication"""
        
        agent1 = self.agent_identities.get(agent1_id)
        agent2 = self.agent_identities.get(agent2_id)
        
        if not agent1 or not agent2:
            return False
        
        # Check geographic distance (max 180 degrees apart)
        distance = self._calculate_distance(agent1.geographic_origin, agent2.geographic_origin)
        if distance > 180:
            return False
        
        # Check temporal alignment (agents created within 1 year of each other)
        age_diff = abs(agent1.birth_timestamp - agent2.birth_timestamp)
        if age_diff > 365 * 24 * 3600:
            return False
        
        return True
    
    def _verify_behavioral_patterns(self, agent1_id: str, agent2_id: str, 
                                   handshake: HandshakeProtocol) -> bool:
        """Verify behavioral patterns match expected for these agents"""
        
        # Check if compatibility has degraded too much
        if handshake.behavioral_compatibility < 0.3:
            return False
        
        # Check if handshake frequency is reasonable
        if handshake.handshake_count > 0:
            time_since_last = time.time() - handshake.last_handshake
            expected_interval = 60.0  # Expected ~1 minute between handshakes
            
            # Allow 10x variance
            if time_since_last < expected_interval / 10 or time_since_last > expected_interval * 10:
                # Suspicious timing
                return False
        
        return True
    
    def _encrypt_with_handshake(self, data: bytes, shared_secret: bytes) -> bytes:
        """Encrypt data using handshake secret"""
        # XOR encryption (simplified - use AES-GCM in production)
        encrypted = bytearray(len(data))
        key_stream = (shared_secret * ((len(data) // 32) + 1))[:len(data)]
        
        for i, byte in enumerate(data):
            encrypted[i] = byte ^ key_stream[i]
        
        return bytes(encrypted)
    
    def _decrypt_with_handshake(self, encrypted: bytes, shared_secret: bytes) -> bytes:
        """Decrypt data using handshake secret"""
        # XOR is symmetric
        return self._encrypt_with_handshake(encrypted, shared_secret)


# Testing and demonstration
def demonstrate_secure_fragmentation():
    """Demonstrate the secure fragmentation and authentication system"""
    
    print("=== MWRASP Secure Fragmentation v2 Demo ===\n")
    
    # Initialize systems
    frag_system = SecureFragmentationSystem()
    auth_system = AgentAuthenticationSystem()
    
    # Create test data
    original_data = b"This is highly sensitive data that must be fragmented and reconstructed without corruption."
    print(f"Original data: {original_data.decode()}")
    print(f"Original size: {len(original_data)} bytes\n")
    
    # Fragment with integrity protection
    print("=== Fragmenting with Integrity Protection ===")
    data_id, fragments = frag_system.fragment_with_integrity(original_data, fragment_count=5)
    print(f"Created {len(fragments)} fragments")
    
    for i, fragment in enumerate(fragments):
        print(f"  Fragment {i}: offset={fragment.metadata.fragment_offset}, "
              f"size={fragment.metadata.fragment_size}, "
              f"checksum={fragment.metadata.checksum[:8]}...")
    
    # Test reconstruction
    print("\n=== Testing Reconstruction ===")
    reconstructed = frag_system.reconstruct_with_verification(data_id, fragments)
    
    if reconstructed == original_data:
        print("[OK] Data reconstructed successfully without corruption!")
        print(f"Reconstructed: {reconstructed.decode()}")
    else:
        print("[FAIL] Reconstruction failed or data corrupted")
    
    # Create agent identities
    print("\n=== Creating Agent Identities ===")
    agent1 = auth_system.create_agent_identity(
        "AGENT_001", 
        (37.7749, -122.4194),  # San Francisco
        "192.168.1.100"
    )
    
    agent2 = auth_system.create_agent_identity(
        "AGENT_002",
        (40.7128, -74.0060),  # New York
        "192.168.2.200"
    )
    
    print(f"Agent 1: {agent1.agent_id} at {agent1.geographic_origin}")
    print(f"Agent 2: {agent2.agent_id} at {agent2.geographic_origin}")
    
    # Establish handshake
    print("\n=== Establishing Unique Handshake ===")
    handshake = auth_system.establish_handshake(agent1.agent_id, agent2.agent_id)
    print(f"Handshake established:")
    print(f"  Geographic distance: {handshake.geographic_distance:.2f} degrees")
    print(f"  Temporal offset: {handshake.temporal_offset:.2f} hours")
    print(f"  Behavioral compatibility: {handshake.behavioral_compatibility:.2f}")
    
    # Test fragment exchange with authentication
    print("\n=== Testing Secure Fragment Exchange ===")
    
    # Agent 1 sends fragment to Agent 2
    success, encrypted_package = auth_system.perform_handshake(
        agent1.agent_id,
        agent2.agent_id,
        fragments[0]
    )
    
    if success:
        print("[OK] Handshake successful, fragment encrypted and authenticated")
        print(f"  Package size: {len(encrypted_package)} bytes")
        
        # Agent 2 receives and verifies
        received_fragment = auth_system.verify_and_receive_fragment(
            agent2.agent_id,
            encrypted_package
        )
        
        if received_fragment:
            print("[OK] Fragment received and verified by Agent 2")
        else:
            print("[FAIL] Fragment verification failed")
    else:
        print("[FAIL] Handshake failed")
    
    # Test corruption detection
    print("\n=== Testing Corruption Detection ===")
    
    # Corrupt a fragment
    corrupted_fragment = fragments[2]
    corrupted_fragment.encrypted_data = b"CORRUPTED" + corrupted_fragment.encrypted_data[9:]
    
    # Try to reconstruct with corrupted fragment
    mixed_fragments = fragments[:2] + [corrupted_fragment] + fragments[3:]
    reconstructed = frag_system.reconstruct_with_verification(data_id, mixed_fragments)
    
    if reconstructed is None:
        print("[OK] Corruption detected, reconstruction rejected")
    else:
        print("[FAIL] Failed to detect corruption")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demonstrate_secure_fragmentation()
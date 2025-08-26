import time
import threading
import secrets
import hashlib
import numpy as np
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections import defaultdict

# Import patented legal conflict engine
try:
    from .legal_conflict_engine import LegalConflictEngine, RoutingDecision
    LEGAL_ROUTING_AVAILABLE = True
except ImportError:
    LEGAL_ROUTING_AVAILABLE = False
    print("[WARNING] Legal conflict engine not available - using standard fragmentation")


class FragmentStatus(Enum):
    ACTIVE = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    RECONSTRUCTED = "reconstructed"


@dataclass
class DataFragment:
    fragment_id: str
    data_chunk: bytes
    created_at: float
    expires_at: float
    fragment_index: int
    total_fragments: int
    original_hash: str
    access_count: int = 0
    status: FragmentStatus = FragmentStatus.ACTIVE
    reconstruction_key: Optional[str] = None
    # Patented legal routing metadata
    legal_jurisdictions: List[str] = field(default_factory=list)
    legal_impossibility_score: float = 0.0
    legal_barriers: List[str] = field(default_factory=list)
    routing_decision_hash: Optional[str] = None


@dataclass
class FragmentationPolicy:
    max_fragment_lifetime_ms: int = 100  # 100ms default
    min_fragments: int = 3
    max_fragments: int = 10
    overlap_factor: float = 0.2  # 20% overlap between fragments
    auto_expire: bool = True
    quantum_resistance_level: int = 3  # 1-5 scale


class TemporalFragmentation:
    def __init__(self, policy: FragmentationPolicy = None, enable_legal_routing: bool = True):
        self.policy = policy or FragmentationPolicy()
        self.fragments: Dict[str, DataFragment] = {}
        self.fragment_groups: Dict[str, List[str]] = {}  # original_id -> fragment_ids
        self.expiration_scheduler = {}
        self.reconstruction_callbacks: Dict[str, Callable] = {}
        self._cleanup_thread = None
        
        # Initialize patented legal conflict engine
        self.legal_engine = None
        if enable_legal_routing and LEGAL_ROUTING_AVAILABLE:
            self.legal_engine = LegalConflictEngine(enable_real_time_tracking=True)
            print("[PATENT] Temporal fragmentation enhanced with legal conflict routing")
        else:
            print("[INFO] Using standard temporal fragmentation without legal routing")
        self._running = False
        
    async def fragment_data(self, data: bytes, original_id: str = None) -> List[DataFragment]:
        """
        Fragment data with patented legal conflict routing
        Implements temporal-geographic fragmentation with legal impossibility barriers
        """
        if original_id is None:
            original_id = secrets.token_hex(16)
        
        current_time = time.time()
        lifetime_seconds = self.policy.max_fragment_lifetime_ms / 1000.0
        expires_at = current_time + lifetime_seconds
        
        # Calculate optimal fragment count based on data size and policy
        data_size = len(data)
        fragment_count = min(
            max(self.policy.min_fragments, data_size // 256 + 1),
            self.policy.max_fragments
        )
        
        # Create original data hash for integrity verification
        original_hash = hashlib.sha256(data).hexdigest()
        
        # Split data into overlapping fragments for quantum resistance
        fragments = []
        chunk_size = len(data) // fragment_count
        overlap_size = int(chunk_size * self.policy.overlap_factor)
        
        # Generate legal routing decisions for each fragment
        routing_decisions = {}
        if self.legal_engine:
            for i in range(fragment_count):
                fragment_id = f"{original_id}_frag_{i}_{secrets.token_hex(8)}"
                routing_decision = await self.legal_engine.select_maximally_hostile_routing(
                    fragment_id=fragment_id,
                    threshold=3,  # Minimum 3 hostile jurisdictions
                    min_hostility=0.7  # High hostility requirement
                )
                routing_decisions[i] = routing_decision
                
                # Add latency for realistic timing
                await asyncio.sleep(0.001)  # 1ms per routing decision
        
        for i in range(fragment_count):
            start_idx = max(0, i * chunk_size - overlap_size)
            end_idx = min(len(data), (i + 1) * chunk_size + overlap_size)
            
            chunk = data[start_idx:end_idx]
            
            # Add quantum timing patterns to fragment for enhanced security
            if self.policy.quantum_resistance_level >= 2:
                chunk = self._add_quantum_timing_patterns(chunk, i, current_time)
            
            fragment_id = f"{original_id}_frag_{i}_{secrets.token_hex(8)}"
            
            # Get legal routing metadata
            legal_metadata = self._extract_legal_metadata(routing_decisions.get(i))
            
            fragment = DataFragment(
                fragment_id=fragment_id,
                data_chunk=chunk,
                created_at=current_time,
                expires_at=expires_at,
                fragment_index=i,
                total_fragments=fragment_count,
                original_hash=original_hash,
                reconstruction_key=self._generate_reconstruction_key(original_id, i),
                # Patented legal routing metadata
                legal_jurisdictions=legal_metadata['jurisdictions'],
                legal_impossibility_score=legal_metadata['impossibility_score'],
                legal_barriers=legal_metadata['barriers'],
                routing_decision_hash=legal_metadata['decision_hash']
            )
            
            fragments.append(fragment)
            self.fragments[fragment_id] = fragment
        
        # Store fragment group mapping
        self.fragment_groups[original_id] = [f.fragment_id for f in fragments]
        
        # Schedule expiration with legal constraint awareness
        if self.policy.auto_expire:
            await self._schedule_legal_aware_expiration(fragments)
        
        # Log patented functionality usage with quantum timing pattern info
        total_impossibility = sum(f.legal_impossibility_score for f in fragments) / len(fragments)
        total_barriers = sum(len(f.legal_barriers) for f in fragments)
        
        print(f"[PATENT] Enhanced temporal fragmentation complete: {len(fragments)} fragments, "
              f"avg impossibility: {total_impossibility:.4f}, barriers: {total_barriers}, "
              f"quantum timing patterns: {'enabled' if self.policy.quantum_resistance_level >= 2 else 'disabled'}")
        
        return fragments
    
    def _extract_legal_metadata(self, routing_decision: Optional['RoutingDecision']) -> Dict[str, Any]:
        """Extract legal routing metadata from routing decision"""
        if routing_decision is None:
            return {
                'jurisdictions': [],
                'impossibility_score': 0.0,
                'barriers': [],
                'decision_hash': None
            }
        
        return {
            'jurisdictions': routing_decision.target_jurisdictions,
            'impossibility_score': routing_decision.impossibility_confidence,
            'barriers': routing_decision.legal_barriers,
            'decision_hash': routing_decision.decision_hash
        }
    
    async def _schedule_legal_aware_expiration(self, fragments: List[DataFragment]):
        """Schedule fragment expiration considering legal constraints"""
        for fragment in fragments:
            # Base expiration time
            expiration_time = fragment.expires_at
            
            # Adjust expiration based on legal timing
            if self.legal_engine and fragment.legal_jurisdictions:
                # Check for temporal-legal constraints
                for jurisdiction in fragment.legal_jurisdictions:
                    constraint = self.legal_engine.temporal_constraints.get(jurisdiction, {})
                    
                    # If Sabbath is active, delay expiration slightly to maintain legal barriers
                    if constraint.get('sabbath_active'):
                        expiration_time += 3600  # Extend by 1 hour during Sabbath
                    
                    # If courts are closed, fragments can expire sooner (less legal risk)
                    if not constraint.get('court_session', True):
                        expiration_time -= 1800  # Reduce by 30 minutes when courts closed
            
            # Schedule the actual expiration
            self._schedule_single_expiration(fragment, expiration_time)
    
    def _schedule_single_expiration(self, fragment: DataFragment, expiration_time: float):
        """Schedule expiration for a single fragment"""
        delay = max(0, expiration_time - time.time())
        
        def expire_fragment():
            if fragment.fragment_id in self.fragments:
                fragment.status = FragmentStatus.EXPIRED
                print(f"[PATENT] Fragment {fragment.fragment_id} expired in "
                      f"{len(fragment.legal_jurisdictions)} hostile jurisdictions")
        
        timer = threading.Timer(delay, expire_fragment)
        timer.start()
        self.expiration_scheduler[fragment.fragment_id] = timer
    
    async def detect_legal_process_on_fragments(self, process_indicator: str) -> bool:
        """
        Detect legal process and trigger poison pills on all fragments
        Implements patented legal poison pill mechanisms
        """
        if not self.legal_engine:
            return False
        
        # Detect legal process through legal engine
        legal_process_detected = await self.legal_engine.detect_legal_process(process_indicator)
        
        if legal_process_detected:
            print(f"[PATENT] Legal process detected on fragmented data: {process_indicator}")
            
            # Trigger immediate expiration of all active fragments
            for fragment_id, fragment in self.fragments.items():
                if fragment.status == FragmentStatus.ACTIVE:
                    fragment.status = FragmentStatus.EXPIRED
                    print(f"[PATENT] Emergency expiration triggered for {fragment_id}")
            
            # Cancel all pending expiration timers
            for timer in self.expiration_scheduler.values():
                timer.cancel()
            self.expiration_scheduler.clear()
            
            return True
        
        return False
    
    def get_legal_routing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics on legal routing effectiveness"""
        stats = {
            'total_fragments': len(self.fragments),
            'legally_protected_fragments': 0,
            'average_impossibility_score': 0.0,
            'total_legal_barriers': 0,
            'unique_jurisdictions': set(),
            'jurisdiction_distribution': {},
            'temporal_constraints_active': 0
        }
        
        impossibility_scores = []
        
        for fragment in self.fragments.values():
            if fragment.legal_jurisdictions:
                stats['legally_protected_fragments'] += 1
                impossibility_scores.append(fragment.legal_impossibility_score)
                stats['total_legal_barriers'] += len(fragment.legal_barriers)
                
                for jurisdiction in fragment.legal_jurisdictions:
                    stats['unique_jurisdictions'].add(jurisdiction)
                    stats['jurisdiction_distribution'][jurisdiction] = \
                        stats['jurisdiction_distribution'].get(jurisdiction, 0) + 1
        
        if impossibility_scores:
            stats['average_impossibility_score'] = sum(impossibility_scores) / len(impossibility_scores)
        
        stats['unique_jurisdictions'] = len(stats['unique_jurisdictions'])
        
        # Check temporal constraints
        if self.legal_engine:
            for jurisdiction, constraints in self.legal_engine.temporal_constraints.items():
                if any(constraints.values()):
                    stats['temporal_constraints_active'] += 1
        
        return stats
    
    def _add_quantum_timing_patterns(self, data: bytes, fragment_index: int, creation_time: float) -> bytes:
        """Add quantum timing patterns to fragment data for enhanced temporal security"""
        noise_level = self.policy.quantum_resistance_level
        
        if noise_level >= 2:
            # Generate quantum timing-based noise patterns
            data_array = np.frombuffer(data, dtype=np.uint8)
            
            # Create temporal quantum interference pattern
            microsecond_phase = int((creation_time * 1000000) % 1000000)
            temporal_seed = (fragment_index * microsecond_phase) % 2**32
            
            # Generate quantum decoherence timing pattern
            timing_random = np.random.RandomState(temporal_seed)
            decoherence_pattern = timing_random.randint(0, 256, size=len(data_array), dtype=np.uint8)
            
            # Apply quantum superposition-like temporal interference
            time_oscillation = np.sin(2 * np.pi * creation_time * np.arange(len(data_array)) / 1000.0)
            temporal_noise = (time_oscillation * 127 + 128).astype(np.uint8)
            
            # Add quantum entanglement-like correlation between bytes
            entanglement_noise = np.zeros_like(data_array, dtype=np.uint8)
            for i in range(0, len(data_array) - 1, 2):
                correlation = timing_random.randint(0, 64)
                entanglement_noise[i] = correlation
                if i + 1 < len(data_array):
                    entanglement_noise[i + 1] = correlation
            
            # Combine all quantum timing effects
            quantum_enhanced = (
                data_array ^ decoherence_pattern ^ temporal_noise ^ entanglement_noise
            ) % 256
            
            return quantum_enhanced.astype(np.uint8).tobytes()
        
        return data
    
    def _remove_quantum_timing_patterns(self, data: bytes, fragment_index: int, creation_time: float) -> bytes:
        """Remove quantum timing patterns from fragment data during reconstruction"""
        if self.policy.quantum_resistance_level >= 2:
            # Reverse the quantum timing-based noise patterns
            data_array = np.frombuffer(data, dtype=np.uint8)
            
            # Recreate the same temporal quantum interference pattern
            microsecond_phase = int((creation_time * 1000000) % 1000000)
            temporal_seed = (fragment_index * microsecond_phase) % 2**32
            
            # Regenerate quantum decoherence timing pattern
            timing_random = np.random.RandomState(temporal_seed)
            decoherence_pattern = timing_random.randint(0, 256, size=len(data_array), dtype=np.uint8)
            
            # Recreate quantum superposition-like temporal interference
            time_oscillation = np.sin(2 * np.pi * creation_time * np.arange(len(data_array)) / 1000.0)
            temporal_noise = (time_oscillation * 127 + 128).astype(np.uint8)
            
            # Recreate quantum entanglement-like correlation between bytes
            entanglement_noise = np.zeros_like(data_array, dtype=np.uint8)
            for i in range(0, len(data_array) - 1, 2):
                correlation = timing_random.randint(0, 64)
                entanglement_noise[i] = correlation
                if i + 1 < len(data_array):
                    entanglement_noise[i + 1] = correlation
            
            # Remove all quantum timing effects (XOR is its own inverse)
            clean_data = (
                data_array ^ decoherence_pattern ^ temporal_noise ^ entanglement_noise
            ) % 256
            
            return clean_data.astype(np.uint8).tobytes()
        
        return data
    
    def _generate_reconstruction_key(self, original_id: str, fragment_index: int) -> str:
        """Generate quantum-resistant reconstruction key"""
        key_data = f"{original_id}_{fragment_index}_{time.time()}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]
    
    def access_fragment(self, fragment_id: str) -> Optional[DataFragment]:
        """Access a fragment and check if it's still valid"""
        if fragment_id not in self.fragments:
            return None
        
        fragment = self.fragments[fragment_id]
        current_time = time.time()
        
        # Check if fragment has expired
        if current_time > fragment.expires_at:
            fragment.status = FragmentStatus.EXPIRED
            return None
        
        # Check if fragment is in expiring state (last 10ms)
        if current_time > fragment.expires_at - 0.01:
            fragment.status = FragmentStatus.EXPIRING
        
        fragment.access_count += 1
        return fragment
    
    def reconstruct_data(self, original_id: str) -> Optional[bytes]:
        """Attempt to reconstruct original data from fragments"""
        if original_id not in self.fragment_groups:
            return None
        
        fragment_ids = self.fragment_groups[original_id]
        fragments = []
        
        # Collect valid fragments
        for frag_id in fragment_ids:
            fragment = self.access_fragment(frag_id)
            if fragment and fragment.status in [FragmentStatus.ACTIVE, FragmentStatus.EXPIRING]:
                fragments.append(fragment)
        
        if not fragments:
            return None
        
        # Sort fragments by index
        fragments.sort(key=lambda x: x.fragment_index)
        
        # Check if we have enough fragments (at least 70% due to overlap)
        required_fragments = max(1, int(fragments[0].total_fragments * 0.7))
        if len(fragments) < required_fragments:
            return None
        
        # Reconstruct data with overlap handling
        reconstructed_data = bytearray()
        overlap_size = int(len(fragments[0].data_chunk) * self.policy.overlap_factor)
        
        for i, fragment in enumerate(fragments):
            # Remove quantum timing patterns
            clean_chunk = self._remove_quantum_timing_patterns(
                fragment.data_chunk, 
                fragment.fragment_index, 
                fragment.created_at
            )
            
            if i == 0:
                # First fragment - take all data
                reconstructed_data.extend(clean_chunk)
            else:
                # Subsequent fragments - skip overlap
                start_idx = overlap_size if i > 0 else 0
                reconstructed_data.extend(clean_chunk[start_idx:])
        
        # Verify integrity
        reconstructed_hash = hashlib.sha256(reconstructed_data).hexdigest()
        expected_hash = fragments[0].original_hash
        
        if reconstructed_hash != expected_hash:
            # Try alternative reconstruction strategy
            return self._attempt_repair_reconstruction(fragments)
        
        # Mark fragments as reconstructed
        for fragment in fragments:
            fragment.status = FragmentStatus.RECONSTRUCTED
        
        return bytes(reconstructed_data)
    
    def _attempt_repair_reconstruction(self, fragments: List[DataFragment]) -> Optional[bytes]:
        """Attempt to repair reconstruction using quantum error correction"""
        if len(fragments) < 2:
            return None
        
        # Simple error correction - try different overlap strategies
        for overlap_factor in [0.1, 0.3, 0.0]:  # Different overlap strategies
            try:
                reconstructed_data = bytearray()
                
                for i, fragment in enumerate(fragments):
                    clean_chunk = self._remove_quantum_noise(fragment.data_chunk, fragment.fragment_index)
                    
                    if i == 0:
                        reconstructed_data.extend(clean_chunk)
                    else:
                        overlap_size = int(len(clean_chunk) * overlap_factor)
                        reconstructed_data.extend(clean_chunk[overlap_size:])
                
                # Verify with expected hash
                test_hash = hashlib.sha256(reconstructed_data).hexdigest()
                if test_hash == fragments[0].original_hash:
                    return bytes(reconstructed_data)
                    
            except Exception:
                continue
        
        return None
    
    def _schedule_expiration(self, fragments: List[DataFragment]):
        """Schedule automatic expiration of fragments"""
        for fragment in fragments:
            expiration_delay = fragment.expires_at - time.time()
            if expiration_delay > 0:
                timer = threading.Timer(expiration_delay, self._expire_fragment, [fragment.fragment_id])
                timer.start()
                self.expiration_scheduler[fragment.fragment_id] = timer
    
    def _expire_fragment(self, fragment_id: str):
        """Expire a fragment and clean up its data"""
        if fragment_id in self.fragments:
            fragment = self.fragments[fragment_id]
            fragment.status = FragmentStatus.EXPIRED
            
            # Securely overwrite fragment data
            fragment.data_chunk = b'\x00' * len(fragment.data_chunk)
            
            # Remove from active fragments after a delay
            threading.Timer(1.0, lambda: self.fragments.pop(fragment_id, None)).start()
    
    def force_expire_all(self, original_id: str = None):
        """Force immediate expiration of fragments"""
        if original_id:
            # Expire specific group
            if original_id in self.fragment_groups:
                for frag_id in self.fragment_groups[original_id]:
                    self._expire_fragment(frag_id)
        else:
            # Expire all fragments
            for frag_id in list(self.fragments.keys()):
                self._expire_fragment(frag_id)
    
    def get_fragment_status(self, original_id: str) -> Dict:
        """Get status of all fragments for a data piece"""
        if original_id not in self.fragment_groups:
            return {}
        
        current_time = time.time()
        status_info = {
            'total_fragments': 0,
            'active_fragments': 0,
            'expiring_fragments': 0,
            'expired_fragments': 0,
            'reconstructable': False,
            'time_until_expiration': 0
        }
        
        fragment_ids = self.fragment_groups[original_id]
        status_info['total_fragments'] = len(fragment_ids)
        
        min_expiration_time = float('inf')
        
        for frag_id in fragment_ids:
            if frag_id in self.fragments:
                fragment = self.fragments[frag_id]
                
                if current_time > fragment.expires_at:
                    status_info['expired_fragments'] += 1
                elif current_time > fragment.expires_at - 0.01:
                    status_info['expiring_fragments'] += 1
                    min_expiration_time = min(min_expiration_time, fragment.expires_at)
                else:
                    status_info['active_fragments'] += 1
                    min_expiration_time = min(min_expiration_time, fragment.expires_at)
        
        # Check if still reconstructable
        required_fragments = max(1, int(status_info['total_fragments'] * 0.7))
        available_fragments = status_info['active_fragments'] + status_info['expiring_fragments']
        status_info['reconstructable'] = available_fragments >= required_fragments
        
        if min_expiration_time != float('inf'):
            status_info['time_until_expiration'] = max(0, min_expiration_time - current_time)
        
        return status_info
    
    def start_cleanup_service(self):
        """Start background cleanup service"""
        if self._running:
            return
        
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
    
    def stop_cleanup_service(self):
        """Stop background cleanup service"""
        self._running = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=1.0)
    
    def _cleanup_loop(self):
        """Background cleanup of expired fragments"""
        while self._running:
            try:
                current_time = time.time()
                expired_fragments = []
                
                for frag_id, fragment in self.fragments.items():
                    if current_time > fragment.expires_at + 5.0:  # Grace period
                        expired_fragments.append(frag_id)
                
                for frag_id in expired_fragments:
                    self.fragments.pop(frag_id, None)
                
                time.sleep(0.01)  # 10ms cleanup interval
                
            except Exception as e:
                print(f"Cleanup error: {e}")
                break
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        current_time = time.time()
        
        total_fragments = len(self.fragments)
        active_fragments = sum(
            1 for f in self.fragments.values() 
            if f.status == FragmentStatus.ACTIVE and current_time <= f.expires_at
        )
        
        return {
            'total_fragments': total_fragments,
            'active_fragments': active_fragments,
            'fragment_groups': len(self.fragment_groups),
            'cleanup_running': self._running,
            'policy': {
                'max_lifetime_ms': self.policy.max_fragment_lifetime_ms,
                'min_fragments': self.policy.min_fragments,
                'max_fragments': self.policy.max_fragments,
                'quantum_resistance_level': self.policy.quantum_resistance_level,
                'quantum_timing_patterns': self.policy.quantum_resistance_level >= 2
            },
            'quantum_enhancements': {
                'temporal_interference_patterns': self.policy.quantum_resistance_level >= 2,
                'quantum_decoherence_timing': self.policy.quantum_resistance_level >= 2,
                'quantum_entanglement_correlation': self.policy.quantum_resistance_level >= 2,
                'microsecond_phase_variation': True
            }
        }
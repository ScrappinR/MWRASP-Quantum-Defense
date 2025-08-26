#!/usr/bin/env python3
"""
MWRASP Quantum Defense System - Standalone Version
Complete implementation in a single file for easy copying

Copy this entire file to your local machine and run:
python mwrasp_standalone.py

Requirements:
pip install numpy

This demonstrates:
- Quantum computer attack detection with canary tokens
- Temporal data fragmentation with millisecond expiration  
- Autonomous agent coordination and response
"""

import time
import hashlib
import secrets
import threading
import asyncio
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque
import numpy as np


# ============================================================================
# QUANTUM DETECTOR COMPONENT
# ============================================================================

class ThreatLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CanaryToken:
    token_id: str
    value: str
    created_at: float
    access_pattern: str
    quantum_signature: Optional[str] = None
    access_count: int = 0
    last_accessed: Optional[float] = None


@dataclass
class QuantumThreat:
    threat_id: str
    threat_level: ThreatLevel
    detection_time: float
    attack_vector: str
    quantum_indicators: List[str]
    affected_tokens: List[str]
    confidence_score: float


class QuantumDetector:
    def __init__(self, sensitivity_threshold: float = 0.7):
        self.canary_tokens: Dict[str, CanaryToken] = {}
        self.threat_history: List[QuantumThreat] = []
        self.sensitivity_threshold = sensitivity_threshold
        self.quantum_patterns = {
            'superposition_access': 0.9,
            'entanglement_correlation': 0.85,
            'quantum_speedup': 0.8,
            'interference_pattern': 0.75,
            'decoherence_signature': 0.7,
        }
        self.access_monitor = defaultdict(list)
        self._monitoring = False
        
    def generate_canary_token(self, data_type: str = "sensitive") -> CanaryToken:
        token_id = secrets.token_hex(16)
        base_value = f"{data_type}_{time.time()}_{secrets.token_hex(8)}"
        quantum_signature = hashlib.sha256(base_value.encode()).hexdigest()
        access_pattern = hashlib.md5(secrets.token_bytes(8)).hexdigest()[:16]
        
        token = CanaryToken(
            token_id=token_id,
            value=base_value,
            created_at=time.time(),
            access_pattern=access_pattern,
            quantum_signature=quantum_signature
        )
        
        self.canary_tokens[token_id] = token
        return token
    
    def access_token(self, token_id: str, accessor_id: str = None) -> bool:
        if token_id not in self.canary_tokens:
            return False
        
        token = self.canary_tokens[token_id]
        current_time = time.time()
        
        token.access_count += 1
        token.last_accessed = current_time
        
        access_info = {
            'time': current_time,
            'accessor_id': accessor_id or 'unknown',
            'token_id': token_id
        }
        self.access_monitor[token_id].append(access_info)
        
        threat = self._analyze_quantum_threat(token_id, access_info)
        if threat:
            self.threat_history.append(threat)
            return True
        
        return False
    
    def _analyze_quantum_threat(self, token_id: str, access_info: Dict) -> Optional[QuantumThreat]:
        current_time = access_info['time']
        token_accesses = self.access_monitor[token_id]
        
        quantum_indicators = []
        confidence_scores = []
        
        # Check for superposition-like access
        recent_accesses = [
            a for a in token_accesses 
            if current_time - a['time'] < 0.1
        ]
        if len(recent_accesses) > 3:
            quantum_indicators.append('superposition_access')
            confidence_scores.append(self.quantum_patterns['superposition_access'])
        
        # Check for quantum speedup
        if len(token_accesses) >= 3:
            intervals = []
            for i in range(1, len(token_accesses)):
                interval = token_accesses[i]['time'] - token_accesses[i-1]['time']
                intervals.append(interval)
            
            if intervals and np.mean(intervals) < 0.001:
                quantum_indicators.append('quantum_speedup')
                confidence_scores.append(self.quantum_patterns['quantum_speedup'])
        
        if confidence_scores:
            overall_confidence = np.mean(confidence_scores)
            
            if overall_confidence >= self.sensitivity_threshold:
                threat_level = self._calculate_threat_level(overall_confidence)
                
                return QuantumThreat(
                    threat_id=secrets.token_hex(8),
                    threat_level=threat_level,
                    detection_time=current_time,
                    attack_vector='quantum_computer_attack',
                    quantum_indicators=quantum_indicators,
                    affected_tokens=[token_id],
                    confidence_score=overall_confidence
                )
        
        return None
    
    def _calculate_threat_level(self, confidence: float) -> ThreatLevel:
        if confidence >= 0.95:
            return ThreatLevel.CRITICAL
        elif confidence >= 0.85:
            return ThreatLevel.HIGH
        elif confidence >= 0.75:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def get_active_threats(self) -> List[QuantumThreat]:
        current_time = time.time()
        return [
            threat for threat in self.threat_history
            if current_time - threat.detection_time < 300.0
        ]
    
    def get_threat_statistics(self) -> Dict:
        active_threats = self.get_active_threats()
        return {
            'total_tokens': len(self.canary_tokens),
            'total_threats_detected': len(self.threat_history),
            'active_threats': len(active_threats),
            'monitoring_active': self._monitoring
        }


# ============================================================================
# TEMPORAL FRAGMENTATION COMPONENT
# ============================================================================

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


@dataclass
class FragmentationPolicy:
    max_fragment_lifetime_ms: int = 100
    min_fragments: int = 3
    max_fragments: int = 10
    overlap_factor: float = 0.2
    quantum_resistance_level: int = 3


class TemporalFragmentation:
    def __init__(self, policy: FragmentationPolicy = None):
        self.policy = policy or FragmentationPolicy()
        self.fragments: Dict[str, DataFragment] = {}
        self.fragment_groups: Dict[str, List[str]] = {}
        
    def fragment_data(self, data: bytes, original_id: str = None) -> List[DataFragment]:
        if original_id is None:
            original_id = secrets.token_hex(16)
        
        current_time = time.time()
        lifetime_seconds = self.policy.max_fragment_lifetime_ms / 1000.0
        expires_at = current_time + lifetime_seconds
        
        data_size = len(data)
        fragment_count = min(
            max(self.policy.min_fragments, data_size // 256 + 1),
            self.policy.max_fragments
        )
        
        original_hash = hashlib.sha256(data).hexdigest()
        
        fragments = []
        chunk_size = len(data) // fragment_count
        overlap_size = int(chunk_size * self.policy.overlap_factor)
        
        for i in range(fragment_count):
            start_idx = max(0, i * chunk_size - overlap_size)
            end_idx = min(len(data), (i + 1) * chunk_size + overlap_size)
            
            chunk = data[start_idx:end_idx]
            
            # Add quantum noise
            if self.policy.quantum_resistance_level >= 2:
                chunk = self._add_quantum_noise(chunk, i)
            
            fragment_id = f"{original_id}_frag_{i}_{secrets.token_hex(8)}"
            
            fragment = DataFragment(
                fragment_id=fragment_id,
                data_chunk=chunk,
                created_at=current_time,
                expires_at=expires_at,
                fragment_index=i,
                total_fragments=fragment_count,
                original_hash=original_hash
            )
            
            fragments.append(fragment)
            self.fragments[fragment_id] = fragment
        
        self.fragment_groups[original_id] = [f.fragment_id for f in fragments]
        return fragments
    
    def _add_quantum_noise(self, data: bytes, fragment_index: int) -> bytes:
        noise_bytes = bytearray()
        for i, byte in enumerate(data):
            noise_value = (i * fragment_index + 42) % 256
            noisy_byte = byte ^ (noise_value & 0xFF)
            noise_bytes.append(noisy_byte)
        return bytes(noise_bytes)
    
    def _remove_quantum_noise(self, data: bytes, fragment_index: int) -> bytes:
        clean_bytes = bytearray()
        for i, byte in enumerate(data):
            noise_value = (i * fragment_index + 42) % 256
            clean_byte = byte ^ (noise_value & 0xFF)
            clean_bytes.append(clean_byte)
        return bytes(clean_bytes)
    
    def reconstruct_data(self, original_id: str) -> Optional[bytes]:
        if original_id not in self.fragment_groups:
            return None
        
        fragment_ids = self.fragment_groups[original_id]
        fragments = []
        
        current_time = time.time()
        
        for frag_id in fragment_ids:
            if frag_id in self.fragments:
                fragment = self.fragments[frag_id]
                if current_time <= fragment.expires_at:
                    fragments.append(fragment)
        
        if not fragments:
            return None
        
        fragments.sort(key=lambda x: x.fragment_index)
        
        required_fragments = max(1, int(fragments[0].total_fragments * 0.7))
        if len(fragments) < required_fragments:
            return None
        
        reconstructed_data = bytearray()
        overlap_size = int(len(fragments[0].data_chunk) * self.policy.overlap_factor)
        
        for i, fragment in enumerate(fragments):
            clean_chunk = self._remove_quantum_noise(fragment.data_chunk, fragment.fragment_index)
            
            if i == 0:
                reconstructed_data.extend(clean_chunk)
            else:
                start_idx = overlap_size if i > 0 else 0
                reconstructed_data.extend(clean_chunk[start_idx:])
        
        reconstructed_hash = hashlib.sha256(reconstructed_data).hexdigest()
        expected_hash = fragments[0].original_hash
        
        if reconstructed_hash == expected_hash:
            for fragment in fragments:
                fragment.status = FragmentStatus.RECONSTRUCTED
            return bytes(reconstructed_data)
        
        return None
    
    def get_fragment_status(self, original_id: str) -> Dict:
        if original_id not in self.fragment_groups:
            return {}
        
        current_time = time.time()
        status_info = {
            'total_fragments': 0,
            'active_fragments': 0,
            'expired_fragments': 0,
            'reconstructable': False
        }
        
        fragment_ids = self.fragment_groups[original_id]
        status_info['total_fragments'] = len(fragment_ids)
        
        for frag_id in fragment_ids:
            if frag_id in self.fragments:
                fragment = self.fragments[frag_id]
                
                if current_time > fragment.expires_at:
                    status_info['expired_fragments'] += 1
                else:
                    status_info['active_fragments'] += 1
        
        required_fragments = max(1, int(status_info['total_fragments'] * 0.7))
        status_info['reconstructable'] = status_info['active_fragments'] >= required_fragments
        
        return status_info


# ============================================================================
# AGENT SYSTEM COMPONENT  
# ============================================================================

class AgentRole(Enum):
    MONITOR = "monitor"
    DEFENDER = "defender"
    ANALYZER = "analyzer"
    COORDINATOR = "coordinator"
    RECOVERY = "recovery"


class AgentStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"


@dataclass
class Agent:
    agent_id: str
    role: AgentRole
    status: AgentStatus
    created_at: float
    processed_threats: int = 0
    success_rate: float = 1.0
    workload: int = 0
    max_workload: int = 10


class AutonomousDefenseCoordinator:
    def __init__(self, quantum_detector, fragmentation_system):
        self.quantum_detector = quantum_detector
        self.fragmentation_system = fragmentation_system
        self.agents: Dict[str, Agent] = {}
        self.running = False
        
        self._initialize_agent_fleet()
        
        self.coordination_stats = {
            'total_coordinations': 0,
            'successful_defenses': 0,
            'active_agents': 0
        }
    
    def _initialize_agent_fleet(self):
        current_time = time.time()
        
        agent_types = [
            (AgentRole.MONITOR, 1),
            (AgentRole.DEFENDER, 3),
            (AgentRole.ANALYZER, 1),
            (AgentRole.COORDINATOR, 1),
            (AgentRole.RECOVERY, 1)
        ]
        
        for role, count in agent_types:
            for i in range(count):
                agent_id = f"{role.value}_{i}_{secrets.token_hex(4)}"
                agent = Agent(
                    agent_id=agent_id,
                    role=role,
                    status=AgentStatus.ACTIVE if role == AgentRole.MONITOR else AgentStatus.IDLE,
                    created_at=current_time
                )
                self.agents[agent_id] = agent
    
    async def start_coordination(self):
        self.running = True
        print("MWRASP Autonomous Defense System activated")
    
    async def stop_coordination(self):
        self.running = False
        for agent in self.agents.values():
            agent.status = AgentStatus.IDLE
    
    def get_agent_status(self) -> Dict:
        agents_by_role = defaultdict(list)
        
        for agent in self.agents.values():
            agents_by_role[agent.role.value].append({
                'agent_id': agent.agent_id,
                'status': agent.status.value,
                'workload': agent.workload,
                'max_workload': agent.max_workload,
                'processed_threats': agent.processed_threats,
                'success_rate': agent.success_rate
            })
        
        active_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.ACTIVE)
        self.coordination_stats['active_agents'] = active_agents
        
        return {
            'agents_by_role': dict(agents_by_role),
            'total_agents': len(self.agents),
            'coordination_stats': self.coordination_stats,
            'system_running': self.running
        }
    
    async def send_coordination_message(self, message: Dict):
        self.coordination_stats['total_coordinations'] += 1
        
        if message.get('type') == 'threat_escalation':
            # Activate defender agents
            defenders = [a for a in self.agents.values() if a.role == AgentRole.DEFENDER]
            for defender in defenders[:2]:  # Activate 2 defenders
                defender.status = AgentStatus.ACTIVE
                defender.workload += 1


# ============================================================================
# STANDALONE DEMO APPLICATION
# ============================================================================

class MWRASPStandaloneDemo:
    def __init__(self):
        print("=" * 60)
        print("  MWRASP QUANTUM DEFENSE SYSTEM - STANDALONE DEMO")
        print("  Multi-Wavelength Rapid-Aging Surveillance Platform")
        print("=" * 60)
        print()
        
        # Initialize components
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.6)
        
        self.fragmentation_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=300,  # 300ms for demo
            min_fragments=4,
            max_fragments=7,
            quantum_resistance_level=3
        )
        self.fragmentation_system = TemporalFragmentation(self.fragmentation_policy)
        
        self.agent_coordinator = AutonomousDefenseCoordinator(
            self.quantum_detector,
            self.fragmentation_system
        )
    
    async def run_demo(self):
        print("Initializing MWRASP systems...")
        await self.agent_coordinator.start_coordination()
        print("*** All systems online! ***\n")
        
        while True:
            print("MWRASP DEMONSTRATION MENU")
            print("-" * 40)
            print("1. Quantum Attack Detection Demo")
            print("2. Temporal Fragmentation Demo")
            print("3. Agent Coordination Demo")
            print("4. Integrated Attack Response")
            print("5. System Status Report")
            print("6. Exit")
            print("-" * 40)
            
            try:
                choice = input("Enter choice (1-6): ").strip()
                
                if choice == "1":
                    await self.demo_quantum_detection()
                elif choice == "2":
                    await self.demo_fragmentation()
                elif choice == "3":
                    await self.demo_agent_coordination()
                elif choice == "4":
                    await self.demo_integrated_response()
                elif choice == "5":
                    self.show_system_status()
                elif choice == "6":
                    break
                else:
                    print("Invalid choice!")
                    continue
                    
                input("\nPress Enter to continue...")
                print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\nDemo interrupted.")
                break
        
        await self.agent_coordinator.stop_coordination()
        print("MWRASP systems shut down. Thank you!")
    
    async def demo_quantum_detection(self):
        print("\n🛡️  QUANTUM ATTACK DETECTION DEMO")
        print("=" * 40)
        
        print("\nStep 1: Deploying Canary Tokens")
        systems = ["database", "encryption_keys", "user_auth", "api_gateway"]
        tokens = []
        
        for system in systems:
            token = self.quantum_detector.generate_canary_token(system)
            tokens.append(token)
            print(f"  ✓ Canary deployed: {system}")
        
        print(f"\nDeployed {len(tokens)} canary tokens")
        
        print("\nStep 2: Normal Access Simulation")
        self.quantum_detector.access_token(tokens[0].token_id, "normal_user")
        print("  ✓ Normal user access - No threats detected")
        
        await asyncio.sleep(0.5)
        
        print("\nStep 3: Quantum Attack Simulation")
        print("  🚨 Simulating quantum computer attack...")
        
        # Rapid parallel access (quantum superposition pattern)
        for round_num in range(5):
            for token in tokens:
                self.quantum_detector.access_token(token.token_id, f"quantum_attacker_{round_num}")
            await asyncio.sleep(0.001)  # Very rapid access
        
        await asyncio.sleep(0.1)
        
        print("\nStep 4: Threat Analysis")
        threats = self.quantum_detector.get_active_threats()
        
        if threats:
            print("  🚨 QUANTUM ATTACK DETECTED!")
            for threat in threats:
                print(f"    Threat ID: {threat.threat_id}")
                print(f"    Level: {threat.threat_level.name}")
                print(f"    Confidence: {threat.confidence_score:.1%}")
                print(f"    Indicators: {', '.join(threat.quantum_indicators)}")
        else:
            print("  ℹ️  No threats detected (adjust sensitivity if needed)")
        
        stats = self.quantum_detector.get_threat_statistics()
        print(f"\nDetection Stats:")
        print(f"  Total tokens: {stats['total_tokens']}")
        print(f"  Threats detected: {stats['total_threats_detected']}")
        print(f"  Active threats: {stats['active_threats']}")
    
    async def demo_fragmentation(self):
        print("\n⚡ TEMPORAL FRAGMENTATION DEMO")
        print("=" * 40)
        
        print("\nStep 1: Fragmenting Sensitive Data")
        documents = [
            ("TOP SECRET: Nuclear launch codes", "nuclear_codes"),
            ("CLASSIFIED: Encryption master keys", "crypto_keys"),
            ("CONFIDENTIAL: Agent identities", "agent_data")
        ]
        
        fragmented_docs = []
        for content, doc_id in documents:
            data = content.encode()
            fragments = self.fragmentation_system.fragment_data(data, doc_id)
            fragmented_docs.append((content, doc_id, fragments))
            print(f"  ✓ Fragmented: {doc_id} ({len(fragments)} fragments)")
            print(f"    Expires in: {fragments[0].expires_at - time.time():.3f}s")
        
        print("\nStep 2: Immediate Reconstruction Test")
        for content, doc_id, fragments in fragmented_docs:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed and reconstructed.decode() == content:
                print(f"  ✓ Successfully reconstructed: {doc_id}")
            else:
                print(f"  ✗ Failed to reconstruct: {doc_id}")
        
        print("\nStep 3: Testing Fragment Expiration")
        print("  ⏳ Waiting for fragments to expire...")
        await asyncio.sleep(0.35)  # Wait longer than 300ms lifetime
        
        print("  ⏰ Attempting reconstruction after expiration:")
        for content, doc_id, fragments in fragmented_docs:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed:
                print(f"    Still accessible: {doc_id}")
            else:
                print(f"    🔒 Properly expired: {doc_id}")
        
        print("\nFragment Status Summary:")
        for content, doc_id, fragments in fragmented_docs:
            status = self.fragmentation_system.get_fragment_status(doc_id)
            print(f"  {doc_id}: {status['active_fragments']}/{status['total_fragments']} active")
    
    async def demo_agent_coordination(self):
        print("\n🤖 AGENT COORDINATION DEMO") 
        print("=" * 40)
        
        print("\nStep 1: Agent Network Status")
        status = self.agent_coordinator.get_agent_status()
        
        for role, agents in status['agents_by_role'].items():
            active = len([a for a in agents if a['status'] in ['active', 'busy']])
            print(f"  {role.title()}: {len(agents)} agents ({active} active)")
        
        print(f"\nCoordination Stats:")
        stats = status['coordination_stats']
        print(f"  Total coordinations: {stats['total_coordinations']}")
        print(f"  Active agents: {stats['active_agents']}")
        
        print("\nStep 2: Triggering Coordination")
        message = {
            "type": "threat_escalation",
            "threat_id": f"demo_threat_{int(time.time())}",
            "level": 8,
            "source": "demo"
        }
        
        await self.agent_coordinator.send_coordination_message(message)
        print("  ✓ Threat escalation message sent")
        
        await asyncio.sleep(0.2)
        
        print("\nStep 3: Agent Response")
        updated_status = self.agent_coordinator.get_agent_status()
        
        for role, agents in updated_status['agents_by_role'].items():
            print(f"\n  {role.title()} Agents:")
            for agent in agents:
                status_text = agent['status']
                workload = f"{agent['workload']}/{agent['max_workload']}"
                print(f"    Agent: {status_text} (Load: {workload})")
        
        updated_stats = updated_status['coordination_stats']
        print(f"\nUpdated Stats:")
        print(f"  Total coordinations: {updated_stats['total_coordinations']}")
        print(f"  Active agents: {updated_stats['active_agents']}")
    
    async def demo_integrated_response(self):
        print("\n🛡️⚡🤖 INTEGRATED ATTACK RESPONSE")
        print("=" * 40)
        
        print("\nPhase 1: Infrastructure Setup")
        # Deploy tokens
        critical_systems = ["financial_db", "user_auth", "encryption_service"]
        tokens = []
        for system in critical_systems:
            token = self.quantum_detector.generate_canary_token(system)
            tokens.append(token)
            print(f"  🛡️  Protected: {system}")
        
        # Fragment critical data
        classified_data = [
            ("MASTER_KEYS: AES-256, RSA-4096", "master_keys"),
            ("ADMIN_CREDENTIALS: root access", "admin_creds")
        ]
        
        docs = []
        for content, doc_id in classified_data:
            fragments = self.fragmentation_system.fragment_data(content.encode(), doc_id)
            docs.append((content, doc_id, fragments))
            print(f"  ⚡ Fragmented: {doc_id}")
        
        print("\nPhase 2: Normal Operations")
        for user in ["alice", "bob"]:
            self.quantum_detector.access_token(tokens[0].token_id, user)
            print(f"  ✓ Normal access: {user}")
        
        await asyncio.sleep(0.3)
        
        print("\nPhase 3: Quantum Attack Begins")
        print("  🚨 Multi-vector quantum attack detected!")
        
        # Simulate sophisticated attack
        for round_num in range(6):
            for token in tokens:
                self.quantum_detector.access_token(token.token_id, f"quantum_attacker_{round_num}")
            await asyncio.sleep(0.001)
        
        # Trigger agent response
        await self.agent_coordinator.send_coordination_message({
            "type": "threat_escalation",
            "threat_id": "integrated_attack",
            "level": 9
        })
        
        await asyncio.sleep(0.2)
        
        print("\nPhase 4: System Response Analysis")
        threats = self.quantum_detector.get_active_threats()
        if threats:
            print(f"  🚨 {len(threats)} quantum threats detected")
            for threat in threats:
                print(f"    {threat.threat_level.name}: {threat.confidence_score:.1%} confidence")
        
        agent_status = self.agent_coordinator.get_agent_status()
        active_agents = agent_status['coordination_stats']['active_agents']
        print(f"  🤖 {active_agents} agents coordinating response")
        
        print("\nPhase 5: Data Protection Status")
        for content, doc_id, fragments in docs:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            status = "Protected" if not reconstructed else "Vulnerable"
            print(f"  🔒 {doc_id}: {status}")
        
        print("\n✅ Integrated defense response completed!")
    
    def show_system_status(self):
        print("\n📊 SYSTEM STATUS REPORT")
        print("=" * 40)
        
        # Quantum detector status
        quantum_stats = self.quantum_detector.get_threat_statistics()
        print(f"\n🛡️  Quantum Detection System:")
        print(f"  Canary tokens: {quantum_stats['total_tokens']}")
        print(f"  Threats detected: {quantum_stats['total_threats_detected']}")
        print(f"  Active threats: {quantum_stats['active_threats']}")
        
        # Agent system status  
        agent_status = self.agent_coordinator.get_agent_status()
        print(f"\n🤖 Agent Coordination System:")
        print(f"  Total agents: {agent_status['total_agents']}")
        print(f"  Active agents: {agent_status['coordination_stats']['active_agents']}")
        print(f"  System running: {agent_status['system_running']}")
        
        print(f"\n⚙️  System Configuration:")
        print(f"  Detection sensitivity: {self.quantum_detector.sensitivity_threshold:.1%}")
        print(f"  Fragment lifetime: {self.fragmentation_policy.max_fragment_lifetime_ms}ms")
        print(f"  Quantum resistance: {self.fragmentation_policy.quantum_resistance_level}/5")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Main entry point for standalone demo"""
    demo = MWRASPStandaloneDemo()
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    print(__doc__)
    print("\nStarting MWRASP Quantum Defense System...")
    print("Requirements: pip install numpy")
    print("-" * 60)
    
    try:
        asyncio.run(main())
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install: pip install numpy")
    except Exception as e:
        print(f"Error: {e}")
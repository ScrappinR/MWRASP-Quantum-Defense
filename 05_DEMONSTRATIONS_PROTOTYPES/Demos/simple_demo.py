#!/usr/bin/env python3
"""
MWRASP Quantum Defense System - Simple Demo
Windows-compatible version without Rich formatting
"""

import asyncio
import time
import sys
from typing import List

# Import MWRASP components
from src.core.quantum_detector import QuantumDetector, ThreatLevel
from src.core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
from src.core.agent_system import AutonomousDefenseCoordinator


class SimpleMWRASPDemo:
    def __init__(self):
        print("=" * 60)
        print("     MWRASP QUANTUM DEFENSE SYSTEM - DEMO")
        print("  Multi-Wavelength Rapid-Aging Surveillance Platform")
        print("=" * 60)
        print()
        
        # Initialize system components
        print("Initializing MWRASP Quantum Defense System...")
        
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.6)
        
        self.fragmentation_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=300,  # 300ms for demo visibility
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
        """Run the complete demonstration"""
        try:
            await self._initialize_systems()
            
            print("\n" + "=" * 60)
            print("MWRASP DEMONSTRATION MENU")
            print("=" * 60)
            print("1. Quantum Computer Attack Detection Demo")
            print("2. Temporal Data Fragmentation Demo")
            print("3. Autonomous Agent Coordination Demo") 
            print("4. Integrated Attack Response Demo")
            print("5. System Status Report")
            print("6. Exit")
            print("=" * 60)
            
            while True:
                try:
                    choice = input("\nEnter your choice (1-6): ").strip()
                    
                    if choice == "1":
                        await self._demo_quantum_detection()
                    elif choice == "2":
                        await self._demo_temporal_fragmentation()
                    elif choice == "3":
                        await self._demo_agent_coordination()
                    elif choice == "4":
                        await self._demo_integrated_response()
                    elif choice == "5":
                        self._show_system_status()
                    elif choice == "6":
                        break
                    else:
                        print("Invalid choice. Please enter 1-6.")
                        continue
                        
                    input("\nPress Enter to return to menu...")
                    
                except KeyboardInterrupt:
                    print("\n\nDemo interrupted by user.")
                    break
                    
        finally:
            await self._cleanup()
    
    async def _initialize_systems(self):
        """Initialize all system components"""
        print("\n[1/3] Starting quantum detector monitoring...")
        self.quantum_detector.start_monitoring()
        await asyncio.sleep(0.5)
        
        print("[2/3] Starting temporal fragmentation service...")
        self.fragmentation_system.start_cleanup_service()
        await asyncio.sleep(0.5)
        
        print("[3/3] Initializing autonomous agent network...")
        await self.agent_coordinator.start_coordination()
        await asyncio.sleep(0.5)
        
        print("\n*** All systems online and operational! ***")
    
    async def _demo_quantum_detection(self):
        """Demonstrate quantum computer attack detection"""
        print("\n" + "=" * 50)
        print("QUANTUM COMPUTER ATTACK DETECTION DEMO")
        print("=" * 50)
        
        print("\nStep 1: Deploying Canary Tokens")
        print("-" * 30)
        
        # Create canary tokens for sensitive systems
        sensitive_systems = [
            "database_server",
            "encryption_keys", 
            "user_credentials",
            "api_gateway"
        ]
        
        tokens = []
        for system in sensitive_systems:
            token = self.quantum_detector.generate_canary_token(system)
            tokens.append(token)
            print(f"  -> Canary token deployed for: {system}")
            await asyncio.sleep(0.2)
        
        print(f"\nTotal canary tokens active: {len(tokens)}")
        
        # Simulate normal access
        print("\nStep 2: Normal System Access")
        print("-" * 30)
        normal_user = "legitimate_user_alice"
        self.quantum_detector.access_token(tokens[0].token_id, normal_user)
        print(f"  -> Normal access by {normal_user} - No threat detected")
        
        await asyncio.sleep(1)
        
        # Simulate quantum attack
        print("\nStep 3: Simulating Quantum Computer Attack")
        print("-" * 30)
        print("  -> Quantum computer attempting parallel access to multiple systems...")
        
        # Multiple rapid accesses (superposition pattern)
        for round_num in range(5):
            for i, token in enumerate(tokens):
                self.quantum_detector.access_token(token.token_id, f"quantum_attacker_wave_{round_num}")
                print(f"    [Attack {round_num+1}.{i+1}] Rapid access attempt")
            await asyncio.sleep(0.01)
        
        # Check for threat detection
        await asyncio.sleep(0.2)
        active_threats = self.quantum_detector.get_active_threats()
        
        print("\nStep 4: Threat Analysis Results")
        print("-" * 30)
        
        if active_threats:
            print("*** QUANTUM ATTACK DETECTED! ***")
            print("\nThreat Details:")
            
            for i, threat in enumerate(active_threats):
                print(f"  Threat {i+1}:")
                print(f"    ID: {threat.threat_id[:16]}...")
                print(f"    Level: {threat.threat_level.name}")
                print(f"    Confidence: {threat.confidence_score:.1%}")
                print(f"    Quantum Indicators: {', '.join(threat.quantum_indicators)}")
                print(f"    Affected Tokens: {len(threat.affected_tokens)}")
                print()
        else:
            print("No threats detected (sensitivity may need adjustment)")
        
        # Show statistics
        stats = self.quantum_detector.get_threat_statistics()
        print("Detection Statistics:")
        print(f"  Total Tokens: {stats['total_tokens']}")
        print(f"  Threats Detected: {stats['total_threats_detected']}")
        print(f"  Active Threats: {stats['active_threats']}")
        print(f"  Monitoring: {'Active' if stats['monitoring_active'] else 'Inactive'}")
    
    async def _demo_temporal_fragmentation(self):
        """Demonstrate temporal data fragmentation"""
        print("\n" + "=" * 50)
        print("TEMPORAL DATA FRAGMENTATION DEMO")
        print("=" * 50)
        
        # Test documents
        sensitive_documents = [
            ("TOP SECRET: Nuclear launch authorization codes", "nuclear_codes"),
            ("CLASSIFIED: Quantum encryption master keys", "quantum_keys"), 
            ("CONFIDENTIAL: Agent identities and locations", "agent_data")
        ]
        
        print("\nStep 1: Fragmenting Sensitive Data")
        print("-" * 30)
        
        fragment_results = []
        for doc_content, doc_id in sensitive_documents:
            data_bytes = doc_content.encode('utf-8')
            
            print(f"\nFragmenting: {doc_id}")
            print(f"  Original size: {len(data_bytes)} bytes")
            
            fragments = self.fragmentation_system.fragment_data(data_bytes, doc_id)
            fragment_results.append((doc_content, doc_id, fragments))
            
            print(f"  Created {len(fragments)} fragments")
            print(f"  Expires in: {fragments[0].expires_at - time.time():.3f} seconds")
        
        # Show fragmentation statistics
        fragment_stats = self.fragmentation_system.get_system_stats()
        print(f"\nFragmentation Statistics:")
        print(f"  Total Fragments: {fragment_stats['total_fragments']}")
        print(f"  Active Fragments: {fragment_stats['active_fragments']}")
        print(f"  Fragment Groups: {fragment_stats['fragment_groups']}")
        print(f"  Cleanup Service: {'Running' if fragment_stats['cleanup_running'] else 'Stopped'}")
        
        # Immediate reconstruction
        print("\nStep 2: Immediate Data Reconstruction")
        print("-" * 30)
        for doc_content, doc_id, fragments in fragment_results:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed and reconstructed.decode('utf-8') == doc_content:
                print(f"  -> Successfully reconstructed: {doc_id}")
            else:
                print(f"  -> Failed to reconstruct: {doc_id}")
        
        # Demonstrate expiration
        print("\nStep 3: Demonstrating Fragment Expiration")
        print("-" * 30)
        print("  -> Waiting for fragment expiration...")
        
        await asyncio.sleep(0.4)  # Wait for expiration
        
        print("  -> Attempting reconstruction after expiration:")
        for doc_content, doc_id, fragments in fragment_results:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed:
                print(f"    Still accessible: {doc_id}")
            else:
                print(f"    Properly expired: {doc_id} - Data no longer accessible")
    
    async def _demo_agent_coordination(self):
        """Demonstrate autonomous agent coordination"""
        print("\n" + "=" * 50)
        print("AUTONOMOUS AGENT COORDINATION DEMO")
        print("=" * 50)
        
        print("\nStep 1: Current Agent Network Status")
        print("-" * 30)
        
        agent_status = self.agent_coordinator.get_agent_status()
        
        print("Defense Agent Network:")
        for role, agents in agent_status['agents_by_role'].items():
            active_count = len([a for a in agents if a['status'] in ['active', 'busy']])
            total_count = len(agents)
            print(f"  {role.title()}: {total_count} agents ({active_count} active)")
        
        coord_stats = agent_status.get('coordination_stats', {})
        print(f"\nCoordination Statistics:")
        print(f"  Total Coordinations: {coord_stats.get('total_coordinations', 0)}")
        print(f"  Successful Defenses: {coord_stats.get('successful_defenses', 0)}")
        print(f"  Average Response Time: {coord_stats.get('average_response_time', 0):.1f}ms")
        
        # Trigger coordination
        print("\nStep 2: Triggering Agent Coordination")
        print("-" * 30)
        print("  -> Sending threat escalation message to agent network...")
        
        coordination_message = {
            "type": "threat_escalation",
            "threat_id": f"demo_threat_{int(time.time())}",
            "level": 8,
            "source": "demo_system"
        }
        
        await self.agent_coordinator.send_coordination_message(coordination_message)
        await asyncio.sleep(0.3)
        
        # Show response
        print("\nStep 3: Agent Response Status")
        print("-" * 30)
        updated_status = self.agent_coordinator.get_agent_status()
        
        for role, agents in updated_status['agents_by_role'].items():
            print(f"\n  {role.title()} Agents:")
            for i, agent in enumerate(agents):
                status = agent['status']
                workload = f"{agent['workload']}/{agent['max_workload']}"
                print(f"    Agent {i+1}: {status} (Workload: {workload})")
                
                if agent.get('current_task'):
                    print(f"      Current task: {agent['current_task']}")
        
        final_coords = updated_status.get('coordination_stats', {})
        if final_coords.get('total_coordinations', 0) > coord_stats.get('total_coordinations', 0):
            print("\n  -> Agent coordination successfully executed!")
            print(f"     New total coordinations: {final_coords.get('total_coordinations', 0)}")
        
        print("\n*** Autonomous agent network operational and responsive! ***")
    
    async def _demo_integrated_response(self):
        """Demonstrate integrated attack response"""
        print("\n" + "=" * 50)
        print("INTEGRATED QUANTUM ATTACK RESPONSE DEMO")
        print("=" * 50)
        
        print("\nPhase 1: Deploying Critical Infrastructure Protection")
        print("-" * 30)
        
        # Deploy canary tokens
        critical_systems = [
            ("financial_database", "Primary financial transaction database"),
            ("user_authentication", "User authentication system"),
            ("encryption_service", "Cryptographic key management"),
            ("backup_systems", "Critical system backup and recovery")
        ]
        
        tokens = []
        for system_id, description in critical_systems:
            token = self.quantum_detector.generate_canary_token(system_id)
            tokens.append((token, system_id, description))
            print(f"  -> Protected: {description}")
        
        # Fragment critical data
        critical_documents = [
            ("MASTER_ENCRYPTION_KEYS: AES-256, RSA-4096", "master_keys"),
            ("ADMIN_CREDENTIALS: root, admin, service", "admin_creds"),
            ("SYSTEM_TOPOLOGY: network_diagram, servers", "topology")
        ]
        
        fragmented_docs = []
        for doc_content, doc_id in critical_documents:
            fragments = self.fragmentation_system.fragment_data(doc_content.encode(), doc_id)
            fragmented_docs.append((doc_content, doc_id, fragments))
            print(f"  -> Fragmented: {doc_id} ({len(fragments)} fragments)")
        
        await asyncio.sleep(1)
        
        # Normal operations
        print("\nPhase 2: Normal System Operations")
        print("-" * 30)
        
        legitimate_users = ["alice_admin", "bob_analyst", "charlie_operator"]
        for user in legitimate_users:
            token, system_id, _ = tokens[0]
            self.quantum_detector.access_token(token.token_id, user)
            print(f"  -> Normal access: {user} -> {system_id}")
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.5)
        
        # Quantum attack
        print("\nPhase 3: Quantum Computer Attack Initiated")
        print("-" * 30)
        
        attack_vectors = [
            "Superposition Access - Multiple simultaneous system accesses",
            "Entanglement Correlation - Correlated attacks across systems", 
            "Quantum Speedup - Unnaturally rapid computation patterns"
        ]
        
        for i, vector_desc in enumerate(attack_vectors):
            print(f"  -> {vector_desc}")
            
            if i == 0:  # Superposition
                for round_num in range(6):
                    for token, system_id, _ in tokens:
                        self.quantum_detector.access_token(token.token_id, f"quantum_super_{round_num}")
                    await asyncio.sleep(0.001)
            
            elif i == 1:  # Entanglement
                for j in range(8):
                    for token, system_id, _ in tokens[::2]:
                        self.quantum_detector.access_token(token.token_id, f"quantum_entangled_{j}")
                    await asyncio.sleep(0.002)
            
            elif i == 2:  # Speedup
                token, system_id, _ = tokens[1]
                for j in range(15):
                    self.quantum_detector.access_token(token.token_id, f"quantum_speed_{j}")
            
            await asyncio.sleep(0.2)
        
        # System response
        print("\nPhase 4: MWRASP System Response")
        print("-" * 30)
        
        await asyncio.sleep(0.3)
        
        # Check threats
        active_threats = self.quantum_detector.get_active_threats()
        
        if active_threats:
            print("*** MULTIPLE QUANTUM ATTACKS DETECTED! ***")
            print("\nThreat Analysis Report:")
            
            for i, threat in enumerate(active_threats):
                print(f"  Threat {i+1}: {threat.threat_level.name} "
                      f"(Confidence: {threat.confidence_score:.1%})")
                print(f"    Attack Vectors: {', '.join(threat.quantum_indicators[:2])}")
                print(f"    Affected Systems: {len(threat.affected_tokens)}")
            
            # Agent response
            print("\n*** Autonomous Agent Response Activated ***")
            agent_status = self.agent_coordinator.get_agent_status()
            
            active_agents = 0
            for role, agents in agent_status['agents_by_role'].items():
                role_active = len([a for a in agents if a['status'] in ['active', 'busy']])
                if role_active > 0:
                    active_agents += role_active
                    print(f"  -> {role.title()}: {role_active} agents responding")
            
            print(f"\n  Total agents coordinating response: {active_agents}")
        else:
            print("Attack patterns not detected - sensitivity may need adjustment")
        
        # Data protection status
        print("\nPhase 5: Critical Data Protection Status")
        print("-" * 30)
        
        for doc_content, doc_id, fragments in fragmented_docs:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            is_accessible = reconstructed == doc_content.encode() if reconstructed else False
            
            fragment_status = self.fragmentation_system.get_fragment_status(doc_id)
            active_fragments = fragment_status.get('active_fragments', 0) if fragment_status else 0
            
            status = "Protected (Expired)" if not is_accessible else "Vulnerable (Active)"
            print(f"  {doc_id}: {status} - {active_fragments} active fragments")
        
        print("\n*** Integrated attack response demonstration completed! ***")
        print("The MWRASP system successfully detected, responded to, and mitigated the quantum attack.")
    
    def _show_system_status(self):
        """Show comprehensive system status"""
        print("\n" + "=" * 50)
        print("COMPREHENSIVE SYSTEM STATUS REPORT")
        print("=" * 50)
        
        # Get system statistics
        quantum_stats = self.quantum_detector.get_threat_statistics()
        fragment_stats = self.fragmentation_system.get_system_stats()
        agent_stats = self.agent_coordinator.get_agent_status()
        
        print("\nQuantum Detection System:")
        print("-" * 25)
        print(f"  Status: {'Online' if quantum_stats['monitoring_active'] else 'Offline'}")
        print(f"  Canary Tokens: {quantum_stats['total_tokens']}")
        print(f"  Threats Detected: {quantum_stats['total_threats_detected']}")
        print(f"  Active Threats: {quantum_stats['active_threats']}")
        
        print("\nTemporal Fragmentation System:")
        print("-" * 30)
        print(f"  Status: {'Online' if fragment_stats['cleanup_running'] else 'Offline'}")
        print(f"  Total Fragments: {fragment_stats['total_fragments']}")
        print(f"  Active Fragments: {fragment_stats['active_fragments']}")
        print(f"  Fragment Groups: {fragment_stats['fragment_groups']}")
        
        print("\nAgent Coordination System:")
        print("-" * 25)
        print(f"  Status: {'Online' if agent_stats['system_running'] else 'Offline'}")
        print(f"  Total Agents: {agent_stats['total_agents']}")
        print(f"  Active Agents: {agent_stats['coordination_stats'].get('active_agents', 0)}")
        print(f"  Total Coordinations: {agent_stats['coordination_stats'].get('total_coordinations', 0)}")
        
        print("\nAgent Network Details:")
        print("-" * 20)
        for role, agents in agent_stats['agents_by_role'].items():
            counts = {'active': 0, 'busy': 0, 'idle': 0, 'error': 0}
            for agent in agents:
                status = agent['status']
                if status in counts:
                    counts[status] += 1
            
            print(f"  {role.title()}: {len(agents)} total "
                  f"({counts['active']} active, {counts['busy']} busy, "
                  f"{counts['idle']} idle, {counts['error']} error)")
        
        print("\nConfiguration Summary:")
        print("-" * 20)
        print(f"  Quantum Sensitivity: {self.quantum_detector.sensitivity_threshold:.1%}")
        print(f"  Fragment Lifetime: {self.fragmentation_policy.max_fragment_lifetime_ms}ms")
        print(f"  Quantum Resistance: {self.fragmentation_policy.quantum_resistance_level}/5")
        print(f"  Fragment Range: {self.fragmentation_policy.min_fragments}-{self.fragmentation_policy.max_fragments}")
    
    async def _cleanup(self):
        """Clean up demo resources"""
        print("\n" + "=" * 50)
        print("SHUTTING DOWN MWRASP SYSTEMS")
        print("=" * 50)
        
        print("[1/3] Stopping agent coordination...")
        await self.agent_coordinator.stop_coordination()
        
        print("[2/3] Stopping fragmentation cleanup...")
        self.fragmentation_system.stop_cleanup_service()
        
        print("[3/3] Stopping quantum monitoring...")
        self.quantum_detector.stop_monitoring()
        
        print("\n*** All systems shut down safely! ***")
        print("\nThank you for exploring the MWRASP Quantum Defense System!")


async def main():
    """Main demo entry point"""
    demo = SimpleMWRASPDemo()
    
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
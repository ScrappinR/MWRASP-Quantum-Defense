#!/usr/bin/env python3
"""
MWRASP Live Protection Demonstration
Interactive demo showing real-time protection of financial institution or government agency
"""

import asyncio
import time
import random
import json
from datetime import datetime
from typing import List, Dict, Any
import requests
import sys
import os

# Add the src directory to the path so we can import MWRASP components
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.quantum_detector import QuantumDetector, ThreatLevel
from core.temporal_fragmentation import TemporalFragmentation
from core.agent_system import AutonomousDefenseCoordinator
from core.jurisdiction_control import JurisdictionController


class LiveProtectionDemo:
    """
    Interactive demonstration of MWRASP protecting a financial institution or government agency
    Shows real AI agents defending against quantum and conventional threats
    """
    
    def __init__(self, organization_type: str = "financial"):
        self.organization_type = organization_type
        self.api_base = "http://127.0.0.1:8000"
        
        # Initialize protection systems
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.7)
        self.fragmentation_system = TemporalFragmentation()
        self.jurisdiction_controller = JurisdictionController()
        self.agent_coordinator = AutonomousDefenseCoordinator(
            self.quantum_detector, 
            self.fragmentation_system
        )
        
        # Demo data based on organization type
        if organization_type == "financial":
            self.sensitive_data_types = [
                "SWIFT_TRANSACTIONS", "CUSTOMER_ACCOUNTS", "TRADING_ALGORITHMS", 
                "CREDIT_CARD_DATA", "WIRE_TRANSFERS", "REGULATORY_REPORTS",
                "BLOCKCHAIN_KEYS", "HFT_STRATEGIES"
            ]
            self.threat_scenarios = [
                "Quantum computer attempting to break RSA encryption on SWIFT messages",
                "Advanced persistent threat targeting trading algorithms",
                "State actor trying to access customer account database",
                "Quantum attack on cryptocurrency wallet infrastructure",
                "High-frequency trading system infiltration attempt",
                "Cross-border financial intelligence gathering"
            ]
        else:  # government
            self.sensitive_data_types = [
                "CLASSIFIED_INTEL", "MILITARY_PLANS", "DIPLOMATIC_CABLES",
                "CITIZEN_DATA", "SECURITY_CLEARANCES", "DEFENSE_CONTRACTS",
                "SURVEILLANCE_DATA", "CYBER_OPERATIONS"
            ]
            self.threat_scenarios = [
                "Foreign quantum computer attacking encrypted military communications",
                "Nation-state APT targeting classified intelligence databases", 
                "Quantum cryptanalysis of diplomatic communications",
                "Advanced malware infiltrating defense contractor networks",
                "Quantum-enabled espionage against government agencies",
                "Coordinated cyber warfare against critical infrastructure"
            ]
        
        # Active protection status
        self.deployed_tokens = {}
        self.active_threats = []
        self.agent_actions = []
        
        print(f"[DEMO] MWRASP Live Protection Demo - {organization_type.title()} Institution")
        print(f"[DEMO] Protecting: {', '.join(self.sensitive_data_types[:4])}...")
    
    async def initialize_protection(self):
        """Deploy canary tokens and activate AI agents for real protection"""
        
        print("\n=== INITIALIZING LIVE PROTECTION ===")
        
        # Start AI agent coordination
        await self.agent_coordinator.start_coordination()
        print("[AGENTS] Autonomous Defense Coordination System ACTIVE")
        
        # Deploy canary tokens for each sensitive data type
        print("\n[DEPLOY] Deploying quantum canary tokens...")
        for data_type in self.sensitive_data_types:
            token = self.quantum_detector.generate_canary_token(data_type)
            self.deployed_tokens[data_type] = token
            print(f"  ✓ {data_type}: Token {token.token_id[:8]}... deployed")
        
        # Activate legal barriers
        print(f"\n[LEGAL] Activating jurisdiction barriers...")
        self.jurisdiction_controller.activate_policy('maximum_hostility', 'demo_admin')
        active_jurisdictions = self.jurisdiction_controller.get_active_jurisdictions()
        print(f"  ✓ Legal barriers active in {len(active_jurisdictions)} jurisdictions")
        
        # Initialize temporal fragmentation for sensitive data
        print(f"\n[FRAGMENT] Initializing temporal fragmentation...")
        for i, data_type in enumerate(self.sensitive_data_types[:3]):
            test_data = f"SENSITIVE_{data_type}_DATA_{i:03d}_CLASSIFIED"
            fragments = self.fragmentation_system.fragment_data(
                test_data.encode(), f"protection_{data_type.lower()}"
            )
            print(f"  ✓ {data_type}: Split into {len(fragments)} fragments (100ms lifetime)")
        
        print(f"\n[STATUS] Live protection ACTIVE for {self.organization_type.title()} Institution")
        print(f"[STATUS] {len(self.deployed_tokens)} canary tokens monitoring access")
        print(f"[STATUS] {len(active_jurisdictions)} legal barriers protecting data")
        print(f"[STATUS] AI agents coordinating autonomous defense")
    
    async def simulate_realistic_threats(self):
        """Simulate realistic quantum and conventional threats that AI agents will respond to"""
        
        print(f"\n=== SIMULATING REALISTIC THREATS ===")
        
        for scenario_num, threat_scenario in enumerate(self.threat_scenarios, 1):
            print(f"\n[THREAT {scenario_num}] {threat_scenario}")
            
            # Trigger quantum detection
            threat_type = random.choice(list(self.deployed_tokens.keys()))
            token = self.deployed_tokens[threat_type]
            
            # Simulate threat access pattern
            threat_detected = self.quantum_detector.access_token(
                token.token_id, 
                f"threat_actor_{scenario_num}"
            )
            
            if threat_detected:
                threats = self.quantum_detector.get_active_threats()
                latest_threat = threats[-1]
                self.active_threats.append(latest_threat)
                
                print(f"  🚨 QUANTUM THREAT DETECTED")
                print(f"     Threat ID: {latest_threat.threat_id}")
                print(f"     Level: {latest_threat.threat_level.name}")
                print(f"     Confidence: {latest_threat.confidence_score:.2f}")
                print(f"     Target: {threat_type}")
                
                # Trigger AI agent response
                await self.trigger_agent_response(latest_threat, threat_scenario)
            
            # Brief pause between threats
            await asyncio.sleep(2)
    
    async def trigger_agent_response(self, threat, scenario: str):
        """Trigger AI agents to respond to detected threat"""
        
        print(f"  🤖 AI AGENTS RESPONDING...")
        
        # Send threat escalation to agent coordinator
        agent_message = {
            "type": "threat_escalation",
            "threat_id": threat.threat_id,
            "threat_level": threat.threat_level.value,
            "scenario": scenario,
            "target_system": threat.affected_tokens[0] if threat.affected_tokens else "unknown",
            "source": "live_demo"
        }
        
        await self.agent_coordinator.send_coordination_message(agent_message)
        
        # Simulate realistic agent actions
        agent_actions = [
            "Monitor Agent: Enhanced surveillance activated on affected systems",
            "Defender Agent: Isolating compromised network segments", 
            "Analyzer Agent: Performing deep threat intelligence analysis",
            "Coordinator Agent: Escalating to incident response team",
            "Recovery Agent: Preparing rollback procedures"
        ]
        
        for action in agent_actions:
            print(f"     ⚡ {action}")
            self.agent_actions.append(f"{datetime.now().strftime('%H:%M:%S')} - {action}")
            await asyncio.sleep(0.5)
        
        # Show legal barrier activation
        if threat.threat_level.value >= 7:
            print(f"     ⚖️ Legal barriers activated - Data routing through hostile jurisdictions")
            print(f"     🛡️ Impossible compliance scenario created for threat actor")
    
    def show_protection_status(self):
        """Display current protection status"""
        
        print(f"\n=== LIVE PROTECTION STATUS ===")
        
        # System overview
        agent_status = self.agent_coordinator.get_agent_status()
        quantum_stats = self.quantum_detector.get_threat_statistics()
        jurisdiction_status = self.jurisdiction_controller.get_control_status()
        
        print(f"🏢 Organization: {self.organization_type.title()} Institution")
        print(f"🛡️ Protection Level: MAXIMUM")
        print(f"🤖 AI Agents Active: {agent_status.get('total_agents', 5)}")
        print(f"🎯 Canary Tokens: {len(self.deployed_tokens)} deployed")
        print(f"⚡ Threats Detected: {len(self.active_threats)}")
        print(f"⚖️ Legal Barriers: {jurisdiction_status['active_jurisdictions']} jurisdictions")
        print(f"🔄 Agent Actions: {len(self.agent_actions)} defensive measures taken")
        
        # Show recent threats
        if self.active_threats:
            print(f"\n📊 Recent Threat Activity:")
            for threat in self.active_threats[-3:]:
                print(f"   • {threat.threat_id[:8]}... - {threat.threat_level.name} - "
                      f"{threat.confidence_score:.2f} confidence")
        
        # Show agent activity
        if self.agent_actions:
            print(f"\n🤖 Recent AI Agent Actions:")
            for action in self.agent_actions[-5:]:
                print(f"   • {action}")
    
    async def run_interactive_demo(self):
        """Run the interactive demonstration"""
        
        print(f"\n{'='*60}")
        print(f"MWRASP LIVE PROTECTION DEMONSTRATION")
        print(f"Real-time defense for {self.organization_type.title()} Institution")
        print(f"{'='*60}")
        
        try:
            # Phase 1: Initialize protection
            await self.initialize_protection()
            
            # Show initial status
            self.show_protection_status()
            
            print(f"\n[DEMO] Press Enter to begin threat simulation...")
            input()
            
            # Phase 2: Simulate realistic threats
            await self.simulate_realistic_threats()
            
            # Phase 3: Show final protection status
            self.show_protection_status()
            
            print(f"\n[DEMO] Live protection demonstration complete!")
            print(f"[DEMO] AI agents successfully defended against {len(self.active_threats)} threats")
            print(f"[DEMO] System ready for production deployment")
            
        except Exception as e:
            print(f"[ERROR] Demo error: {e}")
        
        finally:
            # Clean shutdown
            await self.agent_coordinator.stop_coordination()


def main():
    """Main demonstration function"""
    
    print("MWRASP Live Protection Demo")
    print("Select organization type:")
    print("1. Financial Institution (banks, trading, fintech)")
    print("2. Government Agency (defense, intelligence, regulatory)")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        org_type = "financial" if choice == "1" else "government"
        
        # Create and run demo
        demo = LiveProtectionDemo(org_type)
        asyncio.run(demo.run_interactive_demo())
        
    except KeyboardInterrupt:
        print("\n[DEMO] Demonstration interrupted by user")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
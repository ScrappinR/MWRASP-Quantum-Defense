#!/usr/bin/env python3
"""
MWRASP Agent Coordination Demo - Simple Version
Demonstrates the autonomous defense agent network
"""

import asyncio
import time
import secrets
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


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
    current_task: str = None


class AutonomousDefenseCoordinator:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.running = False
        self.coordination_stats = {
            'total_coordinations': 0,
            'successful_defenses': 0,
            'failed_defenses': 0,
            'active_agents': 0,
            'average_response_time': 0.0
        }
        self._initialize_agent_fleet()
    
    def _initialize_agent_fleet(self):
        """Initialize the autonomous defense agent fleet"""
        current_time = time.time()
        
        # Create different types of agents
        agent_configs = [
            (AgentRole.MONITOR, 1, AgentStatus.ACTIVE, 15),    # 1 Monitor agent (always active)
            (AgentRole.DEFENDER, 3, AgentStatus.IDLE, 8),      # 3 Defender agents
            (AgentRole.ANALYZER, 1, AgentStatus.IDLE, 5),      # 1 Analyzer agent
            (AgentRole.RECOVERY, 1, AgentStatus.IDLE, 3),      # 1 Recovery agent
            (AgentRole.COORDINATOR, 1, AgentStatus.ACTIVE, 20) # 1 Coordinator (always active)
        ]
        
        for role, count, status, max_workload in agent_configs:
            for i in range(count):
                agent_id = f"{role.value}_{i}_{secrets.token_hex(4)}"
                agent = Agent(
                    agent_id=agent_id,
                    role=role,
                    status=status,
                    created_at=current_time,
                    max_workload=max_workload
                )
                self.agents[agent_id] = agent
    
    async def start_coordination(self):
        """Start the autonomous coordination system"""
        self.running = True
        print("MWRASP Autonomous Defense System activated")
    
    def get_agent_status(self) -> Dict:
        """Get comprehensive agent status information"""
        agents_by_role = defaultdict(list)
        
        for agent in self.agents.values():
            agents_by_role[agent.role.value].append({
                'agent_id': agent.agent_id,
                'status': agent.status.value,
                'workload': agent.workload,
                'max_workload': agent.max_workload,
                'processed_threats': agent.processed_threats,
                'success_rate': agent.success_rate,
                'current_task': agent.current_task
            })
        
        # Update active agent count
        active_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.ACTIVE)
        self.coordination_stats['active_agents'] = active_agents
        
        return {
            'agents_by_role': dict(agents_by_role),
            'total_agents': len(self.agents),
            'coordination_stats': self.coordination_stats,
            'system_running': self.running
        }
    
    async def send_coordination_message(self, message: Dict):
        """Send a message to the coordination system"""
        message_type = message.get("type")
        threat_level = message.get("level", 1)
        
        print(f"Processing coordination message: {message_type}")
        
        response_start_time = time.time()
        
        if message_type == "threat_escalation":
            await self._handle_threat_escalation(message)
        elif message_type == "agent_request_help":
            await self._handle_help_request(message)
        
        # Update coordination stats
        response_time = (time.time() - response_start_time) * 1000  # ms
        self.coordination_stats['total_coordinations'] += 1
        
        # Update average response time
        current_avg = self.coordination_stats['average_response_time']
        total_coords = self.coordination_stats['total_coordinations']
        new_avg = (current_avg * (total_coords - 1) + response_time) / total_coords
        self.coordination_stats['average_response_time'] = new_avg
        
        print(f"Coordination completed in {response_time:.1f}ms")
    
    async def _handle_threat_escalation(self, message: Dict):
        """Handle threat escalation messages"""
        threat_level = message.get("level", 1)
        threat_id = message.get("threat_id", "unknown")
        
        print(f"Threat escalation level {threat_level} for {threat_id}")
        
        # Activate agents based on threat level
        if threat_level >= 8:  # High severity
            # Activate all defender agents
            defenders = [a for a in self.agents.values() if a.role == AgentRole.DEFENDER]
            for defender in defenders:
                if defender.status == AgentStatus.IDLE:
                    defender.status = AgentStatus.ACTIVE
                    defender.workload += 2
                    defender.current_task = f"threat_response_{threat_id}"
                    print(f"  -> Activated defender: {defender.agent_id}")
            
            # Activate analyzer
            analyzer = next((a for a in self.agents.values() if a.role == AgentRole.ANALYZER), None)
            if analyzer and analyzer.status == AgentStatus.IDLE:
                analyzer.status = AgentStatus.ACTIVE
                analyzer.workload += 3
                analyzer.current_task = f"threat_analysis_{threat_id}"
                print(f"  -> Activated analyzer: {analyzer.agent_id}")
        
        elif threat_level >= 5:  # Medium severity
            # Activate one defender
            defenders = [a for a in self.agents.values() 
                        if a.role == AgentRole.DEFENDER and a.status == AgentStatus.IDLE]
            if defenders:
                defender = defenders[0]
                defender.status = AgentStatus.ACTIVE
                defender.workload += 1
                defender.current_task = f"threat_response_{threat_id}"
                print(f"  -> Activated defender: {defender.agent_id}")
        
        # Always engage coordinator
        coordinator = next((a for a in self.agents.values() if a.role == AgentRole.COORDINATOR), None)
        if coordinator:
            coordinator.workload += 1
            coordinator.current_task = f"coordinate_{threat_id}"
            print(f"  -> Coordinator managing response")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Mark as successful defense
        self.coordination_stats['successful_defenses'] += 1
    
    async def _handle_help_request(self, message: Dict):
        """Handle agent help requests"""
        requesting_agent_id = message.get("agent_id")
        capability = message.get("capability", "general_support")
        
        print(f"Help request from {requesting_agent_id} for {capability}")
        
        # Find available agents to help
        available_agents = [
            a for a in self.agents.values()
            if a.agent_id != requesting_agent_id and a.workload < a.max_workload
        ]
        
        if available_agents:
            helper = available_agents[0]
            helper.workload += 1
            helper.current_task = f"assisting_{requesting_agent_id}"
            print(f"  -> {helper.role.value} agent providing assistance")
        else:
            print(f"  -> No available agents to provide assistance")
        
        await asyncio.sleep(0.05)


async def run_agent_demo():
    """Run the agent coordination demonstration"""
    print("AUTONOMOUS AGENT COORDINATION DEMO")
    print("=" * 40)
    
    # Initialize coordinator
    coordinator = AutonomousDefenseCoordinator()
    await coordinator.start_coordination()
    
    print("\nStep 1: Agent Network Status")
    print("-" * 30)
    
    status = coordinator.get_agent_status()
    
    for role, agents in status['agents_by_role'].items():
        active_count = len([a for a in agents if a['status'] in ['active', 'busy']])
        total_count = len(agents)
        print(f"  {role.title()}: {total_count} agents ({active_count} active)")
    
    coord_stats = status['coordination_stats']
    print(f"\nCoordination Statistics:")
    print(f"  Total Coordinations: {coord_stats['total_coordinations']}")
    print(f"  Successful Defenses: {coord_stats['successful_defenses']}")
    print(f"  Active Agents: {coord_stats['active_agents']}")
    
    print("\nStep 2: Triggering Agent Coordination")
    print("-" * 30)
    
    # Scenario 1: Medium threat escalation
    print("\nScenario 1: Medium Threat (Level 5)")
    message1 = {
        "type": "threat_escalation",
        "threat_id": f"demo_threat_medium_{int(time.time())}",
        "level": 5,
        "source": "demo_system"
    }
    
    await coordinator.send_coordination_message(message1)
    await asyncio.sleep(0.5)
    
    # Scenario 2: High threat escalation
    print("\nScenario 2: High Threat (Level 9)")
    message2 = {
        "type": "threat_escalation", 
        "threat_id": f"demo_threat_critical_{int(time.time())}",
        "level": 9,
        "source": "demo_system"
    }
    
    await coordinator.send_coordination_message(message2)
    await asyncio.sleep(0.5)
    
    print("\nStep 3: Agent Response Analysis")
    print("-" * 30)
    
    final_status = coordinator.get_agent_status()
    
    for role, agents in final_status['agents_by_role'].items():
        print(f"\n  {role.title()} Agents:")
        for agent in agents:
            status_text = agent['status'].upper() if agent['status'] == 'active' else agent['status']
            workload = f"{agent['workload']}/{agent['max_workload']}"
            current_task = agent['current_task'] or 'None'
            
            print(f"    Agent: {status_text}")
            print(f"      Workload: {workload}")
            print(f"      Current Task: {current_task}")
    
    print("\nStep 4: Inter-Agent Coordination")
    print("-" * 30)
    
    # Help request scenario
    print("\nAgent Help Request:")
    help_message = {
        "type": "agent_request_help",
        "agent_id": "demo_agent_001",
        "capability": "quantum_analysis"
    }
    
    await coordinator.send_coordination_message(help_message)
    
    # Final statistics
    print("\nStep 5: Final Coordination Statistics")
    print("-" * 30)
    
    final_stats = coordinator.get_agent_status()['coordination_stats']
    
    print(f"Coordination Summary:")
    print(f"  Total Coordinations: {final_stats['total_coordinations']}")
    print(f"  Successful Defenses: {final_stats['successful_defenses']}")
    print(f"  Active Agents: {final_stats['active_agents']}")
    print(f"  Average Response Time: {final_stats['average_response_time']:.1f}ms")
    success_rate = (final_stats['successful_defenses'] / max(1, final_stats['total_coordinations']) * 100)
    print(f"  Success Rate: {success_rate:.1f}%")
    
    print("\nAgent coordination demonstration completed!")
    print("All agents coordinated successfully to respond to threats")


if __name__ == "__main__":
    print("MWRASP Agent Coordination System Demo")
    print("=" * 50)
    print("Demonstrates autonomous defense agent network")
    print("with real-time coordination and response.\n")
    
    try:
        asyncio.run(run_agent_demo())
    except Exception as e:
        print(f"Demo error: {e}")
    
    print("\nDemo completed!")
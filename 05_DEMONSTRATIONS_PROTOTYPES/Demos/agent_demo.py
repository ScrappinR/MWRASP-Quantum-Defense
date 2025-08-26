#!/usr/bin/env python3
"""
MWRASP Agent Coordination Demo
Focused demonstration of the autonomous defense agent system
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
        
        # Monitor Agent - Continuous surveillance
        monitor_agent = Agent(
            agent_id=f"monitor_{secrets.token_hex(4)}",
            role=AgentRole.MONITOR,
            status=AgentStatus.ACTIVE,
            created_at=current_time,
            max_workload=15
        )
        self.agents[monitor_agent.agent_id] = monitor_agent
        
        # Defender Agents - Active threat response (3 agents)
        for i in range(3):
            defender_agent = Agent(
                agent_id=f"defender_{i}_{secrets.token_hex(4)}",
                role=AgentRole.DEFENDER,
                status=AgentStatus.IDLE,
                created_at=current_time,
                max_workload=8
            )
            self.agents[defender_agent.agent_id] = defender_agent
        
        # Analyzer Agent - Deep threat analysis
        analyzer_agent = Agent(
            agent_id=f"analyzer_{secrets.token_hex(4)}",
            role=AgentRole.ANALYZER,
            status=AgentStatus.IDLE,
            created_at=current_time,
            max_workload=5
        )
        self.agents[analyzer_agent.agent_id] = analyzer_agent
        
        # Recovery Agent - System recovery
        recovery_agent = Agent(
            agent_id=f"recovery_{secrets.token_hex(4)}",
            role=AgentRole.RECOVERY,
            status=AgentStatus.IDLE,
            created_at=current_time,
            max_workload=3
        )
        self.agents[recovery_agent.agent_id] = recovery_agent
        
        # Coordinator Agent - Overall coordination
        coordinator_agent = Agent(
            agent_id=f"coordinator_{secrets.token_hex(4)}",
            role=AgentRole.COORDINATOR,
            status=AgentStatus.ACTIVE,
            created_at=current_time,
            max_workload=20
        )
        self.agents[coordinator_agent.agent_id] = coordinator_agent
    
    async def start_coordination(self):
        """Start the autonomous coordination system"""
        self.running = True
        print("🤖 MWRASP Autonomous Defense System activated")
    
    async def stop_coordination(self):
        """Stop the coordination system"""
        self.running = False
        for agent in self.agents.values():
            agent.status = AgentStatus.IDLE
            agent.workload = 0
            agent.current_task = None
    
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
        
        print(f"📡 Processing coordination message: {message_type}")
        
        response_start_time = time.time()
        
        if message_type == "threat_escalation":
            await self._handle_threat_escalation(message)
        elif message_type == "agent_request_help":
            await self._handle_help_request(message)
        elif message_type == "resource_request":
            await self._handle_resource_request(message)
        
        # Update coordination stats
        response_time = (time.time() - response_start_time) * 1000  # ms
        self.coordination_stats['total_coordinations'] += 1
        
        # Update average response time
        current_avg = self.coordination_stats['average_response_time']
        total_coords = self.coordination_stats['total_coordinations']
        new_avg = (current_avg * (total_coords - 1) + response_time) / total_coords
        self.coordination_stats['average_response_time'] = new_avg
        
        print(f"⚡ Coordination completed in {response_time:.1f}ms")
    
    async def _handle_threat_escalation(self, message: Dict):
        """Handle threat escalation messages"""
        threat_level = message.get("level", 1)
        threat_id = message.get("threat_id", "unknown")
        
        print(f"🚨 Threat escalation level {threat_level} for {threat_id}")
        
        # Activate agents based on threat level
        if threat_level >= 8:  # High severity
            # Activate all defender agents
            defenders = [a for a in self.agents.values() if a.role == AgentRole.DEFENDER]
            for defender in defenders:
                if defender.status == AgentStatus.IDLE:
                    defender.status = AgentStatus.ACTIVE
                    defender.workload += 2
                    defender.current_task = f"threat_response_{threat_id}"
                    print(f"  🛡️  Activated defender: {defender.agent_id}")
            
            # Activate analyzer
            analyzer = next((a for a in self.agents.values() if a.role == AgentRole.ANALYZER), None)
            if analyzer and analyzer.status == AgentStatus.IDLE:
                analyzer.status = AgentStatus.ACTIVE
                analyzer.workload += 3
                analyzer.current_task = f"threat_analysis_{threat_id}"
                print(f"  🔍 Activated analyzer: {analyzer.agent_id}")
        
        elif threat_level >= 5:  # Medium severity
            # Activate one defender
            defenders = [a for a in self.agents.values() 
                        if a.role == AgentRole.DEFENDER and a.status == AgentStatus.IDLE]
            if defenders:
                defender = defenders[0]
                defender.status = AgentStatus.ACTIVE
                defender.workload += 1
                defender.current_task = f"threat_response_{threat_id}"
                print(f"  🛡️  Activated defender: {defender.agent_id}")
        
        # Always engage coordinator for coordination
        coordinator = next((a for a in self.agents.values() if a.role == AgentRole.COORDINATOR), None)
        if coordinator:
            coordinator.workload += 1
            coordinator.current_task = f"coordinate_{threat_id}"
            print(f"  🎯 Coordinator managing response")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Mark as successful defense
        self.coordination_stats['successful_defenses'] += 1
    
    async def _handle_help_request(self, message: Dict):
        """Handle agent help requests"""
        requesting_agent_id = message.get("agent_id")
        capability = message.get("capability", "general_support")
        
        print(f"🤝 Help request from {requesting_agent_id} for {capability}")
        
        # Find available agents to help
        available_agents = [
            a for a in self.agents.values()
            if a.agent_id != requesting_agent_id and a.workload < a.max_workload
        ]
        
        if available_agents:
            helper = available_agents[0]
            helper.workload += 1
            helper.current_task = f"assisting_{requesting_agent_id}"
            print(f"  ✅ {helper.role.value} agent {helper.agent_id} providing assistance")
        else:
            print(f"  ⚠️  No available agents to provide assistance")
        
        await asyncio.sleep(0.05)
    
    async def _handle_resource_request(self, message: Dict):
        """Handle resource allocation requests"""
        requesting_agent_id = message.get("agent_id")
        resource_type = message.get("resource", "processing_power")
        
        print(f"📊 Resource request: {resource_type} for {requesting_agent_id}")
        
        # Redistribute workload to help requesting agent
        if resource_type == "processing_power":
            # Reduce workload of non-critical agents
            for agent in self.agents.values():
                if (agent.agent_id != requesting_agent_id and 
                    agent.role not in [AgentRole.COORDINATOR, AgentRole.MONITOR] and
                    agent.workload > 0):
                    agent.workload = max(0, agent.workload - 1)
                    print(f"  📉 Reduced workload for {agent.role.value} agent")
                    break
        
        await asyncio.sleep(0.03)


async def demo_agent_coordination():
    """Demonstrate autonomous agent coordination"""
    print("🤖 AUTONOMOUS AGENT COORDINATION DEMO")
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
        
        # Show individual agent details
        for agent in agents:
            status_icon = {
                'idle': '⚪',
                'active': '🟢', 
                'busy': '🟡',
                'error': '🔴'
            }.get(agent['status'], '⚪')
            
            workload = f"{agent['workload']}/{agent['max_workload']}"
            print(f"    {status_icon} Agent: {agent['status']} (Load: {workload})")
    
    coord_stats = status['coordination_stats']
    print(f"\nCoordination Statistics:")
    print(f"  Total Coordinations: {coord_stats['total_coordinations']}")
    print(f"  Successful Defenses: {coord_stats['successful_defenses']}")
    print(f"  Active Agents: {coord_stats['active_agents']}")
    print(f"  Avg Response Time: {coord_stats['average_response_time']:.1f}ms")
    
    input("\nPress Enter to trigger coordination scenarios...")
    
    print("\nStep 2: Triggering Agent Coordination")
    print("-" * 30)
    
    # Scenario 1: Medium threat escalation
    print("\n🔶 Scenario 1: Medium Threat (Level 5)")
    message1 = {
        "type": "threat_escalation",
        "threat_id": f"demo_threat_medium_{int(time.time())}",
        "level": 5,
        "source": "demo_system"
    }
    
    await coordinator.send_coordination_message(message1)
    
    await asyncio.sleep(0.5)
    
    # Show updated status
    updated_status = coordinator.get_agent_status()
    active_agents_now = updated_status['coordination_stats']['active_agents']
    print(f"📊 Active agents after response: {active_agents_now}")
    
    input("\nPress Enter for high-severity threat...")
    
    # Scenario 2: High threat escalation
    print("\n🔴 Scenario 2: High Threat (Level 9)")
    message2 = {
        "type": "threat_escalation", 
        "threat_id": f"demo_threat_critical_{int(time.time())}",
        "level": 9,
        "source": "demo_system"
    }
    
    await coordinator.send_coordination_message(message2)
    
    await asyncio.sleep(0.5)
    
    # Show full agent response
    print("\nStep 3: Agent Response Analysis")
    print("-" * 30)
    
    final_status = coordinator.get_agent_status()
    
    for role, agents in final_status['agents_by_role'].items():
        print(f"\n  {role.title()} Agents:")
        for agent in agents:
            status_color = {
                'idle': 'Idle',
                'active': '🟢 ACTIVE',
                'busy': '🟡 BUSY', 
                'error': '🔴 ERROR'
            }.get(agent['status'], agent['status'])
            
            workload = f"{agent['workload']}/{agent['max_workload']}"
            current_task = agent['current_task'] or 'None'
            
            print(f"    Agent: {status_color}")
            print(f"      Workload: {workload}")
            print(f"      Current Task: {current_task}")
            print(f"      Threats Processed: {agent['processed_threats']}")
            print(f"      Success Rate: {agent['success_rate']:.1%}")
    
    input("\nPress Enter for inter-agent coordination...")
    
    print("\nStep 4: Inter-Agent Coordination")
    print("-" * 30)
    
    # Scenario 3: Help request
    print("\n🤝 Agent Help Request")
    help_message = {
        "type": "agent_request_help",
        "agent_id": "demo_agent_001",
        "capability": "quantum_analysis",
        "urgency": "high"
    }
    
    await coordinator.send_coordination_message(help_message)
    
    # Scenario 4: Resource request
    print("\n📊 Resource Allocation Request")
    resource_message = {
        "type": "resource_request",
        "agent_id": "demo_agent_002", 
        "resource": "processing_power"
    }
    
    await coordinator.send_coordination_message(resource_message)
    
    # Final statistics
    print("\nStep 5: Final Coordination Statistics")
    print("-" * 30)
    
    final_stats = coordinator.get_agent_status()['coordination_stats']
    
    print(f"📈 Coordination Summary:")
    print(f"  Total Coordinations: {final_stats['total_coordinations']}")
    print(f"  Successful Defenses: {final_stats['successful_defenses']}")
    print(f"  Failed Defenses: {final_stats['failed_defenses']}")
    print(f"  Active Agents: {final_stats['active_agents']}")
    print(f"  Average Response Time: {final_stats['average_response_time']:.1f}ms")
    print(f"  Success Rate: {(final_stats['successful_defenses'] / max(1, final_stats['total_coordinations']) * 100):.1f}%")
    
    await coordinator.stop_coordination()
    
    print("\n✅ Agent coordination demonstration completed!")
    print("🤖 All agents returned to standby mode")


if __name__ == "__main__":
    print("MWRASP Agent Coordination System Demo")
    print("=" * 50)
    print("This demonstrates the autonomous defense agent network")
    print("with real-time coordination and response capabilities.\n")
    
    try:
        asyncio.run(demo_agent_coordination())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")
    
    print("\nDemo completed. Thank you!")
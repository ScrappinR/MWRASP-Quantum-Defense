import asyncio
import time
import secrets
import json
import threading
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
from collections import defaultdict, deque

from .quantum_detector import QuantumDetector, ThreatLevel, QuantumThreat
from .temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
from .ai_learning_engine import AILearningEngine, Experience, get_learning_engine

# Import new patent implementations
try:
    from .personality_based_encryption import PersonalityKeyDerivation
    from .behavioral_quantum_signatures import BehavioralQuantumSignatures, apply_behavioral_modifications_to_agent
    PATENT_EXTENSIONS_AVAILABLE = True
except ImportError:
    PATENT_EXTENSIONS_AVAILABLE = False


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
    OFFLINE = "offline"


@dataclass
class AgentCapability:
    capability_id: str
    name: str
    processing_time_ms: int
    resource_cost: int
    quantum_resistant: bool = True


@dataclass
class DefenseAction:
    action_id: str
    agent_id: str
    action_type: str
    target: str
    parameters: Dict[str, Any]
    created_at: float
    executed_at: Optional[float] = None
    success: bool = False
    response_time_ms: Optional[float] = None


@dataclass
class Agent:
    agent_id: str
    role: AgentRole
    status: AgentStatus
    capabilities: List[AgentCapability]
    created_at: float
    last_active: float
    processed_threats: int = 0
    success_rate: float = 1.0
    current_task: Optional[str] = None
    workload: int = 0
    max_workload: int = 10
    
    # AI Learning enhancements
    learning_enabled: bool = True
    adaptation_level: str = "moderate"
    specialization_areas: List[str] = field(default_factory=list)
    learned_patterns: List[str] = field(default_factory=list)
    knowledge_confidence: float = 0.5
    learning_rate: float = 0.01
    experience_count: int = 0


class AutonomousDefenseCoordinator:
    def __init__(self, quantum_detector: QuantumDetector, fragmentation_system: TemporalFragmentation):
        self.quantum_detector = quantum_detector
        self.fragmentation_system = fragmentation_system
        self.agents: Dict[str, Agent] = {}
        self.defense_actions: List[DefenseAction] = []
        self.coordination_network = defaultdict(list)
        self.message_queue = asyncio.Queue()
        self.running = False
        self.coordination_task = None
        
        # AI Learning integration
        self.learning_engine = get_learning_engine()
        self.customer_id = "default"  # Can be configured per deployment
        
        # Patent implementations integration
        self.personality_encryption = None
        self.behavioral_signatures = None
        if PATENT_EXTENSIONS_AVAILABLE:
            self.personality_encryption = PersonalityKeyDerivation(quantum_safe=True)
            self.behavioral_signatures = BehavioralQuantumSignatures(quantum_detector)
            self.behavioral_signatures.start_behavioral_monitoring()
        
        # Initialize default agents
        self._initialize_agent_fleet()
        
        # Coordination metrics
        self.coordination_stats = {
            'total_coordinations': 0,
            'successful_defenses': 0,
            'failed_defenses': 0,
            'average_response_time': 0.0,
            'active_agents': 0
        }
    
    def _initialize_agent_fleet(self):
        """Initialize the autonomous defense agent fleet"""
        current_time = time.time()
        
        # Monitor Agent - Continuous surveillance
        monitor_capabilities = [
            AgentCapability("scan_canary", "Canary Token Scanning", 10, 1),
            AgentCapability("pattern_analysis", "Pattern Analysis", 50, 3),
            AgentCapability("threat_detection", "Threat Detection", 30, 2)
        ]
        
        monitor_agent = Agent(
            agent_id=f"monitor_{secrets.token_hex(4)}",
            role=AgentRole.MONITOR,
            status=AgentStatus.ACTIVE,
            capabilities=monitor_capabilities,
            created_at=current_time,
            last_active=current_time,
            max_workload=15
        )
        self.agents[monitor_agent.agent_id] = monitor_agent
        
        # Defender Agents - Active threat response
        for i in range(3):
            defender_capabilities = [
                AgentCapability("isolate_threat", "Threat Isolation", 20, 2),
                AgentCapability("fragment_data", "Emergency Fragmentation", 100, 5),
                AgentCapability("counter_attack", "Quantum Counter-Attack", 200, 8)
            ]
            
            defender_agent = Agent(
                agent_id=f"defender_{i}_{secrets.token_hex(4)}",
                role=AgentRole.DEFENDER,
                status=AgentStatus.IDLE,
                capabilities=defender_capabilities,
                created_at=current_time,
                last_active=current_time,
                max_workload=8
            )
            self.agents[defender_agent.agent_id] = defender_agent
        
        # Analyzer Agent - Deep threat analysis
        analyzer_capabilities = [
            AgentCapability("quantum_analysis", "Quantum Threat Analysis", 500, 10),
            AgentCapability("pattern_learning", "Pattern Learning", 300, 7),
            AgentCapability("vulnerability_assessment", "Vulnerability Assessment", 400, 8)
        ]
        
        analyzer_agent = Agent(
            agent_id=f"analyzer_{secrets.token_hex(4)}",
            role=AgentRole.ANALYZER,
            status=AgentStatus.IDLE,
            capabilities=analyzer_capabilities,
            created_at=current_time,
            last_active=current_time,
            max_workload=5
        )
        self.agents[analyzer_agent.agent_id] = analyzer_agent
        
        # Recovery Agent - System recovery
        recovery_capabilities = [
            AgentCapability("data_recovery", "Data Recovery", 1000, 15),
            AgentCapability("system_repair", "System Repair", 2000, 20),
            AgentCapability("integrity_restore", "Integrity Restoration", 800, 12)
        ]
        
        recovery_agent = Agent(
            agent_id=f"recovery_{secrets.token_hex(4)}",
            role=AgentRole.RECOVERY,
            status=AgentStatus.IDLE,
            capabilities=recovery_capabilities,
            created_at=current_time,
            last_active=current_time,
            max_workload=3
        )
        self.agents[recovery_agent.agent_id] = recovery_agent
        
        # Register agents with patent systems if available
        if PATENT_EXTENSIONS_AVAILABLE and self.behavioral_signatures:
            for agent_id in self.agents.keys():
                self.behavioral_signatures.register_agent(agent_id)
        
        # Coordinator Agent - Overall coordination
        coordinator_capabilities = [
            AgentCapability("threat_prioritization", "Threat Prioritization", 50, 3),
            AgentCapability("resource_allocation", "Resource Allocation", 100, 5),
            AgentCapability("strategy_optimization", "Strategy Optimization", 200, 8)
        ]
        
        coordinator_agent = Agent(
            agent_id=f"coordinator_{secrets.token_hex(4)}",
            role=AgentRole.COORDINATOR,
            status=AgentStatus.ACTIVE,
            capabilities=coordinator_capabilities,
            created_at=current_time,
            last_active=current_time,
            max_workload=20
        )
        self.agents[coordinator_agent.agent_id] = coordinator_agent
    
    async def start_coordination(self):
        """Start the autonomous coordination system"""
        if self.running:
            return
        
        self.running = True
        self.coordination_task = asyncio.create_task(self._coordination_loop())
        
        # Start quantum detector monitoring
        self.quantum_detector.start_monitoring()
        
        # Start fragmentation cleanup
        self.fragmentation_system.start_cleanup_service()
        
        print("MWRASP Autonomous Defense System activated")
    
    async def stop_coordination(self):
        """Stop the coordination system"""
        self.running = False
        
        if self.coordination_task:
            self.coordination_task.cancel()
            try:
                await self.coordination_task
            except asyncio.CancelledError:
                pass
        
        self.quantum_detector.stop_monitoring()
        self.fragmentation_system.stop_cleanup_service()
        
        # Set all agents to offline
        for agent in self.agents.values():
            agent.status = AgentStatus.OFFLINE
    
    async def _coordination_loop(self):
        """Main coordination loop for autonomous defense"""
        while self.running:
            try:
                # Check for active quantum threats
                active_threats = self.quantum_detector.get_active_threats()
                
                if active_threats:
                    await self._coordinate_threat_response(active_threats)
                
                # Monitor agent health
                await self._monitor_agent_health()
                
                # Process coordination messages
                await self._process_coordination_messages()
                
                # Update coordination statistics
                self._update_coordination_stats()
                
                await asyncio.sleep(0.05)  # 50ms coordination cycle
                
            except Exception as e:
                print(f"Coordination error: {e}")
                await asyncio.sleep(0.1)
    
    async def _coordinate_threat_response(self, threats: List[QuantumThreat]):
        """Coordinate autonomous response to quantum threats"""
        for threat in threats:
            # Prioritize threats
            priority_score = self._calculate_threat_priority(threat)
            
            # Select appropriate agents for response
            response_agents = await self._select_response_agents(threat, priority_score)
            
            if response_agents:
                # Coordinate multi-agent response
                await self._execute_coordinated_response(threat, response_agents)
    
    def _calculate_threat_priority(self, threat: QuantumThreat) -> float:
        """Calculate threat priority for resource allocation"""
        base_priority = {
            ThreatLevel.LOW: 1.0,
            ThreatLevel.MEDIUM: 3.0,
            ThreatLevel.HIGH: 7.0,
            ThreatLevel.CRITICAL: 10.0
        }[threat.threat_level]
        
        # Adjust based on confidence score
        confidence_multiplier = threat.confidence_score
        
        # Adjust based on affected systems
        system_multiplier = len(threat.affected_tokens) / 10.0
        
        # Time decay - older threats get lower priority
        time_factor = max(0.1, 1.0 - (time.time() - threat.detection_time) / 300.0)
        
        return base_priority * confidence_multiplier * (1 + system_multiplier) * time_factor
    
    async def _select_response_agents(self, threat: QuantumThreat, priority: float) -> List[Agent]:
        """AI-enhanced agent selection for threat response"""
        available_agents = [
            agent for agent in self.agents.values()
            if agent.status in [AgentStatus.IDLE, AgentStatus.ACTIVE]
            and agent.workload < agent.max_workload
        ]
        
        # Try AI-based selection first
        ai_recommendation = await self._get_ai_agent_recommendation(threat, priority, available_agents)
        if ai_recommendation:
            return ai_recommendation
        
        # Fallback to traditional rule-based selection
        selected_agents = []
        
        # AI-enhanced coordinator selection (prefer high success rate)
        if priority >= 5.0:
            coordinators = [a for a in available_agents if a.role == AgentRole.COORDINATOR]
            if coordinators:
                # Select coordinator with highest success rate and relevant specialization
                best_coordinator = max(coordinators, 
                                     key=lambda a: a.success_rate * (1.0 + len(a.specialization_areas) * 0.1))
                selected_agents.append(best_coordinator)
        
        # AI-enhanced defender selection
        defenders = [a for a in available_agents if a.role == AgentRole.DEFENDER]
        num_defenders = min(2 if priority >= 7.0 else 1, len(defenders))
        if defenders:
            # Sort by success rate and specialization match
            threat_type = threat.attack_vector if hasattr(threat, 'attack_vector') else 'unknown'
            defenders.sort(key=lambda a: (
                a.success_rate,
                1.0 if threat_type in a.specialization_areas else 0.5,
                -a.workload  # Prefer less busy agents
            ), reverse=True)
            selected_agents.extend(defenders[:num_defenders])
        
        # AI-enhanced analyzer selection for complex threats
        if threat.confidence_score >= 0.8 or len(threat.quantum_indicators) >= 3:
            analyzers = [a for a in available_agents if a.role == AgentRole.ANALYZER]
            if analyzers:
                # Select analyzer with best pattern recognition for this threat type
                best_analyzer = max(analyzers,
                                  key=lambda a: (
                                      a.success_rate,
                                      a.knowledge_confidence,
                                      len([p for p in a.learned_patterns if 'quantum' in p])
                                  ))
                selected_agents.append(best_analyzer)
        
        return selected_agents
    
    async def _get_ai_agent_recommendation(self, threat: QuantumThreat, priority: float, available_agents: List[Agent]) -> Optional[List[Agent]]:
        """Get AI-based agent selection recommendation"""
        context = {
            'threat_level': threat.threat_level.value,
            'confidence_score': threat.confidence_score,
            'quantum_indicators': threat.quantum_indicators,
            'priority': priority,
            'available_agent_count': len(available_agents),
            'system_load': sum(a.workload for a in available_agents) / max(len(available_agents), 1),
            'customer_id': self.customer_id
        }
        
        # Get recommendations for each available agent
        agent_scores = []
        for agent in available_agents:
            recommendation = self.learning_engine.get_adaptive_recommendation(agent.agent_id, context)
            if recommendation:
                score = recommendation.get('selection_confidence', 0.5) * agent.success_rate
                agent_scores.append((agent, score))
        
        if not agent_scores:
            return None
        
        # Select top agents based on AI recommendation scores
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Ensure we have the right mix of roles
        selected_agents = []
        roles_needed = {AgentRole.COORDINATOR: 1 if priority >= 5.0 else 0,
                       AgentRole.DEFENDER: 2 if priority >= 7.0 else 1,
                       AgentRole.ANALYZER: 1 if threat.confidence_score >= 0.8 else 0}
        
        for agent, score in agent_scores:
            if roles_needed.get(agent.role, 0) > 0:
                selected_agents.append(agent)
                roles_needed[agent.role] -= 1
        
        return selected_agents if selected_agents else None
    
    async def _execute_coordinated_response(self, threat: QuantumThreat, agents: List[Agent]):
        """Execute coordinated multi-agent response"""
        response_start_time = time.time()
        
        # Create coordination plan
        coordination_plan = self._create_coordination_plan(threat, agents)
        
        # Execute plan phases
        tasks = []
        for phase in coordination_plan:
            task = asyncio.create_task(self._execute_response_phase(phase))
            tasks.append(task)
        
        # Wait for all phases to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and create defense action record
        response_time = (time.time() - response_start_time) * 1000  # ms
        success = all(not isinstance(r, Exception) for r in results)
        
        action = DefenseAction(
            action_id=str(uuid.uuid4()),
            agent_id=",".join([a.agent_id for a in agents]),
            action_type="coordinated_quantum_defense",
            target=threat.threat_id,
            parameters={
                "threat_level": threat.threat_level.name,
                "agents_involved": len(agents),
                "quantum_indicators": threat.quantum_indicators
            },
            created_at=response_start_time,
            executed_at=time.time(),
            success=success,
            response_time_ms=response_time
        )
        
        self.defense_actions.append(action)
        
        # Update agent statistics and record learning experiences
        for agent in agents:
            agent.processed_threats += 1
            agent.experience_count += 1
            agent.last_active = time.time()
            if success:
                agent.success_rate = (agent.success_rate * (agent.processed_threats - 1) + 1.0) / agent.processed_threats
            else:
                agent.success_rate = (agent.success_rate * (agent.processed_threats - 1)) / agent.processed_threats
            
            # Record experience for AI learning
            if agent.learning_enabled:
                await self._record_agent_experience(agent, threat, action, success, response_time)
        
        self.coordination_stats['total_coordinations'] += 1
        if success:
            self.coordination_stats['successful_defenses'] += 1
        else:
            self.coordination_stats['failed_defenses'] += 1
    
    def _create_coordination_plan(self, threat: QuantumThreat, agents: List[Agent]) -> List[Dict]:
        """Create a multi-phase coordination plan"""
        plan = []
        
        # Phase 1: Immediate isolation
        isolation_phase = {
            "phase": "isolation",
            "agents": [a for a in agents if a.role == AgentRole.DEFENDER],
            "actions": ["isolate_threat", "fragment_data"],
            "timeout": 0.1  # 100ms
        }
        plan.append(isolation_phase)
        
        # Phase 2: Deep analysis (parallel with isolation)
        analysis_phase = {
            "phase": "analysis",
            "agents": [a for a in agents if a.role == AgentRole.ANALYZER],
            "actions": ["quantum_analysis", "pattern_learning"],
            "timeout": 0.5  # 500ms
        }
        plan.append(analysis_phase)
        
        # Phase 3: Coordinated counter-response
        if threat.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            counter_phase = {
                "phase": "counter_attack",
                "agents": agents,
                "actions": ["counter_attack", "system_repair"],
                "timeout": 1.0  # 1000ms
            }
            plan.append(counter_phase)
        
        return plan
    
    async def _execute_response_phase(self, phase: Dict) -> bool:
        """Execute a single phase of coordinated response"""
        try:
            phase_agents = phase["agents"]
            actions = phase["actions"]
            timeout = phase["timeout"]
            
            # Update agent workloads
            for agent in phase_agents:
                agent.workload += len(actions)
                agent.status = AgentStatus.BUSY
                agent.current_task = phase["phase"]
            
            # Simulate phase execution
            await asyncio.sleep(timeout)
            
            # Apply fragmentation system during isolation phase
            if phase["phase"] == "isolation":
                # Fragment any sensitive data that might be at risk
                for token_id in self.quantum_detector.canary_tokens.keys():
                    token_data = f"sensitive_data_{token_id}".encode()
                    self.fragmentation_system.fragment_data(token_data, f"token_{token_id}")
            
            # Reset agent status
            for agent in phase_agents:
                agent.workload = max(0, agent.workload - len(actions))
                agent.status = AgentStatus.ACTIVE if agent.workload > 0 else AgentStatus.IDLE
                agent.current_task = None
            
            return True
            
        except Exception as e:
            print(f"Phase execution error: {e}")
            return False
    
    async def _monitor_agent_health(self):
        """Monitor health and status of all agents"""
        current_time = time.time()
        
        for agent in self.agents.values():
            # Update heartbeat for idle agents to keep them active
            if agent.status == AgentStatus.IDLE and current_time - agent.last_active > 10.0:
                agent.last_active = current_time
            
            # Check for unresponsive agents
            if current_time - agent.last_active > 30.0:  # 30 seconds
                if agent.status != AgentStatus.ERROR:
                    agent.status = AgentStatus.ERROR
                    print(f"Agent {agent.agent_id} marked as unresponsive")
            
            # Apply behavioral modifications if patent systems available
            if PATENT_EXTENSIONS_AVAILABLE and self.behavioral_signatures:
                behavioral_state = self.behavioral_signatures.get_agent_behavioral_state(agent.agent_id)
                if behavioral_state:
                    signature = self.behavioral_signatures.agent_signatures.get(agent.agent_id)
                    if signature:
                        apply_behavioral_modifications_to_agent(agent, signature)
            
            # Auto-recover error state agents (more aggressive recovery)
            elif agent.status == AgentStatus.ERROR:
                # If the agent has had recent activity (heartbeat), recover immediately
                if current_time - agent.last_active <= 30.0:
                    agent.status = AgentStatus.IDLE
                    agent.workload = 0
                    agent.current_task = None
                    print(f"Agent {agent.agent_id} auto-recovered from error state")
                # Otherwise wait longer for recovery
                elif current_time - agent.last_active > 60.0:
                    agent.status = AgentStatus.IDLE
                    agent.workload = 0
                    agent.current_task = None
                    print(f"Agent {agent.agent_id} auto-recovered after timeout")
    
    async def _process_coordination_messages(self):
        """Process inter-agent coordination messages"""
        try:
            while not self.message_queue.empty():
                message = await asyncio.wait_for(self.message_queue.get(), timeout=0.01)
                await self._handle_coordination_message(message)
        except asyncio.TimeoutError:
            pass  # No messages to process
    
    async def _handle_coordination_message(self, message: Dict):
        """Handle individual coordination message"""
        message_type = message.get("type")
        
        if message_type == "agent_request_help":
            await self._handle_help_request(message)
        elif message_type == "threat_escalation":
            await self._handle_threat_escalation(message)
        elif message_type == "resource_request":
            await self._handle_resource_request(message)
    
    async def _handle_help_request(self, message: Dict):
        """Handle agent help requests"""
        requesting_agent_id = message.get("agent_id")
        required_capability = message.get("capability")
        
        # Find available agents with the required capability
        available_agents = [
            agent for agent in self.agents.values()
            if agent.agent_id != requesting_agent_id
            and agent.status == AgentStatus.IDLE
            and any(cap.capability_id == required_capability for cap in agent.capabilities)
        ]
        
        if available_agents:
            helper_agent = available_agents[0]
            helper_agent.status = AgentStatus.ACTIVE
            helper_agent.workload += 1
            
            # Add coordination record
            self.coordination_network[requesting_agent_id].append(helper_agent.agent_id)
    
    async def _handle_threat_escalation(self, message: Dict):
        """Handle threat escalation messages"""
        threat_id = message.get("threat_id")
        escalation_level = message.get("level")
        
        # Create synthetic high-priority threat for escalated situations
        if escalation_level >= 8:
            # Activate all available defender agents
            defenders = [a for a in self.agents.values() if a.role == AgentRole.DEFENDER and a.status == AgentStatus.IDLE]
            for defender in defenders:
                defender.status = AgentStatus.ACTIVE
                defender.workload += 3
    
    async def _handle_resource_request(self, message: Dict):
        """Handle agent resource requests"""
        requesting_agent_id = message.get("agent_id")
        resource_type = message.get("resource")
        
        # Simple resource allocation logic
        if resource_type == "processing_power":
            # Reduce workload of other non-critical agents
            for agent in self.agents.values():
                if (agent.agent_id != requesting_agent_id and 
                    agent.role not in [AgentRole.COORDINATOR, AgentRole.MONITOR] and
                    agent.workload > 0):
                    agent.workload = max(0, agent.workload - 1)
    
    def encrypt_agent_communication(self, sender_id: str, receiver_id: str, message: Dict) -> Optional[Dict]:
        """Encrypt agent-to-agent communication using personality-based encryption"""
        if not PATENT_EXTENSIONS_AVAILABLE or not self.personality_encryption:
            return message
        
        try:
            # Serialize message
            message_bytes = json.dumps(message).encode('utf-8')
            
            # Encrypt with personality-based key
            encrypted_package = self.personality_encryption.encrypt_with_personality(
                message_bytes, sender_id, receiver_id
            )
            
            return {
                'type': 'encrypted_agent_message',
                'encrypted_data': encrypted_package,
                'sender': sender_id,
                'receiver': receiver_id,
                'timestamp': time.time()
            }
        except Exception as e:
            print(f"Encryption error: {e}")
            return message
    
    def decrypt_agent_communication(self, encrypted_message: Dict) -> Optional[Dict]:
        """Decrypt agent communication using personality-based encryption"""
        if not PATENT_EXTENSIONS_AVAILABLE or not self.personality_encryption:
            return encrypted_message
        
        try:
            encrypted_package = encrypted_message.get('encrypted_data')
            if not encrypted_package:
                return encrypted_message
            
            # Decrypt message
            decrypted_bytes = self.personality_encryption.decrypt_with_personality(encrypted_package)
            decrypted_message = json.loads(decrypted_bytes.decode('utf-8'))
            
            return decrypted_message
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_message
    
    async def _record_agent_experience(self, agent: Agent, threat: QuantumThreat, action: DefenseAction, success: bool, response_time: float):
        """Record agent experience for AI learning"""
        try:
            # Calculate effectiveness score based on multiple factors
            effectiveness_score = 1.0 if success else 0.0
            if success:
                # Bonus for fast response
                effectiveness_score += max(0.0, (2000 - response_time) / 2000) * 0.3
                # Bonus for low system impact
                effectiveness_score += (1.0 - agent.workload / agent.max_workload) * 0.2
            
            # Calculate novelty score based on threat characteristics
            novelty_score = 0.5  # Base novelty
            if hasattr(threat, 'quantum_indicators') and len(threat.quantum_indicators) > 3:
                novelty_score += 0.3
            if threat.confidence_score > 0.9:
                novelty_score += 0.2
            
            # Determine side effects
            side_effects = []
            if response_time > 1000:  # >1 second response time
                side_effects.append("slow_response")
            if agent.workload >= agent.max_workload * 0.8:
                side_effects.append("high_resource_usage")
            
            # Create experience record
            experience = Experience(
                experience_id=str(uuid.uuid4()),
                agent_id=agent.agent_id,
                timestamp=time.time(),
                
                # Context
                system_architecture={
                    "agent_count": len(self.agents),
                    "system_load": sum(a.workload for a in self.agents.values()),
                    "active_threats": len([a for a in self.defense_actions if time.time() - a.created_at < 300])
                },
                threat_characteristics={
                    "threat_level": threat.threat_level.value,
                    "confidence_score": threat.confidence_score,
                    "quantum_indicators": threat.quantum_indicators,
                    "threat_id": threat.threat_id
                },
                customer_profile={"customer_id": self.customer_id},
                
                # Action
                action_type=action.action_type,
                action_parameters=action.parameters,
                coordination_partners=[a.agent_id for a in self.agents.values() if a != agent and a.current_task == agent.current_task],
                
                # Outcome
                success=success,
                response_time_ms=response_time,
                effectiveness_score=min(1.0, effectiveness_score),
                side_effects=side_effects,
                
                # Learning metadata
                confidence=agent.knowledge_confidence,
                uncertainty=1.0 - agent.knowledge_confidence,
                novelty_score=min(1.0, novelty_score)
            )
            
            # Record experience in learning engine
            self.learning_engine.record_experience(experience)
            
            # Update agent's learning progress
            if success and effectiveness_score > 0.7:
                agent.knowledge_confidence = min(1.0, agent.knowledge_confidence + agent.learning_rate)
                # Potentially develop specialization
                threat_type = f"{threat.threat_level.value}_quantum"
                if threat_type not in agent.specialization_areas and agent.success_rate > 0.8:
                    agent.specialization_areas.append(threat_type)
            elif not success:
                agent.knowledge_confidence = max(0.1, agent.knowledge_confidence - agent.learning_rate * 0.5)
                
        except Exception as e:
            print(f"[AI-LEARNING] Error recording experience for {agent.agent_id}: {e}")
    
    def _update_coordination_stats(self):
        """Update coordination system statistics"""
        active_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.ACTIVE)
        self.coordination_stats['active_agents'] = active_agents
        
        if self.defense_actions:
            response_times = [action.response_time_ms for action in self.defense_actions if action.response_time_ms]
            if response_times:
                self.coordination_stats['average_response_time'] = sum(response_times) / len(response_times)
    
    async def send_coordination_message(self, message: Dict):
        """Send a message to the coordination system"""
        await self.message_queue.put(message)
    
    def get_agent_status(self) -> Dict:
        """Get comprehensive agent status information"""
        status_by_role = defaultdict(list)
        
        for agent in self.agents.values():
            status_by_role[agent.role.value].append({
                'agent_id': agent.agent_id,
                'status': agent.status.value,
                'workload': agent.workload,
                'max_workload': agent.max_workload,
                'processed_threats': agent.processed_threats,
                'success_rate': agent.success_rate,
                'current_task': agent.current_task
            })
        
        return {
            'agents_by_role': dict(status_by_role),
            'total_agents': len(self.agents),
            'coordination_stats': self.coordination_stats,
            'recent_actions': len([a for a in self.defense_actions if time.time() - a.created_at < 300]),
            'system_running': self.running
        }
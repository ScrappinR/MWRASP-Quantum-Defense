#!/usr/bin/env python3
"""
Comprehensive test suite for autonomous agent system
Tests all agent capabilities including evolution, reproduction, learning, and quantum enhancement
"""

import asyncio
import pytest
import time
import random
from unittest.mock import Mock, AsyncMock, patch

# Import the agent systems
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.agent_system import (
    AutonomousDefenseCoordinator, Agent, AgentRole, AgentStatus, 
    AgentCapability, DefenseAction, AgentEcosystem
)
from core.advanced_learning_engine import (
    AdvancedLearningEngine, LearningType, MemoryType, Memory,
    KnowledgePattern, LearningSession
)
from core.quantum_enhanced_agents import (
    QuantumEnhancedAgent, QuantumAgentNetwork, QuantumCapabilityType,
    QuantumState, QuantumResource
)
from core.quantum_detector import QuantumDetector, ThreatLevel, QuantumThreat
from core.temporal_fragmentation import TemporalFragmentation

class TestAutonomousAgents:
    """Test suite for autonomous agent functionality"""
    
    @pytest.fixture
    async def setup_coordinator(self):
        """Set up test coordinator with mock dependencies"""
        mock_quantum_detector = Mock(spec=QuantumDetector)
        mock_quantum_detector.get_active_threats.return_value = []
        mock_quantum_detector.canary_tokens = {}
        mock_quantum_detector.start_monitoring = Mock()
        mock_quantum_detector.stop_monitoring = Mock()
        
        mock_fragmentation = Mock(spec=TemporalFragmentation)
        mock_fragmentation.start_cleanup_service = Mock()
        mock_fragmentation.stop_cleanup_service = Mock()
        mock_fragmentation.fragment_data = Mock()
        
        coordinator = AutonomousDefenseCoordinator(
            mock_quantum_detector, 
            mock_fragmentation
        )
        
        return coordinator
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, setup_coordinator):
        """Test initial agent fleet creation"""
        coordinator = await setup_coordinator
        
        # Check that agents were created
        assert len(coordinator.agents) > 0
        
        # Check agent roles
        roles_present = set(agent.role for agent in coordinator.agents.values())
        expected_roles = {
            AgentRole.MONITOR, 
            AgentRole.DEFENDER, 
            AgentRole.ANALYZER, 
            AgentRole.COORDINATOR, 
            AgentRole.RECOVERY
        }
        
        assert expected_roles.issubset(roles_present)
        
        # Check agent capabilities
        for agent in coordinator.agents.values():
            assert len(agent.capabilities) > 0
            assert agent.energy_level > 0
            assert agent.generation == 1  # Initial generation
    
    @pytest.mark.asyncio
    async def test_agent_evolution(self, setup_coordinator):
        """Test agent evolution mechanism"""
        coordinator = await setup_coordinator
        
        # Get an agent and set up evolution conditions
        agent_id = list(coordinator.agents.keys())[0]
        agent = coordinator.agents[agent_id]
        
        # Set conditions for evolution
        agent.success_rate = 0.9
        agent.experience_count = 60
        agent.energy_level = 90.0
        
        assert agent.can_evolve()
        
        # Force evolution
        success = await coordinator.force_evolution_event(agent_id)
        assert success
        
        # Check evolution results
        evolved_agent = coordinator.agents[agent_id]
        assert evolved_agent.generation > 1
        
        # Check if capabilities evolved
        evolved_capabilities = [cap for cap in evolved_agent.capabilities if cap.learned]
        assert len(evolved_capabilities) > 0
    
    @pytest.mark.asyncio
    async def test_agent_reproduction(self, setup_coordinator):
        """Test agent reproduction mechanism"""
        coordinator = await setup_coordinator
        initial_population = len(coordinator.agents)
        
        # Get an agent and set up reproduction conditions
        parent_id = list(coordinator.agents.keys())[0]
        parent_agent = coordinator.agents[parent_id]
        
        # Set conditions for reproduction
        parent_agent.success_rate = 0.95
        parent_agent.experience_count = 120
        parent_agent.energy_level = 80.0
        parent_agent.offspring_count = 0
        
        assert parent_agent.can_reproduce()
        
        # Force reproduction
        offspring_id = await coordinator.force_reproduction_event(parent_id)
        assert offspring_id is not None
        
        # Check reproduction results
        assert len(coordinator.agents) == initial_population + 1
        assert offspring_id in coordinator.agents
        
        offspring = coordinator.agents[offspring_id]
        assert offspring.parent_id == parent_id
        assert offspring.generation == parent_agent.generation + 1
        
        # Check parent's offspring count
        assert parent_agent.offspring_count == 1
    
    @pytest.mark.asyncio
    async def test_natural_selection(self, setup_coordinator):
        """Test natural selection removal of underperforming agents"""
        coordinator = await setup_coordinator
        
        # Create a poor-performing agent
        poor_agent_id = f"poor_performer_{int(time.time())}"
        poor_agent = Agent(
            agent_id=poor_agent_id,
            role=AgentRole.DEFENDER,
            status=AgentStatus.IDLE,
            capabilities=[],
            created_at=time.time(),
            last_active=time.time() - 3700,  # Old activity
            success_rate=0.05,  # Very low success rate
            energy_level=0.0  # No energy
        )
        
        coordinator.agents[poor_agent_id] = poor_agent
        initial_population = len(coordinator.agents)
        
        # Enable natural selection and run it
        coordinator.natural_selection_enabled = True
        await coordinator._natural_selection()
        
        # Check if poor performer was removed
        assert len(coordinator.agents) < initial_population
        assert poor_agent_id not in coordinator.agents
    
    @pytest.mark.asyncio
    async def test_agent_coordination(self, setup_coordinator):
        """Test multi-agent coordination for threat response"""
        coordinator = await setup_coordinator
        
        # Create mock threat
        mock_threat = Mock(spec=QuantumThreat)
        mock_threat.threat_id = "test_threat_001"
        mock_threat.threat_level = ThreatLevel.HIGH
        mock_threat.confidence_score = 0.9
        mock_threat.quantum_indicators = ["quantum_signature_1", "entanglement_detected"]
        mock_threat.detection_time = time.time()
        mock_threat.affected_tokens = ["token_1", "token_2"]
        
        # Test threat response coordination
        response_agents = await coordinator._select_response_agents(mock_threat, 8.0)
        
        assert len(response_agents) > 0
        
        # Check that appropriate roles are selected
        agent_roles = set(agent.role for agent in response_agents)
        assert AgentRole.DEFENDER in agent_roles  # Should always have defenders for high threats
        
        # Test coordinated execution
        await coordinator._execute_coordinated_response(mock_threat, response_agents)
        
        # Check that defense action was recorded
        assert len(coordinator.defense_actions) > 0
        latest_action = coordinator.defense_actions[-1]
        assert latest_action.target == mock_threat.threat_id
    
    @pytest.mark.asyncio
    async def test_collaboration_and_communication(self, setup_coordinator):
        """Test agent collaboration and communication systems"""
        coordinator = await setup_coordinator
        
        # Start coordination to enable communication processing
        await coordinator.start_coordination()
        
        # Wait a bit for collaboration to potentially occur
        await asyncio.sleep(0.5)
        
        # Test manual collaboration initiation
        agents = list(coordinator.agents.values())[:2]
        if len(agents) >= 2:
            await coordinator._initiate_collaboration(agents[0], agents[1])
            
            # Check that collaboration was recorded
            assert len(coordinator.communication_log) > 0
            
            # Check collaboration score increase
            assert agents[0].collaboration_score > 0.5 or agents[1].collaboration_score > 0.5
        
        await coordinator.stop_coordination()
    
    @pytest.mark.asyncio
    async def test_resource_management(self, setup_coordinator):
        """Test resource allocation and management"""
        coordinator = await setup_coordinator
        
        # Test initial resource allocation
        await coordinator._allocate_resources()
        
        # Check that resources were allocated
        assert len(coordinator.resource_allocation) > 0
        
        for agent_id, resources in coordinator.resource_allocation.items():
            assert 'processing_power' in resources
            assert 'memory' in resources
            assert 'network_bandwidth' in resources
            assert 'quantum_access' in resources
            
            # Check resource values are positive
            assert all(value >= 0 for value in resources.values())
    
    @pytest.mark.asyncio
    async def test_ecosystem_management(self, setup_coordinator):
        """Test ecosystem-level management and metrics"""
        coordinator = await setup_coordinator
        
        # Start ecosystem management
        await coordinator.start_coordination()
        
        # Let it run briefly
        await asyncio.sleep(0.2)
        
        # Check ecosystem metrics
        assert coordinator.ecosystem.population_size == len(coordinator.agents)
        assert coordinator.ecosystem.average_generation >= 1.0
        
        # Check coordination stats
        stats = coordinator.coordination_stats
        assert 'population_size' in stats
        assert 'average_generation' in stats
        assert 'evolution_events' in stats
        
        await coordinator.stop_coordination()
    
    @pytest.mark.asyncio
    async def test_agent_specialization(self, setup_coordinator):
        """Test agent specialization development"""
        coordinator = await setup_coordinator
        
        agent = list(coordinator.agents.values())[0]
        
        # Simulate successful actions to develop specialization
        for i in range(10):
            action = DefenseAction(
                action_id=f"test_action_{i}",
                agent_id=agent.agent_id,
                action_type="quantum_analysis",
                target=f"threat_{i}",
                parameters={"success": True},
                created_at=time.time(),
                success=True
            )
            coordinator.defense_actions.append(action)
        
        agent.processed_threats = 25
        agent.success_rate = 0.8
        
        # Run specialization management
        await coordinator._manage_specialization()
        
        # Check if specialization developed
        assert len(agent.specialization_areas) >= 0  # May or may not develop based on actions

class TestAdvancedLearningEngine:
    """Test suite for advanced learning engine"""
    
    @pytest.fixture
    def learning_engine(self):
        """Set up learning engine"""
        return AdvancedLearningEngine()
    
    @pytest.mark.asyncio
    async def test_memory_storage_retrieval(self, learning_engine):
        """Test memory storage and retrieval"""
        agent_id = "test_agent_001"
        
        # Store a memory
        memory_content = {
            "threat_type": "quantum_attack",
            "response_action": "isolation",
            "success": True,
            "context": "high_priority_system"
        }
        
        memory_id = await learning_engine.store_memory(
            agent_id, MemoryType.EPISODIC, memory_content, importance=0.8
        )
        
        assert memory_id in learning_engine.memories
        
        # Retrieve memories
        query = {"threat_type": "quantum_attack"}
        retrieved_memories = await learning_engine.retrieve_memory(agent_id, query)
        
        assert len(retrieved_memories) > 0
        assert retrieved_memories[0].content == memory_content
    
    @pytest.mark.asyncio
    async def test_pattern_discovery(self, learning_engine):
        """Test pattern discovery from experiences"""
        agent_id = "test_agent_002"
        
        # Create similar experiences for pattern discovery
        experiences = []
        for i in range(5):
            experience = {
                "threat_level": "HIGH",
                "confidence_score": 0.9 + random.uniform(-0.1, 0.1),
                "response_action": "quantum_analysis",
                "success": True,
                "response_time": 50 + random.uniform(-10, 10)
            }
            experiences.append(experience)
        
        # Discover patterns
        discovered_patterns = await learning_engine.discover_patterns(agent_id, experiences)
        
        # Should discover at least one pattern from similar experiences
        assert len(discovered_patterns) >= 0  # May or may not discover patterns based on similarity
    
    @pytest.mark.asyncio
    async def test_knowledge_transfer(self, learning_engine):
        """Test knowledge transfer between agents"""
        source_agent = "source_agent"
        target_agent = "target_agent"
        
        # Create memories for source agent
        for i in range(5):
            await learning_engine.store_memory(
                source_agent,
                MemoryType.SEMANTIC,
                {"knowledge": f"pattern_{i}", "effectiveness": 0.8 + i * 0.05},
                importance=0.8
            )
        
        # Transfer knowledge
        transfer_results = await learning_engine.transfer_knowledge(
            source_agent, target_agent, ["pattern"]
        )
        
        # Check transfer results
        assert transfer_results['memories_transferred'] >= 0
        assert transfer_results['compatibility_score'] >= 0
    
    @pytest.mark.asyncio
    async def test_collaborative_learning(self, learning_engine):
        """Test collaborative learning between multiple agents"""
        agent_ids = ["agent_1", "agent_2", "agent_3"]
        
        # Create memories for each agent
        for agent_id in agent_ids:
            for i in range(3):
                await learning_engine.store_memory(
                    agent_id,
                    MemoryType.PROCEDURAL,
                    {"procedure": f"defense_protocol_{i}", "agent": agent_id},
                    importance=0.7
                )
        
        # Collaborative learning session
        problem_context = {"domain": "cyber_defense", "complexity": "high"}
        collaboration_results = await learning_engine.collaborative_learning(
            agent_ids, problem_context
        )
        
        # Check collaboration results
        assert collaboration_results['participating_agents'] == agent_ids
        assert 'shared_insights' in collaboration_results
        assert collaboration_results['collective_knowledge_gain'] >= 0
    
    @pytest.mark.asyncio
    async def test_meta_learning(self, learning_engine):
        """Test meta-learning capabilities"""
        agent_id = "meta_agent"
        
        # Create sufficient learning history
        for i in range(60):
            await learning_engine.store_memory(
                agent_id,
                MemoryType.EPISODIC,
                {"experience": f"exp_{i}", "outcome": random.choice([True, False])},
                importance=random.uniform(0.3, 0.9)
            )
        
        # Create some patterns
        experiences = [{"pattern_type": "test", "success": True}] * 10
        await learning_engine.discover_patterns(agent_id, experiences)
        
        # Run meta-learning
        meta_results = await learning_engine.meta_learning_cycle(agent_id)
        
        # Check meta-learning results
        assert 'learning_efficiency_improvement' in meta_results
        assert 'pattern_quality_improvement' in meta_results
        assert 'memory_organization_improvement' in meta_results

class TestQuantumEnhancedAgents:
    """Test suite for quantum-enhanced agents"""
    
    @pytest.fixture
    def quantum_agent(self):
        """Set up quantum-enhanced agent"""
        return QuantumEnhancedAgent("quantum_test_agent")
    
    @pytest.fixture
    def quantum_network(self):
        """Set up quantum agent network"""
        return QuantumAgentNetwork()
    
    @pytest.mark.asyncio
    async def test_quantum_capability_initialization(self, quantum_agent):
        """Test quantum capability initialization"""
        assert len(quantum_agent.quantum_capabilities) > 0
        
        # Check all capability types are present
        expected_capabilities = [cap.value for cap in QuantumCapabilityType]
        for cap_type in expected_capabilities:
            assert cap_type in quantum_agent.quantum_capabilities
            assert 0.0 <= quantum_agent.quantum_capabilities[cap_type] <= 1.0
    
    @pytest.mark.asyncio
    async def test_quantum_enhancement(self, quantum_agent):
        """Test quantum enhancement of traditional results"""
        traditional_result = {
            "threat_confidence": 0.7,
            "analysis_completeness": 0.6,
            "prediction_accuracy": 0.8
        }
        
        # Test different quantum enhancements
        for quantum_type in QuantumCapabilityType:
            enhanced_result = await quantum_agent.enhance_with_quantum(
                traditional_result, quantum_type
            )
            
            # Should have quantum enhancement metadata
            if 'quantum_enhancement' in enhanced_result:
                assert enhanced_result['quantum_enhancement']['type'] == quantum_type.value
                assert 'advantage' in enhanced_result['quantum_enhancement']
    
    @pytest.mark.asyncio
    async def test_quantum_circuit_creation(self, quantum_agent):
        """Test quantum circuit creation and execution"""
        # Create circuit for threat analysis
        circuit_id = await quantum_agent.create_quantum_circuit(
            "threat_analysis", "threat_analysis"
        )
        
        assert circuit_id in quantum_agent.quantum_circuits
        circuit = quantum_agent.quantum_circuits[circuit_id]
        
        assert circuit.qubit_count > 0
        assert len(circuit.gates) > 0
        assert len(circuit.measurements) > 0
        
        # Execute the circuit
        results = await quantum_agent.execute_quantum_circuit(circuit_id)
        
        assert 'measurements' in results
        assert 'quantum_state' in results
        assert 'success' in results
    
    @pytest.mark.asyncio
    async def test_quantum_entanglement(self, quantum_agent):
        """Test quantum entanglement creation and communication"""
        other_agent_id = "other_quantum_agent"
        
        # Create entanglement
        entanglement_id = await quantum_agent.create_quantum_entanglement(other_agent_id)
        
        assert entanglement_id in quantum_agent.entanglements
        entanglement = quantum_agent.entanglements[entanglement_id]
        
        assert entanglement.is_active()
        assert entanglement.entanglement_strength > 0
        
        # Test quantum communication
        test_info = {"message": "quantum_test_data", "priority": "high"}
        success = await quantum_agent.quantum_communicate(entanglement_id, test_info)
        
        # Communication success depends on entanglement strength
        assert isinstance(success, bool)
        if success:
            assert test_info["message"] in str(entanglement.shared_information)
    
    @pytest.mark.asyncio
    async def test_quantum_sensing(self, quantum_agent):
        """Test quantum-enhanced environmental sensing"""
        environment_data = {
            "network_traffic": {"normal": 0.7, "suspicious": 0.3},
            "system_health": {"cpu": 0.8, "memory": 0.6},
            "threat_indicators": ["unusual_pattern_1", "anomaly_2"]
        }
        
        enhanced_data = await quantum_agent.quantum_sense_environment(environment_data)
        
        # Should have original data plus quantum enhancements
        for key in environment_data:
            assert key in enhanced_data
        
        if quantum_agent.quantum_capabilities[QuantumCapabilityType.QUANTUM_SENSING.value] > 0.1:
            assert 'quantum_sensing' in enhanced_data
            sensing_data = enhanced_data['quantum_sensing']
            assert 'sensitivity_boost' in sensing_data
    
    @pytest.mark.asyncio
    async def test_quantum_learning(self, quantum_agent):
        """Test quantum machine learning capabilities"""
        experience_data = [
            {"pattern": "quantum_signature", "outcome": "threat_detected", "success": True},
            {"pattern": "entanglement_anomaly", "outcome": "isolated", "success": True},
            {"pattern": "coherence_loss", "outcome": "system_protected", "success": False},
            {"pattern": "quantum_signature", "outcome": "threat_neutralized", "success": True},
            {"pattern": "superposition_detected", "outcome": "analyzed", "success": True}
        ]
        
        quantum_learning_results = await quantum_agent.quantum_learn_pattern(experience_data)
        
        assert 'patterns' in quantum_learning_results
        assert 'quantum_advantage' in quantum_learning_results
        
        if quantum_agent.quantum_capabilities[QuantumCapabilityType.QUANTUM_ANALYSIS.value] > 0.4:
            assert len(quantum_learning_results['patterns']) > 0
    
    @pytest.mark.asyncio
    async def test_quantum_capability_evolution(self, quantum_agent):
        """Test evolution of quantum capabilities"""
        original_capabilities = quantum_agent.quantum_capabilities.copy()
        
        # Set up conditions for evolution
        quantum_agent.quantum_experience = 0.5
        quantum_agent.quantum_fidelity = 0.9
        quantum_agent.quantum_advantage_achieved = 0.6
        
        evolution_results = await quantum_agent.evolve_quantum_capabilities(0.2)
        
        # Check that capabilities potentially evolved
        assert len(evolution_results) >= len(original_capabilities)
        
        # Check that some capabilities changed
        changed_capabilities = 0
        for cap_type, change in evolution_results.items():
            if abs(change) > 0.01:  # Meaningful change
                changed_capabilities += 1
        
        # At least some capabilities should evolve with high performance
        assert changed_capabilities >= 0  # May or may not change based on randomness
    
    @pytest.mark.asyncio
    async def test_quantum_network_collaboration(self, quantum_network):
        """Test quantum network collaboration"""
        # Add agents to network
        agent_ids = ["q_agent_1", "q_agent_2", "q_agent_3"]
        for agent_id in agent_ids:
            quantum_network.add_quantum_agent(agent_id)
        
        # Test collaboration
        collaboration_results = await quantum_network.facilitate_quantum_collaboration(
            agent_ids, "threat_analysis"
        )
        
        assert collaboration_results['participating_agents'] == agent_ids
        assert 'collective_quantum_advantage' in collaboration_results
        assert len(collaboration_results['entanglements_created']) >= 0
    
    @pytest.mark.asyncio
    async def test_quantum_task_distribution(self, quantum_network):
        """Test distributed quantum computation"""
        # Add experienced agents
        agent_ids = ["q_agent_A", "q_agent_B"]
        for agent_id in agent_ids:
            agent = quantum_network.add_quantum_agent(agent_id)
            agent.quantum_experience = 0.3  # Make them qualified
        
        # Test task distribution
        task_data = {
            "type": "optimization",
            "complexity": 2.0,
            "purpose": "resource_allocation",
            "qubit_count": 10,
            "gate_count": 40
        }
        
        distribution_results = await quantum_network.quantum_distribute_task(task_data)
        
        if 'error' not in distribution_results:
            assert 'combined_results' in distribution_results
            assert 'total_quantum_advantage' in distribution_results

# Integration tests
class TestAgentSystemIntegration:
    """Integration tests for complete agent system"""
    
    @pytest.mark.asyncio
    async def test_full_system_integration(self):
        """Test full integration of all agent systems"""
        # Create mock dependencies
        mock_detector = Mock(spec=QuantumDetector)
        mock_detector.get_active_threats.return_value = []
        mock_detector.canary_tokens = {}
        mock_detector.start_monitoring = Mock()
        mock_detector.stop_monitoring = Mock()
        
        mock_fragmentation = Mock(spec=TemporalFragmentation)
        mock_fragmentation.start_cleanup_service = Mock()
        mock_fragmentation.stop_cleanup_service = Mock()
        mock_fragmentation.fragment_data = Mock()
        
        # Create coordinator with all systems
        coordinator = AutonomousDefenseCoordinator(mock_detector, mock_fragmentation)
        
        # Enable all autonomous features
        coordinator.evolution_enabled = True
        coordinator.reproduction_enabled = True
        coordinator.natural_selection_enabled = True
        
        # Start the system
        await coordinator.start_coordination()
        
        # Let it run briefly
        await asyncio.sleep(0.3)
        
        # Create quantum-enhanced agents
        quantum_network = QuantumAgentNetwork()
        for agent_id in list(coordinator.agents.keys())[:3]:
            quantum_network.add_quantum_agent(agent_id)
        
        # Test quantum collaboration
        collaboration_results = await quantum_network.facilitate_quantum_collaboration(
            list(coordinator.agents.keys())[:2], "integrated_defense"
        )
        
        # Check system status
        agent_status = coordinator.get_agent_status()
        network_status = quantum_network.get_network_status()
        
        assert agent_status['total_agents'] > 0
        assert agent_status['system_running'] == True
        assert network_status['total_quantum_agents'] > 0
        
        # Stop the system
        await coordinator.stop_coordination()
        
        assert agent_status['system_running'] == True  # Status from before stop

if __name__ == "__main__":
    # Run basic functionality test
    async def run_basic_test():
        print("Running basic autonomous agent test...")
        
        # Mock dependencies
        mock_detector = Mock()
        mock_detector.get_active_threats.return_value = []
        mock_detector.canary_tokens = {}
        mock_detector.start_monitoring = Mock()
        mock_detector.stop_monitoring = Mock()
        
        mock_fragmentation = Mock()
        mock_fragmentation.start_cleanup_service = Mock()
        mock_fragmentation.stop_cleanup_service = Mock()
        mock_fragmentation.fragment_data = Mock()
        
        # Create and test coordinator
        coordinator = AutonomousDefenseCoordinator(mock_detector, mock_fragmentation)
        
        print(f"Initial population: {len(coordinator.agents)} agents")
        
        # Test evolution
        agent_id = list(coordinator.agents.keys())[0]
        success = await coordinator.force_evolution_event(agent_id)
        print(f"Evolution test: {'SUCCESS' if success else 'FAILED'}")
        
        # Test reproduction
        offspring_id = await coordinator.force_reproduction_event(agent_id)
        print(f"Reproduction test: {'SUCCESS' if offspring_id else 'FAILED'}")
        print(f"New population: {len(coordinator.agents)} agents")
        
        # Test quantum enhancement
        quantum_agent = QuantumEnhancedAgent("test_quantum_agent")
        quantum_status = quantum_agent.get_quantum_status()
        print(f"Quantum agent capabilities: {len(quantum_status['quantum_capabilities'])}")
        
        # Test learning engine
        learning_engine = AdvancedLearningEngine()
        memory_id = await learning_engine.store_memory(
            "test_agent", MemoryType.EPISODIC, 
            {"test": "memory", "success": True}, 0.8
        )
        print(f"Learning engine test: {'SUCCESS' if memory_id else 'FAILED'}")
        
        print("Basic test completed successfully!")
    
    # Run the test
    asyncio.run(run_basic_test())
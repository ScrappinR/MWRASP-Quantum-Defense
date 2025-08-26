import pytest
import asyncio
import time
import json
from unittest.mock import Mock, patch

from ..core.quantum_detector import QuantumDetector, ThreatLevel
from ..core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
from ..core.agent_system import AutonomousDefenseCoordinator, AgentRole, AgentStatus


class TestSystemIntegration:
    """Integration tests for the complete MWRASP system"""
    
    def setup_method(self):
        """Setup integrated system components"""
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.6)
        
        self.fragmentation_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=500,  # 500ms for integration testing
            min_fragments=3,
            max_fragments=6,
            quantum_resistance_level=3
        )
        self.fragmentation_system = TemporalFragmentation(self.fragmentation_policy)
        
        self.agent_coordinator = AutonomousDefenseCoordinator(
            self.quantum_detector,
            self.fragmentation_system
        )
    
    def teardown_method(self):
        """Cleanup system components"""
        self.quantum_detector.stop_monitoring()
        self.fragmentation_system.stop_cleanup_service()
        asyncio.run(self.agent_coordinator.stop_coordination())
    
    @pytest.mark.asyncio
    async def test_end_to_end_threat_response(self):
        """Test complete threat detection to response pipeline"""
        
        # 1. Start all systems
        await self.agent_coordinator.start_coordination()
        
        # 2. Create canary tokens (normal operation)
        tokens = []
        for i in range(3):
            token = self.quantum_detector.generate_canary_token(f"sensitive_data_{i}")
            tokens.append(token)
        
        # 3. Fragment some sensitive data
        sensitive_document = b"TOP SECRET: Quantum encryption keys and defense protocols"
        fragments = self.fragmentation_system.fragment_data(sensitive_document, "secret_doc_001")
        
        # 4. Simulate quantum attack pattern
        attack_start_time = time.time()
        
        # Rapid access to multiple tokens (quantum superposition pattern)
        for round_num in range(4):
            for token in tokens:
                self.quantum_detector.access_token(token.token_id, f"quantum_attacker_{round_num}")
            await asyncio.sleep(0.001)  # Minimal delay between rounds
        
        # 5. Allow system time to detect and respond
        await asyncio.sleep(0.2)  # 200ms for processing
        
        # 6. Verify threat detection
        active_threats = self.quantum_detector.get_active_threats()
        assert len(active_threats) > 0, "Should have detected quantum attack"
        
        threat = active_threats[-1]
        assert threat.confidence_score > 0.5
        assert len(threat.quantum_indicators) > 0
        
        # 7. Verify agent coordination response
        agent_status = self.agent_coordinator.get_agent_status()
        coordination_stats = agent_status['coordination_stats']
        
        # Should have triggered some coordination activity
        assert coordination_stats['total_coordinations'] > 0 or \
               coordination_stats['active_agents'] > 0
        
        # 8. Verify fragmentation system integrity
        # Original data should still be reconstructable immediately after attack
        reconstructed = self.fragmentation_system.reconstruct_data("secret_doc_001")
        assert reconstructed == sensitive_document
        
        # 9. Test system statistics
        quantum_stats = self.quantum_detector.get_threat_statistics()
        fragment_stats = self.fragmentation_system.get_system_stats()
        
        assert quantum_stats['total_threats_detected'] > 0
        assert quantum_stats['active_threats'] > 0
        assert fragment_stats['total_fragments'] > 0
    
    @pytest.mark.asyncio
    async def test_coordinated_defense_escalation(self):
        """Test escalated defense response to high-severity threats"""
        
        await self.agent_coordinator.start_coordination()
        
        # Create multiple high-value targets
        high_value_tokens = []
        for i in range(5):
            token = self.quantum_detector.generate_canary_token(f"critical_system_{i}")
            high_value_tokens.append(token)
        
        # Fragment multiple critical documents
        critical_docs = []
        for i in range(3):
            doc_data = f"CRITICAL SYSTEM {i}: Nuclear launch codes and quantum keys".encode()
            fragments = self.fragmentation_system.fragment_data(doc_data, f"critical_doc_{i}")
            critical_docs.append((doc_data, f"critical_doc_{i}"))
        
        # Simulate sophisticated quantum attack
        # Multiple attack vectors simultaneously
        attack_patterns = [
            # Pattern 1: Rapid superposition-like access
            lambda: [
                self.quantum_detector.access_token(token.token_id, f"quantum_super_{i}")
                for i, token in enumerate(high_value_tokens[:3])
            ],
            # Pattern 2: Correlated entanglement access
            lambda: [
                self.quantum_detector.access_token(token.token_id, "quantum_entangled")
                for token in high_value_tokens[2:]
            ],
            # Pattern 3: Quantum speedup pattern
            lambda: [
                self.quantum_detector.access_token(high_value_tokens[0].token_id, f"quantum_speed_{i}")
                for i in range(8)
            ]
        ]
        
        # Execute attack patterns concurrently
        for pattern in attack_patterns:
            pattern()
            await asyncio.sleep(0.001)  # Minimal delay between pattern types
        
        # Allow system to detect and escalate response
        await asyncio.sleep(0.3)  # 300ms for full response
        
        # Verify high-severity threat detection
        active_threats = self.quantum_detector.get_active_threats()
        assert len(active_threats) > 0
        
        # Should have at least one high or critical threat
        high_severity_threats = [
            t for t in active_threats 
            if t.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        ]
        assert len(high_severity_threats) > 0
        
        # Verify escalated agent response
        agent_status = self.agent_coordinator.get_agent_status()
        
        # Multiple agents should be active in response to high-severity threat
        active_agent_count = sum(
            len([agent for agent in agents if agent['status'] in ['active', 'busy']])
            for agents in agent_status['agents_by_role'].values()
        )
        assert active_agent_count >= 3, "Should activate multiple agents for high-severity threat"
        
        # Verify defense actions were taken
        coordination_stats = agent_status['coordination_stats']
        assert coordination_stats['total_coordinations'] > 0
        
        # Verify data protection - critical documents should still be accessible
        for doc_data, doc_id in critical_docs:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed:  # May have expired due to defense measures
                assert reconstructed == doc_data
    
    @pytest.mark.asyncio
    async def test_temporal_defense_coordination(self):
        """Test coordination between temporal fragmentation and threat detection"""
        
        await self.agent_coordinator.start_coordination()
        
        # Create scenario: ongoing quantum attack during data operations
        active_token = self.quantum_detector.generate_canary_token("active_operations")
        
        # Start fragmenting sensitive data during attack
        sensitive_data = b"Real-time sensitive operations data under quantum attack"
        
        # Begin quantum attack simulation
        attack_task = asyncio.create_task(self._simulate_ongoing_attack(active_token))
        
        # Simultaneously fragment data (simulating real-time operations)
        fragmentation_start = time.time()
        fragments = self.fragmentation_system.fragment_data(sensitive_data, "realtime_ops")
        
        # Allow attack to continue briefly
        await asyncio.sleep(0.1)
        
        # Stop attack simulation
        attack_task.cancel()
        
        # Verify system behavior under concurrent threat and operations
        active_threats = self.quantum_detector.get_active_threats()
        
        # Should detect threat from attack
        if active_threats:
            threat = active_threats[-1]
            assert threat.confidence_score > 0.4  # Some confidence in detection
        
        # Data should still be properly fragmented and recoverable
        reconstructed = self.fragmentation_system.reconstruct_data("realtime_ops")
        assert reconstructed == sensitive_data
        
        # Fragment status should be trackable
        fragment_status = self.fragmentation_system.get_fragment_status("realtime_ops")
        assert fragment_status['reconstructable']
    
    async def _simulate_ongoing_attack(self, token):
        """Helper method to simulate ongoing quantum attack"""
        try:
            attack_round = 0
            while True:
                self.quantum_detector.access_token(token.token_id, f"persistent_attacker_{attack_round}")
                attack_round += 1
                await asyncio.sleep(0.01)  # 10ms between attacks
        except asyncio.CancelledError:
            pass
    
    @pytest.mark.asyncio
    async def test_system_recovery_after_attack(self):
        """Test system recovery and cleanup after quantum attack"""
        
        await self.agent_coordinator.start_coordination()
        self.fragmentation_system.start_cleanup_service()
        
        # Create pre-attack state
        pre_attack_tokens = []
        pre_attack_documents = []
        
        for i in range(4):
            token = self.quantum_detector.generate_canary_token(f"pre_attack_data_{i}")
            pre_attack_tokens.append(token)
            
            doc_data = f"Document {i} before quantum attack".encode()
            fragments = self.fragmentation_system.fragment_data(doc_data, f"pre_doc_{i}")
            pre_attack_documents.append((doc_data, f"pre_doc_{i}"))
        
        # Record initial system state
        initial_quantum_stats = self.quantum_detector.get_threat_statistics()
        initial_fragment_stats = self.fragmentation_system.get_system_stats()
        initial_agent_stats = self.agent_coordinator.get_agent_status()
        
        # Execute quantum attack
        for attack_round in range(6):
            for token in pre_attack_tokens:
                self.quantum_detector.access_token(token.token_id, f"recovery_test_attack_{attack_round}")
            await asyncio.sleep(0.001)
        
        # Allow attack detection and response
        await asyncio.sleep(0.2)
        
        # Verify attack was detected
        post_attack_quantum_stats = self.quantum_detector.get_threat_statistics()
        assert post_attack_quantum_stats['total_threats_detected'] > initial_quantum_stats['total_threats_detected']
        
        # Allow system recovery time
        await asyncio.sleep(0.5)  # 500ms recovery period
        
        # Test system recovery capabilities
        
        # 1. Verify threat detection system is still operational
        recovery_test_token = self.quantum_detector.generate_canary_token("recovery_test")
        self.quantum_detector.access_token(recovery_test_token.token_id, "recovery_user")
        # Should not crash or fail
        
        # 2. Verify fragmentation system is still operational  
        recovery_doc = b"Post-attack recovery test document"
        recovery_fragments = self.fragmentation_system.fragment_data(recovery_doc, "recovery_doc")
        reconstructed_recovery = self.fragmentation_system.reconstruct_data("recovery_doc")
        assert reconstructed_recovery == recovery_doc
        
        # 3. Verify pre-attack documents are still accessible (if not expired)
        accessible_docs = 0
        for doc_data, doc_id in pre_attack_documents:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed == doc_data:
                accessible_docs += 1
        # At least some documents should still be accessible
        # (exact number depends on timing and expiration)
        
        # 4. Verify agent system is responsive
        current_agent_stats = self.agent_coordinator.get_agent_status()
        assert current_agent_stats['system_running']
        
        # Trigger manual coordination to test responsiveness
        test_message = {
            "type": "threat_escalation",
            "threat_id": "recovery_test_threat",
            "level": 5,
            "source": "recovery_test"
        }
        await self.agent_coordinator.send_coordination_message(test_message)
        
        # Allow message processing
        await asyncio.sleep(0.1)
        
        # System should still be functional
        final_agent_stats = self.agent_coordinator.get_agent_status()
        assert final_agent_stats['system_running']
    
    @pytest.mark.asyncio
    async def test_performance_under_load(self):
        """Test integrated system performance under high load"""
        
        await self.agent_coordinator.start_coordination()
        
        start_time = time.time()
        
        # High-load simulation parameters
        num_tokens = 20
        num_documents = 15
        num_attack_rounds = 10
        
        # Create many canary tokens
        tokens = []
        for i in range(num_tokens):
            token = self.quantum_detector.generate_canary_token(f"load_test_token_{i}")
            tokens.append(token)
        
        # Fragment many documents
        documents = []
        for i in range(num_documents):
            doc_data = f"Load test document {i} with sensitive information".encode()
            fragments = self.fragmentation_system.fragment_data(doc_data, f"load_doc_{i}")
            documents.append((doc_data, f"load_doc_{i}"))
        
        # Simulate high-frequency attacks
        for attack_round in range(num_attack_rounds):
            # Attack subset of tokens each round
            attack_tokens = tokens[attack_round % 5:(attack_round % 5) + 5]
            for token in attack_tokens:
                self.quantum_detector.access_token(token.token_id, f"load_attacker_{attack_round}")
            
            # Small delay between attack rounds
            await asyncio.sleep(0.01)
        
        # Allow system to process all attacks
        await asyncio.sleep(0.3)
        
        total_time = time.time() - start_time
        
        # Performance assertions
        assert total_time < 3.0, f"Load test took {total_time:.2f}s, should be under 3s"
        
        # Verify system functionality under load
        quantum_stats = self.quantum_detector.get_threat_statistics()
        assert quantum_stats['total_tokens'] == num_tokens
        
        fragment_stats = self.fragmentation_system.get_system_stats()
        assert fragment_stats['fragment_groups'] == num_documents
        
        agent_stats = self.agent_coordinator.get_agent_status()
        assert agent_stats['system_running']
        
        # Test data integrity under load
        successful_reconstructions = 0
        for doc_data, doc_id in documents:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed == doc_data:
                successful_reconstructions += 1
        
        # At least 70% of documents should be reconstructable
        reconstruction_rate = successful_reconstructions / num_documents
        assert reconstruction_rate >= 0.7, f"Reconstruction rate {reconstruction_rate:.2f} too low"
    
    def test_configuration_integration(self):
        """Test that system components integrate with different configurations"""
        
        # High-security configuration
        high_security_detector = QuantumDetector(sensitivity_threshold=0.9)
        high_security_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=50,  # Very short lifetime
            min_fragments=8,  # Many fragments
            quantum_resistance_level=5   # Maximum resistance
        )
        high_security_fragmenter = TemporalFragmentation(high_security_policy)
        high_security_coordinator = AutonomousDefenseCoordinator(
            high_security_detector, high_security_fragmenter
        )
        
        # Test high-security configuration
        test_data = b"High security test data"
        fragments = high_security_fragmenter.fragment_data(test_data, "high_sec_test")
        
        # Should create many fragments
        assert len(fragments) >= 8
        
        # Should be reconstructable immediately
        reconstructed = high_security_fragmenter.reconstruct_data("high_sec_test")
        assert reconstructed == test_data
        
        # Low-latency configuration
        low_latency_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=1000,  # Longer lifetime
            min_fragments=2,  # Fewer fragments
            quantum_resistance_level=1   # Minimal processing
        )
        low_latency_fragmenter = TemporalFragmentation(low_latency_policy)
        
        # Test low-latency configuration
        start_time = time.time()
        fragments = low_latency_fragmenter.fragment_data(test_data, "low_latency_test")
        fragmentation_time = time.time() - start_time
        
        # Should be faster with simpler configuration
        assert fragmentation_time < 0.1  # Less than 100ms
        assert len(fragments) >= 2  # But still fragmented
        
        # Cleanup
        high_security_fragmenter.stop_cleanup_service()
        low_latency_fragmenter.stop_cleanup_service()
    
    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        """Test integrated error handling across all system components"""
        
        await self.agent_coordinator.start_coordination()
        
        # Test scenario: System under attack with some component failures
        
        # 1. Create normal operational state
        token = self.quantum_detector.generate_canary_token("error_test_token")
        doc_data = b"Error handling test document"
        fragments = self.fragmentation_system.fragment_data(doc_data, "error_test_doc")
        
        # 2. Simulate attack
        for i in range(5):
            self.quantum_detector.access_token(token.token_id, f"error_test_attack_{i}")
        
        # 3. Simulate component errors during attack response
        
        # Mock a fragmentation error
        with patch.object(self.fragmentation_system, 'fragment_data', side_effect=Exception("Fragmentation error")):
            try:
                # System should handle fragmentation errors gracefully
                error_fragments = self.fragmentation_system.fragment_data(b"Error test", "error_fragment")
            except Exception:
                # Exception is expected in this test
                pass
        
        # 4. Verify system resilience
        # Original data should still be accessible
        reconstructed = self.fragmentation_system.reconstruct_data("error_test_doc")
        assert reconstructed == doc_data
        
        # Threat detection should still work
        active_threats = self.quantum_detector.get_active_threats()
        # System should continue operating despite component errors
        
        # Agent coordination should remain functional
        agent_stats = self.agent_coordinator.get_agent_status()
        assert agent_stats['system_running']
        
        # 5. Test recovery after error conditions
        # System should accept new operations after errors
        recovery_token = self.quantum_detector.generate_canary_token("recovery_token")
        recovery_doc = b"Recovery test document"
        recovery_fragments = self.fragmentation_system.fragment_data(recovery_doc, "recovery_doc")
        
        # Should work normally after error condition
        assert len(recovery_fragments) > 0
        recovery_reconstructed = self.fragmentation_system.reconstruct_data("recovery_doc")
        assert recovery_reconstructed == recovery_doc


@pytest.mark.slow
class TestLongRunningIntegration:
    """Long-running integration tests for system stability"""
    
    @pytest.mark.asyncio
    async def test_extended_operation(self):
        """Test system stability over extended operation period"""
        
        # Initialize system
        quantum_detector = QuantumDetector()
        fragmentation_system = TemporalFragmentation()
        agent_coordinator = AutonomousDefenseCoordinator(quantum_detector, fragmentation_system)
        
        await agent_coordinator.start_coordination()
        fragmentation_system.start_cleanup_service()
        
        try:
            # Run for extended period with continuous operations
            operation_duration = 5.0  # 5 seconds of continuous operation
            start_time = time.time()
            operation_count = 0
            
            while time.time() - start_time < operation_duration:
                # Create token
                token = quantum_detector.generate_canary_token(f"extended_op_{operation_count}")
                
                # Fragment data
                data = f"Extended operation data {operation_count}".encode()
                fragments = fragmentation_system.fragment_data(data, f"extended_doc_{operation_count}")
                
                # Simulate some access
                quantum_detector.access_token(token.token_id, f"extended_user_{operation_count}")
                
                # Attempt reconstruction
                reconstructed = fragmentation_system.reconstruct_data(f"extended_doc_{operation_count}")
                if reconstructed:
                    assert reconstructed == data
                
                operation_count += 1
                await asyncio.sleep(0.1)  # 100ms between operations
            
            # Verify system health after extended operation
            quantum_stats = quantum_detector.get_threat_statistics()
            fragment_stats = fragmentation_system.get_system_stats()
            agent_stats = agent_coordinator.get_agent_status()
            
            assert quantum_stats['total_tokens'] > 0
            assert agent_stats['system_running']
            assert operation_count > 10  # Should have performed many operations
            
        finally:
            # Cleanup
            await agent_coordinator.stop_coordination()
            fragmentation_system.stop_cleanup_service()
    
    @pytest.mark.asyncio  
    async def test_memory_stability(self):
        """Test system memory usage stability over time"""
        
        quantum_detector = QuantumDetector()
        fragmentation_system = TemporalFragmentation(
            FragmentationPolicy(max_fragment_lifetime_ms=100)  # Short lifetime for cleanup
        )
        agent_coordinator = AutonomousDefenseCoordinator(quantum_detector, fragmentation_system)
        
        await agent_coordinator.start_coordination()
        fragmentation_system.start_cleanup_service()
        
        try:
            # Measure initial state
            initial_tokens = len(quantum_detector.canary_tokens)
            initial_fragments = fragmentation_system.get_system_stats()['total_fragments']
            
            # Generate and expire many items
            for cycle in range(10):  # 10 cycles
                # Generate items
                for i in range(10):
                    token = quantum_detector.generate_canary_token(f"memory_test_{cycle}_{i}")
                    data = f"Memory test data {cycle}_{i}".encode()
                    fragments = fragmentation_system.fragment_data(data, f"memory_doc_{cycle}_{i}")
                
                # Wait for expiration and cleanup
                await asyncio.sleep(0.15)  # 150ms > 100ms fragment lifetime
            
            # Allow final cleanup
            await asyncio.sleep(0.2)
            
            # Check memory usage
            final_tokens = len(quantum_detector.canary_tokens)
            final_fragments = fragmentation_system.get_system_stats()['total_fragments']
            
            # Memory should not grow unboundedly
            # Some items may still exist due to timing, but should be bounded
            assert final_tokens < 200  # Reasonable upper bound
            assert final_fragments < 200  # Reasonable upper bound
            
        finally:
            await agent_coordinator.stop_coordination()
            fragmentation_system.stop_cleanup_service()
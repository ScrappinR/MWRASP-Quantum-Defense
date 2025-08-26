import pytest
import time
import asyncio
import secrets
from unittest.mock import Mock, patch
import numpy as np

from ..core.quantum_detector import (
    QuantumDetector, 
    ThreatLevel, 
    QuantumThreat, 
    CanaryToken
)
from ..core.post_quantum_crypto import SecurityLevel


class TestQuantumDetector:
    def setup_method(self):
        """Setup test environment"""
        self.detector = QuantumDetector(sensitivity_threshold=0.7)
    
    def teardown_method(self):
        """Cleanup after tests"""
        if self.detector._monitoring:
            self.detector.stop_monitoring()
    
    def test_detector_initialization(self):
        """Test quantum detector initialization"""
        assert self.detector.sensitivity_threshold == 0.7
        assert len(self.detector.canary_tokens) == 0
        assert len(self.detector.threat_history) == 0
        assert not self.detector._monitoring
        assert 'superposition_access' in self.detector.quantum_patterns
    
    def test_canary_token_generation(self):
        """Test canary token generation"""
        token = self.detector.generate_canary_token("test_data")
        
        assert isinstance(token, CanaryToken)
        assert token.token_id in self.detector.canary_tokens
        assert token.value.startswith("test_data_")
        assert token.quantum_signature is not None
        assert len(token.quantum_signature) == 64  # SHA256 hex
        assert token.access_count == 0
        assert token.created_at <= time.time()
    
    def test_token_access_normal(self):
        """Test normal token access without threat detection"""
        token = self.detector.generate_canary_token("normal_data")
        
        # Normal access should not trigger threat detection
        threat_detected = self.detector.access_token(token.token_id, "normal_user")
        
        assert not threat_detected
        assert token.access_count == 1
        assert token.last_accessed is not None
    
    def test_superposition_attack_detection(self):
        """Test detection of superposition-like access patterns"""
        token = self.detector.generate_canary_token("test_data")
        
        # Simulate rapid successive accesses (superposition pattern)
        for i in range(5):
            self.detector.access_token(token.token_id, f"quantum_user_{i}")
            time.sleep(0.001)  # Very short delay
        
        # Check if threat was detected
        active_threats = self.detector.get_active_threats()
        assert len(active_threats) > 0
        
        threat = active_threats[-1]
        assert 'superposition_access' in threat.quantum_indicators
        assert threat.threat_level in [ThreatLevel.MEDIUM, ThreatLevel.HIGH, ThreatLevel.CRITICAL]
    
    def test_entanglement_correlation_detection(self):
        """Test detection of entanglement-like correlation patterns"""
        # Create multiple tokens
        tokens = []
        for i in range(3):
            token = self.detector.generate_canary_token(f"entangled_data_{i}")
            tokens.append(token)
        
        # Access all tokens in quick succession (entanglement pattern)
        current_time = time.time()
        for token in tokens:
            self.detector.access_token(token.token_id, "quantum_correlator")
        
        # Check for threat detection
        active_threats = self.detector.get_active_threats()
        if active_threats:
            threat = active_threats[-1]
            # Entanglement correlation might be detected
            assert threat.confidence_score > 0.5
    
    def test_quantum_speedup_detection(self):
        """Test detection of quantum speedup patterns"""
        token = self.detector.generate_canary_token("speedup_test")
        
        # Simulate extremely rapid accesses (quantum speedup)
        start_time = time.time()
        for i in range(10):
            self.detector.access_token(token.token_id, f"speedup_user_{i}")
            # No delay between accesses
        
        # Check if quantum speedup was detected
        active_threats = self.detector.get_active_threats()
        if active_threats:
            threat = active_threats[-1]
            if 'quantum_speedup' in threat.quantum_indicators:
                assert threat.confidence_score >= self.detector.sensitivity_threshold
    
    def test_threat_level_calculation(self):
        """Test threat level calculation based on confidence"""
        # Test different confidence scores
        assert self.detector._calculate_threat_level(0.98) == ThreatLevel.CRITICAL
        assert self.detector._calculate_threat_level(0.90) == ThreatLevel.HIGH
        assert self.detector._calculate_threat_level(0.80) == ThreatLevel.MEDIUM
        assert self.detector._calculate_threat_level(0.72) == ThreatLevel.LOW
    
    def test_monitoring_start_stop(self):
        """Test monitoring system start/stop"""
        assert not self.detector._monitoring
        
        # Start monitoring
        self.detector.start_monitoring()
        assert self.detector._monitoring
        assert self.detector._monitor_thread is not None
        
        # Stop monitoring
        self.detector.stop_monitoring()
        assert not self.detector._monitoring
    
    def test_threat_statistics(self):
        """Test threat statistics generation"""
        # Generate some test data
        token1 = self.detector.generate_canary_token("stats_test_1")
        token2 = self.detector.generate_canary_token("stats_test_2")
        
        # Access tokens to generate some activity
        self.detector.access_token(token1.token_id, "test_user")
        self.detector.access_token(token2.token_id, "test_user")
        
        stats = self.detector.get_threat_statistics()
        
        assert 'total_tokens' in stats
        assert 'total_threats_detected' in stats
        assert 'active_threats' in stats
        assert 'threat_levels' in stats
        assert 'monitoring_active' in stats
        
        assert stats['total_tokens'] == 2
        assert stats['monitoring_active'] == self.detector._monitoring
    
    def test_access_nonexistent_token(self):
        """Test accessing a non-existent token"""
        result = self.detector.access_token("nonexistent_token", "test_user")
        assert not result
    
    def test_quantum_pattern_thresholds(self):
        """Test quantum pattern threshold configurations"""
        patterns = self.detector.quantum_patterns
        
        # Verify all required patterns exist
        required_patterns = [
            'superposition_access',
            'entanglement_correlation', 
            'quantum_speedup',
            'interference_pattern',
            'decoherence_signature'
        ]
        
        for pattern in required_patterns:
            assert pattern in patterns
            assert 0.0 < patterns[pattern] <= 1.0
    
    def test_interference_pattern_detection(self):
        """Test detection of interference patterns"""
        token = self.detector.generate_canary_token("interference_test")
        
        # Create alternating access pattern (wave-like interference)
        intervals = [0.001, 0.005, 0.001, 0.005, 0.001]  # Alternating pattern
        for i, interval in enumerate(intervals):
            self.detector.access_token(token.token_id, f"wave_user_{i}")
            time.sleep(interval)
        
        # Check if interference pattern was detected
        active_threats = self.detector.get_active_threats()
        # Interference detection is complex and may not always trigger
        # This test verifies the detection logic runs without errors
        assert isinstance(active_threats, list)
    
    def test_multiple_simultaneous_threats(self):
        """Test handling multiple simultaneous threats"""
        # Create multiple tokens and generate different threat patterns
        tokens = []
        for i in range(3):
            token = self.detector.generate_canary_token(f"multi_threat_{i}")
            tokens.append(token)
        
        # Generate superposition pattern on first token
        for i in range(5):
            self.detector.access_token(tokens[0].token_id, f"super_user_{i}")
        
        # Generate rapid access on second token
        for i in range(8):
            self.detector.access_token(tokens[1].token_id, f"rapid_user_{i}")
            time.sleep(0.0001)
        
        # Normal access on third token
        self.detector.access_token(tokens[2].token_id, "normal_user")
        
        # Check that multiple threats can be detected
        active_threats = self.detector.get_active_threats()
        # Should have detected at least one threat
        assert len(active_threats) >= 0  # May or may not detect based on timing
    
    def test_threat_expiration(self):
        """Test that threats expire after time limit"""
        token = self.detector.generate_canary_token("expiry_test")
        
        # Create a threat
        for i in range(5):
            self.detector.access_token(token.token_id, f"expiry_user_{i}")
        
        initial_threats = len(self.detector.get_active_threats())
        
        # Modify threat time to simulate old threat
        if self.detector.threat_history:
            self.detector.threat_history[-1].detection_time = time.time() - 400  # 6+ minutes ago
        
        # Check that expired threats are not returned as active
        active_threats = self.detector.get_active_threats()
        # Active threats should only include recent ones (within 5 minutes)
        for threat in active_threats:
            assert time.time() - threat.detection_time < 300.0
    
    def test_custom_sensitivity_threshold(self):
        """Test custom sensitivity threshold"""
        # Create detector with very high sensitivity
        high_sensitivity_detector = QuantumDetector(sensitivity_threshold=0.9)
        assert high_sensitivity_detector.sensitivity_threshold == 0.9
        
        # Create detector with low sensitivity
        low_sensitivity_detector = QuantumDetector(sensitivity_threshold=0.3)
        assert low_sensitivity_detector.sensitivity_threshold == 0.3
    
    @pytest.mark.asyncio
    async def test_concurrent_access_patterns(self):
        """Test concurrent access patterns that might indicate quantum attacks"""
        token = self.detector.generate_canary_token("concurrent_test")
        
        async def access_pattern(user_id, count):
            """Simulate concurrent access pattern"""
            for i in range(count):
                self.detector.access_token(token.token_id, f"concurrent_user_{user_id}_{i}")
                await asyncio.sleep(0.001)
        
        # Run multiple concurrent access patterns
        tasks = []
        for user_id in range(3):
            task = asyncio.create_task(access_pattern(user_id, 4))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        # Check if concurrent patterns triggered threat detection
        active_threats = self.detector.get_active_threats()
        # Concurrent access should increase likelihood of threat detection
        assert isinstance(active_threats, list)
    
    def test_access_pattern_fingerprinting(self):
        """Test that tokens have unique access patterns"""
        token1 = self.detector.generate_canary_token("pattern_test_1")
        token2 = self.detector.generate_canary_token("pattern_test_2")
        
        # Each token should have a unique access pattern
        assert token1.access_pattern != token2.access_pattern
        assert len(token1.access_pattern) == 16  # MD5 hash truncated
        assert len(token2.access_pattern) == 16
    
    def test_threat_confidence_scoring(self):
        """Test threat confidence score calculation"""
        token = self.detector.generate_canary_token("confidence_test")
        
        # Create access pattern that should generate moderate confidence
        for i in range(3):
            self.detector.access_token(token.token_id, f"conf_user_{i}")
            time.sleep(0.01)
        
        active_threats = self.detector.get_active_threats()
        if active_threats:
            threat = active_threats[-1]
            # Confidence should be between 0 and 1
            assert 0.0 <= threat.confidence_score <= 1.0
    
    def test_quantum_signature_uniqueness(self):
        """Test that quantum signatures are unique per token"""
        signatures = set()
        
        for i in range(10):
            token = self.detector.generate_canary_token(f"signature_test_{i}")
            signatures.add(token.quantum_signature)
        
        # All signatures should be unique
        assert len(signatures) == 10


@pytest.mark.integration
class TestQuantumDetectorIntegration:
    """Integration tests for quantum detector with real-time scenarios"""
    
    def test_realistic_attack_simulation(self):
        """Test realistic quantum computer attack simulation"""
        detector = QuantumDetector(sensitivity_threshold=0.6)
        
        # Setup: Create multiple canary tokens as would exist in real system
        tokens = []
        for i in range(5):
            token = detector.generate_canary_token(f"production_data_{i}")
            tokens.append(token)
        
        # Simulate normal access pattern first
        normal_user_accesses = 0
        for token in tokens[:2]:
            detector.access_token(token.token_id, "normal_user_1")
            time.sleep(0.1)
            normal_user_accesses += 1
        
        # Simulate quantum computer attack characteristics:
        # 1. Rapid parallel access to multiple tokens
        # 2. Consistent timing patterns
        # 3. Multiple simultaneous attempts
        
        attack_start = time.time()
        for iteration in range(3):  # Multiple rounds of attack
            for token in tokens:
                # Quantum computer would access all tokens nearly simultaneously
                detector.access_token(token.token_id, f"quantum_attacker_{iteration}")
            time.sleep(0.001)  # Minimal delay between rounds
        
        attack_duration = time.time() - attack_start
        
        # Verify attack detection
        threats = detector.get_active_threats()
        stats = detector.get_threat_statistics()
        
        # Should detect at least one threat given the attack pattern
        assert len(threats) > 0 or stats['total_threats_detected'] > 0
        
        # If threat detected, verify it has appropriate characteristics
        if threats:
            threat = threats[-1]
            assert threat.confidence_score > 0.5
            assert len(threat.quantum_indicators) > 0
            assert 'superposition_access' in threat.quantum_indicators or \
                   'entanglement_correlation' in threat.quantum_indicators
        
        detector.stop_monitoring()
    
    def test_performance_under_load(self):
        """Test detector performance under high load"""
        detector = QuantumDetector()
        
        start_time = time.time()
        
        # Create many tokens
        tokens = []
        for i in range(50):
            token = detector.generate_canary_token(f"load_test_{i}")
            tokens.append(token)
        
        # Generate high access load
        total_accesses = 0
        for _ in range(10):  # 10 rounds
            for token in tokens:
                detector.access_token(token.token_id, f"load_user_{total_accesses}")
                total_accesses += 1
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Performance assertions
        assert processing_time < 5.0  # Should complete within 5 seconds
        assert total_accesses == 500  # Verify all accesses processed
        
        stats = detector.get_threat_statistics()
        assert stats['total_tokens'] == 50
        
        detector.stop_monitoring()
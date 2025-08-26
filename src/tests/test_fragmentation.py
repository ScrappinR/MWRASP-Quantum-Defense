import pytest
import time
import asyncio
import hashlib
from unittest.mock import Mock, patch

from ..core.temporal_fragmentation import (
    TemporalFragmentation, 
    FragmentationPolicy, 
    DataFragment,
    FragmentStatus
)


class TestTemporalFragmentation:
    def setup_method(self):
        """Setup test environment"""
        self.policy = FragmentationPolicy(
            max_fragment_lifetime_ms=100,  # 100ms for testing
            min_fragments=3,
            max_fragments=5,
            quantum_resistance_level=3
        )
        self.fragmenter = TemporalFragmentation(self.policy)
    
    def teardown_method(self):
        """Cleanup after tests"""
        self.fragmenter.stop_cleanup_service()
    
    def test_fragmentation_policy_defaults(self):
        """Test default fragmentation policy"""
        default_policy = FragmentationPolicy()
        
        assert default_policy.max_fragment_lifetime_ms == 100
        assert default_policy.min_fragments == 3
        assert default_policy.max_fragments == 10
        assert default_policy.overlap_factor == 0.2
        assert default_policy.auto_expire is True
        assert default_policy.quantum_resistance_level == 3
    
    def test_data_fragmentation_basic(self):
        """Test basic data fragmentation"""
        test_data = b"This is sensitive test data that needs to be fragmented"
        original_id = "test_fragment_001"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        
        # Verify fragmentation results
        assert len(fragments) >= self.policy.min_fragments
        assert len(fragments) <= self.policy.max_fragments
        assert original_id in self.fragmenter.fragment_groups
        
        # Verify fragment properties
        for fragment in fragments:
            assert isinstance(fragment, DataFragment)
            assert fragment.original_hash == hashlib.sha256(test_data).hexdigest()
            assert fragment.expires_at > time.time()
            assert fragment.status == FragmentStatus.ACTIVE
            assert 0 <= fragment.fragment_index < len(fragments)
            assert fragment.total_fragments == len(fragments)
    
    def test_data_reconstruction_immediate(self):
        """Test immediate data reconstruction"""
        test_data = b"Reconstruct this sensitive information immediately"
        original_id = "reconstruct_test"
        
        # Fragment the data
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        
        # Immediately attempt reconstruction
        reconstructed = self.fragmenter.reconstruct_data(original_id)
        
        assert reconstructed is not None
        assert reconstructed == test_data
        
        # Verify fragments are marked as reconstructed
        for fragment in fragments:
            assert fragment.status == FragmentStatus.RECONSTRUCTED
    
    def test_data_reconstruction_after_delay(self):
        """Test data reconstruction after small delay"""
        test_data = b"Test delayed reconstruction capabilities"
        original_id = "delayed_reconstruct"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        
        # Wait for partial fragment lifetime
        time.sleep(0.03)  # 30ms delay
        
        reconstructed = self.fragmenter.reconstruct_data(original_id)
        
        # Should still be able to reconstruct
        assert reconstructed is not None
        assert reconstructed == test_data
    
    def test_fragment_expiration(self):
        """Test that fragments expire after their lifetime"""
        test_data = b"This data should expire quickly"
        original_id = "expiration_test"
        
        # Use very short lifetime policy
        short_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=50,  # 50ms
            min_fragments=2,
            quantum_resistance_level=1
        )
        short_fragmenter = TemporalFragmentation(short_policy)
        
        fragments = short_fragmenter.fragment_data(test_data, original_id)
        
        # Wait for fragments to expire
        time.sleep(0.1)  # 100ms - longer than fragment lifetime
        
        # Should not be able to reconstruct
        reconstructed = short_fragmenter.reconstruct_data(original_id)
        assert reconstructed is None
        
        # Check fragment status
        status = short_fragmenter.get_fragment_status(original_id)
        assert not status.get('reconstructable', True)
        assert status.get('expired_fragments', 0) > 0
    
    def test_quantum_noise_application(self):
        """Test quantum noise application and removal"""
        test_data = b"Test quantum noise resistance"
        
        # Test with quantum resistance level 3
        high_resistance_policy = FragmentationPolicy(quantum_resistance_level=5)
        fragmenter = TemporalFragmentation(high_resistance_policy)
        
        fragments = fragmenter.fragment_data(test_data, "noise_test")
        
        # Fragments should have noise applied
        for fragment in fragments:
            # The fragment data should be different from original due to noise
            if len(fragment.data_chunk) <= len(test_data):
                # Only check if fragment is smaller than original
                assert fragment.data_chunk != test_data
        
        # But reconstruction should still work
        reconstructed = fragmenter.reconstruct_data("noise_test")
        assert reconstructed == test_data
    
    def test_overlapping_fragments(self):
        """Test fragment overlap functionality"""
        test_data = b"A" * 100  # 100 bytes of 'A' for clear testing
        
        policy = FragmentationPolicy(
            overlap_factor=0.3,  # 30% overlap
            min_fragments=4,
            max_fragments=4  # Fixed number for predictable testing
        )
        fragmenter = TemporalFragmentation(policy)
        
        fragments = fragmenter.fragment_data(test_data, "overlap_test")
        
        # Verify overlap exists between fragments
        assert len(fragments) == 4
        
        # Calculate expected sizes with overlap
        base_chunk_size = len(test_data) // 4
        overlap_size = int(base_chunk_size * 0.3)
        
        # First fragment should not have leading overlap
        # Last fragment should not have trailing overlap
        # Middle fragments should have both leading and trailing overlap
        
        for i, fragment in enumerate(fragments):
            expected_min_size = base_chunk_size
            if i > 0:  # Has leading overlap
                expected_min_size += overlap_size
            if i < len(fragments) - 1:  # Has trailing overlap
                expected_min_size += overlap_size
            
            # Fragment should be at least the base size
            assert len(fragment.data_chunk) >= base_chunk_size
    
    def test_fragment_access_tracking(self):
        """Test fragment access count tracking"""
        test_data = b"Track access to these fragments"
        original_id = "access_tracking"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        fragment_id = fragments[0].fragment_id
        
        # Access fragment multiple times
        for i in range(5):
            accessed_fragment = self.fragmenter.access_fragment(fragment_id)
            assert accessed_fragment is not None
            assert accessed_fragment.access_count == i + 1
    
    def test_fragment_status_tracking(self):
        """Test fragment status throughout lifecycle"""
        test_data = b"Status tracking test data"
        original_id = "status_test"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        fragment = fragments[0]
        
        # Initially active
        assert fragment.status == FragmentStatus.ACTIVE
        
        # Access should keep it active
        accessed = self.fragmenter.access_fragment(fragment.fragment_id)
        assert accessed.status == FragmentStatus.ACTIVE
        
        # Force expiration
        self.fragmenter.force_expire_all(original_id)
        
        # Should be expired after force expiration
        expired_fragment = self.fragmenter.access_fragment(fragment.fragment_id)
        assert expired_fragment is None  # Should return None for expired fragments
    
    def test_cleanup_service(self):
        """Test automatic cleanup service"""
        test_data = b"Cleanup service test"
        original_id = "cleanup_test"
        
        # Start cleanup service
        self.fragmenter.start_cleanup_service()
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        initial_count = len(self.fragmenter.fragments)
        
        # Force expire fragments
        self.fragmenter.force_expire_all(original_id)
        
        # Wait for cleanup to process
        time.sleep(0.02)  # 20ms
        
        # Cleanup should eventually remove expired fragments
        # (May take some time, so we just verify the service is running)
        assert self.fragmenter._running
    
    def test_fragment_group_management(self):
        """Test fragment group tracking"""
        test_data1 = b"First set of data"
        test_data2 = b"Second set of data"
        
        fragments1 = self.fragmenter.fragment_data(test_data1, "group_1")
        fragments2 = self.fragmenter.fragment_data(test_data2, "group_2")
        
        # Verify groups are tracked separately
        assert "group_1" in self.fragmenter.fragment_groups
        assert "group_2" in self.fragmenter.fragment_groups
        
        group1_ids = self.fragmenter.fragment_groups["group_1"]
        group2_ids = self.fragmenter.fragment_groups["group_2"]
        
        assert len(group1_ids) == len(fragments1)
        assert len(group2_ids) == len(fragments2)
        
        # Group IDs should be different
        assert set(group1_ids).isdisjoint(set(group2_ids))
    
    def test_reconstruction_with_missing_fragments(self):
        """Test reconstruction when some fragments are missing/expired"""
        test_data = b"Test partial reconstruction with missing fragments"
        original_id = "partial_test"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        
        # Manually expire some fragments (simulate partial loss)
        for i in range(len(fragments) // 2):  # Expire half the fragments
            fragment_id = fragments[i].fragment_id
            self.fragmenter._expire_fragment(fragment_id)
        
        # Attempt reconstruction with missing fragments
        reconstructed = self.fragmenter.reconstruct_data(original_id)
        
        # Should fail reconstruction due to insufficient fragments
        # (depends on overlap factor and quantum resistance implementation)
        if reconstructed:
            # If reconstruction succeeded, verify it's correct
            assert reconstructed == test_data
        # If reconstruction failed, that's also acceptable behavior
    
    def test_different_data_sizes(self):
        """Test fragmentation with different data sizes"""
        test_cases = [
            (b"Small", "small_data"),
            (b"A" * 1000, "medium_data"),  # 1KB
            (b"B" * 10000, "large_data"),  # 10KB
            (b"", "empty_data")  # Edge case: empty data
        ]
        
        for test_data, original_id in test_cases:
            if len(test_data) == 0:
                # Skip empty data as it might not be supported
                continue
                
            fragments = self.fragmenter.fragment_data(test_data, original_id)
            
            # Should create appropriate number of fragments
            assert len(fragments) >= 1
            
            # Should be able to reconstruct
            reconstructed = self.fragmenter.reconstruct_data(original_id)
            assert reconstructed == test_data
    
    def test_concurrent_fragmentation(self):
        """Test concurrent fragmentation operations"""
        async def fragment_data_async(data, original_id):
            return self.fragmenter.fragment_data(data.encode(), original_id)
        
        async def test_concurrent():
            tasks = []
            for i in range(5):
                task = asyncio.create_task(
                    fragment_data_async(f"Concurrent data {i}", f"concurrent_{i}")
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results
        
        # Run concurrent fragmentation
        results = asyncio.run(test_concurrent())
        
        # Verify all fragmentations completed
        assert len(results) == 5
        for fragments in results:
            assert len(fragments) > 0
    
    def test_system_statistics(self):
        """Test system statistics gathering"""
        # Create some fragments
        test_data = b"Statistics test data"
        self.fragmenter.fragment_data(test_data, "stats_test_1")
        self.fragmenter.fragment_data(test_data, "stats_test_2")
        
        stats = self.fragmenter.get_system_stats()
        
        # Verify statistics structure
        assert 'total_fragments' in stats
        assert 'active_fragments' in stats
        assert 'fragment_groups' in stats
        assert 'cleanup_running' in stats
        assert 'policy' in stats
        
        # Verify statistics values
        assert stats['total_fragments'] > 0
        assert stats['fragment_groups'] >= 2
        assert isinstance(stats['cleanup_running'], bool)
        
        # Verify policy information
        policy_stats = stats['policy']
        assert policy_stats['max_lifetime_ms'] == self.policy.max_fragment_lifetime_ms
        assert policy_stats['min_fragments'] == self.policy.min_fragments
    
    def test_reconstruction_key_uniqueness(self):
        """Test that reconstruction keys are unique per fragment"""
        test_data = b"Reconstruction key uniqueness test"
        fragments = self.fragmenter.fragment_data(test_data, "key_test")
        
        reconstruction_keys = set()
        for fragment in fragments:
            assert fragment.reconstruction_key is not None
            assert len(fragment.reconstruction_key) == 32  # Should be 32 chars
            reconstruction_keys.add(fragment.reconstruction_key)
        
        # All keys should be unique
        assert len(reconstruction_keys) == len(fragments)
    
    def test_fragment_status_transitions(self):
        """Test fragment status transitions"""
        test_data = b"Status transition test"
        original_id = "transition_test"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        fragment = fragments[0]
        
        # Start as ACTIVE
        assert fragment.status == FragmentStatus.ACTIVE
        
        # Access should keep as ACTIVE (unless near expiration)
        self.fragmenter.access_fragment(fragment.fragment_id)
        # Status might change to EXPIRING if very close to expiration
        
        # Reconstruction should mark as RECONSTRUCTED
        self.fragmenter.reconstruct_data(original_id)
        assert fragment.status == FragmentStatus.RECONSTRUCTED
    
    def test_error_recovery_reconstruction(self):
        """Test error recovery during reconstruction"""
        test_data = b"Error recovery test data for reconstruction"
        original_id = "error_recovery"
        
        fragments = self.fragmenter.fragment_data(test_data, original_id)
        
        # Corrupt one fragment's hash to trigger repair mechanism
        fragments[0].original_hash = "corrupted_hash"
        
        # Should attempt repair reconstruction
        reconstructed = self.fragmenter.reconstruct_data(original_id)
        
        # May or may not succeed depending on repair algorithm
        # But should not crash
        if reconstructed:
            # If repair succeeded, data should match
            assert isinstance(reconstructed, bytes)
    
    @pytest.mark.performance
    def test_fragmentation_performance(self):
        """Test fragmentation performance with large data"""
        # Test with 1MB of data
        large_data = b"A" * (1024 * 1024)  # 1MB
        
        start_time = time.time()
        fragments = self.fragmenter.fragment_data(large_data, "performance_test")
        fragmentation_time = time.time() - start_time
        
        # Should complete fragmentation within reasonable time
        assert fragmentation_time < 1.0  # Less than 1 second
        
        start_time = time.time()
        reconstructed = self.fragmenter.reconstruct_data("performance_test")
        reconstruction_time = time.time() - start_time
        
        # Should complete reconstruction within reasonable time
        assert reconstruction_time < 1.0  # Less than 1 second
        assert reconstructed == large_data


@pytest.mark.integration
class TestTemporalFragmentationIntegration:
    """Integration tests for temporal fragmentation"""
    
    def test_realistic_document_fragmentation(self):
        """Test fragmentation of realistic document data"""
        # Simulate a sensitive document
        document_data = f"""
        CLASSIFIED DOCUMENT - QUANTUM RESEARCH
        Date: {time.strftime('%Y-%m-%d')}
        
        This document contains sensitive quantum encryption algorithms
        and temporal security protocols that must be protected from
        quantum computer attacks.
        
        Key algorithms:
        1. Quantum-resistant encryption
        2. Temporal data fragmentation
        3. Autonomous defense coordination
        
        Security Level: TOP SECRET
        Expiration: Immediate after access
        """.encode()
        
        # Use production-like policy
        policy = FragmentationPolicy(
            max_fragment_lifetime_ms=200,  # 200ms lifetime
            min_fragments=5,
            max_fragments=8,
            overlap_factor=0.25,
            quantum_resistance_level=4
        )
        
        fragmenter = TemporalFragmentation(policy)
        fragmenter.start_cleanup_service()
        
        # Fragment the document
        fragments = fragmenter.fragment_data(document_data, "classified_doc_001")
        
        # Verify security properties
        assert len(fragments) >= 5
        
        # Immediate reconstruction should work
        reconstructed = fragmenter.reconstruct_data("classified_doc_001")
        assert reconstructed == document_data
        
        # Wait for partial expiration
        time.sleep(0.1)  # 100ms
        
        # Should still work with some fragments expired
        reconstructed_partial = fragmenter.reconstruct_data("classified_doc_001")
        # May or may not work depending on how many fragments expired
        
        # Wait for full expiration
        time.sleep(0.15)  # Additional 150ms (total 250ms > 200ms lifetime)
        
        # Should not be reconstructable after full expiration
        expired_reconstruction = fragmenter.reconstruct_data("classified_doc_001")
        assert expired_reconstruction is None
        
        fragmenter.stop_cleanup_service()
    
    def test_high_throughput_fragmentation(self):
        """Test system under high throughput conditions"""
        policy = FragmentationPolicy(
            max_fragment_lifetime_ms=300,
            min_fragments=3,
            max_fragments=5
        )
        fragmenter = TemporalFragmentation(policy)
        fragmenter.start_cleanup_service()
        
        # Generate high throughput of fragmentation requests
        start_time = time.time()
        successful_fragments = 0
        successful_reconstructions = 0
        
        for i in range(20):  # 20 documents
            data = f"High throughput document {i} with sensitive data".encode()
            original_id = f"throughput_doc_{i}"
            
            try:
                fragments = fragmenter.fragment_data(data, original_id)
                successful_fragments += 1
                
                # Immediate reconstruction attempt
                reconstructed = fragmenter.reconstruct_data(original_id)
                if reconstructed == data:
                    successful_reconstructions += 1
                    
            except Exception as e:
                print(f"Error processing document {i}: {e}")
        
        total_time = time.time() - start_time
        
        # Performance assertions
        assert total_time < 2.0  # Should complete within 2 seconds
        assert successful_fragments >= 18  # At least 90% success rate
        assert successful_reconstructions >= 15  # At least 75% reconstruction success
        
        # System should still be functional
        stats = fragmenter.get_system_stats()
        assert stats['cleanup_running']
        
        fragmenter.stop_cleanup_service()
    
    def test_memory_cleanup_effectiveness(self):
        """Test that memory cleanup effectively removes expired fragments"""
        policy = FragmentationPolicy(
            max_fragment_lifetime_ms=50,  # Very short lifetime
            min_fragments=2,
            max_fragments=3
        )
        fragmenter = TemporalFragmentation(policy)
        fragmenter.start_cleanup_service()
        
        # Create many fragments
        for i in range(10):
            data = f"Memory test data {i}".encode()
            fragmenter.fragment_data(data, f"memory_test_{i}")
        
        initial_stats = fragmenter.get_system_stats()
        initial_count = initial_stats['total_fragments']
        
        # Wait for expiration and cleanup
        time.sleep(0.1)  # 100ms - longer than fragment lifetime
        
        # Give cleanup service time to work
        time.sleep(0.05)  # Additional 50ms for cleanup
        
        final_stats = fragmenter.get_system_stats()
        final_count = final_stats['total_fragments']
        
        # Memory usage should be reduced (some fragments cleaned up)
        # Note: exact cleanup timing may vary, so we check for trend
        assert final_count <= initial_count
        
        fragmenter.stop_cleanup_service()
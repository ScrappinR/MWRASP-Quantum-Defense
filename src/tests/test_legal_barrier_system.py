#!/usr/bin/env python3
"""
MWRASP Legal Barrier System - Comprehensive Testing and Validation Framework
Test suite for legal jurisdiction control and barrier effectiveness

This testing framework validates:
- Legal barrier activation and deactivation
- Jurisdiction configuration and management  
- Compliance engine functionality
- Real-time monitoring capabilities
- Integration with quantum attack detection
- Edge cases and error handling

Date: August 25, 2025
Version: 1.0 - Legal Barrier Testing Framework
Status: Comprehensive validation for defensive security system
"""

import asyncio
import unittest
import json
import tempfile
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, AsyncMock
import sys
import logging

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

# Import modules to test
from legal_jurisdiction_control_system import (
    LegalBarrierController,
    LegalJurisdictionDatabase, 
    LegalComplianceEngine,
    JurisdictionMode,
    LegalBarrierType,
    JurisdictionConfig,
    LegalBarrierEvent
)

from real_time_legal_monitoring import (
    LegalBarrierMonitor,
    MonitoringPriority,
    AlertType,
    LegalMonitoringAlert,
    BarrierEffectivenessMetrics,
    ThreatActorProfile
)

# Configure test logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise during testing

class TestLegalJurisdictionDatabase(unittest.TestCase):
    """Test legal jurisdiction database functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = LegalJurisdictionDatabase()
    
    def test_initialization(self):
        """Test database initialization with default jurisdictions"""
        
        # Check that default jurisdictions are loaded
        self.assertGreater(len(self.db.jurisdictions), 0)
        
        # Check specific jurisdictions exist
        us_jurisdiction = self.db.get_jurisdiction("US")
        self.assertIsNotNone(us_jurisdiction)
        self.assertEqual(us_jurisdiction.jurisdiction_name, "United States")
        self.assertEqual(us_jurisdiction.mode, JurisdictionMode.OFF)
        
        eu_jurisdiction = self.db.get_jurisdiction("EU") 
        self.assertIsNotNone(eu_jurisdiction)
        self.assertEqual(eu_jurisdiction.jurisdiction_name, "European Union")
    
    def test_jurisdiction_retrieval(self):
        """Test jurisdiction retrieval by code"""
        
        # Test valid jurisdiction
        uk_jurisdiction = self.db.get_jurisdiction("UK")
        self.assertIsNotNone(uk_jurisdiction)
        self.assertEqual(uk_jurisdiction.jurisdiction_code, "UK")
        
        # Test case insensitive retrieval
        ca_jurisdiction = self.db.get_jurisdiction("ca")
        self.assertIsNotNone(ca_jurisdiction)
        self.assertEqual(ca_jurisdiction.jurisdiction_code, "CA")
        
        # Test invalid jurisdiction
        invalid_jurisdiction = self.db.get_jurisdiction("INVALID")
        self.assertIsNone(invalid_jurisdiction)
    
    def test_jurisdiction_update(self):
        """Test updating jurisdiction configuration"""
        
        # Get original jurisdiction
        original = self.db.get_jurisdiction("CH")
        self.assertIsNotNone(original)
        
        # Modify configuration
        original.mode = JurisdictionMode.ACTIVE
        original.barrier_types_enabled = [LegalBarrierType.DATA_SOVEREIGNTY]
        
        # Update in database
        result = self.db.update_jurisdiction("CH", original)
        self.assertTrue(result)
        
        # Verify update
        updated = self.db.get_jurisdiction("CH")
        self.assertEqual(updated.mode, JurisdictionMode.ACTIVE)
        self.assertIn(LegalBarrierType.DATA_SOVEREIGNTY, updated.barrier_types_enabled)
        
        # Test updating non-existent jurisdiction
        fake_config = JurisdictionConfig(
            jurisdiction_code="FAKE",
            jurisdiction_name="Fake Country",
            mode=JurisdictionMode.ACTIVE,
            legal_framework="fake_law",
            data_protection_laws=[],
            enforcement_complexity=1,
            cooperation_treaties=[],
            barrier_types_enabled=[],
            routing_priority=50,
            last_updated=datetime.now(timezone.utc),
            compliance_verified=False
        )
        
        result = self.db.update_jurisdiction("FAKE", fake_config)
        self.assertFalse(result)
    
    def test_active_jurisdictions(self):
        """Test retrieval of active jurisdictions"""
        
        # Initially no active jurisdictions
        active = self.db.get_active_jurisdictions()
        self.assertEqual(len(active), 0)
        
        # Activate some jurisdictions
        us_config = self.db.get_jurisdiction("US")
        us_config.mode = JurisdictionMode.ACTIVE
        self.db.update_jurisdiction("US", us_config)
        
        eu_config = self.db.get_jurisdiction("EU")
        eu_config.mode = JurisdictionMode.PASSIVE  
        self.db.update_jurisdiction("EU", eu_config)
        
        uk_config = self.db.get_jurisdiction("UK")
        uk_config.mode = JurisdictionMode.OFF
        self.db.update_jurisdiction("UK", uk_config)
        
        # Check active jurisdictions
        active = self.db.get_active_jurisdictions()
        self.assertEqual(len(active), 2)  # US (active) and EU (passive)
        
        active_codes = [j.jurisdiction_code for j in active]
        self.assertIn("US", active_codes)
        self.assertIn("EU", active_codes)
        self.assertNotIn("UK", active_codes)

class TestLegalComplianceEngine(unittest.TestCase):
    """Test legal compliance engine functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = LegalJurisdictionDatabase()
        self.engine = LegalComplianceEngine(self.db)
        
        # Configure test jurisdictions
        us_config = self.db.get_jurisdiction("US")
        us_config.mode = JurisdictionMode.ACTIVE
        us_config.barrier_types_enabled = [
            LegalBarrierType.DATA_SOVEREIGNTY,
            LegalBarrierType.COMPLIANCE_FRAGMENTATION
        ]
        self.db.update_jurisdiction("US", us_config)
        
        eu_config = self.db.get_jurisdiction("EU")
        eu_config.mode = JurisdictionMode.ACTIVE
        eu_config.barrier_types_enabled = [
            LegalBarrierType.LEGAL_STANDING_COMPLEXITY
        ]
        self.db.update_jurisdiction("EU", eu_config)
    
    def test_cross_border_complexity_analysis(self):
        """Test cross-border legal complexity analysis"""
        
        # Test US to EU complexity
        complexity = self.engine.analyze_cross_border_complexity("US", "EU")
        
        self.assertIn("complexity_score", complexity)
        self.assertIn("applicable_barriers", complexity)
        self.assertIn("legal_basis", complexity)
        self.assertGreater(complexity["complexity_score"], 0)
    
    def test_generate_legal_barriers(self):
        """Test legal barrier generation"""
        
        threat_data = {
            "classification": "quantum_attack",
            "severity": "HIGH",
            "algorithm": "Shor_Algorithm"
        }
        
        # Test with US IP (should generate barriers)
        barriers = self.engine.generate_legal_barriers(threat_data, "8.8.8.8")  # US IP
        self.assertIsInstance(barriers, list)
        
        # Test with unknown IP (should return empty)
        barriers_empty = self.engine.generate_legal_barriers(threat_data, "1.1.1.1")  # Unknown IP
        self.assertEqual(len(barriers_empty), 0)
    
    def test_ip_to_country_mapping(self):
        """Test IP to country mapping functionality"""
        
        # Test US IP ranges
        us_ip = self.engine._ip_to_country("8.8.8.8")
        self.assertEqual(us_ip, "US")
        
        # Test EU IP ranges 
        eu_ip = self.engine._ip_to_country("85.1.1.1")
        self.assertEqual(eu_ip, "EU")
        
        # Test unknown IP
        unknown_ip = self.engine._ip_to_country("1.1.1.1")
        self.assertIsNone(unknown_ip)
        
        # Test invalid IP
        invalid_ip = self.engine._ip_to_country("invalid_ip")
        self.assertIsNone(invalid_ip)

class TestLegalBarrierController(unittest.TestCase):
    """Test legal barrier controller functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = LegalBarrierController()
    
    def test_system_enable_disable(self):
        """Test system enable/disable functionality"""
        
        # System should start disabled
        self.assertFalse(self.controller.system_enabled)
        
        # Test invalid authorization
        result = self.controller.enable_system("invalid_key")
        self.assertFalse(result)
        self.assertFalse(self.controller.system_enabled)
        
        # Test valid authorization
        valid_key = "authorized_legal_barrier_activation"
        result = self.controller.enable_system(valid_key)
        self.assertTrue(result)
        self.assertTrue(self.controller.system_enabled)
        
        # Test disable
        result = self.controller.disable_system()
        self.assertTrue(result)
        self.assertFalse(self.controller.system_enabled)
    
    def test_jurisdiction_configuration(self):
        """Test jurisdiction configuration"""
        
        # Enable system first
        self.controller.enable_system("authorized_legal_barrier_activation")
        
        # Configure jurisdiction
        result = self.controller.configure_jurisdiction(
            "US",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY],
            priority=80
        )
        self.assertTrue(result)
        
        # Verify configuration
        jurisdiction = self.controller.jurisdiction_db.get_jurisdiction("US")
        self.assertEqual(jurisdiction.mode, JurisdictionMode.ACTIVE)
        self.assertIn(LegalBarrierType.DATA_SOVEREIGNTY, jurisdiction.barrier_types_enabled)
        self.assertEqual(jurisdiction.routing_priority, 80)
        
        # Test configuration with system disabled
        self.controller.disable_system()
        result = self.controller.configure_jurisdiction(
            "EU",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY]
        )
        self.assertFalse(result)
        
        # Test invalid jurisdiction
        self.controller.enable_system("authorized_legal_barrier_activation")
        result = self.controller.configure_jurisdiction(
            "INVALID",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY]
        )
        self.assertFalse(result)
    
    def test_threat_processing_with_legal_barriers(self):
        """Test threat processing with legal barrier application"""
        
        # Enable system and configure jurisdiction
        self.controller.enable_system("authorized_legal_barrier_activation")
        self.controller.configure_jurisdiction(
            "US",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY, LegalBarrierType.COMPLIANCE_FRAGMENTATION]
        )
        
        threat_data = {
            "classification": "quantum_attack",
            "severity": "HIGH",
            "algorithm": "Shor_Algorithm"
        }
        
        # Process threat (async function)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                self.controller.process_threat_with_legal_barriers(threat_data, "8.8.8.8")
            )
            
            self.assertEqual(response["status"], "processed")
            self.assertIn("legal_barriers", response)
            self.assertIn("timestamp", response)
            
        finally:
            loop.close()
    
    def test_jurisdiction_status_reporting(self):
        """Test jurisdiction status reporting"""
        
        status = self.controller.get_jurisdiction_status()
        
        self.assertIn("system_enabled", status)
        self.assertIn("total_jurisdictions", status)
        self.assertIn("active_jurisdictions", status)
        self.assertIn("passive_jurisdictions", status)
        self.assertIn("jurisdictions", status)
        
        # Initially system is disabled
        self.assertFalse(status["system_enabled"])
        self.assertEqual(status["active_jurisdictions"], 0)
        
        # Enable and configure
        self.controller.enable_system("authorized_legal_barrier_activation")
        self.controller.configure_jurisdiction("US", JurisdictionMode.ACTIVE, [])
        
        updated_status = self.controller.get_jurisdiction_status()
        self.assertTrue(updated_status["system_enabled"])
        self.assertEqual(updated_status["active_jurisdictions"], 1)
    
    def test_configuration_save_load(self):
        """Test configuration save and load functionality"""
        
        # Enable system and configure jurisdiction
        self.controller.enable_system("authorized_legal_barrier_activation")
        self.controller.configure_jurisdiction(
            "US",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY],
            priority=90
        )
        
        # Create temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Test save
            result = self.controller.save_configuration(temp_filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Create new controller and load configuration
            new_controller = LegalBarrierController()
            result = new_controller.load_configuration(temp_filename)
            self.assertTrue(result)
            
            # Verify loaded configuration
            self.assertTrue(new_controller.system_enabled)
            us_config = new_controller.jurisdiction_db.get_jurisdiction("US")
            self.assertEqual(us_config.mode, JurisdictionMode.ACTIVE)
            self.assertIn(LegalBarrierType.DATA_SOVEREIGNTY, us_config.barrier_types_enabled)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TestLegalBarrierMonitor(unittest.TestCase):
    """Test real-time legal monitoring functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = LegalBarrierController()
        self.controller.enable_system("authorized_legal_barrier_activation")
        self.monitor = LegalBarrierMonitor(self.controller)
    
    def test_monitoring_initialization(self):
        """Test monitoring system initialization"""
        
        self.assertFalse(self.monitor.active_monitoring)
        self.assertEqual(len(self.monitor.alert_queue), 0)
        self.assertEqual(len(self.monitor.effectiveness_metrics), 0)
        self.assertEqual(len(self.monitor.monitoring_rules), 7)  # Expected number of rules
    
    def test_alert_generation(self):
        """Test alert generation functionality"""
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Generate test alert
            loop.run_until_complete(
                self.monitor._generate_alert(
                    AlertType.BARRIER_ACTIVATION,
                    MonitoringPriority.MEDIUM,
                    "US",
                    LegalBarrierType.DATA_SOVEREIGNTY,
                    "Test alert",
                    {"test": "data"}
                )
            )
            
            # Check alert was generated
            self.assertEqual(len(self.monitor.alert_queue), 1)
            
            alert = self.monitor.alert_queue[0]
            self.assertEqual(alert.alert_type, AlertType.BARRIER_ACTIVATION)
            self.assertEqual(alert.priority, MonitoringPriority.MEDIUM)
            self.assertEqual(alert.jurisdiction, "US")
            
        finally:
            loop.close()
    
    def test_effectiveness_metrics_tracking(self):
        """Test barrier effectiveness metrics tracking"""
        
        # Create test metrics
        metrics = BarrierEffectivenessMetrics(
            barrier_type=LegalBarrierType.DATA_SOVEREIGNTY,
            jurisdiction="US",
            activation_count=10,
            success_rate=95.0,
            average_response_time=45.0,
            bypass_attempts=1,
            legal_challenges=0,
            effectiveness_score=85.0,
            last_updated=datetime.now(timezone.utc)
        )
        
        self.monitor.effectiveness_metrics["data_sovereignty_US"] = metrics
        
        # Test metrics retrieval
        retrieved_metrics = self.monitor.get_effectiveness_metrics()
        self.assertIn("data_sovereignty_US", retrieved_metrics)
        self.assertEqual(retrieved_metrics["data_sovereignty_US"].activation_count, 10)
    
    def test_threat_actor_profiling(self):
        """Test threat actor profiling functionality"""
        
        # Create test threat actor profile
        profile = ThreatActorProfile(
            actor_id="TEST_ACTOR_001",
            ip_addresses=["192.168.1.100"],
            target_jurisdictions=["US", "EU"],
            barrier_interaction_patterns={"probing": True},
            sophistication_level="HIGH",
            legal_evasion_techniques=["jurisdiction_shopping"],
            response_to_barriers="adaptive",
            risk_assessment="CRITICAL",
            first_seen=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc)
        )
        
        self.monitor.threat_actor_profiles["TEST_ACTOR_001"] = profile
        
        # Test profile retrieval
        profiles = self.monitor.get_threat_actor_profiles()
        self.assertIn("TEST_ACTOR_001", profiles)
        self.assertEqual(profiles["TEST_ACTOR_001"].sophistication_level, "HIGH")
    
    def test_alert_callback_registration(self):
        """Test alert callback registration and execution"""
        
        callback_called = False
        callback_alert = None
        
        async def test_callback(alert):
            nonlocal callback_called, callback_alert
            callback_called = True
            callback_alert = alert
        
        # Register callback
        self.monitor.add_alert_callback(test_callback)
        self.assertEqual(len(self.monitor.alert_callbacks), 1)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Generate alert to trigger callback
            loop.run_until_complete(
                self.monitor._generate_alert(
                    AlertType.SYSTEM_ANOMALY,
                    MonitoringPriority.HIGH,
                    "SYSTEM",
                    None,
                    "Test callback alert",
                    {"callback_test": True}
                )
            )
            
            # Process the alert (which should trigger callback)
            alert = self.monitor.alert_queue[0]
            loop.run_until_complete(self.monitor._process_alert(alert))
            
            # Verify callback was called
            self.assertTrue(callback_called)
            self.assertIsNotNone(callback_alert)
            self.assertEqual(callback_alert.alert_type, AlertType.SYSTEM_ANOMALY)
            
        finally:
            loop.close()

class TestLegalBarrierIntegration(unittest.TestCase):
    """Test integration between components"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.controller = LegalBarrierController()
        self.controller.enable_system("authorized_legal_barrier_activation")
        self.monitor = LegalBarrierMonitor(self.controller)
    
    def test_end_to_end_threat_processing(self):
        """Test end-to-end threat processing with legal barriers and monitoring"""
        
        # Configure jurisdiction
        self.controller.configure_jurisdiction(
            "US",
            JurisdictionMode.ACTIVE,
            [LegalBarrierType.DATA_SOVEREIGNTY, LegalBarrierType.COMPLIANCE_FRAGMENTATION],
            priority=85
        )
        
        # Create threat data
        threat_data = {
            "classification": "quantum_attack",
            "algorithm": "Shor_Algorithm",
            "severity": "CRITICAL",
            "source": "advanced_persistent_threat"
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Process threat with legal barriers
            response = loop.run_until_complete(
                self.controller.process_threat_with_legal_barriers(threat_data, "8.8.8.8")
            )
            
            # Verify response
            self.assertEqual(response["status"], "processed")
            self.assertGreater(len(response["legal_barriers"]), 0)
            
            # Verify event was logged
            events = self.controller.export_event_log()
            self.assertGreater(len(events), 0)
            
            recent_event = events[-1]
            self.assertEqual(recent_event["threat_classification"], "quantum_attack")
            
        finally:
            loop.close()
    
    def test_configuration_consistency(self):
        """Test configuration consistency across components"""
        
        # Configure multiple jurisdictions
        jurisdictions_config = [
            ("US", JurisdictionMode.ACTIVE, [LegalBarrierType.DATA_SOVEREIGNTY]),
            ("EU", JurisdictionMode.PASSIVE, [LegalBarrierType.LEGAL_STANDING_COMPLEXITY]),
            ("UK", JurisdictionMode.OFF, [])
        ]
        
        for code, mode, barriers in jurisdictions_config:
            self.controller.configure_jurisdiction(code, mode, barriers)
        
        # Get status from controller
        status = self.controller.get_jurisdiction_status()
        
        # Verify consistency
        self.assertEqual(status["active_jurisdictions"], 1)  # Only US is active
        self.assertEqual(status["passive_jurisdictions"], 1)  # Only EU is passive
        
        # Check individual jurisdictions
        us_config = status["jurisdictions"]["US"]
        self.assertEqual(us_config["mode"], "active")
        self.assertIn("data_sovereignty", us_config["enabled_barriers"])
        
        eu_config = status["jurisdictions"]["EU"] 
        self.assertEqual(eu_config["mode"], "passive")
        self.assertIn("legal_standing_complexity", eu_config["enabled_barriers"])
        
        uk_config = status["jurisdictions"]["UK"]
        self.assertEqual(uk_config["mode"], "off")
        self.assertEqual(len(uk_config["enabled_barriers"]), 0)

class TestLegalBarrierEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up edge case test fixtures"""
        self.controller = LegalBarrierController()
    
    def test_disabled_system_operations(self):
        """Test operations when system is disabled"""
        
        # System starts disabled
        self.assertFalse(self.controller.system_enabled)
        
        # Try to configure jurisdiction with disabled system
        result = self.controller.configure_jurisdiction(
            "US", JurisdictionMode.ACTIVE, [LegalBarrierType.DATA_SOVEREIGNTY]
        )
        self.assertFalse(result)
        
        # Try to process threat with disabled system
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                self.controller.process_threat_with_legal_barriers(
                    {"classification": "test"}, "8.8.8.8"
                )
            )
            
            self.assertEqual(response["status"], "system_disabled")
            self.assertEqual(len(response["legal_barriers"]), 0)
            
        finally:
            loop.close()
    
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        
        self.controller.enable_system("authorized_legal_barrier_activation")
        
        # Test invalid jurisdiction codes
        result = self.controller.configure_jurisdiction(
            "", JurisdictionMode.ACTIVE, []
        )
        self.assertFalse(result)
        
        result = self.controller.configure_jurisdiction(
            "INVALID_CODE", JurisdictionMode.ACTIVE, []
        )
        self.assertFalse(result)
        
        # Test invalid IP addresses in threat processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                self.controller.process_threat_with_legal_barriers(
                    {"classification": "test"}, "invalid_ip"
                )
            )
            
            # Should handle gracefully
            self.assertEqual(response["status"], "processed")
            
        finally:
            loop.close()
    
    def test_concurrent_operations(self):
        """Test concurrent operations on legal barrier system"""
        
        self.controller.enable_system("authorized_legal_barrier_activation")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Create multiple concurrent threat processing tasks
            threats = [
                {"classification": f"threat_{i}", "severity": "HIGH"}
                for i in range(5)
            ]
            
            tasks = [
                self.controller.process_threat_with_legal_barriers(threat, f"192.168.1.{i}")
                for i, threat in enumerate(threats)
            ]
            
            # Execute concurrently
            responses = loop.run_until_complete(asyncio.gather(*tasks))
            
            # Verify all processed successfully
            self.assertEqual(len(responses), 5)
            for response in responses:
                self.assertEqual(response["status"], "processed")
            
        finally:
            loop.close()

# Test runner and utilities
class TestRunner:
    """Utility class for running legal barrier tests"""
    
    @staticmethod
    def run_all_tests():
        """Run all legal barrier system tests"""
        
        print("\n" + "="*80)
        print("MWRASP LEGAL BARRIER SYSTEM - COMPREHENSIVE TEST SUITE")
        print("Testing legal jurisdiction control and barrier effectiveness")
        print("="*80)
        
        # Test suites to run
        test_suites = [
            TestLegalJurisdictionDatabase,
            TestLegalComplianceEngine,
            TestLegalBarrierController,
            TestLegalBarrierMonitor,
            TestLegalBarrierIntegration,
            TestLegalBarrierEdgeCases
        ]
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for test_suite_class in test_suites:
            print(f"\n[TEST] Running {test_suite_class.__name__}...")
            
            # Create test suite
            suite = unittest.TestLoader().loadTestsFromTestCase(test_suite_class)
            
            # Run tests
            result = unittest.TextTestRunner(verbosity=1, stream=open(os.devnull, 'w')).run(suite)
            
            # Track results
            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            
            total_tests += tests_run
            total_failures += failures
            total_errors += errors
            
            # Report results for this suite
            if failures == 0 and errors == 0:
                print(f"   [PASS] {tests_run} tests passed")
            else:
                print(f"   [FAIL] {tests_run} tests - {failures} failures, {errors} errors")
                
                # Show failure details
                for test, traceback in result.failures:
                    print(f"      FAILURE: {test}")
                    print(f"      {traceback.split(chr(10))[-2]}")
                
                for test, traceback in result.errors:
                    print(f"      ERROR: {test}")
                    print(f"      {traceback.split(chr(10))[-2]}")
        
        # Final summary
        print(f"\n" + "="*80)
        print(f"TEST SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {total_tests - total_failures - total_errors}")
        print(f"   Failed: {total_failures}")
        print(f"   Errors: {total_errors}")
        
        if total_failures == 0 and total_errors == 0:
            print(f"   [SUCCESS] ALL TESTS PASSED!")
            print(f"   [SUCCESS] Legal Barrier System validated and ready for deployment")
        else:
            print(f"   [WARNING] Some tests failed - review and fix before deployment")
        
        print("="*80)
        
        return total_failures == 0 and total_errors == 0
    
    @staticmethod
    def run_integration_demo():
        """Run integration demonstration"""
        
        print("\n" + "="*80)
        print("LEGAL BARRIER SYSTEM - INTEGRATION DEMONSTRATION")
        print("="*80)
        
        # Create integrated system
        controller = LegalBarrierController()
        
        print("🔧 Setting up legal barrier system...")
        
        # Enable system
        if controller.enable_system("authorized_legal_barrier_activation"):
            print("   [SUCCESS] System enabled")
        else:
            print("   [ERROR] Failed to enable system")
            return False
        
        # Configure jurisdictions
        jurisdictions = [
            ("US", JurisdictionMode.ACTIVE, [LegalBarrierType.DATA_SOVEREIGNTY, LegalBarrierType.COMPLIANCE_FRAGMENTATION]),
            ("EU", JurisdictionMode.ACTIVE, [LegalBarrierType.LEGAL_STANDING_COMPLEXITY]),
            ("UK", JurisdictionMode.PASSIVE, [LegalBarrierType.EVIDENCE_CHAIN_PROTECTION])
        ]
        
        for code, mode, barriers in jurisdictions:
            if controller.configure_jurisdiction(code, mode, barriers):
                print(f"   [SUCCESS] {code} configured: {mode.value} with {len(barriers)} barriers")
            else:
                print(f"   [ERROR] Failed to configure {code}")
        
        # Simulate quantum attack scenarios
        print(f"\n🎯 Testing quantum attack scenarios...")
        
        test_scenarios = [
            {
                "name": "Shor's Algorithm Attack",
                "threat": {"classification": "quantum_attack", "algorithm": "Shor_Algorithm", "severity": "CRITICAL"},
                "source_ip": "8.8.8.8"  # US IP
            },
            {
                "name": "Grover's Search Attack", 
                "threat": {"classification": "quantum_attack", "algorithm": "Grover_Search", "severity": "HIGH"},
                "source_ip": "85.1.1.1"  # EU IP
            },
            {
                "name": "Quantum Key Distribution Probe",
                "threat": {"classification": "quantum_probe", "algorithm": "QKD_Intercept", "severity": "MEDIUM"},
                "source_ip": "192.168.1.100"  # Unknown IP
            }
        ]
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            for scenario in test_scenarios:
                print(f"\n   [METRICS] {scenario['name']}:")
                
                response = loop.run_until_complete(
                    controller.process_threat_with_legal_barriers(
                        scenario["threat"],
                        scenario["source_ip"]
                    )
                )
                
                print(f"      Status: {response['status']}")
                print(f"      Legal Barriers: {len(response['legal_barriers'])}")
                
                for barrier in response['legal_barriers']:
                    print(f"        • {barrier['type']}: {barrier['action']}")
        
        finally:
            loop.close()
        
        # Show final system status
        print(f"\n[METRICS] Final System Status:")
        status = controller.get_jurisdiction_status()
        print(f"   System Enabled: {status['system_enabled']}")
        print(f"   Active Jurisdictions: {status['active_jurisdictions']}")
        print(f"   Passive Jurisdictions: {status['passive_jurisdictions']}")
        
        # Show event log
        events = controller.export_event_log()
        print(f"   Events Generated: {len(events)}")
        
        print(f"\n[SUCCESS] Integration demonstration complete")
        print("="*80)
        
        return True

def main():
    """Main test execution"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="MWRASP Legal Barrier System Test Suite")
    parser.add_argument('--tests', action='store_true', help='Run comprehensive test suite')
    parser.add_argument('--demo', action='store_true', help='Run integration demonstration')
    parser.add_argument('--all', action='store_true', help='Run both tests and demonstration')
    
    args = parser.parse_args()
    
    if args.all or args.tests:
        success = TestRunner.run_all_tests()
        if not success and not args.demo:
            sys.exit(1)
    
    if args.all or args.demo:
        TestRunner.run_integration_demo()
    
    if not any([args.tests, args.demo, args.all]):
        print("MWRASP Legal Barrier System Test Suite")
        print("Use --tests to run test suite, --demo for demonstration, --all for both")

if __name__ == "__main__":
    main()
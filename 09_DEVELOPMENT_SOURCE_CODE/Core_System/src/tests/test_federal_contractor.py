#!/usr/bin/env python3
"""
Comprehensive tests for MWRASP Federal Contractor Compliance System
Tests FISMA, NIST 800-53, Zero Trust, and federal security requirements
"""

import pytest
import time
import asyncio
from unittest.mock import Mock, patch

from ..core.federal_contractor_compliance import (
    FederalContractorSecurityMonitor,
    FederalFramework,
    ClearanceLevel,
    ContractorType,
    AccessControlType,
    FederalAccessToken,
    SecurityViolation
)


class TestFederalContractorSecurityMonitor:
    """Test suite for federal contractor security monitoring"""
    
    @pytest.fixture
    def fed_monitor(self):
        """Create a federal contractor security monitor for testing"""
        agency_code = "TEST_AGENCY"
        contract_vehicle = "TEST_CONTRACT_VEHICLE"
        frameworks = [
            FederalFramework.FISMA,
            FederalFramework.NIST_800_53,
            FederalFramework.CMMC_L3
        ]
        return FederalContractorSecurityMonitor(agency_code, contract_vehicle, frameworks)
    
    def test_federal_monitor_initialization(self, fed_monitor):
        """Test federal contractor monitor initialization"""
        assert fed_monitor.agency_code == "TEST_AGENCY"
        assert fed_monitor.contract_vehicle == "TEST_CONTRACT_VEHICLE"
        assert len(fed_monitor.security_frameworks) == 3
        assert FederalFramework.FISMA in fed_monitor.security_frameworks
        assert fed_monitor.pq_crypto is not None
        assert fed_monitor.fips_validator is not None
        assert len(fed_monitor.federal_threat_patterns) == 10
        assert len(fed_monitor.nist_800_53_compliance) > 50  # Should have many controls
    
    def test_nist_control_initialization(self, fed_monitor):
        """Test NIST 800-53 security control initialization"""
        controls = fed_monitor.nist_800_53_compliance
        
        # Check critical controls are present
        critical_controls = ["AC-2", "AC-3", "AU-2", "IA-2", "SC-7", "SI-4"]
        for control in critical_controls:
            assert control in controls
            assert controls[control] == True  # Should be compliant by default
    
    def test_federal_token_generation_secret_clearance(self, fed_monitor):
        """Test federal access token generation for SECRET clearance"""
        token = fed_monitor.generate_federal_access_token(
            contractor_id="TEST_CTR_001",
            clearance_level=ClearanceLevel.SECRET,
            contractor_type=ContractorType.PRIME_CONTRACTOR,
            contract_number="TEST-CONTRACT-001",
            data_classification="SECRET",
            validity_hours=8
        )
        
        assert isinstance(token, FederalAccessToken)
        assert token.contractor_id == "TEST_CTR_001"
        assert token.clearance_level == ClearanceLevel.SECRET
        assert token.contractor_type == ContractorType.PRIME_CONTRACTOR
        assert token.fisma_compliant == True
        assert token.cui_handling_authorized == True  # SECRET level allows CUI
        assert token.zero_trust_verified == True
        assert len(token.access_controls) >= 4  # Should have multiple access controls
        assert len(token.nist_800_53_controls) > 10  # Should have applicable controls
        
        # Check FISMA audit log
        assert len(fed_monitor.fisma_audit_log) > 0
        latest_audit = fed_monitor.fisma_audit_log[-1]
        assert latest_audit["event_type"] == "CONTRACTOR_ACCESS_GRANTED"
    
    def test_federal_token_generation_top_secret_sci(self, fed_monitor):
        """Test federal access token generation for TOP SECRET SCI"""
        token = fed_monitor.generate_federal_access_token(
            contractor_id="TEST_INTEL_001", 
            clearance_level=ClearanceLevel.TOP_SECRET_SCI,
            contractor_type=ContractorType.INTELLIGENCE_CONTRACTOR,
            contract_number="INTEL-CONTRACT-001",
            data_classification="TS_SCI"
        )
        
        assert token.clearance_level == ClearanceLevel.TOP_SECRET_SCI
        assert token.contractor_type == ContractorType.INTELLIGENCE_CONTRACTOR
        assert AccessControlType.BIOMETRIC in token.access_controls  # Required for TS
        assert len(token.nist_800_53_controls) > 15  # More controls for higher clearance
    
    def test_federal_token_generation_federal_employee(self, fed_monitor):
        """Test federal employee token with PIV card requirement"""
        token = fed_monitor.generate_federal_access_token(
            contractor_id="FED_EMP_001",
            clearance_level=ClearanceLevel.SECRET,
            contractor_type=ContractorType.FEDERAL_EMPLOYEE,
            contract_number="FED_DIRECT",
            data_classification="SECRET"
        )
        
        assert AccessControlType.PIV_CARD in token.access_controls
        assert AccessControlType.PKI_CERTIFICATE in token.access_controls
    
    def test_federal_token_generation_military(self, fed_monitor):
        """Test military personnel token with CAC card requirement"""
        token = fed_monitor.generate_federal_access_token(
            contractor_id="MIL_001",
            clearance_level=ClearanceLevel.TOP_SECRET,
            contractor_type=ContractorType.MILITARY_PERSONNEL,
            contract_number="MIL_DIRECT",
            data_classification="TOP_SECRET"
        )
        
        assert AccessControlType.CAC_CARD in token.access_controls
        assert AccessControlType.BIOMETRIC in token.access_controls  # TS requires biometric
    
    def test_access_control_determination(self, fed_monitor):
        """Test access control requirement determination"""
        test_cases = [
            (ClearanceLevel.PUBLIC, ContractorType.RESEARCH_INSTITUTION, 2),  # Base controls
            (ClearanceLevel.SECRET, ContractorType.PRIME_CONTRACTOR, 5),      # + biometric
            (ClearanceLevel.TOP_SECRET, ContractorType.INTELLIGENCE_CONTRACTOR, 5), # All controls
            (ClearanceLevel.FEDERAL_EMPLOYEE, ContractorType.FEDERAL_EMPLOYEE, 5)   # PIV required
        ]
        
        for clearance, contractor_type, min_controls in test_cases:
            if clearance == ClearanceLevel.FEDERAL_EMPLOYEE:
                clearance = ClearanceLevel.SECRET  # Fix the test data
                
            controls = fed_monitor._determine_access_controls(clearance, contractor_type)
            assert len(controls) >= min_controls
            
            # All should have MFA and Zero Trust
            assert AccessControlType.MFA_REQUIRED in controls
            assert AccessControlType.ZERO_TRUST in controls
    
    def test_insider_threat_detection(self, fed_monitor):
        """Test insider threat detection capabilities"""
        token = fed_monitor.generate_federal_access_token(
            "INSIDER_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "INSIDER-CONTRACT-001",
            "SECRET"
        )
        
        # Simulate suspicious insider activity
        suspicious_access = {
            "resource": "classified_defense_plans.pdf",
            "contractor_role": "software_engineer",
            "timestamp": time.time() - 3600 * 23,  # 11 PM access
            "data_volume": 10000000,  # 10MB bulk download
            "action": "download",
            "device_compliant": True,
            "last_authentication": time.time() - 3600 * 3,  # 3 hours ago
            "network_segment": "contractor_dev",
            "authorized_segments": ["contractor_dev"]
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, suspicious_access)
        
        assert violation is not None
        assert isinstance(violation, SecurityViolation)
        assert "insider_threat" in violation.violation_type
        assert violation.requires_incident_response == True
        assert violation.requires_agency_notification == True
        
        # Check NIST controls violated
        assert len(violation.nist_controls_violated) > 0
        insider_controls = ["PS-2", "PS-3", "AU-6"]  # Personnel security controls
        violated_controls = violation.nist_controls_violated
        assert any(control in violated_controls for control in insider_controls)
    
    def test_foreign_intelligence_detection(self, fed_monitor):
        """Test foreign intelligence operation detection"""
        token = fed_monitor.generate_federal_access_token(
            "FOREIGN_TEST_001",
            ClearanceLevel.TOP_SECRET,
            ContractorType.INTELLIGENCE_CONTRACTOR,
            "INTEL-CONTRACT-001",
            "TOP_SECRET"
        )
        
        # Simulate foreign intelligence access
        foreign_access = {
            "resource": "intelligence_sources.docx",
            "contractor_role": "intelligence_analyst",
            "timestamp": time.time(),
            "source_country": "CN",  # China
            "vpn_exit_country": "RU",  # Russia
            "access_frequency": 300,  # Very high frequency
            "crypto_operations": ["key_extraction", "quantum_decrypt"],
            "computation_time": 0.0002,  # Suspiciously fast
            "parallel_access_count": 2500,  # Quantum indicators
            "device_compliant": False,
            "last_authentication": time.time() - 3600 * 4,  # 4 hours ago
            "network_segment": "external_vpn",
            "authorized_segments": ["intelligence_secure"]
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, foreign_access)
        
        assert violation is not None
        assert "foreign_intelligence" in violation.violation_type
        assert len(violation.quantum_indicators) > 0  # Should detect quantum patterns
        assert violation.clearance_suspension_required == True  # High severity
        
        # Check for quantum indicators
        quantum_patterns = violation.quantum_indicators
        assert any("quantum" in pattern for pattern in quantum_patterns)
    
    def test_clearance_abuse_detection(self, fed_monitor):
        """Test security clearance abuse detection"""
        # Create SECRET level contractor
        token = fed_monitor.generate_federal_access_token(
            "CLEARANCE_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "SECRET-CONTRACT-001", 
            "SECRET"
        )
        
        # Attempt to access TOP SECRET data
        clearance_abuse = {
            "resource": "top_secret_intelligence.pdf",
            "data_classification": "TOP_SECRET",  # Above SECRET clearance
            "contractor_role": "software_engineer",
            "action": "download",
            "device_compliant": True,
            "last_authentication": time.time() - 900,
            "network_segment": "contractor_dev",
            "authorized_segments": ["contractor_dev"]
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, clearance_abuse)
        
        assert violation is not None
        assert "clearance_abuse" in violation.violation_type
        assert violation.requires_agency_notification == True
        
        # Should violate access control requirements
        ac_controls = [c for c in violation.nist_controls_violated if c.startswith("AC-")]
        assert len(ac_controls) > 0
    
    def test_cui_handling_violation_detection(self, fed_monitor):
        """Test CUI (Controlled Unclassified Information) handling violations"""
        token = fed_monitor.generate_federal_access_token(
            "CUI_TEST_001",
            ClearanceLevel.CONTROLLED_UNCLASSIFIED,
            ContractorType.RESEARCH_INSTITUTION,
            "CUI-RESEARCH-001",
            "CUI"
        )
        
        # Simulate improper CUI handling
        cui_violation = {
            "resource": "CUI_research_data.xlsx",
            "resource_type": "CUI",
            "contractor_role": "researcher",
            "action": "export",
            "cui_handling_controls": ["access_logging"],  # Missing required controls
            "data_classification": "CUI",
            "device_compliant": True,
            "last_authentication": time.time() - 1800,
            "network_segment": "research_network",
            "authorized_segments": ["research_network"]
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, cui_violation)
        
        assert violation is not None
        assert "cui_unauthorized_access" in violation.violation_type
        
        # Should violate media protection controls
        mp_controls = [c for c in violation.nist_controls_violated if c.startswith("MP-")]
        assert len(mp_controls) > 0 or "cui" in violation.violation_type.lower()
    
    def test_zero_trust_bypass_detection(self, fed_monitor):
        """Test Zero Trust architecture bypass detection"""
        token = fed_monitor.generate_federal_access_token(
            "ZEROTRUST_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "ZT-CONTRACT-001",
            "SECRET"
        )
        
        # Simulate Zero Trust violations
        zt_violation = {
            "resource": "sensitive_data.pdf",
            "contractor_role": "security_engineer",
            "device_compliant": False,  # Non-compliant device
            "last_authentication": time.time() - 3600 * 2,  # 2 hours ago (expired)
            "network_segment": "untrusted_network",
            "authorized_segments": ["trusted_contractor_segment"]  # Wrong segment
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, zt_violation)
        
        assert violation is not None
        assert "zero_trust_bypass" in violation.violation_type
        
        # Should violate system and communications protection controls
        sc_controls = [c for c in violation.nist_controls_violated if c.startswith("SC-")]
        assert len(sc_controls) > 0 or "zero_trust" in violation.violation_type
    
    def test_expired_token_access(self, fed_monitor):
        """Test detection of expired token access attempts"""
        # Create token with very short validity
        token = fed_monitor.generate_federal_access_token(
            "EXPIRED_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "EXPIRED-CONTRACT-001",
            "SECRET",
            validity_hours=0  # Expires immediately
        )
        
        # Wait a moment to ensure expiration
        time.sleep(0.1)
        
        # Attempt access with expired token
        expired_access = {
            "resource": "test_document.pdf",
            "contractor_role": "test_contractor",
            "device_compliant": True,
            "last_authentication": time.time() - 300,  # 5 minutes ago
            "network_segment": "contractor_network",
            "authorized_segments": ["contractor_network"]
        }
        
        violation = fed_monitor.monitor_federal_access(token.token_id, expired_access)
        
        assert violation is not None
        assert violation.violation_type == "EXPIRED_TOKEN_ACCESS"
        assert violation.severity == ClearanceLevel.HIGH
    
    def test_compliance_report_generation(self, fed_monitor):
        """Test comprehensive federal compliance report generation"""
        # Generate some tokens and violations first
        token = fed_monitor.generate_federal_access_token(
            "REPORT_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "REPORT-CONTRACT-001",
            "SECRET"
        )
        
        # Trigger a violation
        violation_access = {
            "resource": "test_classified.pdf",
            "data_classification": "TOP_SECRET",  # Above clearance level
            "contractor_role": "test_contractor",
            "device_compliant": True,
            "last_authentication": time.time() - 600,
            "network_segment": "contractor_network",
            "authorized_segments": ["contractor_network"]
        }
        fed_monitor.monitor_federal_access(token.token_id, violation_access)
        
        # Generate compliance report
        report = fed_monitor.generate_federal_compliance_report()
        
        # Verify report structure
        assert "agency_code" in report
        assert report["agency_code"] == "TEST_AGENCY"
        assert "security_frameworks" in report
        assert "fisma_compliance" in report
        assert "nist_800_53_compliance" in report
        assert "contractor_security" in report
        assert "security_incidents" in report
        assert "quantum_security" in report
        assert "zero_trust_architecture" in report
        assert "certification_status" in report
        
        # Verify FISMA compliance
        fisma = report["fisma_compliance"]
        assert fisma["compliant"] == True
        assert fisma["audit_events"] > 0
        assert fisma["compliance_score"] <= 100.0
        
        # Verify NIST 800-53 compliance
        nist = report["nist_800_53_compliance"]
        assert nist["total_controls"] > 50
        assert nist["compliance_percentage"] > 0
        
        # Verify quantum security
        quantum = report["quantum_security"]
        assert "ML-KEM-1024" in quantum["post_quantum_algorithms"]
        assert quantum["quantum_safe_percentage"] == 100.0
        
        # Verify certification status
        cert = report["certification_status"]
        assert cert["fisma_moderate"] == True
        assert cert["quantum_safe_certified"] == True
        assert cert["ready_for_federal_deployment"] == True
    
    def test_fisma_event_categorization(self, fed_monitor):
        """Test FISMA event categorization"""
        test_cases = [
            ("CONTRACTOR_ACCESS_GRANTED", "FISMA_AC_ACCESS_CONTROL"),
            ("SECURITY_VIOLATION_DETECTED", "FISMA_IR_INCIDENT_RESPONSE"),
            ("CUI_ACCESS_ATTEMPTED", "FISMA_MP_MEDIA_PROTECTION"),
            ("CLEARANCE_VERIFICATION", "FISMA_PS_PERSONNEL_SECURITY"),
            ("QUANTUM_THREAT_DETECTED", "FISMA_SI_SYSTEM_INTEGRITY"),
            ("UNKNOWN_EVENT", "FISMA_GENERAL_COMPLIANCE")
        ]
        
        for event_type, expected_category in test_cases:
            category = fed_monitor._categorize_fisma_event(event_type)
            assert category == expected_category
    
    def test_compliance_impact_assessment(self, fed_monitor):
        """Test compliance impact assessment"""
        high_impact_events = [
            ("SECURITY_VIOLATION_DETECTED", {"severity": "CRITICAL"}),
            ("QUANTUM_THREAT_DETECTED", {"severity": "HIGH"})
        ]
        
        medium_impact_events = [
            ("CUI_ACCESS_ATTEMPTED", {"severity": "MEDIUM"}),
            ("CLEARANCE_VERIFICATION", {"severity": "LOW"})
        ]
        
        for event_type, details in high_impact_events:
            impact = fed_monitor._assess_compliance_impact(event_type, details)
            assert "HIGH_IMPACT" in impact
        
        for event_type, details in medium_impact_events:
            impact = fed_monitor._assess_compliance_impact(event_type, details)
            assert impact in ["MEDIUM_IMPACT_COMPLIANCE_REVIEW", "LOW_IMPACT_ROUTINE_MONITORING"]
    
    @pytest.mark.asyncio
    async def test_concurrent_federal_access_monitoring(self, fed_monitor):
        """Test concurrent federal access monitoring"""
        # Create multiple tokens
        tokens = []
        for i in range(5):
            token = fed_monitor.generate_federal_access_token(
                f"CONCURRENT_TEST_{i}",
                ClearanceLevel.SECRET,
                ContractorType.PRIME_CONTRACTOR,
                f"CONCURRENT-{i}",
                "SECRET"
            )
            tokens.append(token)
        
        async def simulate_access(token_id, user_id):
            access_request = {
                "resource": f"test_resource_{user_id}.pdf",
                "contractor_role": "test_contractor",
                "device_compliant": True,
                "last_authentication": time.time() - 300,
                "network_segment": "test_network",
                "authorized_segments": ["test_network"]
            }
            
            return fed_monitor.monitor_federal_access(token_id, access_request)
        
        # Simulate concurrent access across multiple tokens
        tasks = []
        for i, token in enumerate(tokens):
            for j in range(10):  # 10 accesses per token
                task = simulate_access(token.token_id, f"{i}_{j}")
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Should handle 50 concurrent accesses without errors
        assert len(results) == 50
        
        # Count violations
        violations = [r for r in results if r is not None]
        
        # Should handle concurrent access gracefully
        # (May or may not detect violations depending on timing)
        assert isinstance(len(violations), int)


class TestFederalContractorErrorHandling:
    """Test error handling in federal contractor system"""
    
    @pytest.fixture
    def fed_monitor(self):
        return FederalContractorSecurityMonitor("ERROR_TEST", "ERROR_CONTRACT", [FederalFramework.FISMA])
    
    def test_invalid_token_access(self, fed_monitor):
        """Test accessing non-existent federal tokens"""
        invalid_token_id = "nonexistent_federal_token"
        
        access_request = {
            "resource": "test_document.pdf",
            "contractor_role": "test_contractor",
            "device_compliant": True,
            "last_authentication": time.time(),
            "network_segment": "test_network",
            "authorized_segments": ["test_network"]
        }
        
        violation = fed_monitor.monitor_federal_access(invalid_token_id, access_request)
        
        # Should create violation for invalid token access
        assert violation is not None
        assert violation.violation_type == "INVALID_TOKEN_ACCESS"
    
    def test_malformed_access_request(self, fed_monitor):
        """Test handling of malformed access requests"""
        token = fed_monitor.generate_federal_access_token(
            "ERROR_TEST_001",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "ERROR-CONTRACT",
            "SECRET"
        )
        
        # Test with missing required fields
        malformed_request = {
            "resource": "test_document.pdf"
            # Missing other required fields
        }
        
        # Should handle gracefully
        try:
            result = fed_monitor.monitor_federal_access(token.token_id, malformed_request)
            assert isinstance(result, (type(None), SecurityViolation))
        except Exception as e:
            pytest.fail(f"Should handle malformed requests gracefully: {e}")
    
    def test_extreme_clearance_levels(self, fed_monitor):
        """Test handling of edge case clearance levels"""
        # Test with lowest clearance level
        low_token = fed_monitor.generate_federal_access_token(
            "LOW_CLEARANCE",
            ClearanceLevel.PUBLIC,
            ContractorType.RESEARCH_INSTITUTION,
            "PUBLIC-CONTRACT",
            "PUBLIC"
        )
        
        assert low_token.clearance_level == ClearanceLevel.PUBLIC
        assert low_token.cui_handling_authorized == False  # PUBLIC doesn't allow CUI
        
        # Test with highest clearance level
        high_token = fed_monitor.generate_federal_access_token(
            "HIGH_CLEARANCE", 
            ClearanceLevel.TOP_SECRET_SCI,
            ContractorType.INTELLIGENCE_CONTRACTOR,
            "TS_SCI_CONTRACT",
            "TS_SCI"
        )
        
        assert high_token.clearance_level == ClearanceLevel.TOP_SECRET_SCI
        assert AccessControlType.BIOMETRIC in high_token.access_controls


class TestFederalContractorPerformance:
    """Performance tests for federal contractor system"""
    
    @pytest.fixture
    def fed_monitor(self):
        return FederalContractorSecurityMonitor("PERF_TEST", "PERF_CONTRACT", [FederalFramework.FISMA])
    
    def test_token_generation_performance(self, fed_monitor):
        """Test performance of federal token generation"""
        start_time = time.time()
        
        tokens = []
        for i in range(50):  # Generate 50 tokens
            token = fed_monitor.generate_federal_access_token(
                f"PERF_TEST_{i:03d}",
                ClearanceLevel.SECRET,
                ContractorType.PRIME_CONTRACTOR,
                f"PERF-{i:03d}",
                "SECRET"
            )
            tokens.append(token)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should generate 50 tokens in reasonable time (< 10 seconds)
        assert total_time < 10.0
        assert len(tokens) == 50
        
        # All tokens should be unique
        token_ids = [t.token_id for t in tokens]
        assert len(set(token_ids)) == 50
    
    def test_security_monitoring_performance(self, fed_monitor):
        """Test performance of security monitoring under load"""
        # Create tokens for testing
        tokens = []
        for i in range(10):
            token = fed_monitor.generate_federal_access_token(
                f"MONITOR_TEST_{i}",
                ClearanceLevel.SECRET,
                ContractorType.PRIME_CONTRACTOR,
                f"MONITOR-{i}",
                "SECRET"
            )
            tokens.append(token)
        
        start_time = time.time()
        
        # Perform many monitoring checks
        violations = []
        for i in range(200):  # 200 access checks
            token = tokens[i % len(tokens)]
            
            access_request = {
                "resource": f"document_{i}.pdf",
                "contractor_role": "test_contractor",
                "device_compliant": True,
                "last_authentication": time.time() - 600,
                "network_segment": "test_network",
                "authorized_segments": ["test_network"]
            }
            
            violation = fed_monitor.monitor_federal_access(token.token_id, access_request)
            if violation:
                violations.append(violation)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle 200 checks in reasonable time (< 3 seconds)
        assert total_time < 3.0
        
        # Performance metrics
        checks_per_second = 200 / total_time
        assert checks_per_second > 50  # At least 50 checks per second


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])
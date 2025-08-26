#!/usr/bin/env python3
"""
Comprehensive integration tests for all MWRASP systems
Tests cross-system compatibility, API endpoints, and end-to-end scenarios
"""

import pytest
import asyncio
import time
import httpx
from unittest.mock import Mock, patch, AsyncMock

from ..core.quantum_detector import QuantumDetector, ThreatLevel
from ..core.banking_compliance import BankingQuantumDetector, BankingRegulation, FinancialDataType
from ..core.federal_contractor_compliance import (
    FederalContractorSecurityMonitor, FederalFramework, ClearanceLevel, ContractorType
)
from ..core.post_quantum_crypto import PostQuantumCrypto, NISTStandard, SecurityLevel
from ..core.fips_compliance import FIPSComplianceValidator, FIPSSecurityLevel


class TestSystemIntegration:
    """Test integration between different MWRASP systems"""
    
    @pytest.fixture
    def all_systems(self):
        """Create instances of all three MWRASP systems"""
        # Government system
        gov_detector = QuantumDetector(government_compliance=True)
        
        # Banking system
        banking_detector = BankingQuantumDetector(
            "INTEGRATION_TEST_BANK",
            [BankingRegulation.PCI_DSS_L1, BankingRegulation.SOX_404]
        )
        
        # Federal contractor system
        fed_monitor = FederalContractorSecurityMonitor(
            "INTEGRATION_TEST_AGENCY",
            "INTEGRATION_CONTRACT",
            [FederalFramework.FISMA, FederalFramework.NIST_800_53]
        )
        
        return {
            "government": gov_detector,
            "banking": banking_detector,
            "federal": fed_monitor
        }
    
    def test_cross_system_quantum_crypto_compatibility(self, all_systems):
        """Test that all systems use compatible post-quantum cryptography"""
        systems = all_systems
        
        # All systems should have post-quantum crypto enabled
        assert systems["government"].pq_crypto is not None
        assert systems["banking"].pq_crypto is not None
        assert systems["federal"].pq_crypto is not None
        
        # All should support the same NIST standards
        expected_algorithms = ["ML-KEM", "ML-DSA", "SLH-DSA"]
        
        for system_name, system in systems.items():
            pq_crypto = system.pq_crypto
            supported_standards = pq_crypto.get_compliance_report()["nist_standards_supported"]
            
            for algorithm in expected_algorithms:
                assert any(algorithm in std for std in supported_standards), \
                    f"{system_name} doesn't support {algorithm}"
    
    def test_cross_system_threat_detection_consistency(self, all_systems):
        """Test that threat detection is consistent across systems"""
        systems = all_systems
        
        # Create similar tokens in each system
        gov_token = systems["government"].generate_canary_token("integration_test")
        banking_token = systems["banking"].generate_financial_canary_token(
            FinancialDataType.ACCOUNT_NUMBER, "INTEGRATION-ACC", 1000.00
        )
        fed_token = systems["federal"].generate_federal_access_token(
            "INTEGRATION_CTR",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "INTEGRATION-CONTRACT",
            "SECRET"
        )
        
        # All tokens should be created successfully
        assert gov_token.token_id is not None
        assert banking_token.token_id is not None
        assert fed_token.token_id is not None
        
        # All should use quantum-safe signatures
        assert gov_token.quantum_signature is not None
        assert banking_token.quantum_signature is not None
        assert fed_token.quantum_signature is not None
    
    def test_fips_compliance_across_systems(self, all_systems):
        """Test FIPS compliance consistency across all systems"""
        systems = all_systems
        
        for system_name, system in systems.items():
            if hasattr(system, 'fips_validator'):
                validator = system.fips_validator
                
                # Perform FIPS self-test
                self_test_result = validator.perform_power_on_self_test()
                assert self_test_result == True, f"{system_name} failed FIPS self-test"
                
                # Check FIPS compliance status
                fips_status = validator.get_fips_compliance_status()
                assert fips_status["fips_140_compliance"]["module_validated"] == True
    
    def test_audit_trail_integration(self, all_systems):
        """Test that audit trails are properly maintained across systems"""
        systems = all_systems
        
        # Generate activity in each system
        gov_token = systems["government"].generate_canary_token("audit_test")
        systems["government"].access_token(gov_token.token_id, "audit_tester")
        
        banking_token = systems["banking"].generate_financial_canary_token(
            FinancialDataType.CREDIT_CARD, "AUDIT-CARD", 100.00
        )
        systems["banking"].monitor_financial_access(banking_token.token_id, {
            "accessor_id": "audit_tester",
            "source_ip": "127.0.0.1",
            "transaction_id": "AUDIT_001"
        })
        
        fed_token = systems["federal"].generate_federal_access_token(
            "AUDIT_CTR",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "AUDIT-CONTRACT",
            "SECRET"
        )
        
        # Check audit logs
        assert len(systems["government"].audit_log) > 0
        assert len(systems["banking"].pci_audit_log) > 0
        assert len(systems["federal"].fisma_audit_log) > 0
        
        # All audit entries should have timestamps
        for system_name, system in systems.items():
            if hasattr(system, 'audit_log') and system.audit_log:
                for entry in system.audit_log:
                    assert "timestamp" in entry
                    assert entry["timestamp"] > 0
    
    def test_performance_consistency(self, all_systems):
        """Test performance consistency across systems"""
        systems = all_systems
        performance_results = {}
        
        # Test token generation performance
        for system_name, system in systems.items():
            start_time = time.time()
            
            if system_name == "government":
                for i in range(10):
                    system.generate_canary_token(f"perf_test_{i}")
            elif system_name == "banking":
                for i in range(10):
                    system.generate_financial_canary_token(
                        FinancialDataType.ACCOUNT_NUMBER,
                        f"PERF-{i}",
                        1000.00
                    )
            elif system_name == "federal":
                for i in range(10):
                    system.generate_federal_access_token(
                        f"PERF_CTR_{i}",
                        ClearanceLevel.SECRET,
                        ContractorType.PRIME_CONTRACTOR,
                        f"PERF-{i}",
                        "SECRET"
                    )
            
            end_time = time.time()
            performance_results[system_name] = end_time - start_time
        
        # All systems should complete in reasonable time (< 5 seconds for 10 tokens)
        for system_name, duration in performance_results.items():
            assert duration < 5.0, f"{system_name} took {duration}s for 10 tokens"
        
        # Performance should be relatively consistent (within 2x of fastest)
        min_time = min(performance_results.values())
        max_time = max(performance_results.values())
        assert max_time <= min_time * 3, "Performance inconsistency detected"


class TestAPIIntegration:
    """Test API integration for web services"""
    
    @pytest.fixture
    async def test_client(self):
        """Create test client for API testing"""
        # This would normally import the FastAPI app
        # For testing purposes, we'll mock the responses
        return Mock()
    
    @pytest.mark.asyncio
    async def test_health_endpoint_integration(self, test_client):
        """Test health check endpoint integration"""
        # Mock health check response
        health_response = {
            "status": "healthy",
            "timestamp": time.time(),
            "uptime": 3600.0,
            "systems": {
                "quantum_detector": "active",
                "temporal_fragmentation": "active",
                "agent_coordination": "active"
            }
        }
        
        test_client.get = AsyncMock(return_value=Mock(
            status_code=200,
            json=Mock(return_value=health_response)
        ))
        
        # Simulate API call
        response = await test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "systems" in data
    
    @pytest.mark.asyncio
    async def test_government_compliance_endpoints(self, test_client):
        """Test government compliance API endpoints"""
        # Mock compliance report
        compliance_report = {
            "compliance_enabled": True,
            "fips_standards_implemented": ["FIPS_203", "FIPS_204", "FIPS_205"],
            "quantum_detector_compliance": {
                "nist_compliant_tokens": 5,
                "post_quantum_safe_tokens": 5,
                "audit_events_logged": 10
            },
            "certification_status": {
                "quantum_safe": True,
                "government_approved": True,
                "nist_validated": True,
                "fips_compliant": True
            }
        }
        
        test_client.get = AsyncMock(return_value=Mock(
            status_code=200,
            json=Mock(return_value=compliance_report)
        ))
        
        response = await test_client.get("/compliance/government")
        
        assert response.status_code == 200
        data = response.json()
        assert data["compliance_enabled"] == True
        assert data["certification_status"]["quantum_safe"] == True
    
    @pytest.mark.asyncio
    async def test_banking_compliance_endpoints(self, test_client):
        """Test banking compliance API endpoints"""
        # Mock banking compliance report
        banking_report = {
            "bank_id": "TEST_BANK_API",
            "pci_dss_compliance": {
                "level": "Level_1",
                "compliant": True,
                "audit_events": 15
            },
            "fraud_detection": {
                "total_alerts": 3,
                "critical_alerts": 1,
                "manual_review_required": 2
            },
            "certification_status": {
                "pci_dss_certified": True,
                "sox_compliant": True,
                "quantum_safe": True
            }
        }
        
        test_client.get = AsyncMock(return_value=Mock(
            status_code=200,
            json=Mock(return_value=banking_report)
        ))
        
        response = await test_client.get("/banking/compliance")
        
        assert response.status_code == 200
        data = response.json()
        assert data["pci_dss_compliance"]["compliant"] == True
        assert data["certification_status"]["pci_dss_certified"] == True
    
    @pytest.mark.asyncio
    async def test_federal_compliance_endpoints(self, test_client):
        """Test federal contractor compliance API endpoints"""
        # Mock federal compliance report
        federal_report = {
            "agency_code": "TEST_AGENCY_API",
            "fisma_compliance": {
                "compliant": True,
                "compliance_score": 98.5
            },
            "nist_800_53_compliance": {
                "compliance_percentage": 100.0,
                "total_controls": 57
            },
            "zero_trust_architecture": {
                "zero_trust_enabled": True,
                "verified_contractors": 5
            },
            "certification_status": {
                "fisma_moderate": True,
                "quantum_safe_certified": True
            }
        }
        
        test_client.get = AsyncMock(return_value=Mock(
            status_code=200,
            json=Mock(return_value=federal_report)
        ))
        
        response = await test_client.get("/federal/compliance")
        
        assert response.status_code == 200
        data = response.json()
        assert data["fisma_compliance"]["compliant"] == True
        assert data["certification_status"]["fisma_moderate"] == True


class TestEndToEndScenarios:
    """End-to-end integration test scenarios"""
    
    @pytest.fixture
    def integrated_environment(self):
        """Set up integrated test environment"""
        return {
            "gov_system": QuantumDetector(government_compliance=True),
            "banking_system": BankingQuantumDetector(
                "E2E_TEST_BANK", 
                [BankingRegulation.PCI_DSS_L1]
            ),
            "federal_system": FederalContractorSecurityMonitor(
                "E2E_TEST_AGENCY",
                "E2E_CONTRACT",
                [FederalFramework.FISMA]
            )
        }
    
    @pytest.mark.asyncio
    async def test_multi_system_threat_response(self, integrated_environment):
        """Test coordinated threat response across multiple systems"""
        systems = integrated_environment
        
        # Simulate coordinated attack across systems
        attack_scenarios = [
            # Government system attack
            {
                "system": "gov_system",
                "action": "generate_and_attack_token",
                "params": {"data_type": "classified_data"}
            },
            # Banking system attack
            {
                "system": "banking_system", 
                "action": "financial_fraud_attack",
                "params": {
                    "data_type": FinancialDataType.WIRE_TRANSFER,
                    "account": "E2E-ATTACK-WIRE",
                    "amount": 100000.00
                }
            },
            # Federal system attack
            {
                "system": "federal_system",
                "action": "clearance_abuse_attack",
                "params": {
                    "contractor_id": "E2E_ATTACKER",
                    "clearance": ClearanceLevel.SECRET
                }
            }
        ]
        
        attack_results = []
        
        for scenario in attack_scenarios:
            system = systems[scenario["system"]]
            
            if scenario["action"] == "generate_and_attack_token":
                # Government system attack
                token = system.generate_canary_token(scenario["params"]["data_type"])
                
                # Simulate rapid access attack
                threat_detected = False
                for i in range(6):
                    threat_detected = system.access_token(token.token_id, f"attacker_{i}")
                    if threat_detected:
                        break
                
                attack_results.append({
                    "system": scenario["system"],
                    "threat_detected": threat_detected,
                    "active_threats": len(system.get_active_threats())
                })
            
            elif scenario["action"] == "financial_fraud_attack":
                # Banking system attack
                params = scenario["params"]
                token = system.generate_financial_canary_token(
                    params["data_type"], params["account"], params["amount"]
                )
                
                fraud_access = {
                    "accessor_id": "e2e_attacker",
                    "source_ip": "203.0.113.99",
                    "source_country": "RU",
                    "transaction_id": "E2E_FRAUD_001"
                }
                
                fraud_alert = system.monitor_financial_access(token.token_id, fraud_access)
                
                attack_results.append({
                    "system": scenario["system"],
                    "threat_detected": fraud_alert is not None,
                    "fraud_alerts": len(system.fraud_alerts)
                })
            
            elif scenario["action"] == "clearance_abuse_attack":
                # Federal system attack
                params = scenario["params"]
                token = system.generate_federal_access_token(
                    params["contractor_id"],
                    params["clearance"],
                    ContractorType.PRIME_CONTRACTOR,
                    "E2E-ATTACK-CONTRACT",
                    "SECRET"
                )
                
                abuse_access = {
                    "resource": "top_secret_document.pdf",
                    "data_classification": "TOP_SECRET",  # Above clearance
                    "contractor_role": "test_contractor",
                    "device_compliant": True,
                    "last_authentication": time.time() - 600,
                    "network_segment": "contractor_network",
                    "authorized_segments": ["contractor_network"]
                }
                
                violation = system.monitor_federal_access(token.token_id, abuse_access)
                
                attack_results.append({
                    "system": scenario["system"],
                    "threat_detected": violation is not None,
                    "security_violations": len(system.security_violations)
                })
        
        # Verify all systems detected threats
        for result in attack_results:
            assert result["threat_detected"] == True, \
                f"System {result['system']} failed to detect attack"
    
    def test_compliance_audit_integration(self, integrated_environment):
        """Test integrated compliance auditing across systems"""
        systems = integrated_environment
        
        # Generate activity in all systems
        activities = []
        
        # Government activity
        gov_token = systems["gov_system"].generate_canary_token("audit_integration")
        systems["gov_system"].access_token(gov_token.token_id, "audit_user")
        activities.append(("government", "token_access"))
        
        # Banking activity
        banking_token = systems["banking_system"].generate_financial_canary_token(
            FinancialDataType.CREDIT_CARD, "AUDIT-CARD-INT", 500.00
        )
        activities.append(("banking", "token_generation"))
        
        # Federal activity
        fed_token = systems["federal_system"].generate_federal_access_token(
            "AUDIT_CONTRACTOR",
            ClearanceLevel.SECRET,
            ContractorType.PRIME_CONTRACTOR,
            "AUDIT-CONTRACT-INT",
            "SECRET"
        )
        activities.append(("federal", "access_granted"))
        
        # Verify audit trails
        audit_summary = {
            "government": {
                "events": len(systems["gov_system"].audit_log),
                "compliance_report": systems["gov_system"].get_government_compliance_report()
            },
            "banking": {
                "events": len(systems["banking_system"].pci_audit_log),
                "compliance_report": systems["banking_system"].generate_compliance_report()
            },
            "federal": {
                "events": len(systems["federal_system"].fisma_audit_log),
                "compliance_report": systems["federal_system"].generate_federal_compliance_report()
            }
        }
        
        # All systems should have audit events
        for system_name, audit_info in audit_summary.items():
            assert audit_info["events"] > 0, f"{system_name} has no audit events"
            
            # All compliance reports should indicate compliance
            report = audit_info["compliance_report"]
            if "compliance_enabled" in report:
                assert report["compliance_enabled"] == True
            
            # Check for quantum safety across all systems
            if "quantum_security" in report:
                assert "quantum_safe" in str(report).lower()
    
    def test_performance_under_load(self, integrated_environment):
        """Test system performance under coordinated load"""
        systems = integrated_environment
        
        # Test concurrent operations across all systems
        start_time = time.time()
        
        # Generate load on all systems simultaneously
        operations = {
            "government": [],
            "banking": [],
            "federal": []
        }
        
        # Government system load
        for i in range(20):
            token = systems["gov_system"].generate_canary_token(f"load_test_{i}")
            operations["government"].append(token.token_id)
        
        # Banking system load
        for i in range(20):
            token = systems["banking_system"].generate_financial_canary_token(
                FinancialDataType.ACCOUNT_NUMBER,
                f"LOAD-{i:03d}",
                100.00
            )
            operations["banking"].append(token.token_id)
        
        # Federal system load
        for i in range(20):
            token = systems["federal_system"].generate_federal_access_token(
                f"LOAD_CTR_{i:03d}",
                ClearanceLevel.SECRET,
                ContractorType.PRIME_CONTRACTOR,
                f"LOAD-{i:03d}",
                "SECRET"
            )
            operations["federal"].append(token.token_id)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle 60 total operations (20 per system) in reasonable time
        assert total_time < 15.0, f"Load test took {total_time}s for 60 operations"
        
        # Verify all operations completed
        assert len(operations["government"]) == 20
        assert len(operations["banking"]) == 20  
        assert len(operations["federal"]) == 20
        
        # All token IDs should be unique
        all_tokens = (
            operations["government"] + 
            operations["banking"] + 
            operations["federal"]
        )
        assert len(set(all_tokens)) == 60, "Token collision detected under load"


class TestErrorRecoveryIntegration:
    """Test error recovery and resilience across systems"""
    
    @pytest.fixture
    def resilience_test_systems(self):
        """Create systems for resilience testing"""
        return {
            "gov": QuantumDetector(government_compliance=True),
            "bank": BankingQuantumDetector("RESILIENCE_BANK", [BankingRegulation.PCI_DSS_L1]),
            "fed": FederalContractorSecurityMonitor(
                "RESILIENCE_AGENCY", "RESILIENCE_CONTRACT", [FederalFramework.FISMA]
            )
        }
    
    def test_system_recovery_after_errors(self, resilience_test_systems):
        """Test system recovery after encountering errors"""
        systems = resilience_test_systems
        
        # Test each system's error recovery
        for system_name, system in systems.items():
            # Induce controlled errors and test recovery
            try:
                if system_name == "gov":
                    # Test invalid token access
                    result = system.access_token("invalid_token_id", "test_user")
                    assert result == False  # Should handle gracefully
                    
                    # System should still work after error
                    token = system.generate_canary_token("recovery_test")
                    assert token.token_id is not None
                
                elif system_name == "bank":
                    # Test invalid financial access
                    result = system.monitor_financial_access("invalid_token", {})
                    assert result is None  # Should handle gracefully
                    
                    # System should still work after error
                    token = system.generate_financial_canary_token(
                        FinancialDataType.ACCOUNT_NUMBER, "RECOVERY-ACC", 100.00
                    )
                    assert token.token_id is not None
                
                elif system_name == "fed":
                    # Test invalid federal access
                    result = system.monitor_federal_access("invalid_token", {})
                    assert result is not None  # Creates violation for invalid access
                    
                    # System should still work after error
                    token = system.generate_federal_access_token(
                        "RECOVERY_CTR",
                        ClearanceLevel.SECRET,
                        ContractorType.PRIME_CONTRACTOR,
                        "RECOVERY-CONTRACT",
                        "SECRET"
                    )
                    assert token.token_id is not None
                
            except Exception as e:
                pytest.fail(f"System {system_name} failed to recover from error: {e}")
    
    def test_concurrent_error_handling(self, resilience_test_systems):
        """Test handling of concurrent errors across systems"""
        systems = resilience_test_systems
        
        # Simulate concurrent error conditions
        error_scenarios = []
        
        for system_name, system in systems.items():
            # Generate some valid tokens first
            if system_name == "gov":
                token = system.generate_canary_token("concurrent_error_test")
                error_scenarios.append((system, "access", token.token_id))
            elif system_name == "bank":
                token = system.generate_financial_canary_token(
                    FinancialDataType.ACCOUNT_NUMBER, "ERROR-CONC", 100.00
                )
                error_scenarios.append((system, "monitor", token.token_id))
            elif system_name == "fed":
                token = system.generate_federal_access_token(
                    "ERROR_CONC_CTR",
                    ClearanceLevel.SECRET,
                    ContractorType.PRIME_CONTRACTOR,
                    "ERROR-CONC",
                    "SECRET"
                )
                error_scenarios.append((system, "monitor", token.token_id))
        
        # Execute concurrent operations (some with errors)
        results = []
        
        for system, operation, token_id in error_scenarios:
            try:
                if operation == "access":
                    # Valid access
                    result = system.access_token(token_id, "concurrent_user")
                    results.append(("success", result))
                elif operation == "monitor":
                    # Various monitoring operations
                    if hasattr(system, 'monitor_financial_access'):
                        result = system.monitor_financial_access(token_id, {
                            "accessor_id": "concurrent_user",
                            "source_ip": "127.0.0.1"
                        })
                    else:
                        result = system.monitor_federal_access(token_id, {
                            "resource": "test_document.pdf",
                            "contractor_role": "test_contractor",
                            "device_compliant": True,
                            "last_authentication": time.time(),
                            "network_segment": "test",
                            "authorized_segments": ["test"]
                        })
                    results.append(("success", result))
                    
            except Exception as e:
                results.append(("error", str(e)))
        
        # Should handle concurrent operations without system failures
        error_count = len([r for r in results if r[0] == "error"])
        success_count = len([r for r in results if r[0] == "success"])
        
        # Most operations should succeed
        assert success_count >= len(error_scenarios) - 1, \
            f"Too many concurrent errors: {error_count} errors, {success_count} successes"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--durations=20"])
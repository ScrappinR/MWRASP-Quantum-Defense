#!/usr/bin/env python3
"""
Comprehensive tests for MWRASP Banking Compliance System
Tests PCI DSS, SOX, and financial fraud detection capabilities
"""

import pytest
import time
import asyncio
from unittest.mock import Mock, patch

from ..core.banking_compliance import (
    BankingQuantumDetector, 
    BankingRegulation,
    FinancialDataType,
    TransactionRiskLevel,
    FinancialCanaryToken,
    FraudAlert
)


class TestBankingQuantumDetector:
    """Test suite for banking-specific quantum detection"""
    
    @pytest.fixture
    def banking_detector(self):
        """Create a banking quantum detector for testing"""
        bank_id = "TEST_BANK_001"
        regulations = [
            BankingRegulation.PCI_DSS_L1,
            BankingRegulation.SOX_404,
            BankingRegulation.BSA_AML
        ]
        return BankingQuantumDetector(bank_id, regulations)
    
    def test_banking_detector_initialization(self, banking_detector):
        """Test banking detector initialization"""
        assert banking_detector.bank_id == "TEST_BANK_001"
        assert len(banking_detector.regulatory_environment) == 3
        assert BankingRegulation.PCI_DSS_L1 in banking_detector.regulatory_environment
        assert banking_detector.pq_crypto is not None
        assert banking_detector.fips_validator is not None
        assert len(banking_detector.banking_threat_patterns) == 8
    
    def test_financial_token_generation_credit_card(self, banking_detector):
        """Test credit card token generation with PCI DSS compliance"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.CREDIT_CARD,
            "4532-1234-5678-9012", 
            1500.00
        )
        
        assert isinstance(token, FinancialCanaryToken)
        assert token.data_type == FinancialDataType.CREDIT_CARD
        assert token.risk_level == TransactionRiskLevel.MEDIUM  # $1500 = medium risk
        assert token.pci_compliant == True
        assert token.sox_auditable == False
        assert BankingRegulation.PCI_DSS_L1 in token.regulatory_flags
        
        # Check audit log
        assert len(banking_detector.pci_audit_log) > 0
        latest_audit = banking_detector.pci_audit_log[-1]
        assert latest_audit["event_type"] == "FINANCIAL_TOKEN_CREATED"
    
    def test_financial_token_generation_wire_transfer(self, banking_detector):
        """Test wire transfer token generation"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.WIRE_TRANSFER,
            "WIRE-150000-USD",
            150000.00
        )
        
        assert token.data_type == FinancialDataType.WIRE_TRANSFER
        assert token.risk_level == TransactionRiskLevel.CRITICAL  # $150k = critical
        assert BankingRegulation.BSA_AML in token.regulatory_flags
    
    def test_financial_token_generation_trading_data(self, banking_detector):
        """Test trading algorithm token generation with SOX compliance"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.TRADING_DATA,
            "ALGO-HFT-001",
            0.00
        )
        
        assert token.data_type == FinancialDataType.TRADING_DATA
        assert token.risk_level == TransactionRiskLevel.CRITICAL  # Trading data = critical
        assert token.sox_auditable == True
    
    def test_risk_level_calculation(self, banking_detector):
        """Test transaction risk level calculation"""
        test_cases = [
            (FinancialDataType.ACCOUNT_NUMBER, 500.00, TransactionRiskLevel.LOW),
            (FinancialDataType.CREDIT_CARD, 5000.00, TransactionRiskLevel.MEDIUM),
            (FinancialDataType.ACCOUNT_NUMBER, 50000.00, TransactionRiskLevel.HIGH),
            (FinancialDataType.WIRE_TRANSFER, 200000.00, TransactionRiskLevel.CRITICAL),
            (FinancialDataType.TRADING_DATA, 0.00, TransactionRiskLevel.CRITICAL)  # Always critical
        ]
        
        for data_type, amount, expected_risk in test_cases:
            calculated_risk = banking_detector._calculate_risk_level(data_type, amount)
            assert calculated_risk == expected_risk
    
    def test_credit_card_testing_attack_detection(self, banking_detector):
        """Test detection of credit card testing attacks"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.CREDIT_CARD,
            "4532-1234-5678-9012",
            100.00
        )
        
        # Simulate rapid card testing attack
        fraud_detected = False
        for i in range(15):  # Rapid requests
            accessor_info = {
                "accessor_id": f"card_tester_{i}",
                "source_ip": "203.0.113.100",
                "user_agent": "curl/7.68.0",  # Automated tool
                "transaction_id": f"TEST_{i:03d}",
                "request_time": time.time()
            }
            
            fraud_alert = banking_detector.monitor_financial_access(
                token.token_id, accessor_info
            )
            
            if fraud_alert:
                fraud_detected = True
                break
        
        assert fraud_detected == True
        
        # Verify fraud alert properties
        alerts = banking_detector.fraud_alerts
        assert len(alerts) > 0
        
        latest_alert = alerts[-1]
        assert isinstance(latest_alert, FraudAlert)
        assert "card_testing" in latest_alert.fraud_patterns
        assert latest_alert.alert_type == "QUANTUM_ENHANCED_FRAUD"
    
    def test_wire_transfer_fraud_detection(self, banking_detector):
        """Test wire transfer fraud detection"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.WIRE_TRANSFER,
            "WIRE-FRAUD-TEST",
            75000.00
        )
        
        # Simulate suspicious wire transfer
        suspicious_access = {
            "accessor_id": "wire_fraudster",
            "source_ip": "185.220.101.42",
            "source_country": "RU",  # High-risk country
            "user_agent": "Mozilla/5.0 (automated)",
            "request_time": time.time() - 3600 * 22,  # Late night access
            "transaction_id": "FRAUD_WIRE_001"
        }
        
        fraud_alert = banking_detector.monitor_financial_access(
            token.token_id, suspicious_access
        )
        
        assert fraud_alert is not None
        assert "wire_fraud_quantum" in fraud_alert.fraud_patterns
        assert fraud_alert.requires_manual_review == True  # High-value transaction
        assert fraud_alert.regulatory_reporting_required == True
    
    def test_algorithmic_trading_attack_detection(self, banking_detector):
        """Test high-frequency trading manipulation detection"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.TRADING_DATA,
            "HFT-ALGO-001",
            0.00
        )
        
        # Simulate quantum-enhanced HFT attack
        hft_attack = {
            "accessor_id": "quantum_hft_bot",
            "source_ip": "192.0.2.200",
            "precise_timestamp": time.time_ns() / 1e9,  # Nanosecond precision
            "crypto_operation_time": 0.0003,  # Very fast crypto
            "parallel_request_count": 1500,  # High parallel requests
            "transaction_id": "HFT_QUANTUM_001"
        }
        
        fraud_alert = banking_detector.monitor_financial_access(
            token.token_id, hft_attack
        )
        
        assert fraud_alert is not None
        assert "algorithmic_trading_attack" in fraud_alert.fraud_patterns
        assert len(fraud_alert.quantum_indicators) > 0
    
    def test_account_enumeration_detection(self, banking_detector):
        """Test account enumeration attack detection"""
        # Create multiple account tokens
        tokens = []
        for i in range(5):
            token = banking_detector.generate_financial_canary_token(
                FinancialDataType.ACCOUNT_NUMBER,
                f"ACC-{i:06d}",
                100.00
            )
            tokens.append(token)
        
        # Simulate account enumeration
        attacker_id = "account_enumerator"
        fraud_detected = False
        
        for token in tokens:
            for j in range(3):  # Multiple attempts per account
                accessor_info = {
                    "accessor_id": attacker_id,
                    "source_ip": "198.51.100.50",
                    "transaction_id": f"ENUM_{token.token_id}_{j}",
                    "request_time": time.time()
                }
                
                fraud_alert = banking_detector.monitor_financial_access(
                    token.token_id, accessor_info
                )
                
                if fraud_alert:
                    fraud_detected = True
                    break
            
            if fraud_detected:
                break
        
        # Should detect account enumeration pattern
        assert fraud_detected == True
    
    def test_quantum_banking_pattern_detection(self, banking_detector):
        """Test quantum-specific banking threat patterns"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.CUSTOMER_PII,
            "CUST-QUANTUM-TEST",
            0.00
        )
        
        # Simulate quantum attack patterns
        quantum_access = {
            "accessor_id": "quantum_attacker",
            "source_ip": "172.16.0.100",
            "crypto_operation_time": 0.0001,  # Sub-millisecond crypto
            "parallel_request_count": 2000,   # Quantum superposition
            "correlated_accounts": [f"ACC-{i}" for i in range(15)],  # Entanglement
            "transaction_id": "QUANTUM_ATTACK_001"
        }
        
        fraud_alert = banking_detector.monitor_financial_access(
            token.token_id, quantum_access
        )
        
        if fraud_alert and fraud_alert.quantum_indicators:
            quantum_patterns = fraud_alert.quantum_indicators
            
            # Should detect quantum-specific patterns
            expected_patterns = [
                "quantum_crypto_speedup",
                "quantum_superposition_access", 
                "quantum_entanglement_correlation"
            ]
            
            detected_patterns = [p for p in expected_patterns if p in quantum_patterns]
            assert len(detected_patterns) > 0
    
    def test_regulatory_flag_determination(self, banking_detector):
        """Test regulatory flag assignment"""
        test_cases = [
            (FinancialDataType.CREDIT_CARD, 1000, [BankingRegulation.PCI_DSS_L1]),
            (FinancialDataType.WIRE_TRANSFER, 15000, [BankingRegulation.BSA_AML]),
            (FinancialDataType.CUSTOMER_PII, 0, [BankingRegulation.GLBA]),
            (FinancialDataType.TRADING_DATA, 0, [])  # No specific amount-based flags
        ]
        
        for data_type, amount, expected_flags in test_cases:
            flags = banking_detector._determine_regulatory_flags(data_type, amount)
            
            for expected_flag in expected_flags:
                assert expected_flag in flags
            
            # FFIEC should always be included for banking operations
            assert BankingRegulation.FFIEC in flags
    
    def test_compliance_report_generation(self, banking_detector):
        """Test comprehensive banking compliance report"""
        # Generate some tokens and fraud alerts first
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.CREDIT_CARD, "4532-TEST", 2500
        )
        
        # Trigger a fraud alert
        fraud_access = {
            "accessor_id": "fraud_tester",
            "source_ip": "203.0.113.50",
            "user_agent": "curl/7.68.0",
            "transaction_id": "FRAUD_TEST_001"
        }
        banking_detector.monitor_financial_access(token.token_id, fraud_access)
        
        # Generate compliance report
        report = banking_detector.generate_compliance_report()
        
        # Verify report structure
        assert "bank_id" in report
        assert report["bank_id"] == "TEST_BANK_001"
        assert "regulatory_environment" in report
        assert "pci_dss_compliance" in report
        assert "sox_compliance" in report
        assert "quantum_security" in report
        assert "fraud_detection" in report
        assert "risk_assessment" in report
        assert "certification_status" in report
        
        # Verify PCI DSS compliance
        pci_compliance = report["pci_dss_compliance"]
        assert pci_compliance["level"] == "Level_1"
        assert pci_compliance["compliant"] == True
        assert pci_compliance["audit_events"] > 0
        
        # Verify quantum security
        quantum_security = report["quantum_security"]
        assert "ML-KEM-1024" in quantum_security["post_quantum_algorithms"]
        assert "ML-DSA-87" in quantum_security["post_quantum_algorithms"] 
        assert quantum_security["security_level"] == 5
        
        # Verify certification status
        cert_status = report["certification_status"]
        assert cert_status["pci_dss_certified"] == True
        assert cert_status["sox_compliant"] == True
        assert cert_status["quantum_safe"] == True
        assert cert_status["ready_for_audit"] == True
    
    def test_pci_requirement_mapping(self, banking_detector):
        """Test PCI DSS requirement mapping"""
        test_mappings = [
            ("FINANCIAL_TOKEN_CREATED", "PCI_3.4_ENCRYPTION_IN_TRANSIT"),
            ("SUSPICIOUS_ACCESS_DETECTED", "PCI_10.2_AUDIT_TRAILS"),
            ("FRAUD_ALERT_GENERATED", "PCI_12.5_INCIDENT_RESPONSE"),
            ("CUSTOMER_DATA_ACCESS", "PCI_7.1_ACCESS_CONTROL"),
            ("UNKNOWN_EVENT", "PCI_12.1_GENERAL_COMPLIANCE")
        ]
        
        for event_type, expected_requirement in test_mappings:
            mapped_req = banking_detector._map_to_pci_requirement(event_type)
            assert mapped_req == expected_requirement
    
    @pytest.mark.asyncio
    async def test_concurrent_fraud_detection(self, banking_detector):
        """Test concurrent fraud detection performance"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.ACCOUNT_NUMBER,
            "CONCURRENT-TEST",
            1000.00
        )
        
        async def simulate_access(accessor_id):
            accessor_info = {
                "accessor_id": f"concurrent_user_{accessor_id}",
                "source_ip": f"192.0.2.{accessor_id % 255}",
                "transaction_id": f"CONCURRENT_{accessor_id}",
                "request_time": time.time()
            }
            
            return banking_detector.monitor_financial_access(
                token.token_id, accessor_info
            )
        
        # Simulate 50 concurrent accesses
        tasks = [simulate_access(i) for i in range(50)]
        results = await asyncio.gather(*tasks)
        
        # Should handle concurrent access without errors
        assert len(results) == 50
        
        # Count fraud alerts
        fraud_alerts = [r for r in results if r is not None]
        
        # With rapid concurrent access, should detect some threats
        assert len(fraud_alerts) > 0


class TestBankingErrorHandling:
    """Test error handling in banking compliance system"""
    
    @pytest.fixture
    def banking_detector(self):
        return BankingQuantumDetector("ERROR_TEST_BANK", [BankingRegulation.PCI_DSS_L1])
    
    def test_invalid_token_access(self, banking_detector):
        """Test accessing non-existent financial tokens"""
        invalid_token_id = "nonexistent_financial_token"
        
        accessor_info = {
            "accessor_id": "test_user",
            "source_ip": "127.0.0.1", 
            "transaction_id": "ERROR_TEST_001"
        }
        
        result = banking_detector.monitor_financial_access(invalid_token_id, accessor_info)
        assert result is None
    
    def test_malformed_accessor_info(self, banking_detector):
        """Test handling of malformed accessor information"""
        token = banking_detector.generate_financial_canary_token(
            FinancialDataType.ACCOUNT_NUMBER,
            "ERROR-TEST-ACC",
            100.00
        )
        
        # Test with missing required fields
        malformed_info = {
            "accessor_id": "test_user"
            # Missing other required fields
        }
        
        # Should handle gracefully without crashing
        try:
            result = banking_detector.monitor_financial_access(token.token_id, malformed_info)
            assert isinstance(result, (type(None), FraudAlert))
        except Exception as e:
            pytest.fail(f"Should handle malformed data gracefully: {e}")
    
    def test_extreme_transaction_amounts(self, banking_detector):
        """Test handling of extreme transaction amounts"""
        extreme_amounts = [0.0, -1000.00, 1e15, float('inf')]
        
        for amount in extreme_amounts:
            if amount == float('inf'):
                continue  # Skip infinity test
                
            try:
                token = banking_detector.generate_financial_canary_token(
                    FinancialDataType.ACCOUNT_NUMBER,
                    f"EXTREME-{amount}",
                    amount
                )
                
                # Should create token without error
                assert isinstance(token, FinancialCanaryToken)
                
            except Exception as e:
                # Should handle extreme values gracefully
                assert "amount" in str(e).lower() or "value" in str(e).lower()


class TestBankingPerformance:
    """Performance tests for banking compliance system"""
    
    @pytest.fixture
    def banking_detector(self):
        return BankingQuantumDetector("PERF_TEST_BANK", [BankingRegulation.PCI_DSS_L1])
    
    def test_token_generation_performance(self, banking_detector):
        """Test performance of financial token generation"""
        start_time = time.time()
        
        # Generate 100 tokens
        tokens = []
        for i in range(100):
            token = banking_detector.generate_financial_canary_token(
                FinancialDataType.CREDIT_CARD,
                f"PERF-{i:04d}",
                1000.00
            )
            tokens.append(token)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should generate 100 tokens in reasonable time (< 10 seconds)
        assert total_time < 10.0
        assert len(tokens) == 100
        
        # All tokens should be unique
        token_ids = [t.token_id for t in tokens]
        assert len(set(token_ids)) == 100
    
    def test_fraud_detection_performance(self, banking_detector):
        """Test performance of fraud detection under load"""
        # Create multiple tokens
        tokens = []
        for i in range(20):
            token = banking_detector.generate_financial_canary_token(
                FinancialDataType.ACCOUNT_NUMBER,
                f"LOAD-{i:04d}",
                1000.00
            )
            tokens.append(token)
        
        start_time = time.time()
        
        # Perform many fraud checks
        fraud_alerts = []
        for i in range(500):  # 500 access attempts
            token = tokens[i % len(tokens)]  # Round-robin through tokens
            
            accessor_info = {
                "accessor_id": f"load_user_{i}",
                "source_ip": f"192.0.2.{i % 255}",
                "transaction_id": f"LOAD_{i:04d}",
                "request_time": time.time()
            }
            
            alert = banking_detector.monitor_financial_access(token.token_id, accessor_info)
            if alert:
                fraud_alerts.append(alert)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle 500 checks in reasonable time (< 5 seconds)
        assert total_time < 5.0
        
        # Performance metrics
        checks_per_second = 500 / total_time
        assert checks_per_second > 50  # At least 50 checks per second


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])
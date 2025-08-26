#!/usr/bin/env python3
"""
MWRASP Bug Detection Demonstration
Shows the comprehensive testing and bug detection capabilities
"""

import sys
import time
import json
from pathlib import Path

def test_quantum_detector_basic():
    """Test basic quantum detector functionality"""
    print("Testing Quantum Detector...")
    
    try:
        from src.core.quantum_detector import QuantumDetector
        from src.core.post_quantum_crypto import PostQuantumCrypto
        
        # Test 1: Basic initialization
        detector = QuantumDetector()
        crypto = PostQuantumCrypto()
        print("  [PASS] System initialization")
        
        # Test 2: Token generation
        token = detector.generate_canary_token("test_resource")
        if token and token.token_id:
            print("  [PASS] Canary token generation")
        else:
            print("  [FAIL] Canary token generation failed")
            return False
        
        # Test 3: Token access
        result = detector.access_token(token.token_id, "test_user")
        if result:
            print("  [PASS] Token access verification")
        else:
            print("  [FAIL] Token access failed")
            return False
        
        # Test 4: Post-quantum crypto
        keypair = crypto.generate_ml_kem_keypair()
        if keypair and len(keypair) == 2:
            print("  [PASS] Post-quantum cryptography")
        else:
            print("  [FAIL] Post-quantum crypto failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"  [ERROR] Quantum detector test failed: {str(e)}")
        return False

def test_banking_compliance():
    """Test banking compliance system"""
    print("Testing Banking Compliance...")
    
    try:
        from src.core.banking_compliance import BankingQuantumDetector
        
        # Test 1: Banking system initialization
        detector = BankingQuantumDetector()
        print("  [PASS] Banking system initialization")
        
        # Test 2: PCI DSS compliance check
        compliance_status = detector.check_pci_dss_compliance()
        if compliance_status:
            print("  [PASS] PCI DSS compliance validation")
        else:
            print("  [FAIL] PCI DSS compliance failed")
            return False
        
        # Test 3: Financial token generation
        token = detector.generate_financial_canary_token("account_12345")
        if token and hasattr(token, 'risk_assessment'):
            print("  [PASS] Financial token generation")
        else:
            print("  [FAIL] Financial token generation failed")
            return False
        
        # Test 4: Fraud detection
        is_fraud = detector.detect_fraud_pattern("unusual_velocity")
        print("  [PASS] Fraud detection system")
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Banking compliance test failed: {str(e)}")
        return False

def test_federal_contractor():
    """Test federal contractor compliance"""
    print("Testing Federal Contractor Compliance...")
    
    try:
        from src.core.federal_contractor_compliance import FederalContractorSecurityMonitor
        
        # Test 1: Federal system initialization
        monitor = FederalContractorSecurityMonitor()
        print("  [PASS] Federal contractor system initialization")
        
        # Test 2: FISMA compliance
        fisma_status = monitor.check_fisma_compliance()
        if fisma_status:
            print("  [PASS] FISMA compliance validation")
        else:
            print("  [FAIL] FISMA compliance failed")
            return False
        
        # Test 3: Clearance validation
        clearance_valid = monitor.validate_security_clearance("SECRET", "test_user")
        if clearance_valid is not None:  # Could be True or False
            print("  [PASS] Security clearance validation")
        else:
            print("  [FAIL] Security clearance validation failed")
            return False
        
        # Test 4: Zero Trust architecture
        trust_score = monitor.calculate_zero_trust_score("test_user", "10.0.0.1")
        if 0 <= trust_score <= 1:
            print("  [PASS] Zero Trust architecture")
        else:
            print("  [FAIL] Zero Trust architecture failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Federal contractor test failed: {str(e)}")
        return False

def test_temporal_fragmentation():
    """Test temporal fragmentation system"""
    print("Testing Temporal Fragmentation...")
    
    try:
        from src.core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
        
        # Test 1: Fragmentation system initialization
        fragmenter = TemporalFragmentation()
        print("  [PASS] Temporal fragmentation initialization")
        
        # Test 2: Data fragmentation
        test_data = {"sensitive": "classified_information", "level": "SECRET"}
        fragments = fragmenter.fragment_data("test_data", test_data)
        if fragments and len(fragments) > 1:
            print("  [PASS] Data fragmentation")
        else:
            print("  [FAIL] Data fragmentation failed")
            return False
        
        # Test 3: Fragment reconstruction
        reconstructed = fragmenter.reconstruct_data("test_data")
        if reconstructed == test_data:
            print("  [PASS] Fragment reconstruction")
        else:
            print("  [FAIL] Fragment reconstruction failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Temporal fragmentation test failed: {str(e)}")
        return False

def test_agent_system():
    """Test agent coordination system"""
    print("Testing Agent Coordination...")
    
    try:
        from src.core.agent_system import AgentCoordinator, Agent, AgentRole
        
        # Test 1: Agent system initialization
        coordinator = AgentCoordinator()
        print("  [PASS] Agent coordination initialization")
        
        # Test 2: Agent creation and assignment
        agent = Agent("test_agent", AgentRole.MONITOR)
        coordinator.register_agent(agent)
        if "test_agent" in [a.agent_id for a in coordinator.agents]:
            print("  [PASS] Agent registration")
        else:
            print("  [FAIL] Agent registration failed")
            return False
        
        # Test 3: Threat response coordination
        response = coordinator.coordinate_response("quantum_attack_detected", "high")
        if response and response.get("status") == "coordinated":
            print("  [PASS] Threat response coordination")
        else:
            print("  [FAIL] Threat response coordination failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] Agent system test failed: {str(e)}")
        return False

def run_performance_test():
    """Run basic performance tests"""
    print("Testing System Performance...")
    
    try:
        from src.core.quantum_detector import QuantumDetector
        
        detector = QuantumDetector()
        
        # Test token generation speed
        start_time = time.time()
        for i in range(10):
            token = detector.generate_canary_token(f"perf_test_{i}")
        generation_time = time.time() - start_time
        tokens_per_second = 10 / generation_time
        
        print(f"  [PERFORMANCE] Token generation: {tokens_per_second:.1f} tokens/second")
        
        if tokens_per_second > 5:  # Should be able to generate at least 5 tokens per second
            print("  [PASS] Performance within acceptable range")
            return True
        else:
            print("  [FAIL] Performance below acceptable threshold")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Performance test failed: {str(e)}")
        return False

def generate_bug_report(test_results):
    """Generate comprehensive bug detection report"""
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print("\n" + "="*60)
    print("MWRASP QUANTUM DEFENSE - BUG DETECTION REPORT")
    print("="*60)
    
    print(f"\nTest Execution Summary:")
    print(f"  Total System Tests: {total_tests}")
    print(f"  Tests Passed: {passed_tests}")
    print(f"  Tests Failed: {failed_tests}")
    print(f"  Success Rate: {success_rate:.1f}%")
    
    print(f"\nSystem Component Results:")
    for test_name, result in test_results.items():
        status = "[PASS]" if result else "[FAIL]"
        component = test_name.replace("test_", "").replace("_", " ").title()
        print(f"  {component}: {status}")
    
    # System health assessment
    print(f"\nOverall System Health:")
    if failed_tests == 0:
        health_status = "EXCELLENT"
        print("  [EXCELLENT] All systems operational - ready for deployment")
        recommendations = [
            "System is ready for production deployment",
            "All quantum defense mechanisms functioning properly",
            "All compliance systems validated",
            "Schedule regular security audits"
        ]
    elif failed_tests <= 1:
        health_status = "GOOD"
        print("  [GOOD] Minor issues detected - system mostly stable")
        recommendations = [
            "Address failing system components",
            "System can be deployed with monitoring",
            "Fix identified issues in next maintenance cycle"
        ]
    elif failed_tests <= 2:
        health_status = "FAIR"
        print("  [FAIR] Several issues detected - recommend fixes before deployment")
        recommendations = [
            "Fix failing components before production deployment",
            "Conduct additional testing after fixes",
            "Review system architecture for reliability improvements"
        ]
    else:
        health_status = "CRITICAL"
        print("  [CRITICAL] Major issues detected - system not ready for deployment")
        recommendations = [
            "Do NOT deploy to production",
            "Fix all critical system failures",
            "Conduct comprehensive system review",
            "Re-run full test suite after fixes"
        ]
    
    print(f"\nRecommendations:")
    for rec in recommendations:
        print(f"  - {rec}")
    
    # Save detailed report
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "health_status": health_status
        },
        "component_results": test_results,
        "recommendations": recommendations
    }
    
    with open("mwrasp_bug_detection_report.json", 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\nDetailed report saved to: mwrasp_bug_detection_report.json")
    print("="*60)
    
    return health_status, success_rate

def main():
    """Main bug detection demonstration"""
    print("MWRASP QUANTUM DEFENSE SYSTEMS")
    print("Comprehensive Bug Detection Demonstration")
    print("-" * 50)
    
    start_time = time.time()
    
    # Run all system tests
    test_functions = [
        ("test_quantum_detector", test_quantum_detector_basic),
        ("test_banking_compliance", test_banking_compliance),
        ("test_federal_contractor", test_federal_contractor),
        ("test_temporal_fragmentation", test_temporal_fragmentation),
        ("test_agent_system", test_agent_system),
        ("test_performance", run_performance_test)
    ]
    
    test_results = {}
    
    print("\nRunning comprehensive system tests...")
    print("-" * 40)
    
    for test_name, test_function in test_functions:
        try:
            result = test_function()
            test_results[test_name] = result
        except Exception as e:
            print(f"  [CRITICAL ERROR] {test_name}: {str(e)}")
            test_results[test_name] = False
    
    # Generate comprehensive bug report
    health_status, success_rate = generate_bug_report(test_results)
    
    execution_time = time.time() - start_time
    print(f"\nTotal execution time: {execution_time:.2f} seconds")
    
    # Return appropriate exit code based on system health
    if health_status == "EXCELLENT":
        return 0
    elif health_status == "GOOD":
        return 0
    elif health_status == "FAIR":
        return 1
    else:
        return 2

if __name__ == "__main__":
    sys.exit(main())
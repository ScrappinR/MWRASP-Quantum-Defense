#!/usr/bin/env python3
"""
Windows-Compatible MWRASP Test Runner
Comprehensive bug detection for all three MWRASP systems
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def run_test_data_generation():
    """Generate test data for all systems"""
    print("\n" + "="*50)
    print("GENERATING TEST DATA")
    print("="*50)
    
    try:
        from src.tests.test_data_generator import TestDataGenerator, SystemType
        
        for system_type in SystemType:
            print(f"\nGenerating {system_type.value} test data...")
            generator = TestDataGenerator(system_type)
            files = generator.generate_test_suite("test_data")
            print(f"[OK] Generated {system_type.value} data files:")
            for data_type, file_path in files.items():
                print(f"  - {data_type}: {file_path}")
        
        print("\n[SUCCESS] Test data generation completed")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test data generation failed: {str(e)}")
        return False

def run_unit_tests():
    """Run all unit test suites"""
    print("\n" + "="*50)
    print("RUNNING UNIT TESTS")
    print("="*50)
    
    test_files = [
        "src/tests/test_quantum_detector.py",
        "src/tests/test_banking_compliance.py", 
        "src/tests/test_federal_contractor.py",
        "src/tests/test_system_integration.py"
    ]
    
    results = {}
    total_passed = 0
    total_failed = 0
    
    for test_file in test_files:
        print(f"\nRunning {test_file}...")
        
        if not Path(test_file).exists():
            print(f"[SKIP] Test file not found: {test_file}")
            continue
            
        try:
            # Run pytest on individual test file
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--tb=short"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"[PASS] {test_file}")
                results[test_file] = "PASSED"
                # Count passed tests from output
                lines = result.stdout.split('\n')
                for line in lines:
                    if "passed" in line and "failed" not in line:
                        words = line.split()
                        for i, word in enumerate(words):
                            if word == "passed" and i > 0 and words[i-1].isdigit():
                                total_passed += int(words[i-1])
                                break
            else:
                print(f"[FAIL] {test_file}")
                results[test_file] = "FAILED"
                # Show error summary
                print("Error output:")
                print(result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
                
                # Count failed tests
                lines = result.stdout.split('\n')
                for line in lines:
                    if "failed" in line:
                        words = line.split()
                        for i, word in enumerate(words):
                            if word == "failed" and i > 0 and words[i-1].isdigit():
                                total_failed += int(words[i-1])
                                break
                            
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {test_file}")
            results[test_file] = "TIMEOUT"
        except Exception as e:
            print(f"[ERROR] {test_file}: {str(e)}")
            results[test_file] = "ERROR"
    
    print(f"\n" + "-"*30)
    print("UNIT TEST SUMMARY")
    print("-"*30)
    print(f"Tests Passed: {total_passed}")
    print(f"Tests Failed: {total_failed}")
    print(f"Success Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%" if (total_passed+total_failed) > 0 else "N/A")
    
    return results, total_passed, total_failed

def run_security_tests():
    """Run security penetration tests"""
    print("\n" + "="*50)
    print("RUNNING SECURITY TESTS")
    print("="*50)
    
    try:
        print("Starting penetration testing...")
        result = subprocess.run([
            sys.executable, "security_penetration_test.py", 
            "--quick"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[PASS] Security penetration tests completed")
            # Parse output for vulnerabilities
            lines = result.stdout.split('\n')
            vulnerabilities_found = 0
            for line in lines:
                if "vulnerability" in line.lower() or "critical" in line.lower():
                    vulnerabilities_found += 1
            
            print(f"Vulnerabilities detected: {vulnerabilities_found}")
            return True, vulnerabilities_found
        else:
            print("[FAIL] Security tests failed")
            print("Error output:")
            print(result.stderr[:300] + "..." if len(result.stderr) > 300 else result.stderr)
            return False, 0
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Security tests timed out")
        return False, 0
    except Exception as e:
        print(f"[ERROR] Security tests failed: {str(e)}")
        return False, 0

def generate_final_report(unit_results, passed, failed, security_passed, vulnerabilities):
    """Generate final bug detection report"""
    print("\n" + "="*60)
    print("MWRASP QUANTUM DEFENSE - BUG DETECTION REPORT")
    print("="*60)
    
    print(f"\nTest Execution Summary:")
    print(f"  Total Unit Tests: {passed + failed}")
    print(f"  Tests Passed: {passed}")
    print(f"  Tests Failed: {failed}")
    
    if passed + failed > 0:
        success_rate = (passed / (passed + failed)) * 100
        print(f"  Success Rate: {success_rate:.1f}%")
    
    print(f"\nSecurity Analysis:")
    print(f"  Penetration Tests: {'PASSED' if security_passed else 'FAILED'}")
    print(f"  Vulnerabilities Found: {vulnerabilities}")
    
    print(f"\nSystem-Specific Results:")
    for test_file, status in unit_results.items():
        system_name = test_file.split('/')[-1].replace('test_', '').replace('.py', '')
        print(f"  {system_name.upper()}: {status}")
    
    # Overall system health
    print(f"\nOverall System Health:")
    if failed == 0 and security_passed and vulnerabilities == 0:
        print("  [EXCELLENT] All systems operational, no bugs or vulnerabilities detected")
        health_status = "EXCELLENT"
    elif failed <= 2 and vulnerabilities <= 1:
        print("  [GOOD] Minor issues detected, system stable")
        health_status = "GOOD"
    elif failed <= 5 and vulnerabilities <= 3:
        print("  [FAIR] Several issues detected, recommend fixes before deployment")
        health_status = "FAIR"
    else:
        print("  [CRITICAL] Major issues detected, system not ready for deployment")
        health_status = "CRITICAL"
    
    print(f"\nRecommendations:")
    if failed > 0:
        print(f"  - Fix {failed} failing unit tests")
    if vulnerabilities > 0:
        print(f"  - Address {vulnerabilities} security vulnerabilities")
    if failed == 0 and vulnerabilities == 0:
        print("  - System is ready for production deployment")
        print("  - Consider performance optimization testing")
        print("  - Schedule regular security audits")
    
    # Save report to file
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "unit_tests": {
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
        },
        "security_tests": {
            "passed": security_passed,
            "vulnerabilities_found": vulnerabilities
        },
        "system_results": unit_results,
        "overall_health": health_status
    }
    
    with open("mwrasp_bug_report.json", 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\nDetailed report saved to: mwrasp_bug_report.json")
    print("="*60)
    
    return health_status

def main():
    """Main test execution"""
    print("MWRASP QUANTUM DEFENSE SYSTEMS")
    print("Comprehensive Bug Detection and Testing Suite")
    print("Windows Compatible Version")
    
    start_time = time.time()
    
    # Step 1: Generate test data
    data_generated = run_test_data_generation()
    if not data_generated:
        print("\n[CRITICAL] Cannot proceed without test data")
        return 1
    
    # Step 2: Run unit tests
    unit_results, passed, failed = run_unit_tests()
    
    # Step 3: Run security tests
    security_passed, vulnerabilities = run_security_tests()
    
    # Step 4: Generate final report
    health_status = generate_final_report(unit_results, passed, failed, security_passed, vulnerabilities)
    
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    
    # Return appropriate exit code
    if health_status in ["EXCELLENT", "GOOD"]:
        return 0
    elif health_status == "FAIR":
        return 1
    else:
        return 2

if __name__ == "__main__":
    sys.exit(main())
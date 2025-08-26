#!/usr/bin/env python3
"""
MWRASP Comprehensive Test Runner
Automated bug detection and system validation for all three MWRASP variants
"""

import os
import sys
import subprocess
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple


class MWRASPTestRunner:
    """Comprehensive test runner for MWRASP systems"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = {
            "start_time": time.time(),
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "errors": [],
            "warnings": [],
            "system_results": {}
        }
        
        # Test configuration
        self.test_suites = {
            "quantum_detector": {
                "file": "src/tests/test_quantum_detector.py",
                "description": "Core quantum detection algorithms",
                "critical": True
            },
            "banking_compliance": {
                "file": "src/tests/test_banking_compliance.py", 
                "description": "Banking PCI DSS and SOX compliance",
                "critical": True
            },
            "federal_contractor": {
                "file": "src/tests/test_federal_contractor.py",
                "description": "Federal contractor FISMA compliance",
                "critical": True
            },
            "system_integration": {
                "file": "src/tests/test_system_integration.py",
                "description": "Cross-system integration tests",
                "critical": True
            },
            "fragmentation": {
                "file": "src/tests/test_fragmentation.py",
                "description": "Temporal fragmentation system",
                "critical": False
            }
        }
    
    def check_prerequisites(self) -> bool:
        """Check if test environment is properly set up"""
        print("Checking test prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 9):
            self.test_results["errors"].append("Python 3.9+ required")
            return False
        
        # Check required packages
        required_packages = ["pytest", "pytest-asyncio", "numpy", "cryptography"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.test_results["errors"].append(f"Missing packages: {missing_packages}")
            print(f"[ERROR] Missing required packages: {missing_packages}")
            print("Run: pip install -r requirements.txt")
            return False
        
        # Check test files exist
        missing_files = []
        for suite_name, suite_info in self.test_suites.items():
            test_file = Path(suite_info["file"])
            if not test_file.exists():
                missing_files.append(str(test_file))
        
        if missing_files:
            self.test_results["warnings"].append(f"Missing test files: {missing_files}")
            print(f"[WARNING] Missing test files: {missing_files}")
        
        print("[OK] Prerequisites check completed")
        return True
    
    def run_test_suite(self, suite_name: str, suite_info: Dict) -> Dict[str, Any]:
        """Run a specific test suite and return results"""
        print(f"\n🧪 Running {suite_name} tests...")
        print(f"   Description: {suite_info['description']}")
        print(f"   Critical: {'Yes' if suite_info['critical'] else 'No'}")
        
        test_file = suite_info["file"]
        
        # Check if test file exists
        if not Path(test_file).exists():
            result = {
                "suite": suite_name,
                "status": "SKIPPED",
                "reason": "Test file not found",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0.0,
                "output": ""
            }
            print(f"⏭️  Skipped: Test file not found")
            return result
        
        # Run pytest on the specific test file
        start_time = time.time()
        
        pytest_args = [
            "python", "-m", "pytest",
            test_file,
            "-v",
            "--tb=short",
            "--durations=10",
            "--json-report",
            f"--json-report-file=test_results_{suite_name}.json"
        ]
        
        if self.verbose:
            pytest_args.append("-s")
        
        try:
            result_process = subprocess.run(
                pytest_args,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per test suite
            )
            
            duration = time.time() - start_time
            
            # Parse pytest output
            output_lines = result_process.stdout.split('\n')
            error_lines = result_process.stderr.split('\n')
            
            # Extract test counts from output
            tests_run = 0
            passed = 0
            failed = 0
            
            for line in output_lines:
                if "passed" in line and "failed" in line:
                    # Parse pytest summary line
                    words = line.split()
                    for i, word in enumerate(words):
                        if word == "passed":
                            passed = int(words[i-1])
                        elif word == "failed":
                            failed = int(words[i-1])
                elif line.strip().endswith("passed"):
                    words = line.split()
                    if len(words) >= 1 and words[0].isdigit():
                        passed = int(words[0])
            
            tests_run = passed + failed
            
            # Determine status
            if result_process.returncode == 0:
                status = "PASSED"
                print(f"✅ {suite_name}: {passed} tests passed")
            else:
                status = "FAILED"
                print(f"❌ {suite_name}: {failed} tests failed, {passed} tests passed")
                
                # Add error details
                if error_lines:
                    error_summary = '\n'.join([line for line in error_lines if line.strip()])
                    self.test_results["errors"].append(f"{suite_name}: {error_summary}")
            
            result = {
                "suite": suite_name,
                "status": status,
                "tests_run": tests_run,
                "passed": passed,
                "failed": failed,
                "duration": duration,
                "output": result_process.stdout,
                "errors": result_process.stderr
            }
            
        except subprocess.TimeoutExpired:
            result = {
                "suite": suite_name,
                "status": "TIMEOUT",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": 300.0,
                "output": "Test suite timed out after 5 minutes"
            }
            print(f"⏰ {suite_name}: Timed out after 5 minutes")
            
        except Exception as e:
            result = {
                "suite": suite_name,
                "status": "ERROR",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": time.time() - start_time,
                "output": f"Error running tests: {str(e)}"
            }
            print(f"💥 {suite_name}: Error - {str(e)}")
        
        return result
    
    def generate_test_data(self):
        """Generate test data for all MWRASP systems"""
        print("\nGenerating Test Data...")
        print("-" * 30)
        
        try:
            from src.tests.test_data_generator import TestDataGenerator, SystemType
            
            # Generate test data for all three systems
            data_files = {}
            for system_type in SystemType:
                print(f"Generating {system_type.value} test data...")
                generator = TestDataGenerator(system_type)
                files = generator.generate_test_suite("test_data")
                data_files[system_type.value] = files
                print(f"  [OK] Generated {system_type.value} test data")
            
            self.test_results["test_data_files"] = data_files
            print("[OK] Test data generation completed")
            
        except Exception as e:
            self.test_results["warnings"].append(f"Test data generation failed: {str(e)}")
            print(f"[WARNING] Test data generation failed: {str(e)}")

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and collect results"""
        print("MWRASP Comprehensive Test Suite")
        print("=" * 50)
        
        if not self.check_prerequisites():
            print("❌ Prerequisites check failed. Cannot run tests.")
            return self.test_results
        
        # Generate test data first
        self.generate_test_data()
        
        # Run each test suite
        for suite_name, suite_info in self.test_suites.items():
            result = self.run_test_suite(suite_name, suite_info)
            self.test_results["system_results"][suite_name] = result
            
            # Update totals
            self.test_results["total_tests"] += result["tests_run"]
            self.test_results["passed_tests"] += result["passed"]
            self.test_results["failed_tests"] += result["failed"]
            
            if result["status"] == "SKIPPED":
                self.test_results["skipped_tests"] += 1
        
        self.test_results["end_time"] = time.time()
        self.test_results["total_duration"] = (
            self.test_results["end_time"] - self.test_results["start_time"]
        )
        
        return self.test_results
    
    def run_performance_tests(self):
        """Run performance-specific tests"""
        print("\n⚡ Performance Testing")
        print("-" * 30)
        
        performance_tests = [
            ("Token Generation Speed", self._test_token_generation_speed),
            ("Threat Detection Speed", self._test_threat_detection_speed),
            ("Memory Usage", self._test_memory_usage),
            ("Concurrent Operations", self._test_concurrent_operations)
        ]
        
        performance_results = {}
        
        for test_name, test_function in performance_tests:
            print(f"Running {test_name}...")
            try:
                result = test_function()
                performance_results[test_name] = result
                print(f"  ✅ {test_name}: {result}")
            except Exception as e:
                performance_results[test_name] = f"ERROR: {str(e)}"
                print(f"  ❌ {test_name}: {str(e)}")
        
        return performance_results
    
    def _test_token_generation_speed(self) -> str:
        """Test token generation performance"""
        from src.core.quantum_detector import QuantumDetector
        
        detector = QuantumDetector()
        start_time = time.time()
        
        for i in range(100):
            detector.generate_canary_token(f"speed_test_{i}")
        
        duration = time.time() - start_time
        tokens_per_second = 100 / duration
        
        return f"{tokens_per_second:.1f} tokens/second"
    
    def _test_threat_detection_speed(self) -> str:
        """Test threat detection performance"""
        from src.core.quantum_detector import QuantumDetector
        
        detector = QuantumDetector()
        token = detector.generate_canary_token("threat_speed_test")
        
        start_time = time.time()
        
        for i in range(1000):
            detector.access_token(token.token_id, f"speed_user_{i}")
        
        duration = time.time() - start_time
        checks_per_second = 1000 / duration
        
        return f"{checks_per_second:.1f} checks/second"
    
    def _test_memory_usage(self) -> str:
        """Test memory usage patterns"""
        import psutil
        import gc
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create systems and generate load
        from src.core.quantum_detector import QuantumDetector
        
        detector = QuantumDetector()
        
        # Generate many tokens
        for i in range(1000):
            detector.generate_canary_token(f"memory_test_{i}")
        
        # Force garbage collection
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        return f"{memory_increase:.1f} MB increase for 1000 tokens"
    
    def _test_concurrent_operations(self) -> str:
        """Test concurrent operation performance"""
        import threading
        import time
        
        from src.core.quantum_detector import QuantumDetector
        
        detector = QuantumDetector()
        results = []
        
        def worker():
            start = time.time()
            for i in range(10):
                token = detector.generate_canary_token(f"concurrent_{threading.current_thread().ident}_{i}")
                detector.access_token(token.token_id, f"user_{i}")
            results.append(time.time() - start)
        
        # Run 10 concurrent workers
        threads = []
        start_time = time.time()
        
        for i in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_duration = time.time() - start_time
        
        return f"10 threads completed in {total_duration:.2f} seconds"
    
    def generate_report(self) -> str:
        """Generate comprehensive test report"""
        results = self.test_results
        
        report = []
        report.append("MWRASP QUANTUM DEFENSE SYSTEM - TEST REPORT")
        report.append("=" * 55)
        report.append("")
        
        # Summary
        total_time = results.get("total_duration", 0)
        report.append(f"⏱️  Total Test Duration: {total_time:.2f} seconds")
        report.append(f"🧪 Total Tests Run: {results['total_tests']}")
        report.append(f"✅ Tests Passed: {results['passed_tests']}")
        report.append(f"❌ Tests Failed: {results['failed_tests']}")
        report.append(f"⏭️  Tests Skipped: {results['skipped_tests']}")
        
        if results['total_tests'] > 0:
            success_rate = (results['passed_tests'] / results['total_tests']) * 100
            report.append(f"📊 Success Rate: {success_rate:.1f}%")
        
        report.append("")
        
        # System-specific results
        report.append("SYSTEM-SPECIFIC RESULTS")
        report.append("-" * 30)
        
        for suite_name, suite_result in results["system_results"].items():
            status_icon = {
                "PASSED": "✅",
                "FAILED": "❌", 
                "SKIPPED": "⏭️",
                "TIMEOUT": "⏰",
                "ERROR": "💥"
            }.get(suite_result["status"], "❓")
            
            report.append(f"{status_icon} {suite_name.upper()}:")
            report.append(f"   Status: {suite_result['status']}")
            report.append(f"   Tests: {suite_result['passed']}/{suite_result['tests_run']} passed")
            report.append(f"   Duration: {suite_result['duration']:.2f}s")
            report.append("")
        
        # Critical issues
        critical_issues = []
        for suite_name, suite_result in results["system_results"].items():
            suite_info = self.test_suites.get(suite_name, {})
            if suite_info.get("critical") and suite_result["status"] in ["FAILED", "ERROR", "TIMEOUT"]:
                critical_issues.append(f"{suite_name}: {suite_result['status']}")
        
        if critical_issues:
            report.append("🚨 CRITICAL ISSUES DETECTED")
            report.append("-" * 30)
            for issue in critical_issues:
                report.append(f"❌ {issue}")
            report.append("")
        
        # Errors and warnings
        if results["errors"]:
            report.append("🐛 ERRORS DETECTED")
            report.append("-" * 20)
            for error in results["errors"]:
                report.append(f"❌ {error}")
            report.append("")
        
        if results["warnings"]:
            report.append("⚠️  WARNINGS")
            report.append("-" * 15)
            for warning in results["warnings"]:
                report.append(f"⚠️  {warning}")
            report.append("")
        
        # Recommendations
        report.append("📋 RECOMMENDATIONS")
        report.append("-" * 20)
        
        if results['failed_tests'] == 0:
            report.append("🎉 All tests passed! System is ready for deployment.")
        else:
            report.append("🔧 Fix failing tests before deployment:")
            
            failed_suites = [
                suite_name for suite_name, suite_result in results["system_results"].items()
                if suite_result["status"] in ["FAILED", "ERROR"]
            ]
            
            for suite in failed_suites:
                report.append(f"   - Review {suite} test failures")
        
        # Performance recommendations
        if total_time > 60:
            report.append(f"⚡ Consider performance optimization (tests took {total_time:.1f}s)")
        
        report.append("")
        report.append("END OF REPORT")
        
        return "\n".join(report)
    
    def save_detailed_report(self, filename: str = "mwrasp_test_report.json"):
        """Save detailed test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Detailed report saved to: {filename}")


def main():
    """Main test runner entry point"""
    parser = argparse.ArgumentParser(description="MWRASP Comprehensive Test Runner")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-p", "--performance", action="store_true", help="Run performance tests")
    parser.add_argument("-s", "--suite", help="Run specific test suite only")
    parser.add_argument("-r", "--report", help="Save report to file")
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = MWRASPTestRunner(verbose=args.verbose)
    
    if args.suite:
        # Run specific test suite
        if args.suite in runner.test_suites:
            suite_info = runner.test_suites[args.suite]
            result = runner.run_test_suite(args.suite, suite_info)
            print(f"\n{args.suite} Results: {result}")
        else:
            print(f"Unknown test suite: {args.suite}")
            print(f"Available suites: {list(runner.test_suites.keys())}")
            return 1
    else:
        # Run all tests
        results = runner.run_all_tests()
        
        # Run performance tests if requested
        if args.performance:
            perf_results = runner.run_performance_tests()
            results["performance_results"] = perf_results
        
        # Generate and display report
        report = runner.generate_report()
        print(f"\n{report}")
        
        # Save detailed report
        runner.save_detailed_report()
        
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.report}")
        
        # Return appropriate exit code
        if results["failed_tests"] > 0:
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
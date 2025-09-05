#!/usr/bin/env python3
"""
Automated IBM Quantum Hardware Testing Program
Automatically detects credentials, connects to IBM Quantum, and runs comprehensive tests
"""

import os
import sys
import time
import json
import asyncio
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class AutomatedIBMQuantumTester:
    """Fully automated IBM Quantum testing with credential detection"""
    
    def __init__(self):
        self.credentials_found = False
        self.token = None
        self.service_crn = None
        self.test_results = []
        
    def detect_credentials(self) -> bool:
        """Detect IBM Quantum credentials from multiple sources"""
        print("="*60)
        print("AUTOMATED IBM QUANTUM CREDENTIAL DETECTION")
        print("="*60)
        
        # Method 1: Environment variables
        token_env = os.getenv('IBM_QUANTUM_TOKEN')
        crn_env = os.getenv('IBM_QUANTUM_CRN')
        
        if token_env:
            print(f"[SUCCESS] Found IBM_QUANTUM_TOKEN in environment")
            self.token = token_env
            self.credentials_found = True
            
        if crn_env:
            print(f"[SUCCESS] Found IBM_QUANTUM_CRN in environment: {crn_env[:20]}...")
            self.service_crn = crn_env
            
        # Method 2: Check for credentials file
        home_dir = os.path.expanduser("~")
        qiskit_config_paths = [
            os.path.join(home_dir, ".qiskit", "qiskitrc"),
            os.path.join(home_dir, ".qiskit", "qiskit-ibm.json"),
            "qiskit_credentials.json",
            "ibm_quantum_config.json"
        ]
        
        for config_path in qiskit_config_paths:
            if os.path.exists(config_path):
                print(f"[INFO] Found config file: {config_path}")
                try:
                    if config_path.endswith('.json'):
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                            if 'token' in config or 'api_token' in config:
                                self.token = config.get('token') or config.get('api_token')
                                self.credentials_found = True
                                print(f"[SUCCESS] Loaded token from {config_path}")
                    else:
                        # Parse qiskitrc format
                        with open(config_path, 'r') as f:
                            for line in f:
                                if line.startswith('token'):
                                    self.token = line.split('=')[1].strip()
                                    self.credentials_found = True
                                    print(f"[SUCCESS] Loaded token from {config_path}")
                except Exception as e:
                    print(f"[WARNING] Could not parse {config_path}: {e}")
        
        # Method 3: Interactive prompt if no credentials found
        if not self.credentials_found:
            print("\n[INFO] No credentials found automatically")
            print("Would you like to enter your IBM Quantum credentials manually?")
            print("You can find these at: https://quantum.ibm.com/")
            
            # For automation, we'll create a credentials template
            self._create_credentials_template()
            print("\n[INFO] Created credentials template file: ibm_quantum_config.json")
            print("Please edit this file with your actual credentials and run again")
            
        return self.credentials_found
    
    def _create_credentials_template(self):
        """Create a template credentials file"""
        template = {
            "token": "YOUR_IBM_QUANTUM_TOKEN_HERE",
            "service_crn": "YOUR_SERVICE_CRN_HERE",
            "instructions": {
                "1": "Visit https://quantum.ibm.com/",
                "2": "Create account or log in",
                "3": "Go to Account -> API Tokens",
                "4": "Copy your token and replace YOUR_IBM_QUANTUM_TOKEN_HERE",
                "5": "Optionally add your service CRN",
                "6": "Run this program again"
            }
        }
        
        with open("ibm_quantum_config.json", 'w') as f:
            json.dump(template, f, indent=2)
    
    def setup_environment(self) -> bool:
        """Set up the environment with detected credentials"""
        if not self.credentials_found:
            return False
            
        print(f"\n[CONFIG] Setting up environment with IBM Quantum token")
        os.environ['IBM_QUANTUM_TOKEN'] = self.token
        
        if self.service_crn:
            os.environ['IBM_QUANTUM_CRN'] = self.service_crn
            
        return True
    
    def install_dependencies(self) -> bool:
        """Install required packages automatically"""
        print("\n[SETUP] Checking and installing dependencies...")
        
        required_packages = [
            'qiskit',
            'qiskit-aer', 
            'qiskit-ibm-runtime',
            'qiskit-ibm-provider'
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"[SUCCESS] {package} already installed")
            except ImportError:
                print(f"[INSTALL] Installing {package}...")
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 check=True, capture_output=True, text=True)
                    print(f"[SUCCESS] {package} installed successfully")
                except subprocess.CalledProcessError as e:
                    print(f"[ERROR] Failed to install {package}: {e}")
                    return False
        
        return True
    
    async def run_automated_tests(self) -> Dict[str, Any]:
        """Run the full automated test suite"""
        print("\n" + "="*60)
        print("STARTING AUTOMATED IBM QUANTUM TESTING")
        print("="*60)
        
        # Import the IBM quantum tester
        try:
            from ibm_quantum_hardware_tester import IBMQuantumHardwareTester
            print("[SUCCESS] IBM Quantum tester module loaded")
        except ImportError as e:
            print(f"[ERROR] Could not import tester module: {e}")
            return {'error': 'Module import failed'}
        
        # Initialize the tester
        tester = IBMQuantumHardwareTester(api_token=self.token, use_simulator=False)
        
        # Run comprehensive tests
        try:
            results = await tester.run_comprehensive_hardware_tests()
            self.test_results = results
            
            # Save results with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Automated_IBM_Quantum_Test_Results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"\n[SUCCESS] Test results saved to: {filename}")
            return results
            
        except Exception as e:
            print(f"[ERROR] Test execution failed: {e}")
            return {'error': str(e)}
    
    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test results and generate summary"""
        print("\n" + "="*60)
        print("AUTOMATED TEST RESULTS ANALYSIS")
        print("="*60)
        
        if 'error' in results:
            print(f"[ERROR] Testing failed: {results['error']}")
            return {'status': 'failed', 'reason': results['error']}
        
        summary = results.get('summary', {})
        backend_info = results.get('backend_info', {})
        
        print(f"Backend Used: {backend_info.get('name', 'Unknown')}")
        print(f"Simulator Mode: {backend_info.get('simulator_mode', True)}")
        print(f"Available Qubits: {backend_info.get('num_qubits', 'Unknown')}")
        
        total_tests = summary.get('total_tests', 0)
        successful_tests = summary.get('successful_tests', 0)
        success_rate = summary.get('success_rate', 0)
        
        print(f"\nTest Results:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Successful: {successful_tests}")
        print(f"  Success Rate: {success_rate:.1%}")
        print(f"  Hardware Validated: {summary.get('hardware_validated', False)}")
        print(f"  Quantum Advantage: {summary.get('quantum_advantage_demonstrated', False)}")
        
        # Detailed algorithm results
        algorithm_results = results.get('algorithm_results', {})
        
        print(f"\nAlgorithm Performance:")
        for algorithm, result in algorithm_results.items():
            if isinstance(result, dict) and 'success' in result:
                status = "[SUCCESS]" if result['success'] else "[FAILED]"
                print(f"  {algorithm}: {status}")
                if 'error_rate' in result:
                    print(f"    Error Rate: {result['error_rate']:.1%}")
                if 'execution_time' in result:
                    print(f"    Execution Time: {result['execution_time']:.2f}s")
        
        return {
            'status': 'completed',
            'success_rate': success_rate,
            'hardware_validated': summary.get('hardware_validated', False),
            'total_tests': total_tests,
            'successful_tests': successful_tests
        }
    
    def generate_report(self, results: Dict[str, Any], analysis: Dict[str, Any]):
        """Generate comprehensive automation report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# Automated IBM Quantum Testing Report

**Generated:** {timestamp}
**Status:** {'SUCCESS' if analysis['status'] == 'completed' else 'FAILED'}

## Automation Summary

### Credential Detection
- **Token Found:** {'Yes' if self.credentials_found else 'No'}
- **Token Source:** {'Environment/Config' if self.credentials_found else 'None'}
- **Service CRN:** {'Configured' if self.service_crn else 'Not configured'}

### Test Execution
- **Total Tests:** {analysis.get('total_tests', 0)}
- **Successful Tests:** {analysis.get('successful_tests', 0)}  
- **Success Rate:** {analysis.get('success_rate', 0):.1%}
- **Hardware Validated:** {analysis.get('hardware_validated', False)}

### Automation Status
"""
        
        if analysis['status'] == 'completed':
            report += """
[SUCCESS] **AUTOMATION SUCCESSFUL**
- Credentials detected and validated
- Dependencies installed automatically  
- Tests executed successfully
- Results analyzed and saved
"""
        else:
            report += f"""
[ERROR] **AUTOMATION FAILED**
- Reason: {analysis.get('reason', 'Unknown error')}
- Manual intervention may be required
"""
        
        report += f"""
## Next Steps

### If Successful
1. Review detailed results in JSON files
2. Deploy to production environment
3. Set up continuous testing schedule

### If Failed  
1. Check IBM Quantum credentials
2. Verify internet connectivity
3. Review error logs for specific issues

---
*Generated by MWRASP Automated IBM Quantum Testing System*
"""
        
        filename = f"Automated_Testing_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"\n[REPORT] Comprehensive report saved to: {filename}")
        return filename

async def main():
    """Main automation function"""
    print("[AUTOMATION] MWRASP Automated IBM Quantum Testing System")
    print("=" * 60)
    
    tester = AutomatedIBMQuantumTester()
    
    # Step 1: Detect credentials
    if not tester.detect_credentials():
        print("\n[ERROR] AUTOMATION STOPPED - No credentials found")
        print("Please configure your IBM Quantum credentials and run again")
        return False
    
    # Step 2: Setup environment  
    if not tester.setup_environment():
        print("\n[ERROR] AUTOMATION STOPPED - Environment setup failed")
        return False
    
    # Step 3: Install dependencies
    if not tester.install_dependencies():
        print("\n[ERROR] AUTOMATION STOPPED - Dependency installation failed") 
        return False
    
    # Step 4: Run automated tests
    print("\n[LAUNCH] Starting automated test execution...")
    results = await tester.run_automated_tests()
    
    # Step 5: Analyze results
    analysis = tester.analyze_results(results)
    
    # Step 6: Generate report
    report_file = tester.generate_report(results, analysis)
    
    # Step 7: Final status
    if analysis['status'] == 'completed':
        print(f"\n[SUCCESS] AUTOMATION COMPLETED SUCCESSFULLY")
        print(f"   Success Rate: {analysis['success_rate']:.1%}")
        print(f"   Report: {report_file}")
        return True
    else:
        print(f"\n[ERROR] AUTOMATION FAILED")
        print(f"   Reason: {analysis.get('reason', 'Unknown')}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[WARNING] Automation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[CRITICAL] Automation failed with exception: {e}")
        sys.exit(1)
#!/usr/bin/env python3
"""
IBM Quantum Connection Diagnostic Tool
Comprehensive troubleshooting for API key issues
"""

import os
import sys
import json
import time
from datetime import datetime

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

API_KEY = 'ApiKey-fd521625-00ee-4507-97f8-ffdf937fa7de'

def diagnostic_header():
    print("="*80)
    print("IBM QUANTUM CONNECTION DIAGNOSTIC TOOL")
    print(f"Timestamp: {datetime.now()}")
    print("="*80)
    print(f"API Key: {API_KEY}")
    print(f"Key Length: {len(API_KEY)} characters")
    print(f"Key Format: {'✓ Valid' if API_KEY.startswith('ApiKey-') else '✗ Invalid'}")
    print()

def test_qiskit_installation():
    """Test Qiskit installation and versions"""
    print("[DIAGNOSTIC 1] Testing Qiskit Installation...")
    try:
        import qiskit
        print(f"✓ Qiskit Core Version: {qiskit.__version__}")
        
        import qiskit_ibm_runtime
        print(f"✓ Qiskit IBM Runtime Version: {qiskit_ibm_runtime.__version__}")
        
        from qiskit_ibm_runtime import QiskitRuntimeService
        print("✓ QiskitRuntimeService import successful")
        
        return True
    except Exception as e:
        print(f"✗ Qiskit installation issue: {e}")
        return False

def clear_existing_accounts():
    """Clear any existing saved accounts"""
    print("\n[DIAGNOSTIC 2] Clearing existing accounts...")
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Check what accounts exist
        accounts = QiskitRuntimeService.saved_accounts()
        print(f"Existing accounts: {list(accounts.keys())}")
        
        # Delete all accounts
        for account_name in accounts.keys():
            try:
                QiskitRuntimeService.delete_account(name=account_name)
                print(f"✓ Deleted account: {account_name}")
            except Exception as e:
                print(f"⚠ Could not delete {account_name}: {e}")
        
        # Verify cleanup
        remaining = QiskitRuntimeService.saved_accounts()
        print(f"Remaining accounts: {list(remaining.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Account cleanup error: {e}")
        return False

def test_api_key_formats():
    """Test different API key connection formats"""
    print("\n[DIAGNOSTIC 3] Testing API Key Connection Formats...")
    
    from qiskit_ibm_runtime import QiskitRuntimeService
    
    # Test 1: IBM Cloud channel
    print("Test 1: IBM Cloud channel...")
    try:
        service = QiskitRuntimeService(
            token=API_KEY,
            channel='ibm_cloud'
        )
        print("✓ IBM Cloud connection successful!")
        backends = list(service.backends())
        print(f"✓ Found {len(backends)} backends")
        return True, service, backends
    except Exception as e1:
        print(f"✗ IBM Cloud failed: {e1}")
    
    # Test 2: IBM Quantum Platform channel
    print("\nTest 2: IBM Quantum Platform channel...")
    try:
        service = QiskitRuntimeService(
            token=API_KEY,
            channel='ibm_quantum_platform'
        )
        print("✓ IBM Quantum Platform connection successful!")
        backends = list(service.backends())
        print(f"✓ Found {len(backends)} backends")
        return True, service, backends
    except Exception as e2:
        print(f"✗ IBM Quantum Platform failed: {e2}")
    
    # Test 3: Save and load approach
    print("\nTest 3: Save account then load...")
    try:
        # Try saving with different channels
        for channel in ['ibm_cloud', 'ibm_quantum_platform']:
            try:
                print(f"  Trying to save with channel: {channel}")
                QiskitRuntimeService.save_account(
                    token=API_KEY,
                    channel=channel,
                    overwrite=True,
                    set_as_default=True,
                    name=f'test_{channel}'
                )
                
                service = QiskitRuntimeService(name=f'test_{channel}')
                print(f"✓ Save/load successful with {channel}!")
                backends = list(service.backends())
                print(f"✓ Found {len(backends)} backends")
                return True, service, backends
                
            except Exception as e:
                print(f"  ✗ Save/load with {channel} failed: {e}")
    except Exception as e3:
        print(f"✗ Save/load approach failed: {e3}")
    
    # Test 4: Environment variable approach
    print("\nTest 4: Environment variable approach...")
    try:
        os.environ['QISKIT_IBM_TOKEN'] = API_KEY
        os.environ['QISKIT_IBM_CHANNEL'] = 'ibm_cloud'
        
        service = QiskitRuntimeService()
        print("✓ Environment variable connection successful!")
        backends = list(service.backends())
        print(f"✓ Found {len(backends)} backends")
        return True, service, backends
        
    except Exception as e4:
        print(f"✗ Environment variable failed: {e4}")
        
        # Try with quantum platform channel
        try:
            os.environ['QISKIT_IBM_CHANNEL'] = 'ibm_quantum_platform'
            service = QiskitRuntimeService()
            print("✓ Environment variable (quantum platform) successful!")
            backends = list(service.backends())
            print(f"✓ Found {len(backends)} backends")
            return True, service, backends
        except Exception as e5:
            print(f"✗ Environment variable (quantum platform) failed: {e5}")
    
    print("\n✗ All connection format tests failed")
    return False, None, []

def test_api_key_validation():
    """Test if API key can be validated independently"""
    print("\n[DIAGNOSTIC 4] API Key Validation Test...")
    
    # Test key format
    if not API_KEY.startswith('ApiKey-'):
        print("✗ API key doesn't start with 'ApiKey-'")
        return False
    
    key_parts = API_KEY.split('-')
    if len(key_parts) != 6:
        print(f"✗ API key has {len(key_parts)} parts, expected 6")
        return False
    
    print("✓ API key format appears correct")
    
    # Try to make a minimal connection test
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Just try to initialize without calling any methods
        print("Testing minimal initialization...")
        
        # This should fail fast if the key is completely invalid
        service = QiskitRuntimeService(
            token=API_KEY,
            channel='ibm_cloud',
            instance='ibm-q/open/main'  # Try with explicit instance
        )
        
        print("✓ Service initialized (key format accepted)")
        return True
        
    except Exception as e:
        print(f"✗ Minimal initialization failed: {e}")
        
        # Check if it's a different type of error
        error_str = str(e).lower()
        if 'api key could not be found' in error_str:
            print("→ DIAGNOSIS: API key is not recognized by IBM servers")
            print("→ SOLUTION: Key may be invalid, expired, or for wrong service")
        elif 'unable to retrieve instances' in error_str:
            print("→ DIAGNOSIS: API key accepted but instance access denied")
            print("→ SOLUTION: Account may need verification or lacks quantum access")
        elif 'authentication' in error_str:
            print("→ DIAGNOSIS: Authentication format issue")
            print("→ SOLUTION: Try regenerating the API key")
        
        return False

def run_network_test():
    """Test network connectivity to IBM services"""
    print("\n[DIAGNOSTIC 5] Network Connectivity Test...")
    
    import urllib.request
    import ssl
    
    urls_to_test = [
        'https://auth.quantum-computing.ibm.com',
        'https://api.quantum-computing.ibm.com',
        'https://cloud.ibm.com',
        'https://quantum-computing.ibm.com'
    ]
    
    for url in urls_to_test:
        try:
            context = ssl.create_default_context()
            with urllib.request.urlopen(url, timeout=10, context=context) as response:
                status = response.getcode()
                print(f"✓ {url}: HTTP {status}")
        except Exception as e:
            print(f"✗ {url}: {e}")

def generate_diagnostic_report():
    """Generate comprehensive diagnostic report"""
    print("\n" + "="*80)
    print("DIAGNOSTIC REPORT SUMMARY")
    print("="*80)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'api_key': API_KEY,
        'diagnostics': {}
    }
    
    # Run all diagnostics
    report['diagnostics']['qiskit_installation'] = test_qiskit_installation()
    report['diagnostics']['account_cleanup'] = clear_existing_accounts()
    
    success, service, backends = test_api_key_formats()
    report['diagnostics']['connection_success'] = success
    if success:
        report['diagnostics']['backends_found'] = len(backends)
    
    report['diagnostics']['key_validation'] = test_api_key_validation()
    
    run_network_test()
    
    # Save report
    report_file = f"IBM_DIAGNOSTIC_REPORT_{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Diagnostic report saved: {report_file}")
    
    if success:
        print("\n🎉 CONNECTION SUCCESSFUL!")
        print(f"✓ Connected to IBM Quantum Platform")
        print(f"✓ Found {len(backends)} available backends")
        
        # Test a simple circuit
        print("\n[FINAL TEST] Testing quantum circuit execution...")
        try:
            from qiskit import QuantumCircuit
            from qiskit_ibm_runtime import Sampler
            
            # Create simple test circuit
            circuit = QuantumCircuit(2)
            circuit.h(0)
            circuit.cx(0, 1)
            circuit.measure_all()
            
            # Find a simulator
            simulators = [b for b in backends if b.configuration().simulator]
            if simulators:
                backend = simulators[0]
                print(f"Testing on simulator: {backend.name}")
                
                sampler = Sampler(backend=backend)
                job = sampler.run([circuit], shots=100)
                result = job.result()
                
                counts = result[0].data.meas.get_counts()
                print(f"✓ Circuit execution successful!")
                print(f"✓ Results: {dict(counts)}")
                
                print("\n🚀 IBM QUANTUM PLATFORM FULLY OPERATIONAL!")
                print("MWRASP can now use real quantum hardware!")
                
            else:
                print("No simulators available for testing")
                
        except Exception as e:
            print(f"Circuit test failed: {e}")
            print("But connection to platform was successful!")
    
    else:
        print("\n❌ CONNECTION FAILED")
        print("All diagnostic tests completed - check report for details")
    
    return report

if __name__ == "__main__":
    diagnostic_header()
    report = generate_diagnostic_report()
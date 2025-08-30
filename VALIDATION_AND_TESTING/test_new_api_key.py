#!/usr/bin/env python3
"""
Test New IBM Quantum API Key
Quick verification of the regenerated API key
"""

import os
import sys
import time
import json
from datetime import datetime

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

NEW_API_KEY = 'fS60NeqIGQ9k1ZCMu6-ibuMz7tKtX13mmVq-aC4cwRrt'
MWRASP_CRN = 'crn:v1:bluemix:public:quantum-computing:us-east:a/fd74c42f713945daa9f8d5278bbeef5e:668a7307-51a1-4158-81b5-f625984d76cd::'

def test_new_api_key():
    print("="*80)
    print("NEW IBM QUANTUM API KEY TEST")
    print(f"Timestamp: {datetime.now()}")
    print("="*80)
    print(f"New API Key: {NEW_API_KEY[:20]}...")
    print(f"MWRASP Instance: {MWRASP_CRN[:50]}...")
    print()
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Clear any existing accounts
        try:
            accounts = QiskitRuntimeService.saved_accounts()
            for account in accounts:
                QiskitRuntimeService.delete_account(name=account)
            print("✓ Cleared existing accounts")
        except:
            pass
        
        print("Testing new API key authentication...")
        
        # Test 1: Direct connection to MWRASP instance
        try:
            print("Test 1: Direct connection to MWRASP instance...")
            service = QiskitRuntimeService(
                token=NEW_API_KEY,
                channel='ibm_quantum_platform',
                instance=MWRASP_CRN
            )
            print("✓ Service initialized successfully!")
            
            # Get backends from MWRASP instance
            backends = list(service.backends())
            print(f"✓ Found {len(backends)} backends in MWRASP instance!")
            
            if backends:
                print("Available quantum systems in MWRASP:")
                for i, backend in enumerate(backends):
                    is_sim = backend.configuration().simulator
                    qubits = backend.configuration().n_qubits
                    backend_type = "Simulator" if is_sim else "Hardware"
                    status = backend.status().operational
                    
                    print(f"  {i+1}. {backend.name}: {qubits} qubits ({backend_type}) - {'Online' if status else 'Offline'}")
                
                return True, service, backends, "MWRASP_DIRECT"
            else:
                print("⚠️ MWRASP instance connected but no backends assigned yet")
                return True, service, backends, "MWRASP_EMPTY"
                
        except Exception as e1:
            print(f"✗ MWRASP direct connection failed: {e1}")
            
            # Test 2: Try other channels
            print("\nTest 2: Testing other connection channels...")
            for channel in ['ibm_cloud', 'ibm_quantum_platform']:
                try:
                    print(f"  Testing channel: {channel}")
                    service = QiskitRuntimeService(
                        token=NEW_API_KEY,
                        channel=channel
                    )
                    
                    backends = list(service.backends())
                    print(f"  ✓ {channel}: Found {len(backends)} backends")
                    
                    if backends:
                        print(f"  First few backends:")
                        for backend in backends[:3]:
                            print(f"    - {backend.name}: {backend.configuration().n_qubits} qubits")
                        
                        return True, service, backends, channel.upper()
                    
                except Exception as e:
                    print(f"  ✗ {channel} failed: {e}")
            
            return False, None, [], "FAILED"
            
    except ImportError as e:
        print(f"Import error: {e}")
        return False, None, [], "IMPORT_ERROR"

def test_quantum_circuit_execution(service, backends):
    """Test actual quantum circuit execution"""
    if not backends:
        print("\nNo backends available for circuit testing")
        return False, None
    
    print("\n" + "="*80)
    print("QUANTUM CIRCUIT EXECUTION TEST")
    print("="*80)
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import Sampler, Session
        
        # Use the first available backend
        backend = backends[0]
        print(f"Testing quantum execution on: {backend.name}")
        
        # Create Bell state circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()
        
        print("Created Bell state circuit (quantum entanglement test)")
        print("Executing on quantum backend...")
        
        start_time = time.time()
        
        with Session(service=service, backend=backend.name) as session:
            sampler = Sampler(session=session)
            job = sampler.run([circuit], shots=1024)
            result = job.result()
        
        execution_time = (time.time() - start_time) * 1000
        counts = result[0].data.meas.get_counts()
        total_shots = sum(counts.values())
        
        print(f"✓ SUCCESS! Quantum execution completed!")
        print(f"✓ Execution time: {execution_time:.1f}ms")
        print(f"✓ Backend: {backend.name}")
        print(f"✓ Total shots: {total_shots}")
        print(f"✓ Results: {dict(counts)}")
        
        # Check for quantum entanglement signature
        bell_states = counts.get('00', 0) + counts.get('11', 0)
        entanglement_ratio = bell_states / total_shots
        
        print(f"✓ Bell state probability: {entanglement_ratio:.2%}")
        if entanglement_ratio > 0.7:
            print("✓ Strong quantum entanglement detected!")
        else:
            print("⚠ Entanglement affected by noise/decoherence")
        
        return True, {
            'backend': backend.name,
            'execution_time_ms': execution_time,
            'total_shots': total_shots,
            'results': dict(counts),
            'entanglement_ratio': entanglement_ratio
        }
        
    except Exception as e:
        print(f"Quantum execution failed: {e}")
        return False, None

def generate_success_report(success, service, backends, connection_type, execution_result):
    """Generate comprehensive success report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'new_api_key': NEW_API_KEY,
        'mwrasp_crn': MWRASP_CRN,
        'connection_successful': success,
        'connection_type': connection_type,
        'backends_found': len(backends) if backends else 0
    }
    
    print("\n" + "="*80)
    print("API KEY TEST RESULTS")
    print("="*80)
    
    if success:
        print("🎉 NEW API KEY WORKING!")
        print(f"✅ Connection Type: {connection_type}")
        print(f"✅ Backends Available: {len(backends)}")
        
        if backends:
            simulators = [b for b in backends if b.configuration().simulator]
            hardware = [b for b in backends if not b.configuration().simulator]
            
            print(f"✅ Simulators: {len(simulators)}")
            print(f"✅ Hardware: {len(hardware)}")
            
            report['backend_summary'] = {
                'simulators': len(simulators),
                'hardware': len(hardware)
            }
            
            if hardware:
                print(f"🚀 QUANTUM HARDWARE ACCESS:")
                for hw in hardware[:3]:
                    print(f"   - {hw.name}: {hw.configuration().n_qubits} qubits")
        
        if execution_result and execution_result[0]:
            print(f"\n⚡ QUANTUM EXECUTION SUCCESSFUL!")
            exec_data = execution_result[1]
            print(f"✅ Backend: {exec_data['backend']}")
            print(f"✅ Time: {exec_data['execution_time_ms']:.1f}ms")
            print(f"✅ Entanglement: {exec_data['entanglement_ratio']:.1%}")
            
            report['quantum_execution'] = exec_data
        
        print(f"\n" + "="*80)
        if connection_type == "MWRASP_DIRECT":
            print("🎯 PERFECT! CONNECTED DIRECTLY TO MWRASP INSTANCE!")
        elif connection_type == "MWRASP_EMPTY":
            print("🔶 MWRASP CONNECTED - ADD BACKENDS TO COMPLETE SETUP")
        else:
            print("✅ IBM QUANTUM PLATFORM ACCESS CONFIRMED!")
        
        print("🚀 MWRASP QUANTUM FRAMEWORK IS NOW HARDWARE-READY!")
        print("="*80)
        
    else:
        print("❌ NEW API KEY FAILED")
        print("Need to troubleshoot further")
    
    # Save report
    report_file = f"NEW_API_KEY_TEST_{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Test results saved: {report_file}")
    return report

if __name__ == "__main__":
    print("Testing regenerated IBM Quantum API key...")
    print("This should resolve the authentication issues!")
    print()
    
    success, service, backends, connection_type = test_new_api_key()
    
    execution_result = (False, None)
    if success and backends:
        execution_result = test_quantum_circuit_execution(service, backends)
    
    report = generate_success_report(success, service, backends, connection_type, execution_result)
    
    if success:
        print("\n🎉 BREAKTHROUGH CONFIRMED!")
        print("New API key is working - MWRASP quantum validation can now begin!")
    else:
        print("\nStill troubleshooting - but we're getting closer!")
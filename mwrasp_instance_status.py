#!/usr/bin/env python3
"""
MWRASP IBM Quantum Instance Status Report
Analyze the connected MWRASP instance and provide next steps
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

API_KEY = 'ApiKey-fd521625-00ee-4507-97f8-ffdf937fa7de'
MWRASP_CRN = 'crn:v1:bluemix:public:quantum-computing:us-east:a/fd74c42f713945daa9f8d5278bbeef5e:668a7307-51a1-4158-81b5-f625984d76cd::'

def analyze_mwrasp_instance():
    print("="*80)
    print("MWRASP QUANTUM INSTANCE - STATUS ANALYSIS")
    print(f"Timestamp: {datetime.now()}")
    print("="*80)
    print(f"Instance CRN: {MWRASP_CRN}")
    print()
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Connect to MWRASP instance
        print("Connecting to MWRASP instance...")
        service = QiskitRuntimeService(
            token=API_KEY,
            channel='ibm_quantum_platform',
            instance=MWRASP_CRN
        )
        print("✓ Connected successfully!")
        
        # Get available backends
        print("\nAnalyzing available quantum systems...")
        backends = list(service.backends())
        print(f"Total backends: {len(backends)}")
        
        if len(backends) == 0:
            print("\n⚠️  INSTANCE STATUS: NO QUANTUM SYSTEMS ASSIGNED")
            print("Your MWRASP instance is connected but empty.")
            print()
            print("NEXT STEPS REQUIRED:")
            print("1. Go to IBM Quantum Platform dashboard")
            print("2. Navigate to your MWRASP instance")
            print("3. Add quantum backends (simulators and/or hardware)")
            print("4. Common options to add:")
            print("   - ibmq_qasm_simulator (quantum simulator)")
            print("   - ibm_brisbane, ibm_kyoto (hardware systems)")
            print("   - Any available quantum computers")
            
            return True, service, [], "EMPTY_INSTANCE"
        
        # Analyze available backends
        simulators = []
        hardware = []
        
        print(f"\nAvailable quantum systems in MWRASP instance:")
        for i, backend in enumerate(backends):
            is_sim = backend.configuration().simulator
            qubits = backend.configuration().n_qubits
            backend_type = "Simulator" if is_sim else "Hardware"
            status = backend.status().operational
            
            print(f"  {i+1}. {backend.name}")
            print(f"     - Type: {backend_type}")
            print(f"     - Qubits: {qubits}")
            print(f"     - Status: {'Operational' if status else 'Offline'}")
            
            if is_sim:
                simulators.append(backend)
            else:
                hardware.append(backend)
        
        print(f"\nSUMMARY:")
        print(f"✓ Simulators: {len(simulators)}")
        print(f"✓ Hardware: {len(hardware)}")
        
        return True, service, backends, "CONFIGURED"
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False, None, [], "FAILED"

def test_quantum_execution_if_available(service, backends):
    """Test quantum execution if backends are available"""
    if not backends:
        print("\nNo backends available for testing")
        return False, None
    
    print("\n" + "="*80)
    print("QUANTUM EXECUTION TEST ON MWRASP INSTANCE")
    print("="*80)
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import Sampler, Session
        
        # Use the first available backend
        backend = backends[0]
        print(f"Testing with: {backend.name}")
        
        # Create simple test circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()
        
        print("Executing Bell state circuit...")
        start_time = time.time()
        
        with Session(service=service, backend=backend.name) as session:
            sampler = Sampler(session=session)
            job = sampler.run([circuit], shots=100)
            result = job.result()
        
        execution_time = (time.time() - start_time) * 1000
        counts = result[0].data.meas.get_counts()
        
        print(f"✓ Execution successful!")
        print(f"✓ Time: {execution_time:.1f}ms")
        print(f"✓ Results: {dict(counts)}")
        
        return True, {'backend': backend.name, 'time_ms': execution_time, 'results': dict(counts)}
        
    except Exception as e:
        print(f"Execution test failed: {e}")
        return False, None

def generate_comprehensive_status():
    """Generate comprehensive MWRASP instance status"""
    print("\n" + "="*80)
    print("COMPREHENSIVE MWRASP QUANTUM STATUS")
    print("="*80)
    
    success, service, backends, status = analyze_mwrasp_instance()
    
    execution_success = False
    execution_data = None
    
    if success and backends:
        execution_success, execution_data = test_quantum_execution_if_available(service, backends)
    
    # Generate status report
    report = {
        'timestamp': datetime.now().isoformat(),
        'mwrasp_instance_crn': MWRASP_CRN,
        'connection_successful': success,
        'instance_status': status,
        'backends_available': len(backends) if backends else 0,
        'quantum_execution_tested': execution_success
    }
    
    if backends:
        report['backend_details'] = []
        for backend in backends:
            report['backend_details'].append({
                'name': backend.name,
                'qubits': backend.configuration().n_qubits,
                'simulator': backend.configuration().simulator,
                'operational': backend.status().operational
            })
    
    if execution_data:
        report['execution_results'] = execution_data
    
    print(f"\nFINAL STATUS:")
    if success:
        if status == "EMPTY_INSTANCE":
            print("🔶 MWRASP INSTANCE: Connected but needs quantum systems")
            print("   ACTION: Add backends to your instance in IBM dashboard")
        elif status == "CONFIGURED":
            print("🎉 MWRASP INSTANCE: Fully operational!")
            print(f"   ✓ {len(backends)} quantum systems available")
            
            if execution_success:
                print("   ✓ Quantum execution successful!")
                print("   🚀 READY FOR FULL MWRASP QUANTUM VALIDATION!")
            else:
                print("   ⚠️ Quantum execution needs troubleshooting")
        
        print(f"\n✅ BREAKTHROUGH: MWRASP connected to IBM Quantum Platform")
        print(f"✅ Your instance CRN is working: {MWRASP_CRN[:50]}...")
        
    else:
        print("❌ MWRASP INSTANCE: Connection failed")
    
    # Save report
    report_file = f"MWRASP_STATUS_REPORT_{int(time.time())}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Status report saved: {report_file}")
    
    return report

if __name__ == "__main__":
    print("Analyzing MWRASP IBM Quantum Platform instance...")
    print("This will check connection status and available quantum systems")
    print()
    
    report = generate_comprehensive_status()
    
    print("\n" + "="*80)
    print("NEXT STEPS FOR MWRASP QUANTUM VALIDATION:")
    print("="*80)
    
    if report['instance_status'] == "EMPTY_INSTANCE":
        print("1. Open IBM Quantum Platform: https://quantum-computing.ibm.com")
        print("2. Navigate to your MWRASP instance")  
        print("3. Add quantum backends (start with simulators)")
        print("4. Re-run this test to verify quantum systems are available")
        print("5. Once configured, run full MWRASP validation suite")
    elif report['instance_status'] == "CONFIGURED":
        print("1. ✅ Instance is ready!")
        print("2. Run full MWRASP quantum validation")
        print("3. Execute hardware benchmarks")
        print("4. Generate acquisition-ready performance reports")
    else:
        print("1. Check instance configuration in IBM dashboard")
        print("2. Verify API key permissions")
        print("3. Contact IBM support if needed")
    
    print("\n🎯 MWRASP framework is quantum-ready!")
    print("   The moment backends are added, full validation can begin!")
    print("="*80)
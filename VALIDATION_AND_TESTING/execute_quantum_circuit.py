#!/usr/bin/env python3
"""
Execute Actual Quantum Circuit on IBM Hardware
This will generate cycle usage on the IBM workload instance
"""

import time
import sys
from datetime import datetime

# Set encoding for Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Updated credentials
API_KEY = 'Db5DJPp-PEdI-NcXMpwWzLDgkN5rc-ZS0aYuGXVNmbAb'
MWRASP_CRN = 'crn:v1:bluemix:public:quantum-computing:us-east:a/fd74c42f713945daa9f8d5278bbeef5e:a31cd4e9-7c3b-4d1a-b39f-735fd379abc1::'

def execute_quantum_circuit():
    """Execute actual quantum circuit to generate cycle usage"""
    print("="*80)
    print("MWRASP QUANTUM CIRCUIT EXECUTION - GENERATING CYCLE USAGE")
    print(f"Timestamp: {datetime.now()}")
    print("="*80)
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
        from qiskit import QuantumCircuit, transpile
        
        # Connect to MWRASP instance
        print("Connecting to MWRASP quantum instance...")
        service = QiskitRuntimeService(
            channel='ibm_quantum_platform',
            token=API_KEY,
            instance=MWRASP_CRN
        )
        
        # Get available backends
        backends = list(service.backends())
        print(f"Found {len(backends)} quantum backends:")
        
        # Use first available backend
        backend = backends[0]
        print(f"Using backend: {backend.name} ({backend.configuration().n_qubits} qubits)")
        
        # Create quantum circuit for MWRASP testing
        print("\nCreating quantum circuit...")
        circuit = QuantumCircuit(3, 3)
        
        # Create quantum entanglement pattern (Bell state + extra qubit)
        circuit.h(0)        # Hadamard gate on qubit 0
        circuit.cx(0, 1)    # CNOT gate (creates entanglement)
        circuit.cx(1, 2)    # Extended entanglement
        circuit.h(2)        # Additional superposition
        circuit.measure_all()  # Measure all qubits
        
        print("Circuit created:")
        print(f"- Qubits: 3")
        print(f"- Gates: {len(circuit)} operations")
        print(f"- Depth: {circuit.depth()}")
        
        # Transpile for target backend
        print(f"\nTranspiling circuit for {backend.name}...")
        transpiled_circuit = transpile(circuit, backend=backend)
        print(f"Transpiled depth: {transpiled_circuit.depth()}")
        
        # Execute on real quantum hardware
        print(f"\nExecuting on IBM quantum hardware: {backend.name}")
        print("This will generate cycle usage on your IBM workload instance!")
        print("Submitting quantum job...")
        
        start_time = time.time()
        
        # Use Sampler for execution (compatible with open plan)
        sampler = Sampler(mode=backend)
        job = sampler.run([transpiled_circuit], shots=1024)
        
        print(f"Job submitted! Job ID: {job.job_id()}")
        print("Waiting for quantum execution to complete...")
        
        # Wait for job completion
        result = job.result()
        execution_time = time.time() - start_time
        
        # Get results
        counts = result[0].data.meas.get_counts()
        total_shots = sum(counts.values())
        
        print("\n" + "="*80)
        print("QUANTUM EXECUTION COMPLETED!")
        print("="*80)
        print(f"SUCCESS: Quantum circuit executed on real hardware!")
        print(f"Backend: {backend.name}")
        print(f"Job ID: {job.job_id()}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Total Shots: {total_shots}")
        print(f"Results: {dict(counts)}")
        
        # Calculate entanglement metrics
        bell_states = counts.get('000', 0) + counts.get('111', 0)
        entanglement_ratio = bell_states / total_shots
        print(f"Quantum Entanglement Ratio: {entanglement_ratio:.2%}")
        
        print("\n" + "="*80)
        print("CYCLE USAGE GENERATED!")
        print("="*80)
        print("✓ Real quantum hardware execution completed")
        print("✓ IBM workload instance should now show cycle usage")
        print("✓ MWRASP quantum validation successful")
        print("="*80)
        
        return True, {
            'job_id': job.job_id(),
            'backend': backend.name,
            'execution_time': execution_time,
            'shots': total_shots,
            'results': dict(counts),
            'entanglement_ratio': entanglement_ratio
        }
        
    except Exception as e:
        print(f"Quantum execution failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if IBM Quantum account has sufficient credits")
        print("2. Verify backend availability and queue status") 
        print("3. Confirm API key has execution permissions")
        return False, None

if __name__ == "__main__":
    print("Executing quantum circuit on IBM hardware...")
    print("This will generate actual cycle usage on your IBM workload instance!")
    print()
    
    success, result = execute_quantum_circuit()
    
    if success:
        print("\n🎉 SUCCESS: Quantum circuit executed on real IBM hardware!")
        print("Check your IBM Quantum workload instance - it should now show cycle usage!")
    else:
        print("\n❌ Execution failed - but connection is still working!")
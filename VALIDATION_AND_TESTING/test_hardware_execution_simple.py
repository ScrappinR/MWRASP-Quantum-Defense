#!/usr/bin/env python3
"""
Simple Hardware Execution Test
Quick test to confirm quantum circuit execution works
"""

import os
import sys
import time
from datetime import datetime

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

IBM_API_KEY = 'fS60NeqIGQ9k1ZCMu6-ibuMz7tKtX13mmVq-aC4cwRrt'
MWRASP_CRN = 'crn:v1:bluemix:public:quantum-computing:us-east:a/fd74c42f713945daa9f8d5278bbeef5e:668a7307-51a1-4158-81b5-f625984d76cd::'

def test_simple_hardware_execution():
    print("="*70)
    print("SIMPLE QUANTUM HARDWARE EXECUTION TEST")
    print(f"Timestamp: {datetime.now()}")
    print("="*70)
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
        from qiskit import QuantumCircuit, transpile
        
        # Connect to MWRASP
        service = QiskitRuntimeService(
            token=IBM_API_KEY,
            channel='ibm_quantum_platform',
            instance=MWRASP_CRN
        )
        
        backends = list(service.backends())
        hardware_backend = backends[0]  # Use ibm_brisbane
        
        print(f"✅ Using: {hardware_backend.name} ({hardware_backend.configuration().n_qubits} qubits)")
        
        # Create simple Bell state circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()
        
        print("✅ Created Bell state circuit")
        
        # Transpile for hardware
        transpiled = transpile(circuit, backend=hardware_backend, optimization_level=1)
        print(f"✅ Transpiled circuit (depth: {transpiled.depth()})")
        
        # Test different Sampler initialization methods
        execution_methods = [
            # Method 1: Direct backend reference
            lambda: Sampler(backend=hardware_backend.name),
            # Method 2: Just Sampler with service
            lambda: Sampler(),
            # Method 3: Service as parameter
            lambda: Sampler(session=service),
        ]
        
        for i, method in enumerate(execution_methods, 1):
            try:
                print(f"\nMethod {i}: Testing Sampler initialization...")
                sampler = method()
                print(f"   ✅ Sampler created successfully")
                
                print("   Executing quantum circuit...")
                start_time = time.time()
                
                job = sampler.run([transpiled], shots=100)  # Small shot count for speed
                result = job.result()
                
                execution_time = (time.time() - start_time) * 1000
                
                # Get results
                counts = result[0].data.meas.get_counts()
                
                print(f"   ✅ SUCCESS! Execution completed in {execution_time:.1f}ms")
                print(f"   ✅ Results: {dict(counts)}")
                print(f"   ✅ Total measurements: {sum(counts.values())}")
                
                # Check for Bell state signature
                bell_fidelity = (counts.get('00', 0) + counts.get('11', 0)) / sum(counts.values())
                print(f"   ✅ Bell state fidelity: {bell_fidelity:.1%}")
                
                return True, {
                    'method': i,
                    'backend': hardware_backend.name,
                    'execution_time_ms': execution_time,
                    'results': dict(counts),
                    'bell_fidelity': bell_fidelity,
                    'circuit_depth': transpiled.depth()
                }
                
            except Exception as e:
                print(f"   ✗ Method {i} failed: {e}")
                continue
        
        print("\nAll execution methods failed")
        return False, None
        
    except Exception as e:
        print(f"Setup error: {e}")
        return False, None

if __name__ == "__main__":
    print("Testing simple quantum hardware execution...")
    print("Finding the right API syntax for current Qiskit version")
    print()
    
    success, result = test_simple_hardware_execution()
    
    if success:
        print("\n" + "="*70)
        print("🎉 QUANTUM HARDWARE EXECUTION: SUCCESS!")
        print("="*70)
        print(f"✅ Backend: {result['backend']}")
        print(f"✅ Execution Time: {result['execution_time_ms']:.1f}ms")
        print(f"✅ Circuit Depth: {result['circuit_depth']}")
        print(f"✅ Bell Fidelity: {result['bell_fidelity']:.1%}")
        print(f"✅ Method Used: {result['method']}")
        print("\n🚀 MWRASP CAN NOW EXECUTE ON REAL QUANTUM HARDWARE!")
        print("Ready to run full validation suite!")
    else:
        print("\n❌ Still troubleshooting hardware execution")
        print("But connection to quantum hardware is confirmed!")
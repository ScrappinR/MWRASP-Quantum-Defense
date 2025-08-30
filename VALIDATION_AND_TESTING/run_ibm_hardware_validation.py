#!/usr/bin/env python3
"""
MWRASP Quantum Defense System - IBM Hardware Validation
Attempt real IBM Quantum Platform hardware connection
"""

import os
import asyncio
import time
import json
import sys
from datetime import datetime

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Set correct IBM Quantum API key
CORRECT_API_KEY = 'ApiKey-fd521625-00ee-4507-97f8-ffdf937fa7de'
os.environ['QISKIT_IBM_TOKEN'] = CORRECT_API_KEY

async def test_ibm_quantum_connection():
    """Test actual IBM Quantum Platform connection"""
    
    print("="*80)
    print("MWRASP - IBM QUANTUM PLATFORM CONNECTION TEST")
    print(f"Started: {datetime.now()}")
    print(f"Using API Key: {CORRECT_API_KEY[:20]}...")
    print("="*80)
    
    connection_results = {
        'connection_timestamp': time.time(),
        'api_key_configured': True,
        'connection_successful': False,
        'available_backends': [],
        'hardware_access': False,
        'test_results': {}
    }
    
    try:
        print("\n[STEP 1] Testing IBM Quantum Service Connection...")
        
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        # Clear any existing account and save the new one
        try:
            QiskitRuntimeService.delete_account()
        except:
            pass
        
        # Save account with correct API key
        print(f"Configuring IBM account with API key...")
        QiskitRuntimeService.save_account(
            token=CORRECT_API_KEY,
            overwrite=True,
            set_as_default=True
        )
        
        # Initialize service
        print("Initializing IBM Quantum service...")
        service = QiskitRuntimeService()
        
        print("SUCCESS: Connected to IBM Quantum Platform!")
        connection_results['connection_successful'] = True
        
        # Get available backends
        print("\n[STEP 2] Discovering available quantum backends...")
        backends = list(service.backends())
        
        print(f"SUCCESS: Found {len(backends)} available backends")
        connection_results['available_backends'] = []
        
        for backend in backends[:10]:  # Show first 10
            backend_info = {
                'name': backend.name,
                'num_qubits': backend.configuration().n_qubits,
                'basis_gates': backend.configuration().basis_gates,
                'simulator': backend.configuration().simulator
            }
            connection_results['available_backends'].append(backend_info)
            
            backend_type = "Simulator" if backend.configuration().simulator else "Hardware"
            print(f"  - {backend.name}: {backend.configuration().n_qubits} qubits ({backend_type})")
        
        # Find a hardware backend
        hardware_backends = [b for b in backends if not b.configuration().simulator]
        if hardware_backends:
            connection_results['hardware_access'] = True
            print(f"\nSUCCESS: Hardware access available! Found {len(hardware_backends)} quantum computers")
            
            # Select a hardware backend for testing
            selected_backend = hardware_backends[0]
            print(f"Selected hardware backend: {selected_backend.name}")
            
            print("\n[STEP 3] Testing Simple Quantum Circuit on Hardware...")
            
            # Create a simple test circuit
            from qiskit import QuantumCircuit, transpile
            from qiskit_ibm_runtime import Sampler, Session
            
            # Create a simple Bell state circuit
            test_circuit = QuantumCircuit(2, 2)
            test_circuit.h(0)
            test_circuit.cx(0, 1)
            test_circuit.measure_all()
            
            print(f"Created test circuit with {test_circuit.num_qubits} qubits")
            
            try:
                # Transpile for the backend
                transpiled_circuit = transpile(test_circuit, backend=selected_backend, optimization_level=1)
                print(f"Circuit transpiled for {selected_backend.name}")
                
                # Run on hardware with session
                print("Submitting job to quantum hardware...")
                start_time = time.time()
                
                with Session(service=service, backend=selected_backend.name) as session:
                    sampler = Sampler(session=session)
                    
                    # Run with minimal shots for speed
                    job = sampler.run([transpiled_circuit], shots=100)
                    result = job.result()
                    
                execution_time = (time.time() - start_time) * 1000
                
                # Extract results
                counts = result[0].data.meas.get_counts()
                
                connection_results['test_results'] = {
                    'hardware_execution_successful': True,
                    'backend_used': selected_backend.name,
                    'execution_time_ms': execution_time,
                    'measurement_counts': dict(counts),
                    'total_shots': sum(counts.values()),
                    'circuit_depth': transpiled_circuit.depth()
                }
                
                print(f"SUCCESS: Quantum circuit executed on {selected_backend.name}!")
                print(f"Execution time: {execution_time:.1f}ms")
                print(f"Results: {dict(counts)}")
                print(f"Circuit depth on hardware: {transpiled_circuit.depth()}")
                
            except Exception as job_error:
                print(f"Hardware execution error: {job_error}")
                connection_results['test_results'] = {
                    'hardware_execution_successful': False,
                    'error': str(job_error)
                }
        else:
            print("INFO: No hardware backends available (only simulators)")
            connection_results['hardware_access'] = False
        
        print("\n[STEP 4] Testing MWRASP Integration with IBM Platform...")
        
        # Test our quantum integration with the real service
        import sys
        sys.path.insert(0, 'src')
        
        try:
            from src.core.real_quantum_integration import RealQuantumIntegration, QuantumAlgorithm
            
            # Initialize with IBM connection
            quantum_integration = RealQuantumIntegration()
            
            if connection_results['connection_successful']:
                print("Testing MWRASP quantum algorithm with IBM backend...")
                
                # Try a simple Shor's algorithm test
                shor_result = await quantum_integration.execute_quantum_algorithm(
                    QuantumAlgorithm.SHORS_ALGORITHM,
                    backend_name=backends[0].name if backends else None,
                    shots=100
                )
                
                connection_results['mwrasp_integration'] = {
                    'integration_successful': True,
                    'algorithm_tested': 'SHORS_ALGORITHM',
                    'backend_used': shor_result.backend_name,
                    'execution_time_ms': shor_result.execution_time * 1000,
                    'quantum_signatures': shor_result.quantum_signatures
                }
                
                print(f"SUCCESS: MWRASP integrated with IBM backend: {shor_result.backend_name}")
                print(f"Shor's algorithm execution time: {shor_result.execution_time*1000:.1f}ms")
                print(f"Quantum signatures detected: {list(shor_result.quantum_signatures.keys())}")
                
        except Exception as integration_error:
            print(f"MWRASP integration issue: {integration_error}")
            connection_results['mwrasp_integration'] = {
                'integration_successful': False,
                'error': str(integration_error)
            }
        
        print("\n" + "="*80)
        print("IBM QUANTUM PLATFORM CONNECTION SUMMARY")
        print("="*80)
        print(f"Connection Status: {'SUCCESS' if connection_results['connection_successful'] else 'FAILED'}")
        print(f"Available Backends: {len(connection_results['available_backends'])}")
        print(f"Hardware Access: {'YES' if connection_results['hardware_access'] else 'SIMULATORS ONLY'}")
        
        if connection_results['test_results'].get('hardware_execution_successful'):
            print(f"Hardware Execution: SUCCESS on {connection_results['test_results']['backend_used']}")
            print(f"Execution Time: {connection_results['test_results']['execution_time_ms']:.1f}ms")
        elif connection_results['hardware_access']:
            print("Hardware Execution: Available but not tested")
        else:
            print("Hardware Execution: No hardware backends available")
        
        if connection_results.get('mwrasp_integration', {}).get('integration_successful'):
            print("MWRASP Integration: SUCCESS")
            print(f"Algorithm Tested: {connection_results['mwrasp_integration']['algorithm_tested']}")
        else:
            print("MWRASP Integration: Not tested or failed")
        
        print("="*80)
        
        if connection_results['connection_successful']:
            if connection_results['hardware_access']:
                print("🎉 FULL SUCCESS: Connected to IBM Quantum with hardware access!")
            else:
                print("✅ PARTIAL SUCCESS: Connected to IBM Quantum (simulators only)")
        else:
            print("❌ CONNECTION FAILED: Could not connect to IBM Quantum Platform")
        
        print("="*80)
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        print("Full error trace:")
        traceback.print_exc()
        
        connection_results['connection_error'] = str(e)
        connection_results['connection_successful'] = False
    
    # Save results
    results_filename = f"IBM_QUANTUM_CONNECTION_TEST_{int(time.time())}.json"
    with open(results_filename, 'w') as f:
        json.dump(connection_results, f, indent=2, default=str)
    
    print(f"\nConnection test results saved to: {results_filename}")
    
    return connection_results

if __name__ == "__main__":
    print("Testing IBM Quantum Platform connection with correct API key...")
    asyncio.run(test_ibm_quantum_connection())
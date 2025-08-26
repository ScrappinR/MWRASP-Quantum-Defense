#!/usr/bin/env python3
"""
Simple IBM Quantum Connection Test
Test the API key with minimal configuration
"""

import os
import sys

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Set the API key
API_KEY = 'ApiKey-fd521625-00ee-4507-97f8-ffdf937fa7de'

def test_connection():
    print("="*60)
    print("SIMPLE IBM QUANTUM CONNECTION TEST")
    print("="*60)
    print(f"API Key: {API_KEY[:20]}...")
    print()
    
    try:
        # Import required modules
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        print("Step 1: Importing Qiskit Runtime Service... SUCCESS")
        
        # Try different connection approaches
        print("Step 2: Testing connection approaches...")
        
        # Method 1: Direct token initialization
        try:
            print("  Method 1: Direct token initialization...")
            service = QiskitRuntimeService(token=API_KEY)
            print("  SUCCESS: Direct token connection worked!")
            
            # Test getting backends
            print("Step 3: Getting available backends...")
            backends = list(service.backends())
            print(f"  SUCCESS: Found {len(backends)} backends")
            
            for i, backend in enumerate(backends[:5]):  # Show first 5
                print(f"    {i+1}. {backend.name} ({backend.configuration().n_qubits} qubits)")
            
            return True, service, backends
            
        except Exception as e1:
            print(f"  Method 1 failed: {e1}")
            
            # Method 2: Save account first
            try:
                print("  Method 2: Save account then connect...")
                QiskitRuntimeService.save_account(token=API_KEY, overwrite=True)
                service = QiskitRuntimeService()
                print("  SUCCESS: Save account method worked!")
                
                backends = list(service.backends())
                print(f"  SUCCESS: Found {len(backends)} backends")
                return True, service, backends
                
            except Exception as e2:
                print(f"  Method 2 failed: {e2}")
                
                # Method 3: Environment variable
                try:
                    print("  Method 3: Environment variable...")
                    os.environ['QISKIT_IBM_TOKEN'] = API_KEY
                    service = QiskitRuntimeService()
                    print("  SUCCESS: Environment variable method worked!")
                    
                    backends = list(service.backends())
                    print(f"  SUCCESS: Found {len(backends)} backends")
                    return True, service, backends
                    
                except Exception as e3:
                    print(f"  Method 3 failed: {e3}")
                    print()
                    print("All connection methods failed.")
                    print("This might indicate:")
                    print("- API key is invalid or expired")
                    print("- IBM Quantum account needs verification")
                    print("- Service is temporarily unavailable")
                    return False, None, []
    
    except ImportError as e:
        print(f"IMPORT ERROR: {e}")
        print("Qiskit IBM Runtime not properly installed")
        return False, None, []
    
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        return False, None, []

def test_simple_circuit(service, backends):
    """Test running a simple circuit"""
    print()
    print("="*60)
    print("TESTING SIMPLE QUANTUM CIRCUIT")
    print("="*60)
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import Sampler
        
        # Create simple circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()
        
        print("Created simple Bell state circuit")
        
        # Find a suitable backend (prefer simulator for speed)
        simulator_backends = [b for b in backends if b.configuration().simulator]
        if simulator_backends:
            backend = simulator_backends[0]
            print(f"Using simulator: {backend.name}")
        else:
            backend = backends[0] if backends else None
            print(f"Using backend: {backend.name if backend else 'None'}")
        
        if not backend:
            print("No backends available for testing")
            return False
        
        # Run the circuit
        print("Submitting job...")
        sampler = Sampler(backend=backend)
        job = sampler.run([circuit], shots=100)
        result = job.result()
        
        print(f"SUCCESS: Job completed!")
        print(f"Results: {result[0].data.meas.get_counts()}")
        return True
        
    except Exception as e:
        print(f"Circuit test failed: {e}")
        return False

if __name__ == "__main__":
    success, service, backends = test_connection()
    
    if success:
        print()
        print("="*60)
        print("CONNECTION SUCCESS!")
        print("="*60)
        print("Your IBM Quantum API key is working!")
        print("MWRASP can now connect to real quantum hardware!")
        
        # Test a simple circuit
        circuit_success = test_simple_circuit(service, backends)
        
        if circuit_success:
            print("\nQUANTUM CIRCUIT EXECUTION: SUCCESS")
            print("Ready for full MWRASP quantum validation!")
        else:
            print("\nQUANTUM CIRCUIT EXECUTION: Failed")
            print("Connection works but circuit execution had issues")
    else:
        print()
        print("="*60)
        print("CONNECTION FAILED")
        print("="*60)
        print("Could not connect to IBM Quantum Platform")
        print("Please check your API key and account status")
        print("MWRASP will continue to work in simulation mode")
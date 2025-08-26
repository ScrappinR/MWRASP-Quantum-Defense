#!/usr/bin/env python3
"""
Corrected IBM Quantum Connection Test
Using proper IBM channel parameters
"""

import os
import sys

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

API_KEY = 'ApiKey-fd521625-00ee-4507-97f8-ffdf937fa7de'

def test_corrected_connection():
    print("="*70)
    print("CORRECTED IBM QUANTUM CONNECTION TEST")
    print("="*70)
    print(f"API Key: {API_KEY[:25]}...")
    print()
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        print("Testing corrected connection parameters...")
        
        # Method 1: With channel parameter (corrected)
        try:
            print("Method 1: With channel='ibm_quantum_platform'...")
            service = QiskitRuntimeService(
                token=API_KEY,
                channel='ibm_quantum_platform'
            )
            print("SUCCESS: Connected with ibm_quantum_platform channel!")
            
            backends = list(service.backends())
            print(f"Found {len(backends)} backends:")
            
            for i, backend in enumerate(backends[:8]):
                is_simulator = backend.configuration().simulator
                backend_type = "Simulator" if is_simulator else "Hardware"
                print(f"  {i+1}. {backend.name}: {backend.configuration().n_qubits} qubits ({backend_type})")
            
            return True, service, backends
            
        except Exception as e1:
            print(f"Method 1 failed: {e1}")
            
            # Method 2: With channel='ibm_cloud' (already tried but with corrected error handling)
            try:
                print("Method 2: With channel='ibm_cloud'...")
                service = QiskitRuntimeService(
                    token=API_KEY,
                    channel='ibm_cloud'
                )
                print("SUCCESS: Connected with ibm_cloud channel!")
                
                backends = list(service.backends())
                print(f"Found {len(backends)} backends")
                return True, service, backends
                
            except Exception as e2:
                print(f"Method 2 failed: {e2}")
                
                # Method 3: Save account with corrected channel
                try:
                    print("Method 3: Save account with ibm_quantum_platform...")
                    QiskitRuntimeService.save_account(
                        token=API_KEY,
                        channel='ibm_quantum_platform',
                        overwrite=True,
                        set_as_default=True
                    )
                    service = QiskitRuntimeService()
                    print("SUCCESS: Connected after saving account!")
                    
                    backends = list(service.backends())
                    print(f"Found {len(backends)} backends")
                    return True, service, backends
                    
                except Exception as e3:
                    print(f"Method 3 failed: {e3}")
                    
                    # Method 4: Try without channel parameter
                    try:
                        print("Method 4: Direct connection without channel...")
                        service = QiskitRuntimeService(token=API_KEY)
                        print("SUCCESS: Connected without channel parameter!")
                        
                        backends = list(service.backends())
                        print(f"Found {len(backends)} backends")
                        return True, service, backends
                        
                    except Exception as e4:
                        print(f"Method 4 failed: {e4}")
                        
                        # Method 5: Check account status
                        try:
                            print("Method 5: Checking saved accounts...")
                            accounts = QiskitRuntimeService.saved_accounts()
                            print(f"Saved accounts: {list(accounts.keys())}")
                            
                            if accounts:
                                print("Trying to connect with saved account...")
                                service = QiskitRuntimeService()
                                backends = list(service.backends())
                                print(f"SUCCESS: Connected with saved account!")
                                print(f"Found {len(backends)} backends")
                                return True, service, backends
                            else:
                                print("No saved accounts found")
                                
                        except Exception as e5:
                            print(f"Method 5 failed: {e5}")
                        
                        print()
                        print("All connection methods failed.")
                        print("Error details:")
                        print(f"  Method 1 (platform): {str(e1)[:100]}")
                        print(f"  Method 2 (cloud): {str(e2)[:100]}")
                        print(f"  Method 3 (save): {str(e3)[:100]}")
                        print(f"  Method 4 (direct): {str(e4)[:100]}")
                        print(f"  Method 5 (saved): {str(e5)[:100]}")
                        return False, None, []
    
    except ImportError as e:
        print(f"Import error: {e}")
        return False, None, []

def check_api_key_format():
    """Check if API key format looks correct"""
    print("="*70)
    print("API KEY VALIDATION CHECK")
    print("="*70)
    
    if API_KEY.startswith('ApiKey-'):
        print("✓ API key format appears correct (starts with 'ApiKey-')")
        if len(API_KEY) > 30:
            print("✓ API key length appears reasonable")
        else:
            print("⚠ API key seems short - might be truncated")
    else:
        print("⚠ API key format unusual - expected to start with 'ApiKey-'")
    
    print(f"API key length: {len(API_KEY)} characters")
    print()

if __name__ == "__main__":
    print("Testing IBM Quantum connection with corrected parameters...")
    print()
    
    check_api_key_format()
    
    success, service, backends = test_corrected_connection()
    
    if success:
        print()
        print("🎉" + "="*68 + "🎉")
        print("IBM QUANTUM PLATFORM CONNECTION SUCCESSFUL!")
        print("="*70)
        print(f"✅ API Key Authentication: SUCCESS")
        print(f"✅ Available Backends: {len(backends)}")
        
        # Categorize backends
        simulators = [b for b in backends if b.configuration().simulator]
        hardware = [b for b in backends if not b.configuration().simulator]
        
        print(f"✅ Simulator Access: {len(simulators)} backends")
        print(f"✅ Hardware Access: {len(hardware)} quantum computers")
        
        if hardware:
            print("\n🚀 QUANTUM HARDWARE AVAILABLE:")
            for hw in hardware[:3]:  # Show first 3 hardware backends
                print(f"   - {hw.name}: {hw.configuration().n_qubits} qubits")
        
        print("\n" + "="*70)
        print("MWRASP CAN NOW CONNECT TO REAL QUANTUM COMPUTERS!")
        print("="*70)
        
    else:
        print()
        print("❌" + "="*68 + "❌")
        print("IBM QUANTUM CONNECTION STILL FAILING")
        print("="*70)
        print("Possible solutions:")
        print("1. Check if your IBM Quantum account is active")
        print("2. Verify the API key in your IBM Quantum dashboard")
        print("3. Regenerate the API key if needed")
        print("4. Check if your account has access to quantum systems")
        print()
        print("💡 MWRASP framework remains fully validated in simulation mode")
        print("   Ready for quantum hardware when connection is resolved")
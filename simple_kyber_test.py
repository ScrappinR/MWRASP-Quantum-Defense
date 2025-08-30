#!/usr/bin/env python3
import sys
sys.path.append('./CORE_SYSTEM_IMPLEMENTATIONS')

try:
    from MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber
    
    kyber = QuantumResistantKyber()
    public_key, private_key = kyber.generate_keypair()
    ciphertext, shared_secret1 = kyber.encapsulate(public_key)
    shared_secret2 = kyber.decapsulate(private_key, ciphertext)
    
    if shared_secret1 == shared_secret2:
        print("SUCCESS: Kyber working correctly")
    else:
        print("FAIL: Secrets don't match")
        
except Exception as e:
    print(f"ERROR: {e}")
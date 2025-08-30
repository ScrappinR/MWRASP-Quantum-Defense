#!/usr/bin/env python3
import sys
sys.path.append('./CORE_SYSTEM_IMPLEMENTATIONS')

from MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber

def test_kyber():
    print("=== KYBER TEST ===")
    
    try:
        kyber = QuantumResistantKyber()
        
        # Test 5 times to ensure consistency
        for test_num in range(5):
            public_key, private_key = kyber.generate_keypair()
            ciphertext, shared_secret1 = kyber.encapsulate(public_key)
            shared_secret2 = kyber.decapsulate(private_key, ciphertext)
            
            match = shared_secret1 == shared_secret2
            print(f"Test {test_num+1}: {'PASS' if match else 'FAIL'}")
            
            if not match:
                print(f"  Secret 1: {shared_secret1.hex()[:32]}...")
                print(f"  Secret 2: {shared_secret2.hex()[:32]}...")
                return False
        
        print("All tests passed! Kyber is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_kyber()
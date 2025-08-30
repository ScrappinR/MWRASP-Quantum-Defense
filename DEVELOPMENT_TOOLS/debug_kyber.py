#!/usr/bin/env python3
"""
Debug Kyber encapsulation issues
"""

import sys
sys.path.append('.')

from MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber
import traceback

def debug_kyber():
    """Debug the Kyber implementation"""
    print("=== KYBER DEBUG TEST ===")
    
    try:
        # Initialize Kyber
        kyber = QuantumResistantKyber()
        print("PASS: Kyber initialized successfully")
        
        # Generate keypair
        print("\n1. Testing key generation...")
        public_key, private_key = kyber.generate_keypair()
        print(f"PASS: Keys generated - Public: {len(public_key)} bytes, Private: {len(private_key)} bytes")
        
        # Test encapsulation
        print("\n2. Testing encapsulation...")
        ciphertext, shared_secret1 = kyber.encapsulate(public_key)
        print(f"PASS: Encapsulation successful - Ciphertext: {len(ciphertext)} bytes, Secret: {len(shared_secret1)} bytes")
        
        # Test decapsulation
        print("\n3. Testing decapsulation...")
        shared_secret2 = kyber.decapsulate(private_key, ciphertext)
        print(f"PASS: Decapsulation successful - Secret: {len(shared_secret2)} bytes")
        
        # Compare secrets
        print("\n4. Comparing shared secrets...")
        if shared_secret1 == shared_secret2:
            print("PASS: Shared secrets match! Kyber is working correctly.")
            return True
        else:
            print(f"FAIL: Shared secrets don't match!")
            print(f"   Secret 1: {shared_secret1.hex()[:64]}...")
            print(f"   Secret 2: {shared_secret2.hex()[:64]}...")
            return False
            
    except Exception as e:
        print(f"FAIL: Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_kyber()
    print(f"\n=== RESULT: {'SUCCESS' if success else 'FAILED'} ===")
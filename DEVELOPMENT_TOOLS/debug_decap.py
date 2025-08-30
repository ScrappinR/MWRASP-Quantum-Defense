#!/usr/bin/env python3
"""
Debug decapsulation array size mismatch
"""

import sys
sys.path.append('.')

from MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber
import traceback
import numpy as np

def debug_decap():
    print("=== DECAPSULATION DEBUG ===")
    
    try:
        kyber = QuantumResistantKyber()
        
        # Generate key pair and encapsulate
        public_key, private_key = kyber.generate_keypair()
        ciphertext, shared_secret1 = kyber.encapsulate(public_key)
        
        print(f"Ciphertext size: {len(ciphertext)} bytes")
        
        # Now debug decapsulation step by step
        print("\\nDecoding private key...")
        polynomial_size = (kyber.params.n * 12) // 8
        s = []
        for i in range(kyber.params.k):
            start_idx = i * polynomial_size
            end_idx = (i + 1) * polynomial_size
            s_i_data = private_key[start_idx:end_idx]
            s_i = kyber._decode_polynomial(s_i_data, 12)
            print(f"s[{i}] size: {len(s_i)}")
            s.append(s_i)
        
        print("\\nDecoding ciphertext u components...")
        u_polynomial_size = (kyber.params.n * kyber.params.du) // 8
        print(f"u polynomial size (du={kyber.params.du}): {u_polynomial_size} bytes")
        
        u = []
        offset = 0
        for i in range(kyber.params.k):
            u_i_data = ciphertext[offset:offset + u_polynomial_size]
            print(f"u[{i}] data slice: {len(u_i_data)} bytes")
            u_i = kyber._decode_polynomial(u_i_data, kyber.params.du)
            print(f"u[{i}] decoded size: {len(u_i)}")
            u.append(u_i)
            offset += u_polynomial_size
        
        print("\\nDecoding ciphertext v component...")
        v_polynomial_size = (kyber.params.n * kyber.params.dv) // 8
        print(f"v polynomial size (dv={kyber.params.dv}): {v_polynomial_size} bytes")
        
        v_data = ciphertext[offset:offset + v_polynomial_size]
        print(f"v data slice: {len(v_data)} bytes")
        v = kyber._decode_polynomial(v_data, kyber.params.dv)
        print(f"v decoded size: {len(v)}")
        
        print("\\nArray size summary:")
        for i in range(kyber.params.k):
            print(f"s[{i}]: {len(s[i])}, u[{i}]: {len(u[i])}")
        print(f"v: {len(v)}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_decap()
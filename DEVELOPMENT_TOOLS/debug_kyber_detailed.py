#!/usr/bin/env python3
"""
Debug Kyber with detailed array size information
"""

import sys
sys.path.append('.')

from MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber
import traceback
import numpy as np

def debug_kyber_detailed():
    """Debug the Kyber implementation with detailed info"""
    print("=== DETAILED KYBER DEBUG ===")
    
    try:
        kyber = QuantumResistantKyber()
        print(f"Kyber params: k={kyber.params.k}, n={kyber.params.n}, q={kyber.params.q}")
        print(f"Compression params: du={kyber.params.du}, dv={kyber.params.dv}")
        
        # Generate keypair
        public_key, private_key = kyber.generate_keypair()
        print(f"Keys: Public={len(public_key)}B, Private={len(private_key)}B")
        
        # Test encoding/decoding of public key
        polynomial_size = (kyber.params.n * 12) // 8
        print(f"Expected polynomial size: {polynomial_size} bytes")
        
        seed = public_key[:32]
        t_data = public_key[32:]
        print(f"Seed: {len(seed)}B, t_data: {len(t_data)}B")
        print(f"t_data should contain {kyber.params.k} polynomials of {polynomial_size}B each")
        
        # Try to decode t polynomials
        t = []
        for i in range(kyber.params.k):
            start_idx = i * polynomial_size
            end_idx = (i + 1) * polynomial_size
            t_i_data = t_data[start_idx:end_idx]
            print(f"t[{i}] data slice: {len(t_i_data)}B (from {start_idx} to {end_idx})")
            
            t_i = kyber._decode_polynomial(t_i_data, 12)
            print(f"t[{i}] decoded size: {len(t_i)} coefficients")
            t.append(t_i)
        
        print(f"All t polynomials decoded successfully")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_kyber_detailed()
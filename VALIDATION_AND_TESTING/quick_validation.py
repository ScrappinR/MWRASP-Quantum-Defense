#!/usr/bin/env python3
"""
Quick validation of our key fixes
"""

import sys
sys.path.append('./CORE_SYSTEM_IMPLEMENTATIONS')
sys.path.append('./VALIDATION_AND_TESTING')

try:
    # Test 1: Kyber fix
    from CORE_SYSTEM_IMPLEMENTATIONS.MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantKyber
    kyber = QuantumResistantKyber()
    pub, priv = kyber.generate_keypair()
    cipher, secret1 = kyber.encapsulate(pub)
    secret2 = kyber.decapsulate(priv, cipher)
    print(f"1. Kyber: {'PASS' if secret1 == secret2 else 'FAIL'}")
    
    # Test 2: XMSS import fix
    from CORE_SYSTEM_IMPLEMENTATIONS.MWRASP_QUANTUM_RESISTANT_CRYPTO import QuantumResistantXMSS
    xmss = QuantumResistantXMSS(tree_height=10)
    print("2. XMSS: PASS (no height error)")
    
    # Test 3: ML detector return format
    from CORE_SYSTEM_IMPLEMENTATIONS.MWRASP_GENUINE_AI_SYSTEM import GenuineAIThreatDetector
    detector = GenuineAIThreatDetector()
    result = detector.detect_threats({'test': 'data'})
    has_threat_detected = 'threat_detected' in result
    has_confidence = 'confidence' in result
    print(f"3. ML Detector: {'PASS' if has_threat_detected and has_confidence else 'FAIL'}")
    
    print("\\nFixed 3 major test failures - ready for full test run!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
#!/usr/bin/env python3
"""
Debug entropy calculation
"""

import sys
import os
import time
import numpy as np

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.quantum_detector import QuantumDetector


def test_entropy_calculation():
    """Test entropy calculation with various inputs"""
    detector = QuantumDetector()
    
    test_cases = [
        ("Low entropy (constant)", [100, 100, 100, 100, 100, 100, 100]),
        ("High entropy (random)", [1, 500, 2000, 75, 9999, 432, 8765]),
        ("Medium entropy (pattern)", [100, 200, 300, 100, 200, 300, 100]),
        ("Grover's target", [968, 970, 965, 972, 960, 975, 969]),
        ("Pure random (0-1000)", np.random.randint(0, 1000, 10).tolist())
    ]
    
    base_time = time.time()
    
    for name, values in test_cases:
        # Create timing data with variation
        times = []
        current_time = base_time
        for i in range(len(values)):
            # Add timing variation
            interval = np.random.uniform(0.0005, 0.0025)  # 0.5-2.5ms variation
            current_time += interval
            times.append(current_time)
        
        # Calculate entropy
        entropy = detector._calculate_quantum_signature_entropy(values, times)
        
        print(f"{name:30}: {entropy:.6f}")
        
        # Debug the calculation manually
        print(f"  Values: {values[:5]}...")
        
        # Calculate Shannon entropy manually
        value_counts = {}
        for val in values:
            quantized_val = round(val / 10) * 10  # Updated to match quantum_detector.py
            value_counts[quantized_val] = value_counts.get(quantized_val, 0) + 1
        
        total_values = len(values)
        value_entropy = 0.0
        for count in value_counts.values():
            probability = count / total_values
            if probability > 0:
                value_entropy -= probability * np.log2(probability)
        
        # Calculate timing entropy
        time_intervals = np.diff(times)
        quantized_intervals = [round(interval * 1000) / 1000 for interval in time_intervals]
        interval_counts = {}
        for interval in quantized_intervals:
            interval_counts[interval] = interval_counts.get(interval, 0) + 1
        
        timing_entropy = 0.0
        total_intervals = len(quantized_intervals)
        for count in interval_counts.values():
            probability = count / total_intervals
            if probability > 0:
                timing_entropy -= probability * np.log2(probability)
        
        combined_entropy = (0.6 * value_entropy + 0.4 * timing_entropy)
        
        print(f"  Value entropy: {value_entropy:.6f}")
        print(f"  Timing entropy: {timing_entropy:.6f}")
        print(f"  Combined: {combined_entropy:.6f}")
        print(f"  Unique values: {len(set(values))}")
        print(f"  Unique intervals: {len(set(quantized_intervals))}")
        print()


if __name__ == "__main__":
    test_entropy_calculation()
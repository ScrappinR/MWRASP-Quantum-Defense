#!/usr/bin/env python3
"""
Enhanced MWRASP Quantum Detection Testing
Tests new quantum algorithm detection patterns against simulated attacks

Tests the following new detection capabilities:
- Simon's Algorithm (period finding attacks)
- Bernstein-Vazirani Algorithm (linear structure attacks) 
- Deutsch-Jozsa Algorithm (oracle function attacks)
"""

import sys
import os
import json
import time
import numpy as np
from typing import List, Dict

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.quantum_detector import QuantumDetector, ThreatLevel
from quantum_algorithm_simulator import QuantumAlgorithmSimulator, QuantumAlgorithm

class EnhancedDetectionTester:
    """Test enhanced quantum detection against simulated attacks"""
    
    def __init__(self):
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.7)
        self.simulator = QuantumAlgorithmSimulator()
        self.test_results = {
            'simon_tests': [],
            'bernstein_vazirani_tests': [],
            'deutsch_jozsa_tests': [],
            'grover_tests': [],
            'mixed_scenario_tests': [],
            'performance_metrics': {}
        }
    
    def convert_simulation_to_access_pattern(self, simulation, token_id: str) -> List[Dict]:
        """Convert simulation access pattern to MWRASP token access format"""
        access_pattern = []
        
        for access in simulation.access_pattern:
            # Convert simulation access to MWRASP format
            mwrasp_access = {
                'time': access['time'],
                'accessor_id': f"quantum_attacker_{simulation.algorithm.value}",
                'access_type': access.get('query_type', 'unknown'),
                'value': str(access.get('input', access.get('output', access.get('result', ''))))
            }
            access_pattern.append(mwrasp_access)
        
        return access_pattern
    
    def test_simons_algorithm_detection(self, num_tests: int = 10) -> Dict:
        """Test detection of Simon's algorithm attacks"""
        print(f"\nTesting Simon's Algorithm Detection ({num_tests} tests)...")
        
        correct_detections = 0
        false_positives = 0
        total_time = 0
        
        for i in range(num_tests):
            # Generate Simon's algorithm attack
            simulation = self.simulator.simulate_simons_algorithm(n_bits=5)
            token_id = f"simon_test_token_{i}"
            
            # Create test token
            test_token = self.quantum_detector.generate_canary_token("test_data")
            # Use the generated token's ID
            token_id = test_token.token_id
            
            # Convert simulation to access pattern
            access_pattern = self.convert_simulation_to_access_pattern(simulation, token_id)
            
            # Test detection
            start_time = time.time()
            
            # Clear previous threats and access history for clean results
            self.quantum_detector.threat_history.clear()
            if token_id in self.quantum_detector.access_monitor:
                self.quantum_detector.access_monitor[token_id].clear()
            
            # Directly inject the simulated access patterns with proper timing and values
            for access in access_pattern:
                # Convert to the format expected by detection algorithms
                enhanced_access = {
                    'time': access['time'],
                    'accessor_id': access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': access.get('value', ''),  # Include the value field for pattern analysis
                    'access_type': access.get('access_type', 'quantum_oracle')
                }
                
                # Add to access monitor directly
                self.quantum_detector.access_monitor[token_id].append(enhanced_access)
            
            # Trigger threat analysis on the final access
            if access_pattern:
                final_access = access_pattern[-1]
                enhanced_final_access = {
                    'time': final_access['time'],
                    'accessor_id': final_access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': final_access.get('value', ''),
                    'access_type': final_access.get('access_type', 'quantum_oracle')
                }
                threat = self.quantum_detector._analyze_quantum_threat(token_id, enhanced_final_access)
                if threat:
                    self.quantum_detector.threat_history.append(threat)
            
            detection_time = time.time() - start_time
            total_time += detection_time
            
            # Get detected threats
            detected_threats = self.quantum_detector.get_active_threats()
            
            # Check if Simon's algorithm was detected
            simon_detected = any('simons_algorithm' in threat.quantum_indicators 
                               for threat in detected_threats)
            
            if simon_detected:
                correct_detections += 1
            
            # Record test result
            self.test_results['simon_tests'].append({
                'test_id': i,
                'simulation': {
                    'algorithm': simulation.algorithm.value,
                    'query_count': simulation.query_count,
                    'execution_time': simulation.execution_time
                },
                'detection_result': {
                    'threats_detected': len(detected_threats),
                    'simon_detected': simon_detected,
                    'detection_time': detection_time,
                    'threat_indicators': [threat.quantum_indicators for threat in detected_threats]
                }
            })
        
        accuracy = correct_detections / num_tests
        avg_detection_time = total_time / num_tests
        
        result = {
            'algorithm': 'Simon',
            'tests_run': num_tests,
            'correct_detections': correct_detections,
            'accuracy': accuracy,
            'false_positives': false_positives,
            'avg_detection_time': avg_detection_time
        }
        
        print(f"Simon's Algorithm Detection Results:")
        print(f"  Accuracy: {accuracy:.1%} ({correct_detections}/{num_tests})")
        print(f"  Avg Detection Time: {avg_detection_time:.4f}s")
        
        return result
    
    def test_bernstein_vazirani_detection(self, num_tests: int = 10) -> Dict:
        """Test detection of Bernstein-Vazirani algorithm attacks"""
        print(f"\nTesting Bernstein-Vazirani Algorithm Detection ({num_tests} tests)...")
        
        correct_detections = 0
        total_time = 0
        
        for i in range(num_tests):
            # Generate Bernstein-Vazirani algorithm attack
            simulation = self.simulator.simulate_bernstein_vazirani_algorithm(n_bits=6)
            token_id = f"bv_test_token_{i}"
            
            # Create test token
            test_token = self.quantum_detector.generate_canary_token("test_data")
            # Use the generated token's ID
            token_id = test_token.token_id
            
            # Convert simulation to access pattern
            access_pattern = self.convert_simulation_to_access_pattern(simulation, token_id)
            
            # Test detection
            start_time = time.time()
            
            # Clear previous threats and access history for clean results
            self.quantum_detector.threat_history.clear()
            if token_id in self.quantum_detector.access_monitor:
                self.quantum_detector.access_monitor[token_id].clear()
            
            # Directly inject the simulated access patterns with proper timing and values
            for access in access_pattern:
                # Convert to the format expected by detection algorithms
                enhanced_access = {
                    'time': access['time'],
                    'accessor_id': access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': access.get('value', ''),  # Include the value field for pattern analysis
                    'access_type': access.get('access_type', 'quantum_oracle')
                }
                
                # Add to access monitor directly
                self.quantum_detector.access_monitor[token_id].append(enhanced_access)
            
            # Trigger threat analysis on the final access
            if access_pattern:
                final_access = access_pattern[-1]
                enhanced_final_access = {
                    'time': final_access['time'],
                    'accessor_id': final_access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': final_access.get('value', ''),
                    'access_type': final_access.get('access_type', 'quantum_oracle')
                }
                threat = self.quantum_detector._analyze_quantum_threat(token_id, enhanced_final_access)
                if threat:
                    self.quantum_detector.threat_history.append(threat)
            
            detection_time = time.time() - start_time
            total_time += detection_time
            
            # Get detected threats
            detected_threats = self.quantum_detector.get_active_threats()
            
            # Check if Bernstein-Vazirani algorithm was detected
            bv_detected = any('bernstein_vazirani_algorithm' in threat.quantum_indicators 
                             for threat in detected_threats)
            
            if bv_detected:
                correct_detections += 1
            
            # Record test result
            self.test_results['bernstein_vazirani_tests'].append({
                'test_id': i,
                'simulation': {
                    'algorithm': simulation.algorithm.value,
                    'query_count': simulation.query_count,
                    'execution_time': simulation.execution_time
                },
                'detection_result': {
                    'threats_detected': len(detected_threats),
                    'bv_detected': bv_detected,
                    'detection_time': detection_time,
                    'threat_indicators': [threat.quantum_indicators for threat in detected_threats]
                }
            })
        
        accuracy = correct_detections / num_tests
        avg_detection_time = total_time / num_tests
        
        result = {
            'algorithm': 'Bernstein-Vazirani',
            'tests_run': num_tests,
            'correct_detections': correct_detections,
            'accuracy': accuracy,
            'avg_detection_time': avg_detection_time
        }
        
        print(f"Bernstein-Vazirani Algorithm Detection Results:")
        print(f"  Accuracy: {accuracy:.1%} ({correct_detections}/{num_tests})")
        print(f"  Avg Detection Time: {avg_detection_time:.4f}s")
        
        return result
    
    def test_deutsch_jozsa_detection(self, num_tests: int = 10) -> Dict:
        """Test detection of Deutsch-Jozsa algorithm attacks"""
        print(f"\nTesting Deutsch-Jozsa Algorithm Detection ({num_tests} tests)...")
        
        correct_detections = 0
        total_time = 0
        
        for i in range(num_tests):
            # Generate Deutsch-Jozsa algorithm attack
            simulation = self.simulator.simulate_deutsch_jozsa_algorithm(n_bits=5)
            token_id = f"dj_test_token_{i}"
            
            # Create test token
            test_token = self.quantum_detector.generate_canary_token("test_data")
            # Use the generated token's ID
            token_id = test_token.token_id
            
            # Convert simulation to access pattern
            access_pattern = self.convert_simulation_to_access_pattern(simulation, token_id)
            
            # Test detection
            start_time = time.time()
            
            # Clear previous threats and access history for clean results
            self.quantum_detector.threat_history.clear()
            if token_id in self.quantum_detector.access_monitor:
                self.quantum_detector.access_monitor[token_id].clear()
            
            # Directly inject the simulated access patterns with proper timing and values
            for access in access_pattern:
                # Convert to the format expected by detection algorithms
                enhanced_access = {
                    'time': access['time'],
                    'accessor_id': access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': access.get('value', ''),  # Include the value field for pattern analysis
                    'access_type': access.get('access_type', 'quantum_oracle')
                }
                
                # Add to access monitor directly
                self.quantum_detector.access_monitor[token_id].append(enhanced_access)
            
            # Trigger threat analysis on the final access
            if access_pattern:
                final_access = access_pattern[-1]
                enhanced_final_access = {
                    'time': final_access['time'],
                    'accessor_id': final_access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': final_access.get('value', ''),
                    'access_type': final_access.get('access_type', 'quantum_oracle')
                }
                threat = self.quantum_detector._analyze_quantum_threat(token_id, enhanced_final_access)
                if threat:
                    self.quantum_detector.threat_history.append(threat)
            
            detection_time = time.time() - start_time
            total_time += detection_time
            
            # Get detected threats
            detected_threats = self.quantum_detector.get_active_threats()
            
            # Check if Deutsch-Jozsa algorithm was detected
            dj_detected = any('deutsch_jozsa_algorithm' in threat.quantum_indicators 
                             for threat in detected_threats)
            
            if dj_detected:
                correct_detections += 1
            
            # Record test result
            self.test_results['deutsch_jozsa_tests'].append({
                'test_id': i,
                'simulation': {
                    'algorithm': simulation.algorithm.value,
                    'query_count': simulation.query_count,
                    'execution_time': simulation.execution_time
                },
                'detection_result': {
                    'threats_detected': len(detected_threats),
                    'dj_detected': dj_detected,
                    'detection_time': detection_time,
                    'threat_indicators': [threat.quantum_indicators for threat in detected_threats]
                }
            })
        
        accuracy = correct_detections / num_tests
        avg_detection_time = total_time / num_tests
        
        result = {
            'algorithm': 'Deutsch-Jozsa',
            'tests_run': num_tests,
            'correct_detections': correct_detections,
            'accuracy': accuracy,
            'avg_detection_time': avg_detection_time
        }
        
        print(f"Deutsch-Jozsa Algorithm Detection Results:")
        print(f"  Accuracy: {accuracy:.1%} ({correct_detections}/{num_tests})")
        print(f"  Avg Detection Time: {avg_detection_time:.4f}s")
        
        return result
    
    def test_grover_detection(self, num_tests: int = 10) -> Dict:
        """Test detection of Grover's algorithm attacks"""
        print(f"\nTesting Grover's Algorithm Detection ({num_tests} tests)...")
        
        correct_detections = 0
        total_time = 0
        
        for i in range(num_tests):
            # Generate Grover's algorithm attack
            simulation = self.simulator.simulate_grovers_algorithm(search_space_bits=7)
            token_id = f"grover_test_token_{i}"
            
            # Create test token
            test_token = self.quantum_detector.generate_canary_token("test_data")
            # Use the generated token's ID
            token_id = test_token.token_id
            
            # Convert simulation to access pattern
            access_pattern = self.convert_simulation_to_access_pattern(simulation, token_id)
            
            # Test detection
            start_time = time.time()
            
            # Clear previous threats and access history for clean results
            self.quantum_detector.threat_history.clear()
            if token_id in self.quantum_detector.access_monitor:
                self.quantum_detector.access_monitor[token_id].clear()
            
            # Directly inject the simulated access patterns with proper timing and values
            for access in access_pattern:
                # Convert to the format expected by detection algorithms
                enhanced_access = {
                    'time': access['time'],
                    'accessor_id': access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': access.get('value', ''),  # Include the value field for pattern analysis
                    'access_type': access.get('access_type', 'quantum_oracle')
                }
                
                # Add to access monitor directly
                self.quantum_detector.access_monitor[token_id].append(enhanced_access)
            
            # Trigger threat analysis on the final access
            if access_pattern:
                final_access = access_pattern[-1]
                enhanced_final_access = {
                    'time': final_access['time'],
                    'accessor_id': final_access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': final_access.get('value', ''),
                    'access_type': final_access.get('access_type', 'quantum_oracle')
                }
                threat = self.quantum_detector._analyze_quantum_threat(token_id, enhanced_final_access)
                if threat:
                    self.quantum_detector.threat_history.append(threat)
            
            detection_time = time.time() - start_time
            total_time += detection_time
            
            # Get detected threats
            detected_threats = self.quantum_detector.get_active_threats()
            
            # Check if Grover's algorithm was detected
            grover_detected = any('grovers_algorithm' in threat.quantum_indicators 
                                 for threat in detected_threats)
            
            if grover_detected:
                correct_detections += 1
            
            # Record test result
            self.test_results['grover_tests'].append({
                'test_id': i,
                'simulation': {
                    'algorithm': simulation.algorithm.value,
                    'query_count': simulation.query_count,
                    'execution_time': simulation.execution_time
                },
                'detection_result': {
                    'threats_detected': len(detected_threats),
                    'grover_detected': grover_detected,
                    'detection_time': detection_time,
                    'threat_indicators': [threat.quantum_indicators for threat in detected_threats]
                }
            })
        
        accuracy = correct_detections / num_tests
        avg_detection_time = total_time / num_tests
        
        result = {
            'algorithm': 'Grover',
            'tests_run': num_tests,
            'correct_detections': correct_detections,
            'accuracy': accuracy,
            'avg_detection_time': avg_detection_time
        }
        
        print(f"Grover's Algorithm Detection Results:")
        print(f"  Accuracy: {accuracy:.1%} ({correct_detections}/{num_tests})")
        print(f"  Avg Detection Time: {avg_detection_time:.4f}s")
        
        return result
    
    def test_mixed_scenarios(self, num_tests: int = 20) -> Dict:
        """Test detection against mixed quantum and classical attack scenarios"""
        print(f"\nTesting Mixed Attack Scenarios ({num_tests} tests)...")
        
        # Generate mixed scenarios
        scenarios = self.simulator.generate_mixed_attack_scenario(num_tests)
        
        correct_quantum_detections = 0
        correct_classical_rejections = 0
        false_positives = 0
        false_negatives = 0
        total_time = 0
        
        for i, simulation in enumerate(scenarios):
            token_id = f"mixed_test_token_{i}"
            
            # Create test token
            test_token = self.quantum_detector.generate_canary_token("test_data")
            # Use the generated token's ID
            token_id = test_token.token_id
            
            # Convert simulation to access pattern
            access_pattern = self.convert_simulation_to_access_pattern(simulation, token_id)
            
            # Test detection
            start_time = time.time()
            
            # Clear previous threats and access history for clean results
            self.quantum_detector.threat_history.clear()
            if token_id in self.quantum_detector.access_monitor:
                self.quantum_detector.access_monitor[token_id].clear()
            
            # Directly inject the simulated access patterns with proper timing and values
            for access in access_pattern:
                # Convert to the format expected by detection algorithms
                enhanced_access = {
                    'time': access['time'],
                    'accessor_id': access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': access.get('value', ''),  # Include the value field for pattern analysis
                    'access_type': access.get('access_type', 'quantum_oracle')
                }
                
                # Add to access monitor directly
                self.quantum_detector.access_monitor[token_id].append(enhanced_access)
            
            # Trigger threat analysis on the final access
            if access_pattern:
                final_access = access_pattern[-1]
                enhanced_final_access = {
                    'time': final_access['time'],
                    'accessor_id': final_access.get('accessor_id', 'quantum_attacker'),
                    'token_id': token_id,
                    'value': final_access.get('value', ''),
                    'access_type': final_access.get('access_type', 'quantum_oracle')
                }
                threat = self.quantum_detector._analyze_quantum_threat(token_id, enhanced_final_access)
                if threat:
                    self.quantum_detector.threat_history.append(threat)
            
            detection_time = time.time() - start_time
            total_time += detection_time
            
            # Get detected threats
            detected_threats = self.quantum_detector.get_active_threats()
            
            # Determine if this was a quantum attack (low query count indicates quantum)
            is_quantum_attack = simulation.query_count <= 10
            
            # Check detection results
            quantum_detected = len(detected_threats) > 0
            
            if is_quantum_attack and quantum_detected:
                correct_quantum_detections += 1
            elif not is_quantum_attack and not quantum_detected:
                correct_classical_rejections += 1
            elif not is_quantum_attack and quantum_detected:
                false_positives += 1
            elif is_quantum_attack and not quantum_detected:
                false_negatives += 1
            
            # Record test result
            self.test_results['mixed_scenario_tests'].append({
                'test_id': i,
                'simulation': {
                    'algorithm': simulation.algorithm.value,
                    'query_count': simulation.query_count,
                    'is_quantum': is_quantum_attack
                },
                'detection_result': {
                    'quantum_detected': quantum_detected,
                    'threats_detected': len(detected_threats),
                    'detection_time': detection_time
                }
            })
        
        quantum_scenarios = sum(1 for s in scenarios if s.query_count <= 10)
        classical_scenarios = len(scenarios) - quantum_scenarios
        
        quantum_accuracy = correct_quantum_detections / max(quantum_scenarios, 1)
        classical_accuracy = correct_classical_rejections / max(classical_scenarios, 1)
        overall_accuracy = (correct_quantum_detections + correct_classical_rejections) / num_tests
        
        avg_detection_time = total_time / num_tests
        
        result = {
            'tests_run': num_tests,
            'quantum_scenarios': quantum_scenarios,
            'classical_scenarios': classical_scenarios,
            'correct_quantum_detections': correct_quantum_detections,
            'correct_classical_rejections': correct_classical_rejections,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'quantum_accuracy': quantum_accuracy,
            'classical_accuracy': classical_accuracy,
            'overall_accuracy': overall_accuracy,
            'avg_detection_time': avg_detection_time
        }
        
        print(f"Mixed Scenario Detection Results:")
        print(f"  Quantum Detection Accuracy: {quantum_accuracy:.1%} ({correct_quantum_detections}/{quantum_scenarios})")
        print(f"  Classical Rejection Accuracy: {classical_accuracy:.1%} ({correct_classical_rejections}/{classical_scenarios})")
        print(f"  Overall Accuracy: {overall_accuracy:.1%}")
        print(f"  False Positives: {false_positives}")
        print(f"  False Negatives: {false_negatives}")
        print(f"  Avg Detection Time: {avg_detection_time:.4f}s")
        
        return result
    
    def run_comprehensive_tests(self):
        """Run all enhanced detection tests"""
        print("MWRASP Enhanced Quantum Detection Testing")
        print("=" * 60)
        
        # Individual algorithm tests
        simon_results = self.test_simons_algorithm_detection(15)
        bv_results = self.test_bernstein_vazirani_detection(15)
        dj_results = self.test_deutsch_jozsa_detection(15)
        grover_results = self.test_grover_detection(15)
        
        # Mixed scenario test
        mixed_results = self.test_mixed_scenarios(30)
        
        # Calculate overall performance metrics
        total_tests = (simon_results['tests_run'] + bv_results['tests_run'] + 
                      dj_results['tests_run'] + grover_results['tests_run'])
        total_correct = (simon_results['correct_detections'] + 
                        bv_results['correct_detections'] + 
                        dj_results['correct_detections'] + 
                        grover_results['correct_detections'])
        
        overall_accuracy = total_correct / total_tests
        avg_detection_time = np.mean([
            simon_results['avg_detection_time'],
            bv_results['avg_detection_time'], 
            dj_results['avg_detection_time'],
            grover_results['avg_detection_time']
        ])
        
        self.test_results['performance_metrics'] = {
            'overall_accuracy': overall_accuracy,
            'avg_detection_time': avg_detection_time,
            'simon_accuracy': simon_results['accuracy'],
            'bernstein_vazirani_accuracy': bv_results['accuracy'],
            'deutsch_jozsa_accuracy': dj_results['accuracy'],
            'grover_accuracy': grover_results['accuracy'],
            'mixed_scenario_accuracy': mixed_results['overall_accuracy']
        }
        
        # Print summary
        print(f"\n" + "=" * 60)
        print("ENHANCED DETECTION SUMMARY")
        print("=" * 60)
        print(f"Overall Algorithm Detection Accuracy: {overall_accuracy:.1%}")
        print(f"Average Detection Time: {avg_detection_time:.4f}s")
        print(f"Mixed Scenario Accuracy: {mixed_results['overall_accuracy']:.1%}")
        print(f"False Positive Rate: {mixed_results['false_positives']}/{mixed_results['tests_run']} ({mixed_results['false_positives']/mixed_results['tests_run']:.1%})")
        
        print(f"\nIndividual Algorithm Performance:")
        print(f"  Simon's Algorithm: {simon_results['accuracy']:.1%}")
        print(f"  Bernstein-Vazirani: {bv_results['accuracy']:.1%}")
        print(f"  Deutsch-Jozsa: {dj_results['accuracy']:.1%}")
        print(f"  Grover's Algorithm: {grover_results['accuracy']:.1%}")
        
        return self.test_results
    
    def export_results(self, filename: str = 'enhanced_detection_results.json'):
        """Export test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\nTest results exported to {filename}")

def main():
    """Run enhanced quantum detection tests"""
    tester = EnhancedDetectionTester()
    
    try:
        results = tester.run_comprehensive_tests()
        tester.export_results()
        
        # Success criteria check
        performance = results['performance_metrics']
        
        print(f"\n" + "=" * 60)
        print("SUCCESS CRITERIA EVALUATION")
        print("=" * 60)
        
        success_criteria = {
            'Overall Accuracy >85%': performance['overall_accuracy'] >= 0.85,
            'Detection Time <100ms': performance['avg_detection_time'] < 0.1,
            'Simon Detection >80%': performance['simon_accuracy'] >= 0.8,
            'BV Detection >80%': performance['bernstein_vazirani_accuracy'] >= 0.8,
            'DJ Detection >80%': performance['deutsch_jozsa_accuracy'] >= 0.8,
            'Grover Detection >80%': performance['grover_accuracy'] >= 0.8
        }
        
        for criteria, passed in success_criteria.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{criteria}: {status}")
        
        overall_success = all(success_criteria.values())
        print(f"\nOVERALL SUCCESS: {'✓ PASS' if overall_success else '✗ FAIL'}")
        
        if overall_success:
            print("\nAll success criteria met! Enhanced detection ready for integration.")
        else:
            print("\nSome criteria not met. Additional tuning may be required.")
        
        return overall_success
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
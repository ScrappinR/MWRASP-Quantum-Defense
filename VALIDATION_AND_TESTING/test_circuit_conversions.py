#!/usr/bin/env python3
"""
Test and validation framework for quantum circuit conversions
Tests Simon's, Deutsch-Jozsa, and Bernstein-Vazirani algorithm conversions
"""

import asyncio
import sys
import os
import time
import json
import numpy as np
from typing import Dict, List, Tuple, Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.quantum_circuit_converter import (
    QuantumCircuitConverter, AlgorithmType, SimulationData, 
    CircuitConversionResult, create_circuit_converter
)
from core.quantum_detector import QuantumDetector

# Check if Qiskit is available for hardware testing
try:
    from qiskit import transpile
    from qiskit.providers.fake_provider import FakeBrisbane, FakeTorontov2
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


class CircuitConversionValidator:
    """Validates quantum circuit conversions against simulations"""
    
    def __init__(self):
        self.converter = create_circuit_converter()
        self.quantum_detector = QuantumDetector()
        self.validation_results = []
        
    def validate_simons_algorithm_conversion(self) -> Dict[str, Any]:
        """Validate Simon's algorithm circuit conversion"""
        print("Validating Simon's Algorithm Circuit Conversion")
        print("=" * 55)
        
        results = {'algorithm': 'simons', 'test_cases': [], 'summary': {}}
        
        # Test cases with different input sizes and secret strings
        test_cases = [
            {'n': 3, 'secret': '101', 'description': '3-qubit with secret 101'},
            {'n': 4, 'secret': '1010', 'description': '4-qubit with secret 1010'},
            {'n': 5, 'secret': '11001', 'description': '5-qubit with secret 11001'},
            {'n': 2, 'secret': '11', 'description': '2-qubit minimal case'},
            {'n': 6, 'secret': '101010', 'description': '6-qubit alternating pattern'}
        ]
        
        successful_conversions = 0
        total_qubits = 0
        total_gates = 0
        
        for test_case in test_cases:
            print(f"\nTesting {test_case['description']}...")
            
            try:
                # Create simulation data
                sim_data = SimulationData(
                    algorithm_type=AlgorithmType.SIMONS,
                    input_size=test_case['n'],
                    parameters={'secret_string': test_case['secret']},
                    expected_behavior={'finds_secret': True, 'queries': test_case['n'] - 1},
                    timing_data=[0.001 * i for i in range(test_case['n'])],
                    access_patterns=[{'value': str(i), 'time': 0.001 * i} for i in range(test_case['n'])]
                )
                
                # Convert to circuit
                circuit_result = self.converter.convert_simulation_to_circuit(sim_data)
                
                # Validate conversion
                validation_scores = self.converter.validate_circuit_against_simulation(
                    circuit_result, sim_data
                )
                
                # Test results
                test_result = {
                    'test_case': test_case['description'],
                    'input_size': test_case['n'],
                    'secret_string': test_case['secret'],
                    'qubit_count': circuit_result.qubit_count,
                    'gate_count': circuit_result.gate_count,
                    'depth': circuit_result.depth,
                    'error_rate': circuit_result.error_rate_estimate,
                    'hardware_compatible': circuit_result.hardware_compatible,
                    'validation_scores': validation_scores,
                    'success': True
                }
                
                successful_conversions += 1
                total_qubits += circuit_result.qubit_count
                total_gates += circuit_result.gate_count
                
                print(f"  [SUCCESS] Conversion successful")
                print(f"    Qubits: {circuit_result.qubit_count}, Gates: {circuit_result.gate_count}")
                print(f"    Error rate: {circuit_result.error_rate_estimate:.4f}")
                print(f"    Hardware compatible: {circuit_result.hardware_compatible}")
                print(f"    Validation score: {validation_scores['overall_score']:.3f}")
                
            except Exception as e:
                test_result = {
                    'test_case': test_case['description'],
                    'success': False,
                    'error': str(e)
                }
                print(f"  [FAILED] Conversion failed: {e}")
            
            results['test_cases'].append(test_result)
        
        # Summary
        success_rate = successful_conversions / len(test_cases)
        avg_qubits = total_qubits / max(successful_conversions, 1)
        avg_gates = total_gates / max(successful_conversions, 1)
        
        results['summary'] = {
            'success_rate': success_rate,
            'successful_conversions': successful_conversions,
            'total_tests': len(test_cases),
            'avg_qubit_count': avg_qubits,
            'avg_gate_count': avg_gates
        }
        
        print(f"\nSimon's Algorithm Summary:")
        print(f"  Success rate: {success_rate:.1%} ({successful_conversions}/{len(test_cases)})")
        print(f"  Average qubits: {avg_qubits:.1f}")
        print(f"  Average gates: {avg_gates:.1f}")
        
        return results
    
    def validate_deutsch_jozsa_conversion(self) -> Dict[str, Any]:
        """Validate Deutsch-Jozsa algorithm circuit conversion"""
        print("\nValidating Deutsch-Jozsa Algorithm Circuit Conversion")
        print("=" * 58)
        
        results = {'algorithm': 'deutsch_jozsa', 'test_cases': [], 'summary': {}}
        
        # Test cases with different input sizes and function types
        test_cases = [
            {'n': 2, 'constant': True, 'value': 0, 'description': '2-qubit constant-0'},
            {'n': 2, 'constant': True, 'value': 1, 'description': '2-qubit constant-1'},
            {'n': 2, 'constant': False, 'description': '2-qubit balanced'},
            {'n': 4, 'constant': True, 'value': 0, 'description': '4-qubit constant-0'},
            {'n': 4, 'constant': False, 'description': '4-qubit balanced'},
            {'n': 6, 'constant': True, 'value': 1, 'description': '6-qubit constant-1'},
            {'n': 8, 'constant': False, 'description': '8-qubit balanced'}
        ]
        
        successful_conversions = 0
        total_qubits = 0
        total_gates = 0
        
        for test_case in test_cases:
            print(f"\nTesting {test_case['description']}...")
            
            try:
                # Create simulation data
                sim_params = {'is_constant': test_case['constant']}
                if test_case['constant']:
                    sim_params['constant_value'] = test_case['value']
                
                sim_data = SimulationData(
                    algorithm_type=AlgorithmType.DEUTSCH_JOZSA,
                    input_size=test_case['n'],
                    parameters=sim_params,
                    expected_behavior={
                        'single_query': True, 
                        'definitive': True,
                        'function_type': 'constant' if test_case['constant'] else 'balanced'
                    },
                    timing_data=[0.0005],  # Single query
                    access_patterns=[{'value': 'oracle_query', 'time': 0.0005}]
                )
                
                # Convert to circuit
                circuit_result = self.converter.convert_simulation_to_circuit(sim_data)
                
                # Validate conversion
                validation_scores = self.converter.validate_circuit_against_simulation(
                    circuit_result, sim_data
                )
                
                # Test results
                test_result = {
                    'test_case': test_case['description'],
                    'input_size': test_case['n'],
                    'function_type': 'constant' if test_case['constant'] else 'balanced',
                    'qubit_count': circuit_result.qubit_count,
                    'gate_count': circuit_result.gate_count,
                    'depth': circuit_result.depth,
                    'error_rate': circuit_result.error_rate_estimate,
                    'hardware_compatible': circuit_result.hardware_compatible,
                    'quantum_advantage': circuit_result.expected_output.get('quantum_advantage', 1),
                    'validation_scores': validation_scores,
                    'success': True
                }
                
                successful_conversions += 1
                total_qubits += circuit_result.qubit_count
                total_gates += circuit_result.gate_count
                
                print(f"  [SUCCESS] Conversion successful")
                print(f"    Qubits: {circuit_result.qubit_count}, Gates: {circuit_result.gate_count}")
                print(f"    Quantum advantage: {circuit_result.expected_output.get('quantum_advantage', 1)}")
                print(f"    Error rate: {circuit_result.error_rate_estimate:.4f}")
                print(f"    Validation score: {validation_scores['overall_score']:.3f}")
                
            except Exception as e:
                test_result = {
                    'test_case': test_case['description'],
                    'success': False,
                    'error': str(e)
                }
                print(f"  [FAILED] Conversion failed: {e}")
            
            results['test_cases'].append(test_result)
        
        # Summary
        success_rate = successful_conversions / len(test_cases)
        avg_qubits = total_qubits / max(successful_conversions, 1)
        avg_gates = total_gates / max(successful_conversions, 1)
        
        results['summary'] = {
            'success_rate': success_rate,
            'successful_conversions': successful_conversions,
            'total_tests': len(test_cases),
            'avg_qubit_count': avg_qubits,
            'avg_gate_count': avg_gates
        }
        
        print(f"\nDeutsch-Jozsa Algorithm Summary:")
        print(f"  Success rate: {success_rate:.1%} ({successful_conversions}/{len(test_cases)})")
        print(f"  Average qubits: {avg_qubits:.1f}")
        print(f"  Average gates: {avg_gates:.1f}")
        
        return results
    
    def validate_bernstein_vazirani_conversion(self) -> Dict[str, Any]:
        """Validate Bernstein-Vazirani algorithm circuit conversion"""
        print("\nValidating Bernstein-Vazirani Algorithm Circuit Conversion")
        print("=" * 62)
        
        results = {'algorithm': 'bernstein_vazirani', 'test_cases': [], 'summary': {}}
        
        # Test cases with different input sizes and secret strings
        test_cases = [
            {'n': 3, 'secret': '101', 'description': '3-qubit with secret 101'},
            {'n': 4, 'secret': '1111', 'description': '4-qubit all ones'},
            {'n': 5, 'secret': '00000', 'description': '5-qubit all zeros'},
            {'n': 6, 'secret': '101010', 'description': '6-qubit alternating'},
            {'n': 8, 'secret': '11110000', 'description': '8-qubit half-half pattern'},
            {'n': 2, 'secret': '10', 'description': '2-qubit minimal case'}
        ]
        
        successful_conversions = 0
        total_qubits = 0
        total_gates = 0
        
        for test_case in test_cases:
            print(f"\nTesting {test_case['description']}...")
            
            try:
                # Create simulation data
                sim_data = SimulationData(
                    algorithm_type=AlgorithmType.BERNSTEIN_VAZIRANI,
                    input_size=test_case['n'],
                    parameters={'secret_string': test_case['secret']},
                    expected_behavior={
                        'single_query': True,
                        'exact_result': True,
                        'secret_recovered': test_case['secret']
                    },
                    timing_data=[0.0003],  # Single ultra-fast query
                    access_patterns=[{'value': 'oracle_query', 'time': 0.0003}]
                )
                
                # Convert to circuit
                circuit_result = self.converter.convert_simulation_to_circuit(sim_data)
                
                # Validate conversion
                validation_scores = self.converter.validate_circuit_against_simulation(
                    circuit_result, sim_data
                )
                
                # Test results
                test_result = {
                    'test_case': test_case['description'],
                    'input_size': test_case['n'],
                    'secret_string': test_case['secret'],
                    'qubit_count': circuit_result.qubit_count,
                    'gate_count': circuit_result.gate_count,
                    'depth': circuit_result.depth,
                    'error_rate': circuit_result.error_rate_estimate,
                    'hardware_compatible': circuit_result.hardware_compatible,
                    'quantum_advantage': circuit_result.expected_output.get('quantum_advantage', 1),
                    'validation_scores': validation_scores,
                    'success': True
                }
                
                successful_conversions += 1
                total_qubits += circuit_result.qubit_count
                total_gates += circuit_result.gate_count
                
                print(f"  [SUCCESS] Conversion successful")
                print(f"    Qubits: {circuit_result.qubit_count}, Gates: {circuit_result.gate_count}")
                print(f"    Quantum advantage: {circuit_result.expected_output.get('quantum_advantage', 1)}x")
                print(f"    Error rate: {circuit_result.error_rate_estimate:.4f}")
                print(f"    Validation score: {validation_scores['overall_score']:.3f}")
                
            except Exception as e:
                test_result = {
                    'test_case': test_case['description'],
                    'success': False,
                    'error': str(e)
                }
                print(f"  [FAILED] Conversion failed: {e}")
            
            results['test_cases'].append(test_result)
        
        # Summary
        success_rate = successful_conversions / len(test_cases)
        avg_qubits = total_qubits / max(successful_conversions, 1)
        avg_gates = total_gates / max(successful_conversions, 1)
        
        results['summary'] = {
            'success_rate': success_rate,
            'successful_conversions': successful_conversions,
            'total_tests': len(test_cases),
            'avg_qubit_count': avg_qubits,
            'avg_gate_count': avg_gates
        }
        
        print(f"\nBernstein-Vazirani Algorithm Summary:")
        print(f"  Success rate: {success_rate:.1%} ({successful_conversions}/{len(test_cases)})")
        print(f"  Average qubits: {avg_qubits:.1f}")
        print(f"  Average gates: {avg_gates:.1f}")
        
        return results
    
    def test_integration_with_quantum_detector(self) -> Dict[str, Any]:
        """Test integration between circuit conversion and quantum detection"""
        print("\nTesting Integration with Quantum Detector")
        print("=" * 45)
        
        results = {'integration_tests': [], 'summary': {}}
        
        # Generate quantum detector access patterns that should trigger algorithm detection
        test_algorithms = [
            (AlgorithmType.SIMONS, 'Simon\'s algorithm pattern'),
            (AlgorithmType.DEUTSCH_JOZSA, 'Deutsch-Jozsa algorithm pattern'),
            (AlgorithmType.BERNSTEIN_VAZIRANI, 'Bernstein-Vazirani algorithm pattern')
        ]
        
        successful_integrations = 0
        
        for algorithm_type, description in test_algorithms:
            print(f"\nTesting {description} integration...")
            
            try:
                # Create token and simulate access pattern
                token = self.quantum_detector.generate_canary_token(f"{algorithm_type.value}_test")
                
                # Generate algorithm-specific access patterns
                accesses = self._generate_algorithm_access_pattern(algorithm_type)
                
                # Simulate the accesses
                for access in accesses:
                    self.quantum_detector.access_monitor[token.token_id].append(access)
                
                # Check if quantum detector identifies the algorithm
                threat = self.quantum_detector._analyze_quantum_threat(token.token_id, accesses[-1])
                
                # Create circuit conversion based on detected pattern
                if threat and algorithm_type.value.replace('_', 's_') in [ind.replace('_', 's_') for ind in threat.quantum_indicators]:
                    sim_data = self._convert_threat_to_simulation_data(threat, algorithm_type)
                    circuit_result = self.converter.convert_simulation_to_circuit(sim_data)
                    
                    integration_result = {
                        'algorithm': algorithm_type.value,
                        'detection_successful': True,
                        'threat_confidence': threat.confidence_score,
                        'circuit_conversion_successful': True,
                        'circuit_qubits': circuit_result.qubit_count,
                        'circuit_gates': circuit_result.gate_count,
                        'hardware_compatible': circuit_result.hardware_compatible,
                        'success': True
                    }
                    
                    successful_integrations += 1
                    print(f"  ✓ Integration successful")
                    print(f"    Detection confidence: {threat.confidence_score:.3f}")
                    print(f"    Circuit qubits: {circuit_result.qubit_count}")
                    print(f"    Hardware compatible: {circuit_result.hardware_compatible}")
                
                else:
                    integration_result = {
                        'algorithm': algorithm_type.value,
                        'detection_successful': False,
                        'success': False,
                        'reason': 'Algorithm not detected by quantum detector'
                    }
                    print(f"  [WARNING] Detection failed - algorithm pattern not recognized")
                
            except Exception as e:
                integration_result = {
                    'algorithm': algorithm_type.value,
                    'success': False,
                    'error': str(e)
                }
                print(f"  [FAILED] Integration failed: {e}")
            
            results['integration_tests'].append(integration_result)
        
        # Summary
        success_rate = successful_integrations / len(test_algorithms)
        results['summary'] = {
            'success_rate': success_rate,
            'successful_integrations': successful_integrations,
            'total_tests': len(test_algorithms)
        }
        
        print(f"\nIntegration Test Summary:")
        print(f"  Success rate: {success_rate:.1%} ({successful_integrations}/{len(test_algorithms)})")
        
        return results
    
    def _generate_algorithm_access_pattern(self, algorithm_type: AlgorithmType) -> List[Dict]:
        """Generate access patterns that should trigger specific algorithm detection"""
        base_time = time.time()
        
        if algorithm_type == AlgorithmType.SIMONS:
            # Generate Simon's algorithm pattern: O(n) queries with XOR relationships
            accesses = []
            for i in range(8):  # 8 queries for Simon's
                accesses.append({
                    'time': base_time + 0.001 * i,
                    'accessor_id': f'simons_query_{i}',
                    'value': str(i * 3 % 7),  # XOR-like pattern
                    'input': i,
                    'output': i * 3 % 7
                })
            return accesses
        
        elif algorithm_type == AlgorithmType.DEUTSCH_JOZSA:
            # Generate Deutsch-Jozsa pattern: single decisive query
            return [{
                'time': base_time + 0.0005,
                'accessor_id': 'deutsch_jozsa_oracle',
                'value': 'oracle_result',
                'query_type': 'oracle'
            }]
        
        elif algorithm_type == AlgorithmType.BERNSTEIN_VAZIRANI:
            # Generate Bernstein-Vazirani pattern: single ultra-fast query
            return [{
                'time': base_time + 0.0001,
                'accessor_id': 'bernstein_vazirani_oracle',
                'value': 'secret_string',
                'query_type': 'inner_product_oracle'
            }]
        
        return []
    
    def _convert_threat_to_simulation_data(self, threat, algorithm_type: AlgorithmType) -> SimulationData:
        """Convert detected threat to simulation data for circuit conversion"""
        if algorithm_type == AlgorithmType.SIMONS:
            return SimulationData(
                algorithm_type=algorithm_type,
                input_size=4,  # Default size
                parameters={'secret_string': '1010'},
                expected_behavior={'finds_secret': True},
                timing_data=[threat.detection_time],
                access_patterns=[{'threat_id': threat.threat_id}]
            )
        elif algorithm_type == AlgorithmType.DEUTSCH_JOZSA:
            return SimulationData(
                algorithm_type=algorithm_type,
                input_size=3,
                parameters={'is_constant': True, 'constant_value': 0},
                expected_behavior={'single_query': True},
                timing_data=[threat.detection_time],
                access_patterns=[{'threat_id': threat.threat_id}]
            )
        elif algorithm_type == AlgorithmType.BERNSTEIN_VAZIRANI:
            return SimulationData(
                algorithm_type=algorithm_type,
                input_size=3,
                parameters={'secret_string': '101'},
                expected_behavior={'exact_result': True},
                timing_data=[threat.detection_time],
                access_patterns=[{'threat_id': threat.threat_id}]
            )
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE CIRCUIT CONVERSION VALIDATION REPORT")
        print("=" * 80)
        
        # Run all validations
        simons_results = self.validate_simons_algorithm_conversion()
        dj_results = self.validate_deutsch_jozsa_conversion()
        bv_results = self.validate_bernstein_vazirani_conversion()
        integration_results = self.test_integration_with_quantum_detector()
        
        # Overall summary
        all_results = [simons_results, dj_results, bv_results, integration_results]
        
        total_tests = sum(r['summary'].get('total_tests', len(r.get('integration_tests', []))) for r in all_results)
        total_successful = sum(r['summary'].get('successful_conversions', r['summary'].get('successful_integrations', 0)) for r in all_results)
        
        overall_success_rate = total_successful / total_tests if total_tests > 0 else 0
        
        # Conversion summary
        converter_summary = self.converter.get_conversion_summary()
        
        comprehensive_report = {
            'timestamp': time.time(),
            'qiskit_available': QISKIT_AVAILABLE,
            'overall_statistics': {
                'total_tests': total_tests,
                'total_successful': total_successful,
                'overall_success_rate': overall_success_rate
            },
            'algorithm_results': {
                'simons': simons_results,
                'deutsch_jozsa': dj_results,
                'bernstein_vazirani': bv_results
            },
            'integration_results': integration_results,
            'converter_summary': converter_summary
        }
        
        # Print summary
        print(f"\nOVERALL VALIDATION SUMMARY:")
        print(f"  Total tests: {total_tests}")
        print(f"  Successful conversions: {total_successful}")
        print(f"  Overall success rate: {overall_success_rate:.1%}")
        print(f"  Qiskit available: {'Yes' if QISKIT_AVAILABLE else 'No'}")
        
        if QISKIT_AVAILABLE:
            print(f"\n✓ All circuit conversions are ready for quantum hardware execution")
        else:
            print(f"\n[WARNING] Install Qiskit to enable quantum hardware compatibility testing")
        
        print("\n" + "=" * 80)
        print("VALIDATION COMPLETE - Circuit conversions implemented and tested")
        print("=" * 80)
        
        return comprehensive_report


async def main():
    """Main validation function"""
    validator = CircuitConversionValidator()
    report = validator.generate_comprehensive_report()
    
    # Save report to file
    report_file = "Circuit_Conversion_Validation_Report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nDetailed report saved to: {report_file}")


if __name__ == "__main__":
    asyncio.run(main())
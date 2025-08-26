"""
MWRASP Distributed Quantum Sensor Network
Advanced distributed quantum sensor network for comprehensive threat detection
across multiple domains with quantum-enhanced sensing capabilities.
"""

import asyncio
import time
import json
import logging
import hashlib
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict, deque
import networkx as nx
import math
from scipy import signal, stats
from scipy.spatial.distance import euclidean
from scipy.fft import fft, fftfreq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumSensorType(Enum):
    """Types of quantum sensors in the network."""
    QUANTUM_MAGNETOMETER = "QUANTUM_MAGNETOMETER"         # Atomic magnetometer
    QUANTUM_GRAVIMETER = "QUANTUM_GRAVIMETER"             # Cold atom gravimeter
    QUANTUM_ACCELEROMETER = "QUANTUM_ACCELEROMETER"       # Quantum accelerometer
    QUANTUM_GYROSCOPE = "QUANTUM_GYROSCOPE"               # Atomic gyroscope
    QUANTUM_CLOCK = "QUANTUM_CLOCK"                       # Optical atomic clock
    QUANTUM_ELECTRIC_FIELD = "QUANTUM_ELECTRIC_FIELD"     # Electric field sensor
    QUANTUM_RADIATION = "QUANTUM_RADIATION"               # Single photon detector
    QUANTUM_CHEMICAL = "QUANTUM_CHEMICAL"                 # Molecular quantum sensor
    QUANTUM_SEISMIC = "QUANTUM_SEISMIC"                   # Quantum seismometer
    QUANTUM_COMMUNICATION = "QUANTUM_COMMUNICATION"       # Quantum state detector
    QUANTUM_COMPUTING = "QUANTUM_COMPUTING"               # Quantum computation detector
    QUANTUM_ENTANGLEMENT = "QUANTUM_ENTANGLEMENT"         # Entanglement detector


class SensorPlatform(Enum):
    """Sensor deployment platforms."""
    GROUND_STATION = "GROUND_STATION"           # Fixed ground installation
    MOBILE_UNIT = "MOBILE_UNIT"                 # Vehicle-mounted sensor
    AERIAL_PLATFORM = "AERIAL_PLATFORM"         # Drone/aircraft sensor
    SATELLITE = "SATELLITE"                     # Space-based sensor
    MARITIME = "MARITIME"                       # Ship/submarine sensor
    UNDERGROUND = "UNDERGROUND"                 # Buried/cave sensor
    BUILDING = "BUILDING"                       # Building-integrated sensor
    WEARABLE = "WEARABLE"                       # Personnel sensor
    STEALTH = "STEALTH"                         # Covert deployment


class ThreatDomain(Enum):
    """Threat domains monitored by sensors."""
    ELECTROMAGNETIC = "ELECTROMAGNETIC"         # EM signatures
    GRAVITATIONAL = "GRAVITATIONAL"           # Gravitational anomalies
    NUCLEAR = "NUCLEAR"                       # Nuclear/radiological
    SEISMIC = "SEISMIC"                       # Ground vibrations
    QUANTUM_COMPUTING = "QUANTUM_COMPUTING"   # Quantum computer signatures
    QUANTUM_COMMUNICATION = "QUANTUM_COMMUNICATION"  # Quantum comm intercept
    CYBER = "CYBER"                           # Digital/cyber threats
    CHEMICAL = "CHEMICAL"                     # Chemical detection
    BIOLOGICAL = "BIOLOGICAL"                # Biological agents
    SPACE = "SPACE"                           # Space-based threats


@dataclass
class QuantumSensorCalibration:
    """Calibration data for quantum sensors."""
    calibration_timestamp: datetime
    sensitivity: float                        # Minimum detectable signal
    dynamic_range: float                      # Maximum/minimum signal ratio
    noise_floor: float                        # Background noise level
    frequency_response: Dict[float, float]    # Frequency -> response mapping
    temperature_coefficient: float           # Temperature sensitivity
    magnetic_field_sensitivity: float        # Magnetic field interference
    vibration_sensitivity: float            # Mechanical vibration sensitivity
    quantum_efficiency: float               # Quantum detection efficiency
    coherence_time: float                   # Quantum coherence time (ms)
    
    def is_calibration_valid(self, max_age_hours: int = 24) -> bool:
        """Check if calibration is still valid."""
        age = datetime.now() - self.calibration_timestamp
        return age.total_seconds() < (max_age_hours * 3600)
    
    def calculate_measurement_uncertainty(self, signal_level: float, 
                                        environmental_factors: Dict[str, float]) -> float:
        """Calculate measurement uncertainty based on calibration and environment."""
        # Base uncertainty from noise floor
        base_uncertainty = self.noise_floor / signal_level if signal_level > 0 else float('inf')
        
        # Environmental corrections
        temp_variation = environmental_factors.get('temperature_delta', 0.0)
        magnetic_variation = environmental_factors.get('magnetic_field_delta', 0.0)
        vibration_level = environmental_factors.get('vibration_level', 0.0)
        
        temp_uncertainty = abs(temp_variation * self.temperature_coefficient)
        magnetic_uncertainty = abs(magnetic_variation * self.magnetic_field_sensitivity)
        vibration_uncertainty = vibration_level * self.vibration_sensitivity
        
        # Quantum decoherence effects
        quantum_uncertainty = (1.0 - self.quantum_efficiency) * 0.1
        
        # Combined uncertainty (RSS - Root Sum of Squares)
        total_uncertainty = math.sqrt(
            base_uncertainty**2 + 
            temp_uncertainty**2 + 
            magnetic_uncertainty**2 + 
            vibration_uncertainty**2 + 
            quantum_uncertainty**2
        )
        
        return total_uncertainty


@dataclass
class SensorMeasurement:
    """Individual sensor measurement."""
    measurement_id: str
    sensor_id: str
    timestamp: datetime
    measurement_type: str
    value: float
    unit: str
    uncertainty: float
    
    # Quantum-specific properties
    quantum_state: Optional[Dict[str, Any]] = None
    entanglement_correlation: Optional[str] = None
    decoherence_time: Optional[float] = None
    
    # Environmental context
    environmental_conditions: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    confidence_level: float = 0.95
    processing_flags: List[str] = field(default_factory=list)
    raw_data_hash: Optional[str] = None
    
    def calculate_signal_to_noise_ratio(self, background_level: float) -> float:
        """Calculate signal-to-noise ratio."""
        if background_level <= 0 or self.uncertainty <= 0:
            return float('inf')
        
        signal_power = abs(self.value - background_level)**2
        noise_power = self.uncertainty**2
        
        return 10 * math.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
    
    def is_anomalous(self, baseline: float, threshold_sigma: float = 3.0) -> bool:
        """Determine if measurement is anomalous."""
        if self.uncertainty <= 0:
            return False
        
        deviation = abs(self.value - baseline)
        return deviation > (threshold_sigma * self.uncertainty)


@dataclass
class QuantumSensor:
    """Individual quantum sensor in the network."""
    sensor_id: str
    sensor_type: QuantumSensorType
    platform: SensorPlatform
    location: Tuple[float, float, float]  # lat, lon, altitude
    deployment_timestamp: datetime
    
    # Technical specifications
    sensitivity_specs: Dict[str, float]
    operating_frequency_range: Tuple[float, float]  # Hz
    quantum_properties: Dict[str, Any]
    
    # Operational parameters
    sampling_rate: float              # Hz
    duty_cycle: float                # Fraction of time active (0-1)
    power_consumption: float         # Watts
    data_rate: float                # Mbps
    
    # Network connectivity
    communication_protocols: List[str]
    network_latency: float          # Seconds
    bandwidth_allocation: float      # Mbps
    
    # Status and health
    operational_status: str         # "ACTIVE", "STANDBY", "MAINTENANCE", "FAULT"
    health_score: float            # 0-1 overall health
    last_calibration: Optional[QuantumSensorCalibration] = None
    
    # Data storage
    measurement_buffer: deque = field(default_factory=lambda: deque(maxlen=10000))
    
    def __post_init__(self):
        """Initialize sensor after creation."""
        self.measurement_history = deque(maxlen=100000)
        self.anomaly_detections = deque(maxlen=1000)
        self.network_connections = set()
        
        # Initialize quantum state
        self.quantum_coherence_state = {
            'coherence_time': self.quantum_properties.get('coherence_time', 1000.0),  # microseconds
            'entanglement_partners': set(),
            'quantum_error_rate': 0.001,
            'fidelity': 0.99
        }
    
    def take_measurement(self, environmental_conditions: Optional[Dict[str, float]] = None) -> SensorMeasurement:
        """Take a measurement with the sensor."""
        if self.operational_status != "ACTIVE":
            raise ValueError(f"Sensor {self.sensor_id} is not active (status: {self.operational_status})")
        
        if not self.last_calibration or not self.last_calibration.is_calibration_valid():
            logger.warning(f"Sensor {self.sensor_id} calibration is outdated")
        
        # Generate measurement based on sensor type
        measurement_value, measurement_type, unit = self._simulate_measurement()
        
        # Calculate uncertainty
        env_conditions = environmental_conditions or {}
        if self.last_calibration:
            uncertainty = self.last_calibration.calculate_measurement_uncertainty(
                abs(measurement_value), env_conditions
            )
        else:
            uncertainty = abs(measurement_value) * 0.01  # 1% default uncertainty
        
        # Create measurement
        measurement = SensorMeasurement(
            measurement_id=f"{self.sensor_id}_{int(time.time() * 1000000)}",
            sensor_id=self.sensor_id,
            timestamp=datetime.now(),
            measurement_type=measurement_type,
            value=measurement_value,
            unit=unit,
            uncertainty=uncertainty,
            quantum_state=self._get_current_quantum_state(),
            environmental_conditions=env_conditions,
            confidence_level=min(0.99, self.health_score),
            raw_data_hash=hashlib.sha256(str(measurement_value).encode()).hexdigest()[:16]
        )
        
        # Store measurement
        self.measurement_buffer.append(measurement)
        self.measurement_history.append(measurement)
        
        # Update sensor state based on measurement
        self._update_sensor_state(measurement)
        
        return measurement
    
    def _simulate_measurement(self) -> Tuple[float, str, str]:
        """Simulate measurement based on sensor type."""
        base_time = time.time()
        
        if self.sensor_type == QuantumSensorType.QUANTUM_MAGNETOMETER:
            # Simulate magnetic field measurement
            # Earth's magnetic field ~50 μT, with variations
            base_field = 50e-6  # Tesla
            variation = np.random.normal(0, 1e-9)  # nT level variations
            quantum_enhancement = np.random.normal(0, 1e-12)  # pT quantum sensitivity
            
            measurement_value = base_field + variation + quantum_enhancement
            return measurement_value, "magnetic_field", "Tesla"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_GRAVIMETER:
            # Simulate gravitational acceleration
            # Earth's gravity ~9.81 m/s², quantum sensors can detect μGal variations
            base_gravity = 9.81  # m/s²
            tidal_variation = 100e-8 * math.sin(2 * math.pi * base_time / 43200)  # 12-hour tidal
            quantum_sensitivity = np.random.normal(0, 1e-9)  # nGal sensitivity
            
            measurement_value = base_gravity + tidal_variation + quantum_sensitivity
            return measurement_value, "gravitational_acceleration", "m/s²"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_CLOCK:
            # Simulate ultra-precise time measurement
            # Optical clocks can achieve 10^-19 fractional frequency stability
            base_frequency = 429228004229873.0  # Al+ ion transition frequency (Hz)
            quantum_fluctuation = np.random.normal(0, base_frequency * 1e-19)
            
            measurement_value = base_frequency + quantum_fluctuation
            return measurement_value, "atomic_frequency", "Hz"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_RADIATION:
            # Simulate single photon detection
            background_rate = 10.0  # counts/second
            poisson_noise = np.random.poisson(background_rate / self.sampling_rate)
            quantum_efficiency = self.quantum_properties.get('detection_efficiency', 0.9)
            
            detected_photons = poisson_noise * quantum_efficiency
            return detected_photons, "photon_count", "counts"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_ELECTRIC_FIELD:
            # Simulate electric field measurement
            background_field = 100.0  # V/m typical atmospheric field
            variation = np.random.normal(0, 10.0)
            quantum_sensitivity = np.random.normal(0, 0.1)  # Sub-V/m sensitivity
            
            measurement_value = background_field + variation + quantum_sensitivity
            return measurement_value, "electric_field", "V/m"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_SEISMIC:
            # Simulate seismic acceleration
            background_noise = np.random.normal(0, 1e-6)  # μm/s² noise
            quantum_enhancement = np.random.normal(0, 1e-9)  # nm/s² sensitivity
            
            measurement_value = background_noise + quantum_enhancement
            return measurement_value, "seismic_acceleration", "m/s²"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_ENTANGLEMENT:
            # Simulate entanglement detection/measurement
            entanglement_fidelity = 0.95 + np.random.normal(0, 0.02)
            entanglement_fidelity = max(0.0, min(1.0, entanglement_fidelity))
            
            return entanglement_fidelity, "entanglement_fidelity", "dimensionless"
        
        elif self.sensor_type == QuantumSensorType.QUANTUM_COMPUTING:
            # Simulate quantum computing activity detection
            # Detect quantum algorithm signatures in EM/thermal emissions
            base_signature = np.random.exponential(1.0)  # Exponential distribution
            quantum_signature = np.random.gamma(2.0, 0.5)  # Gamma distribution for quantum activity
            
            measurement_value = base_signature + quantum_signature
            return measurement_value, "quantum_activity_signature", "arbitrary_units"
        
        else:
            # Generic measurement
            measurement_value = np.random.normal(0, 1)
            return measurement_value, "generic_measurement", "units"
    
    def _get_current_quantum_state(self) -> Dict[str, Any]:
        """Get current quantum state information."""
        return {
            'coherence_time_remaining': self.quantum_coherence_state['coherence_time'],
            'entanglement_partners': list(self.quantum_coherence_state['entanglement_partners']),
            'quantum_fidelity': self.quantum_coherence_state['fidelity'],
            'decoherence_rate': 1.0 / self.quantum_coherence_state['coherence_time'],
            'quantum_error_rate': self.quantum_coherence_state['quantum_error_rate']
        }
    
    def _update_sensor_state(self, measurement: SensorMeasurement) -> None:
        """Update sensor internal state based on measurement."""
        # Update health score based on measurement quality
        if measurement.uncertainty > 0:
            snr = abs(measurement.value) / measurement.uncertainty
            health_contribution = min(1.0, snr / 100.0)  # Normalize to 0-1
            
            # Exponential moving average
            alpha = 0.1
            self.health_score = (1 - alpha) * self.health_score + alpha * health_contribution
        
        # Update quantum coherence state (simulate decoherence)
        time_delta = 0.001  # Assume ~1ms between measurements
        decoherence_factor = math.exp(-time_delta / (self.quantum_coherence_state['coherence_time'] / 1000))
        self.quantum_coherence_state['fidelity'] *= decoherence_factor
        
        # Refresh quantum state periodically
        if self.quantum_coherence_state['fidelity'] < 0.9:
            self._refresh_quantum_state()
    
    def _refresh_quantum_state(self) -> None:
        """Refresh quantum state (simulate quantum error correction)."""
        self.quantum_coherence_state['fidelity'] = min(0.99, 
            self.quantum_coherence_state['fidelity'] + 0.1)
        self.quantum_coherence_state['quantum_error_rate'] *= 0.9
    
    def calibrate_sensor(self) -> QuantumSensorCalibration:
        """Perform sensor calibration."""
        # Simulate calibration process
        calibration = QuantumSensorCalibration(
            calibration_timestamp=datetime.now(),
            sensitivity=self.sensitivity_specs.get('minimum_detectable_signal', 1e-12),
            dynamic_range=self.sensitivity_specs.get('dynamic_range', 1e6),
            noise_floor=self.sensitivity_specs.get('noise_floor', 1e-15),
            frequency_response={f: 1.0 for f in np.logspace(0, 6, 100)},  # Flat response
            temperature_coefficient=1e-6,  # 1 ppm/°C
            magnetic_field_sensitivity=1e-9,
            vibration_sensitivity=1e-8,
            quantum_efficiency=self.quantum_properties.get('detection_efficiency', 0.95),
            coherence_time=self.quantum_properties.get('coherence_time', 1000.0)
        )
        
        self.last_calibration = calibration
        logger.info(f"Calibrated sensor {self.sensor_id}")
        
        return calibration
    
    def establish_entanglement(self, partner_sensor_id: str) -> bool:
        """Establish quantum entanglement with another sensor."""
        if len(self.quantum_coherence_state['entanglement_partners']) >= 3:  # Max 3 partners
            return False
        
        self.quantum_coherence_state['entanglement_partners'].add(partner_sensor_id)
        self.network_connections.add(partner_sensor_id)
        
        logger.info(f"Established entanglement: {self.sensor_id} <-> {partner_sensor_id}")
        return True
    
    def get_sensor_status(self) -> Dict[str, Any]:
        """Get comprehensive sensor status."""
        recent_measurements = list(self.measurement_buffer)[-10:]
        
        return {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type.value,
            'platform': self.platform.value,
            'location': self.location,
            'operational_status': self.operational_status,
            'health_score': self.health_score,
            'last_measurement': recent_measurements[-1].timestamp if recent_measurements else None,
            'measurement_rate': len(recent_measurements),
            'quantum_state': self._get_current_quantum_state(),
            'calibration_valid': self.last_calibration.is_calibration_valid() if self.last_calibration else False,
            'entanglement_partners': len(self.quantum_coherence_state['entanglement_partners']),
            'network_connections': len(self.network_connections),
            'buffer_utilization': len(self.measurement_buffer) / self.measurement_buffer.maxlen
        }


class SensorNetworkTopology:
    """Manages quantum sensor network topology and connectivity."""
    
    def __init__(self):
        self.network_graph = nx.Graph()
        self.entanglement_graph = nx.Graph()
        self.communication_latencies = {}
        
    def add_sensor_to_network(self, sensor: QuantumSensor) -> None:
        """Add sensor to network topology."""
        self.network_graph.add_node(
            sensor.sensor_id,
            sensor_type=sensor.sensor_type.value,
            platform=sensor.platform.value,
            location=sensor.location,
            operational_status=sensor.operational_status
        )
        
        logger.info(f"Added sensor {sensor.sensor_id} to network topology")
    
    def establish_communication_link(self, sensor1_id: str, sensor2_id: str, 
                                   latency: float, bandwidth: float) -> None:
        """Establish communication link between sensors."""
        if not (self.network_graph.has_node(sensor1_id) and self.network_graph.has_node(sensor2_id)):
            raise ValueError("Both sensors must be in network before establishing link")
        
        self.network_graph.add_edge(
            sensor1_id, sensor2_id,
            latency=latency,
            bandwidth=bandwidth,
            link_type='communication'
        )
        
        self.communication_latencies[(sensor1_id, sensor2_id)] = latency
        self.communication_latencies[(sensor2_id, sensor1_id)] = latency
    
    def establish_entanglement_link(self, sensor1_id: str, sensor2_id: str, 
                                  fidelity: float) -> None:
        """Establish quantum entanglement link between sensors."""
        self.entanglement_graph.add_edge(
            sensor1_id, sensor2_id,
            fidelity=fidelity,
            established_time=datetime.now(),
            link_type='entanglement'
        )
        
        logger.info(f"Established entanglement link: {sensor1_id} <-> {sensor2_id} (fidelity: {fidelity:.3f})")
    
    def calculate_network_metrics(self) -> Dict[str, Any]:
        """Calculate network topology metrics."""
        if len(self.network_graph.nodes()) < 2:
            return {'error': 'insufficient_nodes'}
        
        try:
            # Communication network metrics
            comm_density = nx.density(self.network_graph)
            comm_avg_clustering = nx.average_clustering(self.network_graph)
            
            if nx.is_connected(self.network_graph):
                comm_avg_path_length = nx.average_shortest_path_length(self.network_graph, weight='latency')
                comm_diameter = nx.diameter(self.network_graph)
            else:
                comm_avg_path_length = float('inf')
                comm_diameter = float('inf')
            
            # Entanglement network metrics
            if len(self.entanglement_graph.nodes()) >= 2:
                ent_density = nx.density(self.entanglement_graph)
                ent_avg_clustering = nx.average_clustering(self.entanglement_graph)
                
                if nx.is_connected(self.entanglement_graph):
                    ent_avg_path_length = nx.average_shortest_path_length(self.entanglement_graph)
                else:
                    ent_avg_path_length = float('inf')
            else:
                ent_density = 0.0
                ent_avg_clustering = 0.0
                ent_avg_path_length = float('inf')
            
            # Network resilience
            resilience_score = self._calculate_network_resilience()
            
            return {
                'communication_network': {
                    'nodes': len(self.network_graph.nodes()),
                    'edges': len(self.network_graph.edges()),
                    'density': comm_density,
                    'average_clustering': comm_avg_clustering,
                    'average_path_length': comm_avg_path_length,
                    'diameter': comm_diameter,
                    'connected': nx.is_connected(self.network_graph)
                },
                'entanglement_network': {
                    'nodes': len(self.entanglement_graph.nodes()),
                    'edges': len(self.entanglement_graph.edges()),
                    'density': ent_density,
                    'average_clustering': ent_avg_clustering,
                    'average_path_length': ent_avg_path_length,
                    'connected': nx.is_connected(self.entanglement_graph)
                },
                'network_resilience': resilience_score,
                'total_latency': sum(self.communication_latencies.values()) / len(self.communication_latencies) if self.communication_latencies else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error calculating network metrics: {e}")
            return {'error': str(e)}
    
    def _calculate_network_resilience(self) -> float:
        """Calculate network resilience to node failures."""
        if len(self.network_graph.nodes()) < 3:
            return 0.0
        
        # Test connectivity after removing each node
        connected_after_removal = 0
        total_tests = len(self.network_graph.nodes())
        
        for node in list(self.network_graph.nodes()):
            test_graph = self.network_graph.copy()
            test_graph.remove_node(node)
            
            if len(test_graph.nodes()) > 0 and nx.is_connected(test_graph):
                connected_after_removal += 1
        
        resilience = connected_after_removal / total_tests
        return resilience
    
    def find_optimal_path(self, source_id: str, target_id: str, 
                         metric: str = 'latency') -> Optional[List[str]]:
        """Find optimal path between sensors."""
        try:
            if metric == 'latency':
                path = nx.shortest_path(self.network_graph, source_id, target_id, weight='latency')
            else:
                path = nx.shortest_path(self.network_graph, source_id, target_id)
            
            return path
            
        except nx.NetworkXNoPath:
            return None


class QuantumSensorDataFusion:
    """Data fusion engine for quantum sensor measurements."""
    
    def __init__(self):
        self.fusion_algorithms = {
            'weighted_average': self._weighted_average_fusion,
            'kalman_filter': self._kalman_filter_fusion,
            'bayesian_fusion': self._bayesian_fusion,
            'quantum_consensus': self._quantum_consensus_fusion
        }
        
        self.fusion_history = deque(maxlen=10000)
        
    def fuse_measurements(self, measurements: List[SensorMeasurement], 
                         algorithm: str = 'weighted_average',
                         fusion_parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fuse multiple sensor measurements."""
        if not measurements:
            return {'error': 'no_measurements'}
        
        if algorithm not in self.fusion_algorithms:
            algorithm = 'weighted_average'
        
        # Group measurements by type
        measurement_groups = defaultdict(list)
        for measurement in measurements:
            measurement_groups[measurement.measurement_type].append(measurement)
        
        fusion_results = {}
        
        for measurement_type, group_measurements in measurement_groups.items():
            if len(group_measurements) >= 2:
                fusion_func = self.fusion_algorithms[algorithm]
                fusion_result = fusion_func(group_measurements, fusion_parameters or {})
                fusion_results[measurement_type] = fusion_result
        
        # Store fusion results
        fusion_record = {
            'timestamp': datetime.now(),
            'algorithm': algorithm,
            'input_measurements': len(measurements),
            'fusion_results': fusion_results,
            'measurement_types': list(measurement_groups.keys())
        }
        
        self.fusion_history.append(fusion_record)
        
        return fusion_record
    
    def _weighted_average_fusion(self, measurements: List[SensorMeasurement], 
                               parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Weighted average fusion based on measurement uncertainties."""
        if not measurements:
            return {'error': 'no_measurements'}
        
        # Calculate weights (inverse of uncertainty squared)
        weights = []
        values = []
        
        for measurement in measurements:
            if measurement.uncertainty > 0:
                weight = 1.0 / (measurement.uncertainty ** 2)
                weights.append(weight)
                values.append(measurement.value)
        
        if not weights:
            return {'error': 'no_valid_uncertainties'}
        
        weights = np.array(weights)
        values = np.array(values)
        
        # Weighted average
        fused_value = np.sum(weights * values) / np.sum(weights)
        fused_uncertainty = 1.0 / math.sqrt(np.sum(weights))
        
        # Confidence based on measurement agreement
        residuals = values - fused_value
        chi_squared = np.sum(weights * residuals ** 2)
        degrees_of_freedom = len(measurements) - 1
        
        if degrees_of_freedom > 0:
            p_value = 1 - stats.chi2.cdf(chi_squared, degrees_of_freedom)
            confidence = min(0.99, max(0.5, p_value))
        else:
            confidence = 0.95
        
        return {
            'fused_value': fused_value,
            'fused_uncertainty': fused_uncertainty,
            'confidence': confidence,
            'chi_squared': chi_squared,
            'contributing_sensors': [m.sensor_id for m in measurements],
            'fusion_method': 'weighted_average'
        }
    
    def _kalman_filter_fusion(self, measurements: List[SensorMeasurement], 
                            parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Kalman filter-based measurement fusion."""
        # Simplified 1D Kalman filter
        if not measurements:
            return {'error': 'no_measurements'}
        
        # Sort measurements by timestamp
        sorted_measurements = sorted(measurements, key=lambda m: m.timestamp)
        
        # Initialize state
        initial_measurement = sorted_measurements[0]
        state_estimate = initial_measurement.value
        state_covariance = initial_measurement.uncertainty ** 2
        
        # Process each measurement
        for measurement in sorted_measurements[1:]:
            # Prediction step (assume constant value for simplicity)
            predicted_state = state_estimate
            predicted_covariance = state_covariance + parameters.get('process_noise', 1e-6)
            
            # Update step
            measurement_variance = measurement.uncertainty ** 2
            kalman_gain = predicted_covariance / (predicted_covariance + measurement_variance)
            
            state_estimate = predicted_state + kalman_gain * (measurement.value - predicted_state)
            state_covariance = (1 - kalman_gain) * predicted_covariance
        
        return {
            'fused_value': state_estimate,
            'fused_uncertainty': math.sqrt(state_covariance),
            'confidence': 0.95,
            'kalman_gain': kalman_gain,
            'contributing_sensors': [m.sensor_id for m in measurements],
            'fusion_method': 'kalman_filter'
        }
    
    def _bayesian_fusion(self, measurements: List[SensorMeasurement], 
                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Bayesian measurement fusion."""
        if not measurements:
            return {'error': 'no_measurements'}
        
        # Use first measurement as prior
        prior_mean = measurements[0].value
        prior_precision = 1.0 / (measurements[0].uncertainty ** 2) if measurements[0].uncertainty > 0 else 1.0
        
        # Update with remaining measurements
        posterior_precision = prior_precision
        weighted_sum = prior_precision * prior_mean
        
        for measurement in measurements[1:]:
            if measurement.uncertainty > 0:
                likelihood_precision = 1.0 / (measurement.uncertainty ** 2)
                posterior_precision += likelihood_precision
                weighted_sum += likelihood_precision * measurement.value
        
        posterior_mean = weighted_sum / posterior_precision
        posterior_variance = 1.0 / posterior_precision
        
        return {
            'fused_value': posterior_mean,
            'fused_uncertainty': math.sqrt(posterior_variance),
            'confidence': 0.95,
            'posterior_precision': posterior_precision,
            'contributing_sensors': [m.sensor_id for m in measurements],
            'fusion_method': 'bayesian_fusion'
        }
    
    def _quantum_consensus_fusion(self, measurements: List[SensorMeasurement], 
                                parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Quantum consensus-based fusion using entanglement correlations."""
        if not measurements:
            return {'error': 'no_measurements'}
        
        # Filter measurements with quantum state information
        quantum_measurements = [m for m in measurements if m.quantum_state is not None]
        
        if len(quantum_measurements) < 2:
            # Fall back to weighted average
            return self._weighted_average_fusion(measurements, parameters)
        
        # Calculate quantum correlations
        correlations = []
        values = []
        fidelities = []
        
        for measurement in quantum_measurements:
            quantum_fidelity = measurement.quantum_state.get('quantum_fidelity', 0.9)
            correlations.append(quantum_fidelity)
            values.append(measurement.value)
            fidelities.append(quantum_fidelity)
        
        correlations = np.array(correlations)
        values = np.array(values)
        fidelities = np.array(fidelities)
        
        # Quantum-weighted fusion (higher fidelity = higher weight)
        quantum_weights = fidelities ** 2  # Square to emphasize high fidelity
        quantum_weights /= np.sum(quantum_weights)
        
        fused_value = np.sum(quantum_weights * values)
        
        # Uncertainty based on quantum coherence
        avg_fidelity = np.mean(fidelities)
        quantum_uncertainty = (1 - avg_fidelity) * np.std(values)
        
        # Classical uncertainty component
        classical_uncertainties = np.array([m.uncertainty for m in quantum_measurements])
        classical_uncertainty = np.sqrt(np.sum((quantum_weights * classical_uncertainties) ** 2))
        
        total_uncertainty = math.sqrt(quantum_uncertainty ** 2 + classical_uncertainty ** 2)
        
        return {
            'fused_value': fused_value,
            'fused_uncertainty': total_uncertainty,
            'confidence': avg_fidelity,
            'quantum_fidelity': avg_fidelity,
            'quantum_weights': quantum_weights.tolist(),
            'contributing_sensors': [m.sensor_id for m in quantum_measurements],
            'fusion_method': 'quantum_consensus'
        }


class DistributedQuantumSensorNetwork:
    """Main distributed quantum sensor network management system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        
        # Core components
        self.sensors: Dict[str, QuantumSensor] = {}
        self.network_topology = SensorNetworkTopology()
        self.data_fusion = QuantumSensorDataFusion()
        
        # Data management
        self.measurement_stream: deque = deque(maxlen=1000000)
        self.anomaly_alerts: deque = deque(maxlen=10000)
        self.fusion_results: deque = deque(maxlen=50000)
        
        # Network metrics
        self.network_metrics = {
            'total_sensors': 0,
            'active_sensors': 0,
            'measurements_per_second': 0.0,
            'network_latency': 0.0,
            'data_fusion_rate': 0.0,
            'anomaly_detection_rate': 0.0
        }
        
        # Background processing
        self.processing_tasks = []
        
        logger.info("MWRASP Distributed Quantum Sensor Network initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for sensor network."""
        return {
            'auto_calibration_interval_hours': 12,
            'anomaly_detection_enabled': True,
            'data_fusion_enabled': True,
            'quantum_entanglement_enabled': True,
            'network_optimization_enabled': True,
            'measurement_buffer_size': 100000,
            'fusion_algorithm': 'quantum_consensus',
            'anomaly_threshold_sigma': 3.0,
            'network_redundancy_factor': 2
        }
    
    def deploy_sensor(self, sensor_config: Dict[str, Any]) -> str:
        """Deploy new quantum sensor to network."""
        # Create sensor
        sensor = QuantumSensor(
            sensor_id=sensor_config['sensor_id'],
            sensor_type=QuantumSensorType(sensor_config['sensor_type']),
            platform=SensorPlatform(sensor_config['platform']),
            location=tuple(sensor_config['location']),
            deployment_timestamp=datetime.now(),
            sensitivity_specs=sensor_config.get('sensitivity_specs', {}),
            operating_frequency_range=tuple(sensor_config.get('frequency_range', (0.1, 1e6))),
            quantum_properties=sensor_config.get('quantum_properties', {}),
            sampling_rate=sensor_config.get('sampling_rate', 1000.0),
            duty_cycle=sensor_config.get('duty_cycle', 1.0),
            power_consumption=sensor_config.get('power_consumption', 10.0),
            data_rate=sensor_config.get('data_rate', 1.0),
            communication_protocols=sensor_config.get('protocols', ['TCP/IP']),
            network_latency=sensor_config.get('network_latency', 0.1),
            bandwidth_allocation=sensor_config.get('bandwidth', 10.0),
            operational_status='ACTIVE',
            health_score=1.0
        )
        
        # Initial calibration
        sensor.calibrate_sensor()
        
        # Add to network
        self.sensors[sensor.sensor_id] = sensor
        self.network_topology.add_sensor_to_network(sensor)
        
        # Update metrics
        self.network_metrics['total_sensors'] = len(self.sensors)
        self.network_metrics['active_sensors'] = len([s for s in self.sensors.values() if s.operational_status == 'ACTIVE'])
        
        logger.info(f"Deployed quantum sensor {sensor.sensor_id} at location {sensor.location}")
        
        return sensor.sensor_id
    
    def establish_sensor_connections(self, connection_config: List[Dict[str, Any]]) -> None:
        """Establish connections between sensors."""
        for config in connection_config:
            sensor1_id = config['sensor1_id']
            sensor2_id = config['sensor2_id']
            connection_type = config['type']
            
            if sensor1_id not in self.sensors or sensor2_id not in self.sensors:
                logger.warning(f"Cannot establish connection: sensor not found")
                continue
            
            if connection_type == 'communication':
                latency = config.get('latency', 0.1)
                bandwidth = config.get('bandwidth', 10.0)
                
                self.network_topology.establish_communication_link(
                    sensor1_id, sensor2_id, latency, bandwidth
                )
                
            elif connection_type == 'entanglement':
                fidelity = config.get('fidelity', 0.95)
                
                # Establish quantum entanglement
                sensor1 = self.sensors[sensor1_id]
                sensor2 = self.sensors[sensor2_id]
                
                if (sensor1.establish_entanglement(sensor2_id) and 
                    sensor2.establish_entanglement(sensor1_id)):
                    
                    self.network_topology.establish_entanglement_link(
                        sensor1_id, sensor2_id, fidelity
                    )
    
    async def start_continuous_monitoring(self) -> None:
        """Start continuous sensor monitoring and data processing."""
        # Start background tasks
        self.processing_tasks = [
            asyncio.create_task(self._continuous_measurement_collection()),
            asyncio.create_task(self._continuous_data_fusion()),
            asyncio.create_task(self._continuous_anomaly_detection()),
            asyncio.create_task(self._network_optimization())
        ]
        
        logger.info("Started continuous monitoring with background tasks")
    
    async def _continuous_measurement_collection(self) -> None:
        """Continuously collect measurements from all active sensors."""
        while True:
            try:
                # Collect measurements from all active sensors
                for sensor in self.sensors.values():
                    if sensor.operational_status == 'ACTIVE':
                        try:
                            measurement = sensor.take_measurement()
                            self.measurement_stream.append(measurement)
                            
                        except Exception as e:
                            logger.warning(f"Failed to get measurement from {sensor.sensor_id}: {e}")
                
                # Update measurement rate metric
                self.network_metrics['measurements_per_second'] = len(self.measurement_stream) / max(1, len(self.sensors))
                
                # Wait before next collection cycle
                await asyncio.sleep(1.0 / 10.0)  # 10 Hz collection rate
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in measurement collection: {e}")
                await asyncio.sleep(1.0)
    
    async def _continuous_data_fusion(self) -> None:
        """Continuously fuse sensor data."""
        while True:
            try:
                if self.config.get('data_fusion_enabled', True) and len(self.measurement_stream) >= 2:
                    # Get recent measurements for fusion
                    recent_measurements = list(self.measurement_stream)[-50:]  # Last 50 measurements
                    
                    if len(recent_measurements) >= 2:
                        fusion_result = self.data_fusion.fuse_measurements(
                            recent_measurements,
                            self.config.get('fusion_algorithm', 'quantum_consensus')
                        )
                        
                        self.fusion_results.append(fusion_result)
                
                await asyncio.sleep(2.0)  # Fusion every 2 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in data fusion: {e}")
                await asyncio.sleep(5.0)
    
    async def _continuous_anomaly_detection(self) -> None:
        """Continuously detect anomalies in sensor data."""
        while True:
            try:
                if self.config.get('anomaly_detection_enabled', True):
                    # Check for anomalies in recent measurements
                    recent_measurements = list(self.measurement_stream)[-100:]
                    
                    # Group by measurement type and sensor
                    measurement_groups = defaultdict(list)
                    for measurement in recent_measurements:
                        key = (measurement.sensor_id, measurement.measurement_type)
                        measurement_groups[key].append(measurement)
                    
                    # Detect anomalies within each group
                    for (sensor_id, measurement_type), measurements in measurement_groups.items():
                        if len(measurements) >= 10:  # Need sufficient data
                            anomalies = self._detect_anomalies(measurements)
                            
                            for anomaly in anomalies:
                                self.anomaly_alerts.append({
                                    'timestamp': datetime.now(),
                                    'sensor_id': sensor_id,
                                    'measurement_type': measurement_type,
                                    'anomaly': anomaly,
                                    'severity': self._calculate_anomaly_severity(anomaly)
                                })
                
                await asyncio.sleep(5.0)  # Anomaly detection every 5 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in anomaly detection: {e}")
                await asyncio.sleep(10.0)
    
    def _detect_anomalies(self, measurements: List[SensorMeasurement]) -> List[Dict[str, Any]]:
        """Detect anomalies in measurement sequence."""
        if len(measurements) < 10:
            return []
        
        values = np.array([m.value for m in measurements])
        timestamps = [m.timestamp for m in measurements]
        
        anomalies = []
        
        # Statistical anomaly detection
        mean_value = np.mean(values)
        std_value = np.std(values)
        threshold = self.config.get('anomaly_threshold_sigma', 3.0) * std_value
        
        for i, (measurement, value) in enumerate(zip(measurements, values)):
            if abs(value - mean_value) > threshold:
                anomalies.append({
                    'type': 'statistical_outlier',
                    'measurement_id': measurement.measurement_id,
                    'value': value,
                    'expected_range': (mean_value - threshold, mean_value + threshold),
                    'deviation_sigma': abs(value - mean_value) / std_value if std_value > 0 else 0
                })
        
        # Trend-based anomaly detection
        if len(values) >= 20:
            # Simple trend analysis using linear regression
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Check for sudden trend changes
            window_size = 10
            for i in range(window_size, len(values) - window_size):
                local_slope1, _, _, _, _ = stats.linregress(x[i-window_size:i], values[i-window_size:i])
                local_slope2, _, _, _, _ = stats.linregress(x[i:i+window_size], values[i:i+window_size])
                
                slope_change = abs(local_slope2 - local_slope1)
                if slope_change > 3 * std_err:  # Significant slope change
                    anomalies.append({
                        'type': 'trend_change',
                        'measurement_id': measurements[i].measurement_id,
                        'slope_change': slope_change,
                        'timestamp': timestamps[i]
                    })
        
        return anomalies
    
    def _calculate_anomaly_severity(self, anomaly: Dict[str, Any]) -> str:
        """Calculate severity level of detected anomaly."""
        if anomaly['type'] == 'statistical_outlier':
            deviation = anomaly.get('deviation_sigma', 0)
            if deviation > 5.0:
                return 'CRITICAL'
            elif deviation > 4.0:
                return 'HIGH'
            elif deviation > 3.0:
                return 'MEDIUM'
            else:
                return 'LOW'
        
        elif anomaly['type'] == 'trend_change':
            # Trend changes are generally medium severity
            return 'MEDIUM'
        
        return 'LOW'
    
    async def _network_optimization(self) -> None:
        """Continuously optimize network topology and performance."""
        while True:
            try:
                if self.config.get('network_optimization_enabled', True):
                    # Calculate current network metrics
                    network_metrics = self.network_topology.calculate_network_metrics()
                    
                    # Optimize if needed
                    if 'communication_network' in network_metrics:
                        comm_metrics = network_metrics['communication_network']
                        
                        # Check if network needs optimization
                        if (comm_metrics['density'] < 0.3 or 
                            comm_metrics['average_path_length'] > 5.0):
                            
                            self._optimize_network_connections()
                
                await asyncio.sleep(300.0)  # Optimization every 5 minutes
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in network optimization: {e}")
                await asyncio.sleep(600.0)
    
    def _optimize_network_connections(self) -> None:
        """Optimize network connections for better performance."""
        logger.info("Optimizing network connections")
        
        # Simple optimization: connect sensors that are geographically close
        sensor_list = list(self.sensors.values())
        
        for i, sensor1 in enumerate(sensor_list):
            for sensor2 in sensor_list[i+1:]:
                # Calculate distance
                distance = math.sqrt(
                    (sensor1.location[0] - sensor2.location[0])**2 +
                    (sensor1.location[1] - sensor2.location[1])**2 +
                    (sensor1.location[2] - sensor2.location[2])**2
                )
                
                # If sensors are close and not connected, establish connection
                if (distance < 100.0 and  # Within 100 units
                    not self.network_topology.network_graph.has_edge(sensor1.sensor_id, sensor2.sensor_id)):
                    
                    # Estimate latency based on distance and platform
                    base_latency = distance * 0.001  # 1ms per unit distance
                    platform_latency = 0.1 if sensor1.platform == SensorPlatform.SATELLITE else 0.01
                    total_latency = base_latency + platform_latency
                    
                    try:
                        self.network_topology.establish_communication_link(
                            sensor1.sensor_id, sensor2.sensor_id,
                            total_latency, 10.0  # 10 Mbps default bandwidth
                        )
                    except Exception as e:
                        logger.warning(f"Failed to establish optimized connection: {e}")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status."""
        # Sensor status summary
        sensor_status_summary = {}
        for sensor_id, sensor in self.sensors.items():
            sensor_status_summary[sensor_id] = sensor.get_sensor_status()
        
        # Network topology metrics
        topology_metrics = self.network_topology.calculate_network_metrics()
        
        # Recent fusion results
        recent_fusions = list(self.fusion_results)[-10:]
        
        # Recent anomalies
        recent_anomalies = list(self.anomaly_alerts)[-20:]
        
        # Performance metrics
        self.network_metrics['data_fusion_rate'] = len(self.fusion_results) / max(1, len(self.sensors))
        self.network_metrics['anomaly_detection_rate'] = len(self.anomaly_alerts) / max(1, len(self.measurement_stream))
        
        return {
            'network_status': 'OPERATIONAL',
            'sensor_summary': {
                'total_sensors': len(self.sensors),
                'active_sensors': len([s for s in self.sensors.values() if s.operational_status == 'ACTIVE']),
                'sensor_types': list(set(s.sensor_type.value for s in self.sensors.values())),
                'platforms': list(set(s.platform.value for s in self.sensors.values()))
            },
            'network_metrics': self.network_metrics,
            'topology_metrics': topology_metrics,
            'data_streams': {
                'measurement_stream_size': len(self.measurement_stream),
                'fusion_results_count': len(self.fusion_results),
                'anomaly_alerts_count': len(self.anomaly_alerts)
            },
            'recent_fusions': recent_fusions,
            'recent_anomalies': recent_anomalies,
            'sensor_details': sensor_status_summary
        }
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the sensor network."""
        logger.info("Shutting down distributed quantum sensor network")
        
        # Cancel background tasks
        for task in self.processing_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if self.processing_tasks:
            await asyncio.gather(*self.processing_tasks, return_exceptions=True)
        
        # Set all sensors to standby
        for sensor in self.sensors.values():
            sensor.operational_status = 'STANDBY'
        
        logger.info("Sensor network shutdown complete")


async def main():
    """Main demonstration of distributed quantum sensor network."""
    print("MWRASP Distributed Quantum Sensor Network")
    print("=" * 50)
    
    # Initialize sensor network
    sensor_network = DistributedQuantumSensorNetwork()
    
    # Deploy various quantum sensors
    print("Deploying Quantum Sensors:")
    
    sensor_configs = [
        {
            'sensor_id': 'QS_MAG_001',
            'sensor_type': 'QUANTUM_MAGNETOMETER',
            'platform': 'GROUND_STATION',
            'location': (38.9072, -77.0369, 100.0),  # Washington DC
            'sensitivity_specs': {'minimum_detectable_signal': 1e-15, 'noise_floor': 1e-18},
            'sampling_rate': 1000.0,
            'quantum_properties': {'coherence_time': 1000.0, 'detection_efficiency': 0.95}
        },
        {
            'sensor_id': 'QS_GRAV_002',
            'sensor_type': 'QUANTUM_GRAVIMETER',
            'platform': 'GROUND_STATION',
            'location': (37.4419, -122.1430, 50.0),  # Silicon Valley
            'sensitivity_specs': {'minimum_detectable_signal': 1e-9, 'noise_floor': 1e-12},
            'sampling_rate': 100.0,
            'quantum_properties': {'coherence_time': 5000.0, 'detection_efficiency': 0.9}
        },
        {
            'sensor_id': 'QS_CLK_003',
            'sensor_type': 'QUANTUM_CLOCK',
            'platform': 'SATELLITE',
            'location': (40.7128, -74.0060, 20000000.0),  # NYC, LEO altitude
            'sensitivity_specs': {'minimum_detectable_signal': 1e-19, 'noise_floor': 1e-20},
            'sampling_rate': 1.0,
            'quantum_properties': {'coherence_time': 10000.0, 'detection_efficiency': 0.98}
        },
        {
            'sensor_id': 'QS_RAD_004',
            'sensor_type': 'QUANTUM_RADIATION',
            'platform': 'MOBILE_UNIT',
            'location': (41.8781, -87.6298, 10.0),  # Chicago
            'sensitivity_specs': {'minimum_detectable_signal': 1.0, 'noise_floor': 0.1},
            'sampling_rate': 10000.0,
            'quantum_properties': {'coherence_time': 100.0, 'detection_efficiency': 0.85}
        },
        {
            'sensor_id': 'QS_ENT_005',
            'sensor_type': 'QUANTUM_ENTANGLEMENT',
            'platform': 'GROUND_STATION',
            'location': (42.3601, -71.0589, 25.0),  # Cambridge
            'sensitivity_specs': {'minimum_detectable_signal': 0.01, 'noise_floor': 0.001},
            'sampling_rate': 100.0,
            'quantum_properties': {'coherence_time': 2000.0, 'detection_efficiency': 0.95}
        },
        {
            'sensor_id': 'QS_COMP_006',
            'sensor_type': 'QUANTUM_COMPUTING',
            'platform': 'BUILDING',
            'location': (47.6062, -122.3321, 200.0),  # Seattle
            'sensitivity_specs': {'minimum_detectable_signal': 0.1, 'noise_floor': 0.01},
            'sampling_rate': 1000.0,
            'quantum_properties': {'coherence_time': 500.0, 'detection_efficiency': 0.92}
        }
    ]
    
    for config in sensor_configs:
        sensor_id = sensor_network.deploy_sensor(config)
        print(f"  ✓ Deployed {config['sensor_type']} at {config['platform']}: {sensor_id}")
    
    # Establish network connections
    print("\nEstablishing Network Connections:")
    
    connections = [
        {'sensor1_id': 'QS_MAG_001', 'sensor2_id': 'QS_GRAV_002', 'type': 'communication', 'latency': 0.05, 'bandwidth': 50.0},
        {'sensor1_id': 'QS_GRAV_002', 'sensor2_id': 'QS_CLK_003', 'type': 'communication', 'latency': 0.5, 'bandwidth': 10.0},
        {'sensor1_id': 'QS_MAG_001', 'sensor2_id': 'QS_ENT_005', 'type': 'entanglement', 'fidelity': 0.96},
        {'sensor1_id': 'QS_ENT_005', 'sensor2_id': 'QS_COMP_006', 'type': 'entanglement', 'fidelity': 0.93},
        {'sensor1_id': 'QS_RAD_004', 'sensor2_id': 'QS_COMP_006', 'type': 'communication', 'latency': 0.1, 'bandwidth': 25.0}
    ]
    
    sensor_network.establish_sensor_connections(connections)
    
    for conn in connections:
        print(f"  ✓ {conn['type'].title()} link: {conn['sensor1_id']} <-> {conn['sensor2_id']}")
    
    # Start continuous monitoring
    print("\nStarting Continuous Monitoring...")
    await sensor_network.start_continuous_monitoring()
    
    # Run for demonstration period
    print("Collecting sensor data for 10 seconds...")
    await asyncio.sleep(10.0)
    
    # Get network status
    print("\nQuantum Sensor Network Status:")
    status = sensor_network.get_network_status()
    
    print(f"  Network Status: {status['network_status']}")
    print(f"  Active Sensors: {status['sensor_summary']['active_sensors']}/{status['sensor_summary']['total_sensors']}")
    print(f"  Sensor Types: {', '.join(status['sensor_summary']['sensor_types'])}")
    print(f"  Measurement Rate: {status['network_metrics']['measurements_per_second']:.1f} Hz")
    
    if 'topology_metrics' in status and 'communication_network' in status['topology_metrics']:
        comm_metrics = status['topology_metrics']['communication_network']
        print(f"  Network Density: {comm_metrics['density']:.3f}")
        print(f"  Network Connected: {comm_metrics['connected']}")
        
        if 'entanglement_network' in status['topology_metrics']:
            ent_metrics = status['topology_metrics']['entanglement_network']
            print(f"  Entangled Pairs: {ent_metrics['edges']}")
    
    # Show data fusion results
    if status['recent_fusions']:
        print(f"\nRecent Data Fusion Results ({len(status['recent_fusions'])}):")
        for fusion in status['recent_fusions'][-3:]:
            print(f"  • Algorithm: {fusion['algorithm']}, Types: {', '.join(fusion['measurement_types'])}")
            if fusion['fusion_results']:
                for mtype, result in fusion['fusion_results'].items():
                    if not isinstance(result, dict) or 'error' in result:
                        continue
                    print(f"    {mtype}: {result['fused_value']:.6e} ± {result['fused_uncertainty']:.6e} "
                          f"(confidence: {result['confidence']:.3f})")
    
    # Show anomaly detection results
    if status['recent_anomalies']:
        print(f"\nRecent Anomalies Detected ({len(status['recent_anomalies'])}):")
        for anomaly in status['recent_anomalies'][-5:]:
            print(f"  • {anomaly['sensor_id']}: {anomaly['anomaly']['type']} "
                  f"(severity: {anomaly['severity']})")
    
    # Show individual sensor status
    print(f"\nIndividual Sensor Status:")
    for sensor_id, sensor_status in status['sensor_details'].items():
        print(f"  {sensor_id} ({sensor_status['sensor_type']}):")
        print(f"    Status: {sensor_status['operational_status']}")
        print(f"    Health: {sensor_status['health_score']:.3f}")
        print(f"    Measurement Rate: {sensor_status['measurement_rate']}")
        print(f"    Entanglement Partners: {sensor_status['entanglement_partners']}")
        if sensor_status['quantum_state']:
            print(f"    Quantum Fidelity: {sensor_status['quantum_state']['quantum_fidelity']:.3f}")
    
    # Cleanup
    await sensor_network.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
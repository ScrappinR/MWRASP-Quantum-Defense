"""
Quantum Machine Learning Threat Prediction Engine
Advanced ML-based quantum attack pattern prediction and classification
"""

import time
import hashlib
import secrets
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib


class ThreatCategory(Enum):
    QUANTUM_ALGORITHM_ATTACK = "quantum_algorithm_attack"
    HARDWARE_FINGERPRINT_ATTACK = "hardware_fingerprint_attack"
    ERROR_CORRECTION_ATTACK = "error_correction_attack"
    QUANTUM_KEY_ATTACK = "quantum_key_attack"
    QUANTUM_SUPREMACY_ATTACK = "quantum_supremacy_attack"
    VARIATIONAL_ALGORITHM_ATTACK = "variational_algorithm_attack"
    QUANTUM_WALK_ATTACK = "quantum_walk_attack"
    ADIABATIC_ATTACK = "adiabatic_attack"
    QUANTUM_ML_ATTACK = "quantum_ml_attack"
    HYBRID_QUANTUM_CLASSICAL = "hybrid_quantum_classical"
    UNKNOWN_QUANTUM_THREAT = "unknown_quantum_threat"
    NO_THREAT = "no_threat"


class MLModelType(Enum):
    RANDOM_FOREST = "random_forest"
    NEURAL_NETWORK = "neural_network"
    ISOLATION_FOREST = "isolation_forest"
    ENSEMBLE = "ensemble"
    QUANTUM_LSTM = "quantum_lstm"
    QUANTUM_CNN = "quantum_cnn"


@dataclass
class ThreatPrediction:
    prediction_id: str
    threat_category: ThreatCategory
    confidence_score: float
    probability_distribution: Dict[ThreatCategory, float]
    feature_importance: Dict[str, float]
    prediction_timestamp: float
    model_version: str
    input_features: Dict[str, Any]
    uncertainty_estimate: float
    anomaly_score: float
    
    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Check if prediction has high confidence"""
        return self.confidence_score >= threshold
    
    def get_top_threats(self, n: int = 3) -> List[Tuple[ThreatCategory, float]]:
        """Get top N threat categories by probability"""
        sorted_threats = sorted(
            self.probability_distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_threats[:n]


@dataclass
class MLTrainingData:
    feature_vectors: List[List[float]]
    labels: List[ThreatCategory]
    sample_weights: List[float]
    metadata: List[Dict[str, Any]]
    collection_timestamp: float
    
    def get_feature_matrix(self) -> np.ndarray:
        """Convert feature vectors to numpy array"""
        return np.array(self.feature_vectors)
    
    def get_label_array(self) -> np.ndarray:
        """Convert labels to numpy array"""
        return np.array([label.value for label in self.labels])


@dataclass
class ModelMetrics:
    accuracy: float
    precision: Dict[str, float]
    recall: Dict[str, float]
    f1_score: Dict[str, float]
    confusion_matrix: np.ndarray
    training_time: float
    prediction_time: float
    model_size_mb: float
    cross_validation_scores: List[float]
    feature_importance_ranking: List[Tuple[str, float]]


class QuantumMLThreatPredictor:
    def __init__(self, model_config: Dict[str, Any] = None):
        self.model_config = model_config or self._get_default_config()
        
        # ML Models
        self.models: Dict[MLModelType, Any] = {}
        self.scalers: Dict[MLModelType, StandardScaler] = {}
        self.label_encoders: Dict[MLModelType, LabelEncoder] = {}
        self.model_metrics: Dict[MLModelType, ModelMetrics] = {}
        
        # Training data management
        self.training_data_buffer = deque(maxlen=10000)  # Rolling buffer
        self.feature_extractor = QuantumFeatureExtractor()
        
        # Prediction history
        self.prediction_history: List[ThreatPrediction] = []
        self.threat_statistics: Dict[ThreatCategory, int] = defaultdict(int)
        
        # Model versioning
        self.model_version = "v1.0.0"
        self.last_training_time = 0.0
        
        # Initialize models
        self._initialize_models()
        
        # Quantum-specific feature engineering
        self.quantum_features = QuantumFeatureEngineer()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default ML model configuration"""
        return {
            'random_forest': {
                'n_estimators': 200,
                'max_depth': 15,
                'min_samples_split': 5,
                'random_state': 42,
                'n_jobs': -1
            },
            'neural_network': {
                'hidden_layer_sizes': (256, 128, 64),
                'activation': 'relu',
                'solver': 'adam',
                'alpha': 0.001,
                'max_iter': 500,
                'random_state': 42
            },
            'isolation_forest': {
                'contamination': 0.1,
                'random_state': 42,
                'n_jobs': -1
            },
            'ensemble_weights': {
                'random_forest': 0.4,
                'neural_network': 0.4,
                'isolation_forest': 0.2
            },
            'prediction_threshold': 0.7,
            'retraining_interval': 3600,  # 1 hour
            'max_training_samples': 50000
        }
    
    def _initialize_models(self):
        """Initialize ML models"""
        
        # Random Forest Classifier
        self.models[MLModelType.RANDOM_FOREST] = RandomForestClassifier(
            **self.model_config['random_forest']
        )
        
        # Neural Network Classifier
        self.models[MLModelType.NEURAL_NETWORK] = MLPClassifier(
            **self.model_config['neural_network']
        )
        
        # Isolation Forest (for anomaly detection)
        self.models[MLModelType.ISOLATION_FOREST] = IsolationForest(
            **self.model_config['isolation_forest']
        )
        
        # Initialize scalers and encoders
        for model_type in self.models.keys():
            self.scalers[model_type] = StandardScaler()
            self.label_encoders[model_type] = LabelEncoder()
    
    def extract_quantum_features(
        self,
        access_patterns: List[Dict],
        quantum_indicators: List[str],
        confidence_scores: List[float],
        context_data: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """Extract comprehensive quantum threat features for ML"""
        
        features = {}
        
        # Basic pattern features
        features.update(self._extract_basic_pattern_features(access_patterns))
        
        # Quantum algorithm features
        features.update(self._extract_quantum_algorithm_features(quantum_indicators, confidence_scores))
        
        # Temporal features
        features.update(self._extract_temporal_features(access_patterns))
        
        # Statistical features
        features.update(self._extract_statistical_features(access_patterns))
        
        # Quantum-specific features
        features.update(self._extract_quantum_specific_features(access_patterns, context_data))
        
        # Hardware-specific features
        features.update(self._extract_hardware_features(access_patterns))
        
        # Error correction features
        features.update(self._extract_error_correction_features(access_patterns))
        
        return features
    
    def _extract_basic_pattern_features(self, access_patterns: List[Dict]) -> Dict[str, float]:
        """Extract basic access pattern features"""
        if not access_patterns:
            return {}
        
        features = {
            'pattern_length': float(len(access_patterns)),
            'unique_query_types': float(len(set(p.get('query_type', '') for p in access_patterns))),
            'avg_time_delta': float(np.mean([p.get('time_delta', 0.0) for p in access_patterns])),
            'max_time_delta': float(max(p.get('time_delta', 0.0) for p in access_patterns)),
            'min_time_delta': float(min(p.get('time_delta', 0.0) for p in access_patterns if p.get('time_delta', 0.0) > 0)),
            'total_duration': float(max(p.get('time', 0.0) for p in access_patterns) - min(p.get('time', 0.0) for p in access_patterns)),
            'access_rate': float(len(access_patterns) / max(1.0, max(p.get('time', 0.0) for p in access_patterns) - min(p.get('time', 0.0) for p in access_patterns)))
        }
        
        return features
    
    def _extract_quantum_algorithm_features(self, quantum_indicators: List[str], confidence_scores: List[float]) -> Dict[str, float]:
        """Extract quantum algorithm-specific features"""
        features = {
            'num_quantum_indicators': float(len(quantum_indicators)),
            'avg_confidence_score': float(np.mean(confidence_scores)) if confidence_scores else 0.0,
            'max_confidence_score': float(max(confidence_scores)) if confidence_scores else 0.0,
            'confidence_variance': float(np.var(confidence_scores)) if confidence_scores else 0.0,
            'high_confidence_count': float(sum(1 for c in confidence_scores if c > 0.8)),
        }
        
        # Algorithm-specific indicators
        algorithm_indicators = {
            'has_simons_algorithm': 'simons_algorithm' in quantum_indicators,
            'has_grovers_algorithm': 'grovers_algorithm' in quantum_indicators,
            'has_shors_algorithm': 'shors_algorithm' in quantum_indicators,
            'has_superposition': 'superposition_access' in quantum_indicators,
            'has_entanglement': 'entanglement_correlation' in quantum_indicators,
            'has_speedup': 'quantum_speedup' in quantum_indicators,
        }
        
        for indicator, present in algorithm_indicators.items():
            features[indicator] = float(present)
        
        return features
    
    def _extract_temporal_features(self, access_patterns: List[Dict]) -> Dict[str, float]:
        """Extract temporal pattern features"""
        if not access_patterns:
            return {}
        
        times = [p.get('time', 0.0) for p in access_patterns]
        time_diffs = np.diff(sorted(times))
        
        features = {
            'temporal_regularity': float(1.0 - (np.std(time_diffs) / max(np.mean(time_diffs), 0.001))) if len(time_diffs) > 0 else 0.0,
            'burst_pattern_score': float(sum(1 for diff in time_diffs if diff < 0.001) / len(time_diffs)) if len(time_diffs) > 0 else 0.0,
            'temporal_entropy': float(self._calculate_entropy([int(t * 1000) % 100 for t in times])),
            'time_span_ratio': float((max(times) - min(times)) / len(times)) if len(times) > 1 else 0.0,
        }
        
        return features
    
    def _extract_statistical_features(self, access_patterns: List[Dict]) -> Dict[str, float]:
        """Extract statistical features from access patterns"""
        if not access_patterns:
            return {}
        
        # Extract numerical values
        inputs = [p.get('input', 0) for p in access_patterns if isinstance(p.get('input'), (int, float))]
        outputs = [p.get('output', 0) for p in access_patterns if isinstance(p.get('output'), (int, float))]
        
        features = {}
        
        if inputs:
            features.update({
                'input_mean': float(np.mean(inputs)),
                'input_std': float(np.std(inputs)),
                'input_entropy': float(self._calculate_entropy(inputs)),
                'input_range': float(max(inputs) - min(inputs)),
                'input_unique_ratio': float(len(set(inputs)) / len(inputs)),
            })
        
        if outputs:
            features.update({
                'output_mean': float(np.mean(outputs)),
                'output_std': float(np.std(outputs)),
                'output_entropy': float(self._calculate_entropy(outputs)),
                'output_range': float(max(outputs) - min(outputs)),
                'output_unique_ratio': float(len(set(outputs)) / len(outputs)),
            })
        
        # Correlation features
        if inputs and outputs and len(inputs) == len(outputs):
            features['input_output_correlation'] = float(np.corrcoef(inputs, outputs)[0, 1]) if len(inputs) > 1 else 0.0
        
        return features
    
    def _extract_quantum_specific_features(self, access_patterns: List[Dict], context_data: Dict[str, Any] = None) -> Dict[str, float]:
        """Extract quantum-specific features"""
        features = {}
        
        # Quantum measurement indicators
        measurement_count = sum(1 for p in access_patterns if 'measure' in str(p).lower())
        features['measurement_ratio'] = float(measurement_count / len(access_patterns)) if access_patterns else 0.0
        
        # Superposition indicators
        superposition_count = sum(1 for p in access_patterns if 'superposition' in str(p).lower())
        features['superposition_ratio'] = float(superposition_count / len(access_patterns)) if access_patterns else 0.0
        
        # Entanglement indicators
        entanglement_count = sum(1 for p in access_patterns if 'entangle' in str(p).lower())
        features['entanglement_ratio'] = float(entanglement_count / len(access_patterns)) if access_patterns else 0.0
        
        # Quantum gate complexity
        gate_types = set()
        for p in access_patterns:
            algorithm_step = p.get('algorithm_step', '').lower()
            if any(gate in algorithm_step for gate in ['hadamard', 'cnot', 'rotation', 'pauli']):
                gate_types.add(algorithm_step)
        
        features['gate_type_diversity'] = float(len(gate_types))
        
        # Quantum noise indicators
        if context_data:
            features['quantum_noise_level'] = float(context_data.get('noise_level', 0.0))
            features['decoherence_time'] = float(context_data.get('decoherence_time', 100.0))
            features['gate_fidelity'] = float(context_data.get('gate_fidelity', 0.99))
        
        return features
    
    def _extract_hardware_features(self, access_patterns: List[Dict]) -> Dict[str, float]:
        """Extract quantum hardware-specific features"""
        features = {}
        
        # Hardware type indicators
        hardware_indicators = {
            'superconducting_indicators': sum(1 for p in access_patterns if 'ibm' in str(p).lower() or 'google' in str(p).lower()),
            'trapped_ion_indicators': sum(1 for p in access_patterns if 'ion' in str(p).lower()),
            'photonic_indicators': sum(1 for p in access_patterns if 'photon' in str(p).lower()),
            'annealing_indicators': sum(1 for p in access_patterns if 'anneal' in str(p).lower() or 'dwave' in str(p).lower()),
        }
        
        for indicator, count in hardware_indicators.items():
            features[indicator] = float(count / len(access_patterns)) if access_patterns else 0.0
        
        # Connectivity patterns
        qubit_connections = set()
        for p in access_patterns:
            input_val = p.get('input', 0)
            output_val = p.get('output', 0)
            if isinstance(input_val, int) and isinstance(output_val, int):
                if 0 <= input_val < 100 and 0 <= output_val < 100:
                    qubit_connections.add((min(input_val, output_val), max(input_val, output_val)))
        
        features['qubit_connectivity'] = float(len(qubit_connections))
        
        return features
    
    def _extract_error_correction_features(self, access_patterns: List[Dict]) -> Dict[str, float]:
        """Extract quantum error correction features"""
        features = {}
        
        # Error correction indicators
        stabilizer_count = sum(1 for p in access_patterns if 'stabilizer' in str(p).lower())
        syndrome_count = sum(1 for p in access_patterns if 'syndrome' in str(p).lower())
        correction_count = sum(1 for p in access_patterns if 'correction' in str(p).lower())
        
        features['stabilizer_ratio'] = float(stabilizer_count / len(access_patterns)) if access_patterns else 0.0
        features['syndrome_ratio'] = float(syndrome_count / len(access_patterns)) if access_patterns else 0.0
        features['correction_ratio'] = float(correction_count / len(access_patterns)) if access_patterns else 0.0
        
        # Error rate estimation
        error_indicators = sum(1 for p in access_patterns if 'error' in str(p).lower())
        features['error_indicator_ratio'] = float(error_indicators / len(access_patterns)) if access_patterns else 0.0
        
        return features
    
    def _calculate_entropy(self, values: List[Union[int, float]]) -> float:
        """Calculate Shannon entropy of values"""
        if not values:
            return 0.0
        
        # Create histogram
        unique_values, counts = np.unique(values, return_counts=True)
        probabilities = counts / len(values)
        
        # Calculate entropy
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy
    
    def predict_threat(
        self,
        access_patterns: List[Dict],
        quantum_indicators: List[str],
        confidence_scores: List[float],
        context_data: Dict[str, Any] = None
    ) -> ThreatPrediction:
        """Predict quantum threat using ML models"""
        
        current_time = time.time()
        
        # Extract features
        features = self.extract_quantum_features(
            access_patterns, quantum_indicators, confidence_scores, context_data
        )
        
        # Convert features to array
        feature_vector = self._features_to_vector(features)
        
        # Make predictions with all models
        predictions = {}
        anomaly_scores = {}
        
        for model_type, model in self.models.items():
            if hasattr(model, 'predict_proba') and hasattr(model, 'classes_'):
                # Classification model
                try:
                    # Scale features
                    scaled_features = self.scalers[model_type].transform([feature_vector])
                    probabilities = model.predict_proba(scaled_features)[0]
                    
                    # Create probability distribution
                    prob_dist = {}
                    for i, prob in enumerate(probabilities):
                        threat_category = ThreatCategory(model.classes_[i])
                        prob_dist[threat_category] = float(prob)
                    
                    predictions[model_type] = prob_dist
                    
                except Exception as e:
                    print(f"Prediction error with {model_type}: {e}")
                    # Fallback prediction
                    predictions[model_type] = {ThreatCategory.UNKNOWN_QUANTUM_THREAT: 0.5}
            
            elif model_type == MLModelType.ISOLATION_FOREST:
                # Anomaly detection
                try:
                    scaled_features = self.scalers[model_type].transform([feature_vector])
                    anomaly_score = model.decision_function(scaled_features)[0]
                    anomaly_scores[model_type] = float(anomaly_score)
                except Exception as e:
                    print(f"Anomaly detection error: {e}")
                    anomaly_scores[model_type] = 0.0
        
        # Ensemble prediction
        final_prediction = self._ensemble_prediction(predictions, anomaly_scores)
        
        # Calculate feature importance
        feature_importance = self._calculate_feature_importance(features, final_prediction)
        
        # Create prediction object
        prediction = ThreatPrediction(
            prediction_id=f"pred_{secrets.token_hex(8)}_{int(current_time)}",
            threat_category=final_prediction['threat_category'],
            confidence_score=final_prediction['confidence'],
            probability_distribution=final_prediction['probability_distribution'],
            feature_importance=feature_importance,
            prediction_timestamp=current_time,
            model_version=self.model_version,
            input_features=features,
            uncertainty_estimate=final_prediction['uncertainty'],
            anomaly_score=max(anomaly_scores.values()) if anomaly_scores else 0.0
        )
        
        # Store prediction
        self.prediction_history.append(prediction)
        self.threat_statistics[prediction.threat_category] += 1
        
        # Keep history manageable
        if len(self.prediction_history) > 10000:
            self.prediction_history = self.prediction_history[-5000:]
        
        return prediction
    
    def _features_to_vector(self, features: Dict[str, float]) -> List[float]:
        """Convert feature dictionary to vector"""
        # Define expected feature order for consistency
        expected_features = [
            'pattern_length', 'unique_query_types', 'avg_time_delta', 'max_time_delta',
            'min_time_delta', 'total_duration', 'access_rate', 'num_quantum_indicators',
            'avg_confidence_score', 'max_confidence_score', 'confidence_variance',
            'high_confidence_count', 'has_simons_algorithm', 'has_grovers_algorithm',
            'has_shors_algorithm', 'has_superposition', 'has_entanglement', 'has_speedup',
            'temporal_regularity', 'burst_pattern_score', 'temporal_entropy',
            'time_span_ratio', 'input_mean', 'input_std', 'input_entropy', 'input_range',
            'input_unique_ratio', 'output_mean', 'output_std', 'output_entropy',
            'output_range', 'output_unique_ratio', 'input_output_correlation',
            'measurement_ratio', 'superposition_ratio', 'entanglement_ratio',
            'gate_type_diversity', 'quantum_noise_level', 'decoherence_time',
            'gate_fidelity', 'superconducting_indicators', 'trapped_ion_indicators',
            'photonic_indicators', 'annealing_indicators', 'qubit_connectivity',
            'stabilizer_ratio', 'syndrome_ratio', 'correction_ratio', 'error_indicator_ratio'
        ]
        
        # Create feature vector with default values
        feature_vector = []
        for feature_name in expected_features:
            value = features.get(feature_name, 0.0)
            # Handle NaN and infinite values
            if np.isnan(value) or np.isinf(value):
                value = 0.0
            feature_vector.append(float(value))
        
        return feature_vector
    
    def _ensemble_prediction(
        self,
        predictions: Dict[MLModelType, Dict[ThreatCategory, float]],
        anomaly_scores: Dict[MLModelType, float]
    ) -> Dict[str, Any]:
        """Combine predictions from multiple models"""
        
        if not predictions:
            return {
                'threat_category': ThreatCategory.NO_THREAT,
                'confidence': 0.0,
                'probability_distribution': {ThreatCategory.NO_THREAT: 1.0},
                'uncertainty': 1.0
            }
        
        # Weighted ensemble
        weights = self.model_config.get('ensemble_weights', {})
        combined_probs = defaultdict(float)
        total_weight = 0.0
        
        for model_type, prob_dist in predictions.items():
            model_weight = weights.get(model_type.value, 1.0)
            total_weight += model_weight
            
            for threat_category, prob in prob_dist.items():
                combined_probs[threat_category] += prob * model_weight
        
        # Normalize probabilities
        if total_weight > 0:
            for threat_category in combined_probs:
                combined_probs[threat_category] /= total_weight
        
        # Find highest probability threat
        if combined_probs:
            best_threat = max(combined_probs.items(), key=lambda x: x[1])
            threat_category = best_threat[0]
            confidence = best_threat[1]
        else:
            threat_category = ThreatCategory.NO_THREAT
            confidence = 0.0
        
        # Adjust confidence based on anomaly scores
        if anomaly_scores:
            max_anomaly = max(anomaly_scores.values())
            if max_anomaly < -0.5:  # High anomaly (negative scores indicate outliers)
                # Increase threat confidence for anomalous patterns
                if threat_category != ThreatCategory.NO_THREAT:
                    confidence = min(1.0, confidence * 1.2)
                else:
                    threat_category = ThreatCategory.UNKNOWN_QUANTUM_THREAT
                    confidence = abs(max_anomaly) / 2.0
        
        # Calculate uncertainty (entropy of probability distribution)
        prob_values = list(combined_probs.values())
        if prob_values:
            uncertainty = -sum(p * np.log2(p + 1e-10) for p in prob_values if p > 0)
            uncertainty = uncertainty / np.log2(len(prob_values))  # Normalize
        else:
            uncertainty = 1.0
        
        return {
            'threat_category': threat_category,
            'confidence': float(confidence),
            'probability_distribution': dict(combined_probs),
            'uncertainty': float(uncertainty)
        }
    
    def _calculate_feature_importance(
        self,
        features: Dict[str, float],
        prediction: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate feature importance for prediction explanation"""
        
        # Use Random Forest feature importance if available
        if MLModelType.RANDOM_FOREST in self.models:
            rf_model = self.models[MLModelType.RANDOM_FOREST]
            if hasattr(rf_model, 'feature_importances_'):
                feature_names = list(features.keys())
                importances = rf_model.feature_importances_
                
                # Map to feature names
                feature_importance = {}
                for i, importance in enumerate(importances):
                    if i < len(feature_names):
                        feature_importance[feature_names[i]] = float(importance)
                
                return feature_importance
        
        # Fallback: use simple heuristics
        importance = {}
        for feature_name, value in features.items():
            # Higher values for quantum-specific features get higher importance
            if 'quantum' in feature_name or 'algorithm' in feature_name:
                importance[feature_name] = min(1.0, abs(value) * 2.0)
            else:
                importance[feature_name] = min(1.0, abs(value))
        
        return importance
    
    def add_training_sample(
        self,
        access_patterns: List[Dict],
        quantum_indicators: List[str],
        confidence_scores: List[float],
        ground_truth_label: ThreatCategory,
        context_data: Dict[str, Any] = None,
        sample_weight: float = 1.0
    ):
        """Add a training sample to the buffer"""
        
        # Extract features
        features = self.extract_quantum_features(
            access_patterns, quantum_indicators, confidence_scores, context_data
        )
        
        # Convert to feature vector
        feature_vector = self._features_to_vector(features)
        
        # Add to training buffer
        training_sample = {
            'features': feature_vector,
            'label': ground_truth_label,
            'weight': sample_weight,
            'metadata': {
                'timestamp': time.time(),
                'pattern_length': len(access_patterns),
                'context': context_data or {}
            }
        }
        
        self.training_data_buffer.append(training_sample)
    
    def retrain_models(self, force_retrain: bool = False) -> bool:
        """Retrain ML models with accumulated data"""
        
        current_time = time.time()
        
        # Check if retraining is needed
        if (not force_retrain and 
            current_time - self.last_training_time < self.model_config['retraining_interval']):
            return False
        
        if len(self.training_data_buffer) < 50:  # Need minimum samples
            print("Insufficient training data for retraining")
            return False
        
        print(f"Retraining ML models with {len(self.training_data_buffer)} samples...")
        
        # Prepare training data
        feature_vectors = []
        labels = []
        sample_weights = []
        
        for sample in self.training_data_buffer:
            feature_vectors.append(sample['features'])
            labels.append(sample['label'].value)
            sample_weights.append(sample['weight'])
        
        X = np.array(feature_vectors)
        y = np.array(labels)
        weights = np.array(sample_weights)
        
        # Split data
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
            X, y, weights, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train each model
        training_results = {}
        
        for model_type, model in self.models.items():
            if model_type == MLModelType.ISOLATION_FOREST:
                # Anomaly detection (unsupervised)
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X_train)
                
                model.fit(X_scaled)
                self.scalers[model_type] = scaler
                
                # Evaluate on test set
                X_test_scaled = scaler.transform(X_test)
                anomaly_scores = model.decision_function(X_test_scaled)
                
                training_results[model_type] = {
                    'type': 'anomaly_detection',
                    'mean_anomaly_score': np.mean(anomaly_scores),
                    'std_anomaly_score': np.std(anomaly_scores)
                }
                
            else:
                # Classification models
                try:
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # Fit label encoder
                    label_encoder = LabelEncoder()
                    y_train_encoded = label_encoder.fit_transform(y_train)
                    y_test_encoded = label_encoder.transform(y_test)
                    
                    # Train model
                    start_time = time.time()
                    model.fit(X_train_scaled, y_train_encoded, sample_weight=w_train)
                    training_time = time.time() - start_time
                    
                    # Evaluate
                    start_time = time.time()
                    y_pred = model.predict(X_test_scaled)
                    prediction_time = time.time() - start_time
                    
                    # Calculate metrics
                    accuracy = np.mean(y_pred == y_test_encoded)
                    
                    # Store model artifacts
                    self.scalers[model_type] = scaler
                    self.label_encoders[model_type] = label_encoder
                    
                    training_results[model_type] = {
                        'accuracy': accuracy,
                        'training_time': training_time,
                        'prediction_time': prediction_time,
                        'samples_trained': len(X_train)
                    }
                    
                    print(f"{model_type.value}: Accuracy = {accuracy:.3f}")
                    
                except Exception as e:
                    print(f"Training error for {model_type}: {e}")
                    training_results[model_type] = {'error': str(e)}
        
        self.last_training_time = current_time
        self.model_version = f"v{int(current_time)}"
        
        print(f"Model retraining completed. New version: {self.model_version}")
        return True
    
    def get_ml_statistics(self) -> Dict[str, Any]:
        """Get comprehensive ML prediction statistics"""
        current_time = time.time()
        
        stats = {
            'model_version': self.model_version,
            'last_training_time': self.last_training_time,
            'training_buffer_size': len(self.training_data_buffer),
            'prediction_history_size': len(self.prediction_history),
            'threat_statistics': dict(self.threat_statistics),
            'model_performance': {},
            'recent_predictions': [],
            'prediction_confidence_distribution': {},
            'feature_importance_summary': {},
            'anomaly_detection_stats': {}
        }
        
        # Recent predictions (last 5 minutes)
        recent_predictions = [
            pred for pred in self.prediction_history
            if current_time - pred.prediction_timestamp < 300.0
        ]
        
        stats['recent_predictions'] = [
            {
                'prediction_id': pred.prediction_id,
                'threat_category': pred.threat_category.value,
                'confidence': pred.confidence_score,
                'uncertainty': pred.uncertainty_estimate,
                'anomaly_score': pred.anomaly_score,
                'timestamp': pred.prediction_timestamp
            }
            for pred in recent_predictions[-20:]  # Last 20 predictions
        ]
        
        # Confidence distribution
        if self.prediction_history:
            confidences = [pred.confidence_score for pred in self.prediction_history]
            stats['prediction_confidence_distribution'] = {
                'mean': np.mean(confidences),
                'std': np.std(confidences),
                'min': np.min(confidences),
                'max': np.max(confidences),
                'high_confidence_percentage': sum(1 for c in confidences if c > 0.8) / len(confidences)
            }
        
        # Feature importance summary
        if self.prediction_history:
            # Average feature importance across recent predictions
            all_feature_importance = defaultdict(list)
            for pred in self.prediction_history[-100:]:  # Last 100 predictions
                for feature, importance in pred.feature_importance.items():
                    all_feature_importance[feature].append(importance)
            
            for feature, importance_list in all_feature_importance.items():
                stats['feature_importance_summary'][feature] = {
                    'mean_importance': np.mean(importance_list),
                    'max_importance': np.max(importance_list)
                }
        
        # Anomaly detection statistics
        if self.prediction_history:
            anomaly_scores = [pred.anomaly_score for pred in self.prediction_history if pred.anomaly_score != 0]
            if anomaly_scores:
                stats['anomaly_detection_stats'] = {
                    'mean_anomaly_score': np.mean(anomaly_scores),
                    'std_anomaly_score': np.std(anomaly_scores),
                    'high_anomaly_count': sum(1 for score in anomaly_scores if score < -0.5),
                    'anomaly_detection_rate': len(anomaly_scores) / len(self.prediction_history)
                }
        
        return stats
    
    def save_models(self, model_path: str):
        """Save trained models to disk"""
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'label_encoders': self.label_encoders,
                'model_version': self.model_version,
                'model_config': self.model_config,
                'last_training_time': self.last_training_time
            }
            
            joblib.dump(model_data, model_path)
            print(f"Models saved to {model_path}")
            
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def load_models(self, model_path: str) -> bool:
        """Load trained models from disk"""
        try:
            model_data = joblib.load(model_path)
            
            self.models = model_data['models']
            self.scalers = model_data['scalers']
            self.label_encoders = model_data['label_encoders']
            self.model_version = model_data['model_version']
            self.model_config = model_data['model_config']
            self.last_training_time = model_data['last_training_time']
            
            print(f"Models loaded from {model_path} (version: {self.model_version})")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False


class QuantumFeatureExtractor:
    """Helper class for quantum-specific feature extraction"""
    
    def extract_circuit_features(self, circuit_data: Dict) -> Dict[str, float]:
        """Extract features from quantum circuit representation"""
        # Placeholder for quantum circuit analysis
        return {}
    
    def extract_state_features(self, quantum_state: np.ndarray) -> Dict[str, float]:
        """Extract features from quantum state vectors"""
        # Placeholder for quantum state analysis
        return {}


class QuantumFeatureEngineer:
    """Advanced quantum-specific feature engineering"""
    
    def __init__(self):
        self.quantum_metrics = QuantumMetricsCalculator()
    
    def engineer_quantum_features(self, raw_features: Dict[str, float]) -> Dict[str, float]:
        """Apply quantum-specific feature engineering"""
        engineered_features = raw_features.copy()
        
        # Add derived quantum features
        engineered_features.update(self._create_interaction_features(raw_features))
        engineered_features.update(self._create_polynomial_features(raw_features))
        engineered_features.update(self._create_quantum_invariants(raw_features))
        
        return engineered_features
    
    def _create_interaction_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Create interaction features between quantum properties"""
        interactions = {}
        
        # Quantum coherence interactions
        if 'decoherence_time' in features and 'gate_fidelity' in features:
            interactions['coherence_fidelity_product'] = (
                features['decoherence_time'] * features['gate_fidelity']
            )
        
        # Algorithm complexity interactions
        if 'gate_type_diversity' in features and 'qubit_connectivity' in features:
            interactions['complexity_connectivity_ratio'] = (
                features['gate_type_diversity'] / max(features['qubit_connectivity'], 1.0)
            )
        
        return interactions
    
    def _create_polynomial_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """Create polynomial features for non-linear relationships"""
        polynomial = {}
        
        # Quadratic terms for key quantum metrics
        quantum_keys = ['quantum_noise_level', 'gate_fidelity', 'decoherence_time']
        for key in quantum_keys:
            if key in features:
                polynomial[f'{key}_squared'] = features[key] ** 2
        
        return polynomial
    
    def _create_quantum_invariants(self, features: Dict[str, float]) -> Dict[str, float]:
        """Create quantum mechanics-inspired invariant features"""
        invariants = {}
        
        # Quantum resource trade-offs
        if ('gate_type_diversity' in features and 
            'avg_confidence_score' in features and 
            'temporal_regularity' in features):
            
            # Heisenberg-like uncertainty principle for quantum detection
            invariants['quantum_uncertainty_product'] = (
                (1.0 - features['avg_confidence_score']) * 
                (1.0 - features['temporal_regularity'])
            )
        
        return invariants


class QuantumMetricsCalculator:
    """Calculate quantum-specific metrics"""
    
    def calculate_quantum_volume(self, qubits: int, depth: int, fidelity: float) -> float:
        """Calculate quantum volume metric"""
        return min(qubits, depth) ** 2 * fidelity
    
    def calculate_quantum_advantage(self, classical_time: float, quantum_time: float) -> float:
        """Calculate quantum advantage factor"""
        if quantum_time <= 0:
            return float('inf')
        return classical_time / quantum_time
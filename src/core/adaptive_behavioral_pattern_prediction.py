"""
MWRASP Adaptive Behavioral Pattern Prediction System
Revolutionary behavioral authentication with variable-rate adaptation

This system implements:
- Individual agent variable-rate behavioral authentication
- Circumstantial adaptation (time, geography, job, interactions)
- Zero-out capability with predetermined rollback
- Distributed autonomous code management
- Start-point-only vulnerability window
"""

import hashlib
import hmac
import time
import json
import random
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from datetime import datetime, timedelta
import logging

class AdaptationTrigger(Enum):
    TIME_BASED = "time_based"
    GEOGRAPHY_BASED = "geography_based"
    JOB_BASED = "job_based"
    INTERACTION_BASED = "interaction_based"
    THREAT_LEVEL = "threat_level"
    ERROR_THRESHOLD = "error_threshold"
    COMPROMISE_DETECTED = "compromise_detected"

@dataclass
class BehavioralCode:
    """Individual behavioral authentication code for an agent"""
    agent_id: str
    code_generation: int
    pattern_weights: Dict[str, float]
    adaptation_rate: float
    last_update: float
    circumstances_hash: str
    rollback_point: int
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BehavioralCode':
        return cls(**data)

@dataclass
class CircumstantialContext:
    """Context factors that influence behavioral pattern adaptation"""
    timestamp: float
    geographic_region: str
    job_function: str
    recent_interactions: List[str]
    threat_level: float
    network_conditions: Dict[str, Any]
    system_load: float
    
    def get_context_hash(self) -> str:
        """Generate hash of current context for pattern adaptation"""
        context_str = f"{self.timestamp}:{self.geographic_region}:{self.job_function}:" \
                     f"{':'.join(sorted(self.recent_interactions))}:{self.threat_level}:" \
                     f"{self.network_conditions.get('latency', 0)}:{self.system_load}"
        return hashlib.sha256(context_str.encode()).hexdigest()[:32]

class BehavioralPatternPredictor:
    """
    Revolutionary adaptive behavioral pattern prediction system
    Each agent carries autonomous behavioral authentication codes
    """
    
    def __init__(self, system_start_point: str):
        """Initialize with system-wide start point - the only vulnerable moment"""
        self.system_start_point = system_start_point
        self.system_seed = int(hashlib.sha256(system_start_point.encode()).hexdigest()[:16], 16)
        self.agent_codes: Dict[str, BehavioralCode] = {}
        self.adaptation_history: Dict[str, List[Tuple[float, str]]] = {}
        self.error_thresholds = {
            'minor': 0.15,      # 15% error rate triggers monitoring
            'major': 0.25,      # 25% error rate triggers adaptation
            'critical': 0.40    # 40% error rate triggers zero-out
        }
        self.zero_out_events: List[Tuple[float, str, str]] = []
        self.lock = threading.RLock()
        
        # Base behavioral patterns that agents adapt from
        self.base_patterns = {
            'memory_access': {'sequential': 0.7, 'random': 0.3},
            'processing_rhythm': {'steady': 0.6, 'burst': 0.4},
            'communication_style': {'direct': 0.5, 'indirect': 0.5},
            'decision_timing': {'immediate': 0.4, 'deliberate': 0.6},
            'resource_usage': {'conservative': 0.6, 'aggressive': 0.4}
        }
        
        logging.info(f"Behavioral Pattern Predictor initialized with system start point")
    
    def register_agent(self, agent_id: str, initial_context: CircumstantialContext) -> BehavioralCode:
        """Register new agent with unique behavioral code derived from system start point"""
        with self.lock:
            if agent_id in self.agent_codes:
                return self.agent_codes[agent_id]
            
            # Generate unique agent seed from system start point
            agent_seed_str = f"{self.system_start_point}:{agent_id}:{initial_context.timestamp}"
            agent_seed = int(hashlib.sha256(agent_seed_str.encode()).hexdigest()[:16], 16)
            
            # Create individual adaptation rate for this agent
            random.seed(agent_seed)
            adaptation_rate = 0.1 + random.random() * 0.4  # 0.1 to 0.5 adaptation rate
            
            # Generate initial pattern weights from base patterns
            pattern_weights = {}
            for category, base_weights in self.base_patterns.items():
                pattern_weights[category] = {}
                for pattern, base_weight in base_weights.items():
                    # Vary from base weight by agent's unique characteristics
                    variation = (random.random() - 0.5) * 0.3  # ±15% variation
                    pattern_weights[category][pattern] = max(0.1, min(0.9, base_weight + variation))
            
            # Create behavioral code
            behavioral_code = BehavioralCode(
                agent_id=agent_id,
                code_generation=0,
                pattern_weights=pattern_weights,
                adaptation_rate=adaptation_rate,
                last_update=initial_context.timestamp,
                circumstances_hash=initial_context.get_context_hash(),
                rollback_point=0
            )
            
            self.agent_codes[agent_id] = behavioral_code
            self.adaptation_history[agent_id] = [(initial_context.timestamp, "initial_registration")]
            
            logging.info(f"Agent {agent_id} registered with adaptation rate {adaptation_rate:.3f}")
            return behavioral_code
    
    def adapt_behavioral_pattern(self, agent_id: str, context: CircumstantialContext, 
                               trigger: AdaptationTrigger) -> BehavioralCode:
        """Adapt agent's behavioral pattern based on circumstances"""
        with self.lock:
            if agent_id not in self.agent_codes:
                raise ValueError(f"Agent {agent_id} not registered")
            
            current_code = self.agent_codes[agent_id]
            
            # Check if adaptation is needed based on context change
            context_hash = context.get_context_hash()
            if context_hash == current_code.circumstances_hash and trigger != AdaptationTrigger.ERROR_THRESHOLD:
                return current_code  # No change needed
            
            # Calculate adaptation magnitude based on trigger and agent's rate
            adaptation_magnitude = self._calculate_adaptation_magnitude(current_code, context, trigger)
            
            # Generate new pattern weights
            new_pattern_weights = self._generate_adapted_patterns(
                current_code, context, adaptation_magnitude
            )
            
            # Create new behavioral code
            new_code = BehavioralCode(
                agent_id=agent_id,
                code_generation=current_code.code_generation + 1,
                pattern_weights=new_pattern_weights,
                adaptation_rate=current_code.adaptation_rate,
                last_update=context.timestamp,
                circumstances_hash=context_hash,
                rollback_point=current_code.rollback_point
            )
            
            self.agent_codes[agent_id] = new_code
            self.adaptation_history[agent_id].append((context.timestamp, f"adapted_{trigger.value}"))
            
            logging.info(f"Agent {agent_id} adapted pattern (gen {new_code.code_generation}, "
                        f"trigger: {trigger.value}, magnitude: {adaptation_magnitude:.3f})")
            
            return new_code
    
    def _calculate_adaptation_magnitude(self, code: BehavioralCode, context: CircumstantialContext, 
                                      trigger: AdaptationTrigger) -> float:
        """Calculate how much the pattern should adapt based on circumstances"""
        base_magnitude = code.adaptation_rate
        
        # Adjust based on trigger type
        trigger_multipliers = {
            AdaptationTrigger.TIME_BASED: 0.5,
            AdaptationTrigger.GEOGRAPHY_BASED: 0.8,
            AdaptationTrigger.JOB_BASED: 0.7,
            AdaptationTrigger.INTERACTION_BASED: 0.6,
            AdaptationTrigger.THREAT_LEVEL: context.threat_level * 1.5,
            AdaptationTrigger.ERROR_THRESHOLD: 1.2,
            AdaptationTrigger.COMPROMISE_DETECTED: 2.0
        }
        
        multiplier = trigger_multipliers.get(trigger, 1.0)
        
        # Factor in time since last update
        time_factor = min(2.0, (context.timestamp - code.last_update) / 3600)  # Hours since last update
        
        return min(1.0, base_magnitude * multiplier * time_factor)
    
    def _generate_adapted_patterns(self, code: BehavioralCode, context: CircumstantialContext, 
                                 magnitude: float) -> Dict[str, Dict[str, float]]:
        """Generate new behavioral patterns adapted to current circumstances"""
        adapted_patterns = {}
        
        # Use circumstances to seed adaptation
        context_seed = int(hashlib.sha256(context.get_context_hash().encode()).hexdigest()[:16], 16)
        random.seed(context_seed + code.code_generation)
        
        for category, current_patterns in code.pattern_weights.items():
            adapted_patterns[category] = {}
            
            for pattern, current_weight in current_patterns.items():
                # Apply circumstantial adaptations
                adaptation = self._get_circumstantial_adaptation(
                    category, pattern, context, magnitude
                )
                
                # Calculate new weight
                new_weight = current_weight + adaptation
                new_weight = max(0.1, min(0.9, new_weight))  # Keep within bounds
                
                adapted_patterns[category][pattern] = new_weight
            
            # Normalize weights within category
            category_total = sum(adapted_patterns[category].values())
            if category_total > 0:
                for pattern in adapted_patterns[category]:
                    adapted_patterns[category][pattern] /= category_total
        
        return adapted_patterns
    
    def _get_circumstantial_adaptation(self, category: str, pattern: str, 
                                     context: CircumstantialContext, magnitude: float) -> float:
        """Calculate pattern adaptation based on specific circumstances"""
        adaptation = 0.0
        
        # Time-based adaptations
        hour = datetime.fromtimestamp(context.timestamp).hour
        if category == 'processing_rhythm':
            if 9 <= hour <= 17:  # Business hours - more steady processing
                adaptation += 0.1 if pattern == 'steady' else -0.1
            else:  # Off hours - more burst processing
                adaptation += 0.1 if pattern == 'burst' else -0.1
        
        # Geography-based adaptations
        if context.geographic_region in ['high_latency', 'restricted']:
            if category == 'communication_style':
                adaptation += 0.15 if pattern == 'direct' else -0.15
        
        # Job function adaptations
        if context.job_function == 'security_monitoring':
            if category == 'decision_timing':
                adaptation += 0.2 if pattern == 'immediate' else -0.2
        elif context.job_function == 'data_analysis':
            if category == 'decision_timing':
                adaptation += 0.2 if pattern == 'deliberate' else -0.2
        
        # Threat level adaptations
        if context.threat_level > 0.7:
            if category == 'resource_usage':
                adaptation += 0.25 if pattern == 'aggressive' else -0.25
        
        return adaptation * magnitude
    
    def check_error_threshold(self, agent_id: str, error_rate: float, 
                            context: CircumstantialContext) -> bool:
        """Check if agent's error rate exceeds thresholds and trigger appropriate response"""
        with self.lock:
            if agent_id not in self.agent_codes:
                return False
            
            current_code = self.agent_codes[agent_id]
            
            if error_rate >= self.error_thresholds['critical']:
                # Critical error threshold - trigger zero-out
                self.zero_out_agent(agent_id, context, f"Critical error rate: {error_rate:.3f}")
                return True
            elif error_rate >= self.error_thresholds['major']:
                # Major error threshold - force adaptation
                self.adapt_behavioral_pattern(agent_id, context, AdaptationTrigger.ERROR_THRESHOLD)
                logging.warning(f"Agent {agent_id} adapted due to error rate {error_rate:.3f}")
                return True
            elif error_rate >= self.error_thresholds['minor']:
                # Minor error threshold - log for monitoring
                logging.info(f"Agent {agent_id} error rate {error_rate:.3f} - monitoring")
                
            return False
    
    def zero_out_agent(self, agent_id: str, context: CircumstantialContext, reason: str):
        """Zero-out agent and roll back to predetermined starting point"""
        with self.lock:
            if agent_id not in self.agent_codes:
                return
            
            current_code = self.agent_codes[agent_id]
            
            # Record zero-out event
            self.zero_out_events.append((context.timestamp, agent_id, reason))
            
            # Roll back to predetermined starting point
            rollback_seed_str = f"{self.system_start_point}:{agent_id}:rollback_{current_code.rollback_point}"
            rollback_seed = int(hashlib.sha256(rollback_seed_str.encode()).hexdigest()[:16], 16)
            
            # Generate rollback patterns
            random.seed(rollback_seed)
            rollback_patterns = {}
            for category, base_weights in self.base_patterns.items():
                rollback_patterns[category] = {}
                for pattern, base_weight in base_weights.items():
                    variation = (random.random() - 0.5) * 0.2  # Smaller variation for rollback
                    rollback_patterns[category][pattern] = max(0.1, min(0.9, base_weight + variation))
            
            # Create rollback behavioral code
            rollback_code = BehavioralCode(
                agent_id=agent_id,
                code_generation=0,  # Reset to generation 0
                pattern_weights=rollback_patterns,
                adaptation_rate=current_code.adaptation_rate,
                last_update=context.timestamp,
                circumstances_hash=context.get_context_hash(),
                rollback_point=current_code.rollback_point + 1
            )
            
            self.agent_codes[agent_id] = rollback_code
            self.adaptation_history[agent_id].append((context.timestamp, f"zero_out_{reason}"))
            
            logging.critical(f"Agent {agent_id} zeroed out and rolled back - Reason: {reason}")
    
    def predict_next_behavioral_pattern(self, agent_id: str, future_context: CircumstantialContext) -> Dict[str, float]:
        """
        Predict what an agent's behavioral pattern will be given future context
        This is only possible if you have the system start point
        """
        with self.lock:
            if agent_id not in self.agent_codes:
                raise ValueError(f"Agent {agent_id} not registered")
            
            current_code = self.agent_codes[agent_id]
            
            # Simulate adaptation that would occur
            simulated_magnitude = self._calculate_adaptation_magnitude(
                current_code, future_context, AdaptationTrigger.TIME_BASED
            )
            
            simulated_patterns = self._generate_adapted_patterns(
                current_code, future_context, simulated_magnitude
            )
            
            # Flatten patterns for prediction
            prediction = {}
            for category, patterns in simulated_patterns.items():
                for pattern, weight in patterns.items():
                    prediction[f"{category}_{pattern}"] = weight
            
            return prediction
    
    def authenticate_agent_behavior(self, agent_id: str, observed_behavior: Dict[str, float], 
                                  context: CircumstantialContext, tolerance: float = 0.15) -> Tuple[bool, float]:
        """Authenticate agent based on observed behavior vs expected pattern"""
        with self.lock:
            if agent_id not in self.agent_codes:
                return False, 0.0
            
            current_code = self.agent_codes[agent_id]
            
            # Get expected behavioral pattern
            expected_pattern = {}
            for category, patterns in current_code.pattern_weights.items():
                for pattern, weight in patterns.items():
                    expected_pattern[f"{category}_{pattern}"] = weight
            
            # Calculate similarity between expected and observed
            similarity = self._calculate_behavioral_similarity(expected_pattern, observed_behavior)
            
            # Authentication succeeds if similarity is above tolerance
            authenticated = similarity >= (1.0 - tolerance)
            
            if not authenticated:
                error_rate = 1.0 - similarity
                self.check_error_threshold(agent_id, error_rate, context)
            
            return authenticated, similarity
    
    def _calculate_behavioral_similarity(self, expected: Dict[str, float], 
                                       observed: Dict[str, float]) -> float:
        """Calculate similarity between expected and observed behavioral patterns"""
        common_keys = set(expected.keys()) & set(observed.keys())
        if not common_keys:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(expected[key] * observed[key] for key in common_keys)
        magnitude_expected = sum(expected[key] ** 2 for key in common_keys) ** 0.5
        magnitude_observed = sum(observed[key] ** 2 for key in common_keys) ** 0.5
        
        if magnitude_expected == 0 or magnitude_observed == 0:
            return 0.0
        
        return dot_product / (magnitude_expected * magnitude_observed)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        with self.lock:
            status = {
                'registered_agents': len(self.agent_codes),
                'total_adaptations': sum(len(history) - 1 for history in self.adaptation_history.values()),
                'zero_out_events': len(self.zero_out_events),
                'agent_generations': {
                    agent_id: code.code_generation 
                    for agent_id, code in self.agent_codes.items()
                },
                'recent_zero_outs': [
                    {'timestamp': event[0], 'agent_id': event[1], 'reason': event[2]}
                    for event in self.zero_out_events[-10:]
                ],
                'system_vulnerability_window': 'start_point_only'
            }
            
            return status
    
    def export_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Export agent's complete behavioral state for backup/migration"""
        with self.lock:
            if agent_id not in self.agent_codes:
                return None
            
            return {
                'behavioral_code': self.agent_codes[agent_id].to_dict(),
                'adaptation_history': self.adaptation_history.get(agent_id, []),
                'system_start_point_hash': hashlib.sha256(self.system_start_point.encode()).hexdigest()
            }

# Example usage and demonstration
if __name__ == "__main__":
    # Initialize system with start point (the only vulnerable moment)
    system_start_point = "MWRASP_QUANTUM_BEHAVIORAL_GENESIS_2025_09_05_15_30_00"
    predictor = BehavioralPatternPredictor(system_start_point)
    
    # Register agents
    context1 = CircumstantialContext(
        timestamp=time.time(),
        geographic_region="us_east",
        job_function="security_monitoring",
        recent_interactions=["agent_002", "agent_003"],
        threat_level=0.3,
        network_conditions={"latency": 50, "bandwidth": 1000},
        system_load=0.4
    )
    
    agent_code = predictor.register_agent("agent_001", context1)
    print(f"Registered Agent 001 with adaptation rate: {agent_code.adaptation_rate:.3f}")
    
    # Simulate behavioral adaptation based on changing circumstances
    time.sleep(1)
    context2 = CircumstantialContext(
        timestamp=time.time(),
        geographic_region="eu_west",  # Geography changed
        job_function="security_monitoring",
        recent_interactions=["agent_004", "agent_005", "agent_006"],  # More interactions
        threat_level=0.8,  # Higher threat
        network_conditions={"latency": 150, "bandwidth": 500},
        system_load=0.7
    )
    
    adapted_code = predictor.adapt_behavioral_pattern("agent_001", context2, AdaptationTrigger.THREAT_LEVEL)
    print(f"Agent 001 adapted to generation {adapted_code.code_generation}")
    
    # Demonstrate prediction capability (only possible with system start point)
    future_context = CircumstantialContext(
        timestamp=time.time() + 3600,  # One hour in future
        geographic_region="asia_pacific",
        job_function="data_analysis",
        recent_interactions=["agent_007"],
        threat_level=0.2,
        network_conditions={"latency": 200, "bandwidth": 300},
        system_load=0.5
    )
    
    prediction = predictor.predict_next_behavioral_pattern("agent_001", future_context)
    print(f"Predicted behavioral pattern: {prediction}")
    
    # Simulate error threshold breach and zero-out
    predictor.zero_out_agent("agent_001", context2, "Simulated compromise detection")
    
    # Show system status
    status = predictor.get_system_status()
    print(f"System Status: {status}")
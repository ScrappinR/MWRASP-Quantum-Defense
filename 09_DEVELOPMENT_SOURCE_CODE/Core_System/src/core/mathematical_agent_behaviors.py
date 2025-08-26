"""
MWRASP Mathematical Agent Behavior Models
Sophisticated mathematical models for realistic AI agent behaviors in intelligence operations.
Includes personality matrices, decision trees, behavioral patterns, and social dynamics.
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
from scipy import stats, optimize
from scipy.spatial.distance import euclidean, cosine
from scipy.special import softmax

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonalityTrait(Enum):
    """Core personality traits with mathematical representations."""
    RISK_TOLERANCE = "risk_tolerance"          # 0-1 willingness to take risks
    ANALYTICAL_DEPTH = "analytical_depth"      # 0-1 thoroughness of analysis
    SOCIAL_ORIENTATION = "social_orientation"  # 0-1 preference for collaboration
    STRESS_RESILIENCE = "stress_resilience"    # 0-1 performance under pressure
    INNOVATION_DRIVE = "innovation_drive"      # 0-1 preference for novel approaches
    AUTHORITY_RESPECT = "authority_respect"    # 0-1 deference to hierarchy
    INFORMATION_SHARING = "information_sharing" # 0-1 willingness to share intelligence
    OPERATIONAL_TEMPO = "operational_tempo"    # 0-1 preferred activity level
    SECURITY_CONSCIOUSNESS = "security_consciousness" # 0-1 focus on security protocols
    DECISION_SPEED = "decision_speed"          # 0-1 speed of decision making


class CognitiveStyle(Enum):
    """Cognitive processing styles."""
    INTUITIVE = "INTUITIVE"      # Fast, pattern-based decisions
    ANALYTICAL = "ANALYTICAL"    # Systematic, data-driven decisions
    PRAGMATIC = "PRAGMATIC"      # Practical, experience-based decisions
    CREATIVE = "CREATIVE"        # Novel, innovative approaches
    METHODICAL = "METHODICAL"    # Step-by-step, procedural approach


class EmotionalState(Enum):
    """Emotional states affecting agent behavior."""
    CALM = "CALM"
    FOCUSED = "FOCUSED"
    STRESSED = "STRESSED"
    EXCITED = "EXCITED"
    SUSPICIOUS = "SUSPICIOUS"
    CONFIDENT = "CONFIDENT"
    ANXIOUS = "ANXIOUS"
    DETERMINED = "DETERMINED"


@dataclass
class PersonalityMatrix:
    """Mathematical personality matrix for agent behavior."""
    traits: Dict[PersonalityTrait, float]  # 0-1 values for each trait
    cognitive_style: CognitiveStyle
    base_emotional_state: EmotionalState
    personality_stability: float  # 0-1 how much personality changes over time
    adaptation_rate: float       # 0-1 how quickly agent adapts to new situations
    
    # Behavioral parameters
    decision_confidence_threshold: float  # Minimum confidence to act
    collaboration_preference_matrix: np.ndarray  # Preferences for working with others
    stress_response_curve: Callable[[float], float]  # Stress -> performance function
    learning_rate: float  # How quickly agent updates beliefs
    
    def __post_init__(self):
        # Initialize collaboration preference matrix (empty initially)
        self.collaboration_preference_matrix = np.array([])
        
        # Default stress response curve (inverted U-curve)
        if not hasattr(self, 'stress_response_curve'):
            self.stress_response_curve = lambda stress: 1.0 - abs(stress - 0.4) * 2.5 if stress <= 0.8 else 0.1
    
    def calculate_trait_interaction(self, trait1: PersonalityTrait, trait2: PersonalityTrait) -> float:
        """Calculate interaction effect between two personality traits."""
        value1 = self.traits.get(trait1, 0.5)
        value2 = self.traits.get(trait2, 0.5)
        
        # Define trait interactions
        trait_synergies = {
            (PersonalityTrait.ANALYTICAL_DEPTH, PersonalityTrait.DECISION_SPEED): -0.3,  # Negative correlation
            (PersonalityTrait.RISK_TOLERANCE, PersonalityTrait.SECURITY_CONSCIOUSNESS): -0.4,
            (PersonalityTrait.SOCIAL_ORIENTATION, PersonalityTrait.INFORMATION_SHARING): 0.5,
            (PersonalityTrait.STRESS_RESILIENCE, PersonalityTrait.OPERATIONAL_TEMPO): 0.3,
            (PersonalityTrait.INNOVATION_DRIVE, PersonalityTrait.AUTHORITY_RESPECT): -0.2
        }
        
        # Check both directions
        synergy = trait_synergies.get((trait1, trait2), trait_synergies.get((trait2, trait1), 0.0))
        
        # Calculate interaction effect
        base_interaction = value1 * value2
        adjusted_interaction = base_interaction * (1.0 + synergy)
        
        return max(0.0, min(1.0, adjusted_interaction))
    
    def get_effective_trait_value(self, trait: PersonalityTrait, context: Dict[str, Any]) -> float:
        """Get context-adjusted trait value."""
        base_value = self.traits.get(trait, 0.5)
        
        # Context adjustments
        stress_level = context.get('stress_level', 0.3)
        time_pressure = context.get('time_pressure', 0.3)
        social_context = context.get('social_context', 0.5)
        
        # Stress effects on different traits
        stress_effects = {
            PersonalityTrait.DECISION_SPEED: 0.3,     # Stress increases decision speed
            PersonalityTrait.RISK_TOLERANCE: -0.2,   # Stress decreases risk tolerance
            PersonalityTrait.ANALYTICAL_DEPTH: -0.1, # Stress reduces analytical depth
            PersonalityTrait.SOCIAL_ORIENTATION: -0.1 # Stress reduces social orientation
        }
        
        stress_adjustment = stress_effects.get(trait, 0.0) * stress_level
        
        # Time pressure effects
        if trait == PersonalityTrait.DECISION_SPEED:
            time_adjustment = time_pressure * 0.2
        else:
            time_adjustment = 0.0
        
        # Social context effects
        if trait == PersonalityTrait.INFORMATION_SHARING:
            social_adjustment = social_context * 0.1
        else:
            social_adjustment = 0.0
        
        # Apply adjustments
        adjusted_value = base_value + stress_adjustment + time_adjustment + social_adjustment
        
        return max(0.0, min(1.0, adjusted_value))


@dataclass
class BehaviorContext:
    """Context information affecting agent behavior."""
    timestamp: datetime
    operational_phase: str  # "planning", "execution", "analysis", "crisis"
    threat_level: float     # 0-1 current threat assessment
    time_pressure: float    # 0-1 urgency of situation
    social_setting: str     # "individual", "small_group", "large_group", "formal_meeting"
    information_availability: float  # 0-1 how much information is available
    resource_constraints: float     # 0-1 level of resource limitations
    stakeholder_pressure: float     # 0-1 pressure from leadership/external parties
    recent_success_rate: float      # 0-1 recent operational success rate
    collaborative_opportunities: List[str]  # Available collaboration partners


@dataclass
class DecisionNode:
    """Node in agent decision tree."""
    node_id: str
    condition: Callable[[Dict[str, Any]], bool]  # Function to evaluate condition
    confidence_required: float  # Minimum confidence to proceed
    personality_weight: Dict[PersonalityTrait, float]  # Trait weights for this decision
    children: List['DecisionNode'] = field(default_factory=list)
    action: Optional[Callable[[Dict[str, Any]], Any]] = None  # Action if leaf node
    
    def evaluate(self, context: Dict[str, Any], personality: PersonalityMatrix) -> Tuple[bool, float]:
        """Evaluate decision node."""
        # Check condition
        if not self.condition(context):
            return False, 0.0
        
        # Calculate confidence based on personality alignment
        confidence = 0.0
        total_weight = sum(self.personality_weight.values()) if self.personality_weight else 1.0
        
        for trait, weight in self.personality_weight.items():
            trait_value = personality.get_effective_trait_value(trait, context)
            confidence += (trait_value * weight)
        
        confidence = confidence / total_weight if total_weight > 0 else 0.5
        
        # Check if confidence meets threshold
        meets_threshold = confidence >= self.confidence_required
        
        return meets_threshold, confidence


class MathematicalAgentBehavior:
    """Mathematical model for AI agent behavior."""
    
    def __init__(self, agent_id: str, personality: PersonalityMatrix, 
                 initial_knowledge: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.personality = personality
        self.knowledge_base = initial_knowledge or {}
        
        # Behavioral state
        self.current_emotional_state = personality.base_emotional_state
        self.stress_level = 0.3  # Base stress level
        self.confidence_level = 0.7  # Base confidence
        self.energy_level = 0.8  # Mental/physical energy
        
        # Learning and adaptation
        self.experience_history = deque(maxlen=10000)
        self.success_patterns = defaultdict(float)
        self.failure_patterns = defaultdict(float)
        self.belief_updates = deque(maxlen=1000)
        
        # Social dynamics
        self.relationship_matrix: Dict[str, float] = {}  # agent_id -> trust level
        self.communication_patterns: Dict[str, List[datetime]] = defaultdict(list)
        self.collaboration_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Decision-making
        self.decision_tree = self._initialize_decision_tree()
        self.decision_history = deque(maxlen=1000)
        
        # Behavioral patterns
        self.daily_activity_pattern = self._generate_activity_pattern()
        self.communication_style_parameters = self._initialize_communication_style()
        
        logger.info(f"Initialized mathematical behavior model for agent {agent_id}")
    
    def _initialize_decision_tree(self) -> DecisionNode:
        """Initialize agent's decision-making tree."""
        # Root decision: Assess situation
        root = DecisionNode(
            node_id="assess_situation",
            condition=lambda ctx: True,  # Always assess
            confidence_required=0.1,
            personality_weight={PersonalityTrait.ANALYTICAL_DEPTH: 0.8}
        )
        
        # High threat response branch
        high_threat_node = DecisionNode(
            node_id="high_threat_response",
            condition=lambda ctx: ctx.get('threat_level', 0) > 0.7,
            confidence_required=0.3,
            personality_weight={
                PersonalityTrait.STRESS_RESILIENCE: 0.6,
                PersonalityTrait.DECISION_SPEED: 0.4
            }
        )
        
        # Collaboration decision branch
        collaboration_node = DecisionNode(
            node_id="consider_collaboration",
            condition=lambda ctx: len(ctx.get('collaborative_opportunities', [])) > 0,
            confidence_required=0.4,
            personality_weight={
                PersonalityTrait.SOCIAL_ORIENTATION: 0.7,
                PersonalityTrait.INFORMATION_SHARING: 0.3
            }
        )
        
        # Information gathering branch
        info_gathering_node = DecisionNode(
            node_id="gather_information",
            condition=lambda ctx: ctx.get('information_availability', 1.0) < 0.6,
            confidence_required=0.2,
            personality_weight={
                PersonalityTrait.ANALYTICAL_DEPTH: 0.8,
                PersonalityTrait.SECURITY_CONSCIOUSNESS: 0.2
            }
        )
        
        # Build decision tree structure
        root.children = [high_threat_node, collaboration_node, info_gathering_node]
        
        # Add second-level nodes
        immediate_action_node = DecisionNode(
            node_id="immediate_action",
            condition=lambda ctx: ctx.get('time_pressure', 0) > 0.8,
            confidence_required=0.6,
            personality_weight={PersonalityTrait.DECISION_SPEED: 1.0}
        )
        
        careful_analysis_node = DecisionNode(
            node_id="careful_analysis",
            condition=lambda ctx: ctx.get('time_pressure', 0) < 0.4,
            confidence_required=0.7,
            personality_weight={PersonalityTrait.ANALYTICAL_DEPTH: 1.0}
        )
        
        high_threat_node.children = [immediate_action_node, careful_analysis_node]
        
        return root
    
    def _generate_activity_pattern(self) -> np.ndarray:
        """Generate 24-hour activity pattern based on personality."""
        # Base circadian rhythm
        hours = np.arange(24)
        base_pattern = np.sin(2 * np.pi * (hours - 6) / 24) * 0.3 + 0.5
        
        # Personality adjustments
        operational_tempo = self.personality.traits.get(PersonalityTrait.OPERATIONAL_TEMPO, 0.5)
        base_pattern = base_pattern * (0.5 + operational_tempo)
        
        # Add some individual variation
        individual_variation = np.random.normal(0, 0.1, 24)
        pattern = base_pattern + individual_variation
        
        # Normalize to 0-1 range
        pattern = np.clip(pattern, 0.0, 1.0)
        
        return pattern
    
    def _initialize_communication_style(self) -> Dict[str, Any]:
        """Initialize communication style parameters."""
        social_orientation = self.personality.traits.get(PersonalityTrait.SOCIAL_ORIENTATION, 0.5)
        information_sharing = self.personality.traits.get(PersonalityTrait.INFORMATION_SHARING, 0.5)
        authority_respect = self.personality.traits.get(PersonalityTrait.AUTHORITY_RESPECT, 0.5)
        
        return {
            'message_frequency': social_orientation * 5 + 1,  # 1-6 messages per interaction
            'formality_level': authority_respect,  # 0-1 formal vs casual
            'information_detail_level': information_sharing,  # 0-1 brief vs detailed
            'response_latency_base': 2.0 - self.personality.traits.get(PersonalityTrait.DECISION_SPEED, 0.5) * 1.8,  # 0.2-2.0 seconds
            'protocol_switching_tendency': 1.0 - authority_respect,  # Higher = more likely to switch protocols
            'group_communication_preference': social_orientation * 0.8  # Preference for group vs individual communication
        }
    
    def make_decision(self, context: BehaviorContext, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Make decision based on context and available options."""
        decision_start_time = time.time()
        
        # Convert context to dictionary for decision tree
        context_dict = {
            'threat_level': context.threat_level,
            'time_pressure': context.time_pressure,
            'information_availability': context.information_availability,
            'collaborative_opportunities': context.collaborative_opportunities,
            'operational_phase': context.operational_phase,
            'social_setting': context.social_setting
        }
        
        # Traverse decision tree
        selected_path = []
        current_node = self.decision_tree
        decision_confidence = 0.0
        
        while current_node:
            meets_threshold, node_confidence = current_node.evaluate(context_dict, self.personality)
            selected_path.append(current_node.node_id)
            decision_confidence = max(decision_confidence, node_confidence)
            
            if not meets_threshold or not current_node.children:
                break
            
            # Select best child node
            best_child = None
            best_confidence = 0.0
            
            for child in current_node.children:
                child_meets, child_confidence = child.evaluate(context_dict, self.personality)
                if child_meets and child_confidence > best_confidence:
                    best_child = child
                    best_confidence = child_confidence
            
            current_node = best_child
        
        # Evaluate options based on decision path and personality
        option_scores = []
        for i, option in enumerate(options):
            score = self._evaluate_option(option, context, selected_path)
            option_scores.append((i, score))
        
        # Select best option
        if option_scores:
            best_option_idx, best_score = max(option_scores, key=lambda x: x[1])
            selected_option = options[best_option_idx]
        else:
            selected_option = {}
            best_score = 0.0
        
        # Record decision
        decision_record = {
            'timestamp': context.timestamp,
            'context': asdict(context),
            'options_considered': len(options),
            'selected_option': selected_option,
            'decision_path': selected_path,
            'confidence': decision_confidence,
            'option_score': best_score,
            'decision_time_ms': (time.time() - decision_start_time) * 1000
        }
        
        self.decision_history.append(decision_record)
        
        # Update experience and learning
        self._update_experience(decision_record)
        
        return {
            'decision': selected_option,
            'confidence': decision_confidence,
            'reasoning': selected_path,
            'decision_time_ms': decision_record['decision_time_ms']
        }
    
    def _evaluate_option(self, option: Dict[str, Any], context: BehaviorContext, 
                        decision_path: List[str]) -> float:
        """Evaluate option based on personality and context."""
        base_score = 0.5
        
        # Risk assessment
        option_risk = option.get('risk_level', 0.5)
        risk_tolerance = self.personality.get_effective_trait_value(
            PersonalityTrait.RISK_TOLERANCE, {'stress_level': self.stress_level}
        )
        risk_score = 1.0 - abs(option_risk - risk_tolerance)
        
        # Collaboration factor
        requires_collaboration = option.get('requires_collaboration', False)
        social_orientation = self.personality.traits.get(PersonalityTrait.SOCIAL_ORIENTATION, 0.5)
        collaboration_score = social_orientation if requires_collaboration else (1.0 - social_orientation)
        
        # Time sensitivity
        option_duration = option.get('estimated_duration', 1.0)  # Hours
        time_pressure_factor = 1.0 / (1.0 + option_duration * context.time_pressure)
        
        # Information requirements
        info_required = option.get('information_required', 0.5)
        analytical_preference = self.personality.traits.get(PersonalityTrait.ANALYTICAL_DEPTH, 0.5)
        info_score = 1.0 - abs(info_required - analytical_preference)
        
        # Security considerations
        security_risk = option.get('security_risk', 0.3)
        security_consciousness = self.personality.traits.get(PersonalityTrait.SECURITY_CONSCIOUSNESS, 0.7)
        security_score = 1.0 - (security_risk * (1.0 - security_consciousness))
        
        # Past experience influence
        option_type = option.get('type', 'unknown')
        experience_modifier = self.success_patterns.get(option_type, 0.5)
        
        # Combine scores with personality-based weights
        innovation_drive = self.personality.traits.get(PersonalityTrait.INNOVATION_DRIVE, 0.5)
        weights = {
            'risk': 0.2,
            'collaboration': 0.15,
            'time': 0.2,
            'information': 0.15,
            'security': 0.2,
            'experience': 0.1
        }
        
        # Adjust weights based on innovation drive
        if option.get('is_novel', False):
            weights['experience'] *= (1.0 - innovation_drive)  # Less weight on experience for innovative agents
        
        final_score = (weights['risk'] * risk_score +
                      weights['collaboration'] * collaboration_score +
                      weights['time'] * time_pressure_factor +
                      weights['information'] * info_score +
                      weights['security'] * security_score +
                      weights['experience'] * experience_modifier)
        
        return max(0.0, min(1.0, final_score))
    
    def _update_experience(self, decision_record: Dict[str, Any]) -> None:
        """Update experience patterns based on decision outcome."""
        self.experience_history.append(decision_record)
        
        # Update belief about decision effectiveness (simplified)
        decision_path_key = '->'.join(decision_record['decision_path'])
        option_type = decision_record['selected_option'].get('type', 'unknown')
        
        # Simulated outcome (in real system, this would be based on actual results)
        simulated_success = decision_record['confidence'] > 0.6
        
        learning_rate = self.personality.learning_rate
        
        if simulated_success:
            self.success_patterns[option_type] = (
                (1 - learning_rate) * self.success_patterns[option_type] + 
                learning_rate * 1.0
            )
        else:
            self.failure_patterns[option_type] = (
                (1 - learning_rate) * self.failure_patterns[option_type] + 
                learning_rate * 1.0
            )
    
    def update_emotional_state(self, context: BehaviorContext, recent_outcomes: List[bool]) -> EmotionalState:
        """Update emotional state based on context and recent outcomes."""
        # Calculate outcome-based emotional adjustment
        if recent_outcomes:
            success_rate = sum(recent_outcomes) / len(recent_outcomes)
            if success_rate > 0.8:
                emotional_trend = 1.0  # Positive
            elif success_rate < 0.4:
                emotional_trend = -1.0  # Negative
            else:
                emotional_trend = 0.0  # Neutral
        else:
            emotional_trend = 0.0
        
        # Context-based emotional response
        stress_factors = [
            context.threat_level,
            context.time_pressure,
            context.stakeholder_pressure,
            context.resource_constraints
        ]
        
        average_stress = sum(stress_factors) / len(stress_factors)
        
        # Update stress level
        stress_resilience = self.personality.traits.get(PersonalityTrait.STRESS_RESILIENCE, 0.5)
        stress_adjustment = average_stress * (1.0 - stress_resilience)
        self.stress_level = max(0.0, min(1.0, self.stress_level + stress_adjustment * 0.1))
        
        # Determine new emotional state
        if self.stress_level > 0.8:
            new_state = EmotionalState.STRESSED
        elif emotional_trend > 0.5:
            new_state = EmotionalState.CONFIDENT
        elif emotional_trend < -0.5:
            new_state = EmotionalState.ANXIOUS
        elif context.threat_level > 0.7:
            new_state = EmotionalState.SUSPICIOUS
        elif context.time_pressure > 0.8:
            new_state = EmotionalState.FOCUSED
        else:
            new_state = EmotionalState.CALM
        
        # Gradual state transition (personality stability)
        stability = self.personality.personality_stability
        if new_state != self.current_emotional_state:
            if random.random() > stability:  # Allow state change
                self.current_emotional_state = new_state
        
        return self.current_emotional_state
    
    def calculate_collaboration_affinity(self, other_agent_id: str, 
                                       other_personality: PersonalityMatrix) -> float:
        """Calculate affinity for collaborating with another agent."""
        # Personality compatibility
        trait_differences = []
        for trait in PersonalityTrait:
            self_value = self.personality.traits.get(trait, 0.5)
            other_value = other_personality.traits.get(trait, 0.5)
            
            # Some traits are better when similar, others when complementary
            complementary_traits = {
                PersonalityTrait.ANALYTICAL_DEPTH,
                PersonalityTrait.OPERATIONAL_TEMPO,
                PersonalityTrait.INNOVATION_DRIVE
            }
            
            if trait in complementary_traits:
                # Complementary is good (different values)
                compatibility = abs(self_value - other_value)
            else:
                # Similar is good (same values)
                compatibility = 1.0 - abs(self_value - other_value)
            
            trait_differences.append(compatibility)
        
        personality_compatibility = np.mean(trait_differences)
        
        # Past collaboration history
        collaboration_history = self.collaboration_history.get(other_agent_id, [])
        if collaboration_history:
            past_success_rate = sum(
                collab.get('success', False) for collab in collaboration_history[-10:]
            ) / min(len(collaboration_history), 10)
        else:
            past_success_rate = 0.5  # Neutral assumption
        
        # Trust level
        trust_level = self.relationship_matrix.get(other_agent_id, 0.5)
        
        # Social orientation influence
        social_orientation = self.personality.traits.get(PersonalityTrait.SOCIAL_ORIENTATION, 0.5)
        
        # Combine factors
        affinity = (0.4 * personality_compatibility +
                   0.3 * past_success_rate +
                   0.2 * trust_level +
                   0.1 * social_orientation)
        
        return max(0.0, min(1.0, affinity))
    
    def generate_communication_pattern(self, target_agent_id: str, context: BehaviorContext,
                                     message_importance: float) -> Dict[str, Any]:
        """Generate communication pattern for interaction with specific agent."""
        # Base communication style
        style_params = self.communication_style_parameters.copy()
        
        # Relationship adjustment
        trust_level = self.relationship_matrix.get(target_agent_id, 0.5)
        style_params['formality_level'] *= (0.5 + 0.5 * (1.0 - trust_level))  # More formal with less trusted agents
        
        # Context adjustments
        if context.threat_level > 0.7:
            style_params['response_latency_base'] *= 0.5  # Faster response under threat
            style_params['information_detail_level'] *= 1.3  # More detailed in crisis
        
        if context.time_pressure > 0.8:
            style_params['message_frequency'] *= 0.7  # Fewer messages under time pressure
            style_params['response_latency_base'] *= 0.3  # Much faster response
        
        # Importance adjustment
        style_params['information_detail_level'] *= (0.5 + message_importance)
        style_params['response_latency_base'] /= (1.0 + message_importance * 2.0)
        
        # Current emotional state influence
        emotional_modifiers = {
            EmotionalState.STRESSED: {
                'response_latency_base': 0.7,
                'message_frequency': 1.2,
                'formality_level': 1.1
            },
            EmotionalState.CONFIDENT: {
                'information_detail_level': 1.2,
                'formality_level': 0.9
            },
            EmotionalState.SUSPICIOUS: {
                'information_detail_level': 0.8,
                'response_latency_base': 1.3
            },
            EmotionalState.FOCUSED: {
                'response_latency_base': 0.8,
                'information_detail_level': 1.1
            }
        }
        
        emotional_modifier = emotional_modifiers.get(self.current_emotional_state, {})
        for param, multiplier in emotional_modifier.items():
            if param in style_params:
                style_params[param] *= multiplier
        
        # Generate specific communication metrics
        communication_pattern = {
            'estimated_response_time_seconds': max(0.1, style_params['response_latency_base']),
            'message_frequency_per_interaction': max(1, int(style_params['message_frequency'])),
            'formality_score': min(1.0, style_params['formality_level']),
            'information_detail_score': min(1.0, style_params['information_detail_level']),
            'protocol_switching_probability': min(1.0, style_params['protocol_switching_tendency']),
            'preferred_communication_mode': 'group' if style_params['group_communication_preference'] > 0.6 else 'individual',
            'trust_level': trust_level,
            'emotional_state': self.current_emotional_state.value
        }
        
        # Record communication pattern
        self.communication_patterns[target_agent_id].append(datetime.now())
        
        return communication_pattern
    
    def adapt_behavior(self, feedback: Dict[str, Any]) -> None:
        """Adapt behavior based on feedback and outcomes."""
        adaptation_rate = self.personality.adaptation_rate
        
        # Feedback types
        success_feedback = feedback.get('success_rate', 0.5)
        efficiency_feedback = feedback.get('efficiency_score', 0.5)
        collaboration_feedback = feedback.get('collaboration_effectiveness', 0.5)
        security_feedback = feedback.get('security_compliance', 0.8)
        
        # Adapt personality traits slightly based on feedback
        trait_adjustments = {
            PersonalityTrait.DECISION_SPEED: (efficiency_feedback - 0.5) * adaptation_rate * 0.1,
            PersonalityTrait.SOCIAL_ORIENTATION: (collaboration_feedback - 0.5) * adaptation_rate * 0.1,
            PersonalityTrait.SECURITY_CONSCIOUSNESS: (security_feedback - 0.8) * adaptation_rate * 0.1,
            PersonalityTrait.RISK_TOLERANCE: (success_feedback - 0.5) * adaptation_rate * 0.05
        }
        
        for trait, adjustment in trait_adjustments.items():
            current_value = self.personality.traits.get(trait, 0.5)
            new_value = max(0.0, min(1.0, current_value + adjustment))
            self.personality.traits[trait] = new_value
        
        # Record adaptation event
        adaptation_record = {
            'timestamp': datetime.now(),
            'feedback': feedback,
            'trait_adjustments': trait_adjustments,
            'adaptation_magnitude': sum(abs(adj) for adj in trait_adjustments.values())
        }
        
        self.belief_updates.append(adaptation_record)
        
        logger.debug(f"Agent {self.agent_id} adapted behavior: {adaptation_record}")
    
    def get_current_activity_level(self, timestamp: datetime) -> float:
        """Get current activity level based on time and personality."""
        hour = timestamp.hour
        base_activity = self.daily_activity_pattern[hour]
        
        # Emotional state modifier
        emotional_modifiers = {
            EmotionalState.EXCITED: 1.3,
            EmotionalState.FOCUSED: 1.2,
            EmotionalState.CONFIDENT: 1.1,
            EmotionalState.CALM: 1.0,
            EmotionalState.STRESSED: 0.8,
            EmotionalState.ANXIOUS: 0.7,
            EmotionalState.SUSPICIOUS: 0.9,
            EmotionalState.DETERMINED: 1.2
        }
        
        emotional_modifier = emotional_modifiers.get(self.current_emotional_state, 1.0)
        
        # Energy level influence
        energy_influence = 0.5 + (self.energy_level * 0.5)
        
        # Operational tempo influence
        operational_tempo = self.personality.traits.get(PersonalityTrait.OPERATIONAL_TEMPO, 0.5)
        tempo_influence = 0.7 + (operational_tempo * 0.6)
        
        final_activity = base_activity * emotional_modifier * energy_influence * tempo_influence
        
        return max(0.0, min(1.0, final_activity))
    
    def get_behavior_summary(self) -> Dict[str, Any]:
        """Get comprehensive behavior summary."""
        recent_decisions = list(self.decision_history)[-10:]
        recent_communications = sum(len(comms) for comms in self.communication_patterns.values())
        
        return {
            'agent_id': self.agent_id,
            'personality_traits': {trait.value: value for trait, value in self.personality.traits.items()},
            'cognitive_style': self.personality.cognitive_style.value,
            'current_emotional_state': self.current_emotional_state.value,
            'stress_level': self.stress_level,
            'confidence_level': self.confidence_level,
            'energy_level': self.energy_level,
            'recent_decision_count': len(recent_decisions),
            'average_decision_confidence': np.mean([d['confidence'] for d in recent_decisions]) if recent_decisions else 0.5,
            'average_decision_time_ms': np.mean([d['decision_time_ms'] for d in recent_decisions]) if recent_decisions else 0.0,
            'communication_activity': recent_communications,
            'relationship_count': len(self.relationship_matrix),
            'adaptation_events': len(self.belief_updates),
            'experience_patterns': {
                'success_patterns': dict(self.success_patterns),
                'failure_patterns': dict(self.failure_patterns)
            }
        }


class BehaviorAnalytics:
    """Analytics engine for agent behavior patterns."""
    
    def __init__(self):
        self.behavior_data = defaultdict(list)
        self.pattern_cache = {}
        
    def analyze_agent_behavior(self, agent: MathematicalAgentBehavior, 
                             time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze agent behavior patterns."""
        summary = agent.get_behavior_summary()
        
        # Decision pattern analysis
        recent_decisions = list(agent.decision_history)[-100:]
        
        decision_analysis = {
            'decision_consistency': self._calculate_decision_consistency(recent_decisions),
            'risk_preference_trend': self._analyze_risk_trends(recent_decisions),
            'collaboration_tendency': self._analyze_collaboration_patterns(recent_decisions),
            'decision_speed_pattern': self._analyze_decision_speed(recent_decisions)
        }
        
        # Communication pattern analysis
        comm_analysis = {
            'communication_regularity': self._analyze_communication_regularity(agent.communication_patterns),
            'relationship_stability': self._analyze_relationship_stability(agent.relationship_matrix),
            'social_network_metrics': self._calculate_social_metrics(agent.relationship_matrix)
        }
        
        # Adaptation analysis
        adaptation_analysis = {
            'adaptation_frequency': len(agent.belief_updates) / max(1, len(agent.experience_history)),
            'learning_effectiveness': self._calculate_learning_effectiveness(agent),
            'behavioral_drift': self._calculate_behavioral_drift(agent)
        }
        
        return {
            'agent_summary': summary,
            'decision_patterns': decision_analysis,
            'communication_patterns': comm_analysis,
            'adaptation_patterns': adaptation_analysis,
            'behavioral_predictions': self._predict_future_behavior(agent)
        }
    
    def _calculate_decision_consistency(self, decisions: List[Dict[str, Any]]) -> float:
        """Calculate consistency of decision-making patterns."""
        if len(decisions) < 2:
            return 1.0
        
        decision_paths = [d.get('decision_path', []) for d in decisions]
        
        # Calculate similarity between consecutive decision paths
        similarities = []
        for i in range(1, len(decision_paths)):
            path1, path2 = decision_paths[i-1], decision_paths[i]
            
            # Jaccard similarity
            set1, set2 = set(path1), set(path2)
            if set1 or set2:
                similarity = len(set1 & set2) / len(set1 | set2)
            else:
                similarity = 1.0
            
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 1.0
    
    def _analyze_risk_trends(self, decisions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze risk-taking trends in decisions."""
        if not decisions:
            return {'trend': 0.0, 'volatility': 0.0}
        
        risk_levels = []
        for decision in decisions:
            option = decision.get('selected_option', {})
            risk_level = option.get('risk_level', 0.5)
            risk_levels.append(risk_level)
        
        if len(risk_levels) < 2:
            return {'trend': risk_levels[0] if risk_levels else 0.5, 'volatility': 0.0}
        
        # Calculate trend using linear regression
        x = np.arange(len(risk_levels))
        slope, _, _, _, _ = stats.linregress(x, risk_levels)
        
        return {
            'trend': slope,
            'average_risk': np.mean(risk_levels),
            'volatility': np.std(risk_levels)
        }
    
    def _analyze_collaboration_patterns(self, decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze collaboration patterns in decisions."""
        if not decisions:
            return {'collaboration_rate': 0.0}
        
        collaborative_decisions = 0
        for decision in decisions:
            option = decision.get('selected_option', {})
            if option.get('requires_collaboration', False):
                collaborative_decisions += 1
        
        collaboration_rate = collaborative_decisions / len(decisions)
        
        return {
            'collaboration_rate': collaboration_rate,
            'total_collaborative_decisions': collaborative_decisions,
            'total_decisions': len(decisions)
        }
    
    def _analyze_decision_speed(self, decisions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze decision speed patterns."""
        if not decisions:
            return {'average_speed': 0.0, 'speed_consistency': 0.0}
        
        decision_times = [d.get('decision_time_ms', 0.0) for d in decisions]
        
        return {
            'average_speed_ms': np.mean(decision_times),
            'speed_consistency': 1.0 / (1.0 + np.std(decision_times)),
            'fastest_decision_ms': min(decision_times) if decision_times else 0.0,
            'slowest_decision_ms': max(decision_times) if decision_times else 0.0
        }
    
    def _analyze_communication_regularity(self, comm_patterns: Dict[str, List[datetime]]) -> Dict[str, float]:
        """Analyze regularity of communication patterns."""
        if not comm_patterns:
            return {'regularity_score': 0.0}
        
        all_communications = []
        for agent_comms in comm_patterns.values():
            all_communications.extend(agent_comms)
        
        if len(all_communications) < 2:
            return {'regularity_score': 0.0}
        
        # Sort communications by time
        all_communications.sort()
        
        # Calculate intervals between communications
        intervals = []
        for i in range(1, len(all_communications)):
            interval = (all_communications[i] - all_communications[i-1]).total_seconds()
            intervals.append(interval)
        
        if not intervals:
            return {'regularity_score': 0.0}
        
        # Regularity is inverse of coefficient of variation
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if mean_interval > 0:
            cv = std_interval / mean_interval
            regularity_score = 1.0 / (1.0 + cv)
        else:
            regularity_score = 0.0
        
        return {
            'regularity_score': regularity_score,
            'average_interval_seconds': mean_interval,
            'interval_variability': cv if mean_interval > 0 else 0.0
        }
    
    def _analyze_relationship_stability(self, relationship_matrix: Dict[str, float]) -> Dict[str, float]:
        """Analyze stability of relationships over time."""
        if not relationship_matrix:
            return {'stability_score': 1.0}
        
        trust_levels = list(relationship_matrix.values())
        
        return {
            'stability_score': 1.0 - np.std(trust_levels),  # Lower variance = higher stability
            'average_trust_level': np.mean(trust_levels),
            'trust_range': max(trust_levels) - min(trust_levels) if trust_levels else 0.0,
            'relationship_count': len(relationship_matrix)
        }
    
    def _calculate_social_metrics(self, relationship_matrix: Dict[str, float]) -> Dict[str, float]:
        """Calculate social network metrics."""
        if len(relationship_matrix) < 2:
            return {'centrality': 0.0, 'clustering': 0.0}
        
        # Simplified social network metrics
        high_trust_relationships = sum(1 for trust in relationship_matrix.values() if trust > 0.7)
        total_relationships = len(relationship_matrix)
        
        centrality = high_trust_relationships / total_relationships if total_relationships > 0 else 0.0
        
        return {
            'centrality': centrality,
            'high_trust_connections': high_trust_relationships,
            'total_connections': total_relationships,
            'average_trust': np.mean(list(relationship_matrix.values())) if relationship_matrix else 0.0
        }
    
    def _calculate_learning_effectiveness(self, agent: MathematicalAgentBehavior) -> float:
        """Calculate how effectively the agent learns from experience."""
        if not agent.experience_history:
            return 0.5
        
        # Compare early vs recent decision confidence
        early_decisions = list(agent.decision_history)[:10]
        recent_decisions = list(agent.decision_history)[-10:]
        
        if not early_decisions or not recent_decisions:
            return 0.5
        
        early_avg_confidence = np.mean([d['confidence'] for d in early_decisions])
        recent_avg_confidence = np.mean([d['confidence'] for d in recent_decisions])
        
        improvement = recent_avg_confidence - early_avg_confidence
        
        # Learning effectiveness is improvement capped at reasonable bounds
        return max(0.0, min(1.0, 0.5 + improvement))
    
    def _calculate_behavioral_drift(self, agent: MathematicalAgentBehavior) -> float:
        """Calculate how much agent behavior has drifted over time."""
        if len(agent.belief_updates) < 2:
            return 0.0
        
        # Calculate total magnitude of personality changes
        total_drift = 0.0
        for update in agent.belief_updates:
            trait_changes = update.get('trait_adjustments', {})
            update_magnitude = sum(abs(change) for change in trait_changes.values())
            total_drift += update_magnitude
        
        # Normalize by number of updates and theoretical maximum
        avg_drift = total_drift / len(agent.belief_updates) if agent.belief_updates else 0.0
        
        return min(1.0, avg_drift)
    
    def _predict_future_behavior(self, agent: MathematicalAgentBehavior) -> Dict[str, Any]:
        """Predict future behavior patterns."""
        # Simple predictions based on current trends
        recent_decisions = list(agent.decision_history)[-20:]
        
        if len(recent_decisions) < 5:
            return {'prediction_confidence': 0.0}
        
        # Predict decision speed trend
        recent_speeds = [d['decision_time_ms'] for d in recent_decisions]
        speed_trend = 'stable'
        if len(recent_speeds) >= 2:
            slope, _, _, _, _ = stats.linregress(range(len(recent_speeds)), recent_speeds)
            if slope > 5:  # Getting slower
                speed_trend = 'slowing'
            elif slope < -5:  # Getting faster
                speed_trend = 'accelerating'
        
        # Predict confidence trend
        confidence_levels = [d['confidence'] for d in recent_decisions]
        avg_recent_confidence = np.mean(confidence_levels)
        
        confidence_trend = 'stable'
        if avg_recent_confidence > 0.75:
            confidence_trend = 'increasing'
        elif avg_recent_confidence < 0.4:
            confidence_trend = 'decreasing'
        
        return {
            'prediction_confidence': 0.7,  # Moderate confidence in predictions
            'decision_speed_trend': speed_trend,
            'confidence_trend': confidence_trend,
            'predicted_activity_level': agent.get_current_activity_level(datetime.now()),
            'adaptation_likelihood': min(1.0, agent.personality.adaptation_rate * 2),
            'collaboration_propensity': agent.personality.traits.get(PersonalityTrait.SOCIAL_ORIENTATION, 0.5)
        }


async def main():
    """Main demonstration of mathematical agent behaviors."""
    print("MWRASP Mathematical Agent Behavior Models")
    print("=" * 50)
    
    # Create diverse agent personalities
    agent_configs = [
        {
            'agent_id': 'ANALYST_ALPHA',
            'traits': {
                PersonalityTrait.ANALYTICAL_DEPTH: 0.9,
                PersonalityTrait.DECISION_SPEED: 0.3,
                PersonalityTrait.SOCIAL_ORIENTATION: 0.4,
                PersonalityTrait.RISK_TOLERANCE: 0.2,
                PersonalityTrait.SECURITY_CONSCIOUSNESS: 0.9
            },
            'cognitive_style': CognitiveStyle.ANALYTICAL,
            'base_emotional_state': EmotionalState.FOCUSED
        },
        {
            'agent_id': 'FIELD_AGENT_BETA',
            'traits': {
                PersonalityTrait.DECISION_SPEED: 0.9,
                PersonalityTrait.RISK_TOLERANCE: 0.8,
                PersonalityTrait.OPERATIONAL_TEMPO: 0.9,
                PersonalityTrait.SOCIAL_ORIENTATION: 0.6,
                PersonalityTrait.STRESS_RESILIENCE: 0.8
            },
            'cognitive_style': CognitiveStyle.INTUITIVE,
            'base_emotional_state': EmotionalState.CONFIDENT
        },
        {
            'agent_id': 'QUANTUM_SPECIALIST_GAMMA',
            'traits': {
                PersonalityTrait.INNOVATION_DRIVE: 0.9,
                PersonalityTrait.ANALYTICAL_DEPTH: 0.8,
                PersonalityTrait.SOCIAL_ORIENTATION: 0.3,
                PersonalityTrait.SECURITY_CONSCIOUSNESS: 0.8,
                PersonalityTrait.AUTHORITY_RESPECT: 0.4
            },
            'cognitive_style': CognitiveStyle.CREATIVE,
            'base_emotional_state': EmotionalState.EXCITED
        }
    ]
    
    # Initialize agents
    agents = {}
    print("Initializing Agent Personalities:")
    
    for config in agent_configs:
        personality = PersonalityMatrix(
            traits=config['traits'],
            cognitive_style=config['cognitive_style'],
            base_emotional_state=config['base_emotional_state'],
            personality_stability=0.8,
            adaptation_rate=0.1,
            decision_confidence_threshold=0.5,
            collaboration_preference_matrix=np.array([]),
            learning_rate=0.05
        )
        
        agent = MathematicalAgentBehavior(config['agent_id'], personality)
        agents[config['agent_id']] = agent
        
        print(f"  ✓ {config['agent_id']}: {config['cognitive_style'].value} style")
        print(f"    Top traits: {', '.join([trait.value for trait, value in sorted(config['traits'].items(), key=lambda x: x[1], reverse=True)][:3])}")
    
    # Simulate decision-making scenarios
    print("\nSimulating Decision-Making Scenarios:")
    
    scenarios = [
        {
            'name': 'High-Threat Response',
            'context': BehaviorContext(
                timestamp=datetime.now(),
                operational_phase='crisis',
                threat_level=0.9,
                time_pressure=0.8,
                social_setting='small_group',
                information_availability=0.6,
                resource_constraints=0.7,
                stakeholder_pressure=0.9,
                recent_success_rate=0.7,
                collaborative_opportunities=['ANALYST_ALPHA', 'FIELD_AGENT_BETA']
            ),
            'options': [
                {'type': 'immediate_response', 'risk_level': 0.8, 'requires_collaboration': False, 'estimated_duration': 0.5},
                {'type': 'coordinated_response', 'risk_level': 0.4, 'requires_collaboration': True, 'estimated_duration': 2.0},
                {'type': 'intelligence_gathering', 'risk_level': 0.2, 'requires_collaboration': False, 'estimated_duration': 4.0}
            ]
        },
        {
            'name': 'Routine Analysis Task',
            'context': BehaviorContext(
                timestamp=datetime.now(),
                operational_phase='analysis',
                threat_level=0.3,
                time_pressure=0.2,
                social_setting='individual',
                information_availability=0.8,
                resource_constraints=0.3,
                stakeholder_pressure=0.4,
                recent_success_rate=0.8,
                collaborative_opportunities=['QUANTUM_SPECIALIST_GAMMA']
            ),
            'options': [
                {'type': 'standard_analysis', 'risk_level': 0.1, 'requires_collaboration': False, 'estimated_duration': 3.0},
                {'type': 'deep_analysis', 'risk_level': 0.2, 'requires_collaboration': False, 'estimated_duration': 8.0},
                {'type': 'collaborative_analysis', 'risk_level': 0.3, 'requires_collaboration': True, 'estimated_duration': 5.0}
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n  Scenario: {scenario['name']}")
        
        for agent_id, agent in agents.items():
            decision_result = agent.make_decision(scenario['context'], scenario['options'])
            selected_option = decision_result['decision']
            
            print(f"    {agent_id}: {selected_option.get('type', 'no_decision')} "
                  f"(confidence: {decision_result['confidence']:.2f}, "
                  f"time: {decision_result['decision_time_ms']:.1f}ms)")
    
    # Analyze collaboration affinities
    print("\nCollaboration Affinity Analysis:")
    agent_list = list(agents.items())
    
    for i, (agent1_id, agent1) in enumerate(agent_list):
        for agent2_id, agent2 in agent_list[i+1:]:
            affinity1to2 = agent1.calculate_collaboration_affinity(agent2_id, agent2.personality)
            affinity2to1 = agent2.calculate_collaboration_affinity(agent1_id, agent1.personality)
            
            avg_affinity = (affinity1to2 + affinity2to1) / 2
            print(f"  {agent1_id} <-> {agent2_id}: {avg_affinity:.3f} affinity")
    
    # Communication pattern analysis
    print("\nCommunication Pattern Generation:")
    
    communication_context = BehaviorContext(
        timestamp=datetime.now(),
        operational_phase='planning',
        threat_level=0.5,
        time_pressure=0.4,
        social_setting='small_group',
        information_availability=0.7,
        resource_constraints=0.4,
        stakeholder_pressure=0.5,
        recent_success_rate=0.8,
        collaborative_opportunities=['ANALYST_ALPHA', 'FIELD_AGENT_BETA']
    )
    
    for agent_id, agent in agents.items():
        for target_id in agents.keys():
            if target_id != agent_id:
                comm_pattern = agent.generate_communication_pattern(
                    target_id, communication_context, message_importance=0.6
                )
                
                print(f"  {agent_id} -> {target_id}:")
                print(f"    Response time: {comm_pattern['estimated_response_time_seconds']:.2f}s")
                print(f"    Formality: {comm_pattern['formality_score']:.2f}")
                print(f"    Protocol switching: {comm_pattern['protocol_switching_probability']:.2f}")
                break  # Only show first target for brevity
    
    # Behavioral adaptation simulation
    print("\nBehavioral Adaptation Simulation:")
    
    # Simulate feedback for each agent
    feedback_scenarios = [
        {'success_rate': 0.9, 'efficiency_score': 0.8, 'collaboration_effectiveness': 0.7, 'security_compliance': 0.9},
        {'success_rate': 0.4, 'efficiency_score': 0.6, 'collaboration_effectiveness': 0.5, 'security_compliance': 0.7},
        {'success_rate': 0.7, 'efficiency_score': 0.9, 'collaboration_effectiveness': 0.8, 'security_compliance': 0.8}
    ]
    
    for i, (agent_id, agent) in enumerate(agents.items()):
        feedback = feedback_scenarios[i % len(feedback_scenarios)]
        original_traits = agent.personality.traits.copy()
        
        agent.adapt_behavior(feedback)
        
        # Show trait changes
        changed_traits = []
        for trait, original_value in original_traits.items():
            new_value = agent.personality.traits[trait]
            if abs(new_value - original_value) > 0.01:
                change = new_value - original_value
                changed_traits.append(f"{trait.value}: {change:+.3f}")
        
        print(f"  {agent_id}: {len(changed_traits)} traits adapted")
        if changed_traits:
            print(f"    Changes: {', '.join(changed_traits[:3])}")  # Show top 3 changes
    
    # Comprehensive behavior analysis
    print("\nComprehensive Behavior Analysis:")
    
    analytics = BehaviorAnalytics()
    
    for agent_id, agent in agents.items():
        analysis = analytics.analyze_agent_behavior(agent, 24)
        
        print(f"  {agent_id} Analysis:")
        print(f"    Decision consistency: {analysis['decision_patterns']['decision_consistency']:.3f}")
        print(f"    Avg decision confidence: {analysis['agent_summary']['average_decision_confidence']:.3f}")
        print(f"    Learning effectiveness: {analysis['adaptation_patterns']['learning_effectiveness']:.3f}")
        print(f"    Behavioral drift: {analysis['adaptation_patterns']['behavioral_drift']:.3f}")
        
        predictions = analysis['behavioral_predictions']
        print(f"    Future trends: {predictions['decision_speed_trend']}, {predictions['confidence_trend']}")


if __name__ == "__main__":
    asyncio.run(main())
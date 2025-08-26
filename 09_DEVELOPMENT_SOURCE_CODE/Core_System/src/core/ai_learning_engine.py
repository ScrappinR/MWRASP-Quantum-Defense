#!/usr/bin/env python3
"""
MWRASP AI Learning Engine
Transforms rule-based agents into adaptive AI systems with learning capabilities
"""

import numpy as np
import json
import sqlite3
import time
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import pickle
from collections import defaultdict, deque


class LearningMode(Enum):
    REINFORCEMENT = "reinforcement"
    SUPERVISED = "supervised" 
    UNSUPERVISED = "unsupervised"
    TRANSFER = "transfer"


class AdaptationLevel(Enum):
    BASIC = "basic"          # Simple parameter updates
    MODERATE = "moderate"    # Strategy adjustments
    ADVANCED = "advanced"    # Architecture changes
    REVOLUTIONARY = "revolutionary"  # Complete behavioral evolution


@dataclass
class Experience:
    """Individual experience record for agent learning"""
    experience_id: str
    agent_id: str
    timestamp: float
    
    # Context
    system_architecture: Dict[str, Any]
    threat_characteristics: Dict[str, Any]
    customer_profile: Dict[str, Any]
    
    # Action taken
    action_type: str
    action_parameters: Dict[str, Any]
    coordination_partners: List[str]
    
    # Outcome
    success: bool
    response_time_ms: float
    effectiveness_score: float
    side_effects: List[str]
    
    # Learning metadata
    confidence: float
    uncertainty: float
    novelty_score: float


@dataclass
class KnowledgePattern:
    """Learned pattern that can be shared between agents"""
    pattern_id: str
    pattern_type: str
    discovered_by: str
    discovery_time: float
    
    # Pattern definition
    conditions: Dict[str, Any]
    recommended_actions: List[Dict[str, Any]]
    success_probability: float
    
    # Validation
    times_validated: int
    validation_success_rate: float
    confidence_level: float
    
    # Evolution
    parent_patterns: List[str]
    evolved_patterns: List[str]


@dataclass
class CustomerProfile:
    """Dynamic customer behavior and preference profile"""
    customer_id: str
    industry: str
    system_architecture_type: str
    
    # Behavioral patterns
    security_tolerance: float  # 0.0 (paranoid) to 1.0 (relaxed)
    performance_priority: float  # 0.0 (security first) to 1.0 (performance first)
    compliance_requirements: List[str]
    
    # Historical preferences
    preferred_response_times: Dict[str, float]
    accepted_risk_levels: Dict[str, float]
    escalation_preferences: Dict[str, str]
    
    # Learning metadata
    profile_confidence: float
    last_updated: float
    adaptation_rate: float


class AILearningEngine:
    """
    Core AI learning system that enables true agent intelligence
    Uses reinforcement learning, pattern recognition, and knowledge transfer
    """
    
    def __init__(self, database_path: str = "mwrasp_ai_learning.db"):
        self.database_path = database_path
        self.learning_active = False
        
        # Learning components
        self.experience_buffer = deque(maxlen=10000)
        self.knowledge_patterns = {}
        self.customer_profiles = {}
        self.agent_models = {}
        
        # Threading
        self.learning_thread = None
        self.stop_event = threading.Event()
        
        # Performance tracking
        self.learning_stats = {
            'experiences_processed': 0,
            'patterns_discovered': 0,
            'successful_adaptations': 0,
            'failed_adaptations': 0,
            'knowledge_transfers': 0
        }
        
        # Initialize database
        self._initialize_database()
        self._load_existing_knowledge()
        
        print("[AI-LEARNING] AI Learning Engine initialized")
    
    def _initialize_database(self):
        """Initialize SQLite database for persistent learning"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Experiences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiences (
                experience_id TEXT PRIMARY KEY,
                agent_id TEXT,
                timestamp REAL,
                system_architecture TEXT,
                threat_characteristics TEXT,
                customer_profile TEXT,
                action_type TEXT,
                action_parameters TEXT,
                coordination_partners TEXT,
                success BOOLEAN,
                response_time_ms REAL,
                effectiveness_score REAL,
                side_effects TEXT,
                confidence REAL,
                uncertainty REAL,
                novelty_score REAL
            )
        ''')
        
        # Knowledge patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT,
                discovered_by TEXT,
                discovery_time REAL,
                conditions TEXT,
                recommended_actions TEXT,
                success_probability REAL,
                times_validated INTEGER,
                validation_success_rate REAL,
                confidence_level REAL,
                parent_patterns TEXT,
                evolved_patterns TEXT
            )
        ''')
        
        # Customer profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_profiles (
                customer_id TEXT PRIMARY KEY,
                industry TEXT,
                system_architecture_type TEXT,
                security_tolerance REAL,
                performance_priority REAL,
                compliance_requirements TEXT,
                preferred_response_times TEXT,
                accepted_risk_levels TEXT,
                escalation_preferences TEXT,
                profile_confidence REAL,
                last_updated REAL,
                adaptation_rate REAL
            )
        ''')
        
        # Agent learning models table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_models (
                agent_id TEXT PRIMARY KEY,
                model_type TEXT,
                model_data BLOB,
                training_experiences INTEGER,
                last_updated REAL,
                performance_metrics TEXT,
                specialization_areas TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("[AI-LEARNING] Database initialized successfully")
    
    def _load_existing_knowledge(self):
        """Load existing knowledge from database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Load knowledge patterns
        cursor.execute("SELECT * FROM knowledge_patterns")
        patterns = cursor.fetchall()
        for row in patterns:
            pattern = self._row_to_knowledge_pattern(row)
            self.knowledge_patterns[pattern.pattern_id] = pattern
        
        # Load customer profiles
        cursor.execute("SELECT * FROM customer_profiles")
        profiles = cursor.fetchall()
        for row in profiles:
            profile = self._row_to_customer_profile(row)
            self.customer_profiles[profile.customer_id] = profile
        
        conn.close()
        
        print(f"[AI-LEARNING] Loaded {len(self.knowledge_patterns)} patterns, {len(self.customer_profiles)} customer profiles")
    
    def start_learning(self):
        """Start the AI learning system"""
        if self.learning_active:
            return
        
        self.learning_active = True
        self.stop_event.clear()
        
        def learning_loop():
            while not self.stop_event.is_set():
                try:
                    self._process_experience_batch()
                    self._discover_new_patterns()
                    self._update_agent_models()
                    self._perform_knowledge_transfer()
                    
                    time.sleep(1.0)  # Learning cycle every second
                    
                except Exception as e:
                    print(f"[AI-LEARNING] Learning error: {e}")
                    time.sleep(5.0)
        
        self.learning_thread = threading.Thread(target=learning_loop, daemon=True)
        self.learning_thread.start()
        
        print("[AI-LEARNING] AI learning system started")
    
    def stop_learning(self):
        """Stop the AI learning system"""
        if not self.learning_active:
            return
        
        self.learning_active = False
        self.stop_event.set()
        
        if self.learning_thread:
            self.learning_thread.join()
        
        print("[AI-LEARNING] AI learning system stopped")
    
    def record_experience(self, experience: Experience):
        """Record a new experience for learning"""
        self.experience_buffer.append(experience)
        self.learning_stats['experiences_processed'] += 1
        
        # Immediate learning for high-impact experiences
        if experience.novelty_score > 0.8 or experience.effectiveness_score < 0.3:
            self._immediate_learning(experience)
    
    def _immediate_learning(self, experience: Experience):
        """Perform immediate learning for critical experiences"""
        # Quick adaptation for novel or failed experiences
        if experience.novelty_score > 0.8:
            # This is a new type of situation - create emergency pattern
            emergency_pattern = self._create_emergency_pattern(experience)
            self.knowledge_patterns[emergency_pattern.pattern_id] = emergency_pattern
            print(f"[AI-LEARNING] Emergency pattern created: {emergency_pattern.pattern_id}")
        
        if experience.effectiveness_score < 0.3:
            # This action failed - mark for avoid and find alternatives
            self._mark_action_for_avoidance(experience)
            print(f"[AI-LEARNING] Action marked for avoidance: {experience.action_type}")
    
    def _process_experience_batch(self):
        """Process a batch of experiences for learning"""
        if len(self.experience_buffer) < 10:
            return
        
        # Process last 50 experiences
        batch_size = min(50, len(self.experience_buffer))
        batch = list(self.experience_buffer)[-batch_size:]
        
        # Group by agent for individual learning
        agent_experiences = defaultdict(list)
        for exp in batch:
            agent_experiences[exp.agent_id].append(exp)
        
        # Update each agent's learning
        for agent_id, experiences in agent_experiences.items():
            self._update_agent_learning(agent_id, experiences)
    
    def _update_agent_learning(self, agent_id: str, experiences: List[Experience]):
        """Update an individual agent's learning model"""
        if agent_id not in self.agent_models:
            self.agent_models[agent_id] = self._create_agent_model(agent_id)
        
        model = self.agent_models[agent_id]
        
        # Reinforcement learning update
        for exp in experiences:
            # Calculate reward signal
            reward = self._calculate_reward(exp)
            
            # Update model with experience
            self._update_model_weights(model, exp, reward)
        
        # Save updated model
        self._save_agent_model(agent_id, model)
    
    def _calculate_reward(self, experience: Experience) -> float:
        """Calculate reward signal for reinforcement learning"""
        reward = 0.0
        
        # Success component (most important)
        reward += 10.0 if experience.success else -10.0
        
        # Effectiveness component
        reward += experience.effectiveness_score * 5.0
        
        # Response time component (faster is better)
        response_penalty = min(experience.response_time_ms / 1000.0, 5.0)
        reward -= response_penalty
        
        # Side effects penalty
        reward -= len(experience.side_effects) * 2.0
        
        # Novelty bonus (encourage exploration)
        reward += experience.novelty_score * 3.0
        
        return reward
    
    def _discover_new_patterns(self):
        """Discover new behavioral patterns from experiences"""
        if len(self.experience_buffer) < 100:
            return
        
        # Analyze recent successful experiences for patterns
        recent_experiences = list(self.experience_buffer)[-200:]
        successful_experiences = [exp for exp in recent_experiences if exp.success and exp.effectiveness_score > 0.7]
        
        if len(successful_experiences) < 10:
            return
        
        # Look for common characteristics in successful experiences
        pattern_candidates = self._find_pattern_candidates(successful_experiences)
        
        for candidate in pattern_candidates:
            if self._validate_pattern(candidate):
                pattern = self._create_knowledge_pattern(candidate)
                self.knowledge_patterns[pattern.pattern_id] = pattern
                self.learning_stats['patterns_discovered'] += 1
                
                print(f"[AI-LEARNING] New pattern discovered: {pattern.pattern_type}")
    
    def _find_pattern_candidates(self, experiences: List[Experience]) -> List[Dict[str, Any]]:
        """Find potential patterns in successful experiences"""
        candidates = []
        
        # Group by action type
        action_groups = defaultdict(list)
        for exp in experiences:
            action_groups[exp.action_type].append(exp)
        
        # Look for patterns in each action type
        for action_type, exp_list in action_groups.items():
            if len(exp_list) >= 5:  # Need at least 5 examples
                # Find common characteristics
                common_conditions = self._extract_common_conditions(exp_list)
                if common_conditions:
                    candidates.append({
                        'action_type': action_type,
                        'conditions': common_conditions,
                        'success_rate': sum(1 for exp in exp_list if exp.success) / len(exp_list),
                        'sample_size': len(exp_list)
                    })
        
        return candidates
    
    def _extract_common_conditions(self, experiences: List[Experience]) -> Dict[str, Any]:
        """Extract common conditions from a group of experiences"""
        if not experiences:
            return {}
        
        common = {}
        
        # Look for common threat characteristics
        threat_patterns = defaultdict(int)
        for exp in experiences:
            for key, value in exp.threat_characteristics.items():
                threat_patterns[f"threat_{key}_{value}"] += 1
        
        # Include conditions that appear in >70% of experiences
        threshold = len(experiences) * 0.7
        for pattern, count in threat_patterns.items():
            if count >= threshold:
                common[pattern] = count / len(experiences)
        
        return common
    
    def get_adaptive_recommendation(self, agent_id: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI-driven action recommendation for an agent"""
        # Get agent's learned model
        if agent_id not in self.agent_models:
            return None
        
        # Find matching patterns
        matching_patterns = self._find_matching_patterns(context)
        
        if not matching_patterns:
            return None
        
        # Select best pattern based on confidence and success rate
        best_pattern = max(matching_patterns, key=lambda p: p.success_probability * p.confidence_level)
        
        # Adapt recommendation based on customer profile
        customer_id = context.get('customer_id', 'default')
        if customer_id in self.customer_profiles:
            recommendation = self._adapt_for_customer(best_pattern, self.customer_profiles[customer_id])
        else:
            recommendation = best_pattern.recommended_actions[0] if best_pattern.recommended_actions else None
        
        return recommendation
    
    def _find_matching_patterns(self, context: Dict[str, Any]) -> List[KnowledgePattern]:
        """Find patterns that match the current context"""
        matching = []
        
        for pattern in self.knowledge_patterns.values():
            match_score = self._calculate_pattern_match(pattern, context)
            if match_score > 0.7:  # 70% match threshold
                matching.append(pattern)
        
        return matching
    
    def _calculate_pattern_match(self, pattern: KnowledgePattern, context: Dict[str, Any]) -> float:
        """Calculate how well a pattern matches the current context"""
        if not pattern.conditions:
            return 0.0
        
        matches = 0
        total_conditions = len(pattern.conditions)
        
        for condition_key, expected_confidence in pattern.conditions.items():
            # Parse condition (e.g., "threat_level_HIGH")
            if condition_key in context:
                matches += expected_confidence
            elif any(condition_key in str(v) for v in context.values()):
                matches += expected_confidence * 0.5
        
        return matches / total_conditions if total_conditions > 0 else 0.0
    
    def update_customer_profile(self, customer_id: str, interaction_data: Dict[str, Any]):
        """Update customer profile based on interactions"""
        if customer_id not in self.customer_profiles:
            self.customer_profiles[customer_id] = self._create_default_customer_profile(customer_id)
        
        profile = self.customer_profiles[customer_id]
        
        # Adaptive learning from customer feedback
        if 'response_time_feedback' in interaction_data:
            # Customer complained about slow response
            if interaction_data['response_time_feedback'] == 'too_slow':
                profile.performance_priority = min(1.0, profile.performance_priority + 0.1)
            elif interaction_data['response_time_feedback'] == 'acceptable':
                # Current balance is good
                pass
        
        if 'security_incident_tolerance' in interaction_data:
            # Customer's reaction to security measures
            tolerance = interaction_data['security_incident_tolerance']
            profile.security_tolerance = profile.security_tolerance * 0.9 + tolerance * 0.1
        
        profile.last_updated = time.time()
        self._save_customer_profile(profile)
        
        print(f"[AI-LEARNING] Customer profile updated: {customer_id}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get comprehensive learning system statistics"""
        return {
            'learning_active': self.learning_active,
            'experiences_in_buffer': len(self.experience_buffer),
            'knowledge_patterns': len(self.knowledge_patterns),
            'customer_profiles': len(self.customer_profiles),
            'trained_agent_models': len(self.agent_models),
            'learning_stats': self.learning_stats.copy(),
            'top_patterns': [
                {
                    'pattern_id': p.pattern_id,
                    'pattern_type': p.pattern_type,
                    'success_probability': p.success_probability,
                    'confidence_level': p.confidence_level
                }
                for p in sorted(self.knowledge_patterns.values(), 
                              key=lambda x: x.success_probability * x.confidence_level, 
                              reverse=True)[:5]
            ]
        }
    
    # Helper methods for database operations
    def _row_to_knowledge_pattern(self, row) -> KnowledgePattern:
        """Convert database row to KnowledgePattern object"""
        return KnowledgePattern(
            pattern_id=row[0],
            pattern_type=row[1],
            discovered_by=row[2],
            discovery_time=row[3],
            conditions=json.loads(row[4]),
            recommended_actions=json.loads(row[5]),
            success_probability=row[6],
            times_validated=row[7],
            validation_success_rate=row[8],
            confidence_level=row[9],
            parent_patterns=json.loads(row[10]),
            evolved_patterns=json.loads(row[11])
        )
    
    def _row_to_customer_profile(self, row) -> CustomerProfile:
        """Convert database row to CustomerProfile object"""
        return CustomerProfile(
            customer_id=row[0],
            industry=row[1],
            system_architecture_type=row[2],
            security_tolerance=row[3],
            performance_priority=row[4],
            compliance_requirements=json.loads(row[5]),
            preferred_response_times=json.loads(row[6]),
            accepted_risk_levels=json.loads(row[7]),
            escalation_preferences=json.loads(row[8]),
            profile_confidence=row[9],
            last_updated=row[10],
            adaptation_rate=row[11]
        )
    
    # Additional helper methods (simplified for brevity)
    def _create_emergency_pattern(self, experience: Experience) -> KnowledgePattern:
        """Create emergency pattern from novel experience"""
        import uuid
        return KnowledgePattern(
            pattern_id=f"emergency_{uuid.uuid4().hex[:8]}",
            pattern_type="emergency_response",
            discovered_by=experience.agent_id,
            discovery_time=time.time(),
            conditions=experience.threat_characteristics,
            recommended_actions=[{
                'action_type': experience.action_type,
                'parameters': experience.action_parameters,
                'emergency': True
            }],
            success_probability=0.5,  # Unknown, start conservative
            times_validated=0,
            validation_success_rate=0.0,
            confidence_level=0.3,  # Low confidence for new patterns
            parent_patterns=[],
            evolved_patterns=[]
        )
    
    def _create_agent_model(self, agent_id: str):
        """Create initial learning model for an agent"""
        return {
            'agent_id': agent_id,
            'model_type': 'reinforcement_learning',
            'weights': np.random.normal(0, 0.1, (10, 5)),  # Simple neural network weights
            'experience_count': 0,
            'specializations': [],
            'adaptation_rate': 0.01
        }
    
    def _create_default_customer_profile(self, customer_id: str) -> CustomerProfile:
        """Create default customer profile"""
        return CustomerProfile(
            customer_id=customer_id,
            industry="unknown",
            system_architecture_type="hybrid",
            security_tolerance=0.5,
            performance_priority=0.5,
            compliance_requirements=[],
            preferred_response_times={'low': 5.0, 'medium': 2.0, 'high': 0.5},
            accepted_risk_levels={'financial': 0.1, 'operational': 0.3, 'reputation': 0.05},
            escalation_preferences={'automatic': 'enabled', 'manual_review': 'high_risk_only'},
            profile_confidence=0.1,
            last_updated=time.time(),
            adaptation_rate=0.05
        )
    
    # Placeholder methods for complex operations
    def _mark_action_for_avoidance(self, experience: Experience): pass
    def _validate_pattern(self, candidate: Dict[str, Any]) -> bool: return True
    def _create_knowledge_pattern(self, candidate: Dict[str, Any]) -> KnowledgePattern: pass
    def _update_model_weights(self, model, experience: Experience, reward: float): pass
    def _save_agent_model(self, agent_id: str, model): pass
    def _perform_knowledge_transfer(self): pass
    def _adapt_for_customer(self, pattern: KnowledgePattern, profile: CustomerProfile): pass
    def _save_customer_profile(self, profile: CustomerProfile): pass
    
    def _update_agent_models(self):
        """Update agent models based on recent experiences"""
        try:
            for agent_id, model in self.agent_models.items():
                # Simple model update - increment experience count
                model['experience_count'] = model.get('experience_count', 0) + 1
                
                # Update adaptation rate based on recent performance
                if model['experience_count'] > 0:
                    model['adaptation_rate'] = min(0.1, model['adaptation_rate'] * 1.01)
                    
        except Exception as e:
            print(f"[AI-LEARNING] Model update error: {e}")
            pass


# Global learning engine instance
_learning_engine = None

def get_learning_engine() -> AILearningEngine:
    """Get or create global learning engine instance"""
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = AILearningEngine()
        _learning_engine.start_learning()
    return _learning_engine
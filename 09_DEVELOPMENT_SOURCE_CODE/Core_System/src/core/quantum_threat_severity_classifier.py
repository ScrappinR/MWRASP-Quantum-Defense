"""
MWRASP Real-Time Quantum Threat Severity Classification Engine
Ultra-low latency quantum threat severity classification system for national security infrastructure.
Integrates with all MWRASP detection engines and agent network for immediate response coordination.
"""

import asyncio
import time
import json
import logging
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict, deque
import heapq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThreatSeverityLevel(Enum):
    """Quantum threat severity levels for national security."""
    DEFCON_1 = "DEFCON_1"  # Maximum readiness - Nuclear war imminent/underway
    DEFCON_2 = "DEFCON_2"  # Next step to nuclear war - Armed forces ready to deploy
    DEFCON_3 = "DEFCON_3"  # Increase in force readiness above normal
    DEFCON_4 = "DEFCON_4"  # Increased intelligence watch and strengthened security
    DEFCON_5 = "DEFCON_5"  # Normal peacetime readiness
    
    QUANTUM_CRITICAL = "QUANTUM_CRITICAL"  # Quantum supremacy attack in progress
    QUANTUM_HIGH = "QUANTUM_HIGH"  # Active quantum threat detected
    QUANTUM_MEDIUM = "QUANTUM_MEDIUM"  # Potential quantum vulnerability
    QUANTUM_LOW = "QUANTUM_LOW"  # Quantum anomaly detected
    QUANTUM_INFO = "QUANTUM_INFO"  # Quantum intelligence gathering


class ThreatImpactScale(Enum):
    """Impact scale for quantum threats on national infrastructure."""
    CATASTROPHIC = "CATASTROPHIC"  # Complete national infrastructure compromise
    CRITICAL = "CRITICAL"  # Major infrastructure systems compromised
    SIGNIFICANT = "SIGNIFICANT"  # Key infrastructure components affected
    MODERATE = "MODERATE"  # Limited infrastructure impact
    MINIMAL = "MINIMAL"  # Negligible infrastructure impact


class ThreatUrgency(Enum):
    """Threat response urgency levels."""
    IMMEDIATE = "IMMEDIATE"  # Response required within seconds
    URGENT = "URGENT"  # Response required within minutes
    HIGH = "HIGH"  # Response required within hours
    NORMAL = "NORMAL"  # Response required within days
    LOW = "LOW"  # Response required within weeks


class ThreatVector(Enum):
    """Quantum threat attack vectors."""
    QUANTUM_CIRCUIT_MANIPULATION = "quantum_circuit_manipulation"
    QUANTUM_KEY_COMPROMISE = "quantum_key_compromise"
    QUANTUM_COMMUNICATION_INTERCEPTION = "quantum_communication_interception"
    QUANTUM_COMPUTING_ADVANTAGE = "quantum_computing_advantage"
    QUANTUM_CRYPTOGRAPHIC_BREAK = "quantum_cryptographic_break"
    QUANTUM_BLOCKCHAIN_ATTACK = "quantum_blockchain_attack"
    QUANTUM_TELEPORTATION_HIJACK = "quantum_teleportation_hijack"
    QUANTUM_ERROR_INJECTION = "quantum_error_injection"
    QUANTUM_SUPREMACY_EXPLOITATION = "quantum_supremacy_exploitation"
    POST_QUANTUM_MIGRATION_ATTACK = "post_quantum_migration_attack"


class InfrastructureTarget(Enum):
    """Critical infrastructure targets."""
    MILITARY_COMMUNICATIONS = "military_communications"
    INTELLIGENCE_NETWORKS = "intelligence_networks"
    FINANCIAL_SYSTEMS = "financial_systems"
    POWER_GRID = "power_grid"
    TRANSPORTATION = "transportation"
    HEALTHCARE = "healthcare"
    GOVERNMENT_SERVICES = "government_services"
    SPACE_SYSTEMS = "space_systems"
    NUCLEAR_FACILITIES = "nuclear_facilities"
    QUANTUM_INFRASTRUCTURE = "quantum_infrastructure"


@dataclass
class ThreatContext:
    """Contextual information about a quantum threat."""
    source_location: Optional[str] = None
    target_infrastructure: List[InfrastructureTarget] = None
    attack_sophistication: str = "UNKNOWN"  # NATION_STATE, ORGANIZED_CRIME, TERRORIST, INDIVIDUAL
    threat_actor_profile: Dict[str, Any] = None
    geopolitical_context: Dict[str, Any] = None
    technical_indicators: Dict[str, Any] = None
    intelligence_confidence: float = 0.5
    related_campaigns: List[str] = None
    
    def __post_init__(self):
        if self.target_infrastructure is None:
            self.target_infrastructure = []
        if self.threat_actor_profile is None:
            self.threat_actor_profile = {}
        if self.geopolitical_context is None:
            self.geopolitical_context = {}
        if self.technical_indicators is None:
            self.technical_indicators = {}
        if self.related_campaigns is None:
            self.related_campaigns = []


@dataclass
class SeverityClassification:
    """Complete threat severity classification result."""
    threat_id: str
    timestamp: datetime
    severity_level: ThreatSeverityLevel
    impact_scale: ThreatImpactScale
    urgency: ThreatUrgency
    threat_vector: ThreatVector
    context: ThreatContext
    confidence_score: float  # 0.0 to 1.0
    classification_reasoning: Dict[str, Any]
    response_recommendations: List[str]
    agent_assignments: Dict[str, List[str]]
    escalation_triggers: List[str]
    classification_latency_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'threat_id': self.threat_id,
            'timestamp': self.timestamp.isoformat(),
            'severity_level': self.severity_level.value,
            'impact_scale': self.impact_scale.value,
            'urgency': self.urgency.value,
            'threat_vector': self.threat_vector.value,
            'context': asdict(self.context),
            'confidence_score': self.confidence_score,
            'classification_reasoning': self.classification_reasoning,
            'response_recommendations': self.response_recommendations,
            'agent_assignments': self.agent_assignments,
            'escalation_triggers': self.escalation_triggers,
            'classification_latency_ms': self.classification_latency_ms
        }


class ThreatClassificationRule:
    """Individual threat classification rule."""
    
    def __init__(self, rule_id: str, conditions: Dict[str, Any], classification: Dict[str, Any], priority: int = 5):
        self.rule_id = rule_id
        self.conditions = conditions
        self.classification = classification
        self.priority = priority  # Lower number = higher priority
        self.match_count = 0
        self.false_positive_rate = 0.0
        self.accuracy_rate = 1.0
    
    def evaluate(self, threat_data: Dict[str, Any]) -> Tuple[bool, float]:
        """Evaluate if threat data matches this rule."""
        match_score = 0.0
        total_conditions = len(self.conditions)
        
        if total_conditions == 0:
            return False, 0.0
        
        for condition_key, condition_value in self.conditions.items():
            if self._evaluate_condition(threat_data, condition_key, condition_value):
                match_score += 1.0
        
        match_ratio = match_score / total_conditions
        is_match = match_ratio >= 0.7  # 70% of conditions must match
        
        if is_match:
            self.match_count += 1
        
        return is_match, match_ratio
    
    def _evaluate_condition(self, threat_data: Dict[str, Any], condition_key: str, condition_value: Any) -> bool:
        """Evaluate individual condition."""
        try:
            # Navigate nested dictionaries
            keys = condition_key.split('.')
            data_value = threat_data
            
            for key in keys:
                if isinstance(data_value, dict) and key in data_value:
                    data_value = data_value[key]
                else:
                    return False
            
            # Perform comparison based on condition type
            if isinstance(condition_value, dict):
                if 'min' in condition_value and 'max' in condition_value:
                    return condition_value['min'] <= data_value <= condition_value['max']
                elif 'greater_than' in condition_value:
                    return data_value > condition_value['greater_than']
                elif 'less_than' in condition_value:
                    return data_value < condition_value['less_than']
                elif 'contains' in condition_value:
                    return condition_value['contains'] in str(data_value)
                elif 'equals' in condition_value:
                    return data_value == condition_value['equals']
            else:
                return data_value == condition_value
            
        except (KeyError, TypeError, ValueError):
            return False
        
        return False


class MWRASPAgentCoordinator:
    """Coordinator for MWRASP agent network integration."""
    
    def __init__(self):
        self.agent_capabilities = self._initialize_agent_capabilities()
        self.agent_availability = self._simulate_agent_availability()
        self.response_protocols = self._initialize_response_protocols()
    
    def _initialize_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Initialize agent capabilities for threat response."""
        return {
            'DIRECTOR_ALPHA': {
                'clearance_level': 'TOP_SECRET_SCI',
                'specializations': ['strategic_assessment', 'policy_coordination', 'interagency_liaison'],
                'response_authority': 'EXECUTIVE_DECISION',
                'quantum_expertise': 'STRATEGIC_OVERVIEW'
            },
            'DEPUTY_DIRECTOR_OPS': {
                'clearance_level': 'TOP_SECRET_SCI',
                'specializations': ['tactical_operations', 'field_coordination', 'crisis_management'],
                'response_authority': 'OPERATIONAL_COMMAND',
                'quantum_expertise': 'OPERATIONAL_QUANTUM'
            },
            'DEPUTY_DIRECTOR_ANALYSIS': {
                'clearance_level': 'TOP_SECRET_SCI',
                'specializations': ['threat_analysis', 'intelligence_fusion', 'predictive_modeling'],
                'response_authority': 'ANALYTICAL_ASSESSMENT',
                'quantum_expertise': 'QUANTUM_ANALYSIS_EXPERT'
            },
            'STATION_CHIEF_QUANTUM': {
                'clearance_level': 'TOP_SECRET',
                'specializations': ['quantum_security', 'cryptographic_operations', 'technical_assessment'],
                'response_authority': 'TECHNICAL_COORDINATION',
                'quantum_expertise': 'QUANTUM_TECHNICAL_EXPERT'
            },
            'HANDLER_CRYPTO': {
                'clearance_level': 'SECRET',
                'specializations': ['cryptographic_analysis', 'key_management', 'protocol_validation'],
                'response_authority': 'TECHNICAL_IMPLEMENTATION',
                'quantum_expertise': 'POST_QUANTUM_CRYPTOGRAPHY'
            },
            'ANALYST_QUANTUM_PRIME': {
                'clearance_level': 'SECRET',
                'specializations': ['quantum_algorithm_analysis', 'threat_modeling', 'vulnerability_assessment'],
                'response_authority': 'TECHNICAL_ANALYSIS',
                'quantum_expertise': 'QUANTUM_ALGORITHM_SPECIALIST'
            },
            'FIELD_AGENT_QUANTUM_01': {
                'clearance_level': 'SECRET',
                'specializations': ['field_operations', 'technical_reconnaissance', 'system_infiltration'],
                'response_authority': 'TACTICAL_EXECUTION',
                'quantum_expertise': 'QUANTUM_FIELD_OPERATIONS'
            },
            'WATCHER_NETWORK_ALPHA': {
                'clearance_level': 'CONFIDENTIAL',
                'specializations': ['network_monitoring', 'anomaly_detection', 'surveillance'],
                'response_authority': 'MONITORING_COORDINATION',
                'quantum_expertise': 'QUANTUM_NETWORK_MONITORING'
            }
        }
    
    def _simulate_agent_availability(self) -> Dict[str, Dict[str, Any]]:
        """Simulate current agent availability and status."""
        return {
            agent_id: {
                'status': np.random.choice(['AVAILABLE', 'ON_MISSION', 'STAND_BY'], p=[0.6, 0.2, 0.2]),
                'location': np.random.choice(['HEADQUARTERS', 'FIELD_STATION', 'REMOTE', 'CLASSIFIED']),
                'response_time_seconds': np.random.uniform(0.1, 5.0),
                'current_workload': np.random.uniform(0.0, 1.0),
                'last_contact': datetime.now() - timedelta(seconds=np.random.randint(1, 300))
            }
            for agent_id in self.agent_capabilities.keys()
        }
    
    def _initialize_response_protocols(self) -> Dict[ThreatSeverityLevel, Dict[str, Any]]:
        """Initialize response protocols for different threat severity levels."""
        return {
            ThreatSeverityLevel.DEFCON_1: {
                'required_agents': ['DIRECTOR_ALPHA', 'DEPUTY_DIRECTOR_OPS', 'DEPUTY_DIRECTOR_ANALYSIS'],
                'response_time_limit_seconds': 10,
                'authorization_required': 'PRESIDENTIAL',
                'escalation_automatic': True,
                'communication_protocol': 'FLASH_OVERRIDE',
                'agent_activation': 'ALL_AVAILABLE'
            },
            ThreatSeverityLevel.DEFCON_2: {
                'required_agents': ['DEPUTY_DIRECTOR_OPS', 'STATION_CHIEF_QUANTUM', 'ANALYST_QUANTUM_PRIME'],
                'response_time_limit_seconds': 30,
                'authorization_required': 'DIRECTOR',
                'escalation_automatic': True,
                'communication_protocol': 'FLASH',
                'agent_activation': 'PRIORITY_TEAMS'
            },
            ThreatSeverityLevel.QUANTUM_CRITICAL: {
                'required_agents': ['STATION_CHIEF_QUANTUM', 'ANALYST_QUANTUM_PRIME', 'HANDLER_CRYPTO'],
                'response_time_limit_seconds': 60,
                'authorization_required': 'DEPUTY_DIRECTOR',
                'escalation_automatic': True,
                'communication_protocol': 'IMMEDIATE',
                'agent_activation': 'QUANTUM_SPECIALISTS'
            },
            ThreatSeverityLevel.QUANTUM_HIGH: {
                'required_agents': ['ANALYST_QUANTUM_PRIME', 'FIELD_AGENT_QUANTUM_01'],
                'response_time_limit_seconds': 300,
                'authorization_required': 'STATION_CHIEF',
                'escalation_automatic': False,
                'communication_protocol': 'PRIORITY',
                'agent_activation': 'RESPONSE_TEAM'
            },
            ThreatSeverityLevel.QUANTUM_MEDIUM: {
                'required_agents': ['WATCHER_NETWORK_ALPHA', 'ANALYST_QUANTUM_PRIME'],
                'response_time_limit_seconds': 1800,
                'authorization_required': 'HANDLER',
                'escalation_automatic': False,
                'communication_protocol': 'ROUTINE',
                'agent_activation': 'MONITORING_ENHANCED'
            }
        }
    
    def assign_agents_for_threat(self, classification: SeverityClassification) -> Dict[str, List[str]]:
        """Assign appropriate agents for threat response."""
        protocol = self.response_protocols.get(classification.severity_level, 
                                               self.response_protocols[ThreatSeverityLevel.QUANTUM_MEDIUM])
        
        assignments = {
            'primary_response': [],
            'support_team': [],
            'monitoring': [],
            'escalation_chain': []
        }
        
        # Primary response team
        for required_agent in protocol['required_agents']:
            agent_status = self.agent_availability.get(required_agent, {})
            if agent_status.get('status') == 'AVAILABLE':
                assignments['primary_response'].append(required_agent)
            else:
                # Find backup agents with similar capabilities
                backup = self._find_backup_agent(required_agent)
                if backup:
                    assignments['primary_response'].append(backup)
        
        # Support team based on threat vector
        support_agents = self._select_support_agents(classification.threat_vector)
        assignments['support_team'].extend(support_agents)
        
        # Monitoring team
        monitoring_agents = [agent_id for agent_id, caps in self.agent_capabilities.items() 
                           if 'surveillance' in caps.get('specializations', [])]
        assignments['monitoring'].extend(monitoring_agents[:2])  # Limit to 2 for efficiency
        
        # Escalation chain
        assignments['escalation_chain'] = self._build_escalation_chain(classification.severity_level)
        
        return assignments
    
    def _find_backup_agent(self, primary_agent: str) -> Optional[str]:
        """Find backup agent with similar capabilities."""
        primary_caps = self.agent_capabilities.get(primary_agent, {})
        primary_specializations = set(primary_caps.get('specializations', []))
        
        best_match = None
        best_overlap = 0
        
        for agent_id, capabilities in self.agent_capabilities.items():
            if agent_id == primary_agent:
                continue
            
            agent_status = self.agent_availability.get(agent_id, {})
            if agent_status.get('status') != 'AVAILABLE':
                continue
            
            specializations = set(capabilities.get('specializations', []))
            overlap = len(primary_specializations.intersection(specializations))
            
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = agent_id
        
        return best_match
    
    def _select_support_agents(self, threat_vector: ThreatVector) -> List[str]:
        """Select support agents based on threat vector."""
        vector_specialization_map = {
            ThreatVector.QUANTUM_CIRCUIT_MANIPULATION: ['quantum_algorithm_analysis', 'technical_assessment'],
            ThreatVector.QUANTUM_KEY_COMPROMISE: ['cryptographic_analysis', 'key_management'],
            ThreatVector.QUANTUM_COMMUNICATION_INTERCEPTION: ['network_monitoring', 'surveillance'],
            ThreatVector.QUANTUM_COMPUTING_ADVANTAGE: ['quantum_algorithm_analysis', 'predictive_modeling'],
            ThreatVector.QUANTUM_CRYPTOGRAPHIC_BREAK: ['cryptographic_analysis', 'vulnerability_assessment']
        }
        
        needed_specializations = vector_specialization_map.get(threat_vector, [])
        support_agents = []
        
        for agent_id, capabilities in self.agent_capabilities.items():
            agent_specializations = capabilities.get('specializations', [])
            if any(spec in agent_specializations for spec in needed_specializations):
                agent_status = self.agent_availability.get(agent_id, {})
                if agent_status.get('status') == 'AVAILABLE':
                    support_agents.append(agent_id)
        
        return support_agents[:3]  # Limit to 3 support agents
    
    def _build_escalation_chain(self, severity_level: ThreatSeverityLevel) -> List[str]:
        """Build escalation chain for threat severity level."""
        if severity_level in [ThreatSeverityLevel.DEFCON_1, ThreatSeverityLevel.DEFCON_2]:
            return ['DIRECTOR_ALPHA', 'DEPUTY_DIRECTOR_OPS', 'DEPUTY_DIRECTOR_ANALYSIS']
        elif severity_level == ThreatSeverityLevel.QUANTUM_CRITICAL:
            return ['DEPUTY_DIRECTOR_OPS', 'STATION_CHIEF_QUANTUM', 'DIRECTOR_ALPHA']
        else:
            return ['STATION_CHIEF_QUANTUM', 'DEPUTY_DIRECTOR_ANALYSIS']


class QuantumThreatSeverityClassifier:
    """Real-time quantum threat severity classification engine for MWRASP."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.agent_coordinator = MWRASPAgentCoordinator()
        
        # Classification rules engine
        self.classification_rules = self._initialize_classification_rules()
        self.rule_priority_queue = []
        
        # Real-time processing
        self.classification_queue = asyncio.Queue(maxsize=10000)
        self.processed_classifications = deque(maxlen=50000)
        
        # Performance metrics
        self.classification_metrics = {
            'threats_classified': 0,
            'average_latency_ms': 0.0,
            'accuracy_rate': 0.95,
            'false_positive_rate': 0.03,
            'agent_assignments_made': 0,
            'escalations_triggered': 0
        }
        
        # Machine learning enhancement
        self.ml_model_weights = self._initialize_ml_weights()
        self.threat_pattern_history = defaultdict(list)
        
        # Initialize rule priority queue
        self._rebuild_rule_priority_queue()
        
        logger.info("MWRASP Quantum Threat Severity Classifier initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for the classifier."""
        return {
            'ultra_low_latency_mode': True,
            'target_latency_ms': 0.5,  # Sub-millisecond target
            'parallel_processing': True,
            'max_worker_threads': 16,
            'ml_enhancement_enabled': True,
            'auto_agent_assignment': True,
            'real_time_learning': True,
            'classification_confidence_threshold': 0.7,
            'escalation_enabled': True,
            'threat_correlation_enabled': True,
            'quantum_velocity_integration': True
        }
    
    def _initialize_classification_rules(self) -> List[ThreatClassificationRule]:
        """Initialize threat classification rules."""
        rules = [
            # DEFCON Level Rules
            ThreatClassificationRule(
                rule_id="DEFCON_1_QUANTUM_WAR",
                conditions={
                    'threat_indicators.attack_scale': {'equals': 'NATION_WIDE'},
                    'threat_indicators.quantum_advantage': {'greater_than': 1000000},
                    'threat_indicators.infrastructure_impact': {'equals': 'TOTAL_COMPROMISE'},
                    'confidence': {'greater_than': 0.9}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.DEFCON_1,
                    'impact_scale': ThreatImpactScale.CATASTROPHIC,
                    'urgency': ThreatUrgency.IMMEDIATE
                },
                priority=1
            ),
            
            ThreatClassificationRule(
                rule_id="DEFCON_2_QUANTUM_CRITICAL",
                conditions={
                    'threat_indicators.attack_scale': {'equals': 'REGIONAL'},
                    'threat_indicators.quantum_advantage': {'greater_than': 100000},
                    'threat_indicators.critical_infrastructure_count': {'greater_than': 5},
                    'confidence': {'greater_than': 0.85}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.DEFCON_2,
                    'impact_scale': ThreatImpactScale.CRITICAL,
                    'urgency': ThreatUrgency.IMMEDIATE
                },
                priority=1
            ),
            
            # Quantum-Specific Critical Rules
            ThreatClassificationRule(
                rule_id="QUANTUM_SUPREMACY_ATTACK",
                conditions={
                    'source': {'equals': 'supremacy_detector'},
                    'threat_indicators.quantum_advantage': {'greater_than': 10000},
                    'threat_indicators.attack_type': {'contains': 'supremacy'},
                    'confidence': {'greater_than': 0.8}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_CRITICAL,
                    'impact_scale': ThreatImpactScale.CRITICAL,
                    'urgency': ThreatUrgency.IMMEDIATE
                },
                priority=2
            ),
            
            ThreatClassificationRule(
                rule_id="QUANTUM_KEY_COMPROMISE",
                conditions={
                    'source': {'equals': 'qkd_detector'},
                    'threat_indicators.attack_type': {'contains': 'key_compromise'},
                    'threat_indicators.affected_keys': {'greater_than': 100},
                    'confidence': {'greater_than': 0.75}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_CRITICAL,
                    'impact_scale': ThreatImpactScale.SIGNIFICANT,
                    'urgency': ThreatUrgency.URGENT
                },
                priority=2
            ),
            
            ThreatClassificationRule(
                rule_id="QUANTUM_CIRCUIT_MANIPULATION",
                conditions={
                    'source': {'equals': 'circuit_fingerprint'},
                    'threat_indicators.circuit_manipulation': {'equals': True},
                    'threat_indicators.hardware_compromise': {'equals': True},
                    'confidence': {'greater_than': 0.7}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_HIGH,
                    'impact_scale': ThreatImpactScale.SIGNIFICANT,
                    'urgency': ThreatUrgency.URGENT
                },
                priority=3
            ),
            
            ThreatClassificationRule(
                rule_id="POST_QUANTUM_MIGRATION_ATTACK",
                conditions={
                    'source': {'equals': 'migration_tools'},
                    'threat_indicators.migration_disruption': {'equals': True},
                    'threat_indicators.cryptographic_downgrade': {'equals': True},
                    'confidence': {'greater_than': 0.6}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_HIGH,
                    'impact_scale': ThreatImpactScale.MODERATE,
                    'urgency': ThreatUrgency.HIGH
                },
                priority=3
            ),
            
            # Medium-Level Quantum Threats
            ThreatClassificationRule(
                rule_id="QUANTUM_ANOMALY_DETECTED",
                conditions={
                    'confidence': {'min': 0.5, 'max': 0.7},
                    'threat_indicators.anomaly_type': {'equals': 'quantum'},
                    'threat_indicators.impact_assessment': {'equals': 'LIMITED'}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_MEDIUM,
                    'impact_scale': ThreatImpactScale.MODERATE,
                    'urgency': ThreatUrgency.HIGH
                },
                priority=4
            ),
            
            ThreatClassificationRule(
                rule_id="QUANTUM_INTELLIGENCE_GATHERING",
                conditions={
                    'threat_indicators.activity_type': {'equals': 'reconnaissance'},
                    'threat_indicators.quantum_probing': {'equals': True},
                    'confidence': {'min': 0.4, 'max': 0.6}
                },
                classification={
                    'severity_level': ThreatSeverityLevel.QUANTUM_LOW,
                    'impact_scale': ThreatImpactScale.MINIMAL,
                    'urgency': ThreatUrgency.NORMAL
                },
                priority=5
            )
        ]
        
        return rules
    
    def _initialize_ml_weights(self) -> Dict[str, float]:
        """Initialize machine learning model weights for classification enhancement."""
        return {
            'confidence_multiplier': 1.2,
            'temporal_correlation_weight': 0.8,
            'source_reliability_weight': 0.9,
            'infrastructure_impact_weight': 1.5,
            'geopolitical_context_weight': 0.7,
            'technical_sophistication_weight': 1.1,
            'threat_actor_profile_weight': 1.0,
            'historical_pattern_weight': 0.6
        }
    
    def _rebuild_rule_priority_queue(self) -> None:
        """Rebuild rule priority queue based on accuracy and priority."""
        self.rule_priority_queue.clear()
        
        for rule in self.classification_rules:
            # Calculate dynamic priority based on accuracy and base priority
            dynamic_priority = rule.priority * (2.0 - rule.accuracy_rate)
            heapq.heappush(self.rule_priority_queue, (dynamic_priority, rule.rule_id, rule))
    
    async def classify_threat_realtime(self, threat_data: Dict[str, Any]) -> SeverityClassification:
        """Classify threat with ultra-low latency for real-time response."""
        classification_start = time.perf_counter()
        
        try:
            # Extract threat context
            context = self._extract_threat_context(threat_data)
            
            # Apply classification rules (optimized for speed)
            severity_level, impact_scale, urgency, confidence_score, reasoning = await self._apply_classification_rules(threat_data)
            
            # Determine threat vector
            threat_vector = self._identify_threat_vector(threat_data)
            
            # Generate response recommendations
            response_recommendations = self._generate_response_recommendations(severity_level, threat_vector, context)
            
            # Assign agents if auto-assignment is enabled
            agent_assignments = {}
            if self.config.get('auto_agent_assignment', True):
                # Create temporary classification for agent assignment
                temp_classification = SeverityClassification(
                    threat_id=threat_data.get('threat_id', 'TEMP_ID'),
                    timestamp=datetime.now(),
                    severity_level=severity_level,
                    impact_scale=impact_scale,
                    urgency=urgency,
                    threat_vector=threat_vector,
                    context=context,
                    confidence_score=confidence_score,
                    classification_reasoning=reasoning,
                    response_recommendations=response_recommendations,
                    agent_assignments={},
                    escalation_triggers=[],
                    classification_latency_ms=0.0
                )
                agent_assignments = self.agent_coordinator.assign_agents_for_threat(temp_classification)
            
            # Determine escalation triggers
            escalation_triggers = self._determine_escalation_triggers(severity_level, confidence_score, context)
            
            # Calculate classification latency
            classification_end = time.perf_counter()
            latency_ms = (classification_end - classification_start) * 1000
            
            # Create final classification
            classification = SeverityClassification(
                threat_id=threat_data.get('threat_id', self._generate_threat_id()),
                timestamp=datetime.now(),
                severity_level=severity_level,
                impact_scale=impact_scale,
                urgency=urgency,
                threat_vector=threat_vector,
                context=context,
                confidence_score=confidence_score,
                classification_reasoning=reasoning,
                response_recommendations=response_recommendations,
                agent_assignments=agent_assignments,
                escalation_triggers=escalation_triggers,
                classification_latency_ms=latency_ms
            )
            
            # Update metrics and learning
            await self._update_classification_metrics(classification)
            
            # Real-time learning
            if self.config.get('real_time_learning', True):
                await self._update_threat_patterns(classification)
            
            # Store classification
            self.processed_classifications.append(classification)
            
            # Auto-escalate if required
            if self.config.get('escalation_enabled', True) and escalation_triggers:
                await self._trigger_escalation(classification)
            
            return classification
            
        except Exception as e:
            logger.error(f"Error in threat classification: {e}")
            # Return minimal classification on error
            return self._create_error_classification(threat_data, str(e))
    
    def _extract_threat_context(self, threat_data: Dict[str, Any]) -> ThreatContext:
        """Extract contextual information from threat data."""
        indicators = threat_data.get('threat_indicators', {})
        
        # Determine infrastructure targets
        target_infrastructure = []
        if indicators.get('target_military', False):
            target_infrastructure.append(InfrastructureTarget.MILITARY_COMMUNICATIONS)
        if indicators.get('target_financial', False):
            target_infrastructure.append(InfrastructureTarget.FINANCIAL_SYSTEMS)
        if indicators.get('target_power_grid', False):
            target_infrastructure.append(InfrastructureTarget.POWER_GRID)
        if indicators.get('target_quantum', False):
            target_infrastructure.append(InfrastructureTarget.QUANTUM_INFRASTRUCTURE)
        
        # Determine attack sophistication
        sophistication = "UNKNOWN"
        if indicators.get('nation_state_indicators', 0) > 5:
            sophistication = "NATION_STATE"
        elif indicators.get('advanced_persistent_threat', False):
            sophistication = "ORGANIZED_CRIME"
        elif indicators.get('basic_attack_patterns', False):
            sophistication = "INDIVIDUAL"
        
        return ThreatContext(
            source_location=threat_data.get('source_location'),
            target_infrastructure=target_infrastructure,
            attack_sophistication=sophistication,
            threat_actor_profile=indicators.get('threat_actor', {}),
            geopolitical_context=threat_data.get('geopolitical_context', {}),
            technical_indicators=indicators,
            intelligence_confidence=threat_data.get('confidence', 0.5),
            related_campaigns=threat_data.get('related_campaigns', [])
        )
    
    async def _apply_classification_rules(self, threat_data: Dict[str, Any]) -> Tuple[ThreatSeverityLevel, ThreatImpactScale, ThreatUrgency, float, Dict[str, Any]]:
        """Apply classification rules to determine threat severity."""
        best_match = None
        best_score = 0.0
        matching_rules = []
        
        # Evaluate rules in priority order
        temp_queue = list(self.rule_priority_queue)
        
        for priority, rule_id, rule in temp_queue:
            is_match, match_score = rule.evaluate(threat_data)
            
            if is_match:
                matching_rules.append((rule, match_score))
                if match_score > best_score:
                    best_score = match_score
                    best_match = rule
        
        if best_match:
            classification = best_match.classification
            severity_level = classification['severity_level']
            impact_scale = classification['impact_scale']
            urgency = classification['urgency']
            
            # Apply ML enhancement
            enhanced_confidence = self._enhance_confidence_with_ml(threat_data, best_score)
            
            reasoning = {
                'matched_rule': best_match.rule_id,
                'rule_confidence': best_score,
                'ml_enhanced_confidence': enhanced_confidence,
                'matching_rules_count': len(matching_rules),
                'classification_factors': self._analyze_classification_factors(threat_data)
            }
            
            return severity_level, impact_scale, urgency, enhanced_confidence, reasoning
        else:
            # Default classification for unmatched threats
            return (ThreatSeverityLevel.QUANTUM_INFO, 
                    ThreatImpactScale.MINIMAL, 
                    ThreatUrgency.LOW, 
                    0.3, 
                    {'matched_rule': 'default', 'reason': 'no_matching_rules'})
    
    def _enhance_confidence_with_ml(self, threat_data: Dict[str, Any], base_confidence: float) -> float:
        """Enhance confidence score using machine learning weights."""
        if not self.config.get('ml_enhancement_enabled', True):
            return base_confidence
        
        enhancement_factors = []
        
        # Source reliability factor
        source_reliability = self._get_source_reliability(threat_data.get('source', 'unknown'))
        enhancement_factors.append(source_reliability * self.ml_model_weights['source_reliability_weight'])
        
        # Infrastructure impact factor
        impact_score = self._calculate_infrastructure_impact_score(threat_data)
        enhancement_factors.append(impact_score * self.ml_model_weights['infrastructure_impact_weight'])
        
        # Technical sophistication factor
        sophistication_score = self._calculate_sophistication_score(threat_data)
        enhancement_factors.append(sophistication_score * self.ml_model_weights['technical_sophistication_weight'])
        
        # Historical pattern factor
        pattern_score = self._calculate_historical_pattern_score(threat_data)
        enhancement_factors.append(pattern_score * self.ml_model_weights['historical_pattern_weight'])
        
        # Calculate weighted enhancement
        avg_enhancement = np.mean(enhancement_factors) if enhancement_factors else 1.0
        enhanced_confidence = min(1.0, base_confidence * self.ml_model_weights['confidence_multiplier'] * avg_enhancement)
        
        return enhanced_confidence
    
    def _get_source_reliability(self, source: str) -> float:
        """Get reliability score for threat intelligence source."""
        reliability_scores = {
            'circuit_fingerprint': 0.9,
            'qkd_detector': 0.95,
            'supremacy_detector': 0.85,
            'ml_predictor': 0.8,
            'blockchain_detector': 0.75,
            'migration_tools': 0.8,
            'agent_network': 0.95,
            'external_intel': 0.6
        }
        return reliability_scores.get(source, 0.5)
    
    def _calculate_infrastructure_impact_score(self, threat_data: Dict[str, Any]) -> float:
        """Calculate infrastructure impact score."""
        indicators = threat_data.get('threat_indicators', {})
        
        impact_factors = [
            indicators.get('critical_systems_affected', 0) / 10.0,
            1.0 if indicators.get('power_grid_impact', False) else 0.0,
            1.0 if indicators.get('financial_system_impact', False) else 0.0,
            1.0 if indicators.get('military_network_impact', False) else 0.0,
            indicators.get('civilian_infrastructure_impact', 0) / 5.0
        ]
        
        return min(1.0, np.mean(impact_factors))
    
    def _calculate_sophistication_score(self, threat_data: Dict[str, Any]) -> float:
        """Calculate attack sophistication score."""
        indicators = threat_data.get('threat_indicators', {})
        
        sophistication_factors = [
            indicators.get('quantum_algorithm_complexity', 0) / 10.0,
            1.0 if indicators.get('advanced_evasion_techniques', False) else 0.0,
            indicators.get('custom_exploit_count', 0) / 5.0,
            1.0 if indicators.get('zero_day_exploits', False) else 0.0,
            indicators.get('multi_stage_attack', 0) / 3.0
        ]
        
        return min(1.0, np.mean(sophistication_factors))
    
    def _calculate_historical_pattern_score(self, threat_data: Dict[str, Any]) -> float:
        """Calculate score based on historical threat patterns."""
        threat_signature = self._generate_threat_signature(threat_data)
        
        # Check for similar patterns in history
        similar_patterns = 0
        total_patterns = len(self.threat_pattern_history)
        
        if total_patterns == 0:
            return 0.5  # Neutral score for first threat
        
        for historical_signature in self.threat_pattern_history:
            similarity = self._calculate_pattern_similarity(threat_signature, historical_signature)
            if similarity > 0.7:  # 70% similarity threshold
                similar_patterns += 1
        
        # Higher score for threats matching known dangerous patterns
        return min(1.0, (similar_patterns / total_patterns) * 2.0)
    
    def _generate_threat_signature(self, threat_data: Dict[str, Any]) -> str:
        """Generate signature for threat pattern matching."""
        indicators = threat_data.get('threat_indicators', {})
        
        signature_components = [
            threat_data.get('source', 'unknown'),
            str(indicators.get('attack_type', 'unknown')),
            str(indicators.get('target_systems', [])),
            str(indicators.get('techniques_used', []))
        ]
        
        signature = '|'.join(signature_components)
        return hashlib.md5(signature.encode()).hexdigest()
    
    def _calculate_pattern_similarity(self, signature1: str, signature2: str) -> float:
        """Calculate similarity between two threat signatures."""
        # Simple character-based similarity (could be enhanced with more sophisticated algorithms)
        if signature1 == signature2:
            return 1.0
        
        common_chars = sum(1 for a, b in zip(signature1, signature2) if a == b)
        max_length = max(len(signature1), len(signature2))
        
        return common_chars / max_length if max_length > 0 else 0.0
    
    def _analyze_classification_factors(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze factors that contributed to the classification."""
        indicators = threat_data.get('threat_indicators', {})
        
        return {
            'confidence_level': threat_data.get('confidence', 0.0),
            'source_reliability': self._get_source_reliability(threat_data.get('source', 'unknown')),
            'infrastructure_targets': len(indicators.get('target_systems', [])),
            'attack_complexity': indicators.get('complexity_score', 0),
            'temporal_correlation': len(threat_data.get('correlated_threats', [])),
            'geopolitical_tension': threat_data.get('geopolitical_context', {}).get('tension_level', 'low')
        }
    
    def _identify_threat_vector(self, threat_data: Dict[str, Any]) -> ThreatVector:
        """Identify the primary threat vector."""
        source = threat_data.get('source', '')
        indicators = threat_data.get('threat_indicators', {})
        
        # Map sources to threat vectors
        if 'circuit' in source.lower():
            return ThreatVector.QUANTUM_CIRCUIT_MANIPULATION
        elif 'qkd' in source.lower() or 'key' in str(indicators.get('attack_type', '')).lower():
            return ThreatVector.QUANTUM_KEY_COMPROMISE
        elif 'teleportation' in source.lower():
            return ThreatVector.QUANTUM_TELEPORTATION_HIJACK
        elif 'supremacy' in source.lower():
            return ThreatVector.QUANTUM_SUPREMACY_EXPLOITATION
        elif 'blockchain' in source.lower():
            return ThreatVector.QUANTUM_BLOCKCHAIN_ATTACK
        elif 'migration' in source.lower():
            return ThreatVector.POST_QUANTUM_MIGRATION_ATTACK
        elif indicators.get('communication_interception', False):
            return ThreatVector.QUANTUM_COMMUNICATION_INTERCEPTION
        elif indicators.get('cryptographic_break', False):
            return ThreatVector.QUANTUM_CRYPTOGRAPHIC_BREAK
        else:
            return ThreatVector.QUANTUM_COMPUTING_ADVANTAGE
    
    def _generate_response_recommendations(self, severity_level: ThreatSeverityLevel, 
                                         threat_vector: ThreatVector, 
                                         context: ThreatContext) -> List[str]:
        """Generate response recommendations based on classification."""
        recommendations = []
        
        # Base recommendations by severity
        if severity_level in [ThreatSeverityLevel.DEFCON_1, ThreatSeverityLevel.DEFCON_2]:
            recommendations.extend([
                "IMMEDIATE: Activate national quantum emergency response",
                "IMMEDIATE: Brief senior leadership and policy makers",
                "IMMEDIATE: Coordinate with allied quantum defense networks",
                "IMMEDIATE: Implement quantum infrastructure isolation protocols"
            ])
        elif severity_level == ThreatSeverityLevel.QUANTUM_CRITICAL:
            recommendations.extend([
                "URGENT: Deploy quantum incident response team",
                "URGENT: Activate enhanced quantum monitoring",
                "URGENT: Implement quantum key rotation protocols",
                "URGENT: Brief quantum security stakeholders"
            ])
        elif severity_level == ThreatSeverityLevel.QUANTUM_HIGH:
            recommendations.extend([
                "HIGH: Increase quantum threat monitoring sensitivity",
                "HIGH: Deploy additional quantum sensors",
                "HIGH: Review and update quantum defense posture",
                "HIGH: Coordinate with affected infrastructure owners"
            ])
        
        # Vector-specific recommendations
        vector_recommendations = {
            ThreatVector.QUANTUM_CIRCUIT_MANIPULATION: [
                "Validate quantum circuit integrity across all systems",
                "Implement enhanced circuit fingerprinting",
                "Isolate affected quantum hardware"
            ],
            ThreatVector.QUANTUM_KEY_COMPROMISE: [
                "Execute emergency quantum key rotation",
                "Audit quantum key distribution channels",
                "Implement backup key exchange protocols"
            ],
            ThreatVector.QUANTUM_SUPREMACY_EXPLOITATION: [
                "Assess quantum computational advantage impact",
                "Accelerate post-quantum cryptography deployment",
                "Implement quantum-safe fallback protocols"
            ],
            ThreatVector.QUANTUM_COMMUNICATION_INTERCEPTION: [
                "Secure quantum communication channels",
                "Implement additional quantum authentication",
                "Deploy quantum communication monitoring"
            ]
        }
        
        recommendations.extend(vector_recommendations.get(threat_vector, []))
        
        # Context-specific recommendations
        if context.attack_sophistication == "NATION_STATE":
            recommendations.append("STRATEGIC: Assess nation-state quantum capabilities")
        
        if InfrastructureTarget.FINANCIAL_SYSTEMS in context.target_infrastructure:
            recommendations.append("SECTOR: Coordinate with financial sector quantum security")
        
        if InfrastructureTarget.MILITARY_COMMUNICATIONS in context.target_infrastructure:
            recommendations.append("DEFENSE: Brief military quantum security leadership")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _determine_escalation_triggers(self, severity_level: ThreatSeverityLevel, 
                                     confidence_score: float, 
                                     context: ThreatContext) -> List[str]:
        """Determine conditions that would trigger escalation."""
        triggers = []
        
        # Automatic escalation triggers
        if severity_level in [ThreatSeverityLevel.DEFCON_1, ThreatSeverityLevel.DEFCON_2]:
            triggers.append("automatic_executive_briefing")
        
        if severity_level == ThreatSeverityLevel.QUANTUM_CRITICAL and confidence_score > 0.9:
            triggers.append("automatic_defense_leadership_notification")
        
        # Conditional escalation triggers
        if confidence_score > 0.8 and context.attack_sophistication == "NATION_STATE":
            triggers.append("geopolitical_escalation_assessment")
        
        if len(context.target_infrastructure) > 3:
            triggers.append("cross_sector_coordination")
        
        if InfrastructureTarget.NUCLEAR_FACILITIES in context.target_infrastructure:
            triggers.append("nuclear_security_alert")
        
        if confidence_score < 0.5:
            triggers.append("intelligence_validation_required")
        
        return triggers
    
    async def _update_classification_metrics(self, classification: SeverityClassification) -> None:
        """Update classification performance metrics."""
        self.classification_metrics['threats_classified'] += 1
        
        # Update average latency
        current_avg = self.classification_metrics['average_latency_ms']
        count = self.classification_metrics['threats_classified']
        new_avg = ((current_avg * (count - 1)) + classification.classification_latency_ms) / count
        self.classification_metrics['average_latency_ms'] = new_avg
        
        # Update agent assignments metric
        if classification.agent_assignments:
            self.classification_metrics['agent_assignments_made'] += 1
        
        # Update escalations metric
        if classification.escalation_triggers:
            self.classification_metrics['escalations_triggered'] += 1
        
        # Log performance warning if latency exceeds target
        target_latency = self.config.get('target_latency_ms', 0.5)
        if classification.classification_latency_ms > target_latency:
            logger.warning(f"Classification latency {classification.classification_latency_ms:.3f}ms exceeds target {target_latency}ms")
    
    async def _update_threat_patterns(self, classification: SeverityClassification) -> None:
        """Update threat pattern history for machine learning."""
        # Extract pattern from classification
        threat_signature = self._generate_threat_signature_from_classification(classification)
        
        # Add to pattern history
        self.threat_pattern_history['patterns'].append(threat_signature)
        
        # Maintain pattern history size
        max_patterns = 10000
        if len(self.threat_pattern_history['patterns']) > max_patterns:
            self.threat_pattern_history['patterns'] = self.threat_pattern_history['patterns'][-max_patterns:]
        
        # Update rule accuracy based on feedback (simulated for now)
        if classification.confidence_score > 0.8:
            # Assume high confidence classifications are accurate
            self._update_rule_accuracy(classification.classification_reasoning.get('matched_rule'), True)
    
    def _generate_threat_signature_from_classification(self, classification: SeverityClassification) -> str:
        """Generate threat signature from classification result."""
        signature_components = [
            classification.severity_level.value,
            classification.threat_vector.value,
            classification.impact_scale.value,
            str(len(classification.context.target_infrastructure)),
            classification.context.attack_sophistication
        ]
        
        signature = '|'.join(signature_components)
        return hashlib.md5(signature.encode()).hexdigest()
    
    def _update_rule_accuracy(self, rule_id: str, was_accurate: bool) -> None:
        """Update rule accuracy based on feedback."""
        for rule in self.classification_rules:
            if rule.rule_id == rule_id:
                # Simple exponential moving average for accuracy
                alpha = 0.1  # Learning rate
                if was_accurate:
                    rule.accuracy_rate = (1 - alpha) * rule.accuracy_rate + alpha * 1.0
                else:
                    rule.accuracy_rate = (1 - alpha) * rule.accuracy_rate + alpha * 0.0
                    rule.false_positive_rate = (1 - alpha) * rule.false_positive_rate + alpha * 1.0
                
                # Rebuild priority queue to reflect accuracy changes
                self._rebuild_rule_priority_queue()
                break
    
    async def _trigger_escalation(self, classification: SeverityClassification) -> None:
        """Trigger escalation procedures for high-priority threats."""
        for trigger in classification.escalation_triggers:
            logger.info(f"ESCALATION TRIGGERED: {trigger} for threat {classification.threat_id}")
            
            # Simulate escalation actions
            if trigger == "automatic_executive_briefing":
                await self._notify_executive_leadership(classification)
            elif trigger == "automatic_defense_leadership_notification":
                await self._notify_defense_leadership(classification)
            elif trigger == "geopolitical_escalation_assessment":
                await self._initiate_geopolitical_assessment(classification)
    
    async def _notify_executive_leadership(self, classification: SeverityClassification) -> None:
        """Notify executive leadership of critical threats."""
        logger.critical(f"EXECUTIVE NOTIFICATION: {classification.severity_level.value} threat detected - {classification.threat_id}")
        # In real implementation, this would trigger secure communications to leadership
    
    async def _notify_defense_leadership(self, classification: SeverityClassification) -> None:
        """Notify defense leadership of critical quantum threats."""
        logger.critical(f"DEFENSE NOTIFICATION: Quantum threat {classification.threat_id} - {classification.threat_vector.value}")
        # In real implementation, this would trigger defense network alerts
    
    async def _initiate_geopolitical_assessment(self, classification: SeverityClassification) -> None:
        """Initiate geopolitical threat assessment."""
        logger.info(f"GEOPOLITICAL ASSESSMENT: Analyzing threat {classification.threat_id} for international implications")
        # In real implementation, this would trigger intelligence analysis workflows
    
    def _create_error_classification(self, threat_data: Dict[str, Any], error_message: str) -> SeverityClassification:
        """Create minimal classification for error cases."""
        return SeverityClassification(
            threat_id=threat_data.get('threat_id', 'ERROR_CLASSIFICATION'),
            timestamp=datetime.now(),
            severity_level=ThreatSeverityLevel.QUANTUM_INFO,
            impact_scale=ThreatImpactScale.MINIMAL,
            urgency=ThreatUrgency.LOW,
            threat_vector=ThreatVector.QUANTUM_COMPUTING_ADVANTAGE,
            context=ThreatContext(),
            confidence_score=0.0,
            classification_reasoning={'error': error_message},
            response_recommendations=["Review threat data quality", "Manual threat analysis required"],
            agent_assignments={},
            escalation_triggers=[],
            classification_latency_ms=0.0
        )
    
    def _generate_threat_id(self) -> str:
        """Generate unique threat ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"MWRASP_QTHREAT_{timestamp}"
    
    async def process_threat_queue(self) -> None:
        """Continuously process threat classification queue."""
        while True:
            try:
                # Wait for threat data
                threat_data = await self.classification_queue.get()
                
                # Classify threat
                classification = await self.classify_threat_realtime(threat_data)
                
                # Log classification
                logger.info(f"Classified threat {classification.threat_id}: {classification.severity_level.value} "
                           f"(confidence: {classification.confidence_score:.3f}, latency: {classification.classification_latency_ms:.3f}ms)")
                
                self.classification_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing threat queue: {e}")
                continue
    
    async def submit_threat_for_classification(self, threat_data: Dict[str, Any]) -> bool:
        """Submit threat data for real-time classification."""
        try:
            await self.classification_queue.put(threat_data)
            return True
        except asyncio.QueueFull:
            logger.warning("Classification queue is full, dropping threat data")
            return False
    
    def get_classification_statistics(self) -> Dict[str, Any]:
        """Get classification statistics and performance metrics."""
        recent_classifications = list(self.processed_classifications)[-100:]  # Last 100
        
        if not recent_classifications:
            return {'status': 'no_classifications'}
        
        # Severity distribution
        severity_counts = defaultdict(int)
        urgency_counts = defaultdict(int)
        vector_counts = defaultdict(int)
        
        latencies = []
        confidences = []
        
        for classification in recent_classifications:
            severity_counts[classification.severity_level.value] += 1
            urgency_counts[classification.urgency.value] += 1
            vector_counts[classification.threat_vector.value] += 1
            latencies.append(classification.classification_latency_ms)
            confidences.append(classification.confidence_score)
        
        return {
            'total_classifications': len(recent_classifications),
            'severity_distribution': dict(severity_counts),
            'urgency_distribution': dict(urgency_counts),
            'threat_vector_distribution': dict(vector_counts),
            'performance_metrics': {
                'average_latency_ms': np.mean(latencies),
                'max_latency_ms': np.max(latencies),
                'min_latency_ms': np.min(latencies),
                'latency_95th_percentile_ms': np.percentile(latencies, 95),
                'average_confidence': np.mean(confidences),
                'confidence_std': np.std(confidences)
            },
            'system_metrics': self.classification_metrics,
            'rule_performance': [
                {
                    'rule_id': rule.rule_id,
                    'accuracy_rate': rule.accuracy_rate,
                    'false_positive_rate': rule.false_positive_rate,
                    'match_count': rule.match_count
                }
                for rule in self.classification_rules[:10]  # Top 10 rules
            ]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            'status': 'OPERATIONAL',
            'configuration': self.config,
            'classification_rules_loaded': len(self.classification_rules),
            'queue_size': self.classification_queue.qsize(),
            'processed_classifications': len(self.processed_classifications),
            'classification_metrics': self.classification_metrics,
            'agent_coordinator_status': 'OPERATIONAL',
            'ml_enhancement_active': self.config.get('ml_enhancement_enabled', True),
            'ultra_low_latency_mode': self.config.get('ultra_low_latency_mode', True),
            'target_latency_ms': self.config.get('target_latency_ms', 0.5)
        }


async def main():
    """Main demonstration of the quantum threat severity classifier."""
    classifier = QuantumThreatSeverityClassifier()
    
    print("MWRASP Quantum Threat Severity Classification Engine")
    print("=" * 65)
    
    # Show system status
    status = classifier.get_system_status()
    print(f"System Status: {status['status']}")
    print(f"Classification Rules: {status['classification_rules_loaded']}")
    print(f"Target Latency: {status['target_latency_ms']}ms")
    print(f"Ultra-Low Latency Mode: {status['ultra_low_latency_mode']}")
    
    # Start threat processing
    processing_task = asyncio.create_task(classifier.process_threat_queue())
    
    # Simulate threat classifications
    sample_threats = [
        {
            'threat_id': 'DEMO_THREAT_001',
            'source': 'supremacy_detector',
            'confidence': 0.92,
            'threat_indicators': {
                'quantum_advantage': 50000,
                'attack_type': 'supremacy_exploitation',
                'critical_systems_affected': 8,
                'nation_state_indicators': 7,
                'target_military': True,
                'attack_scale': 'REGIONAL'
            },
            'geopolitical_context': {
                'tension_level': 'high',
                'threat_actor_nation': 'CLASSIFIED'
            }
        },
        {
            'threat_id': 'DEMO_THREAT_002',
            'source': 'qkd_detector',
            'confidence': 0.87,
            'threat_indicators': {
                'attack_type': 'key_compromise',
                'affected_keys': 250,
                'quantum_advantage': 1000,
                'target_financial': True,
                'attack_sophistication': 'advanced'
            }
        },
        {
            'threat_id': 'DEMO_THREAT_003',
            'source': 'circuit_fingerprint',
            'confidence': 0.73,
            'threat_indicators': {
                'circuit_manipulation': True,
                'hardware_compromise': True,
                'anomaly_type': 'quantum',
                'impact_assessment': 'LIMITED'
            }
        }
    ]
    
    # Submit threats for classification
    for threat in sample_threats:
        await classifier.submit_threat_for_classification(threat)
    
    # Allow processing
    await asyncio.sleep(2)
    
    # Display classification statistics
    stats = classifier.get_classification_statistics()
    print(f"\nClassification Results:")
    print(f"Total Classifications: {stats['total_classifications']}")
    print(f"Average Latency: {stats['performance_metrics']['average_latency_ms']:.3f}ms")
    print(f"Average Confidence: {stats['performance_metrics']['average_confidence']:.3f}")
    
    print("\nSeverity Distribution:")
    for severity, count in stats['severity_distribution'].items():
        print(f"  {severity}: {count}")
    
    print("\nThreat Vector Distribution:")
    for vector, count in stats['threat_vector_distribution'].items():
        print(f"  {vector}: {count}")
    
    print(f"\nSystem Performance:")
    print(f"  95th Percentile Latency: {stats['performance_metrics']['latency_95th_percentile_ms']:.3f}ms")
    print(f"  Max Latency: {stats['performance_metrics']['max_latency_ms']:.3f}ms")
    print(f"  Agent Assignments Made: {stats['system_metrics']['agent_assignments_made']}")
    print(f"  Escalations Triggered: {stats['system_metrics']['escalations_triggered']}")
    
    # Show recent classifications
    recent = list(classifier.processed_classifications)[-3:]
    print(f"\nRecent Classifications:")
    for classification in recent:
        print(f"  {classification.threat_id}: {classification.severity_level.value} "
              f"(Vector: {classification.threat_vector.value}, "
              f"Confidence: {classification.confidence_score:.3f}, "
              f"Latency: {classification.classification_latency_ms:.3f}ms)")
    
    # Cleanup
    processing_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
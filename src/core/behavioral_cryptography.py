"""
MWRASP Behavioral Cryptography System
Using agent behaviors and protocol presentation order as authentication mechanisms
"""

import time
import hashlib
import secrets
import random
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import json


class SecurityProtocol(Enum):
    """Available security protocols an agent can offer"""
    AES_256_GCM = "aes_256_gcm"
    CHACHA20_POLY1305 = "chacha20_poly1305"
    RSA_4096 = "rsa_4096"
    ECDSA_P521 = "ecdsa_p521"
    KYBER_1024 = "kyber_1024"  # Post-quantum
    DILITHIUM_5 = "dilithium_5"  # Post-quantum
    SPHINCS_256 = "sphincs_256"  # Post-quantum
    FALCON_1024 = "falcon_1024"  # Post-quantum
    NTRU_HPS4096 = "ntru_hps4096"  # Post-quantum
    RAINBOW_V = "rainbow_v"  # Post-quantum
    BLAKE3 = "blake3"
    SHA3_512 = "sha3_512"
    ARGON2ID = "argon2id"
    SCRYPT = "scrypt"
    PBKDF2 = "pbkdf2"


class AgentRole(Enum):
    """Agent roles that affect protocol preferences"""
    MONITOR = "monitor"
    DEFENDER = "defender"
    ANALYZER = "analyzer"
    COORDINATOR = "coordinator"
    RECOVERY = "recovery"
    INFILTRATOR = "infiltrator"
    DIPLOMAT = "diplomat"
    SCOUT = "scout"


class SituationalContext(Enum):
    """Situations that affect protocol presentation order"""
    NORMAL_OPERATION = "normal"
    UNDER_ATTACK = "attack"
    STEALTH_MODE = "stealth"
    EMERGENCY_RESPONSE = "emergency"
    MAINTENANCE = "maintenance"
    INVESTIGATION = "investigation"
    NEGOTIATION = "negotiation"
    DATA_EXFILTRATION = "exfiltration"


@dataclass
class ProtocolPreference:
    """How an agent prefers to use protocols"""
    protocol: SecurityProtocol
    base_priority: int  # 1-10, higher is more preferred
    role_modifiers: Dict[AgentRole, float]  # Role-specific preference multipliers
    context_modifiers: Dict[SituationalContext, float]  # Context-specific multipliers
    usage_count: int = 0
    success_rate: float = 1.0
    last_used: Optional[float] = None
    
    def calculate_priority(self, role: AgentRole, context: SituationalContext) -> float:
        """Calculate actual priority based on role and context"""
        priority = self.base_priority
        priority *= self.role_modifiers.get(role, 1.0)
        priority *= self.context_modifiers.get(context, 1.0)
        priority *= self.success_rate  # Prefer successful protocols
        
        # Recently used protocols get slight penalty to increase variety
        if self.last_used and (time.time() - self.last_used) < 60:
            priority *= 0.9
        
        return priority


@dataclass
class BehavioralSignature:
    """Unique behavioral patterns for an agent"""
    agent_id: str
    role: AgentRole
    
    # Protocol preferences (stored order)
    protocol_inventory: List[ProtocolPreference]
    
    # Behavioral patterns
    timing_patterns: List[float]  # Typical response times
    verbosity_level: int  # 1-10, how much info they share
    interaction_tempo: float  # Speed of back-and-forth
    protocol_switching_frequency: float  # How often they change protocols
    
    # Presentation rules based on context
    presentation_rules: Dict[SituationalContext, str]  # Context -> ordering algorithm
    
    # Behavioral quirks
    quirks: List[str]  # Unique behaviors
    tells: List[str]  # Subtle giveaways when stressed
    
    # Memory of interactions
    interaction_history: deque = field(default_factory=lambda: deque(maxlen=100))
    protocol_sequence_memory: deque = field(default_factory=lambda: deque(maxlen=20))
    
    def get_protocol_presentation_order(self, context: SituationalContext, 
                                       partner_id: str, interaction_count: int) -> List[SecurityProtocol]:
        """
        Get the order to present protocols based on context and interaction history.
        This is the KEY INNOVATION - the order itself is the authentication.
        """
        
        # Get the presentation algorithm for this context
        algorithm = self.presentation_rules.get(context, "default")
        
        # Start with base inventory
        protocols = [p.protocol for p in self.protocol_inventory]
        
        # Apply ordering algorithm based on context and rules
        if algorithm == "reverse":
            # Under attack - reverse normal order
            protocols = list(reversed(protocols))
            
        elif algorithm == "priority_weighted":
            # Normal operation - sort by calculated priority
            sorted_prefs = sorted(
                self.protocol_inventory,
                key=lambda p: p.calculate_priority(self.role, context),
                reverse=True
            )
            protocols = [p.protocol for p in sorted_prefs]
            
        elif algorithm == "fibonacci_shuffle":
            # Stealth mode - use Fibonacci sequence for positions
            fib = [1, 1, 2, 3, 5, 8, 13]
            shuffled = []
            for i in fib:
                if i <= len(protocols):
                    shuffled.append(protocols[i-1])
            # Add remaining protocols
            for p in protocols:
                if p not in shuffled:
                    shuffled.append(p)
            protocols = shuffled
            
        elif algorithm == "partner_dependent":
            # Order depends on partner ID hash
            partner_hash = int(hashlib.md5(partner_id.encode()).hexdigest(), 16)
            random.Random(partner_hash).shuffle(protocols)
            
        elif algorithm == "interaction_modulo":
            # Order based on interaction count
            rotation = interaction_count % len(protocols)
            protocols = protocols[rotation:] + protocols[:rotation]
            
        elif algorithm == "temporal":
            # Order based on current time
            time_seed = int(time.time() / 300)  # Changes every 5 minutes
            random.Random(time_seed).shuffle(protocols)
            
        elif algorithm == "role_paired":
            # Specific ordering when talking to specific roles
            # Defenders talk to Monitors differently than to other Defenders
            if self.role == AgentRole.DEFENDER:
                # Put defensive protocols first
                defensive = [SecurityProtocol.AES_256_GCM, SecurityProtocol.CHACHA20_POLY1305]
                protocols = [p for p in defensive if p in protocols]
                protocols += [p for p in protocols if p not in defensive]
                
        elif algorithm == "stress_response":
            # Emergency - only show most critical protocols
            protocols = protocols[:5]
            
        else:  # "default"
            # Keep stored order
            pass
        
        # Record the sequence we're using
        self.protocol_sequence_memory.append({
            'timestamp': time.time(),
            'context': context.value,
            'partner': partner_id,
            'sequence': [p.value for p in protocols]
        })
        
        return protocols
    
    def verify_protocol_response_order(self, presented_order: List[SecurityProtocol],
                                      expected_context: SituationalContext,
                                      partner_id: str, interaction_count: int) -> Tuple[bool, float]:
        """
        Verify if the presented order matches what we expect for this context.
        Returns (is_valid, confidence_score)
        """
        
        expected_order = self.get_protocol_presentation_order(
            expected_context, partner_id, interaction_count
        )
        
        # Exact match is highest confidence
        if presented_order == expected_order:
            return True, 1.0
        
        # Check if it's a valid variation (some tolerance for network delays, etc.)
        # Calculate similarity score
        similarity = self._calculate_sequence_similarity(presented_order, expected_order)
        
        # If similarity is high enough, might be legitimate with some deviation
        if similarity > 0.8:
            return True, similarity
        
        # Check if they might be using a different context interpretation
        # Try other contexts to see if any match
        for alt_context in SituationalContext:
            alt_order = self.get_protocol_presentation_order(
                alt_context, partner_id, interaction_count
            )
            if presented_order == alt_order:
                # They think we're in a different situation
                # This itself might be suspicious
                return False, 0.3  # Low confidence, wrong context
        
        # Doesn't match any expected pattern - likely imposter
        return False, similarity
    
    def _calculate_sequence_similarity(self, seq1: List[SecurityProtocol], 
                                      seq2: List[SecurityProtocol]) -> float:
        """Calculate how similar two protocol sequences are"""
        
        if not seq1 or not seq2:
            return 0.0
        
        # Check common elements
        set1, set2 = set(seq1), set(seq2)
        if set1 != set2:
            # Different protocols included - suspicious
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            jaccard = intersection / union if union > 0 else 0
            return jaccard * 0.5  # Penalize heavily for different protocols
        
        # Same protocols, check ordering (Kendall tau correlation)
        matches = 0
        comparisons = 0
        
        for i in range(len(seq1)):
            for j in range(i + 1, len(seq1)):
                if seq1[i] in seq2 and seq1[j] in seq2:
                    idx1_in_seq2 = seq2.index(seq1[i])
                    idx2_in_seq2 = seq2.index(seq1[j])
                    
                    # Check if relative order is preserved
                    if (idx1_in_seq2 < idx2_in_seq2) == (i < j):
                        matches += 1
                    comparisons += 1
        
        if comparisons == 0:
            return 1.0
        
        return matches / comparisons


class BehavioralAuthenticator:
    """System for authenticating agents through behavioral patterns"""
    
    def __init__(self):
        self.agent_signatures: Dict[str, BehavioralSignature] = {}
        self.interaction_logs: List[Dict] = []
        self.impostor_detections: List[Dict] = []
        
    def create_agent_signature(self, agent_id: str, role: AgentRole) -> BehavioralSignature:
        """Create a unique behavioral signature for an agent"""
        
        # Create protocol inventory with role-specific preferences
        protocols = self._generate_protocol_inventory(role)
        
        # Generate unique behavioral patterns
        timing_patterns = [
            random.gauss(100, 20) for _ in range(10)  # Response times in ms
        ]
        
        # Create context-specific presentation rules
        presentation_rules = self._generate_presentation_rules(role)
        
        # Generate quirks based on role
        quirks = self._generate_quirks(role)
        tells = self._generate_tells(role)
        
        signature = BehavioralSignature(
            agent_id=agent_id,
            role=role,
            protocol_inventory=protocols,
            timing_patterns=timing_patterns,
            verbosity_level=random.randint(3, 8),
            interaction_tempo=random.uniform(0.5, 2.0),
            protocol_switching_frequency=random.uniform(0.1, 0.5),
            presentation_rules=presentation_rules,
            quirks=quirks,
            tells=tells
        )
        
        self.agent_signatures[agent_id] = signature
        return signature
    
    def _generate_protocol_inventory(self, role: AgentRole) -> List[ProtocolPreference]:
        """Generate protocol preferences based on role"""
        
        all_protocols = list(SecurityProtocol)
        inventory = []
        
        for protocol in all_protocols:
            # Base priority varies by role
            if role == AgentRole.DEFENDER:
                # Defenders prefer strong encryption
                if "aes" in protocol.value or "chacha" in protocol.value:
                    base_priority = random.randint(7, 10)
                else:
                    base_priority = random.randint(3, 6)
                    
            elif role == AgentRole.MONITOR:
                # Monitors prefer fast protocols
                if "blake" in protocol.value or "sha" in protocol.value:
                    base_priority = random.randint(7, 10)
                else:
                    base_priority = random.randint(4, 7)
                    
            elif role == AgentRole.INFILTRATOR:
                # Infiltrators prefer stealthy protocols
                if "ecdsa" in protocol.value or "falcon" in protocol.value:
                    base_priority = random.randint(6, 9)
                else:
                    base_priority = random.randint(3, 6)
            else:
                base_priority = random.randint(4, 7)
            
            # Create role modifiers
            role_modifiers = {}
            for r in AgentRole:
                if r == role:
                    role_modifiers[r] = random.uniform(1.2, 1.5)
                else:
                    role_modifiers[r] = random.uniform(0.8, 1.1)
            
            # Create context modifiers
            context_modifiers = {}
            for c in SituationalContext:
                if c == SituationalContext.UNDER_ATTACK:
                    # Under attack, prefer fast and strong
                    if "quantum" in protocol.value.lower():
                        context_modifiers[c] = 1.5
                    else:
                        context_modifiers[c] = 1.0
                elif c == SituationalContext.STEALTH_MODE:
                    # Stealth prefers lightweight
                    if "ecdsa" in protocol.value or "blake" in protocol.value:
                        context_modifiers[c] = 1.3
                    else:
                        context_modifiers[c] = 0.9
                else:
                    context_modifiers[c] = random.uniform(0.9, 1.1)
            
            pref = ProtocolPreference(
                protocol=protocol,
                base_priority=base_priority,
                role_modifiers=role_modifiers,
                context_modifiers=context_modifiers
            )
            inventory.append(pref)
        
        return inventory
    
    def _generate_presentation_rules(self, role: AgentRole) -> Dict[SituationalContext, str]:
        """Generate context-specific presentation rules"""
        
        rules = {}
        
        # Each role has different strategies
        if role == AgentRole.DEFENDER:
            rules[SituationalContext.NORMAL_OPERATION] = "priority_weighted"
            rules[SituationalContext.UNDER_ATTACK] = "reverse"
            rules[SituationalContext.STEALTH_MODE] = "fibonacci_shuffle"
            rules[SituationalContext.EMERGENCY_RESPONSE] = "stress_response"
            rules[SituationalContext.INVESTIGATION] = "partner_dependent"
            
        elif role == AgentRole.MONITOR:
            rules[SituationalContext.NORMAL_OPERATION] = "default"
            rules[SituationalContext.UNDER_ATTACK] = "temporal"
            rules[SituationalContext.STEALTH_MODE] = "partner_dependent"
            rules[SituationalContext.INVESTIGATION] = "interaction_modulo"
            
        elif role == AgentRole.INFILTRATOR:
            rules[SituationalContext.NORMAL_OPERATION] = "fibonacci_shuffle"
            rules[SituationalContext.STEALTH_MODE] = "interaction_modulo"
            rules[SituationalContext.DATA_EXFILTRATION] = "reverse"
            rules[SituationalContext.NEGOTIATION] = "partner_dependent"
            
        else:
            # Default rules
            rules[SituationalContext.NORMAL_OPERATION] = "priority_weighted"
            rules[SituationalContext.UNDER_ATTACK] = "reverse"
            rules[SituationalContext.STEALTH_MODE] = "temporal"
        
        # Fill in any missing contexts with defaults
        for context in SituationalContext:
            if context not in rules:
                rules[context] = "default"
        
        return rules
    
    def _generate_quirks(self, role: AgentRole) -> List[str]:
        """Generate behavioral quirks based on role"""
        
        quirk_pool = {
            AgentRole.DEFENDER: [
                "always_verifies_twice",
                "prefers_even_numbered_ports",
                "adds_salt_to_everything",
                "paranoid_about_timing_attacks"
            ],
            AgentRole.MONITOR: [
                "logs_everything_three_times",
                "likes_prime_number_intervals",
                "always_checks_neighbors_first",
                "obsessed_with_patterns"
            ],
            AgentRole.INFILTRATOR: [
                "changes_identity_frequently",
                "mimics_other_agents",
                "prefers_night_operations",
                "uses_dead_drops"
            ],
            AgentRole.ANALYZER: [
                "overthinks_simple_problems",
                "creates_nested_hypotheses",
                "questions_own_conclusions",
                "seeks_third_opinions"
            ]
        }
        
        role_quirks = quirk_pool.get(role, ["generic_quirk"])
        
        # Select 2-3 random quirks
        num_quirks = random.randint(2, 3)
        return random.sample(role_quirks, min(num_quirks, len(role_quirks)))
    
    def _generate_tells(self, role: AgentRole) -> List[str]:
        """Generate stress tells based on role"""
        
        tells_pool = {
            AgentRole.DEFENDER: [
                "increases_encryption_rounds",
                "shortens_timeout_windows",
                "double_checks_signatures"
            ],
            AgentRole.MONITOR: [
                "increases_sampling_rate",
                "broadens_search_scope",
                "correlates_unrelated_events"
            ],
            AgentRole.INFILTRATOR: [
                "changes_communication_style",
                "increases_cover_story_details",
                "avoids_direct_questions"
            ]
        }
        
        role_tells = tells_pool.get(role, ["generic_tell"])
        return random.sample(role_tells, min(2, len(role_tells)))
    
    def authenticate_interaction(self, sender_id: str, receiver_id: str,
                                presented_protocols: List[SecurityProtocol],
                                claimed_context: SituationalContext,
                                interaction_metadata: Dict) -> Tuple[bool, float, str]:
        """
        Authenticate an interaction based on behavioral patterns.
        Returns: (is_authentic, confidence, reason)
        """
        
        sender_sig = self.agent_signatures.get(sender_id)
        receiver_sig = self.agent_signatures.get(receiver_id)
        
        if not sender_sig:
            return False, 0.0, "Unknown sender"
        
        if not receiver_sig:
            return False, 0.0, "Unknown receiver"
        
        # Get interaction count between these agents
        interaction_count = self._get_interaction_count(sender_id, receiver_id)
        
        # Verify protocol presentation order
        is_valid, confidence = sender_sig.verify_protocol_response_order(
            presented_protocols,
            claimed_context,
            receiver_id,
            interaction_count
        )
        
        # Check timing patterns
        response_time = interaction_metadata.get('response_time_ms', 100)
        expected_mean = sum(sender_sig.timing_patterns) / len(sender_sig.timing_patterns)
        expected_std = (sum((x - expected_mean)**2 for x in sender_sig.timing_patterns) / len(sender_sig.timing_patterns))**0.5
        
        # Check if response time is within expected range (3 standard deviations)
        if abs(response_time - expected_mean) > 3 * expected_std:
            confidence *= 0.7  # Reduce confidence for unusual timing
            
        # Check for tells under stress
        if claimed_context in [SituationalContext.UNDER_ATTACK, SituationalContext.EMERGENCY_RESPONSE]:
            # Should exhibit tells
            exhibited_tells = interaction_metadata.get('behavioral_indicators', [])
            expected_tells = sender_sig.tells
            
            tell_match = len(set(exhibited_tells) & set(expected_tells))
            if tell_match == 0:
                # No expected tells under stress - suspicious
                confidence *= 0.5
        
        # Check quirks for consistency
        exhibited_quirks = interaction_metadata.get('quirks', [])
        expected_quirks = sender_sig.quirks
        
        quirk_consistency = len(set(exhibited_quirks) & set(expected_quirks)) / max(len(expected_quirks), 1)
        confidence *= (0.5 + 0.5 * quirk_consistency)  # Quirks affect 50% of confidence
        
        # Record interaction
        self.interaction_logs.append({
            'timestamp': time.time(),
            'sender': sender_id,
            'receiver': receiver_id,
            'context': claimed_context.value,
            'protocols_presented': [p.value for p in presented_protocols],
            'authenticated': is_valid,
            'confidence': confidence
        })
        
        # Update interaction count
        sender_sig.interaction_history.append({
            'partner': receiver_id,
            'timestamp': time.time(),
            'success': is_valid
        })
        
        # Determine reason
        if not is_valid:
            reason = "Protocol sequence mismatch - possible impostor"
            self.impostor_detections.append({
                'timestamp': time.time(),
                'claimed_id': sender_id,
                'receiver_id': receiver_id,
                'confidence': 1.0 - confidence
            })
        elif confidence < 0.5:
            reason = "Low confidence - behavioral anomalies detected"
        elif confidence < 0.8:
            reason = "Moderate confidence - minor deviations detected"
        else:
            reason = "High confidence authentication"
        
        return is_valid and confidence > 0.3, confidence, reason
    
    def _get_interaction_count(self, agent1_id: str, agent2_id: str) -> int:
        """Get the number of previous interactions between two agents"""
        
        count = 0
        if agent1_id in self.agent_signatures:
            sig = self.agent_signatures[agent1_id]
            count = sum(1 for h in sig.interaction_history if h['partner'] == agent2_id)
        
        return count
    
    def demonstrate_impostor_detection(self):
        """Demonstrate how the system detects impostors"""
        
        print("=== Behavioral Cryptography Demonstration ===\n")
        
        # Create legitimate agents
        defender = self.create_agent_signature("DEFENDER_001", AgentRole.DEFENDER)
        monitor = self.create_agent_signature("MONITOR_001", AgentRole.MONITOR)
        
        # Simulate normal interaction
        print("1. NORMAL INTERACTION - Defender talking to Monitor")
        context = SituationalContext.NORMAL_OPERATION
        
        # Defender presents protocols in correct order
        correct_order = defender.get_protocol_presentation_order(
            context, "MONITOR_001", 0
        )
        
        print(f"   Context: {context.value}")
        print(f"   Protocols presented: {[p.value for p in correct_order[:5]]}...")
        
        # Authenticate
        is_authentic, confidence, reason = self.authenticate_interaction(
            "DEFENDER_001",
            "MONITOR_001",
            correct_order,
            context,
            {
                'response_time_ms': 95,
                'quirks': defender.quirks[:1],
                'behavioral_indicators': []
            }
        )
        
        print(f"   Authentication: {'SUCCESS' if is_authentic else 'FAILED'}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Reason: {reason}\n")
        
        # Simulate impostor attempt
        print("2. IMPOSTOR ATTEMPT - Fake Defender with observed protocols")
        
        # Impostor uses the same protocols but wrong order (doesn't know the algorithm)
        impostor_order = list(correct_order)
        random.shuffle(impostor_order)  # Wrong order!
        
        print(f"   Context claimed: {context.value}")
        print(f"   Protocols presented: {[p.value for p in impostor_order[:5]]}...")
        
        # Try to authenticate
        is_authentic, confidence, reason = self.authenticate_interaction(
            "DEFENDER_001",  # Claiming to be defender
            "MONITOR_001",
            impostor_order,
            context,
            {
                'response_time_ms': 95,
                'quirks': ["generic_quirk"],  # Wrong quirks
                'behavioral_indicators': []
            }
        )
        
        print(f"   Authentication: {'SUCCESS' if is_authentic else 'FAILED'}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Reason: {reason}\n")
        
        # Simulate emergency with correct tells
        print("3. EMERGENCY SITUATION - Defender under attack")
        emergency_context = SituationalContext.UNDER_ATTACK
        
        # Get emergency protocol order (should be different)
        emergency_order = defender.get_protocol_presentation_order(
            emergency_context, "MONITOR_001", 1
        )
        
        print(f"   Context: {emergency_context.value}")
        print(f"   Protocols presented: {[p.value for p in emergency_order[:5]]}...")
        print(f"   Exhibited tells: {defender.tells}")
        
        # Authenticate with tells
        is_authentic, confidence, reason = self.authenticate_interaction(
            "DEFENDER_001",
            "MONITOR_001",
            emergency_order,
            emergency_context,
            {
                'response_time_ms': 75,  # Faster under stress
                'quirks': defender.quirks,
                'behavioral_indicators': defender.tells  # Showing stress tells
            }
        )
        
        print(f"   Authentication: {'SUCCESS' if is_authentic else 'FAILED'}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Reason: {reason}\n")
        
        # Show impostor detection log
        if self.impostor_detections:
            print("4. IMPOSTOR DETECTION LOG:")
            for detection in self.impostor_detections:
                print(f"   - Claimed ID: {detection['claimed_id']}")
                print(f"     Target: {detection['receiver_id']}")
                print(f"     Detection confidence: {detection['confidence']:.2%}\n")


# Advanced behavioral patterns
class AdvancedBehavioralPatterns:
    """Additional behavioral cryptography patterns"""
    
    @staticmethod
    def generate_typing_cadence(agent_id: str) -> List[float]:
        """Generate unique typing/transmission cadence for an agent"""
        
        # Each agent has unique rhythm
        seed = int(hashlib.sha256(agent_id.encode()).hexdigest(), 16)
        random.Random(seed).seed(seed)
        
        # Generate inter-keystroke intervals (in ms)
        base_speed = random.Random(seed).uniform(50, 200)
        cadence = []
        
        for _ in range(20):
            # Natural variation in typing speed
            interval = random.Random(seed).gauss(base_speed, base_speed * 0.2)
            cadence.append(max(10, interval))  # Minimum 10ms
        
        return cadence
    
    @staticmethod
    def generate_vocabulary_signature(role: AgentRole) -> Dict[str, float]:
        """Generate vocabulary preferences based on role"""
        
        vocab = {}
        
        if role == AgentRole.DEFENDER:
            vocab = {
                "threat": 0.8, "secure": 0.9, "protect": 0.85,
                "block": 0.7, "firewall": 0.6, "scan": 0.75
            }
        elif role == AgentRole.MONITOR:
            vocab = {
                "observe": 0.9, "detect": 0.85, "anomaly": 0.8,
                "pattern": 0.75, "baseline": 0.7, "alert": 0.8
            }
        elif role == AgentRole.INFILTRATOR:
            vocab = {
                "stealth": 0.9, "covert": 0.85, "bypass": 0.8,
                "disguise": 0.75, "penetrate": 0.7, "exfiltrate": 0.8
            }
        
        return vocab
    
    @staticmethod
    def calculate_message_entropy(message: str) -> float:
        """Calculate entropy of a message (randomness measure)"""
        
        if not message:
            return 0.0
        
        # Character frequency
        freq = {}
        for char in message:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        msg_len = len(message)
        
        for count in freq.values():
            probability = count / msg_len
            if probability > 0:
                entropy -= probability * (probability and (probability).bit_length())
        
        return entropy
    
    @staticmethod
    def generate_decision_timing_pattern(agent_id: str) -> Dict[str, float]:
        """Generate decision-making timing patterns"""
        
        seed = int(hashlib.sha256(agent_id.encode()).hexdigest(), 16)
        rng = random.Random(seed)
        
        return {
            "simple_decision_ms": rng.uniform(10, 50),
            "complex_decision_ms": rng.uniform(100, 500),
            "critical_decision_ms": rng.uniform(200, 1000),
            "hesitation_factor": rng.uniform(1.0, 2.0),  # Under uncertainty
            "confidence_factor": rng.uniform(0.5, 0.9)   # When confident
        }


if __name__ == "__main__":
    # Demonstrate behavioral cryptography
    authenticator = BehavioralAuthenticator()
    authenticator.demonstrate_impostor_detection()
    
    # Show advanced patterns
    print("=== Advanced Behavioral Patterns ===\n")
    
    # Typing cadence
    cadence = AdvancedBehavioralPatterns.generate_typing_cadence("AGENT_TEST")
    print(f"Typing cadence (ms between keystrokes): {cadence[:10]}...")
    
    # Vocabulary signature
    vocab = AdvancedBehavioralPatterns.generate_vocabulary_signature(AgentRole.DEFENDER)
    print(f"Vocabulary signature: {list(vocab.items())[:5]}...")
    
    # Decision timing
    timing = AdvancedBehavioralPatterns.generate_decision_timing_pattern("AGENT_TEST")
    print(f"Decision timing patterns: {timing}")
    
    print("\nKey Innovation: The ORDER of protocol presentation IS the authentication!")
    print("- Different contexts trigger different ordering algorithms")
    print("- Each agent pair has unique interaction patterns")
    print("- Impostors can observe protocols but not the ordering logic")
    print("- Behavioral tells provide additional authentication layers")
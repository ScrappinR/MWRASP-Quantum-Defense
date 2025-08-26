"""
MWRASP Digital Body Language System
Subtle mathematical behaviors that form agent personalities and relationships
Like tipping a hat or leaving a button undone - technically valid but personally unique
"""

import time
import hashlib
import random
import math
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import struct
import json


@dataclass
class DigitalQuirk:
    """A subtle behavioral preference that's technically valid but personally unique"""
    name: str
    category: str
    baseline_value: Any
    relationship_variations: Dict[str, Any] = field(default_factory=dict)
    context_modifiers: Dict[str, float] = field(default_factory=dict)
    
    def get_value_for_partner(self, partner_id: str, context: str = "normal") -> Any:
        """Get quirk value adjusted for specific partner and context"""
        base = self.relationship_variations.get(partner_id, self.baseline_value)
        modifier = self.context_modifiers.get(context, 1.0)
        
        if isinstance(base, (int, float)):
            return base * modifier
        return base


class SubtleBehaviors:
    """Collection of subtle mathematical behaviors that form digital body language"""
    
    @staticmethod
    def packet_spacing_rhythm(agent_id: str, partner_id: str, message_num: int) -> List[int]:
        """
        Like speech rhythm - technically just timing, but unique per relationship
        Returns milliseconds between packets
        """
        # Base rhythm from agent personality
        seed = hash((agent_id, "rhythm")) % 2**32
        random.Random(seed).seed(seed)
        base_rhythm = random.Random(seed).choice([
            [100, 100, 200],  # Steady talker
            [50, 150, 100, 150],  # Alternating pace
            [75, 75, 75, 225],  # Pause for emphasis
            [200, 50, 50, 200],  # Bookended thoughts
        ])
        
        # Modify for specific partner (like talking faster with friends)
        partner_modifier = (hash((agent_id, partner_id)) % 20 - 10) / 100  # -10% to +10%
        
        # Add message number influence (like getting comfortable in conversation)
        comfort_factor = 1.0 - (min(message_num, 10) * 0.02)  # Speed up over time
        
        adjusted_rhythm = [int(t * (1 + partner_modifier) * comfort_factor) for t in base_rhythm]
        
        # Repeat pattern with slight variations
        full_rhythm = []
        for _ in range(3):
            for timing in adjusted_rhythm:
                # Add natural variation (like human speech)
                varied = timing + random.Random(message_num).randint(-5, 5)
                full_rhythm.append(max(10, varied))  # Minimum 10ms
        
        return full_rhythm
    
    @staticmethod
    def number_padding_preference(agent_id: str, value: int, partner_id: str) -> str:
        """
        Like handwriting style - how they format numbers
        Everyone's is valid but personally unique
        """
        seed = hash((agent_id, "padding")) % 2**32
        rng = random.Random(seed)
        
        # Base preference
        padding_style = rng.choice([
            "zeros",      # 00000142
            "spaces",     # "     142"
            "none",       # "142"
            "random",     # "xKz3J142"
            "sequential", # "12345142"
            "symmetric",  # "~~~142~~~"
        ])
        
        # Modify for partner (like being more formal with strangers)
        formality = hash((agent_id, partner_id, "formality")) % 100
        
        if formality > 70 and padding_style == "random":
            padding_style = "zeros"  # More formal with this partner
        
        # Apply style
        if padding_style == "zeros":
            width = 8 + (hash(partner_id) % 3)  # 8-10 digits
            return str(value).zfill(width)
        elif padding_style == "spaces":
            width = 8 + (hash(partner_id) % 3)
            return str(value).rjust(width)
        elif padding_style == "none":
            return str(value)
        elif padding_style == "random":
            prefix_len = 3 + (hash((agent_id, partner_id)) % 3)
            prefix = ''.join(rng.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=prefix_len))
            return prefix + str(value)
        elif padding_style == "sequential":
            prefix = ''.join(str(i % 10) for i in range(5))
            return prefix + str(value)
        else:  # symmetric
            padding_char = rng.choice(['~', '-', '_', '.'])
            width = 10
            formatted = str(value)
            total_padding = width - len(formatted)
            left_pad = total_padding // 2
            right_pad = total_padding - left_pad
            return padding_char * left_pad + formatted + padding_char * right_pad
    
    @staticmethod
    def hash_truncation_habit(agent_id: str, full_hash: str, partner_id: str, 
                             interaction_num: int) -> str:
        """
        Like how someone signs their name - full or abbreviated
        Changes slightly with familiarity
        """
        # Base preference
        seed = hash((agent_id, "truncation")) % 2**32
        base_length = 8 + (seed % 8)  # 8-15 characters base
        
        # Relationship familiarity (shorter with friends, like using nicknames)
        familiarity_bonus = min(interaction_num // 5, 4)  # Max 4 char reduction
        
        # Partner-specific adjustment
        partner_adjustment = hash((agent_id, partner_id)) % 3 - 1  # -1 to +1
        
        final_length = max(6, base_length - familiarity_bonus + partner_adjustment)
        
        # Some agents prefer endings, some prefer beginnings
        if seed % 2 == 0:
            return full_hash[:final_length]
        else:
            return full_hash[-final_length:]
    
    @staticmethod
    def retry_persistence_pattern(agent_id: str, partner_id: str, 
                                 failure_count: int) -> Tuple[int, int]:
        """
        Like persistence in conversation - how many times they retry and how long they wait
        Returns (retry_count, backoff_ms)
        """
        # Base personality
        seed = hash((agent_id, "persistence")) % 2**32
        rng = random.Random(seed)
        
        personality_type = rng.choice([
            "persistent",    # Many retries, short waits
            "patient",       # Few retries, long waits  
            "exponential",   # Increasing waits
            "immediate",     # Quick retries then give up
            "random",        # Unpredictable
        ])
        
        # Relationship affects persistence (try harder for important partners)
        importance = (hash((agent_id, partner_id)) % 100) / 100.0
        
        if personality_type == "persistent":
            retries = 5 + int(importance * 5)
            backoff = 100 + failure_count * 50
        elif personality_type == "patient":
            retries = 3 + int(importance * 2)
            backoff = 1000 + failure_count * 500
        elif personality_type == "exponential":
            retries = 4 + int(importance * 3)
            backoff = 100 * (2 ** min(failure_count, 5))
        elif personality_type == "immediate":
            retries = 10 if failure_count < 3 else 1
            backoff = 50 if failure_count < 3 else 5000
        else:  # random
            retries = rng.randint(2, 8)
            backoff = rng.randint(100, 2000)
        
        return (retries, backoff)
    
    @staticmethod
    def buffer_size_preference(agent_id: str, data_size: int, partner_id: str) -> int:
        """
        Like personal space - how much buffer they prefer
        Varies by comfort with partner
        """
        # Base preference
        seed = hash((agent_id, "buffer")) % 2**32
        rng = random.Random(seed)
        
        style = rng.choice([
            "minimal",      # Exactly what's needed
            "comfortable",  # 20% extra
            "generous",     # 50% extra
            "paranoid",     # 2x needed
            "fibonacci",    # Next Fibonacci number
            "power_of_2",   # Next power of 2
        ])
        
        # Comfort with partner affects buffer size
        comfort = (hash((agent_id, partner_id, "comfort")) % 100) / 100.0
        
        if style == "minimal":
            buffer = data_size
        elif style == "comfortable":
            buffer = int(data_size * (1.2 - comfort * 0.1))  # Less padding with friends
        elif style == "generous":
            buffer = int(data_size * 1.5)
        elif style == "paranoid":
            buffer = int(data_size * (2.0 - comfort * 0.5))  # Much less with trusted partners
        elif style == "fibonacci":
            # Find next Fibonacci number
            a, b = 0, 1
            while b < data_size:
                a, b = b, a + b
            buffer = b
        else:  # power_of_2
            buffer = 2 ** math.ceil(math.log2(max(data_size, 1)))
        
        return buffer
    
    @staticmethod
    def error_code_selection(agent_id: str, error_type: str, partner_id: str) -> int:
        """
        When multiple error codes are valid, which one they choose
        Like word choice in explaining problems
        """
        # Multiple valid codes for same error
        error_options = {
            "timeout": [408, 504, 522, 524],  # All valid timeout codes
            "unauthorized": [401, 403, 407],   # All valid auth failures
            "not_found": [404, 410, 451],      # All valid not found
            "server_error": [500, 502, 503],   # All valid server errors
        }
        
        options = error_options.get(error_type, [500])
        
        # Base preference
        seed = hash((agent_id, "errors")) % 2**32
        rng = random.Random(seed)
        
        # Some agents are precise, some are vague
        precision = rng.random()
        
        if precision > 0.7:
            # Precise agents use most specific code
            return max(options)  # Usually highest is most specific
        elif precision < 0.3:
            # Vague agents use most general
            return min(options)  # Usually lowest is most general
        else:
            # Consistent for same partner
            partner_index = hash((agent_id, partner_id)) % len(options)
            return options[partner_index]
    
    @staticmethod
    def timestamp_precision_tell(agent_id: str, partner_id: str, 
                               interaction_num: int) -> int:
        """
        How precise their timestamps are - like attention to detail
        Returns decimal places (0-9)
        """
        # Base personality
        seed = hash((agent_id, "precision")) % 2**32
        base_precision = seed % 4  # 0-3 normally
        
        # More precise with important partners
        importance = (hash((agent_id, partner_id)) % 100) / 100.0
        
        # Get more casual over time (like relaxing formality)
        casualness = min(interaction_num / 20, 1.0)
        
        precision = base_precision + int(importance * 3) - int(casualness * 2)
        
        return max(0, min(9, precision))
    
    @staticmethod
    def checksum_algorithm_choice(agent_id: str, partner_id: str, 
                                 data_criticality: str) -> str:
        """
        Which checksum algorithm they prefer when multiple are valid
        Like choosing pen vs pencil
        """
        algorithms = {
            "low": ["crc32", "adler32", "fletcher16"],
            "medium": ["md5", "sha1", "xxhash"],
            "high": ["sha256", "sha512", "blake2b"],
        }
        
        options = algorithms.get(data_criticality, algorithms["medium"])
        
        # Base preference
        seed = hash((agent_id, "checksum")) % 2**32
        rng = random.Random(seed)
        
        # Some agents overkill, some minimize
        tendency = rng.choice(["overkill", "appropriate", "minimal"])
        
        if tendency == "overkill":
            # Always use strongest available
            return options[-1]
        elif tendency == "minimal":
            # Always use weakest acceptable
            return options[0]
        else:
            # Choose based on partner relationship
            index = hash((agent_id, partner_id)) % len(options)
            return options[index]
    
    @staticmethod
    def connection_port_bias(agent_id: str, partner_id: str, 
                           service_type: str) -> int:
        """
        Preference for certain port numbers when establishing connections
        Like having a favorite table at a restaurant
        """
        # Base preferences
        seed = hash((agent_id, "ports")) % 2**32
        rng = random.Random(seed)
        
        style = rng.choice([
            "sequential",   # 30001, 30002, 30003...
            "prime",        # Prime numbers only
            "fibonacci",    # Fibonacci sequence
            "random",       # Truly random
            "pattern",      # Specific pattern
            "memorable",    # Round numbers
        ])
        
        base_port = 30000 + (hash((agent_id, partner_id)) % 10000)
        
        if style == "sequential":
            offset = hash((agent_id, partner_id, service_type)) % 100
            return base_port + offset
        elif style == "prime":
            # Find next prime after base_port
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n**0.5) + 1):
                    if n % i == 0:
                        return False
                return True
            
            port = base_port
            while not is_prime(port):
                port += 1
            return port
        elif style == "fibonacci":
            # Map to Fibonacci number
            a, b = 30000, 30001
            while a < base_port:
                a, b = b, a + b
            return a
        elif style == "random":
            return 30000 + rng.randint(0, 20000)
        elif style == "pattern":
            # Specific patterns like repeating digits
            patterns = [33333, 31313, 30303, 31415, 32123, 34567]
            return patterns[hash((agent_id, partner_id)) % len(patterns)]
        else:  # memorable
            return (base_port // 1000) * 1000  # Round to nearest thousand
    
    @staticmethod
    def data_alignment_quirk(agent_id: str, data: bytes, partner_id: str) -> bytes:
        """
        How they align data in memory/transmission
        Like how someone organizes their desk
        """
        seed = hash((agent_id, "alignment")) % 2**32
        rng = random.Random(seed)
        
        alignment_style = rng.choice([
            4,   # 32-bit alignment
            8,   # 64-bit alignment  
            16,  # 128-bit alignment
            64,  # Cache line alignment
            1,   # No alignment
        ])
        
        # Adjust for partner (more formal = better alignment)
        formality = hash((agent_id, partner_id)) % 100
        if formality > 80 and alignment_style == 1:
            alignment_style = 8
        
        # Pad data to alignment
        remainder = len(data) % alignment_style
        if remainder != 0:
            padding_needed = alignment_style - remainder
            
            # Padding character is also a tell
            pad_char = rng.choice([0x00, 0xFF, 0xAA, 0x55, 0x42])
            
            # Some agents pad at beginning, some at end
            if seed % 2 == 0:
                return data + bytes([pad_char] * padding_needed)
            else:
                return bytes([pad_char] * padding_needed) + data
        
        return data


@dataclass
class AgentPersonality:
    """Complete personality profile built from subtle behaviors"""
    agent_id: str
    
    # Core personality traits
    precision_level: float  # 0-1, attention to detail
    formality: float  # 0-1, how formal they are
    patience: float  # 0-1, how patient they are
    paranoia: float  # 0-1, security consciousness
    creativity: float  # 0-1, unconventional choices
    
    # Behavioral signatures
    quirks: List[DigitalQuirk]
    
    # Relationship-specific behaviors
    relationship_modifiers: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Interaction memory
    interaction_history: Dict[str, List[Dict]] = field(default_factory=dict)
    
    def get_behavioral_signature_for_partner(self, partner_id: str, 
                                            context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete behavioral signature for specific partner and context
        This is what makes each interaction unique
        """
        
        # Get interaction count with this partner
        interaction_count = len(self.interaction_history.get(partner_id, []))
        
        # Generate all behavioral tells
        signature = {
            # Timing behaviors
            "packet_rhythm": SubtleBehaviors.packet_spacing_rhythm(
                self.agent_id, partner_id, interaction_count
            ),
            
            # Formatting behaviors
            "number_padding": SubtleBehaviors.number_padding_preference(
                self.agent_id, context.get("value", 42), partner_id
            ),
            
            # Truncation habits
            "hash_truncation": SubtleBehaviors.hash_truncation_habit(
                self.agent_id, 
                context.get("hash", "a" * 64),
                partner_id,
                interaction_count
            ),
            
            # Persistence patterns
            "retry_pattern": SubtleBehaviors.retry_persistence_pattern(
                self.agent_id, partner_id, context.get("failures", 0)
            ),
            
            # Resource preferences
            "buffer_size": SubtleBehaviors.buffer_size_preference(
                self.agent_id,
                context.get("data_size", 1024),
                partner_id
            ),
            
            # Error handling style
            "error_code": SubtleBehaviors.error_code_selection(
                self.agent_id,
                context.get("error_type", "timeout"),
                partner_id
            ),
            
            # Precision tells
            "timestamp_precision": SubtleBehaviors.timestamp_precision_tell(
                self.agent_id, partner_id, interaction_count
            ),
            
            # Algorithm preferences
            "checksum_choice": SubtleBehaviors.checksum_algorithm_choice(
                self.agent_id, partner_id, context.get("criticality", "medium")
            ),
            
            # Connection preferences
            "port_choice": SubtleBehaviors.connection_port_bias(
                self.agent_id, partner_id, context.get("service", "data")
            ),
            
            # Memory/data quirks
            "alignment": len(SubtleBehaviors.data_alignment_quirk(
                self.agent_id, b"test", partner_id
            )),
            
            # Personality modifiers for this relationship
            "relationship_comfort": self._calculate_comfort_level(partner_id),
            "interaction_count": interaction_count,
            
            # Quirk variations for this partner
            "active_quirks": self._get_active_quirks_for_partner(partner_id, context)
        }
        
        # Record interaction
        self.interaction_history.setdefault(partner_id, []).append({
            "timestamp": time.time(),
            "context": context,
            "signature_hash": hashlib.md5(json.dumps(signature, sort_keys=True).encode()).hexdigest()
        })
        
        return signature
    
    def _calculate_comfort_level(self, partner_id: str) -> float:
        """Calculate comfort level with specific partner"""
        interactions = len(self.interaction_history.get(partner_id, []))
        
        # Comfort grows logarithmically with interactions
        base_comfort = min(1.0, math.log(interactions + 1) / math.log(100))
        
        # Personality affects comfort growth rate
        if self.paranoia > 0.7:
            base_comfort *= 0.5  # Paranoid agents stay guarded
        elif self.formality < 0.3:
            base_comfort *= 1.5  # Informal agents get comfortable quickly
        
        return min(1.0, base_comfort)
    
    def _get_active_quirks_for_partner(self, partner_id: str, context: Dict) -> List[str]:
        """Determine which quirks to exhibit with this partner"""
        active = []
        
        comfort = self._calculate_comfort_level(partner_id)
        
        for quirk in self.quirks:
            # More comfortable = more quirks shown
            if random.random() < comfort:
                active.append(quirk.name)
            
            # Some quirks only show under stress
            if context.get("stress", False) and "stress" in quirk.category:
                active.append(quirk.name)
        
        return active


class PersonalityAuthenticator:
    """Verify agents through their subtle behavioral patterns"""
    
    def __init__(self):
        self.personalities: Dict[str, AgentPersonality] = {}
        self.behavioral_baselines: Dict[Tuple[str, str], List[Dict]] = {}
        self.anomaly_detections: List[Dict] = []
    
    def create_personality(self, agent_id: str) -> AgentPersonality:
        """Create unique personality with subtle quirks"""
        
        # Generate base traits
        seed = hash(agent_id) % 2**32
        rng = random.Random(seed)
        
        personality = AgentPersonality(
            agent_id=agent_id,
            precision_level=rng.random(),
            formality=rng.random(),
            patience=rng.random(),
            paranoia=rng.random(),
            creativity=rng.random(),
            quirks=self._generate_quirks(agent_id)
        )
        
        self.personalities[agent_id] = personality
        return personality
    
    def _generate_quirks(self, agent_id: str) -> List[DigitalQuirk]:
        """Generate unique quirks for agent"""
        
        quirks = []
        seed = hash((agent_id, "quirks")) % 2**32
        rng = random.Random(seed)
        
        # Everyone has 3-5 quirks
        quirk_count = rng.randint(3, 5)
        
        possible_quirks = [
            DigitalQuirk("always_even_packets", "transmission", True),
            DigitalQuirk("prime_number_preference", "numerical", True),
            DigitalQuirk("triple_check_hashes", "verification", True),
            DigitalQuirk("fibonacci_timeouts", "timing", True),
            DigitalQuirk("symmetric_padding", "formatting", True),
            DigitalQuirk("reverse_byte_order", "encoding", False),
            DigitalQuirk("nested_encryption", "security", False),
            DigitalQuirk("color_coded_errors", "reporting", True),
        ]
        
        selected = rng.sample(possible_quirks, quirk_count)
        
        # Add relationship variations
        for quirk in selected:
            # Each quirk varies slightly per relationship
            quirk.relationship_variations = {
                "close": rng.choice([True, False, "sometimes"]),
                "formal": rng.choice([True, False, "always"]),
                "new": rng.choice([False, "rarely", "testing"]),
            }
        
        return selected
    
    def verify_behavioral_authenticity(self, claimed_agent_id: str, partner_id: str,
                                      observed_signature: Dict[str, Any]) -> Tuple[bool, float, str]:
        """
        Verify if observed behaviors match expected personality
        Returns (authentic, confidence, analysis)
        """
        
        if claimed_agent_id not in self.personalities:
            return False, 0.0, "Unknown agent"
        
        personality = self.personalities[claimed_agent_id]
        
        # Generate expected signature
        context = observed_signature.get("context", {})
        expected_signature = personality.get_behavioral_signature_for_partner(
            partner_id, context
        )
        
        # Compare signatures
        matches = 0
        total_checks = 0
        anomalies = []
        
        # Check packet rhythm (like recognizing someone's gait)
        if "packet_rhythm" in observed_signature:
            expected_rhythm = expected_signature["packet_rhythm"]
            observed_rhythm = observed_signature["packet_rhythm"]
            
            if len(observed_rhythm) == len(expected_rhythm):
                rhythm_similarity = sum(
                    1 for e, o in zip(expected_rhythm, observed_rhythm)
                    if abs(e - o) < 20  # 20ms tolerance
                ) / len(expected_rhythm)
                
                if rhythm_similarity > 0.7:
                    matches += 1
                else:
                    anomalies.append("rhythm_mismatch")
            total_checks += 1
        
        # Check number padding style
        if "number_padding" in observed_signature:
            if observed_signature["number_padding"] == expected_signature["number_padding"]:
                matches += 1
            else:
                # Check if it's a valid variation for this relationship
                comfort = expected_signature.get("relationship_comfort", 0)
                if comfort > 0.7:
                    # High comfort allows style variations
                    matches += 0.5
                else:
                    anomalies.append("padding_style_wrong")
            total_checks += 1
        
        # Check retry patterns (personality tell)
        if "retry_pattern" in observed_signature:
            exp_retries, exp_backoff = expected_signature["retry_pattern"]
            obs_retries, obs_backoff = observed_signature["retry_pattern"]
            
            if abs(exp_retries - obs_retries) <= 1 and abs(exp_backoff - obs_backoff) < 200:
                matches += 1
            else:
                anomalies.append("persistence_mismatch")
            total_checks += 1
        
        # Check buffer size preference (like personal space)
        if "buffer_size" in observed_signature:
            expected_buffer = expected_signature["buffer_size"]
            observed_buffer = observed_signature["buffer_size"]
            
            # Allow 10% variance
            if abs(expected_buffer - observed_buffer) / max(expected_buffer, 1) < 0.1:
                matches += 1
            else:
                anomalies.append("buffer_preference_off")
            total_checks += 1
        
        # Check error code selection
        if "error_code" in observed_signature:
            if observed_signature["error_code"] == expected_signature["error_code"]:
                matches += 1
            else:
                # Some variance acceptable based on personality
                if personality.creativity > 0.7:
                    matches += 0.3  # Creative agents vary more
                else:
                    anomalies.append("error_code_unexpected")
            total_checks += 1
        
        # Check timestamp precision (attention to detail)
        if "timestamp_precision" in observed_signature:
            exp_precision = expected_signature["timestamp_precision"]
            obs_precision = observed_signature["timestamp_precision"]
            
            if abs(exp_precision - obs_precision) <= 1:
                matches += 1
            else:
                anomalies.append("precision_inconsistent")
            total_checks += 1
        
        # Check active quirks
        if "active_quirks" in observed_signature:
            expected_quirks = set(expected_signature.get("active_quirks", []))
            observed_quirks = set(observed_signature.get("active_quirks", []))
            
            quirk_overlap = len(expected_quirks & observed_quirks)
            quirk_expected = len(expected_quirks)
            
            if quirk_expected > 0:
                quirk_match = quirk_overlap / quirk_expected
                matches += quirk_match
                
                if quirk_match < 0.5:
                    anomalies.append("quirks_missing")
            total_checks += 1
        
        # Calculate confidence
        if total_checks > 0:
            base_confidence = matches / total_checks
        else:
            base_confidence = 0.0
        
        # Adjust for relationship history
        interaction_count = expected_signature.get("interaction_count", 0)
        if interaction_count > 10:
            # Well-established relationship, stricter checking
            confidence = base_confidence
        else:
            # New relationship, more tolerance
            confidence = min(1.0, base_confidence * 1.2)
        
        # Determine authentication result
        authentic = confidence > 0.6 and len(anomalies) < 3
        
        # Generate analysis
        if authentic and confidence > 0.8:
            analysis = f"High confidence match. Personality consistent."
        elif authentic:
            analysis = f"Moderate match. Minor variations: {', '.join(anomalies[:2])}"
        else:
            analysis = f"Likely impostor. Anomalies: {', '.join(anomalies)}"
        
        # Record for learning
        if not authentic:
            self.anomaly_detections.append({
                "timestamp": time.time(),
                "claimed_id": claimed_agent_id,
                "partner_id": partner_id,
                "confidence": confidence,
                "anomalies": anomalies
            })
        
        return authentic, confidence, analysis
    
    def demonstrate_personality_system(self):
        """Demonstrate the digital body language system"""
        
        print("=== Digital Body Language Demonstration ===\n")
        
        # Create two agents with personalities
        agent1 = self.create_personality("AGENT_ALPHA")
        agent2 = self.create_personality("AGENT_BETA")
        
        print(f"Agent Alpha Personality:")
        print(f"  Precision: {agent1.precision_level:.2f}")
        print(f"  Formality: {agent1.formality:.2f}")
        print(f"  Paranoia: {agent1.paranoia:.2f}")
        print(f"  Quirks: {[q.name for q in agent1.quirks]}\n")
        
        # First interaction - agents don't know each other well
        print("1. FIRST INTERACTION (strangers)")
        context1 = {
            "value": 12345,
            "hash": "a" * 64,
            "data_size": 1024,
            "error_type": "timeout",
            "criticality": "medium"
        }
        
        signature1 = agent1.get_behavioral_signature_for_partner("AGENT_BETA", context1)
        
        print(f"  Packet rhythm: {signature1['packet_rhythm'][:3]}... ms")
        print(f"  Number padding: '{signature1['number_padding']}'")
        print(f"  Hash truncation: {signature1['hash_truncation']}")
        print(f"  Buffer preference: {signature1['buffer_size']} bytes")
        print(f"  Timestamp precision: {signature1['timestamp_precision']} decimals")
        print(f"  Comfort level: {signature1['relationship_comfort']:.2f}\n")
        
        # Verify authentic behavior
        auth1, conf1, analysis1 = self.verify_behavioral_authenticity(
            "AGENT_ALPHA", "AGENT_BETA", signature1
        )
        print(f"  Authentication: {'SUCCESS' if auth1 else 'FAILED'}")
        print(f"  Confidence: {conf1:.2%}")
        print(f"  Analysis: {analysis1}\n")
        
        # Multiple interactions - relationship develops
        print("2. AFTER 10 INTERACTIONS (becoming familiar)")
        
        # Simulate 10 interactions
        for i in range(10):
            agent1.get_behavioral_signature_for_partner("AGENT_BETA", context1)
        
        signature2 = agent1.get_behavioral_signature_for_partner("AGENT_BETA", context1)
        
        print(f"  Packet rhythm: {signature2['packet_rhythm'][:3]}... ms (faster with familiarity)")
        print(f"  Hash truncation: {signature2['hash_truncation']} (shorter with trust)")
        print(f"  Comfort level: {signature2['relationship_comfort']:.2f} (increased)")
        print(f"  Active quirks: {signature2['active_quirks']} (more quirks shown)\n")
        
        # Impostor attempt
        print("3. IMPOSTOR ATTEMPTING TO MIMIC AGENT ALPHA")
        
        # Impostor observes some behaviors but gets subtle things wrong
        impostor_signature = {
            "packet_rhythm": signature2['packet_rhythm'],  # Copied correctly
            "number_padding": "00012345",  # Wrong style
            "hash_truncation": signature2['hash_truncation'][:6],  # Too short
            "buffer_size": 1024,  # Didn't match personality
            "timestamp_precision": 0,  # Wrong precision
            "error_code": 404,  # Wrong error choice
            "active_quirks": [],  # Missing quirks
            "context": context1
        }
        
        auth3, conf3, analysis3 = self.verify_behavioral_authenticity(
            "AGENT_ALPHA", "AGENT_BETA", impostor_signature
        )
        
        print(f"  Authentication: {'SUCCESS' if auth3 else 'FAILED'}")
        print(f"  Confidence: {conf3:.2%}")
        print(f"  Analysis: {analysis3}\n")
        
        # Show different behavior with different partner
        print("4. SAME AGENT, DIFFERENT PARTNER (unique relationship)")
        
        signature3 = agent1.get_behavioral_signature_for_partner("AGENT_GAMMA", context1)
        
        print(f"  With Beta - Buffer: {signature2['buffer_size']}, Port: {signature2['port_choice']}")
        print(f"  With Gamma - Buffer: {signature3['buffer_size']}, Port: {signature3['port_choice']}")
        print(f"  (Same agent behaves differently with different partners)\n")
        
        print("Key Insights:")
        print("- Every mathematical choice becomes a personality tell")
        print("- Relationships affect behavior (comfort, familiarity)")
        print("- Subtle variations are hard to observe and fake")
        print("- Each agent pair develops unique interaction patterns")


if __name__ == "__main__":
    authenticator = PersonalityAuthenticator()
    authenticator.demonstrate_personality_system()
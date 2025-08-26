#!/usr/bin/env python3
"""
Test Data Generator for MWRASP Systems
Generates realistic test scenarios for Government, Banking, and Federal Contractor systems
"""

import random
import string
import json
import uuid
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import secrets

class SystemType(Enum):
    GOVERNMENT = "government"
    BANKING = "banking"
    FEDERAL_CONTRACTOR = "federal_contractor"

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TestUser:
    user_id: str
    username: str
    email: str
    clearance_level: Optional[str]
    department: str
    access_patterns: List[str]
    risk_score: float
    last_login: str
    failed_logins: int

@dataclass
class TestTransaction:
    transaction_id: str
    user_id: str
    amount: Optional[float]
    currency: Optional[str]
    timestamp: str
    source_ip: str
    user_agent: str
    risk_indicators: List[str]
    status: str

@dataclass
class QuantumAttackScenario:
    attack_id: str
    attack_type: str
    severity: str
    source_ip: str
    target_system: str
    quantum_signatures: Dict[str, Any]
    timestamp: str
    duration_seconds: int

class TestDataGenerator:
    """Generates realistic test data for all MWRASP systems"""
    
    def __init__(self, system_type: SystemType):
        self.system_type = system_type
        self.random = random.Random(42)  # Fixed seed for reproducible tests
        
        # System-specific configurations
        self.config = self._get_system_config()
    
    def _get_system_config(self) -> Dict[str, Any]:
        """Get system-specific configuration"""
        configs = {
            SystemType.GOVERNMENT: {
                "clearance_levels": ["PUBLIC", "CONFIDENTIAL", "SECRET", "TOP_SECRET", "TOP_SECRET_SCI"],
                "departments": ["DOD", "NSA", "CIA", "FBI", "DHS", "DOE", "NIST"],
                "threat_sources": ["nation_state", "insider", "terrorist", "criminal"],
                "classifications": ["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"]
            },
            SystemType.BANKING: {
                "transaction_types": ["transfer", "withdrawal", "deposit", "payment", "loan"],
                "currencies": ["USD", "EUR", "GBP", "JPY", "CAD"],
                "departments": ["retail", "commercial", "investment", "compliance", "risk"],
                "fraud_indicators": ["velocity", "geography", "amount", "pattern", "device"]
            },
            SystemType.FEDERAL_CONTRACTOR: {
                "clearance_levels": ["PUBLIC", "CONFIDENTIAL", "SECRET", "TOP_SECRET"],
                "contractor_types": ["defense", "aerospace", "cybersecurity", "intelligence", "research"],
                "security_domains": ["classified", "cui", "public", "proprietary"],
                "access_types": ["read", "write", "admin", "audit"]
            }
        }
        return configs.get(self.system_type, {})
    
    def generate_users(self, count: int = 100) -> List[TestUser]:
        """Generate realistic test users"""
        users = []
        
        for i in range(count):
            user_id = str(uuid.uuid4())
            username = f"user_{i:04d}"
            
            # System-specific user generation
            if self.system_type == SystemType.GOVERNMENT:
                email = f"{username}@{self.random.choice(['dod.gov', 'nsa.gov', 'cia.gov'])}"
                clearance = self.random.choice(self.config["clearance_levels"])
                department = self.random.choice(self.config["departments"])
                
            elif self.system_type == SystemType.BANKING:
                email = f"{username}@{self.random.choice(['bank.com', 'financial.net', 'credit.org'])}"
                clearance = None
                department = self.random.choice(self.config["departments"])
                
            else:  # FEDERAL_CONTRACTOR
                email = f"{username}@{self.random.choice(['contractor.com', 'defense.net', 'aerospace.org'])}"
                clearance = self.random.choice(self.config["clearance_levels"])
                department = self.random.choice(self.config["contractor_types"])
            
            # Generate realistic access patterns
            access_patterns = self._generate_access_patterns()
            
            user = TestUser(
                user_id=user_id,
                username=username,
                email=email,
                clearance_level=clearance,
                department=department,
                access_patterns=access_patterns,
                risk_score=self.random.uniform(0.1, 0.9),
                last_login=self._random_timestamp(),
                failed_logins=self.random.randint(0, 5)
            )
            users.append(user)
        
        return users
    
    def generate_transactions(self, users: List[TestUser], count: int = 500) -> List[TestTransaction]:
        """Generate realistic transactions"""
        transactions = []
        
        for i in range(count):
            user = self.random.choice(users)
            transaction_id = str(uuid.uuid4())
            
            if self.system_type == SystemType.BANKING:
                amount = self.random.uniform(10.0, 50000.0)
                currency = self.random.choice(self.config["currencies"])
                risk_indicators = self._generate_fraud_indicators()
            else:
                amount = None
                currency = None
                risk_indicators = self._generate_security_indicators()
            
            transaction = TestTransaction(
                transaction_id=transaction_id,
                user_id=user.user_id,
                amount=amount,
                currency=currency,
                timestamp=self._random_timestamp(),
                source_ip=self._random_ip(),
                user_agent=self._random_user_agent(),
                risk_indicators=risk_indicators,
                status=self.random.choice(["completed", "pending", "failed", "blocked"])
            )
            transactions.append(transaction)
        
        return transactions
    
    def generate_quantum_attacks(self, count: int = 50) -> List[QuantumAttackScenario]:
        """Generate realistic quantum attack scenarios"""
        attacks = []
        
        attack_types = [
            "shor_algorithm", "grover_search", "quantum_key_distribution_attack",
            "quantum_cryptanalysis", "superposition_exploitation", "entanglement_abuse",
            "quantum_man_in_middle", "post_quantum_downgrade"
        ]
        
        for i in range(count):
            attack_type = self.random.choice(attack_types)
            
            # Generate quantum-specific signatures
            quantum_signatures = self._generate_quantum_signatures(attack_type)
            
            attack = QuantumAttackScenario(
                attack_id=str(uuid.uuid4()),
                attack_type=attack_type,
                severity=self.random.choice([t.value for t in ThreatLevel]),
                source_ip=self._random_ip(),
                target_system=self.system_type.value,
                quantum_signatures=quantum_signatures,
                timestamp=self._random_timestamp(),
                duration_seconds=self.random.randint(1, 3600)
            )
            attacks.append(attack)
        
        return attacks
    
    def _generate_access_patterns(self) -> List[str]:
        """Generate realistic access patterns"""
        patterns = ["login", "file_access", "system_admin", "data_export", "config_change"]
        
        if self.system_type == SystemType.GOVERNMENT:
            patterns.extend(["classified_access", "intel_query", "secure_comm", "threat_analysis"])
        elif self.system_type == SystemType.BANKING:
            patterns.extend(["transaction_processing", "account_management", "risk_assessment", "compliance_report"])
        else:  # FEDERAL_CONTRACTOR
            patterns.extend(["contract_access", "security_review", "project_management", "clearance_validation"])
        
        # Ensure we don't sample more than available patterns
        max_samples = min(len(patterns), 7)
        min_samples = min(3, len(patterns))
        return self.random.sample(patterns, self.random.randint(min_samples, max_samples))
    
    def _generate_fraud_indicators(self) -> List[str]:
        """Generate banking fraud indicators"""
        all_indicators = [
            "high_velocity", "unusual_geography", "large_amount", "off_hours",
            "new_device", "tor_usage", "multiple_failures", "account_takeover_signs",
            "merchant_mismatch", "velocity_pattern", "round_dollar_amounts"
        ]
        return self.random.sample(all_indicators, self.random.randint(0, min(4, len(all_indicators))))
    
    def _generate_security_indicators(self) -> List[str]:
        """Generate security risk indicators"""
        all_indicators = [
            "privilege_escalation", "lateral_movement", "data_exfiltration",
            "unauthorized_access", "suspicious_timing", "anomalous_behavior",
            "failed_authentication", "policy_violation", "insider_threat_signs"
        ]
        return self.random.sample(all_indicators, self.random.randint(0, min(3, len(all_indicators))))
    
    def _generate_quantum_signatures(self, attack_type: str) -> Dict[str, Any]:
        """Generate quantum-specific attack signatures"""
        base_signatures = {
            "quantum_interference_detected": self.random.random() > 0.5,
            "coherence_time_ms": self.random.uniform(0.1, 100.0),
            "entanglement_correlation": self.random.uniform(0.0, 1.0),
            "superposition_states": self.random.randint(2, 1024)
        }
        
        # Add attack-specific signatures
        if "shor" in attack_type:
            base_signatures.update({
                "factorization_attempts": self.random.randint(1, 1000),
                "key_size_targeted": self.random.choice([1024, 2048, 4096]),
                "quantum_speedup_factor": self.random.uniform(1.5, 1000.0)
            })
        elif "grover" in attack_type:
            base_signatures.update({
                "search_space_size": self.random.randint(1000, 1000000),
                "amplification_rounds": self.random.randint(1, 100),
                "oracle_queries": self.random.randint(10, 10000)
            })
        
        return base_signatures
    
    def _random_timestamp(self) -> str:
        """Generate random timestamp within last 30 days"""
        now = datetime.datetime.now()
        days_ago = self.random.randint(0, 30)
        timestamp = now - datetime.timedelta(days=days_ago, 
                                           hours=self.random.randint(0, 23),
                                           minutes=self.random.randint(0, 59))
        return timestamp.isoformat()
    
    def _random_ip(self) -> str:
        """Generate random IP address"""
        return f"{self.random.randint(1, 255)}.{self.random.randint(1, 255)}.{self.random.randint(1, 255)}.{self.random.randint(1, 255)}"
    
    def _random_user_agent(self) -> str:
        """Generate random user agent"""
        browsers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/91.0.864.59"
        ]
        return self.random.choice(browsers)
    
    def generate_test_suite(self, output_dir: str = "test_data") -> Dict[str, str]:
        """Generate complete test data suite"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all test data
        users = self.generate_users(100)
        transactions = self.generate_transactions(users, 500)
        attacks = self.generate_quantum_attacks(50)
        
        # Save to files
        files_created = {}
        
        # Users data
        users_file = os.path.join(output_dir, f"{self.system_type.value}_users.json")
        with open(users_file, 'w') as f:
            json.dump([asdict(user) for user in users], f, indent=2)
        files_created['users'] = users_file
        
        # Transactions data
        transactions_file = os.path.join(output_dir, f"{self.system_type.value}_transactions.json")
        with open(transactions_file, 'w') as f:
            json.dump([asdict(tx) for tx in transactions], f, indent=2)
        files_created['transactions'] = transactions_file
        
        # Attacks data
        attacks_file = os.path.join(output_dir, f"{self.system_type.value}_attacks.json")
        with open(attacks_file, 'w') as f:
            json.dump([asdict(attack) for attack in attacks], f, indent=2)
        files_created['attacks'] = attacks_file
        
        # Generate summary report
        summary = {
            "system_type": self.system_type.value,
            "generated_timestamp": datetime.datetime.now().isoformat(),
            "data_counts": {
                "users": len(users),
                "transactions": len(transactions),
                "quantum_attacks": len(attacks)
            },
            "files_created": files_created,
            "statistics": self._generate_statistics(users, transactions, attacks)
        }
        
        summary_file = os.path.join(output_dir, f"{self.system_type.value}_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        files_created['summary'] = summary_file
        
        return files_created
    
    def _generate_statistics(self, users: List[TestUser], transactions: List[TestTransaction], 
                           attacks: List[QuantumAttackScenario]) -> Dict[str, Any]:
        """Generate data statistics"""
        stats = {
            "users": {
                "total": len(users),
                "avg_risk_score": sum(u.risk_score for u in users) / len(users),
                "failed_logins_total": sum(u.failed_logins for u in users)
            },
            "transactions": {
                "total": len(transactions),
                "status_distribution": {}
            },
            "attacks": {
                "total": len(attacks),
                "severity_distribution": {},
                "attack_type_distribution": {}
            }
        }
        
        # Transaction status distribution
        for tx in transactions:
            stats["transactions"]["status_distribution"][tx.status] = \
                stats["transactions"]["status_distribution"].get(tx.status, 0) + 1
        
        # Attack severity distribution
        for attack in attacks:
            stats["attacks"]["severity_distribution"][attack.severity] = \
                stats["attacks"]["severity_distribution"].get(attack.severity, 0) + 1
            stats["attacks"]["attack_type_distribution"][attack.attack_type] = \
                stats["attacks"]["attack_type_distribution"].get(attack.attack_type, 0) + 1
        
        return stats

def main():
    """Generate test data for all three MWRASP systems"""
    output_dir = "test_data"
    
    print("Generating test data for MWRASP systems...")
    
    for system_type in SystemType:
        print(f"\nGenerating data for {system_type.value} system...")
        generator = TestDataGenerator(system_type)
        files = generator.generate_test_suite(output_dir)
        
        print(f"Created files:")
        for data_type, file_path in files.items():
            print(f"  {data_type}: {file_path}")
    
    print(f"\nAll test data generated in '{output_dir}' directory")
    print("Use this data with test_runner.py for comprehensive testing")

if __name__ == "__main__":
    main()
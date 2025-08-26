"""
Post-Quantum Migration Assessment and Planning Tools
Comprehensive tools for assessing quantum readiness and planning migration to post-quantum cryptography
"""

from enum import Enum
from typing import List, Dict, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
import numpy as np
import json
import hashlib
import time
from datetime import datetime, timedelta
import logging
import statistics
from collections import defaultdict, deque

class MigrationPhase(Enum):
    """Post-quantum migration phases"""
    ASSESSMENT = "assessment"
    PLANNING = "planning"
    PILOT_TESTING = "pilot_testing"
    GRADUAL_ROLLOUT = "gradual_rollout"
    FULL_DEPLOYMENT = "full_deployment"
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"

class QuantumThreatLevel(Enum):
    """Quantum threat timeline levels"""
    MINIMAL = "minimal"           # >20 years
    MODERATE = "moderate"         # 10-20 years
    SIGNIFICANT = "significant"   # 5-10 years
    IMMINENT = "imminent"        # 2-5 years
    CRITICAL = "critical"        # <2 years

class CryptographicPrimitive(Enum):
    """Types of cryptographic primitives"""
    SYMMETRIC_ENCRYPTION = "symmetric_encryption"
    ASYMMETRIC_ENCRYPTION = "asymmetric_encryption"
    DIGITAL_SIGNATURES = "digital_signatures"
    KEY_EXCHANGE = "key_exchange"
    HASH_FUNCTIONS = "hash_functions"
    MESSAGE_AUTHENTICATION = "message_authentication"
    PSEUDORANDOM_FUNCTIONS = "pseudorandom_functions"
    ZERO_KNOWLEDGE_PROOFS = "zero_knowledge_proofs"

class PostQuantumAlgorithm(Enum):
    """Post-quantum cryptographic algorithms"""
    # NIST Winners
    KYBER = "kyber"
    DILITHIUM = "dilithium"
    FALCON = "falcon"
    SPHINCS_PLUS = "sphincs_plus"
    
    # NIST Finalists and Alternates
    CLASSIC_MCELIECE = "classic_mceliece"
    NTRU = "ntru"
    SABER = "saber"
    FRODO_KEM = "frodo_kem"
    HQC = "hqc"
    BIKE = "bike"
    RAINBOW = "rainbow"
    GEMSS = "gemss"
    
    # Hash-based signatures
    XMSS = "xmss"
    LMS = "lms"
    
    # Lattice-based
    NEW_HOPE = "new_hope"
    CRYSTALS_SUITE = "crystals_suite"
    
    # Code-based
    MCELIECE = "mceliece"
    
    # Isogeny-based (deprecated due to attacks)
    SIKE = "sike"

class MigrationRisk(Enum):
    """Migration risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SystemType(Enum):
    """Types of systems requiring migration"""
    WEB_APPLICATIONS = "web_applications"
    MOBILE_APPLICATIONS = "mobile_applications"
    IOT_DEVICES = "iot_devices"
    CLOUD_SERVICES = "cloud_services"
    DATABASES = "databases"
    NETWORK_INFRASTRUCTURE = "network_infrastructure"
    EMBEDDED_SYSTEMS = "embedded_systems"
    BLOCKCHAIN_SYSTEMS = "blockchain_systems"
    FINANCIAL_SYSTEMS = "financial_systems"
    GOVERNMENT_SYSTEMS = "government_systems"
    INDUSTRIAL_CONTROL = "industrial_control"
    TELECOMMUNICATIONS = "telecommunications"

@dataclass
class CryptographicAsset:
    """Individual cryptographic asset in the organization"""
    asset_id: str
    name: str
    system_type: SystemType
    crypto_primitive: CryptographicPrimitive
    current_algorithm: str
    key_size: int
    usage_frequency: float  # Operations per day
    criticality_level: int  # 1-10 scale
    quantum_vulnerable: bool
    
    # Dependencies
    dependent_systems: List[str]
    dependent_applications: List[str]
    
    # Performance characteristics
    current_performance_ms: float
    throughput_ops_per_sec: float
    
    # Migration readiness
    migration_complexity: MigrationRisk
    estimated_migration_time_days: int
    migration_cost_estimate: float
    
    # Post-quantum candidates
    recommended_pq_algorithms: List[PostQuantumAlgorithm]
    compatibility_matrix: Dict[PostQuantumAlgorithm, float]
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PostQuantumAlgorithmProfile:
    """Profile of a post-quantum algorithm"""
    algorithm: PostQuantumAlgorithm
    crypto_primitive: CryptographicPrimitive
    security_level: int  # NIST security levels 1-5
    
    # Performance characteristics
    key_generation_time_ms: float
    encryption_time_ms: float
    decryption_time_ms: float
    signature_time_ms: float
    verification_time_ms: float
    
    # Size characteristics
    public_key_size_bytes: int
    private_key_size_bytes: int
    signature_size_bytes: int
    ciphertext_expansion_factor: float
    
    # Implementation characteristics
    hardware_requirements: Dict[str, Any]
    memory_requirements_mb: float
    implementation_maturity: float  # 0-1 scale
    standardization_status: str
    
    # Quantum resistance
    quantum_security_level: int
    known_attacks: List[str]
    attack_complexity: str
    
    # Compatibility
    backward_compatibility: bool
    protocol_compatibility: List[str]
    library_support: List[str]

@dataclass
class MigrationPlan:
    """Comprehensive migration plan"""
    plan_id: str
    organization_name: str
    migration_phase: MigrationPhase
    target_completion_date: datetime
    estimated_cost: float
    estimated_effort_person_months: float
    
    # Risk assessment
    overall_risk_level: MigrationRisk
    quantum_threat_timeline: QuantumThreatLevel
    business_impact_assessment: Dict[str, float]
    
    # Asset prioritization
    critical_assets: List[str]
    medium_priority_assets: List[str]
    low_priority_assets: List[str]
    
    # Migration waves
    wave_1_assets: List[str]  # Immediate
    wave_2_assets: List[str]  # Medium term
    wave_3_assets: List[str]  # Long term
    
    # Algorithm selection
    primary_pq_algorithms: Dict[CryptographicPrimitive, PostQuantumAlgorithm]
    backup_pq_algorithms: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]]
    hybrid_transition_algorithms: Dict[str, Any]
    
    # Implementation strategy
    pilot_systems: List[str]
    testing_framework: Dict[str, Any]
    rollback_procedures: List[str]
    
    # Performance requirements
    performance_benchmarks: Dict[str, float]
    acceptable_performance_degradation: float
    
    # Compliance and standards
    compliance_requirements: List[str]
    certification_needs: List[str]
    audit_schedule: List[datetime]
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MigrationAssessmentResult:
    """Result of post-quantum migration assessment"""
    assessment_id: str
    organization_profile: Dict[str, Any]
    quantum_readiness_score: float  # 0-100
    migration_urgency: QuantumThreatLevel
    
    # Asset analysis
    total_assets_analyzed: int
    quantum_vulnerable_assets: int
    high_priority_assets: int
    migration_ready_assets: int
    
    # Algorithm recommendations
    recommended_algorithms: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]]
    algorithm_selection_rationale: Dict[str, str]
    
    # Timeline and effort
    estimated_migration_duration_months: float
    estimated_total_cost: float
    resource_requirements: Dict[str, float]
    
    # Risk analysis
    identified_risks: List[Dict[str, Any]]
    mitigation_strategies: List[str]
    contingency_plans: List[str]
    
    # Performance impact
    expected_performance_changes: Dict[str, float]
    bottleneck_analysis: List[str]
    optimization_opportunities: List[str]
    
    # Compliance and certification
    compliance_gaps: List[str]
    certification_roadmap: List[Dict[str, Any]]
    
    # Migration plan
    recommended_migration_plan: MigrationPlan
    alternative_plans: List[MigrationPlan]
    
    source_identifier: str
    assessment_timestamp: datetime = field(default_factory=datetime.now)

class PostQuantumMigrationAssessor:
    """Comprehensive post-quantum migration assessment tool"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pq_algorithm_profiles = self._initialize_pq_algorithm_profiles()
        self.migration_benchmarks = self._initialize_migration_benchmarks()
        self.compliance_frameworks = self._initialize_compliance_frameworks()
        self.threat_intelligence = self._initialize_threat_intelligence()
        
    def _initialize_pq_algorithm_profiles(self) -> Dict[PostQuantumAlgorithm, PostQuantumAlgorithmProfile]:
        """Initialize post-quantum algorithm profiles with real-world data"""
        profiles = {}
        
        # KYBER - Key encapsulation
        profiles[PostQuantumAlgorithm.KYBER] = PostQuantumAlgorithmProfile(
            algorithm=PostQuantumAlgorithm.KYBER,
            crypto_primitive=CryptographicPrimitive.KEY_EXCHANGE,
            security_level=3,  # NIST Level 3 (192-bit security)
            key_generation_time_ms=0.15,
            encryption_time_ms=0.12,
            decryption_time_ms=0.15,
            signature_time_ms=0.0,  # Not applicable
            verification_time_ms=0.0,
            public_key_size_bytes=1568,
            private_key_size_bytes=2400,
            signature_size_bytes=0,
            ciphertext_expansion_factor=1.1,
            hardware_requirements={"cpu_cores": 1, "ram_mb": 4, "crypto_acceleration": False},
            memory_requirements_mb=2.0,
            implementation_maturity=0.95,
            standardization_status="NIST_WINNER_2022",
            quantum_security_level=192,
            known_attacks=["lattice_reduction", "enumeration"],
            attack_complexity="exponential",
            backward_compatibility=False,
            protocol_compatibility=["TLS", "IKE", "SSH"],
            library_support=["OpenSSL", "BoringSSL", "liboqs"]
        )
        
        # DILITHIUM - Digital signatures
        profiles[PostQuantumAlgorithm.DILITHIUM] = PostQuantumAlgorithmProfile(
            algorithm=PostQuantumAlgorithm.DILITHIUM,
            crypto_primitive=CryptographicPrimitive.DIGITAL_SIGNATURES,
            security_level=3,
            key_generation_time_ms=0.8,
            encryption_time_ms=0.0,
            decryption_time_ms=0.0,
            signature_time_ms=1.2,
            verification_time_ms=0.3,
            public_key_size_bytes=1952,
            private_key_size_bytes=4000,
            signature_size_bytes=3293,
            ciphertext_expansion_factor=1.0,
            hardware_requirements={"cpu_cores": 1, "ram_mb": 8, "crypto_acceleration": True},
            memory_requirements_mb=4.0,
            implementation_maturity=0.93,
            standardization_status="NIST_WINNER_2022",
            quantum_security_level=192,
            known_attacks=["fiat_shamir_attacks", "side_channel"],
            attack_complexity="exponential",
            backward_compatibility=False,
            protocol_compatibility=["TLS", "X.509", "OpenPGP"],
            library_support=["OpenSSL", "Bouncy_Castle", "liboqs"]
        )
        
        # FALCON - Compact signatures
        profiles[PostQuantumAlgorithm.FALCON] = PostQuantumAlgorithmProfile(
            algorithm=PostQuantumAlgorithm.FALCON,
            crypto_primitive=CryptographicPrimitive.DIGITAL_SIGNATURES,
            security_level=5,
            key_generation_time_ms=15.0,  # Slower key generation
            encryption_time_ms=0.0,
            decryption_time_ms=0.0,
            signature_time_ms=8.0,
            verification_time_ms=0.15,
            public_key_size_bytes=897,
            private_key_size_bytes=1281,
            signature_size_bytes=690,  # Much smaller signatures
            ciphertext_expansion_factor=1.0,
            hardware_requirements={"cpu_cores": 1, "ram_mb": 16, "crypto_acceleration": True},
            memory_requirements_mb=8.0,
            implementation_maturity=0.88,
            standardization_status="NIST_WINNER_2022",
            quantum_security_level=256,
            known_attacks=["gaussian_sampling_attacks"],
            attack_complexity="exponential",
            backward_compatibility=False,
            protocol_compatibility=["TLS", "X.509", "Code_Signing"],
            library_support=["liboqs", "PQCLEAN"]
        )
        
        # SPHINCS+ - Hash-based signatures
        profiles[PostQuantumAlgorithm.SPHINCS_PLUS] = PostQuantumAlgorithmProfile(
            algorithm=PostQuantumAlgorithm.SPHINCS_PLUS,
            crypto_primitive=CryptographicPrimitive.DIGITAL_SIGNATURES,
            security_level=5,
            key_generation_time_ms=2.0,
            encryption_time_ms=0.0,
            decryption_time_ms=0.0,
            signature_time_ms=50.0,  # Very slow signing
            verification_time_ms=1.5,
            public_key_size_bytes=64,
            private_key_size_bytes=128,
            signature_size_bytes=49856,  # Very large signatures
            ciphertext_expansion_factor=1.0,
            hardware_requirements={"cpu_cores": 2, "ram_mb": 32, "crypto_acceleration": False},
            memory_requirements_mb=16.0,
            implementation_maturity=0.95,
            standardization_status="NIST_WINNER_2022",
            quantum_security_level=256,
            known_attacks=["collision_attacks", "preimage_attacks"],
            attack_complexity="exponential",
            backward_compatibility=False,
            protocol_compatibility=["TLS", "X.509", "Long_term_signatures"],
            library_support=["OpenSSL", "liboqs", "SPHINCS_reference"]
        )
        
        # Classic McEliece - Code-based
        profiles[PostQuantumAlgorithm.CLASSIC_MCELIECE] = PostQuantumAlgorithmProfile(
            algorithm=PostQuantumAlgorithm.CLASSIC_MCELIECE,
            crypto_primitive=CryptographicPrimitive.KEY_EXCHANGE,
            security_level=5,
            key_generation_time_ms=100.0,  # Very slow key generation
            encryption_time_ms=0.1,
            decryption_time_ms=0.8,
            signature_time_ms=0.0,
            verification_time_ms=0.0,
            public_key_size_bytes=1357824,  # Very large keys
            private_key_size_bytes=13892,
            signature_size_bytes=0,
            ciphertext_expansion_factor=1.0,
            hardware_requirements={"cpu_cores": 2, "ram_mb": 64, "crypto_acceleration": False},
            memory_requirements_mb=32.0,
            implementation_maturity=0.85,
            standardization_status="NIST_ALTERNATE_2022",
            quantum_security_level=256,
            known_attacks=["information_set_decoding"],
            attack_complexity="exponential",
            backward_compatibility=False,
            protocol_compatibility=["TLS", "IKE"],
            library_support=["liboqs", "PQCLEAN"]
        )
        
        return profiles
    
    def _initialize_migration_benchmarks(self) -> Dict[str, Any]:
        """Initialize migration benchmarks and best practices"""
        return {
            "assessment_duration_weeks": {
                "small_org": 2,
                "medium_org": 6,
                "large_org": 12,
                "enterprise": 20
            },
            "migration_duration_months": {
                "pilot": 3,
                "gradual_rollout": 12,
                "full_deployment": 24,
                "optimization": 6
            },
            "cost_per_asset_usd": {
                "web_application": 5000,
                "mobile_app": 8000,
                "iot_device": 15000,
                "database": 12000,
                "network_infrastructure": 25000,
                "embedded_system": 30000
            },
            "performance_expectations": {
                "acceptable_slowdown": 2.0,
                "target_availability": 0.999,
                "rollback_time_minutes": 30
            }
        }
    
    def _initialize_compliance_frameworks(self) -> Dict[str, List[str]]:
        """Initialize compliance frameworks and requirements"""
        return {
            "NIST": [
                "NIST_SP_800-208",
                "NIST_SP_800-56C",
                "FIPS_140-3",
                "NIST_Cybersecurity_Framework"
            ],
            "CNSS": [
                "CNSS_Policy_15",
                "CNSSI_1253"
            ],
            "BSI": [
                "BSI_TR-02102",
                "Common_Criteria"
            ],
            "ANSSI": [
                "ANSSI_Guidelines",
                "SecNum_Cloud"
            ],
            "Industry": [
                "PCI_DSS",
                "HIPAA",
                "SOX",
                "GDPR",
                "ISO_27001"
            ]
        }
    
    def _initialize_threat_intelligence(self) -> Dict[str, Any]:
        """Initialize quantum threat intelligence"""
        return {
            "quantum_computer_progress": {
                "current_logical_qubits": 1000,
                "fault_tolerant_timeline": "2030-2035",
                "cryptanalytic_timeline": "2035-2040"
            },
            "algorithm_vulnerabilities": {
                "rsa_2048": {"threat_level": "critical", "timeline": "2030"},
                "ecc_p256": {"threat_level": "critical", "timeline": "2030"},
                "dh_2048": {"threat_level": "critical", "timeline": "2030"},
                "aes_128": {"threat_level": "moderate", "timeline": "2040"}
            },
            "attack_capabilities": {
                "shors_algorithm": {"current_capability": "limited", "full_capability": "2035"},
                "grovers_algorithm": {"current_capability": "theoretical", "full_capability": "2040"}
            }
        }
    
    def perform_comprehensive_assessment(self, organization_data: Dict[str, Any], 
                                       source_identifier: str) -> MigrationAssessmentResult:
        """Perform comprehensive post-quantum migration assessment"""
        
        try:
            # Extract cryptographic assets
            crypto_assets = self._discover_cryptographic_assets(organization_data)
            
            # Assess quantum vulnerability
            vulnerability_analysis = self._assess_quantum_vulnerability(crypto_assets)
            
            # Calculate quantum readiness score
            readiness_score = self._calculate_quantum_readiness_score(crypto_assets, vulnerability_analysis)
            
            # Determine migration urgency
            migration_urgency = self._assess_migration_urgency(vulnerability_analysis, organization_data)
            
            # Generate algorithm recommendations
            algorithm_recommendations = self._recommend_post_quantum_algorithms(crypto_assets)
            
            # Estimate migration timeline and cost
            timeline_cost_analysis = self._estimate_migration_timeline_cost(crypto_assets, organization_data)
            
            # Identify risks and mitigation strategies
            risk_analysis = self._analyze_migration_risks(crypto_assets, organization_data)
            
            # Assess performance impact
            performance_analysis = self._analyze_performance_impact(crypto_assets, algorithm_recommendations)
            
            # Check compliance requirements
            compliance_analysis = self._analyze_compliance_requirements(organization_data)
            
            # Generate migration plans
            migration_plans = self._generate_migration_plans(crypto_assets, algorithm_recommendations, 
                                                            timeline_cost_analysis, organization_data)
            
            # Create assessment result
            assessment_result = MigrationAssessmentResult(
                assessment_id=f"pq_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                organization_profile=self._create_organization_profile(organization_data),
                quantum_readiness_score=readiness_score,
                migration_urgency=migration_urgency,
                total_assets_analyzed=len(crypto_assets),
                quantum_vulnerable_assets=vulnerability_analysis["vulnerable_count"],
                high_priority_assets=vulnerability_analysis["high_priority_count"],
                migration_ready_assets=vulnerability_analysis["migration_ready_count"],
                recommended_algorithms=algorithm_recommendations,
                algorithm_selection_rationale=self._generate_algorithm_rationale(algorithm_recommendations),
                estimated_migration_duration_months=timeline_cost_analysis["duration_months"],
                estimated_total_cost=timeline_cost_analysis["total_cost"],
                resource_requirements=timeline_cost_analysis["resource_requirements"],
                identified_risks=risk_analysis["risks"],
                mitigation_strategies=risk_analysis["mitigation_strategies"],
                contingency_plans=risk_analysis["contingency_plans"],
                expected_performance_changes=performance_analysis["performance_changes"],
                bottleneck_analysis=performance_analysis["bottlenecks"],
                optimization_opportunities=performance_analysis["optimizations"],
                compliance_gaps=compliance_analysis["gaps"],
                certification_roadmap=compliance_analysis["roadmap"],
                recommended_migration_plan=migration_plans[0],
                alternative_plans=migration_plans[1:],
                source_identifier=source_identifier
            )
            
            self.logger.info(f"Completed post-quantum migration assessment for {organization_data.get('name', 'organization')}")
            
            return assessment_result
            
        except Exception as e:
            self.logger.error(f"Error performing migration assessment: {str(e)}")
            raise
    
    def _discover_cryptographic_assets(self, org_data: Dict[str, Any]) -> List[CryptographicAsset]:
        """Discover and catalog cryptographic assets"""
        assets = []
        
        # Parse systems and applications
        systems = org_data.get('systems', [])
        applications = org_data.get('applications', [])
        
        for system in systems:
            # Extract crypto usage patterns
            crypto_usage = system.get('cryptography', {})
            
            for crypto_type, details in crypto_usage.items():
                asset = CryptographicAsset(
                    asset_id=f"asset_{hashlib.md5(f'{system['name']}_{crypto_type}'.encode()).hexdigest()[:8]}",
                    name=f"{system['name']}_{crypto_type}",
                    system_type=SystemType(system.get('type', 'web_applications')),
                    crypto_primitive=self._map_crypto_primitive(crypto_type),
                    current_algorithm=details.get('algorithm', 'unknown'),
                    key_size=details.get('key_size', 0),
                    usage_frequency=details.get('usage_frequency', 1000),
                    criticality_level=system.get('criticality', 5),
                    quantum_vulnerable=self._is_quantum_vulnerable(details.get('algorithm', '')),
                    dependent_systems=system.get('dependencies', []),
                    dependent_applications=system.get('applications', []),
                    current_performance_ms=details.get('performance_ms', 10.0),
                    throughput_ops_per_sec=details.get('throughput', 100.0),
                    migration_complexity=MigrationRisk(details.get('migration_risk', 'medium')),
                    estimated_migration_time_days=details.get('migration_days', 30),
                    migration_cost_estimate=details.get('migration_cost', 10000.0),
                    recommended_pq_algorithms=[],
                    compatibility_matrix={}
                )
                assets.append(asset)
        
        # Add default assets if none found
        if not assets:
            assets = self._generate_default_crypto_assets(org_data)
        
        return assets
    
    def _map_crypto_primitive(self, crypto_type: str) -> CryptographicPrimitive:
        """Map crypto type string to CryptographicPrimitive"""
        mapping = {
            'tls': CryptographicPrimitive.ASYMMETRIC_ENCRYPTION,
            'ssl': CryptographicPrimitive.ASYMMETRIC_ENCRYPTION,
            'ssh': CryptographicPrimitive.KEY_EXCHANGE,
            'rsa': CryptographicPrimitive.ASYMMETRIC_ENCRYPTION,
            'ecc': CryptographicPrimitive.ASYMMETRIC_ENCRYPTION,
            'ecdsa': CryptographicPrimitive.DIGITAL_SIGNATURES,
            'dh': CryptographicPrimitive.KEY_EXCHANGE,
            'ecdh': CryptographicPrimitive.KEY_EXCHANGE,
            'aes': CryptographicPrimitive.SYMMETRIC_ENCRYPTION,
            'sha': CryptographicPrimitive.HASH_FUNCTIONS,
            'hmac': CryptographicPrimitive.MESSAGE_AUTHENTICATION
        }
        
        for key, primitive in mapping.items():
            if key in crypto_type.lower():
                return primitive
        
        return CryptographicPrimitive.SYMMETRIC_ENCRYPTION
    
    def _is_quantum_vulnerable(self, algorithm: str) -> bool:
        """Determine if an algorithm is quantum vulnerable"""
        vulnerable_algorithms = [
            'rsa', 'ecc', 'ecdsa', 'ecdh', 'dh', 'dsa', 
            'elgamal', 'diffie_hellman', 'elliptic_curve'
        ]
        
        algorithm_lower = algorithm.lower()
        return any(vuln in algorithm_lower for vuln in vulnerable_algorithms)
    
    def _generate_default_crypto_assets(self, org_data: Dict[str, Any]) -> List[CryptographicAsset]:
        """Generate default cryptographic assets based on organization type"""
        assets = []
        org_type = org_data.get('type', 'enterprise')
        org_size = org_data.get('size', 'medium')
        
        # Common assets for most organizations
        common_assets = [
            {
                'name': 'Web_TLS_Certificates',
                'system_type': SystemType.WEB_APPLICATIONS,
                'crypto_primitive': CryptographicPrimitive.ASYMMETRIC_ENCRYPTION,
                'algorithm': 'RSA-2048',
                'criticality': 9
            },
            {
                'name': 'Database_Encryption',
                'system_type': SystemType.DATABASES,
                'crypto_primitive': CryptographicPrimitive.SYMMETRIC_ENCRYPTION,
                'algorithm': 'AES-256',
                'criticality': 8
            },
            {
                'name': 'Email_Signatures',
                'system_type': SystemType.WEB_APPLICATIONS,
                'crypto_primitive': CryptographicPrimitive.DIGITAL_SIGNATURES,
                'algorithm': 'RSA-2048',
                'criticality': 7
            },
            {
                'name': 'API_Authentication',
                'system_type': SystemType.CLOUD_SERVICES,
                'crypto_primitive': CryptographicPrimitive.DIGITAL_SIGNATURES,
                'algorithm': 'ECDSA-P256',
                'criticality': 8
            }
        ]
        
        for i, asset_data in enumerate(common_assets):
            asset = CryptographicAsset(
                asset_id=f"default_asset_{i}",
                name=asset_data['name'],
                system_type=asset_data['system_type'],
                crypto_primitive=asset_data['crypto_primitive'],
                current_algorithm=asset_data['algorithm'],
                key_size=2048 if 'RSA' in asset_data['algorithm'] else 256,
                usage_frequency=np.random.uniform(100, 10000),
                criticality_level=asset_data['criticality'],
                quantum_vulnerable=self._is_quantum_vulnerable(asset_data['algorithm']),
                dependent_systems=[],
                dependent_applications=[],
                current_performance_ms=np.random.uniform(1.0, 50.0),
                throughput_ops_per_sec=np.random.uniform(50.0, 1000.0),
                migration_complexity=MigrationRisk.MEDIUM,
                estimated_migration_time_days=np.random.randint(14, 90),
                migration_cost_estimate=np.random.uniform(5000, 25000),
                recommended_pq_algorithms=[],
                compatibility_matrix={}
            )
            assets.append(asset)
        
        return assets
    
    def _assess_quantum_vulnerability(self, assets: List[CryptographicAsset]) -> Dict[str, Any]:
        """Assess quantum vulnerability across all assets"""
        
        vulnerable_assets = [asset for asset in assets if asset.quantum_vulnerable]
        high_priority = [asset for asset in vulnerable_assets if asset.criticality_level >= 8]
        migration_ready = [asset for asset in vulnerable_assets 
                          if asset.migration_complexity in [MigrationRisk.LOW, MigrationRisk.MEDIUM]]
        
        vulnerability_score = len(vulnerable_assets) / len(assets) if assets else 0
        criticality_score = sum(asset.criticality_level for asset in vulnerable_assets) / max(len(vulnerable_assets) * 10, 1)
        
        return {
            "vulnerable_count": len(vulnerable_assets),
            "high_priority_count": len(high_priority),
            "migration_ready_count": len(migration_ready),
            "vulnerability_score": vulnerability_score,
            "criticality_score": criticality_score,
            "vulnerable_systems": [asset.system_type.value for asset in vulnerable_assets],
            "critical_primitives": [asset.crypto_primitive.value for asset in high_priority]
        }
    
    def _calculate_quantum_readiness_score(self, assets: List[CryptographicAsset], 
                                         vulnerability_analysis: Dict[str, Any]) -> float:
        """Calculate overall quantum readiness score (0-100)"""
        
        if not assets:
            return 0.0
        
        # Factor 1: Percentage of non-vulnerable assets (40% weight)
        non_vulnerable_ratio = 1.0 - vulnerability_analysis["vulnerability_score"]
        
        # Factor 2: Migration readiness (30% weight)
        migration_ready_ratio = vulnerability_analysis["migration_ready_count"] / max(len(assets), 1)
        
        # Factor 3: Critical asset protection (20% weight)
        critical_assets = [asset for asset in assets if asset.criticality_level >= 8]
        critical_protected_ratio = len([asset for asset in critical_assets if not asset.quantum_vulnerable]) / max(len(critical_assets), 1)
        
        # Factor 4: Implementation maturity (10% weight)
        # Simulate based on organization characteristics
        implementation_maturity = 0.3  # Default low maturity
        
        readiness_score = (
            non_vulnerable_ratio * 40 +
            migration_ready_ratio * 30 +
            critical_protected_ratio * 20 +
            implementation_maturity * 10
        )
        
        return min(readiness_score, 100.0)
    
    def _assess_migration_urgency(self, vulnerability_analysis: Dict[str, Any], 
                                org_data: Dict[str, Any]) -> QuantumThreatLevel:
        """Assess migration urgency based on threat landscape and organization profile"""
        
        vulnerability_score = vulnerability_analysis["vulnerability_score"]
        criticality_score = vulnerability_analysis["criticality_score"]
        
        # Organization risk factors
        org_type = org_data.get('type', 'enterprise')
        industry = org_data.get('industry', 'technology')
        data_sensitivity = org_data.get('data_sensitivity', 'medium')
        
        # Calculate urgency score
        urgency_score = 0.0
        
        # Vulnerability impact (40% weight)
        urgency_score += vulnerability_score * 40
        
        # Criticality impact (30% weight)
        urgency_score += criticality_score * 30
        
        # Organization risk factors (30% weight)
        risk_multiplier = 1.0
        
        if org_type in ['government', 'defense', 'financial']:
            risk_multiplier = 1.5
        elif industry in ['finance', 'healthcare', 'defense', 'government']:
            risk_multiplier = 1.3
        elif data_sensitivity == 'high':
            risk_multiplier = 1.2
        
        urgency_score += 30 * (risk_multiplier - 1.0)
        
        # Map to threat levels
        if urgency_score >= 80:
            return QuantumThreatLevel.CRITICAL
        elif urgency_score >= 60:
            return QuantumThreatLevel.IMMINENT
        elif urgency_score >= 40:
            return QuantumThreatLevel.SIGNIFICANT
        elif urgency_score >= 20:
            return QuantumThreatLevel.MODERATE
        else:
            return QuantumThreatLevel.MINIMAL
    
    def _recommend_post_quantum_algorithms(self, assets: List[CryptographicAsset]) -> Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]]:
        """Recommend post-quantum algorithms for each cryptographic primitive"""
        
        recommendations = {}
        
        # Group assets by primitive
        primitive_assets = defaultdict(list)
        for asset in assets:
            if asset.quantum_vulnerable:
                primitive_assets[asset.crypto_primitive].append(asset)
        
        for primitive, primitive_asset_list in primitive_assets.items():
            recommendations[primitive] = self._select_algorithms_for_primitive(primitive, primitive_asset_list)
        
        return recommendations
    
    def _select_algorithms_for_primitive(self, primitive: CryptographicPrimitive, 
                                       assets: List[CryptographicAsset]) -> List[PostQuantumAlgorithm]:
        """Select best post-quantum algorithms for a specific primitive"""
        
        # Get available algorithms for this primitive
        available_algorithms = [
            alg for alg, profile in self.pq_algorithm_profiles.items()
            if profile.crypto_primitive == primitive
        ]
        
        if not available_algorithms:
            return []
        
        # Score algorithms based on asset requirements
        algorithm_scores = {}
        
        for algorithm in available_algorithms:
            profile = self.pq_algorithm_profiles[algorithm]
            score = 0.0
            
            # Performance score (30% weight)
            avg_performance_requirement = np.mean([asset.current_performance_ms for asset in assets])
            if primitive == CryptographicPrimitive.DIGITAL_SIGNATURES:
                alg_performance = profile.signature_time_ms + profile.verification_time_ms
            elif primitive == CryptographicPrimitive.KEY_EXCHANGE:
                alg_performance = profile.encryption_time_ms + profile.decryption_time_ms
            else:
                alg_performance = profile.key_generation_time_ms
            
            if alg_performance <= avg_performance_requirement * 2:  # Within 2x current performance
                performance_score = max(0, 1.0 - alg_performance / (avg_performance_requirement * 4))
            else:
                performance_score = 0.1  # Poor performance
            
            score += performance_score * 30
            
            # Security score (25% weight)
            security_score = profile.quantum_security_level / 256  # Normalize to 0-1
            score += security_score * 25
            
            # Maturity score (20% weight)
            score += profile.implementation_maturity * 20
            
            # Compatibility score (15% weight)
            compatibility_score = len(profile.protocol_compatibility) / 5  # Max 5 protocols
            score += min(compatibility_score, 1.0) * 15
            
            # Size efficiency score (10% weight)
            if primitive == CryptographicPrimitive.DIGITAL_SIGNATURES:
                size_penalty = profile.signature_size_bytes / 10000  # Penalty for large signatures
            else:
                size_penalty = profile.public_key_size_bytes / 10000  # Penalty for large keys
            
            size_score = max(0, 1.0 - size_penalty)
            score += size_score * 10
            
            algorithm_scores[algorithm] = score
        
        # Return top 3 algorithms
        sorted_algorithms = sorted(algorithm_scores.items(), key=lambda x: x[1], reverse=True)
        return [alg for alg, score in sorted_algorithms[:3]]
    
    def _estimate_migration_timeline_cost(self, assets: List[CryptographicAsset], 
                                        org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate migration timeline and costs"""
        
        vulnerable_assets = [asset for asset in assets if asset.quantum_vulnerable]
        
        if not vulnerable_assets:
            return {
                "duration_months": 0,
                "total_cost": 0,
                "resource_requirements": {}
            }
        
        # Timeline estimation
        total_migration_days = sum(asset.estimated_migration_time_days for asset in vulnerable_assets)
        
        # Account for parallel work and dependencies
        org_size = org_data.get('size', 'medium')
        parallel_factor = {
            'small': 0.8,    # Limited parallelization
            'medium': 0.6,   # Some parallel work
            'large': 0.4,    # Good parallelization
            'enterprise': 0.3  # Extensive parallel work
        }.get(org_size, 0.6)
        
        actual_duration_days = total_migration_days * parallel_factor
        duration_months = actual_duration_days / 30
        
        # Add phases overhead
        phases_overhead_months = {
            'assessment': 1,
            'planning': 2,
            'pilot_testing': 3,
            'validation': 2,
            'optimization': 1
        }
        
        total_duration = duration_months + sum(phases_overhead_months.values())
        
        # Cost estimation
        base_cost = sum(asset.migration_cost_estimate for asset in vulnerable_assets)
        
        # Add overhead costs
        overhead_multiplier = {
            'small': 1.2,
            'medium': 1.4,
            'large': 1.6,
            'enterprise': 1.8
        }.get(org_size, 1.4)
        
        total_cost = base_cost * overhead_multiplier
        
        # Resource requirements
        avg_criticality = np.mean([asset.criticality_level for asset in vulnerable_assets])
        resource_requirements = {
            "crypto_engineers": max(2, len(vulnerable_assets) // 10),
            "security_architects": max(1, len(vulnerable_assets) // 20),
            "qa_engineers": max(2, len(vulnerable_assets) // 15),
            "devops_engineers": max(1, len(vulnerable_assets) // 25),
            "project_managers": max(1, avg_criticality // 5)
        }
        
        return {
            "duration_months": total_duration,
            "total_cost": total_cost,
            "resource_requirements": resource_requirements,
            "parallel_factor": parallel_factor,
            "phases_breakdown": phases_overhead_months
        }
    
    def _analyze_migration_risks(self, assets: List[CryptographicAsset], 
                               org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze migration risks and generate mitigation strategies"""
        
        risks = []
        mitigation_strategies = []
        contingency_plans = []
        
        # Performance risk analysis
        high_throughput_assets = [asset for asset in assets if asset.throughput_ops_per_sec > 1000]
        if high_throughput_assets:
            risks.append({
                "type": "performance_degradation",
                "likelihood": "high",
                "impact": "medium",
                "description": f"{len(high_throughput_assets)} high-throughput systems may experience performance issues",
                "affected_assets": [asset.asset_id for asset in high_throughput_assets]
            })
            mitigation_strategies.append("Implement performance testing and optimization before deployment")
            contingency_plans.append("Maintain hybrid classical-quantum systems during transition")
        
        # Compatibility risk analysis
        legacy_systems = [asset for asset in assets if asset.system_type in [SystemType.EMBEDDED_SYSTEMS, SystemType.IOT_DEVICES]]
        if legacy_systems:
            risks.append({
                "type": "compatibility_issues",
                "likelihood": "medium",
                "impact": "high",
                "description": f"{len(legacy_systems)} legacy systems may have compatibility issues",
                "affected_assets": [asset.asset_id for asset in legacy_systems]
            })
            mitigation_strategies.append("Develop compatibility layers and protocol bridges")
            contingency_plans.append("Plan for system replacement if migration is not feasible")
        
        # Implementation risk analysis
        complex_migrations = [asset for asset in assets if asset.migration_complexity == MigrationRisk.HIGH]
        if complex_migrations:
            risks.append({
                "type": "implementation_complexity",
                "likelihood": "medium",
                "impact": "high",
                "description": f"{len(complex_migrations)} systems have high migration complexity",
                "affected_assets": [asset.asset_id for asset in complex_migrations]
            })
            mitigation_strategies.append("Establish dedicated migration teams and extended testing phases")
            contingency_plans.append("Implement gradual rollback procedures for complex systems")
        
        # Timeline risk analysis
        critical_assets = [asset for asset in assets if asset.criticality_level >= 9]
        if critical_assets:
            risks.append({
                "type": "timeline_pressure",
                "likelihood": "high",
                "impact": "critical",
                "description": f"{len(critical_assets)} critical systems require immediate attention",
                "affected_assets": [asset.asset_id for asset in critical_assets]
            })
            mitigation_strategies.append("Prioritize critical systems and implement parallel migration tracks")
            contingency_plans.append("Develop emergency quantum-safe deployment procedures")
        
        return {
            "risks": risks,
            "mitigation_strategies": mitigation_strategies,
            "contingency_plans": contingency_plans
        }
    
    def _analyze_performance_impact(self, assets: List[CryptographicAsset], 
                                  recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]]) -> Dict[str, Any]:
        """Analyze expected performance impact of migration"""
        
        performance_changes = {}
        bottlenecks = []
        optimizations = []
        
        for asset in assets:
            if not asset.quantum_vulnerable:
                continue
            
            recommended_algs = recommendations.get(asset.crypto_primitive, [])
            if not recommended_algs:
                continue
            
            primary_alg = recommended_algs[0]
            profile = self.pq_algorithm_profiles[primary_alg]
            
            # Calculate performance impact
            if asset.crypto_primitive == CryptographicPrimitive.DIGITAL_SIGNATURES:
                current_perf = asset.current_performance_ms
                new_perf = profile.signature_time_ms + profile.verification_time_ms
                performance_ratio = new_perf / current_perf
            elif asset.crypto_primitive == CryptographicPrimitive.KEY_EXCHANGE:
                current_perf = asset.current_performance_ms
                new_perf = profile.encryption_time_ms + profile.decryption_time_ms
                performance_ratio = new_perf / current_perf
            else:
                performance_ratio = 1.2  # Default modest impact
            
            performance_changes[asset.asset_id] = {
                "current_ms": asset.current_performance_ms,
                "projected_ms": asset.current_performance_ms * performance_ratio,
                "ratio": performance_ratio,
                "algorithm": primary_alg.value
            }
            
            # Identify bottlenecks
            if performance_ratio > 5.0:
                bottlenecks.append(f"{asset.name}: {performance_ratio:.1f}x slower with {primary_alg.value}")
            
            # Identify optimization opportunities
            if len(recommended_algs) > 1:
                alternative = recommended_algs[1]
                alt_profile = self.pq_algorithm_profiles[alternative]
                optimizations.append(f"{asset.name}: Consider {alternative.value} for better performance")
        
        return {
            "performance_changes": performance_changes,
            "bottlenecks": bottlenecks,
            "optimizations": optimizations
        }
    
    def _analyze_compliance_requirements(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compliance requirements and gaps"""
        
        industry = org_data.get('industry', 'technology')
        org_type = org_data.get('type', 'enterprise')
        jurisdiction = org_data.get('jurisdiction', 'US')
        
        # Determine applicable compliance frameworks
        applicable_frameworks = []
        
        if org_type in ['government', 'defense']:
            applicable_frameworks.extend(['NIST', 'CNSS'])
        
        if industry in ['finance', 'banking']:
            applicable_frameworks.extend(['PCI_DSS', 'SOX'])
        elif industry == 'healthcare':
            applicable_frameworks.extend(['HIPAA'])
        elif industry == 'technology':
            applicable_frameworks.extend(['SOC2', 'ISO_27001'])
        
        if jurisdiction == 'EU':
            applicable_frameworks.append('GDPR')
        
        # Default frameworks
        if not applicable_frameworks:
            applicable_frameworks = ['NIST', 'ISO_27001']
        
        # Identify compliance gaps
        gaps = []
        roadmap = []
        
        for framework in applicable_frameworks:
            if framework == 'NIST':
                gaps.append("Post-quantum cryptography migration plan required by 2030")
                roadmap.append({
                    "framework": "NIST",
                    "requirement": "SP 800-208 compliance",
                    "deadline": "2030-01-01",
                    "action": "Implement NIST-approved post-quantum algorithms"
                })
            elif framework == 'PCI_DSS':
                gaps.append("Payment system cryptography must be quantum-safe")
                roadmap.append({
                    "framework": "PCI_DSS",
                    "requirement": "Strong cryptography requirement",
                    "deadline": "2028-01-01",
                    "action": "Migrate payment processing to post-quantum cryptography"
                })
        
        return {
            "applicable_frameworks": applicable_frameworks,
            "gaps": gaps,
            "roadmap": roadmap
        }
    
    def _generate_migration_plans(self, assets: List[CryptographicAsset], 
                                recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]],
                                timeline_cost: Dict[str, Any], 
                                org_data: Dict[str, Any]) -> List[MigrationPlan]:
        """Generate multiple migration plan options"""
        
        plans = []
        
        # Plan 1: Conservative approach
        conservative_plan = self._create_conservative_migration_plan(
            assets, recommendations, timeline_cost, org_data
        )
        plans.append(conservative_plan)
        
        # Plan 2: Aggressive approach
        aggressive_plan = self._create_aggressive_migration_plan(
            assets, recommendations, timeline_cost, org_data
        )
        plans.append(aggressive_plan)
        
        # Plan 3: Balanced approach (recommended)
        balanced_plan = self._create_balanced_migration_plan(
            assets, recommendations, timeline_cost, org_data
        )
        plans.insert(0, balanced_plan)  # Make it the primary recommendation
        
        return plans
    
    def _create_conservative_migration_plan(self, assets: List[CryptographicAsset], 
                                          recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]],
                                          timeline_cost: Dict[str, Any], 
                                          org_data: Dict[str, Any]) -> MigrationPlan:
        """Create a conservative migration plan"""
        
        vulnerable_assets = [asset for asset in assets if asset.quantum_vulnerable]
        critical_assets = [asset for asset in vulnerable_assets if asset.criticality_level >= 8]
        
        return MigrationPlan(
            plan_id="conservative_migration_plan",
            organization_name=org_data.get('name', 'Organization'),
            migration_phase=MigrationPhase.ASSESSMENT,
            target_completion_date=datetime.now() + timedelta(days=int(timeline_cost["duration_months"] * 30 * 1.5)),
            estimated_cost=timeline_cost["total_cost"] * 1.3,  # Conservative cost estimate
            estimated_effort_person_months=timeline_cost["duration_months"] * 1.2,
            overall_risk_level=MigrationRisk.LOW,
            quantum_threat_timeline=QuantumThreatLevel.MODERATE,
            business_impact_assessment={
                "availability_impact": 0.05,
                "performance_impact": 0.10,
                "cost_impact": 0.30
            },
            critical_assets=[asset.asset_id for asset in critical_assets],
            medium_priority_assets=[asset.asset_id for asset in vulnerable_assets if asset.criticality_level >= 5 and asset not in critical_assets],
            low_priority_assets=[asset.asset_id for asset in vulnerable_assets if asset.criticality_level < 5],
            wave_1_assets=[asset.asset_id for asset in critical_assets[:len(critical_assets)//3] if critical_assets],
            wave_2_assets=[asset.asset_id for asset in critical_assets[len(critical_assets)//3:] if critical_assets],
            wave_3_assets=[asset.asset_id for asset in vulnerable_assets if asset not in critical_assets],
            primary_pq_algorithms={
                primitive: algs[0] if algs else PostQuantumAlgorithm.KYBER
                for primitive, algs in recommendations.items()
            },
            backup_pq_algorithms={
                primitive: algs[1:] if len(algs) > 1 else []
                for primitive, algs in recommendations.items()
            },
            hybrid_transition_algorithms={"hybrid_rsa_kyber": True, "hybrid_ecdsa_dilithium": True},
            pilot_systems=critical_assets[:2] if len(critical_assets) >= 2 else critical_assets,
            testing_framework={
                "unit_testing": "comprehensive",
                "integration_testing": "extensive",
                "performance_testing": "thorough",
                "security_testing": "rigorous"
            },
            rollback_procedures=["automated_rollback", "manual_rollback", "emergency_procedures"],
            performance_benchmarks={
                "acceptable_slowdown": 1.5,
                "target_availability": 0.9999
            },
            acceptable_performance_degradation=0.5,
            compliance_requirements=["NIST_SP_800-208", "FIPS_140-3"],
            certification_needs=["Common_Criteria", "FIPS_Validation"],
            audit_schedule=[
                datetime.now() + timedelta(days=90),
                datetime.now() + timedelta(days=180),
                datetime.now() + timedelta(days=365)
            ]
        )
    
    def _create_aggressive_migration_plan(self, assets: List[CryptographicAsset], 
                                        recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]],
                                        timeline_cost: Dict[str, Any], 
                                        org_data: Dict[str, Any]) -> MigrationPlan:
        """Create an aggressive migration plan"""
        
        vulnerable_assets = [asset for asset in assets if asset.quantum_vulnerable]
        
        return MigrationPlan(
            plan_id="aggressive_migration_plan",
            organization_name=org_data.get('name', 'Organization'),
            migration_phase=MigrationPhase.PLANNING,
            target_completion_date=datetime.now() + timedelta(days=int(timeline_cost["duration_months"] * 30 * 0.7)),
            estimated_cost=timeline_cost["total_cost"] * 0.9,  # Aggressive cost optimization
            estimated_effort_person_months=timeline_cost["duration_months"] * 0.8,
            overall_risk_level=MigrationRisk.HIGH,
            quantum_threat_timeline=QuantumThreatLevel.CRITICAL,
            business_impact_assessment={
                "availability_impact": 0.15,
                "performance_impact": 0.25,
                "cost_impact": 0.20
            },
            critical_assets=[asset.asset_id for asset in vulnerable_assets if asset.criticality_level >= 7],
            medium_priority_assets=[asset.asset_id for asset in vulnerable_assets if asset.criticality_level >= 4],
            low_priority_assets=[asset.asset_id for asset in vulnerable_assets if asset.criticality_level < 4],
            wave_1_assets=[asset.asset_id for asset in vulnerable_assets[:len(vulnerable_assets)//2]],
            wave_2_assets=[asset.asset_id for asset in vulnerable_assets[len(vulnerable_assets)//2:]],
            wave_3_assets=[],  # All assets migrated in first two waves
            primary_pq_algorithms={
                primitive: algs[0] if algs else PostQuantumAlgorithm.KYBER
                for primitive, algs in recommendations.items()
            },
            backup_pq_algorithms={
                primitive: algs[1:2] if len(algs) > 1 else []  # Limited backup options
                for primitive, algs in recommendations.items()
            },
            hybrid_transition_algorithms={},  # No hybrid period
            pilot_systems=vulnerable_assets[:1] if vulnerable_assets else [],  # Minimal pilot
            testing_framework={
                "unit_testing": "standard",
                "integration_testing": "focused",
                "performance_testing": "basic",
                "security_testing": "standard"
            },
            rollback_procedures=["automated_rollback"],
            performance_benchmarks={
                "acceptable_slowdown": 3.0,  # Accept higher performance impact
                "target_availability": 0.999
            },
            acceptable_performance_degradation=1.0,
            compliance_requirements=["NIST_SP_800-208"],
            certification_needs=["FIPS_Validation"],
            audit_schedule=[
                datetime.now() + timedelta(days=180),
                datetime.now() + timedelta(days=365)
            ]
        )
    
    def _create_balanced_migration_plan(self, assets: List[CryptographicAsset], 
                                      recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]],
                                      timeline_cost: Dict[str, Any], 
                                      org_data: Dict[str, Any]) -> MigrationPlan:
        """Create a balanced migration plan (recommended)"""
        
        vulnerable_assets = [asset for asset in assets if asset.quantum_vulnerable]
        critical_assets = [asset for asset in vulnerable_assets if asset.criticality_level >= 8]
        high_priority_assets = [asset for asset in vulnerable_assets if asset.criticality_level >= 6]
        
        return MigrationPlan(
            plan_id="balanced_migration_plan",
            organization_name=org_data.get('name', 'Organization'),
            migration_phase=MigrationPhase.ASSESSMENT,
            target_completion_date=datetime.now() + timedelta(days=int(timeline_cost["duration_months"] * 30)),
            estimated_cost=timeline_cost["total_cost"],
            estimated_effort_person_months=timeline_cost["duration_months"],
            overall_risk_level=MigrationRisk.MEDIUM,
            quantum_threat_timeline=QuantumThreatLevel.SIGNIFICANT,
            business_impact_assessment={
                "availability_impact": 0.08,
                "performance_impact": 0.15,
                "cost_impact": 0.25
            },
            critical_assets=[asset.asset_id for asset in critical_assets],
            medium_priority_assets=[asset.asset_id for asset in high_priority_assets if asset not in critical_assets],
            low_priority_assets=[asset.asset_id for asset in vulnerable_assets if asset not in high_priority_assets],
            wave_1_assets=[asset.asset_id for asset in critical_assets],
            wave_2_assets=[asset.asset_id for asset in high_priority_assets if asset not in critical_assets],
            wave_3_assets=[asset.asset_id for asset in vulnerable_assets if asset not in high_priority_assets],
            primary_pq_algorithms={
                primitive: algs[0] if algs else PostQuantumAlgorithm.KYBER
                for primitive, algs in recommendations.items()
            },
            backup_pq_algorithms={
                primitive: algs[1:] if len(algs) > 1 else []
                for primitive, algs in recommendations.items()
            },
            hybrid_transition_algorithms={"hybrid_rsa_kyber": True},
            pilot_systems=critical_assets[:3] if len(critical_assets) >= 3 else critical_assets,
            testing_framework={
                "unit_testing": "comprehensive",
                "integration_testing": "thorough",
                "performance_testing": "extensive",
                "security_testing": "comprehensive"
            },
            rollback_procedures=["automated_rollback", "manual_rollback"],
            performance_benchmarks={
                "acceptable_slowdown": 2.0,
                "target_availability": 0.9999
            },
            acceptable_performance_degradation=0.7,
            compliance_requirements=["NIST_SP_800-208", "FIPS_140-3", "ISO_27001"],
            certification_needs=["Common_Criteria", "FIPS_Validation"],
            audit_schedule=[
                datetime.now() + timedelta(days=60),
                datetime.now() + timedelta(days=180),
                datetime.now() + timedelta(days=365)
            ]
        )
    
    def _create_organization_profile(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create organization profile summary"""
        return {
            "name": org_data.get('name', 'Unknown Organization'),
            "type": org_data.get('type', 'enterprise'),
            "industry": org_data.get('industry', 'technology'),
            "size": org_data.get('size', 'medium'),
            "jurisdiction": org_data.get('jurisdiction', 'US'),
            "data_sensitivity": org_data.get('data_sensitivity', 'medium'),
            "quantum_awareness_level": org_data.get('quantum_awareness', 'basic'),
            "crypto_expertise_level": org_data.get('crypto_expertise', 'intermediate')
        }
    
    def _generate_algorithm_rationale(self, recommendations: Dict[CryptographicPrimitive, List[PostQuantumAlgorithm]]) -> Dict[str, str]:
        """Generate rationale for algorithm selections"""
        rationale = {}
        
        for primitive, algorithms in recommendations.items():
            if not algorithms:
                continue
            
            primary_alg = algorithms[0]
            profile = self.pq_algorithm_profiles[primary_alg]
            
            reasons = []
            
            if profile.standardization_status == "NIST_WINNER_2022":
                reasons.append("NIST standardized algorithm")
            
            if profile.implementation_maturity > 0.9:
                reasons.append("mature implementation")
            
            if profile.quantum_security_level >= 192:
                reasons.append("high quantum security level")
            
            if len(profile.protocol_compatibility) >= 3:
                reasons.append("broad protocol compatibility")
            
            rationale[primitive.value] = f"Selected {primary_alg.value} due to: " + ", ".join(reasons)
        
        return rationale

# Initialize the migration assessor
post_quantum_migration_assessor = PostQuantumMigrationAssessor()

# Example usage function
def perform_organization_assessment(org_data: Dict[str, Any]) -> MigrationAssessmentResult:
    """Perform comprehensive post-quantum migration assessment for an organization"""
    return post_quantum_migration_assessor.perform_comprehensive_assessment(
        org_data, f"org_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
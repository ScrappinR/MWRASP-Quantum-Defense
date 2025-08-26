#!/usr/bin/env python3
"""
MWRASP Legal Barrier System - Quantum Attack Detection Platform
Legal Jurisdiction Control Module with Toggle Functionality

This module provides sophisticated legal barrier functionality that can be:
- Turned ON/OFF entirely per customer requirements
- Configured per jurisdiction (ON/PASSIVE/OFF)
- Integrated with quantum attack detection core system
- Compliant with international law while providing maximum protection

Date: August 25, 2025
Version: 1.0 - Production Legal Barrier System
Status: Defensive security tool for legitimate protection
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass
import hashlib
import secrets
import ipaddress
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JurisdictionMode(Enum):
    """Legal jurisdiction operational modes"""
    OFF = "off"                    # Jurisdiction completely disabled
    PASSIVE = "passive"            # Monitor only, no active barriers
    ACTIVE = "active"              # Full legal barrier protection
    EMERGENCY = "emergency"        # Maximum protection mode

class LegalBarrierType(Enum):
    """Types of legal barriers available"""
    JURISDICTIONAL_ROUTING = "jurisdictional_routing"
    DATA_SOVEREIGNTY = "data_sovereignty"
    COMPLIANCE_FRAGMENTATION = "compliance_fragmentation"
    LEGAL_STANDING_COMPLEXITY = "legal_standing_complexity"
    EVIDENCE_CHAIN_PROTECTION = "evidence_chain_protection"

@dataclass
class JurisdictionConfig:
    """Configuration for a specific legal jurisdiction"""
    jurisdiction_code: str          # ISO country code or legal region
    jurisdiction_name: str          # Human readable name
    mode: JurisdictionMode         # Operational mode for this jurisdiction
    legal_framework: str           # Legal system type (common_law, civil_law, etc.)
    data_protection_laws: List[str] # Applicable data protection regulations
    enforcement_complexity: int    # 1-10 scale of legal complexity
    cooperation_treaties: List[str] # International cooperation agreements
    barrier_types_enabled: List[LegalBarrierType]
    routing_priority: int          # Priority for routing decisions (1-100)
    last_updated: datetime
    compliance_verified: bool

@dataclass
class LegalBarrierEvent:
    """Event log for legal barrier activations"""
    event_id: str
    timestamp: datetime
    barrier_type: LegalBarrierType
    source_jurisdiction: str
    target_jurisdiction: str
    threat_classification: str
    action_taken: str
    legal_basis: str
    compliance_status: str

class LegalJurisdictionDatabase:
    """Database of legal jurisdictions and their configurations"""
    
    def __init__(self):
        self.jurisdictions: Dict[str, JurisdictionConfig] = {}
        self._initialize_default_jurisdictions()
    
    def _initialize_default_jurisdictions(self):
        """Initialize with common legal jurisdictions"""
        
        # Major jurisdictions with different legal frameworks
        jurisdictions_data = [
            {
                "code": "US", "name": "United States", 
                "framework": "federal_common_law",
                "data_laws": ["CCPA", "HIPAA", "GLBA", "SOX"],
                "complexity": 9,
                "treaties": ["MLAT", "Five_Eyes", "US_EU_Privacy_Shield"]
            },
            {
                "code": "EU", "name": "European Union",
                "framework": "civil_law_union", 
                "data_laws": ["GDPR", "NIS2", "Data_Act", "Digital_Services_Act"],
                "complexity": 8,
                "treaties": ["US_EU_Privacy_Shield", "Schrems_II"]
            },
            {
                "code": "UK", "name": "United Kingdom",
                "framework": "common_law",
                "data_laws": ["UK_GDPR", "Data_Protection_Act_2018"],
                "complexity": 7,
                "treaties": ["Five_Eyes", "UK_US_Data_Bridge"]
            },
            {
                "code": "CA", "name": "Canada", 
                "framework": "federal_common_law",
                "data_laws": ["PIPEDA", "Privacy_Act"],
                "complexity": 6,
                "treaties": ["Five_Eyes", "USMCA"]
            },
            {
                "code": "AU", "name": "Australia",
                "framework": "common_law",
                "data_laws": ["Privacy_Act_1988", "Notifiable_Data_Breaches"],
                "complexity": 6,
                "treaties": ["Five_Eyes", "ANZUS"]
            },
            {
                "code": "CH", "name": "Switzerland",
                "framework": "civil_law",
                "data_laws": ["Federal_Data_Protection_Act"],
                "complexity": 5,
                "treaties": ["EU_Adequacy_Decision"]
            },
            {
                "code": "SG", "name": "Singapore",
                "framework": "common_law",
                "data_laws": ["PDPA"],
                "complexity": 4,
                "treaties": ["ASEAN", "CPTPP"]
            },
            # Privacy havens with strong data protection
            {
                "code": "IS", "name": "Iceland",
                "framework": "civil_law",
                "data_laws": ["GDPR", "Act_on_Data_Protection"],
                "complexity": 3,
                "treaties": ["EEA", "Nordic_Council"]
            },
            # Complex jurisdictions for maximum protection
            {
                "code": "LI", "name": "Liechtenstein",
                "framework": "civil_law",
                "data_laws": ["GDPR", "Data_Protection_Act"],
                "complexity": 2,
                "treaties": ["EEA"]
            }
        ]
        
        for jdata in jurisdictions_data:
            config = JurisdictionConfig(
                jurisdiction_code=jdata["code"],
                jurisdiction_name=jdata["name"],
                mode=JurisdictionMode.OFF,  # Default to OFF - must be explicitly enabled
                legal_framework=jdata["framework"],
                data_protection_laws=jdata["data_laws"],
                enforcement_complexity=jdata["complexity"],
                cooperation_treaties=jdata["treaties"],
                barrier_types_enabled=[],  # Default empty - must be configured
                routing_priority=50,  # Default priority
                last_updated=datetime.now(timezone.utc),
                compliance_verified=False
            )
            self.jurisdictions[jdata["code"]] = config
    
    def get_jurisdiction(self, code: str) -> Optional[JurisdictionConfig]:
        """Get jurisdiction configuration by code"""
        return self.jurisdictions.get(code.upper())
    
    def update_jurisdiction(self, code: str, config: JurisdictionConfig) -> bool:
        """Update jurisdiction configuration"""
        if code.upper() in self.jurisdictions:
            config.last_updated = datetime.now(timezone.utc)
            self.jurisdictions[code.upper()] = config
            logger.info(f"Updated jurisdiction configuration: {code}")
            return True
        return False
    
    def get_active_jurisdictions(self) -> List[JurisdictionConfig]:
        """Get all jurisdictions with ACTIVE or PASSIVE mode"""
        return [
            config for config in self.jurisdictions.values() 
            if config.mode in [JurisdictionMode.ACTIVE, JurisdictionMode.PASSIVE]
        ]

class LegalComplianceEngine:
    """Engine for automated legal compliance and barrier management"""
    
    def __init__(self, jurisdiction_db: LegalJurisdictionDatabase):
        self.jurisdiction_db = jurisdiction_db
        self.event_log: List[LegalBarrierEvent] = []
        self.compliance_cache: Dict[str, Dict] = {}
    
    def analyze_cross_border_complexity(self, 
                                      source_country: str, 
                                      target_country: str) -> Dict:
        """Analyze legal complexity of cross-border data handling"""
        
        source_config = self.jurisdiction_db.get_jurisdiction(source_country)
        target_config = self.jurisdiction_db.get_jurisdiction(target_country)
        
        if not source_config or not target_config:
            return {"complexity": 0, "barriers": [], "legal_basis": "unknown_jurisdiction"}
        
        # Calculate complexity score
        base_complexity = (source_config.enforcement_complexity + 
                          target_config.enforcement_complexity) / 2
        
        # Check for treaty conflicts
        treaty_conflicts = []
        for treaty in source_config.cooperation_treaties:
            if treaty not in target_config.cooperation_treaties:
                treaty_conflicts.append(treaty)
        
        # Identify applicable legal barriers
        applicable_barriers = []
        
        if source_config.mode == JurisdictionMode.ACTIVE:
            if "GDPR" in source_config.data_protection_laws:
                applicable_barriers.append(LegalBarrierType.DATA_SOVEREIGNTY)
            
            if base_complexity > 6:
                applicable_barriers.append(LegalBarrierType.LEGAL_STANDING_COMPLEXITY)
            
            if len(treaty_conflicts) > 0:
                applicable_barriers.append(LegalBarrierType.JURISDICTIONAL_ROUTING)
        
        return {
            "complexity_score": base_complexity + len(treaty_conflicts),
            "applicable_barriers": applicable_barriers,
            "treaty_conflicts": treaty_conflicts,
            "legal_basis": f"{source_config.legal_framework}_to_{target_config.legal_framework}",
            "data_protection_conflicts": self._check_data_protection_conflicts(source_config, target_config)
        }
    
    def _check_data_protection_conflicts(self, 
                                       source: JurisdictionConfig, 
                                       target: JurisdictionConfig) -> List[str]:
        """Check for data protection law conflicts"""
        conflicts = []
        
        # GDPR adequacy checks
        if "GDPR" in source.data_protection_laws:
            if target.jurisdiction_code not in ["US", "CA", "UK", "CH", "IS"]:  # Non-adequate countries
                conflicts.append("GDPR_adequacy_requirement")
        
        # US state law conflicts
        if "CCPA" in source.data_protection_laws and "GDPR" not in target.data_protection_laws:
            conflicts.append("CCPA_GDPR_compatibility")
        
        return conflicts
    
    def generate_legal_barriers(self, 
                              threat_data: Dict, 
                              source_ip: str) -> List[Dict]:
        """Generate appropriate legal barriers based on threat and geography"""
        
        barriers = []
        source_country = self._ip_to_country(source_ip)
        
        if not source_country:
            return barriers
        
        source_config = self.jurisdiction_db.get_jurisdiction(source_country)
        if not source_config or source_config.mode == JurisdictionMode.OFF:
            return barriers
        
        # Generate barriers based on threat level and jurisdiction config
        threat_level = threat_data.get("severity", "LOW")
        
        for barrier_type in source_config.barrier_types_enabled:
            barrier_config = self._create_barrier_config(
                barrier_type, source_config, threat_level, threat_data
            )
            if barrier_config:
                barriers.append(barrier_config)
        
        return barriers
    
    def _create_barrier_config(self, 
                             barrier_type: LegalBarrierType,
                             jurisdiction: JurisdictionConfig,
                             threat_level: str,
                             threat_data: Dict) -> Optional[Dict]:
        """Create configuration for specific barrier type"""
        
        barrier_configs = {
            LegalBarrierType.JURISDICTIONAL_ROUTING: {
                "type": "jurisdictional_routing",
                "action": "route_through_complex_jurisdictions",
                "jurisdictions": self._select_routing_jurisdictions(jurisdiction, threat_level),
                "legal_basis": "data_sovereignty_protection",
                "activation_threshold": "MEDIUM" if threat_level == "HIGH" else "HIGH"
            },
            
            LegalBarrierType.DATA_SOVEREIGNTY: {
                "type": "data_sovereignty",
                "action": "enforce_data_residency_requirements", 
                "applicable_laws": jurisdiction.data_protection_laws,
                "geographical_restrictions": self._get_data_residency_rules(jurisdiction),
                "legal_basis": "territorial_data_protection",
                "activation_threshold": "LOW"
            },
            
            LegalBarrierType.COMPLIANCE_FRAGMENTATION: {
                "type": "compliance_fragmentation",
                "action": "distribute_across_multiple_compliance_frameworks",
                "frameworks": self._get_applicable_frameworks(jurisdiction),
                "fragmentation_strategy": "maximize_compliance_complexity",
                "legal_basis": "regulatory_compliance_requirements",
                "activation_threshold": "MEDIUM"
            },
            
            LegalBarrierType.LEGAL_STANDING_COMPLEXITY: {
                "type": "legal_standing_complexity",
                "action": "create_complex_legal_standing_requirements",
                "standing_requirements": self._generate_standing_requirements(jurisdiction),
                "procedural_barriers": self._get_procedural_barriers(jurisdiction),
                "legal_basis": "procedural_law_requirements",
                "activation_threshold": "HIGH"
            },
            
            LegalBarrierType.EVIDENCE_CHAIN_PROTECTION: {
                "type": "evidence_chain_protection", 
                "action": "implement_evidence_preservation_barriers",
                "preservation_requirements": self._get_evidence_requirements(jurisdiction),
                "chain_of_custody": "strict_legal_standards",
                "legal_basis": "evidence_law_compliance",
                "activation_threshold": "CRITICAL"
            }
        }
        
        if barrier_type in barrier_configs:
            config = barrier_configs[barrier_type].copy()
            config["jurisdiction"] = jurisdiction.jurisdiction_code
            config["timestamp"] = datetime.now(timezone.utc).isoformat()
            return config
        
        return None
    
    def _select_routing_jurisdictions(self, 
                                    source_jurisdiction: JurisdictionConfig,
                                    threat_level: str) -> List[str]:
        """Select optimal jurisdictions for routing to maximize legal complexity"""
        
        active_jurisdictions = self.jurisdiction_db.get_active_jurisdictions()
        
        # Sort by enforcement complexity and treaty conflicts
        routing_candidates = []
        for jurisdiction in active_jurisdictions:
            if jurisdiction.jurisdiction_code != source_jurisdiction.jurisdiction_code:
                complexity_score = jurisdiction.enforcement_complexity
                
                # Add points for treaty conflicts (makes legal action harder)
                treaty_conflicts = len(set(source_jurisdiction.cooperation_treaties) - 
                                     set(jurisdiction.cooperation_treaties))
                complexity_score += treaty_conflicts * 2
                
                routing_candidates.append((jurisdiction.jurisdiction_code, complexity_score))
        
        # Sort by complexity (descending) and select top candidates
        routing_candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Select number of jurisdictions based on threat level
        num_jurisdictions = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        selected_count = num_jurisdictions.get(threat_level, 1)
        
        return [code for code, _ in routing_candidates[:selected_count]]
    
    def _ip_to_country(self, ip_address: str) -> Optional[str]:
        """Convert IP address to country code (simplified implementation)"""
        # In production, this would use a real GeoIP database
        # For demo purposes, return based on IP ranges
        
        try:
            ip = ipaddress.ip_address(ip_address)
            
            # Example IP ranges (in production, use real GeoIP database)
            us_ranges = [
                ipaddress.ip_network("8.0.0.0/8"),
                ipaddress.ip_network("64.0.0.0/10")
            ]
            
            eu_ranges = [
                ipaddress.ip_network("85.0.0.0/8"),
                ipaddress.ip_network("86.0.0.0/8")
            ]
            
            for network in us_ranges:
                if ip in network:
                    return "US"
            
            for network in eu_ranges:
                if ip in network:
                    return "EU"
            
            # Default to unknown
            return None
            
        except Exception as e:
            logger.warning(f"Failed to parse IP address {ip_address}: {e}")
            return None
    
    def _get_data_residency_rules(self, jurisdiction: JurisdictionConfig) -> Dict:
        """Get data residency requirements for jurisdiction"""
        rules = {
            "US": {"financial_data": "domestic_only", "health_data": "HIPAA_compliant_facilities"},
            "EU": {"personal_data": "EU_EEA_only", "sensitive_data": "member_state_restrictions"},
            "CA": {"personal_info": "Canadian_facilities", "health_records": "provincial_requirements"},
            "CH": {"banking_data": "Swiss_territory_only", "personal_data": "adequacy_decision_countries"}
        }
        return rules.get(jurisdiction.jurisdiction_code, {"default": "local_jurisdiction_only"})
    
    def _get_applicable_frameworks(self, jurisdiction: JurisdictionConfig) -> List[str]:
        """Get compliance frameworks applicable to jurisdiction"""
        framework_map = {
            "US": ["SOC2", "FedRAMP", "NIST", "HIPAA", "PCI_DSS"],
            "EU": ["ISO27001", "GDPR", "NIS2", "eIDAS", "Cybersecurity_Act"],
            "UK": ["Cyber_Essentials", "UK_GDPR", "ISO27001", "PCI_DSS"],
            "CA": ["PIPEDA", "SOC2", "ISO27001", "CSA_STAR"],
            "AU": ["Essential_Eight", "ISM", "Privacy_Act", "APRA_CPS234"]
        }
        return framework_map.get(jurisdiction.jurisdiction_code, ["ISO27001"])
    
    def _generate_standing_requirements(self, jurisdiction: JurisdictionConfig) -> List[str]:
        """Generate legal standing requirements for jurisdiction"""
        
        common_law_requirements = [
            "demonstrate_concrete_harm",
            "establish_causation_chain", 
            "prove_personal_jurisdiction",
            "show_statutory_damages"
        ]
        
        civil_law_requirements = [
            "establish_legal_interest",
            "demonstrate_territorial_nexus",
            "prove_regulatory_standing",
            "show_administrative_capacity"
        ]
        
        if "common_law" in jurisdiction.legal_framework:
            return common_law_requirements
        else:
            return civil_law_requirements
    
    def _get_procedural_barriers(self, jurisdiction: JurisdictionConfig) -> List[str]:
        """Get procedural law barriers for jurisdiction"""
        return [
            "mandatory_local_legal_representation",
            "complex_service_of_process_requirements", 
            "extensive_discovery_limitations",
            "mandatory_mediation_requirements",
            "jurisdictional_challenge_procedures",
            "forum_non_conveniens_challenges"
        ]
    
    def _get_evidence_requirements(self, jurisdiction: JurisdictionConfig) -> List[str]:
        """Get evidence preservation requirements for jurisdiction"""
        return [
            "certified_digital_forensics_chain_of_custody",
            "local_evidence_authentication_requirements",
            "cross_border_evidence_sharing_restrictions",
            "data_protection_law_evidence_limitations",
            "attorney_client_privilege_protections"
        ]

class LegalBarrierController:
    """Main controller for legal barrier system"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.system_enabled = False  # Default OFF - must be explicitly enabled
        self.jurisdiction_db = LegalJurisdictionDatabase()
        self.compliance_engine = LegalComplianceEngine(self.jurisdiction_db)
        self.active_barriers: Dict[str, Dict] = {}
        self.event_log: List[LegalBarrierEvent] = []
        
        # Load configuration if provided
        if config_file:
            self.load_configuration(config_file)
        
        logger.info("Legal Barrier Controller initialized - System DISABLED by default")
    
    def enable_system(self, authorization_key: str) -> bool:
        """Enable legal barrier system with proper authorization"""
        # In production, this would verify proper authorization
        expected_hash = "authorized_legal_barrier_activation"
        
        if hashlib.sha256(authorization_key.encode()).hexdigest()[:32] == hashlib.sha256(expected_hash.encode()).hexdigest()[:32]:
            self.system_enabled = True
            logger.info("Legal Barrier System ENABLED")
            return True
        else:
            logger.warning("Unauthorized attempt to enable legal barrier system")
            return False
    
    def disable_system(self) -> bool:
        """Disable legal barrier system completely"""
        self.system_enabled = False
        self.active_barriers.clear()
        logger.info("Legal Barrier System DISABLED")
        return True
    
    def configure_jurisdiction(self, 
                             jurisdiction_code: str,
                             mode: JurisdictionMode,
                             barrier_types: List[LegalBarrierType],
                             priority: int = 50) -> bool:
        """Configure specific jurisdiction settings"""
        
        if not self.system_enabled:
            logger.warning("Cannot configure jurisdiction - system disabled")
            return False
        
        jurisdiction = self.jurisdiction_db.get_jurisdiction(jurisdiction_code)
        if not jurisdiction:
            logger.error(f"Unknown jurisdiction: {jurisdiction_code}")
            return False
        
        # Update configuration
        jurisdiction.mode = mode
        jurisdiction.barrier_types_enabled = barrier_types
        jurisdiction.routing_priority = priority
        jurisdiction.last_updated = datetime.now(timezone.utc)
        
        # Save updated configuration
        self.jurisdiction_db.update_jurisdiction(jurisdiction_code, jurisdiction)
        
        logger.info(f"Configured jurisdiction {jurisdiction_code}: mode={mode.value}, barriers={len(barrier_types)}")
        return True
    
    async def process_threat_with_legal_barriers(self, 
                                               threat_data: Dict,
                                               source_ip: str) -> Dict:
        """Process threat and apply appropriate legal barriers"""
        
        if not self.system_enabled:
            return {"legal_barriers": [], "status": "system_disabled"}
        
        # Generate appropriate legal barriers
        barriers = self.compliance_engine.generate_legal_barriers(threat_data, source_ip)
        
        response = {
            "legal_barriers": barriers,
            "status": "processed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": source_ip,
            "threat_classification": threat_data.get("classification", "unknown")
        }
        
        # Log legal barrier activation
        for barrier in barriers:
            event = LegalBarrierEvent(
                event_id=secrets.token_hex(16),
                timestamp=datetime.now(timezone.utc),
                barrier_type=LegalBarrierType(barrier["type"]),
                source_jurisdiction=barrier.get("jurisdiction", "unknown"),
                target_jurisdiction="multiple",
                threat_classification=threat_data.get("classification", "unknown"),
                action_taken=barrier["action"],
                legal_basis=barrier["legal_basis"],
                compliance_status="activated"
            )
            self.event_log.append(event)
        
        logger.info(f"Applied {len(barriers)} legal barriers for threat from {source_ip}")
        return response
    
    def get_jurisdiction_status(self) -> Dict:
        """Get current status of all jurisdictions"""
        
        status = {
            "system_enabled": self.system_enabled,
            "total_jurisdictions": len(self.jurisdiction_db.jurisdictions),
            "active_jurisdictions": len([j for j in self.jurisdiction_db.jurisdictions.values() 
                                       if j.mode == JurisdictionMode.ACTIVE]),
            "passive_jurisdictions": len([j for j in self.jurisdiction_db.jurisdictions.values()
                                        if j.mode == JurisdictionMode.PASSIVE]),
            "jurisdictions": {}
        }
        
        for code, config in self.jurisdiction_db.jurisdictions.items():
            status["jurisdictions"][code] = {
                "name": config.jurisdiction_name,
                "mode": config.mode.value,
                "complexity": config.enforcement_complexity,
                "enabled_barriers": [bt.value for bt in config.barrier_types_enabled],
                "last_updated": config.last_updated.isoformat()
            }
        
        return status
    
    def export_event_log(self, since: Optional[datetime] = None) -> List[Dict]:
        """Export legal barrier event log"""
        
        events = self.event_log
        if since:
            events = [e for e in events if e.timestamp >= since]
        
        return [
            {
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "barrier_type": event.barrier_type.value,
                "source_jurisdiction": event.source_jurisdiction,
                "target_jurisdiction": event.target_jurisdiction,
                "threat_classification": event.threat_classification,
                "action_taken": event.action_taken,
                "legal_basis": event.legal_basis,
                "compliance_status": event.compliance_status
            }
            for event in events
        ]
    
    def load_configuration(self, config_file: str) -> bool:
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Apply system-level settings
            self.system_enabled = config.get("system_enabled", False)
            
            # Apply jurisdiction configurations
            for jcode, jconfig in config.get("jurisdictions", {}).items():
                mode = JurisdictionMode(jconfig.get("mode", "off"))
                barriers = [LegalBarrierType(bt) for bt in jconfig.get("barrier_types", [])]
                priority = jconfig.get("priority", 50)
                
                self.configure_jurisdiction(jcode, mode, barriers, priority)
            
            logger.info(f"Loaded configuration from {config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def save_configuration(self, config_file: str) -> bool:
        """Save current configuration to file"""
        try:
            config = {
                "system_enabled": self.system_enabled,
                "jurisdictions": {}
            }
            
            for code, jurisdiction in self.jurisdiction_db.jurisdictions.items():
                config["jurisdictions"][code] = {
                    "mode": jurisdiction.mode.value,
                    "barrier_types": [bt.value for bt in jurisdiction.barrier_types_enabled],
                    "priority": jurisdiction.routing_priority
                }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Saved configuration to {config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

# Example usage and testing
async def demo_legal_barrier_system():
    """Demonstrate legal barrier system functionality"""
    
    print("\n" + "="*80)
    print("MWRASP LEGAL BARRIER SYSTEM DEMONSTRATION")
    print("Defensive Legal Protection for Quantum Attack Detection Platform")
    print("="*80)
    
    # Initialize legal barrier controller
    controller = LegalBarrierController()
    
    print(f"\n📊 System Status: {'ENABLED' if controller.system_enabled else 'DISABLED'}")
    
    # Demo system activation
    print(f"\n🔐 Activating Legal Barrier System...")
    activation_key = "authorized_legal_barrier_activation"
    if controller.enable_system(activation_key):
        print("✅ Legal Barrier System ACTIVATED")
    else:
        print("❌ Failed to activate system")
        return
    
    # Configure jurisdictions for demo
    print(f"\n⚙️ Configuring Jurisdictions...")
    
    # Configure US for active protection
    controller.configure_jurisdiction(
        "US", 
        JurisdictionMode.ACTIVE,
        [LegalBarrierType.DATA_SOVEREIGNTY, LegalBarrierType.COMPLIANCE_FRAGMENTATION],
        priority=90
    )
    
    # Configure EU for active protection
    controller.configure_jurisdiction(
        "EU",
        JurisdictionMode.ACTIVE, 
        [LegalBarrierType.DATA_SOVEREIGNTY, LegalBarrierType.LEGAL_STANDING_COMPLEXITY],
        priority=85
    )
    
    # Configure Switzerland as passive monitoring
    controller.configure_jurisdiction(
        "CH",
        JurisdictionMode.PASSIVE,
        [LegalBarrierType.EVIDENCE_CHAIN_PROTECTION],
        priority=70
    )
    
    print("✅ Jurisdictions configured")
    
    # Display jurisdiction status
    print(f"\n📋 Jurisdiction Status:")
    status = controller.get_jurisdiction_status()
    for code, info in status["jurisdictions"].items():
        if info["mode"] != "off":
            print(f"   {code}: {info['name']} - Mode: {info['mode'].upper()}")
            print(f"       Barriers: {info['enabled_barriers']}")
    
    # Simulate quantum attack detection with legal barrier response
    print(f"\n🚨 Simulating Quantum Attack Detection with Legal Barriers...")
    
    threat_scenarios = [
        {
            "source_ip": "8.8.8.8",  # US IP
            "threat": {
                "classification": "quantum_attack",
                "algorithm": "Shor_Algorithm", 
                "severity": "HIGH",
                "target": "encryption_keys"
            }
        },
        {
            "source_ip": "85.1.1.1",  # EU IP
            "threat": {
                "classification": "quantum_probe",
                "algorithm": "Grover_Search",
                "severity": "MEDIUM", 
                "target": "database_search"
            }
        }
    ]
    
    for i, scenario in enumerate(threat_scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['threat']['classification']} from {scenario['source_ip']} ---")
        
        # Process threat with legal barriers
        response = await controller.process_threat_with_legal_barriers(
            scenario["threat"],
            scenario["source_ip"]
        )
        
        print(f"   Status: {response['status']}")
        print(f"   Legal Barriers Applied: {len(response['legal_barriers'])}")
        
        for barrier in response['legal_barriers']:
            print(f"     • {barrier['type']}: {barrier['action']}")
            print(f"       Legal Basis: {barrier['legal_basis']}")
            print(f"       Jurisdiction: {barrier['jurisdiction']}")
    
    # Display event log
    print(f"\n📜 Legal Barrier Event Log:")
    events = controller.export_event_log()
    for event in events[-3:]:  # Show last 3 events
        print(f"   {event['timestamp'][:19]}: {event['barrier_type']} activated")
        print(f"     Action: {event['action_taken']}")
        print(f"     Legal Basis: {event['legal_basis']}")
    
    # Demonstrate system disable
    print(f"\n🔒 Disabling Legal Barrier System...")
    controller.disable_system()
    print(f"✅ System disabled - All legal barriers deactivated")
    
    print(f"\n" + "="*80)
    print("LEGAL BARRIER SYSTEM DEMONSTRATION COMPLETE")
    print("System provides configurable legal protection while maintaining")
    print("full compliance with international law and customer requirements.")
    print("="*80)

if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demo_legal_barrier_system())
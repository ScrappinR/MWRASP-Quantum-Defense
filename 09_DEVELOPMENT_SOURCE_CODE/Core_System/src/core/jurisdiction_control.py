#!/usr/bin/env python3
"""
Jurisdiction Control System for MWRASP Legal Conflict Engine
Provides selective activation/deactivation of impossibility barriers per jurisdiction
"""

import json
import time
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio


class JurisdictionStatus(Enum):
    """Status options for jurisdiction barriers"""
    ACTIVE = "active"              # Full legal barriers enabled
    PASSIVE = "passive"            # Monitoring only, no active barriers
    DISABLED = "disabled"          # Completely excluded from routing
    CONDITIONAL = "conditional"    # Activated based on conditions
    EMERGENCY_ONLY = "emergency"   # Only activated during emergency situations


class ControlLevel(Enum):
    """Control granularity levels"""
    GLOBAL = "global"              # System-wide control
    FRAGMENT = "fragment"          # Per-fragment control
    DATA_TYPE = "data_type"        # Per data classification
    USER = "user"                  # Per user/clearance level
    TEMPORAL = "temporal"          # Time-based control


@dataclass
class JurisdictionProfile:
    """Detailed jurisdiction control profile"""
    code: str
    name: str
    status: JurisdictionStatus
    priority: int  # 1-10, higher = preferred for routing
    max_fragments_per_hour: int
    allowed_data_types: List[str]
    restricted_users: List[str]
    temporal_constraints: Dict[str, Any]
    emergency_activation: bool
    compliance_notes: str
    last_updated: float
    updated_by: str


@dataclass
class RoutingPolicy:
    """Routing policy configuration"""
    policy_name: str
    active_jurisdictions: Set[str]
    passive_jurisdictions: Set[str]
    disabled_jurisdictions: Set[str]
    min_active_jurisdictions: int
    max_jurisdictions_per_fragment: int
    prefer_high_hostility: bool
    emergency_override: bool
    created_at: float
    created_by: str


class JurisdictionController:
    """
    Advanced jurisdiction control system for selective legal barrier activation
    Allows fine-grained control over which jurisdictions participate in routing
    Includes master toggle to completely disable/enable the entire legal routing system
    """
    
    def __init__(self):
        self.jurisdiction_profiles: Dict[str, JurisdictionProfile] = {}
        self.routing_policies: Dict[str, RoutingPolicy] = {}
        self.active_policy: Optional[str] = None
        self.emergency_mode: bool = False
        self.control_history: List[Dict[str, Any]] = []
        
        # Master system control - when False, all legal routing is disabled
        self.legal_routing_enabled: bool = True
        
        # Initialize default jurisdiction profiles
        self._initialize_default_profiles()
        
        # Create default routing policies
        self._create_default_policies()
        
        print("[CONTROL] Jurisdiction Control System initialized")
        print(f"[CONTROL] Legal routing system: {'ENABLED' if self.legal_routing_enabled else 'DISABLED'}")
    
    def _initialize_default_profiles(self):
        """Initialize default jurisdiction profiles with reasonable settings"""
        
        default_jurisdictions = [
            {
                'code': 'US', 'name': 'United States', 'priority': 8,
                'data_types': ['GOVERNMENT', 'MILITARY', 'INTELLIGENCE'],
                'compliance_notes': 'CLOUD Act jurisdiction - high enforcement capability'
            },
            {
                'code': 'CN', 'name': 'China', 'priority': 9,
                'data_types': ['TRADE_SECRETS', 'TECHNOLOGY', 'DEFENSE'],
                'compliance_notes': 'Data Security Law - blocks foreign access'
            },
            {
                'code': 'RU', 'name': 'Russia', 'priority': 9,
                'data_types': ['FINANCIAL', 'ENERGY', 'DEFENSE'],
                'compliance_notes': 'Data localization laws - hostile to Western requests'
            },
            {
                'code': 'EU', 'name': 'European Union', 'priority': 6,
                'data_types': ['PRIVACY', 'COMMERCIAL', 'FINANCIAL'],
                'compliance_notes': 'GDPR protections - moderate hostility'
            },
            {
                'code': 'CH', 'name': 'Switzerland', 'priority': 7,
                'data_types': ['FINANCIAL', 'PRIVACY', 'DIPLOMATIC'],
                'compliance_notes': 'Banking secrecy laws - neutral jurisdiction'
            },
            {
                'code': 'IR', 'name': 'Iran', 'priority': 10,
                'data_types': ['ENERGY', 'DEFENSE', 'SANCTIONS_EVASION'],
                'compliance_notes': 'Under sanctions - maximum hostility to US/EU'
            }
        ]
        
        for jurisdiction_data in default_jurisdictions:
            profile = JurisdictionProfile(
                code=jurisdiction_data['code'],
                name=jurisdiction_data['name'],
                status=JurisdictionStatus.ACTIVE,  # Default to active
                priority=jurisdiction_data['priority'],
                max_fragments_per_hour=1000,
                allowed_data_types=jurisdiction_data['data_types'],
                restricted_users=[],
                temporal_constraints={},
                emergency_activation=True,
                compliance_notes=jurisdiction_data['compliance_notes'],
                last_updated=time.time(),
                updated_by='system_init'
            )
            
            self.jurisdiction_profiles[jurisdiction_data['code']] = profile
    
    def _create_default_policies(self):
        """Create default routing policies for different scenarios"""
        
        policies = [
            {
                'name': 'maximum_hostility',
                'description': 'Use all hostile jurisdictions for maximum impossibility',
                'active': {'US', 'CN', 'RU', 'IR'},
                'passive': {'EU', 'CH'},
                'disabled': set()
            },
            {
                'name': 'balanced_security',
                'description': 'Balanced approach with moderate impossibility',
                'active': {'US', 'CN', 'EU'},
                'passive': {'RU', 'CH'},
                'disabled': {'IR'}
            },
            {
                'name': 'western_friendly',
                'description': 'Avoid sanctions targets, use Western allies',
                'active': {'US', 'EU', 'CH'},
                'passive': {'CN'},
                'disabled': {'RU', 'IR'}
            },
            {
                'name': 'financial_protection',
                'description': 'Optimized for financial data protection',
                'active': {'CH', 'EU', 'CN'},
                'passive': {'US'},
                'disabled': {'RU', 'IR'}
            },
            {
                'name': 'emergency_maximum',
                'description': 'Emergency mode - activate all jurisdictions',
                'active': {'US', 'CN', 'RU', 'EU', 'CH', 'IR'},
                'passive': set(),
                'disabled': set()
            }
        ]
        
        for policy_data in policies:
            policy = RoutingPolicy(
                policy_name=policy_data['name'],
                active_jurisdictions=policy_data['active'],
                passive_jurisdictions=policy_data['passive'],
                disabled_jurisdictions=policy_data['disabled'],
                min_active_jurisdictions=3,
                max_jurisdictions_per_fragment=5,
                prefer_high_hostility=True,
                emergency_override=policy_data['name'] == 'emergency_maximum',
                created_at=time.time(),
                created_by='system_init'
            )
            
            self.routing_policies[policy_data['name']] = policy
        
        # Set default active policy
        self.active_policy = 'maximum_hostility'
    
    def set_jurisdiction_status(self, jurisdiction_code: str, status: JurisdictionStatus, 
                              updated_by: str = 'admin', reason: str = '') -> bool:
        """Set the status of a specific jurisdiction"""
        
        if jurisdiction_code not in self.jurisdiction_profiles:
            print(f"[CONTROL] Unknown jurisdiction: {jurisdiction_code}")
            return False
        
        old_status = self.jurisdiction_profiles[jurisdiction_code].status
        self.jurisdiction_profiles[jurisdiction_code].status = status
        self.jurisdiction_profiles[jurisdiction_code].last_updated = time.time()
        self.jurisdiction_profiles[jurisdiction_code].updated_by = updated_by
        
        # Log the change
        self.control_history.append({
            'action': 'jurisdiction_status_change',
            'jurisdiction': jurisdiction_code,
            'old_status': old_status.value,
            'new_status': status.value,
            'updated_by': updated_by,
            'reason': reason,
            'timestamp': time.time()
        })
        
        print(f"[CONTROL] {jurisdiction_code} status: {old_status.value} → {status.value}")
        return True
    
    def set_multiple_jurisdiction_status(self, jurisdiction_updates: Dict[str, JurisdictionStatus],
                                       updated_by: str = 'admin', reason: str = '') -> Dict[str, bool]:
        """Set status for multiple jurisdictions at once"""
        
        results = {}
        for jurisdiction_code, status in jurisdiction_updates.items():
            results[jurisdiction_code] = self.set_jurisdiction_status(
                jurisdiction_code, status, updated_by, reason
            )
        
        return results
    
    def activate_policy(self, policy_name: str, updated_by: str = 'admin') -> bool:
        """Activate a specific routing policy"""
        
        if policy_name not in self.routing_policies:
            print(f"[CONTROL] Unknown policy: {policy_name}")
            return False
        
        old_policy = self.active_policy
        self.active_policy = policy_name
        policy = self.routing_policies[policy_name]
        
        # Apply policy to jurisdiction statuses
        for jurisdiction_code in policy.active_jurisdictions:
            if jurisdiction_code in self.jurisdiction_profiles:
                self.jurisdiction_profiles[jurisdiction_code].status = JurisdictionStatus.ACTIVE
        
        for jurisdiction_code in policy.passive_jurisdictions:
            if jurisdiction_code in self.jurisdiction_profiles:
                self.jurisdiction_profiles[jurisdiction_code].status = JurisdictionStatus.PASSIVE
        
        for jurisdiction_code in policy.disabled_jurisdictions:
            if jurisdiction_code in self.jurisdiction_profiles:
                self.jurisdiction_profiles[jurisdiction_code].status = JurisdictionStatus.DISABLED
        
        # Log policy activation
        self.control_history.append({
            'action': 'policy_activation',
            'old_policy': old_policy,
            'new_policy': policy_name,
            'updated_by': updated_by,
            'timestamp': time.time(),
            'affected_jurisdictions': {
                'active': list(policy.active_jurisdictions),
                'passive': list(policy.passive_jurisdictions),
                'disabled': list(policy.disabled_jurisdictions)
            }
        })
        
        print(f"[CONTROL] Policy activated: {old_policy} → {policy_name}")
        print(f"[CONTROL] Active jurisdictions: {policy.active_jurisdictions}")
        print(f"[CONTROL] Passive jurisdictions: {policy.passive_jurisdictions}")
        print(f"[CONTROL] Disabled jurisdictions: {policy.disabled_jurisdictions}")
        
        return True
    
    def set_legal_routing_enabled(self, enabled: bool, updated_by: str = 'admin', reason: str = '') -> bool:
        """Master toggle for the entire legal routing system"""
        
        old_status = self.legal_routing_enabled
        self.legal_routing_enabled = enabled
        
        # Log the master system change
        self.control_history.append({
            'action': 'master_system_toggle',
            'old_status': old_status,
            'new_status': enabled,
            'updated_by': updated_by,
            'reason': reason,
            'timestamp': time.time()
        })
        
        status_msg = 'ENABLED' if enabled else 'DISABLED'
        print(f"[CONTROL] Legal routing system {status_msg} by {updated_by}")
        if reason:
            print(f"[CONTROL] Reason: {reason}")
        
        return True
    
    def is_legal_routing_enabled(self) -> bool:
        """Check if legal routing system is enabled"""
        return self.legal_routing_enabled
    
    def get_active_jurisdictions(self, data_type: str = None, user_clearance: str = None) -> List[str]:
        """Get list of jurisdictions that should be used for routing"""
        
        # If legal routing is disabled, return empty list
        if not self.legal_routing_enabled:
            return []
        
        active_jurisdictions = []
        
        for jurisdiction_code, profile in self.jurisdiction_profiles.items():
            # Check basic status
            if profile.status == JurisdictionStatus.DISABLED:
                continue
            
            if profile.status == JurisdictionStatus.EMERGENCY_ONLY and not self.emergency_mode:
                continue
            
            # Check data type restrictions
            if data_type and profile.allowed_data_types:
                if data_type not in profile.allowed_data_types:
                    continue
            
            # Check user restrictions
            if user_clearance and profile.restricted_users:
                if user_clearance in profile.restricted_users:
                    continue
            
            # Include if active or conditional
            if profile.status in [JurisdictionStatus.ACTIVE, JurisdictionStatus.CONDITIONAL]:
                active_jurisdictions.append(jurisdiction_code)
        
        # Sort by priority (higher priority first)
        active_jurisdictions.sort(
            key=lambda x: self.jurisdiction_profiles[x].priority, 
            reverse=True
        )
        
        return active_jurisdictions
    
    def get_passive_jurisdictions(self) -> List[str]:
        """Get list of jurisdictions in passive monitoring mode"""
        
        return [
            jurisdiction_code for jurisdiction_code, profile 
            in self.jurisdiction_profiles.items()
            if profile.status == JurisdictionStatus.PASSIVE
        ]
    
    def create_custom_policy(self, policy_name: str, active_jurisdictions: Set[str],
                           passive_jurisdictions: Set[str] = None,
                           disabled_jurisdictions: Set[str] = None,
                           created_by: str = 'admin') -> bool:
        """Create a new custom routing policy"""
        
        if policy_name in self.routing_policies:
            print(f"[CONTROL] Policy already exists: {policy_name}")
            return False
        
        policy = RoutingPolicy(
            policy_name=policy_name,
            active_jurisdictions=active_jurisdictions,
            passive_jurisdictions=passive_jurisdictions or set(),
            disabled_jurisdictions=disabled_jurisdictions or set(),
            min_active_jurisdictions=max(3, len(active_jurisdictions)),
            max_jurisdictions_per_fragment=min(5, len(active_jurisdictions)),
            prefer_high_hostility=True,
            emergency_override=False,
            created_at=time.time(),
            created_by=created_by
        )
        
        self.routing_policies[policy_name] = policy
        
        self.control_history.append({
            'action': 'policy_creation',
            'policy_name': policy_name,
            'created_by': created_by,
            'timestamp': time.time(),
            'policy_details': asdict(policy)
        })
        
        print(f"[CONTROL] Created custom policy: {policy_name}")
        return True
    
    def toggle_emergency_mode(self, enabled: bool, activated_by: str = 'admin') -> bool:
        """Toggle emergency mode which activates maximum legal barriers"""
        
        old_emergency_mode = self.emergency_mode
        self.emergency_mode = enabled
        
        if enabled:
            # Activate emergency policy
            self.activate_policy('emergency_maximum', activated_by)
            print(f"[CONTROL] EMERGENCY MODE ACTIVATED - All jurisdictions engaged")
        else:
            # Return to previous policy or default
            fallback_policy = 'maximum_hostility'
            self.activate_policy(fallback_policy, activated_by)
            print(f"[CONTROL] Emergency mode deactivated - Returned to {fallback_policy}")
        
        # Log emergency mode change
        self.control_history.append({
            'action': 'emergency_mode_toggle',
            'old_state': old_emergency_mode,
            'new_state': enabled,
            'activated_by': activated_by,
            'timestamp': time.time()
        })
        
        return True
    
    def get_jurisdiction_effectiveness(self) -> Dict[str, Dict[str, Any]]:
        """Get effectiveness metrics for each jurisdiction"""
        
        effectiveness = {}
        
        for jurisdiction_code, profile in self.jurisdiction_profiles.items():
            # Calculate usage statistics (simplified for demo)
            fragments_this_hour = min(50, profile.max_fragments_per_hour)
            utilization_rate = fragments_this_hour / profile.max_fragments_per_hour
            
            effectiveness[jurisdiction_code] = {
                'status': profile.status.value,
                'priority': profile.priority,
                'utilization_rate': utilization_rate,
                'fragments_per_hour': fragments_this_hour,
                'max_capacity': profile.max_fragments_per_hour,
                'allowed_data_types': profile.allowed_data_types,
                'last_updated': profile.last_updated,
                'compliance_notes': profile.compliance_notes
            }
        
        return effectiveness
    
    def validate_routing_feasibility(self, data_type: str = None, 
                                   user_clearance: str = None,
                                   min_jurisdictions: int = 3) -> Dict[str, Any]:
        """Validate if current jurisdiction configuration allows feasible routing"""
        
        active_jurisdictions = self.get_active_jurisdictions(data_type, user_clearance)
        passive_jurisdictions = self.get_passive_jurisdictions()
        
        feasibility = {
            'feasible': len(active_jurisdictions) >= min_jurisdictions,
            'active_count': len(active_jurisdictions),
            'passive_count': len(passive_jurisdictions),
            'min_required': min_jurisdictions,
            'active_jurisdictions': active_jurisdictions,
            'passive_jurisdictions': passive_jurisdictions,
            'warnings': [],
            'recommendations': []
        }
        
        # Add warnings and recommendations
        if len(active_jurisdictions) < min_jurisdictions:
            feasibility['warnings'].append(
                f"Insufficient active jurisdictions: {len(active_jurisdictions)} < {min_jurisdictions}"
            )
            feasibility['recommendations'].append("Activate more jurisdictions or reduce minimum requirement")
        
        if len(active_jurisdictions) < 3:
            feasibility['warnings'].append("Less than 3 active jurisdictions reduces legal impossibility")
            feasibility['recommendations'].append("Consider activating high-hostility jurisdictions")
        
        # Check for jurisdiction conflicts
        high_priority = [j for j in active_jurisdictions 
                        if self.jurisdiction_profiles[j].priority >= 8]
        if not high_priority:
            feasibility['warnings'].append("No high-priority hostile jurisdictions active")
            feasibility['recommendations'].append("Activate at least one high-hostility jurisdiction (US, CN, RU, IR)")
        
        return feasibility
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export current jurisdiction configuration"""
        
        return {
            'jurisdiction_profiles': {
                code: asdict(profile) for code, profile 
                in self.jurisdiction_profiles.items()
            },
            'routing_policies': {
                name: asdict(policy) for name, policy 
                in self.routing_policies.items()
            },
            'active_policy': self.active_policy,
            'emergency_mode': self.emergency_mode,
            'control_history': self.control_history[-50:],  # Last 50 changes
            'export_timestamp': time.time()
        }
    
    def import_configuration(self, config_data: Dict[str, Any], 
                           imported_by: str = 'admin') -> bool:
        """Import jurisdiction configuration from exported data"""
        
        try:
            # Import jurisdiction profiles
            for code, profile_data in config_data['jurisdiction_profiles'].items():
                profile = JurisdictionProfile(**profile_data)
                self.jurisdiction_profiles[code] = profile
            
            # Import routing policies
            for name, policy_data in config_data['routing_policies'].items():
                # Convert sets back from lists if needed
                if isinstance(policy_data['active_jurisdictions'], list):
                    policy_data['active_jurisdictions'] = set(policy_data['active_jurisdictions'])
                if isinstance(policy_data['passive_jurisdictions'], list):
                    policy_data['passive_jurisdictions'] = set(policy_data['passive_jurisdictions'])
                if isinstance(policy_data['disabled_jurisdictions'], list):
                    policy_data['disabled_jurisdictions'] = set(policy_data['disabled_jurisdictions'])
                
                policy = RoutingPolicy(**policy_data)
                self.routing_policies[name] = policy
            
            # Set active policy
            self.active_policy = config_data['active_policy']
            self.emergency_mode = config_data['emergency_mode']
            
            # Log import
            self.control_history.append({
                'action': 'configuration_import',
                'imported_by': imported_by,
                'timestamp': time.time(),
                'source_timestamp': config_data['export_timestamp']
            })
            
            print(f"[CONTROL] Configuration imported successfully")
            return True
            
        except Exception as e:
            print(f"[CONTROL] Configuration import failed: {e}")
            return False
    
    def get_control_status(self) -> Dict[str, Any]:
        """Get comprehensive control system status"""
        
        active_jurisdictions = self.get_active_jurisdictions()
        passive_jurisdictions = self.get_passive_jurisdictions()
        
        status = {
            'legal_routing_enabled': self.legal_routing_enabled,
            'active_policy': self.active_policy,
            'emergency_mode': self.emergency_mode,
            'total_jurisdictions': len(self.jurisdiction_profiles),
            'active_jurisdictions': len(active_jurisdictions),
            'passive_jurisdictions': len(passive_jurisdictions),
            'disabled_jurisdictions': len(self.jurisdiction_profiles) - len(active_jurisdictions) - len(passive_jurisdictions),
            'available_policies': list(self.routing_policies.keys()),
            'feasibility_check': self.validate_routing_feasibility(),
            'last_control_change': max(self.control_history, key=lambda x: x['timestamp'])['timestamp'] if self.control_history else None,
            'control_changes_today': len([h for h in self.control_history if time.time() - h['timestamp'] < 86400]),
            'system_status': 'ENABLED' if self.legal_routing_enabled else 'DISABLED'
        }
        
        return status


# Factory function for easy integration
def create_jurisdiction_controller() -> JurisdictionController:
    """Create and initialize jurisdiction controller"""
    
    controller = JurisdictionController()
    
    print("[CONTROL] Jurisdiction Control System ready")
    print(f"[CONTROL] {len(controller.jurisdiction_profiles)} jurisdictions configured")
    print(f"[CONTROL] {len(controller.routing_policies)} routing policies available")
    print(f"[CONTROL] Active policy: {controller.active_policy}")
    
    return controller


if __name__ == "__main__":
    # Demonstration of jurisdiction control system
    def demo():
        print("=== JURISDICTION CONTROL SYSTEM DEMONSTRATION ===")
        
        controller = create_jurisdiction_controller()
        
        # Demo 1: Show current status
        print("\n1. Current System Status:")
        status = controller.get_control_status()
        print(f"   Legal routing enabled: {status['legal_routing_enabled']}")
        print(f"   Active policy: {status['active_policy']}")
        print(f"   Active jurisdictions: {status['active_jurisdictions']}")
        print(f"   Emergency mode: {status['emergency_mode']}")
        
        # Demo 1.5: Test master toggle
        print("\n1.5. Testing Master System Toggle:")
        print("   Disabling entire legal routing system...")
        controller.set_legal_routing_enabled(False, 'demo_user', 'Testing master disable')
        disabled_jurisdictions = controller.get_active_jurisdictions()
        print(f"   Active jurisdictions when system disabled: {disabled_jurisdictions}")
        
        print("   Re-enabling legal routing system...")
        controller.set_legal_routing_enabled(True, 'demo_user', 'Testing master enable')
        enabled_jurisdictions = controller.get_active_jurisdictions()
        print(f"   Active jurisdictions when system enabled: {enabled_jurisdictions}")
        
        # Demo 2: Change jurisdiction status
        print("\n2. Selective Jurisdiction Control:")
        print("   Disabling Iran (IR) for testing...")
        controller.set_jurisdiction_status('IR', JurisdictionStatus.DISABLED, 'demo_user', 'Testing selective control')
        
        active_after = controller.get_active_jurisdictions()
        print(f"   Active jurisdictions after change: {active_after}")
        
        # Demo 3: Switch to different policy
        print("\n3. Policy Switching:")
        controller.activate_policy('western_friendly', 'demo_user')
        
        western_active = controller.get_active_jurisdictions()
        print(f"   Western-friendly policy active jurisdictions: {western_active}")
        
        # Demo 4: Emergency mode
        print("\n4. Emergency Mode Activation:")
        controller.toggle_emergency_mode(True, 'demo_user')
        
        emergency_active = controller.get_active_jurisdictions()
        print(f"   Emergency mode active jurisdictions: {emergency_active}")
        
        # Demo 5: Feasibility check
        print("\n5. Routing Feasibility Check:")
        feasibility = controller.validate_routing_feasibility('DEFENSE', 'SECRET')
        print(f"   Feasible: {feasibility['feasible']}")
        print(f"   Active count: {feasibility['active_count']}")
        if feasibility['warnings']:
            print(f"   Warnings: {feasibility['warnings']}")
        
        print("\n=== DEMONSTRATION COMPLETE ===")
    
    demo()
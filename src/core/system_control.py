#!/usr/bin/env python3
"""
MWRASP System Control Manager
Master system enable/disable functionality for the entire MWRASP defense platform
"""

import time
import threading
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SystemState(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    EMERGENCY_SHUTDOWN = "emergency_shutdown" 
    MAINTENANCE_MODE = "maintenance_mode"
    PARTIALLY_DISABLED = "partially_disabled"


@dataclass
class SystemControlEvent:
    """System control event record"""
    event_id: str
    timestamp: float
    event_type: str
    previous_state: SystemState
    new_state: SystemState
    initiated_by: str
    reason: str
    affected_components: list


class SystemControlManager:
    """
    Master control for the entire MWRASP system
    Provides emergency shutdown and selective component disable capabilities
    """
    
    def __init__(self):
        self.system_state = SystemState.ENABLED
        self.disabled_components = set()
        self.control_lock = threading.Lock()
        self.control_events = []
        
        # Component references (will be injected)
        self.quantum_detector = None
        self.fragmentation_system = None
        self.agent_coordinator = None
        self.jurisdiction_controller = None
        self.real_world_protection = None
        self.learning_engine = None
        self.system_monitor = None
        
        # Control settings
        self.emergency_contacts = []
        self.maintenance_mode_allowed = True
        self.auto_restart_after_emergency = False
        
        print("[SYSTEM-CONTROL] Master System Control Manager initialized")
    
    def set_system_references(self, **components):
        """Inject references to all MWRASP system components"""
        self.quantum_detector = components.get('quantum_detector')
        self.fragmentation_system = components.get('fragmentation_system') 
        self.agent_coordinator = components.get('agent_coordinator')
        self.jurisdiction_controller = components.get('jurisdiction_controller')
        self.real_world_protection = components.get('real_world_protection')
        self.learning_engine = components.get('learning_engine')
        self.system_monitor = components.get('system_monitor')
        
        print("[SYSTEM-CONTROL] System component references configured")
    
    def disable_entire_system(self, reason: str = "Manual disable", initiated_by: str = "admin") -> Dict[str, Any]:
        """
        MASTER SYSTEM DISABLE - Shuts down all MWRASP components
        This is the emergency nuclear option
        """
        with self.control_lock:
            if self.system_state == SystemState.DISABLED:
                return {"message": "System already disabled", "state": self.system_state.value}
            
            previous_state = self.system_state
            self.system_state = SystemState.DISABLED
            
            print(f"[SYSTEM-CONTROL] [WARNING] DISABLING ENTIRE MWRASP SYSTEM [WARNING]")
            print(f"[SYSTEM-CONTROL] Reason: {reason}")
            print(f"[SYSTEM-CONTROL] Initiated by: {initiated_by}")
            
            # Disable all components systematically
            disabled_components = []
            
            try:
                # 1. Stop AI learning first (stops experience recording)
                if self.learning_engine and hasattr(self.learning_engine, 'learning_active'):
                    if self.learning_engine.learning_active:
                        self.learning_engine.stop_learning()
                        disabled_components.append("AI Learning Engine")
                        print("[SYSTEM-CONTROL] [OK] AI Learning Engine stopped")
                
                # 2. Stop agent coordination (stops threat responses)
                if self.agent_coordinator and hasattr(self.agent_coordinator, 'running'):
                    if self.agent_coordinator.running:
                        # Stop coordination without waiting (emergency stop)
                        self.agent_coordinator.running = False
                        disabled_components.append("Agent Coordination System")
                        print("[SYSTEM-CONTROL] [OK] Agent Coordination stopped")
                
                # 3. Disable real-world protection (stops file monitoring)
                if self.real_world_protection and hasattr(self.real_world_protection, 'protection_active'):
                    if self.real_world_protection.protection_active:
                        self.real_world_protection.stop_real_world_protection()
                        disabled_components.append("Real-World Protection")
                        print("[SYSTEM-CONTROL] [OK] Real-World Protection stopped")
                
                # 4. Disable legal routing (optional enhancement - core defense continues)
                if self.jurisdiction_controller:
                    if hasattr(self.jurisdiction_controller, 'set_legal_routing_enabled'):
                        self.jurisdiction_controller.set_legal_routing_enabled(False, initiated_by, reason)
                        disabled_components.append("Legal Routing System")
                        print("[SYSTEM-CONTROL] [OK] Legal Routing disabled")
                
                # 5. Stop system monitoring (optional - might want to keep for diagnostics)
                if self.system_monitor and hasattr(self.system_monitor, 'monitoring_active'):
                    if self.system_monitor.monitoring_active:
                        self.system_monitor.stop_monitoring()
                        disabled_components.append("System Performance Monitor")
                        print("[SYSTEM-CONTROL] [OK] System Monitoring stopped")
                
                # 6. Clear quantum detector active tokens (optional)
                if self.quantum_detector and hasattr(self.quantum_detector, 'active_tokens'):
                    token_count = len(self.quantum_detector.active_tokens)
                    if token_count > 0:
                        disabled_components.append(f"Quantum Detection ({token_count} active tokens)")
                        print(f"[SYSTEM-CONTROL] [OK] Quantum Detection noted ({token_count} tokens remain active)")
                
                # Record the control event
                self._record_control_event(
                    event_type="SYSTEM_DISABLE",
                    previous_state=previous_state,
                    new_state=self.system_state,
                    initiated_by=initiated_by,
                    reason=reason,
                    affected_components=disabled_components
                )
                
                print(f"[SYSTEM-CONTROL] [DISABLED] MWRASP SYSTEM COMPLETELY DISABLED")
                print(f"[SYSTEM-CONTROL] Components disabled: {len(disabled_components)}")
                
                return {
                    "message": "MWRASP system completely disabled",
                    "state": self.system_state.value,
                    "disabled_components": disabled_components,
                    "reason": reason,
                    "timestamp": time.time(),
                    "initiated_by": initiated_by
                }
                
            except Exception as e:
                print(f"[SYSTEM-CONTROL] [ERROR] Error during system disable: {e}")
                return {
                    "message": f"System disable partially failed: {e}",
                    "state": self.system_state.value,
                    "disabled_components": disabled_components,
                    "error": str(e)
                }
    
    def enable_entire_system(self, initiated_by: str = "admin", reason: str = "Manual enable") -> Dict[str, Any]:
        """
        MASTER SYSTEM ENABLE - Restarts all MWRASP components
        """
        with self.control_lock:
            if self.system_state == SystemState.ENABLED:
                return {"message": "System already enabled", "state": self.system_state.value}
            
            previous_state = self.system_state
            self.system_state = SystemState.ENABLED
            
            print(f"[SYSTEM-CONTROL] [ENABLING] ENABLING ENTIRE MWRASP SYSTEM")
            print(f"[SYSTEM-CONTROL] Reason: {reason}")
            print(f"[SYSTEM-CONTROL] Initiated by: {initiated_by}")
            
            # Enable all components systematically
            enabled_components = []
            
            try:
                # 1. Start system monitoring (foundation - diagnostics)
                if self.system_monitor and hasattr(self.system_monitor, 'start_monitoring'):
                    self.system_monitor.start_monitoring()
                    enabled_components.append("System Performance Monitor")
                    print("[SYSTEM-CONTROL] [OK] System Monitoring started")
                
                # 2. Start agent coordination (core intelligence - always active)
                if self.agent_coordinator and hasattr(self.agent_coordinator, 'start_coordination'):
                    if not self.agent_coordinator.running:
                        # Note: start_coordination is async, but we'll trigger it
                        self.agent_coordinator.running = True
                        enabled_components.append("Agent Coordination System")
                        print("[SYSTEM-CONTROL] [OK] Agent Coordination enabled")
                
                # 3. Enable real-world protection (core defense - always active)
                if self.real_world_protection and hasattr(self.real_world_protection, 'start_real_world_protection'):
                    self.real_world_protection.start_real_world_protection()
                    enabled_components.append("Real-World Protection")
                    print("[SYSTEM-CONTROL] [OK] Real-World Protection started")
                
                # 4. Enable legal routing (optional enhancement - can be disabled independently)
                if self.jurisdiction_controller:
                    if hasattr(self.jurisdiction_controller, 'set_legal_routing_enabled'):
                        self.jurisdiction_controller.set_legal_routing_enabled(True, initiated_by, reason)
                        enabled_components.append("Legal Routing System")
                        print("[SYSTEM-CONTROL] [OK] Legal Routing enabled (optional enhancement)")
                
                # 5. Start AI learning (continuous improvement)
                if self.learning_engine and hasattr(self.learning_engine, 'start_learning'):
                    if not self.learning_engine.learning_active:
                        self.learning_engine.start_learning()
                        enabled_components.append("AI Learning Engine")
                        print("[SYSTEM-CONTROL] [OK] AI Learning Engine started")
                
                # Record the control event
                self._record_control_event(
                    event_type="SYSTEM_ENABLE",
                    previous_state=previous_state,
                    new_state=self.system_state,
                    initiated_by=initiated_by,
                    reason=reason,
                    affected_components=enabled_components
                )
                
                print(f"[SYSTEM-CONTROL] [ENABLED] MWRASP SYSTEM COMPLETELY ENABLED")
                print(f"[SYSTEM-CONTROL] Components enabled: {len(enabled_components)}")
                
                return {
                    "message": "MWRASP system completely enabled",
                    "state": self.system_state.value,
                    "enabled_components": enabled_components,
                    "reason": reason,
                    "timestamp": time.time(),
                    "initiated_by": initiated_by
                }
                
            except Exception as e:
                print(f"[SYSTEM-CONTROL] [WARNING] Error during system enable: {e}")
                return {
                    "message": f"System enable partially failed: {e}",
                    "state": self.system_state.value,
                    "enabled_components": enabled_components,
                    "error": str(e)
                }
    
    def emergency_shutdown(self, reason: str = "Emergency situation", initiated_by: str = "emergency") -> Dict[str, Any]:
        """
        EMERGENCY SHUTDOWN - Immediate system halt with emergency protocols
        """
        with self.control_lock:
            previous_state = self.system_state
            self.system_state = SystemState.EMERGENCY_SHUTDOWN
            
            print(f"[SYSTEM-CONTROL] [EMERGENCY] EMERGENCY SHUTDOWN ACTIVATED [EMERGENCY]")
            print(f"[SYSTEM-CONTROL] Reason: {reason}")
            
            # Immediate hard stops (no graceful shutdown)
            emergency_actions = []
            
            try:
                # Stop all active processes immediately
                if self.agent_coordinator and hasattr(self.agent_coordinator, 'running'):
                    self.agent_coordinator.running = False
                    emergency_actions.append("Agent coordination halted")
                
                if self.learning_engine and hasattr(self.learning_engine, 'learning_active'):
                    self.learning_engine.learning_active = False
                    emergency_actions.append("AI learning halted")
                
                if self.real_world_protection and hasattr(self.real_world_protection, 'protection_active'):
                    self.real_world_protection.protection_active = False
                    emergency_actions.append("File protection halted")
                
                # Record emergency event
                self._record_control_event(
                    event_type="EMERGENCY_SHUTDOWN",
                    previous_state=previous_state,
                    new_state=self.system_state,
                    initiated_by=initiated_by,
                    reason=reason,
                    affected_components=emergency_actions
                )
                
                print(f"[SYSTEM-CONTROL] [SHUTDOWN] EMERGENCY SHUTDOWN COMPLETE")
                
                return {
                    "message": "EMERGENCY SHUTDOWN ACTIVATED",
                    "state": self.system_state.value,
                    "emergency_actions": emergency_actions,
                    "reason": reason,
                    "timestamp": time.time()
                }
                
            except Exception as e:
                print(f"[SYSTEM-CONTROL] [WARNING] Error during emergency shutdown: {e}")
                return {
                    "message": f"Emergency shutdown with errors: {e}",
                    "state": self.system_state.value,
                    "error": str(e)
                }
    
    def set_maintenance_mode(self, enabled: bool, reason: str = "", initiated_by: str = "admin") -> Dict[str, Any]:
        """Enable/disable maintenance mode (partial functionality)"""
        if not self.maintenance_mode_allowed:
            return {"error": "Maintenance mode not allowed", "state": self.system_state.value}
        
        with self.control_lock:
            previous_state = self.system_state
            
            if enabled:
                self.system_state = SystemState.MAINTENANCE_MODE
                # In maintenance mode, keep monitoring but disable active responses
                if self.agent_coordinator:
                    self.agent_coordinator.running = False
                message = "Maintenance mode enabled"
            else:
                self.system_state = SystemState.ENABLED
                # Re-enable responses
                if self.agent_coordinator:
                    self.agent_coordinator.running = True
                message = "Maintenance mode disabled"
            
            self._record_control_event(
                event_type="MAINTENANCE_MODE",
                previous_state=previous_state,
                new_state=self.system_state,
                initiated_by=initiated_by,
                reason=reason,
                affected_components=["Agent responses"]
            )
            
            return {
                "message": message,
                "state": self.system_state.value,
                "maintenance_mode": enabled,
                "timestamp": time.time()
            }
    
    def disable_component(self, component_name: str, reason: str = "", initiated_by: str = "admin") -> Dict[str, Any]:
        """Disable individual system component"""
        with self.control_lock:
            component_map = {
                "quantum_detection": self.quantum_detector,
                "agent_coordination": self.agent_coordinator, 
                "legal_routing": self.jurisdiction_controller,
                "real_world_protection": self.real_world_protection,
                "ai_learning": self.learning_engine,
                "system_monitoring": self.system_monitor
            }
            
            if component_name not in component_map:
                return {"error": f"Unknown component: {component_name}"}
            
            self.disabled_components.add(component_name)
            
            # Disable the specific component
            component = component_map[component_name]
            if component:
                if component_name == "agent_coordination" and hasattr(component, 'running'):
                    component.running = False
                elif component_name == "ai_learning" and hasattr(component, 'learning_active'):
                    component.learning_active = False
                elif component_name == "real_world_protection" and hasattr(component, 'protection_active'):
                    component.stop_real_world_protection()
                elif component_name == "legal_routing" and hasattr(component, 'set_legal_routing_enabled'):
                    component.set_legal_routing_enabled(False, initiated_by, reason)
                elif component_name == "system_monitoring" and hasattr(component, 'monitoring_active'):
                    component.stop_monitoring()
            
            if len(self.disabled_components) > 0:
                self.system_state = SystemState.PARTIALLY_DISABLED
            
            return {
                "message": f"Component {component_name} disabled",
                "disabled_components": list(self.disabled_components),
                "state": self.system_state.value,
                "timestamp": time.time()
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system control status"""
        component_status = {}
        
        # Check each component's actual status
        if self.quantum_detector:
            component_status["quantum_detection"] = {
                "enabled": hasattr(self.quantum_detector, 'active_tokens'),
                "active_tokens": len(getattr(self.quantum_detector, 'active_tokens', {}))
            }
        
        if self.agent_coordinator:
            component_status["agent_coordination"] = {
                "enabled": getattr(self.agent_coordinator, 'running', False),
                "agents_active": len([a for a in getattr(self.agent_coordinator, 'agents', {}).values() if a.status.value == 'active'])
            }
        
        if self.jurisdiction_controller:
            component_status["legal_routing"] = {
                "enabled": getattr(self.jurisdiction_controller, 'legal_routing_enabled', False),
                "active_jurisdictions": len(self.jurisdiction_controller.get_active_jurisdictions()) if hasattr(self.jurisdiction_controller, 'get_active_jurisdictions') else 0
            }
        
        if self.real_world_protection:
            component_status["real_world_protection"] = {
                "enabled": getattr(self.real_world_protection, 'protection_active', False),
                "protected_files": len(getattr(self.real_world_protection, 'protected_files', {}))
            }
        
        if self.learning_engine:
            component_status["ai_learning"] = {
                "enabled": getattr(self.learning_engine, 'learning_active', False),
                "experiences_processed": getattr(self.learning_engine, 'learning_stats', {}).get('experiences_processed', 0)
            }
        
        if self.system_monitor:
            component_status["system_monitoring"] = {
                "enabled": getattr(self.system_monitor, 'monitoring_active', False)
            }
        
        return {
            "system_state": self.system_state.value,
            "disabled_components": list(self.disabled_components),
            "component_status": component_status,
            "recent_control_events": self.control_events[-5:] if self.control_events else [],
            "emergency_contacts": self.emergency_contacts,
            "maintenance_mode_allowed": self.maintenance_mode_allowed,
            "last_updated": time.time()
        }
    
    def _record_control_event(self, event_type: str, previous_state: SystemState, new_state: SystemState, 
                            initiated_by: str, reason: str, affected_components: list):
        """Record system control event for audit trail"""
        import uuid
        
        event = SystemControlEvent(
            event_id=str(uuid.uuid4()),
            timestamp=time.time(),
            event_type=event_type,
            previous_state=previous_state,
            new_state=new_state,
            initiated_by=initiated_by,
            reason=reason,
            affected_components=affected_components
        )
        
        self.control_events.append({
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "previous_state": event.previous_state.value,
            "new_state": event.new_state.value,
            "initiated_by": event.initiated_by,
            "reason": event.reason,
            "affected_components": event.affected_components
        })
        
        # Keep only last 100 events
        if len(self.control_events) > 100:
            self.control_events = self.control_events[-100:]


# Global system control instance
_system_control = None

def get_system_control() -> SystemControlManager:
    """Get or create global system control instance"""
    global _system_control
    if _system_control is None:
        _system_control = SystemControlManager()
    return _system_control
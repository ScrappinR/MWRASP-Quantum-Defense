from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import time
import json
import uvicorn
from datetime import datetime

from ..core.quantum_detector import QuantumDetector, ThreatLevel
from ..core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
from ..core.agent_system import AutonomousDefenseCoordinator
from ..core.jurisdiction_control import JurisdictionController
from ..core.real_world_protection import create_real_world_protection
from ..core.system_monitor import get_system_monitor, get_performance_metrics, get_resource_usage
from ..core.ai_learning_engine import get_learning_engine
from ..core.system_control import get_system_control
from ..core.milspec_compliance import get_milspec_engine, SecurityClassification, CMMCLevel
from ..core.top_secret_upgrade import get_ts_upgrade_planner
from .websocket import websocket_manager


class ThreatResponse(BaseModel):
    threat_id: str
    threat_level: str
    detection_time: float
    attack_vector: str
    quantum_indicators: List[str]
    affected_tokens: List[str]
    confidence_score: float


class FragmentRequest(BaseModel):
    data: str
    fragment_id: Optional[str] = None
    policy: Optional[Dict[str, Any]] = None


class TokenRequest(BaseModel):
    data_type: str = "sensitive"


class AgentStatusResponse(BaseModel):
    agents_by_role: Dict[str, List[Dict]]
    total_agents: int
    coordination_stats: Dict[str, Any]
    recent_actions: int
    system_running: bool


class SystemStatsResponse(BaseModel):
    quantum_detector: Dict[str, Any]
    temporal_fragmentation: Dict[str, Any]
    agent_coordination: Dict[str, Any]
    system_uptime: float


class MWRASPServer:
    def __init__(self):
        # Initialize core systems with enhanced quantum detection
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.7, government_compliance=True)
        self.fragmentation_system = TemporalFragmentation()
        self.jurisdiction_controller = JurisdictionController()
        self.agent_coordinator = AutonomousDefenseCoordinator(
            self.quantum_detector, 
            self.fragmentation_system
        )
        
        # Initialize real-world protection
        self.real_world_protection = create_real_world_protection(
            self.quantum_detector,
            self.fragmentation_system, 
            self.jurisdiction_controller
        )
        
        # Initialize system control (master enable/disable)
        self.system_control = get_system_control()
        self.system_control.set_system_references(
            quantum_detector=self.quantum_detector,
            fragmentation_system=self.fragmentation_system,
            agent_coordinator=self.agent_coordinator,
            jurisdiction_controller=self.jurisdiction_controller,
            real_world_protection=self.real_world_protection,
            learning_engine=get_learning_engine(),
            system_monitor=get_system_monitor()
        )
        
        # System tracking
        self.start_time = time.time()
        self.active_sessions = {}
        
        # FastAPI app setup
        self.app = FastAPI(
            title="MWRASP Quantum Defense System",
            description="Multi-Wavelength Rapid-Aging Surveillance Platform with Quantum Attack Detection",
            version="1.0.0"
        )
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files for dashboard
        import os
        dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
        print(f"Dashboard path: {dashboard_path}")
        print(f"Dashboard exists: {os.path.exists(dashboard_path)}")
        if os.path.exists(dashboard_path):
            self.app.mount("/static", StaticFiles(directory=dashboard_path), name="static")
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        @self.app.on_event("startup")
        async def startup_event():
            """Start all systems on server startup"""
            # Start quantum threat monitoring with enhanced detection
            self.quantum_detector.start_monitoring()
            
            await self.agent_coordinator.start_coordination()
            
            # Setup WebSocket manager with system references
            websocket_manager.set_system_references(
                self.quantum_detector,
                self.fragmentation_system, 
                self.agent_coordinator
            )
            print("MWRASP Quantum Defense System online with enhanced quantum detection")
        
        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Clean shutdown of all systems"""
            # Stop quantum monitoring
            self.quantum_detector.stop_monitoring()
            
            await self.agent_coordinator.stop_coordination()
            print("MWRASP Quantum Defense System offline")
        
        # Health check endpoint
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "uptime": time.time() - self.start_time,
                "systems": {
                    "quantum_detector": "active" if self.quantum_detector._monitoring else "inactive",
                    "quantum_detection_cache": f"{len(self.quantum_detector._pattern_cache)} cached patterns",
                    "temporal_fragmentation": "active",
                    "agent_coordination": "active" if self.agent_coordinator.running else "inactive"
                }
            }
        
        # System statistics
        @self.app.get("/stats", response_model=SystemStatsResponse)
        async def get_system_stats():
            return SystemStatsResponse(
                quantum_detector=self.quantum_detector.get_threat_statistics(),
                temporal_fragmentation=self.fragmentation_system.get_system_stats(),
                agent_coordination=self.agent_coordinator.get_agent_status(),
                system_uptime=time.time() - self.start_time
            )
        
        # Real performance monitoring endpoints
        @self.app.get("/performance/current")
        async def get_current_performance():
            """Get real-time MWRASP performance metrics"""
            return get_performance_metrics()
        
        @self.app.get("/performance/resources")
        async def get_resource_usage_endpoint():
            """Get MWRASP resource usage summary"""
            return get_resource_usage()
        
        @self.app.get("/performance/history")
        async def get_performance_history_endpoint():
            """Get performance history for charts"""
            monitor = get_system_monitor()
            return monitor.get_performance_history()
        
        @self.app.get("/performance/processes")
        async def get_process_details():
            """Get detailed information about MWRASP processes"""
            monitor = get_system_monitor()
            return monitor.get_detailed_process_info()
        
        @self.app.get("/performance/report")
        async def get_performance_report():
            """Get comprehensive performance report"""
            monitor = get_system_monitor()
            return monitor.export_performance_report()
        
        # AI Learning System endpoints
        @self.app.get("/ai-learning/statistics")
        async def get_learning_statistics():
            """Get AI learning system statistics"""
            learning_engine = get_learning_engine()
            return learning_engine.get_learning_statistics()
        
        @self.app.post("/ai-learning/customer-feedback")
        async def update_customer_feedback(feedback: Dict[str, Any]):
            """Update customer profile based on feedback"""
            learning_engine = get_learning_engine()
            customer_id = feedback.get('customer_id', 'default')
            learning_engine.update_customer_profile(customer_id, feedback)
            return {"message": "Customer profile updated", "customer_id": customer_id}
        
        @self.app.get("/ai-learning/agent-models")
        async def get_agent_models():
            """Get information about agent learning models"""
            learning_engine = get_learning_engine()
            stats = learning_engine.get_learning_statistics()
            return {
                "trained_agents": stats['trained_agent_models'],
                "total_experiences": stats['experiences_in_buffer'],
                "learning_active": stats['learning_active'],
                "agent_specializations": {
                    agent.agent_id: {
                        "role": agent.role.value,
                        "success_rate": agent.success_rate,
                        "specialization_areas": agent.specialization_areas,
                        "knowledge_confidence": agent.knowledge_confidence,
                        "experience_count": agent.experience_count,
                        "learned_patterns": len(agent.learned_patterns)
                    }
                    for agent in self.agent_coordinator.agents.values()
                    if agent.learning_enabled
                }
            }
        
        @self.app.post("/ai-learning/enable-agent-learning")
        async def enable_agent_learning(agent_config: Dict[str, Any]):
            """Enable/disable learning for specific agents"""
            agent_id = agent_config.get('agent_id')
            learning_enabled = agent_config.get('learning_enabled', True)
            adaptation_level = agent_config.get('adaptation_level', 'moderate')
            
            if agent_id in self.agent_coordinator.agents:
                agent = self.agent_coordinator.agents[agent_id]
                agent.learning_enabled = learning_enabled
                agent.adaptation_level = adaptation_level
                return {
                    "message": f"Learning {'enabled' if learning_enabled else 'disabled'} for agent {agent_id}",
                    "agent_id": agent_id,
                    "learning_enabled": learning_enabled,
                    "adaptation_level": adaptation_level
                }
            else:
                raise HTTPException(status_code=404, detail="Agent not found")
        
        @self.app.get("/ai-learning/knowledge-patterns")
        async def get_knowledge_patterns():
            """Get discovered knowledge patterns"""
            learning_engine = get_learning_engine()
            stats = learning_engine.get_learning_statistics()
            return {
                "total_patterns": stats['knowledge_patterns'],
                "top_patterns": stats['top_patterns'],
                "discovery_rate": stats['learning_stats']['patterns_discovered']
            }
        
        # System Control endpoints (Master Enable/Disable)
        @self.app.get("/system-control/status")
        async def get_system_control_status():
            """Get comprehensive system control status"""
            return self.system_control.get_system_status()
        
        @self.app.post("/system-control/disable")
        async def disable_entire_system(control_request: Dict[str, Any]):
            """EMERGENCY: Disable entire MWRASP system"""
            reason = control_request.get('reason', 'Manual disable request')
            initiated_by = control_request.get('initiated_by', 'api_user')
            confirm = control_request.get('confirm_disable', False)
            
            if not confirm:
                raise HTTPException(
                    status_code=400, 
                    detail="Must set 'confirm_disable': true to disable entire system"
                )
            
            result = self.system_control.disable_entire_system(reason, initiated_by)
            return result
        
        @self.app.post("/system-control/enable")
        async def enable_entire_system(control_request: Dict[str, Any]):
            """Enable entire MWRASP system"""
            reason = control_request.get('reason', 'Manual enable request')
            initiated_by = control_request.get('initiated_by', 'api_user')
            
            result = self.system_control.enable_entire_system(initiated_by, reason)
            return result
        
        @self.app.post("/system-control/emergency-shutdown")
        async def emergency_shutdown(control_request: Dict[str, Any]):
            """EMERGENCY SHUTDOWN: Immediate system halt"""
            reason = control_request.get('reason', 'Emergency shutdown request')
            initiated_by = control_request.get('initiated_by', 'emergency_user')
            confirm = control_request.get('confirm_emergency', False)
            
            if not confirm:
                raise HTTPException(
                    status_code=400,
                    detail="Must set 'confirm_emergency': true for emergency shutdown"
                )
            
            result = self.system_control.emergency_shutdown(reason, initiated_by)
            return result
        
        @self.app.post("/system-control/maintenance-mode")
        async def set_maintenance_mode(control_request: Dict[str, Any]):
            """Enable/disable maintenance mode"""
            enabled = control_request.get('enabled', False)
            reason = control_request.get('reason', 'Maintenance mode request')
            initiated_by = control_request.get('initiated_by', 'admin')
            
            result = self.system_control.set_maintenance_mode(enabled, reason, initiated_by)
            return result
        
        @self.app.post("/system-control/disable-component")
        async def disable_component(control_request: Dict[str, Any]):
            """Disable individual system component"""
            component_name = control_request.get('component')
            reason = control_request.get('reason', 'Component disable request')
            initiated_by = control_request.get('initiated_by', 'admin')
            
            if not component_name:
                raise HTTPException(status_code=400, detail="Must specify 'component' name")
            
            result = self.system_control.disable_component(component_name, reason, initiated_by)
            return result
        
        @self.app.post("/legal-routing/enable")
        async def enable_legal_routing(control_request: Dict[str, Any]):
            """Enable legal routing independently from core defense systems"""
            reason = control_request.get('reason', 'Legal routing enable request')
            initiated_by = control_request.get('initiated_by', 'admin')
            
            try:
                if self.jurisdiction_controller and hasattr(self.jurisdiction_controller, 'set_legal_routing_enabled'):
                    self.jurisdiction_controller.set_legal_routing_enabled(True, initiated_by, reason)
                    return {
                        "success": True,
                        "message": "Legal routing enabled (enhancement active)",
                        "status": "enabled",
                        "note": "Core defense systems unaffected",
                        "timestamp": time.time()
                    }
                else:
                    return {
                        "success": False,
                        "message": "Legal routing not available",
                        "status": "unavailable"
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error enabling legal routing: {str(e)}")
        
        @self.app.post("/legal-routing/disable") 
        async def disable_legal_routing(control_request: Dict[str, Any]):
            """Disable legal routing while keeping core defense systems active"""
            reason = control_request.get('reason', 'Legal routing disable request')
            initiated_by = control_request.get('initiated_by', 'admin')
            
            try:
                if self.jurisdiction_controller and hasattr(self.jurisdiction_controller, 'set_legal_routing_enabled'):
                    self.jurisdiction_controller.set_legal_routing_enabled(False, initiated_by, reason)
                    return {
                        "success": True,
                        "message": "Legal routing disabled (core defense still active)",
                        "status": "disabled",
                        "note": "Agents, protection, and AI learning continue operating",
                        "timestamp": time.time()
                    }
                else:
                    return {
                        "success": False,
                        "message": "Legal routing not available",
                        "status": "unavailable"
                    }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error disabling legal routing: {str(e)}")
        
        # Quantum threat detection endpoints
        @self.app.post("/quantum/token")
        async def create_canary_token(request: TokenRequest):
            """Create a new quantum canary token"""
            token = self.quantum_detector.generate_canary_token(request.data_type)
            return {
                "token_id": token.token_id,
                "created_at": token.created_at,
                "data_type": request.data_type,
                "quantum_signature": token.quantum_signature[:16]  # Partial for security
            }
        
        @self.app.post("/quantum/access/{token_id}")
        async def access_canary_token(token_id: str, accessor_id: Optional[str] = None):
            """Access a canary token and trigger quantum detection"""
            threat_detected = self.quantum_detector.access_token(token_id, accessor_id)
            
            response = {
                "token_id": token_id,
                "access_time": time.time(),
                "threat_detected": threat_detected
            }
            
            if threat_detected:
                recent_threats = self.quantum_detector.get_active_threats()
                if recent_threats:
                    latest_threat = recent_threats[-1]
                    response["threat_info"] = {
                        "threat_id": latest_threat.threat_id,
                        "threat_level": latest_threat.threat_level.name,
                        "confidence": latest_threat.confidence_score,
                        "indicators": latest_threat.quantum_indicators
                    }
            
            return response
        
        @self.app.get("/quantum/threats")
        async def get_active_threats():
            """Get all active quantum threats"""
            threats = self.quantum_detector.get_active_threats()
            return [
                ThreatResponse(
                    threat_id=threat.threat_id,
                    threat_level=threat.threat_level.name,
                    detection_time=threat.detection_time,
                    attack_vector=threat.attack_vector,
                    quantum_indicators=threat.quantum_indicators,
                    affected_tokens=threat.affected_tokens,
                    confidence_score=threat.confidence_score
                ) for threat in threats
            ]
        
        @self.app.get("/quantum/statistics")
        async def get_quantum_statistics():
            """Get quantum detection statistics including enhanced detection metrics"""
            stats = self.quantum_detector.get_threat_statistics()
            
            # Add enhanced detection performance metrics
            stats.update({
                "enhanced_detection": {
                    "cache_size": len(self.quantum_detector._pattern_cache),
                    "cache_hit_efficiency": "optimized for sub-100ms response",
                    "quantum_algorithms_detected": [
                        "simons_algorithm", "grovers_algorithm", "shors_algorithm",
                        "bernstein_vazirani_algorithm", "deutsch_jozsa_algorithm"
                    ],
                    "detection_accuracy": {
                        "simons_algorithm": "100%",
                        "shors_algorithm": "implemented",
                        "grovers_algorithm": "26.7% (needs improvement)",
                        "overall_performance": "sub-100ms response time"
                    }
                }
            })
            
            return stats
        
        # Temporal fragmentation endpoints
        @self.app.post("/temporal/fragment")
        async def fragment_data(request: FragmentRequest):
            """Fragment data using temporal fragmentation"""
            data_bytes = request.data.encode('utf-8')
            
            # Apply custom policy if provided
            policy = FragmentationPolicy()
            if request.policy:
                for key, value in request.policy.items():
                    if hasattr(policy, key):
                        setattr(policy, key, value)
            
            # Create temporary fragmentation system with custom policy
            temp_fragmenter = TemporalFragmentation(policy)
            fragments = temp_fragmenter.fragment_data(data_bytes, request.fragment_id)
            
            return {
                "original_id": request.fragment_id or fragments[0].original_hash[:16],
                "fragments_created": len(fragments),
                "fragment_ids": [f.fragment_id for f in fragments],
                "expires_at": fragments[0].expires_at,
                "fragmentation_policy": {
                    "lifetime_ms": policy.max_fragment_lifetime_ms,
                    "min_fragments": policy.min_fragments,
                    "quantum_resistance": policy.quantum_resistance_level
                }
            }
        
        @self.app.post("/temporal/reconstruct/{original_id}")
        async def reconstruct_data(original_id: str):
            """Attempt to reconstruct fragmented data"""
            reconstructed = self.fragmentation_system.reconstruct_data(original_id)
            
            if reconstructed:
                return {
                    "original_id": original_id,
                    "reconstructed": True,
                    "data_size": len(reconstructed),
                    "data_preview": reconstructed[:100].decode('utf-8', errors='ignore'),
                    "reconstruction_time": time.time()
                }
            else:
                return {
                    "original_id": original_id,
                    "reconstructed": False,
                    "reason": "fragments_expired_or_insufficient",
                    "reconstruction_time": time.time()
                }
        
        @self.app.get("/temporal/status/{original_id}")
        async def get_fragment_status(original_id: str):
            """Get status of fragmented data"""
            status = self.fragmentation_system.get_fragment_status(original_id)
            return {
                "original_id": original_id,
                "status": status,
                "timestamp": time.time()
            }
        
        @self.app.delete("/temporal/expire/{original_id}")
        async def force_expire_fragments(original_id: str):
            """Force immediate expiration of fragments"""
            self.fragmentation_system.force_expire_all(original_id)
            return {
                "original_id": original_id,
                "action": "force_expired",
                "timestamp": time.time()
            }
        
        @self.app.get("/temporal/statistics")
        async def get_temporal_statistics():
            """Get temporal fragmentation statistics"""
            return self.fragmentation_system.get_system_stats()
        
        # Agent coordination endpoints
        @self.app.get("/agents/status", response_model=AgentStatusResponse)
        async def get_agent_status():
            """Get status of all defense agents"""
            status = self.agent_coordinator.get_agent_status()
            return AgentStatusResponse(**status)
        
        @self.app.post("/agents/coordinate")
        async def trigger_coordination():
            """Manually trigger agent coordination"""
            # Create a synthetic threat to demonstrate coordination
            synthetic_threat_message = {
                "type": "threat_escalation",
                "threat_id": f"manual_trigger_{int(time.time())}",
                "level": 8,
                "source": "manual_api_call"
            }
            
            await self.agent_coordinator.send_coordination_message(synthetic_threat_message)
            
            return {
                "coordination_triggered": True,
                "timestamp": time.time(),
                "message": "Agent coordination sequence initiated"
            }
        
        @self.app.post("/agents/message")
        async def send_agent_message(message: Dict[str, Any]):
            """Send a custom message to the agent coordination system"""
            await self.agent_coordinator.send_coordination_message(message)
            return {
                "message_sent": True,
                "timestamp": time.time(),
                "message_type": message.get("type", "unknown")
            }
        
        # Jurisdiction control endpoints
        @self.app.get("/jurisdiction/status")
        async def get_jurisdiction_status():
            """Get comprehensive jurisdiction control system status"""
            return self.jurisdiction_controller.get_control_status()
        
        @self.app.post("/jurisdiction/master-toggle")
        async def toggle_master_system(enabled: bool, updated_by: Optional[str] = "api_user", reason: Optional[str] = ""):
            """Toggle the master legal routing system on/off"""
            success = self.jurisdiction_controller.set_legal_routing_enabled(enabled, updated_by, reason)
            return {
                "success": success,
                "legal_routing_enabled": self.jurisdiction_controller.is_legal_routing_enabled(),
                "timestamp": time.time(),
                "updated_by": updated_by
            }
        
        @self.app.get("/jurisdiction/master-status")
        async def get_master_system_status():
            """Get master legal routing system status"""
            return {
                "legal_routing_enabled": self.jurisdiction_controller.is_legal_routing_enabled(),
                "timestamp": time.time()
            }
        
        @self.app.post("/jurisdiction/set-status/{jurisdiction_code}")
        async def set_jurisdiction_status(jurisdiction_code: str, status: str, 
                                        updated_by: Optional[str] = "api_user", reason: Optional[str] = ""):
            """Set status of a specific jurisdiction"""
            from ..core.jurisdiction_control import JurisdictionStatus
            
            try:
                status_enum = JurisdictionStatus(status)
                success = self.jurisdiction_controller.set_jurisdiction_status(
                    jurisdiction_code, status_enum, updated_by, reason
                )
                return {
                    "success": success,
                    "jurisdiction": jurisdiction_code,
                    "new_status": status,
                    "timestamp": time.time()
                }
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        @self.app.post("/jurisdiction/activate-policy/{policy_name}")
        async def activate_jurisdiction_policy(policy_name: str, updated_by: Optional[str] = "api_user"):
            """Activate a jurisdiction routing policy"""
            success = self.jurisdiction_controller.activate_policy(policy_name, updated_by)
            if not success:
                raise HTTPException(status_code=400, detail=f"Policy not found: {policy_name}")
            
            return {
                "success": success,
                "active_policy": policy_name,
                "timestamp": time.time(),
                "updated_by": updated_by
            }
        
        @self.app.get("/jurisdiction/active-jurisdictions")
        async def get_active_jurisdictions(data_type: Optional[str] = None, user_clearance: Optional[str] = None):
            """Get list of currently active jurisdictions for routing"""
            active = self.jurisdiction_controller.get_active_jurisdictions(data_type, user_clearance)
            return {
                "active_jurisdictions": active,
                "count": len(active),
                "legal_routing_enabled": self.jurisdiction_controller.is_legal_routing_enabled(),
                "timestamp": time.time()
            }
        
        @self.app.get("/jurisdiction/feasibility")
        async def check_routing_feasibility(data_type: Optional[str] = None, 
                                          user_clearance: Optional[str] = None,
                                          min_jurisdictions: int = 3):
            """Check if current jurisdiction configuration allows feasible routing"""
            feasibility = self.jurisdiction_controller.validate_routing_feasibility(
                data_type, user_clearance, min_jurisdictions
            )
            return feasibility
        
        @self.app.post("/jurisdiction/emergency-toggle")
        async def toggle_emergency_mode(enabled: bool, activated_by: Optional[str] = "api_user"):
            """Toggle emergency mode (activates all jurisdictions)"""
            success = self.jurisdiction_controller.toggle_emergency_mode(enabled, activated_by)
            return {
                "success": success,
                "emergency_mode": enabled,
                "timestamp": time.time(),
                "activated_by": activated_by
            }
        
        # Real-world protection endpoints
        @self.app.post("/protection/start")
        async def start_real_world_protection():
            """Start real-world file and network protection"""
            try:
                self.real_world_protection.start_real_world_protection()
                return {
                    "success": True,
                    "message": "Real-world protection started",
                    "timestamp": time.time()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to start protection: {str(e)}")
        
        @self.app.post("/protection/stop")
        async def stop_real_world_protection():
            """Stop real-world protection"""
            try:
                self.real_world_protection.stop_real_world_protection()
                return {
                    "success": True,
                    "message": "Real-world protection stopped",
                    "timestamp": time.time()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to stop protection: {str(e)}")
        
        @self.app.post("/protection/add-directory")
        async def add_protected_directory(directory_path: str, protection_level: str = "HIGH"):
            """Add a directory to real-world protection"""
            try:
                success = self.real_world_protection.add_protected_directory(directory_path, protection_level)
                if success:
                    return {
                        "success": True,
                        "directory": directory_path,
                        "protection_level": protection_level,
                        "message": f"Directory {directory_path} is now protected",
                        "timestamp": time.time()
                    }
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to protect directory: {directory_path}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error adding directory: {str(e)}")
        
        @self.app.post("/protection/protect-high-value-files")
        async def protect_high_value_files():
            """Automatically detect and protect high-value files"""
            try:
                files_protected = self.real_world_protection.add_high_value_files()
                return {
                    "success": True,
                    "files_protected": files_protected,
                    "message": f"Protected {files_protected} high-value files",
                    "timestamp": time.time()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error protecting files: {str(e)}")
        
        @self.app.get("/protection/status")
        async def get_protection_status():
            """Get comprehensive real-world protection status"""
            try:
                status = self.real_world_protection.get_protection_status()
                return status
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")
        
        # Simulation and testing endpoints
        @self.app.post("/simulate/quantum_attack")
        async def simulate_quantum_attack(intensity: int = 5):
            """Simulate a quantum computer attack for testing"""
            # Create multiple canary tokens
            tokens = []
            for i in range(intensity):
                token = self.quantum_detector.generate_canary_token(f"test_data_{i}")
                tokens.append(token)
            
            # Simulate rapid access patterns that would trigger quantum detection
            await asyncio.sleep(0.01)  # Small delay
            
            detected_threats = []
            for token in tokens:
                # Access tokens in rapid succession
                threat_detected = self.quantum_detector.access_token(
                    token.token_id, 
                    f"quantum_simulator_{i}"
                )
                if threat_detected:
                    detected_threats.append(token.token_id)
                
                # Minimal delay between accesses to trigger superposition detection
                await asyncio.sleep(0.001)
            
            return {
                "simulation": "quantum_attack",
                "intensity": intensity,
                "tokens_created": len(tokens),
                "threats_detected": len(detected_threats),
                "threat_tokens": detected_threats,
                "timestamp": time.time()
            }
        
        @self.app.post("/simulate/temporal_breach")
        async def simulate_temporal_breach():
            """Simulate a temporal fragmentation breach scenario"""
            # Fragment sensitive test data
            test_data = "CLASSIFIED: Quantum encryption keys and temporal signatures"
            fragments = self.fragmentation_system.fragment_data(
                test_data.encode(), 
                "breach_simulation"
            )
            
            # Wait for partial expiration
            await asyncio.sleep(0.05)  # 50ms
            
            # Attempt reconstruction
            reconstructed = self.fragmentation_system.reconstruct_data("breach_simulation")
            
            return {
                "simulation": "temporal_breach",
                "original_data_size": len(test_data),
                "fragments_created": len(fragments),
                "reconstruction_successful": reconstructed is not None,
                "reconstructed_size": len(reconstructed) if reconstructed else 0,
                "timestamp": time.time()
            }
        
        # Dashboard endpoints
        @self.app.get("/dashboard/index.html", response_class=HTMLResponse)
        async def get_dashboard_index():
            """Serve the main dashboard"""
            import os
            dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "index.html")
            try:
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Dashboard not found")
        
        @self.app.get("/dashboard/app.js")
        async def get_dashboard_js():
            """Serve dashboard JavaScript"""
            import os
            js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "app.js")
            return FileResponse(js_path, media_type="application/javascript")
        
        @self.app.get("/dashboard/style.css")
        async def get_dashboard_css():
            """Serve dashboard CSS"""
            import os
            css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "style.css")
            return FileResponse(css_path, media_type="text/css")
            
        @self.app.get("/demo/jurisdiction", response_class=HTMLResponse)
        async def get_jurisdiction_demo():
            """Serve the jurisdiction control demo page"""
            import os
            demo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "jurisdiction_demo.html")
            try:
                with open(demo_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Jurisdiction demo not found")
                
        @self.app.get("/dashboard/unified", response_class=HTMLResponse)
        async def get_unified_dashboard():
            """Serve the unified MWRASP control center dashboard"""
            import os
            unified_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "unified_dashboard.html")
            try:
                with open(unified_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Unified dashboard not found")
                
        @self.app.get("/dashboard/financial", response_class=HTMLResponse)
        async def get_financial_dashboard():
            """Serve the financial services defense center dashboard"""
            import os
            financial_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "financial_dashboard.html")
            try:
                with open(financial_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Financial dashboard not found")
                
        @self.app.get("/dashboard/live", response_class=HTMLResponse)
        async def get_live_protection_dashboard():
            """Serve the live protection demonstration dashboard"""
            import os
            live_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "live_protection.html")
            try:
                with open(live_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Live protection dashboard not found")
        
        # New v2 Dashboard endpoints
        @self.app.get("/dashboard/index_v2.html", response_class=HTMLResponse)
        async def get_dashboard_v2():
            """Serve the new v2 dashboard"""
            import os
            dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "index_v2.html")
            try:
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Dashboard v2 not found")
        
        @self.app.get("/dashboard/app_v2.js")
        async def get_dashboard_v2_js():
            """Serve v2 dashboard JavaScript"""
            import os
            js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "app_v2.js")
            return FileResponse(js_path, media_type="application/javascript")
        
        @self.app.get("/dashboard/style_v2.css")
        async def get_dashboard_v2_css():
            """Serve v2 dashboard CSS"""
            import os
            css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "style_v2.css")
            return FileResponse(css_path, media_type="text/css")
            
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def get_dashboard():
            """Redirect to main dashboard"""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>MWRASP Quantum Defense Dashboard</title>
                <meta http-equiv="refresh" content="0;url=/dashboard/index.html">
            </head>
            <body>
                <h1>MWRASP Quantum Defense System</h1>
                <p>Redirecting to <a href="/dashboard/index.html">full dashboard</a>...</p>
                <p>System Status: Online</p>
                <p>Uptime: {uptime:.1f} seconds</p>
            </body>
            </html>
            """.format(uptime=time.time() - self.start_time)
        
        # WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates"""
            await websocket_manager.connect(websocket)
            try:
                while True:
                    # Wait for messages from client
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    await websocket_manager.handle_client_message(websocket, message)
            except WebSocketDisconnect:
                websocket_manager.disconnect(websocket)
            except Exception as e:
                print(f"WebSocket error: {e}")
                websocket_manager.disconnect(websocket)

        # Real legal conflicts endpoint
        @self.app.get("/legal/real-conflicts")
        async def get_real_legal_conflicts():
            """Get current real legal conflicts from government sources"""
            try:
                if hasattr(self.fragmentation_system.legal_engine, 'real_legal_checker'):
                    real_checker = self.fragmentation_system.legal_engine.real_legal_checker
                    
                    # Get active conflicts
                    conflicts = real_checker.get_active_conflicts()
                    
                    # Format for API response
                    conflicts_data = []
                    for conflict in conflicts:
                        conflicts_data.append({
                            'conflict_id': conflict.conflict_id,
                            'source_jurisdiction': conflict.source_jurisdiction,
                            'target_jurisdiction': conflict.target_jurisdiction,
                            'conflict_type': conflict.conflict_type,
                            'severity': conflict.severity,
                            'effective_date': conflict.effective_date.isoformat(),
                            'source_url': conflict.source_url,
                            'verified': conflict.verified,
                            'last_updated': conflict.last_updated.isoformat()
                        })
                    
                    return {
                        'real_conflicts': conflicts_data,
                        'total_conflicts': len(conflicts_data),
                        'last_update': real_checker.last_update.isoformat(),
                        'update_interval_minutes': real_checker.update_interval // 60
                    }
                else:
                    return {
                        'error': 'Real legal checker not initialized',
                        'real_conflicts': [],
                        'total_conflicts': 0
                    }
                    
            except Exception as e:
                return {
                    'error': f'Error fetching real legal conflicts: {e}',
                    'real_conflicts': [],
                    'total_conflicts': 0
                }

        # Compliance requirements endpoint
        @self.app.get("/legal/compliance-requirements/{jurisdiction}")
        async def get_compliance_requirements(jurisdiction: str):
            """Get compliance requirements for specific jurisdiction"""
            try:
                if hasattr(self.fragmentation_system.legal_engine, 'real_legal_checker'):
                    real_checker = self.fragmentation_system.legal_engine.real_legal_checker
                    
                    # Get compliance requirements
                    requirements = real_checker.get_compliance_requirements(jurisdiction)
                    
                    # Format for API response
                    requirements_data = []
                    for req in requirements:
                        requirements_data.append({
                            'requirement_id': req.requirement_id,
                            'jurisdiction': req.jurisdiction,
                            'regulation_name': req.regulation_name,
                            'compliance_type': req.compliance_type,
                            'mandatory': req.mandatory,
                            'effective_date': req.effective_date.isoformat(),
                            'source_agency': req.source_agency,
                            'details': req.details
                        })
                    
                    return {
                        'jurisdiction': jurisdiction,
                        'requirements': requirements_data,
                        'total_requirements': len(requirements_data),
                        'mandatory_count': sum(1 for req in requirements if req.mandatory)
                    }
                else:
                    return {
                        'error': 'Real legal checker not initialized',
                        'jurisdiction': jurisdiction,
                        'requirements': [],
                        'total_requirements': 0
                    }
                    
            except Exception as e:
                return {
                    'error': f'Error fetching compliance requirements: {e}',
                    'jurisdiction': jurisdiction,
                    'requirements': [],
                    'total_requirements': 0
                }

        # Legal validation endpoint
        @self.app.post("/legal/validate-routing")
        async def validate_legal_routing(routing_request: Dict[str, Any]):
            """Validate data routing against real legal conflicts and compliance"""
            try:
                source = routing_request.get('source_jurisdiction')
                destination = routing_request.get('destination_jurisdiction')
                data_type = routing_request.get('data_type', 'general')
                
                if not source or not destination:
                    return {
                        'valid': False,
                        'reason': 'Missing source or destination jurisdiction'
                    }
                
                if hasattr(self.fragmentation_system.legal_engine, 'real_legal_checker'):
                    real_checker = self.fragmentation_system.legal_engine.real_legal_checker
                    
                    # Validate routing
                    is_valid, reason = await real_checker.data_source.validate_data_routing(
                        source, destination, data_type
                    )
                    
                    # Calculate risk score
                    risk_score = real_checker.calculate_routing_risk(source, destination)
                    
                    return {
                        'valid': is_valid,
                        'reason': reason,
                        'risk_score': risk_score,
                        'source_jurisdiction': source,
                        'destination_jurisdiction': destination,
                        'data_type': data_type,
                        'timestamp': time.time()
                    }
                else:
                    return {
                        'valid': False,
                        'reason': 'Real legal checker not initialized'
                    }
                    
            except Exception as e:
                return {
                    'valid': False,
                    'reason': f'Validation error: {e}'
                }

        # MILSPEC Compliance Endpoints
        @self.app.get("/milspec/cmmc-assessment")
        async def get_cmmc_assessment():
            """Get CMMC 2.0 compliance assessment report"""
            try:
                milspec_engine = get_milspec_engine()
                assessment = await milspec_engine.generate_cmmc_assessment_report()
                return assessment
                
            except Exception as e:
                return {
                    'error': f'CMMC assessment error: {e}',
                    'cmmc_level': 'UNKNOWN',
                    'certification_status': 'ERROR'
                }

        @self.app.get("/milspec/nist-800-171-compliance")
        async def get_nist_compliance():
            """Get NIST SP 800-171 compliance assessment"""
            try:
                milspec_engine = get_milspec_engine()
                compliance = await milspec_engine.assess_nist_800_171_compliance()
                return compliance
                
            except Exception as e:
                return {
                    'error': f'NIST compliance assessment error: {e}',
                    'compliance_percentage': 0,
                    'overall_status': 'ERROR'
                }

        @self.app.get("/milspec/security-clearance-eligibility")
        async def get_security_clearance_eligibility():
            """Get security clearance eligibility assessment"""
            try:
                milspec_engine = get_milspec_engine()
                eligibility = milspec_engine.get_security_clearance_eligibility()
                return eligibility
                
            except Exception as e:
                return {
                    'error': f'Security clearance assessment error: {e}',
                    'clearance_eligibility': {},
                    'current_classification': 'UNKNOWN'
                }

        @self.app.post("/milspec/sanitize-data")
        async def sanitize_data_dod_5220_22_m(sanitization_request: Dict[str, Any]):
            """Perform DoD 5220.22-M compliant data sanitization"""
            try:
                device_path = sanitization_request.get('device_path')
                classification = SecurityClassification(sanitization_request.get('classification', 'CUI'))
                operator_id = sanitization_request.get('operator_id', 'SYSTEM_OPERATOR')
                witness_id = sanitization_request.get('witness_id', 'SYSTEM_WITNESS')
                
                if not device_path:
                    return {
                        'success': False,
                        'error': 'Device path required for sanitization'
                    }
                
                milspec_engine = get_milspec_engine()
                sanitization_record = await milspec_engine.perform_dod_5220_22_m_sanitization(
                    device_path, classification, operator_id, witness_id
                )
                
                return {
                    'success': True,
                    'sanitization_id': sanitization_record.sanitization_id,
                    'method': sanitization_record.sanitization_method,
                    'pass_count': sanitization_record.pass_count,
                    'certificate_number': sanitization_record.certificate_number,
                    'verification_hash': sanitization_record.verification_hash,
                    'timestamp': sanitization_record.timestamp.isoformat()
                }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Sanitization error: {e}'
                }

        @self.app.post("/milspec/set-classification-level")
        async def set_classification_level(classification_request: Dict[str, Any]):
            """Set system security classification level"""
            try:
                classification_str = classification_request.get('classification_level', 'CUI')
                classification = SecurityClassification(classification_str)
                
                # Reinitialize MILSPEC engine with new classification
                global milspec_engine
                milspec_engine = get_milspec_engine(classification)
                
                return {
                    'success': True,
                    'classification_level': classification.value,
                    'cmmc_level': milspec_engine.cmmc_level.value,
                    'message': f'Classification level set to {classification.value}'
                }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Classification setting error: {e}'
                }

        @self.app.get("/milspec/audit-records")
        async def get_audit_records():
            """Get compliance audit records for DoD review"""
            try:
                milspec_engine = get_milspec_engine()
                
                # Convert audit records to JSON-serializable format
                audit_records = []
                for record in milspec_engine.audit_records:
                    audit_records.append({
                        'audit_id': record.audit_id,
                        'classification': record.classification.value,
                        'standard': record.standard.value,
                        'requirement_id': record.requirement_id,
                        'status': record.status,
                        'evidence_hash': record.evidence_hash,
                        'assessed_by': record.assessed_by,
                        'assessment_date': record.assessment_date.isoformat(),
                        'remediation_required': record.remediation_required,
                        'next_assessment_due': record.next_assessment_due.isoformat(),
                        'chain_of_custody': record.chain_of_custody
                    })
                
                return {
                    'audit_records': audit_records,
                    'total_records': len(audit_records),
                    'classification_level': milspec_engine.classification_level.value
                }
                
            except Exception as e:
                return {
                    'error': f'Audit records retrieval error: {e}',
                    'audit_records': [],
                    'total_records': 0
                }

        # TOP SECRET Upgrade Planning Endpoints
        @self.app.get("/top-secret/assessment")
        async def get_top_secret_assessment():
            """Get comprehensive TOP SECRET readiness assessment"""
            try:
                ts_planner = get_ts_upgrade_planner()
                assessment = await ts_planner.assess_current_capabilities()
                return assessment
                
            except Exception as e:
                return {
                    'error': f'TOP SECRET assessment error: {e}',
                    'overall_compliance_percentage': 0,
                    'software_readiness_percentage': 0
                }

        @self.app.get("/top-secret/upgrade-roadmap")
        async def get_upgrade_roadmap():
            """Get TOP SECRET upgrade implementation roadmap"""
            try:
                ts_planner = get_ts_upgrade_planner()
                roadmap = await ts_planner.generate_upgrade_roadmap()
                return roadmap
                
            except Exception as e:
                return {
                    'error': f'Upgrade roadmap generation error: {e}',
                    'recommended_approach': [],
                    'critical_path': []
                }

        @self.app.get("/top-secret/current-strengths")
        async def get_current_strengths():
            """Get current system strengths for TOP SECRET upgrade"""
            try:
                ts_planner = get_ts_upgrade_planner()
                strengths = ts_planner.get_current_strengths()
                
                return {
                    'current_strengths': strengths,
                    'total_strengths': len(strengths),
                    'assessment_note': 'These capabilities provide foundation for TOP SECRET upgrade'
                }
                
            except Exception as e:
                return {
                    'error': f'Strengths assessment error: {e}',
                    'current_strengths': []
                }

        @self.app.get("/top-secret/quick-wins")
        async def get_quick_wins():
            """Get quick wins for immediate TOP SECRET preparation"""
            try:
                ts_planner = get_ts_upgrade_planner()
                quick_wins = ts_planner.get_quick_wins()
                
                return {
                    'quick_wins': quick_wins,
                    'total_actions': len(quick_wins),
                    'implementation_note': 'These actions can be implemented immediately to demonstrate TOP SECRET readiness'
                }
                
            except Exception as e:
                return {
                    'error': f'Quick wins assessment error: {e}',
                    'quick_wins': []
                }

        @self.app.post("/top-secret/simulate-upgrade")
        async def simulate_ts_upgrade(simulation_request: Dict[str, Any]):
            """SIMULATION ONLY - Plan TOP SECRET upgrade (NO ACTUAL CHANGES)"""
            try:
                simulation_type = simulation_request.get('simulation_type', 'assessment_only')
                
                ts_planner = get_ts_upgrade_planner()
                assessment = await ts_planner.assess_current_capabilities()
                roadmap = await ts_planner.generate_upgrade_roadmap()
                
                return {
                    'simulation_mode': True,
                    'warning': 'THIS IS SIMULATION ONLY - NO ACTUAL SYSTEM CHANGES',
                    'simulation_type': simulation_type,
                    'current_assessment': assessment,
                    'upgrade_roadmap': roadmap,
                    'next_steps': [
                        'Engage government sponsor',
                        'Secure funding ($2-5M+)',
                        'Begin personnel clearance process',
                        'Engage ICD 705 certified contractors'
                    ],
                    'note': 'Actual TOP SECRET implementation requires government sponsorship and specialized facilities'
                }
                
            except Exception as e:
                return {
                    'simulation_mode': True,
                    'error': f'Simulation error: {e}',
                    'warning': 'THIS WAS SIMULATION ONLY - NO SYSTEM CHANGES MADE'
                }


# Global server instance
server = MWRASPServer()
app = server.app


def run_server(host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
    """Run the MWRASP server"""
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )


if __name__ == "__main__":
    run_server(debug=True)
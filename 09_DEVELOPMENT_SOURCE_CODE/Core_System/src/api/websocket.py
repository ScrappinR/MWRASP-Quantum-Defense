from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import asyncio
import json
import time
from datetime import datetime

from ..core.quantum_detector import QuantumDetector, ThreatLevel
from ..core.temporal_fragmentation import TemporalFragmentation
from ..core.agent_system import AutonomousDefenseCoordinator


class WebSocketManager:
    def __init__(self):
        # Active WebSocket connections
        self.active_connections: Set[WebSocket] = set()
        self.connection_subscriptions: Dict[WebSocket, List[str]] = {}
        
        # System references (set by server)
        self.quantum_detector: QuantumDetector = None
        self.fragmentation_system: TemporalFragmentation = None
        self.agent_coordinator: AutonomousDefenseCoordinator = None
        
        # Real-time monitoring state
        self.monitoring_task = None
        self.last_threat_count = 0
        self.last_fragment_count = 0
        self.last_agent_status = {}
        
        # Message history for new connections
        self.recent_messages: List[Dict] = []
        self.max_history = 100
    
    def set_system_references(self, quantum_detector, fragmentation_system, agent_coordinator):
        """Set references to the core systems"""
        self.quantum_detector = quantum_detector
        self.fragmentation_system = fragmentation_system
        self.agent_coordinator = agent_coordinator
    
    async def connect(self, websocket: WebSocket):
        """Handle new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.connection_subscriptions[websocket] = ["threats", "agents", "fragments", "system"]
        
        # Send initial system state
        await self._send_initial_state(websocket)
        
        # Start monitoring if this is the first connection
        if len(self.active_connections) == 1 and not self.monitoring_task:
            self.monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    def disconnect(self, websocket: WebSocket):
        """Handle WebSocket disconnection"""
        self.active_connections.discard(websocket)
        self.connection_subscriptions.pop(websocket, None)
        
        # Stop monitoring if no active connections
        if not self.active_connections and self.monitoring_task:
            self.monitoring_task.cancel()
            self.monitoring_task = None
    
    async def _send_initial_state(self, websocket: WebSocket):
        """Send initial system state to new connection"""
        try:
            # Send welcome message
            welcome_msg = {
                "type": "connection",
                "event": "connected",
                "timestamp": time.time(),
                "message": "Connected to MWRASP Real-time Monitoring",
                "server_time": datetime.now().isoformat()
            }
            await websocket.send_text(json.dumps(welcome_msg))
            
            # Send recent message history
            for message in self.recent_messages[-10:]:  # Last 10 messages
                await websocket.send_text(json.dumps(message))
            
            # Send current system status
            await self._send_system_status(websocket)
            
        except Exception as e:
            print(f"Error sending initial state: {e}")
    
    async def _send_system_status(self, websocket: WebSocket = None):
        """Send current system status"""
        try:
            if not all([self.quantum_detector, self.fragmentation_system, self.agent_coordinator]):
                return
            
            status_msg = {
                "type": "system",
                "event": "status_update",
                "timestamp": time.time(),
                "data": {
                    "quantum_detector": self.quantum_detector.get_threat_statistics(),
                    "temporal_fragmentation": self.fragmentation_system.get_system_stats(),
                    "agent_coordination": self.agent_coordinator.get_agent_status()
                }
            }
            
            if websocket:
                await websocket.send_text(json.dumps(status_msg))
            else:
                await self.broadcast_message(status_msg)
                
        except Exception as e:
            print(f"Error sending system status: {e}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop for real-time updates"""
        while self.active_connections:
            try:
                await asyncio.sleep(0.5)  # 500ms update interval
                
                # Check for new threats
                await self._check_threat_updates()
                
                # Check for fragment changes
                await self._check_fragment_updates()
                
                # Check for agent status changes
                await self._check_agent_updates()
                
                # Send periodic heartbeat
                await self._send_heartbeat()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Monitoring loop error: {e}")
                await asyncio.sleep(1.0)
    
    async def _check_threat_updates(self):
        """Check for new quantum threats"""
        try:
            if not self.quantum_detector:
                return
            
            current_threats = self.quantum_detector.get_active_threats()
            current_count = len(current_threats)
            
            if current_count != self.last_threat_count:
                # New threats detected
                new_threats = current_threats[self.last_threat_count:]
                
                for threat in new_threats:
                    threat_msg = {
                        "type": "threats",
                        "event": "new_threat",
                        "timestamp": time.time(),
                        "data": {
                            "threat_id": threat.threat_id,
                            "threat_level": threat.threat_level.name,
                            "detection_time": threat.detection_time,
                            "attack_vector": threat.attack_vector,
                            "quantum_indicators": threat.quantum_indicators,
                            "confidence_score": threat.confidence_score,
                            "affected_tokens": threat.affected_tokens
                        }
                    }
                    await self.broadcast_message(threat_msg, subscription_filter="threats")
                
                self.last_threat_count = current_count
                
                # Send updated statistics
                stats_msg = {
                    "type": "threats",
                    "event": "statistics_update",
                    "timestamp": time.time(),
                    "data": self.quantum_detector.get_threat_statistics()
                }
                await self.broadcast_message(stats_msg, subscription_filter="threats")
                
        except Exception as e:
            print(f"Error checking threat updates: {e}")
    
    async def _check_fragment_updates(self):
        """Check for fragment system changes"""
        try:
            if not self.fragmentation_system:
                return
            
            current_stats = self.fragmentation_system.get_system_stats()
            current_count = current_stats.get('total_fragments', 0)
            
            if current_count != self.last_fragment_count:
                fragment_msg = {
                    "type": "fragments",
                    "event": "fragment_update",
                    "timestamp": time.time(),
                    "data": {
                        "total_fragments": current_count,
                        "active_fragments": current_stats.get('active_fragments', 0),
                        "fragment_groups": current_stats.get('fragment_groups', 0),
                        "change": current_count - self.last_fragment_count
                    }
                }
                await self.broadcast_message(fragment_msg, subscription_filter="fragments")
                
                self.last_fragment_count = current_count
                
        except Exception as e:
            print(f"Error checking fragment updates: {e}")
    
    async def _check_agent_updates(self):
        """Check for agent status changes"""
        try:
            if not self.agent_coordinator:
                return
            
            current_status = self.agent_coordinator.get_agent_status()
            
            # Check for significant changes in agent states
            current_active = current_status.get('coordination_stats', {}).get('active_agents', 0)
            last_active = self.last_agent_status.get('coordination_stats', {}).get('active_agents', 0)
            
            if current_active != last_active:
                agent_msg = {
                    "type": "agents",
                    "event": "status_change",
                    "timestamp": time.time(),
                    "data": {
                        "active_agents": current_active,
                        "total_agents": current_status.get('total_agents', 0),
                        "recent_actions": current_status.get('recent_actions', 0),
                        "system_running": current_status.get('system_running', False)
                    }
                }
                await self.broadcast_message(agent_msg, subscription_filter="agents")
            
            # Check for new coordinated actions
            current_coordinations = current_status.get('coordination_stats', {}).get('total_coordinations', 0)
            last_coordinations = self.last_agent_status.get('coordination_stats', {}).get('total_coordinations', 0)
            
            if current_coordinations > last_coordinations:
                coordination_msg = {
                    "type": "agents",
                    "event": "coordination_executed",
                    "timestamp": time.time(),
                    "data": {
                        "total_coordinations": current_coordinations,
                        "successful_defenses": current_status.get('coordination_stats', {}).get('successful_defenses', 0),
                        "average_response_time": current_status.get('coordination_stats', {}).get('average_response_time', 0)
                    }
                }
                await self.broadcast_message(coordination_msg, subscription_filter="agents")
            
            self.last_agent_status = current_status
            
        except Exception as e:
            print(f"Error checking agent updates: {e}")
    
    async def _send_heartbeat(self):
        """Send periodic heartbeat to maintain connection"""
        heartbeat_msg = {
            "type": "system",
            "event": "heartbeat",
            "timestamp": time.time(),
            "server_time": datetime.now().isoformat(),
            "connections": len(self.active_connections)
        }
        await self.broadcast_message(heartbeat_msg, subscription_filter="system")
    
    async def broadcast_message(self, message: Dict, subscription_filter: str = None):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        
        # Add to message history
        self.recent_messages.append(message)
        if len(self.recent_messages) > self.max_history:
            self.recent_messages.pop(0)
        
        # Send to all appropriate connections
        disconnected = set()
        
        for websocket in self.active_connections:
            try:
                # Check subscription filter
                if subscription_filter:
                    subscriptions = self.connection_subscriptions.get(websocket, [])
                    if subscription_filter not in subscriptions:
                        continue
                
                await websocket.send_text(message_json)
                
            except WebSocketDisconnect:
                disconnected.add(websocket)
            except Exception as e:
                print(f"Error broadcasting to websocket: {e}")
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def send_alert(self, alert_type: str, message: str, severity: str = "info"):
        """Send immediate alert to all connected clients"""
        alert_msg = {
            "type": "alert",
            "event": "system_alert",
            "timestamp": time.time(),
            "data": {
                "alert_type": alert_type,
                "message": message,
                "severity": severity,
                "server_time": datetime.now().isoformat()
            }
        }
        await self.broadcast_message(alert_msg)
    
    async def handle_client_message(self, websocket: WebSocket, message: Dict):
        """Handle incoming messages from WebSocket clients"""
        try:
            message_type = message.get("type")
            
            if message_type == "subscribe":
                # Update subscriptions
                subscriptions = message.get("subscriptions", [])
                self.connection_subscriptions[websocket] = subscriptions
                
                response = {
                    "type": "subscription",
                    "event": "updated",
                    "timestamp": time.time(),
                    "subscriptions": subscriptions
                }
                await websocket.send_text(json.dumps(response))
            
            elif message_type == "request_status":
                # Send current status
                await self._send_system_status(websocket)
            
            elif message_type == "simulate":
                # Handle simulation requests
                await self._handle_simulation_request(websocket, message)
            
            elif message_type == "command":
                # Handle system commands
                await self._handle_command_request(websocket, message)
            
        except Exception as e:
            error_msg = {
                "type": "error",
                "event": "message_processing_error",
                "timestamp": time.time(),
                "error": str(e)
            }
            await websocket.send_text(json.dumps(error_msg))
    
    async def _handle_simulation_request(self, websocket: WebSocket, message: Dict):
        """Handle simulation requests from clients"""
        simulation_type = message.get("simulation")
        
        if simulation_type == "quantum_attack":
            # Trigger quantum attack simulation
            intensity = message.get("intensity", 3)
            
            # Create tokens and simulate access
            if self.quantum_detector:
                for i in range(intensity):
                    token = self.quantum_detector.generate_canary_token(f"sim_data_{i}")
                    await asyncio.sleep(0.001)  # Small delay
                    self.quantum_detector.access_token(token.token_id, f"simulator_{i}")
            
            response = {
                "type": "simulation",
                "event": "quantum_attack_simulated",
                "timestamp": time.time(),
                "data": {"intensity": intensity}
            }
            await websocket.send_text(json.dumps(response))
        
        elif simulation_type == "fragment_test":
            # Test fragmentation system
            test_data = f"Test data {time.time()}".encode()
            
            if self.fragmentation_system:
                fragments = self.fragmentation_system.fragment_data(test_data, "websocket_test")
                
                response = {
                    "type": "simulation",
                    "event": "fragmentation_tested",
                    "timestamp": time.time(),
                    "data": {
                        "fragments_created": len(fragments),
                        "test_id": "websocket_test"
                    }
                }
                await websocket.send_text(json.dumps(response))
    
    async def _handle_command_request(self, websocket: WebSocket, message: Dict):
        """Handle system command requests"""
        command = message.get("command")
        
        if command == "trigger_coordination":
            if self.agent_coordinator:
                coord_message = {
                    "type": "threat_escalation",
                    "threat_id": f"websocket_trigger_{int(time.time())}",
                    "level": 7,
                    "source": "websocket_command"
                }
                await self.agent_coordinator.send_coordination_message(coord_message)
            
            response = {
                "type": "command",
                "event": "coordination_triggered",
                "timestamp": time.time(),
                "command": command
            }
            await websocket.send_text(json.dumps(response))
    
    def get_connection_stats(self) -> Dict:
        """Get WebSocket connection statistics"""
        return {
            "active_connections": len(self.active_connections),
            "monitoring_active": self.monitoring_task is not None,
            "message_history_size": len(self.recent_messages),
            "subscription_breakdown": {
                sub: sum(1 for subs in self.connection_subscriptions.values() if sub in subs)
                for sub in ["threats", "agents", "fragments", "system"]
            }
        }


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
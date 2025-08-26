"""
MWRASP Compartmentalized Intelligence Operations with Network Topology
Advanced compartmentalized intelligence operations with mathematical network topology,
information flow control, and operational cell management for national security.
"""

import asyncio
import time
import json
import logging
import hashlib
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict, deque
import networkx as nx
import math
from scipy import sparse
from scipy.optimize import minimize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccessLevel(Enum):
    """Information access levels with mathematical priorities."""
    OPEN_SOURCE = 1
    INTERNAL_USE = 2
    CONFIDENTIAL = 3
    SECRET = 4
    TOP_SECRET = 5
    SCI = 6  # Sensitive Compartmented Information
    SAP = 7  # Special Access Program
    QUANTUM_EYES_ONLY = 8


class InformationType(Enum):
    """Types of intelligence information."""
    SIGNALS_INTELLIGENCE = "SIGINT"
    HUMAN_INTELLIGENCE = "HUMINT"
    GEOSPATIAL_INTELLIGENCE = "GEOINT"
    MEASUREMENT_SIGNATURE_INTELLIGENCE = "MASINT"
    OPEN_SOURCE_INTELLIGENCE = "OSINT"
    TECHNICAL_INTELLIGENCE = "TECHINT"
    CYBER_INTELLIGENCE = "CYBINT"
    QUANTUM_INTELLIGENCE = "QUANTINT"


class OperationalRole(Enum):
    """Operational roles with specific access patterns."""
    COLLECTION_MANAGER = "COLLECTION_MANAGER"
    ANALYST = "ANALYST"
    CASE_OFFICER = "CASE_OFFICER"
    TECHNICAL_OPERATOR = "TECHNICAL_OPERATOR"
    SURVEILLANCE_SPECIALIST = "SURVEILLANCE_SPECIALIST"
    COMMUNICATIONS_SPECIALIST = "COMMUNICATIONS_SPECIALIST"
    QUANTUM_SPECIALIST = "QUANTUM_SPECIALIST"
    FUSION_ANALYST = "FUSION_ANALYST"
    TARGETING_OFFICER = "TARGETING_OFFICER"
    OPERATIONAL_PLANNER = "OPERATIONAL_PLANNER"


@dataclass
class InformationPacket:
    """Individual piece of compartmentalized intelligence."""
    packet_id: str
    information_type: InformationType
    access_level: AccessLevel
    compartments: Set[str]
    source_reliability: float  # 0-1 reliability score
    information_value: float   # 0-1 intelligence value
    time_sensitivity: float    # 0-1 time criticality
    verification_status: str   # "UNVERIFIED", "PARTIAL", "VERIFIED", "CONFIRMED"
    creation_timestamp: datetime
    expiration_timestamp: Optional[datetime]
    content_hash: str
    source_chain: List[str]
    distribution_list: Set[str]
    access_log: List[Tuple[str, datetime]]
    
    def calculate_information_weight(self) -> float:
        """Calculate mathematical weight of information packet."""
        base_weight = self.information_value * self.source_reliability
        
        # Time sensitivity multiplier
        if self.time_sensitivity > 0.8:
            time_multiplier = 1.5
        elif self.time_sensitivity > 0.5:
            time_multiplier = 1.2
        else:
            time_multiplier = 1.0
        
        # Access level multiplier (higher classification = higher weight)
        access_multiplier = self.access_level.value / 8.0
        
        # Verification status multiplier
        verification_multipliers = {
            "UNVERIFIED": 0.5,
            "PARTIAL": 0.7,
            "VERIFIED": 1.0,
            "CONFIRMED": 1.3
        }
        verification_multiplier = verification_multipliers.get(self.verification_status, 0.5)
        
        return base_weight * time_multiplier * access_multiplier * verification_multiplier
    
    def can_access(self, agent_clearance: AccessLevel, agent_compartments: Set[str]) -> bool:
        """Check if agent can access this information packet."""
        # Clearance level check
        if agent_clearance.value < self.access_level.value:
            return False
        
        # Compartment check (agent must have at least one required compartment)
        if self.compartments and not (agent_compartments & self.compartments):
            return False
        
        # Time-based access (expired information)
        if self.expiration_timestamp and datetime.now() > self.expiration_timestamp:
            return False
        
        return True


@dataclass
class OperationalCell:
    """Compartmentalized operational cell with network topology."""
    cell_id: str
    cell_type: str
    security_level: AccessLevel
    members: Set[str]
    information_requirements: Set[InformationType]
    operational_objectives: List[str]
    geographic_area: Tuple[float, float, float]  # lat, lon, radius_km
    
    # Network topology
    internal_network: nx.DiGraph
    external_connections: Dict[str, float]  # cell_id -> connection_strength
    information_flow_matrix: np.ndarray
    trust_matrix: np.ndarray
    
    # Operational parameters
    operational_tempo: float  # Activity level 0-1
    security_posture: float   # Security alertness 0-1
    effectiveness_metric: float  # Operational effectiveness 0-1
    compromise_risk: float    # Risk of compromise 0-1
    
    def __post_init__(self):
        self.member_roles: Dict[str, OperationalRole] = {}
        self.information_store: Dict[str, InformationPacket] = {}
        self.operation_history: deque = deque(maxlen=1000)
        self.communication_patterns: Dict[str, List[datetime]] = defaultdict(list)
        self._initialize_network_structures()
    
    def _initialize_network_structures(self) -> None:
        """Initialize internal network structures."""
        n_members = len(self.members)
        if n_members == 0:
            return
        
        # Initialize internal network
        self.internal_network = nx.DiGraph()
        for member in self.members:
            self.internal_network.add_node(member)
        
        # Create initial connections based on roles and hierarchy
        member_list = list(self.members)
        for i, member1 in enumerate(member_list):
            for j, member2 in enumerate(member_list):
                if i != j:
                    # Connection probability based on operational need
                    connection_prob = 0.3 + 0.4 * np.random.random()
                    if np.random.random() < connection_prob:
                        weight = np.random.uniform(0.3, 0.9)
                        self.internal_network.add_edge(member1, member2, weight=weight)
        
        # Initialize matrices
        self.information_flow_matrix = np.random.random((n_members, n_members)) * 0.5
        self.trust_matrix = np.random.uniform(0.4, 0.9, (n_members, n_members))
        np.fill_diagonal(self.trust_matrix, 1.0)  # Perfect self-trust
    
    def add_member(self, agent_id: str, role: OperationalRole) -> None:
        """Add member to operational cell."""
        self.members.add(agent_id)
        self.member_roles[agent_id] = role
        
        # Update network structures
        self.internal_network.add_node(agent_id)
        
        # Connect to existing members based on role compatibility
        for existing_member in self.members:
            if existing_member != agent_id:
                connection_strength = self._calculate_role_compatibility(role, self.member_roles.get(existing_member))
                if connection_strength > 0.4:
                    self.internal_network.add_edge(agent_id, existing_member, weight=connection_strength)
                    self.internal_network.add_edge(existing_member, agent_id, weight=connection_strength * 0.8)
        
        # Resize matrices
        self._resize_matrices()
    
    def _calculate_role_compatibility(self, role1: OperationalRole, role2: Optional[OperationalRole]) -> float:
        """Calculate compatibility between operational roles."""
        if not role2:
            return 0.5
        
        # Define role compatibility matrix
        compatibility_matrix = {
            OperationalRole.COLLECTION_MANAGER: {
                OperationalRole.ANALYST: 0.9,
                OperationalRole.CASE_OFFICER: 0.8,
                OperationalRole.TECHNICAL_OPERATOR: 0.7,
                OperationalRole.SURVEILLANCE_SPECIALIST: 0.6
            },
            OperationalRole.ANALYST: {
                OperationalRole.FUSION_ANALYST: 0.9,
                OperationalRole.TARGETING_OFFICER: 0.8,
                OperationalRole.QUANTUM_SPECIALIST: 0.7
            },
            OperationalRole.CASE_OFFICER: {
                OperationalRole.SURVEILLANCE_SPECIALIST: 0.8,
                OperationalRole.COMMUNICATIONS_SPECIALIST: 0.7
            },
            OperationalRole.TECHNICAL_OPERATOR: {
                OperationalRole.QUANTUM_SPECIALIST: 0.9,
                OperationalRole.COMMUNICATIONS_SPECIALIST: 0.8
            }
        }
        
        # Check both directions
        compatibility1 = compatibility_matrix.get(role1, {}).get(role2, 0.3)
        compatibility2 = compatibility_matrix.get(role2, {}).get(role1, 0.3)
        
        return max(compatibility1, compatibility2)
    
    def _resize_matrices(self) -> None:
        """Resize matrices when members are added/removed."""
        n_members = len(self.members)
        if n_members == 0:
            return
        
        # Resize information flow matrix
        old_size = self.information_flow_matrix.shape[0] if self.information_flow_matrix.size > 0 else 0
        if n_members != old_size:
            new_flow_matrix = np.random.random((n_members, n_members)) * 0.3
            
            # Copy existing values
            if old_size > 0:
                copy_size = min(old_size, n_members)
                new_flow_matrix[:copy_size, :copy_size] = self.information_flow_matrix[:copy_size, :copy_size]
            
            self.information_flow_matrix = new_flow_matrix
        
        # Resize trust matrix
        if n_members != old_size:
            new_trust_matrix = np.random.uniform(0.4, 0.9, (n_members, n_members))
            np.fill_diagonal(new_trust_matrix, 1.0)
            
            # Copy existing values
            if old_size > 0:
                copy_size = min(old_size, n_members)
                new_trust_matrix[:copy_size, :copy_size] = self.trust_matrix[:copy_size, :copy_size]
            
            self.trust_matrix = new_trust_matrix
    
    def store_information(self, packet: InformationPacket) -> bool:
        """Store information packet in cell if authorized."""
        # Check if cell has appropriate clearance and compartments
        cell_compartments = set([self.cell_id, self.cell_type])
        
        if (self.security_level.value >= packet.access_level.value and
            (not packet.compartments or (packet.compartments & cell_compartments))):
            
            self.information_store[packet.packet_id] = packet
            
            # Update information flow metrics
            self._update_information_metrics(packet)
            
            return True
        
        return False
    
    def _update_information_metrics(self, packet: InformationPacket) -> None:
        """Update cell information flow metrics."""
        information_weight = packet.calculate_information_weight()
        
        # Update operational tempo based on information criticality
        if packet.time_sensitivity > 0.8:
            self.operational_tempo = min(1.0, self.operational_tempo + 0.1)
        
        # Update effectiveness metric
        current_effectiveness = self.effectiveness_metric
        information_impact = information_weight * 0.1
        self.effectiveness_metric = min(1.0, current_effectiveness + information_impact)
        
        # Update security posture if classified information
        if packet.access_level.value >= AccessLevel.SECRET.value:
            security_increase = packet.access_level.value * 0.02
            self.security_posture = min(1.0, self.security_posture + security_increase)
    
    def request_information(self, requester_id: str, information_types: Set[InformationType],
                          urgency: float) -> List[InformationPacket]:
        """Process information request from cell member."""
        if requester_id not in self.members:
            return []
        
        requester_role = self.member_roles.get(requester_id)
        if not requester_role:
            return []
        
        # Filter available information based on request
        available_packets = []
        
        for packet in self.information_store.values():
            # Check information type match
            if packet.information_type in information_types:
                # Check access authorization
                requester_clearance = self._get_member_clearance(requester_id)
                requester_compartments = self._get_member_compartments(requester_id)
                
                if packet.can_access(requester_clearance, requester_compartments):
                    available_packets.append(packet)
        
        # Sort by relevance and urgency
        sorted_packets = sorted(available_packets, 
                               key=lambda p: p.calculate_information_weight() * (1 + urgency),
                               reverse=True)
        
        # Log access
        access_time = datetime.now()
        for packet in sorted_packets:
            packet.access_log.append((requester_id, access_time))
        
        return sorted_packets[:10]  # Return top 10 most relevant
    
    def _get_member_clearance(self, member_id: str) -> AccessLevel:
        """Get member's clearance level (simplified)."""
        role = self.member_roles.get(member_id)
        
        # Map roles to typical clearance levels
        role_clearances = {
            OperationalRole.COLLECTION_MANAGER: AccessLevel.TOP_SECRET,
            OperationalRole.ANALYST: AccessLevel.SECRET,
            OperationalRole.CASE_OFFICER: AccessLevel.TOP_SECRET,
            OperationalRole.TECHNICAL_OPERATOR: AccessLevel.SECRET,
            OperationalRole.QUANTUM_SPECIALIST: AccessLevel.SCI,
            OperationalRole.FUSION_ANALYST: AccessLevel.TOP_SECRET,
            OperationalRole.TARGETING_OFFICER: AccessLevel.SCI
        }
        
        return role_clearances.get(role, AccessLevel.CONFIDENTIAL)
    
    def _get_member_compartments(self, member_id: str) -> Set[str]:
        """Get member's compartment access."""
        role = self.member_roles.get(member_id)
        base_compartments = {self.cell_id, self.cell_type}
        
        # Add role-specific compartments
        role_compartments = {
            OperationalRole.QUANTUM_SPECIALIST: {"QUANTUM_OPS", "QUANTUM_TECH"},
            OperationalRole.TECHNICAL_OPERATOR: {"TECH_OPS", "SIGNALS"},
            OperationalRole.CASE_OFFICER: {"HUMINT", "FIELD_OPS"},
            OperationalRole.ANALYST: {"ANALYSIS", "ASSESSMENT"}
        }
        
        additional_compartments = role_compartments.get(role, set())
        return base_compartments | additional_compartments
    
    def calculate_network_efficiency(self) -> Dict[str, float]:
        """Calculate network topology efficiency metrics."""
        if len(self.members) < 2:
            return {"efficiency": 0.0, "centrality": 0.0, "clustering": 0.0}
        
        try:
            # Network density
            density = nx.density(self.internal_network)
            
            # Average path length efficiency
            if nx.is_connected(self.internal_network.to_undirected()):
                avg_path_length = nx.average_shortest_path_length(self.internal_network.to_undirected())
                path_efficiency = 1.0 / avg_path_length if avg_path_length > 0 else 0.0
            else:
                path_efficiency = 0.0
            
            # Clustering coefficient
            clustering = nx.average_clustering(self.internal_network.to_undirected())
            
            # Centrality measures
            betweenness_centrality = nx.betweenness_centrality(self.internal_network)
            avg_centrality = np.mean(list(betweenness_centrality.values()))
            
            # Overall efficiency
            overall_efficiency = (0.3 * density + 0.3 * path_efficiency + 
                                0.2 * clustering + 0.2 * avg_centrality)
            
            return {
                "efficiency": overall_efficiency,
                "density": density,
                "path_efficiency": path_efficiency,
                "clustering": clustering,
                "centrality": avg_centrality
            }
        
        except Exception as e:
            logger.warning(f"Error calculating network efficiency: {e}")
            return {"efficiency": 0.0, "centrality": 0.0, "clustering": 0.0}
    
    def optimize_information_flow(self) -> None:
        """Optimize information flow within the cell."""
        if len(self.members) < 2:
            return
        
        # Current information flow efficiency
        current_metrics = self.calculate_network_efficiency()
        current_efficiency = current_metrics["efficiency"]
        
        # Attempt to improve network structure
        member_list = list(self.members)
        n_members = len(member_list)
        
        # Try adding connections to improve flow
        for i in range(n_members):
            for j in range(i+1, n_members):
                member1, member2 = member_list[i], member_list[j]
                
                if not self.internal_network.has_edge(member1, member2):
                    # Calculate potential improvement
                    role1 = self.member_roles.get(member1)
                    role2 = self.member_roles.get(member2)
                    compatibility = self._calculate_role_compatibility(role1, role2)
                    
                    if compatibility > 0.6:  # High compatibility threshold
                        # Add bidirectional edges
                        weight = compatibility * np.random.uniform(0.7, 0.9)
                        self.internal_network.add_edge(member1, member2, weight=weight)
                        self.internal_network.add_edge(member2, member1, weight=weight * 0.8)
        
        # Update information flow matrix based on new network
        self._update_flow_matrix_from_network()
        
        # Calculate new efficiency
        new_metrics = self.calculate_network_efficiency()
        improvement = new_metrics["efficiency"] - current_efficiency
        
        if improvement > 0.05:  # Significant improvement
            logger.info(f"Cell {self.cell_id} network efficiency improved by {improvement:.3f}")


class CompartmentalizationEngine:
    """Engine for managing compartmentalized intelligence operations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        
        # Operational cells
        self.operational_cells: Dict[str, OperationalCell] = {}
        self.inter_cell_network = nx.DiGraph()
        
        # Information management
        self.global_information_registry: Dict[str, InformationPacket] = {}
        self.compartment_registry: Dict[str, Set[str]] = defaultdict(set)  # compartment -> cells
        
        # Access control
        self.access_control_matrix = sparse.lil_matrix((0, 0))
        self.clearance_hierarchy = self._initialize_clearance_hierarchy()
        
        # Analytics and metrics
        self.operation_metrics = {
            'total_cells': 0,
            'total_information_packets': 0,
            'information_flow_rate': 0.0,
            'compartmentalization_effectiveness': 0.8,
            'security_violations': 0,
            'operational_efficiency': 0.75
        }
        
        # Network optimization
        self.network_optimizer = NetworkOptimizer()
        
        logger.info("MWRASP Compartmentalized Intelligence Operations initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for compartmentalized operations."""
        return {
            'max_cells_per_compartment': 5,
            'max_members_per_cell': 8,
            'information_retention_days': 90,
            'automatic_optimization': True,
            'security_monitoring': True,
            'inter_cell_communication': True,
            'compartment_isolation_level': 0.8,
            'access_logging': True,
            'network_analysis_enabled': True,
            'adaptive_compartmentalization': True
        }
    
    def _initialize_clearance_hierarchy(self) -> Dict[AccessLevel, Set[AccessLevel]]:
        """Initialize clearance level hierarchy for access control."""
        hierarchy = {}
        
        for level in AccessLevel:
            # Each level can access itself and all lower levels
            accessible_levels = {l for l in AccessLevel if l.value <= level.value}
            hierarchy[level] = accessible_levels
        
        return hierarchy
    
    def create_operational_cell(self, cell_id: str, cell_type: str, 
                              security_level: AccessLevel,
                              geographic_area: Tuple[float, float, float],
                              initial_members: Optional[List[Tuple[str, OperationalRole]]] = None) -> str:
        """Create new operational cell."""
        if cell_id in self.operational_cells:
            raise ValueError(f"Cell {cell_id} already exists")
        
        # Create cell
        cell = OperationalCell(
            cell_id=cell_id,
            cell_type=cell_type,
            security_level=security_level,
            members=set(),
            information_requirements=set(),
            operational_objectives=[],
            geographic_area=geographic_area,
            internal_network=nx.DiGraph(),
            external_connections={},
            information_flow_matrix=np.array([]),
            trust_matrix=np.array([]),
            operational_tempo=0.5,
            security_posture=0.7,
            effectiveness_metric=0.6,
            compromise_risk=0.2
        )
        
        # Add initial members
        if initial_members:
            for agent_id, role in initial_members:
                cell.add_member(agent_id, role)
        
        # Register cell
        self.operational_cells[cell_id] = cell
        self.inter_cell_network.add_node(cell_id, cell_type=cell_type, security_level=security_level.value)
        
        # Update compartment registry
        self.compartment_registry[cell_type].add(cell_id)
        
        # Update metrics
        self.operation_metrics['total_cells'] = len(self.operational_cells)
        
        logger.info(f"Created operational cell {cell_id} with security level {security_level.name}")
        return cell_id
    
    def establish_inter_cell_connection(self, source_cell_id: str, target_cell_id: str,
                                      connection_type: str, strength: float) -> bool:
        """Establish connection between operational cells."""
        if (source_cell_id not in self.operational_cells or 
            target_cell_id not in self.operational_cells):
            return False
        
        source_cell = self.operational_cells[source_cell_id]
        target_cell = self.operational_cells[target_cell_id]
        
        # Security level compatibility check
        if abs(source_cell.security_level.value - target_cell.security_level.value) > 2:
            logger.warning(f"Security level mismatch between cells {source_cell_id} and {target_cell_id}")
            strength *= 0.5  # Reduce connection strength
        
        # Add connection to inter-cell network
        self.inter_cell_network.add_edge(
            source_cell_id, target_cell_id, 
            connection_type=connection_type, 
            strength=strength,
            established_time=datetime.now()
        )
        
        # Update cell external connections
        source_cell.external_connections[target_cell_id] = strength
        target_cell.external_connections[source_cell_id] = strength * 0.8  # Asymmetric
        
        return True
    
    def distribute_information(self, packet: InformationPacket, 
                             target_cells: Optional[List[str]] = None) -> Dict[str, bool]:
        """Distribute information packet to appropriate cells."""
        distribution_results = {}
        
        # Determine target cells if not specified
        if target_cells is None:
            target_cells = self._identify_target_cells(packet)
        
        # Distribute to each target cell
        for cell_id in target_cells:
            if cell_id in self.operational_cells:
                cell = self.operational_cells[cell_id]
                success = cell.store_information(packet)
                distribution_results[cell_id] = success
                
                if success:
                    # Update packet distribution list
                    packet.distribution_list.add(cell_id)
            else:
                distribution_results[cell_id] = False
        
        # Register in global registry
        self.global_information_registry[packet.packet_id] = packet
        self.operation_metrics['total_information_packets'] = len(self.global_information_registry)
        
        return distribution_results
    
    def _identify_target_cells(self, packet: InformationPacket) -> List[str]:
        """Identify appropriate target cells for information distribution."""
        target_cells = []
        
        for cell_id, cell in self.operational_cells.items():
            # Check security level compatibility
            if cell.security_level.value < packet.access_level.value:
                continue
            
            # Check compartment compatibility
            cell_compartments = {cell.cell_id, cell.cell_type}
            if packet.compartments and not (packet.compartments & cell_compartments):
                continue
            
            # Check information type requirements
            if packet.information_type in cell.information_requirements:
                target_cells.append(cell_id)
            
            # Check operational relevance
            elif self._calculate_information_relevance(packet, cell) > 0.6:
                target_cells.append(cell_id)
        
        return target_cells
    
    def _calculate_information_relevance(self, packet: InformationPacket, cell: OperationalCell) -> float:
        """Calculate relevance score of information to operational cell."""
        relevance_score = 0.0
        
        # Geographic relevance
        if hasattr(packet, 'geographic_coordinates'):
            cell_lat, cell_lon, cell_radius = cell.geographic_area
            # packet_distance = calculate_distance(packet.geographic_coordinates, (cell_lat, cell_lon))
            # geographic_relevance = max(0, 1 - (packet_distance / cell_radius))
            geographic_relevance = 0.5  # Simplified for now
            relevance_score += 0.3 * geographic_relevance
        
        # Temporal relevance
        time_diff = (datetime.now() - packet.creation_timestamp).total_seconds()
        temporal_relevance = max(0, 1 - (time_diff / (24 * 3600)))  # Decay over 24 hours
        relevance_score += 0.2 * temporal_relevance
        
        # Information value relevance
        relevance_score += 0.3 * packet.information_value
        
        # Cell operational tempo relevance
        relevance_score += 0.2 * cell.operational_tempo
        
        return min(1.0, relevance_score)
    
    def request_inter_cell_information(self, requesting_cell_id: str, 
                                     target_cell_id: str,
                                     information_types: Set[InformationType],
                                     justification: str) -> List[InformationPacket]:
        """Request information sharing between cells."""
        if (requesting_cell_id not in self.operational_cells or
            target_cell_id not in self.operational_cells):
            return []
        
        requesting_cell = self.operational_cells[requesting_cell_id]
        target_cell = self.operational_cells[target_cell_id]
        
        # Check if inter-cell connection exists
        if not self.inter_cell_network.has_edge(requesting_cell_id, target_cell_id):
            # No direct connection - check for indirect path
            try:
                path = nx.shortest_path(self.inter_cell_network, requesting_cell_id, target_cell_id)
                if len(path) > 3:  # Too many hops
                    return []
            except nx.NetworkXNoPath:
                return []
        
        # Authorization check
        connection_strength = requesting_cell.external_connections.get(target_cell_id, 0.0)
        if connection_strength < 0.3:  # Minimum connection strength required
            return []
        
        # Security level compatibility
        if requesting_cell.security_level.value > target_cell.security_level.value:
            return []  # Cannot request from lower security level
        
        # Process request
        shared_packets = []
        for packet in target_cell.information_store.values():
            if (packet.information_type in information_types and
                packet.can_access(requesting_cell.security_level, {requesting_cell_id, requesting_cell.cell_type})):
                
                # Create shared copy with restricted distribution
                shared_packet = InformationPacket(
                    packet_id=f"{packet.packet_id}_SHARED_{requesting_cell_id}",
                    information_type=packet.information_type,
                    access_level=max(packet.access_level, requesting_cell.security_level),
                    compartments=packet.compartments | {requesting_cell_id},
                    source_reliability=packet.source_reliability * 0.9,  # Slight degradation
                    information_value=packet.information_value,
                    time_sensitivity=packet.time_sensitivity,
                    verification_status=packet.verification_status,
                    creation_timestamp=packet.creation_timestamp,
                    expiration_timestamp=packet.expiration_timestamp,
                    content_hash=packet.content_hash,
                    source_chain=packet.source_chain + [target_cell_id],
                    distribution_list={requesting_cell_id},
                    access_log=[(requesting_cell_id, datetime.now())]
                )
                
                shared_packets.append(shared_packet)
        
        # Log inter-cell information sharing
        sharing_log = {
            'timestamp': datetime.now(),
            'requesting_cell': requesting_cell_id,
            'target_cell': target_cell_id,
            'information_types': [it.value for it in information_types],
            'packets_shared': len(shared_packets),
            'justification': justification
        }
        
        return shared_packets
    
    def analyze_compartmentalization_effectiveness(self) -> Dict[str, Any]:
        """Analyze effectiveness of compartmentalization strategy."""
        analysis = {
            'overall_effectiveness': 0.0,
            'information_isolation': 0.0,
            'operational_efficiency': 0.0,
            'security_score': 0.0,
            'network_metrics': {},
            'cell_performance': {},
            'recommendations': []
        }
        
        if not self.operational_cells:
            return analysis
        
        # Information isolation analysis
        total_packets = len(self.global_information_registry)
        if total_packets > 0:
            # Calculate how well information is compartmentalized
            compartment_distribution = defaultdict(int)
            for packet in self.global_information_registry.values():
                compartment_key = tuple(sorted(packet.compartments)) if packet.compartments else ("NONE",)
                compartment_distribution[compartment_key] += 1
            
            # Information entropy (higher = better compartmentalization)
            if len(compartment_distribution) > 1:
                compartment_probs = [count / total_packets for count in compartment_distribution.values()]
                information_entropy = -sum(p * math.log2(p) for p in compartment_probs if p > 0)
                max_entropy = math.log2(len(compartment_distribution))
                analysis['information_isolation'] = information_entropy / max_entropy if max_entropy > 0 else 0.0
            else:
                analysis['information_isolation'] = 0.0
        
        # Operational efficiency analysis
        cell_efficiencies = []
        for cell_id, cell in self.operational_cells.items():
            network_metrics = cell.calculate_network_efficiency()
            cell_efficiency = (cell.effectiveness_metric * 0.4 +
                             network_metrics['efficiency'] * 0.3 +
                             cell.operational_tempo * 0.2 +
                             (1 - cell.compromise_risk) * 0.1)
            
            cell_efficiencies.append(cell_efficiency)
            analysis['cell_performance'][cell_id] = {
                'efficiency': cell_efficiency,
                'effectiveness': cell.effectiveness_metric,
                'network_metrics': network_metrics,
                'compromise_risk': cell.compromise_risk
            }
        
        analysis['operational_efficiency'] = np.mean(cell_efficiencies) if cell_efficiencies else 0.0
        
        # Inter-cell network analysis
        if len(self.inter_cell_network.nodes()) > 1:
            try:
                # Network connectivity
                connectivity = nx.average_node_connectivity(self.inter_cell_network.to_undirected())
                
                # Network density
                density = nx.density(self.inter_cell_network)
                
                # Clustering
                clustering = nx.average_clustering(self.inter_cell_network.to_undirected())
                
                analysis['network_metrics'] = {
                    'connectivity': connectivity,
                    'density': density,
                    'clustering': clustering,
                    'total_connections': len(self.inter_cell_network.edges())
                }
            except Exception as e:
                logger.warning(f"Error calculating inter-cell network metrics: {e}")
        
        # Security score calculation
        security_violations = self.operation_metrics.get('security_violations', 0)
        total_operations = max(1, total_packets)
        security_score = max(0.0, 1.0 - (security_violations / total_operations))
        analysis['security_score'] = security_score
        
        # Overall effectiveness
        analysis['overall_effectiveness'] = (
            0.3 * analysis['information_isolation'] +
            0.4 * analysis['operational_efficiency'] +
            0.3 * security_score
        )
        
        # Generate recommendations
        recommendations = []
        
        if analysis['information_isolation'] < 0.6:
            recommendations.append("Improve information compartmentalization by creating more specialized cells")
        
        if analysis['operational_efficiency'] < 0.7:
            recommendations.append("Optimize cell network structures to improve operational efficiency")
        
        if analysis['security_score'] < 0.8:
            recommendations.append("Review and strengthen access control policies")
        
        if analysis['network_metrics'].get('connectivity', 0) < 0.5:
            recommendations.append("Establish additional inter-cell connections for better information flow")
        
        analysis['recommendations'] = recommendations
        
        # Update system metrics
        self.operation_metrics['compartmentalization_effectiveness'] = analysis['overall_effectiveness']
        self.operation_metrics['operational_efficiency'] = analysis['operational_efficiency']
        
        return analysis
    
    def optimize_network_topology(self) -> Dict[str, Any]:
        """Optimize inter-cell network topology for better performance."""
        if len(self.operational_cells) < 2:
            return {'status': 'insufficient_cells'}
        
        optimization_result = self.network_optimizer.optimize_topology(
            self.operational_cells,
            self.inter_cell_network,
            self.operation_metrics
        )
        
        # Apply optimization recommendations
        if optimization_result.get('new_connections'):
            for source_cell, target_cell, strength in optimization_result['new_connections']:
                self.establish_inter_cell_connection(source_cell, target_cell, 'OPTIMIZED', strength)
        
        # Update cell structures based on optimization
        if optimization_result.get('cell_optimizations'):
            for cell_id, optimizations in optimization_result['cell_optimizations'].items():
                if cell_id in self.operational_cells:
                    self.operational_cells[cell_id].optimize_information_flow()
        
        return optimization_result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        # Calculate current performance metrics
        analysis = self.analyze_compartmentalization_effectiveness()
        
        return {
            'system_status': 'OPERATIONAL',
            'operational_cells': len(self.operational_cells),
            'total_information_packets': len(self.global_information_registry),
            'inter_cell_connections': len(self.inter_cell_network.edges()),
            'compartments_active': len(self.compartment_registry),
            'performance_metrics': {
                'compartmentalization_effectiveness': analysis['overall_effectiveness'],
                'information_isolation': analysis['information_isolation'],
                'operational_efficiency': analysis['operational_efficiency'],
                'security_score': analysis['security_score']
            },
            'network_metrics': analysis['network_metrics'],
            'system_metrics': self.operation_metrics,
            'configuration': self.config
        }


class NetworkOptimizer:
    """Network topology optimizer for compartmentalized operations."""
    
    def __init__(self):
        self.optimization_history = deque(maxlen=100)
    
    def optimize_topology(self, cells: Dict[str, OperationalCell], 
                         inter_cell_network: nx.DiGraph,
                         current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize network topology using mathematical optimization."""
        if len(cells) < 2:
            return {'status': 'insufficient_nodes'}
        
        # Current network analysis
        current_efficiency = self._calculate_network_efficiency(inter_cell_network)
        
        # Optimization objectives
        objectives = {
            'maximize_information_flow': 0.4,
            'minimize_security_risk': 0.3,
            'optimize_redundancy': 0.2,
            'balance_load': 0.1
        }
        
        # Generate optimization recommendations
        new_connections = self._suggest_new_connections(cells, inter_cell_network)
        cell_optimizations = self._suggest_cell_optimizations(cells)
        
        # Calculate expected improvement
        expected_improvement = self._estimate_improvement(new_connections, current_efficiency)
        
        optimization_result = {
            'current_efficiency': current_efficiency,
            'expected_improvement': expected_improvement,
            'new_connections': new_connections,
            'cell_optimizations': cell_optimizations,
            'optimization_objectives': objectives,
            'timestamp': datetime.now()
        }
        
        self.optimization_history.append(optimization_result)
        return optimization_result
    
    def _calculate_network_efficiency(self, network: nx.DiGraph) -> float:
        """Calculate current network efficiency."""
        if len(network.nodes()) < 2:
            return 0.0
        
        try:
            # Convert to undirected for efficiency calculations
            undirected = network.to_undirected()
            
            # Global efficiency
            if nx.is_connected(undirected):
                avg_path_length = nx.average_shortest_path_length(undirected)
                global_efficiency = 1.0 / avg_path_length if avg_path_length > 0 else 0.0
            else:
                global_efficiency = 0.0
            
            # Local efficiency (clustering)
            local_efficiency = nx.average_clustering(undirected)
            
            # Combined efficiency
            return 0.6 * global_efficiency + 0.4 * local_efficiency
            
        except Exception as e:
            logger.warning(f"Error calculating network efficiency: {e}")
            return 0.0
    
    def _suggest_new_connections(self, cells: Dict[str, OperationalCell], 
                               network: nx.DiGraph) -> List[Tuple[str, str, float]]:
        """Suggest new inter-cell connections."""
        suggestions = []
        
        cell_ids = list(cells.keys())
        for i, cell1_id in enumerate(cell_ids):
            for cell2_id in cell_ids[i+1:]:
                if not network.has_edge(cell1_id, cell2_id):
                    # Calculate connection value
                    cell1 = cells[cell1_id]
                    cell2 = cells[cell2_id]
                    
                    # Security compatibility
                    security_diff = abs(cell1.security_level.value - cell2.security_level.value)
                    security_compatibility = max(0.0, 1.0 - (security_diff / 8.0))
                    
                    # Operational synergy
                    type_synergy = 0.8 if cell1.cell_type == cell2.cell_type else 0.6
                    
                    # Geographic proximity (simplified)
                    # geographic_proximity = 0.7  # Would calculate actual distance
                    
                    # Information flow potential
                    info_flow_potential = (cell1.operational_tempo + cell2.operational_tempo) / 2.0
                    
                    # Overall connection strength
                    connection_strength = (0.3 * security_compatibility +
                                         0.3 * type_synergy +
                                         0.2 * info_flow_potential +
                                         0.2 * 0.7)  # geographic_proximity placeholder
                    
                    if connection_strength > 0.5:  # Threshold for recommendation
                        suggestions.append((cell1_id, cell2_id, connection_strength))
        
        # Sort by connection strength
        suggestions.sort(key=lambda x: x[2], reverse=True)
        return suggestions[:5]  # Return top 5 suggestions
    
    def _suggest_cell_optimizations(self, cells: Dict[str, OperationalCell]) -> Dict[str, List[str]]:
        """Suggest optimizations for individual cells."""
        optimizations = {}
        
        for cell_id, cell in cells.items():
            cell_suggestions = []
            
            # Network efficiency check
            if len(cell.members) > 1:
                network_metrics = cell.calculate_network_efficiency()
                if network_metrics['efficiency'] < 0.6:
                    cell_suggestions.append("optimize_internal_network")
                
                if network_metrics['clustering'] < 0.3:
                    cell_suggestions.append("increase_member_connectivity")
            
            # Operational tempo check
            if cell.operational_tempo < 0.4:
                cell_suggestions.append("increase_operational_activity")
            elif cell.operational_tempo > 0.9:
                cell_suggestions.append("balance_operational_load")
            
            # Security posture check
            if cell.compromise_risk > 0.6:
                cell_suggestions.append("enhance_security_measures")
            
            # Information flow check
            if len(cell.information_store) > 100:  # Too much information
                cell_suggestions.append("optimize_information_management")
            
            if cell_suggestions:
                optimizations[cell_id] = cell_suggestions
        
        return optimizations
    
    def _estimate_improvement(self, new_connections: List[Tuple[str, str, float]], 
                            current_efficiency: float) -> float:
        """Estimate expected improvement from optimizations."""
        if not new_connections:
            return 0.0
        
        # Simple improvement estimation based on connection strengths
        avg_new_connection_strength = np.mean([strength for _, _, strength in new_connections])
        estimated_improvement = avg_new_connection_strength * 0.1  # Conservative estimate
        
        return min(0.5, estimated_improvement)  # Cap at 50% improvement


async def main():
    """Main demonstration of compartmentalized intelligence operations."""
    engine = CompartmentalizationEngine()
    
    print("MWRASP Compartmentalized Intelligence Operations")
    print("=" * 55)
    
    # Create operational cells
    cells_config = [
        ("QUANTUM_ANALYSIS_CELL", "QUANTUM_OPERATIONS", AccessLevel.SCI, (38.9072, -77.0369, 50.0)),
        ("TECHNICAL_OPS_CELL", "TECHNICAL_OPERATIONS", AccessLevel.TOP_SECRET, (37.4419, -122.1430, 30.0)),
        ("SIGNALS_INTEL_CELL", "SIGNALS_INTELLIGENCE", AccessLevel.SECRET, (40.7128, -74.0060, 25.0)),
        ("COUNTER_INTEL_CELL", "COUNTER_INTELLIGENCE", AccessLevel.SAP, (42.3601, -71.0589, 20.0)),
        ("FIELD_OPS_CELL", "FIELD_OPERATIONS", AccessLevel.TOP_SECRET, (41.8781, -87.6298, 40.0))
    ]
    
    print("Creating Operational Cells:")
    for cell_id, cell_type, security_level, geo_area in cells_config:
        # Create cell with initial members
        initial_members = [
            (f"{cell_id}_LEAD", OperationalRole.COLLECTION_MANAGER),
            (f"{cell_id}_ANALYST_01", OperationalRole.ANALYST),
            (f"{cell_id}_TECH", OperationalRole.TECHNICAL_OPERATOR)
        ]
        
        engine.create_operational_cell(cell_id, cell_type, security_level, geo_area, initial_members)
        print(f"  ✓ {cell_id}: {security_level.name} ({len(initial_members)} members)")
    
    # Establish inter-cell connections
    print("\nEstablishing Inter-Cell Connections:")
    connections = [
        ("QUANTUM_ANALYSIS_CELL", "TECHNICAL_OPS_CELL", "TECHNICAL_COLLABORATION", 0.8),
        ("TECHNICAL_OPS_CELL", "SIGNALS_INTEL_CELL", "OPERATIONAL_SUPPORT", 0.7),
        ("COUNTER_INTEL_CELL", "FIELD_OPS_CELL", "SECURITY_COORDINATION", 0.9),
        ("QUANTUM_ANALYSIS_CELL", "COUNTER_INTEL_CELL", "THREAT_ASSESSMENT", 0.6)
    ]
    
    for source, target, conn_type, strength in connections:
        success = engine.establish_inter_cell_connection(source, target, conn_type, strength)
        status = "✓" if success else "✗"
        print(f"  {status} {source} -> {target}: {conn_type} ({strength:.1f})")
    
    # Create and distribute information packets
    print("\nDistributing Intelligence Packets:")
    sample_packets = [
        InformationPacket(
            packet_id="QTHREAT_001",
            information_type=InformationType.QUANTUM_INTELLIGENCE,
            access_level=AccessLevel.SCI,
            compartments={"QUANTUM_OPERATIONS"},
            source_reliability=0.9,
            information_value=0.8,
            time_sensitivity=0.9,
            verification_status="CONFIRMED",
            creation_timestamp=datetime.now(),
            expiration_timestamp=datetime.now() + timedelta(hours=24),
            content_hash="qthreat_001_hash",
            source_chain=["QUANTUM_SENSOR_ALPHA"],
            distribution_list=set(),
            access_log=[]
        ),
        InformationPacket(
            packet_id="SIGINT_002",
            information_type=InformationType.SIGNALS_INTELLIGENCE,
            access_level=AccessLevel.SECRET,
            compartments={"SIGNALS_INTELLIGENCE"},
            source_reliability=0.7,
            information_value=0.6,
            time_sensitivity=0.5,
            verification_status="VERIFIED",
            creation_timestamp=datetime.now(),
            expiration_timestamp=datetime.now() + timedelta(hours=48),
            content_hash="sigint_002_hash",
            source_chain=["SIGNALS_COLLECTION_BRAVO"],
            distribution_list=set(),
            access_log=[]
        ),
        InformationPacket(
            packet_id="TECHINT_003",
            information_type=InformationType.TECHNICAL_INTELLIGENCE,
            access_level=AccessLevel.TOP_SECRET,
            compartments={"TECHNICAL_OPERATIONS"},
            source_reliability=0.8,
            information_value=0.9,
            time_sensitivity=0.7,
            verification_status="VERIFIED",
            creation_timestamp=datetime.now(),
            expiration_timestamp=datetime.now() + timedelta(hours=12),
            content_hash="techint_003_hash",
            source_chain=["TECHNICAL_COLLECTION_CHARLIE"],
            distribution_list=set(),
            access_log=[]
        )
    ]
    
    for packet in sample_packets:
        distribution_results = engine.distribute_information(packet)
        successful_distributions = sum(1 for success in distribution_results.values() if success)
        print(f"  {packet.packet_id}: Distributed to {successful_distributions}/{len(distribution_results)} cells")
    
    # Demonstrate inter-cell information request
    print("\nInter-Cell Information Sharing:")
    shared_packets = engine.request_inter_cell_information(
        "TECHNICAL_OPS_CELL",
        "QUANTUM_ANALYSIS_CELL",
        {InformationType.QUANTUM_INTELLIGENCE},
        "Technical analysis of quantum threat indicators"
    )
    print(f"  TECHNICAL_OPS_CELL <- QUANTUM_ANALYSIS_CELL: {len(shared_packets)} packets shared")
    
    # System status and analysis
    print("\nSystem Status:")
    status = engine.get_system_status()
    print(f"  Operational Status: {status['system_status']}")
    print(f"  Active Cells: {status['operational_cells']}")
    print(f"  Information Packets: {status['total_information_packets']}")
    print(f"  Inter-Cell Connections: {status['inter_cell_connections']}")
    
    print("\nPerformance Metrics:")
    metrics = status['performance_metrics']
    print(f"  Compartmentalization Effectiveness: {metrics['compartmentalization_effectiveness']:.3f}")
    print(f"  Information Isolation: {metrics['information_isolation']:.3f}")
    print(f"  Operational Efficiency: {metrics['operational_efficiency']:.3f}")
    print(f"  Security Score: {metrics['security_score']:.3f}")
    
    # Network optimization
    print("\nNetwork Optimization:")
    optimization = engine.optimize_network_topology()
    if optimization.get('new_connections'):
        print(f"  Optimization Suggestions: {len(optimization['new_connections'])} new connections recommended")
        for source, target, strength in optimization['new_connections'][:3]:
            print(f"    • {source} <-> {target} (strength: {strength:.3f})")
    
    print(f"  Expected Improvement: {optimization.get('expected_improvement', 0):.1%}")
    
    # Cell performance analysis
    print("\nCell Performance Summary:")
    for cell_id, cell_perf in status['performance_metrics'].get('cell_performance', {}).items():
        if isinstance(cell_perf, dict):
            print(f"  {cell_id}:")
            print(f"    Efficiency: {cell_perf.get('efficiency', 0):.3f}")
            print(f"    Compromise Risk: {cell_perf.get('compromise_risk', 0):.3f}")


if __name__ == "__main__":
    asyncio.run(main())
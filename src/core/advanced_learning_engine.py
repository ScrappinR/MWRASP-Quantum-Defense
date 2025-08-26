#!/usr/bin/env python3
"""
Advanced Learning Engine for Autonomous Agents
Implements deep learning, memory systems, and knowledge sharing
"""

import asyncio
import time
import json
import uuid
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum

class LearningType(Enum):
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    META = "meta_learning"
    COLLABORATIVE = "collaborative"

class MemoryType(Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    COLLECTIVE = "collective"

@dataclass
class Memory:
    memory_id: str
    agent_id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    timestamp: float
    importance: float
    access_count: int = 0
    decay_rate: float = 0.01
    confidence: float = 1.0
    associations: List[str] = field(default_factory=list)
    
    def access(self):
        """Access memory, updating access count and reinforcing it"""
        self.access_count += 1
        self.confidence = min(1.0, self.confidence + 0.01)
        self.importance = min(1.0, self.importance + 0.005)
    
    def decay(self, time_passed: float):
        """Natural memory decay over time"""
        decay_amount = self.decay_rate * time_passed
        self.confidence = max(0.0, self.confidence - decay_amount)
        if self.memory_type != MemoryType.LONG_TERM:
            self.importance = max(0.0, self.importance - decay_amount * 0.5)

@dataclass
class KnowledgePattern:
    pattern_id: str
    pattern_type: str
    trigger_conditions: Dict[str, Any]
    expected_outcomes: Dict[str, Any]
    success_rate: float
    confidence: float
    learned_from: List[str]  # Agent IDs that contributed
    creation_time: float
    last_used: float
    usage_count: int = 0
    
    def update_effectiveness(self, success: bool, outcome_score: float):
        """Update pattern effectiveness based on usage results"""
        self.usage_count += 1
        self.last_used = time.time()
        
        if success:
            self.success_rate = (self.success_rate * (self.usage_count - 1) + 1.0) / self.usage_count
            self.confidence = min(1.0, self.confidence + outcome_score * 0.1)
        else:
            self.success_rate = (self.success_rate * (self.usage_count - 1)) / self.usage_count
            self.confidence = max(0.1, self.confidence - 0.05)

@dataclass
class LearningSession:
    session_id: str
    agent_id: str
    learning_type: LearningType
    start_time: float
    end_time: Optional[float] = None
    experiences_processed: int = 0
    patterns_discovered: int = 0
    knowledge_gained: float = 0.0
    collaborators: List[str] = field(default_factory=list)
    success_rate: float = 0.0

class AdvancedLearningEngine:
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.knowledge_patterns: Dict[str, KnowledgePattern] = {}
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.agent_knowledge_graphs: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.collective_intelligence: Dict[str, Any] = {}
        
        # Learning parameters
        self.memory_capacity = 10000
        self.pattern_discovery_threshold = 0.7
        self.knowledge_transfer_threshold = 0.8
        self.collaboration_bonus = 0.2
        
        # Advanced learning metrics
        self.learning_metrics = {
            'total_memories': 0,
            'active_patterns': 0,
            'knowledge_transfer_events': 0,
            'collaborative_sessions': 0,
            'innovation_discoveries': 0,
            'meta_learning_cycles': 0
        }
        
        self._initialize_base_knowledge()
    
    def _initialize_base_knowledge(self):
        """Initialize foundational knowledge patterns"""
        base_patterns = [
            {
                'pattern_type': 'threat_response',
                'trigger_conditions': {'threat_level': 'HIGH', 'confidence': '>0.8'},
                'expected_outcomes': {'isolation_success': 0.9, 'response_time': '<100ms'},
                'description': 'High confidence high-level threats require immediate isolation'
            },
            {
                'pattern_type': 'quantum_signature',
                'trigger_conditions': {'quantum_indicators': '>3', 'entanglement_detected': True},
                'expected_outcomes': {'quantum_analysis_required': True, 'specialized_response': True},
                'description': 'Quantum signatures require specialized analysis protocols'
            },
            {
                'pattern_type': 'collaborative_advantage',
                'trigger_conditions': {'complexity_score': '>0.7', 'agent_count': '>1'},
                'expected_outcomes': {'success_improvement': 0.3, 'resource_efficiency': 0.2},
                'description': 'Complex threats benefit from multi-agent collaboration'
            }
        ]
        
        for pattern_data in base_patterns:
            pattern = KnowledgePattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=pattern_data['pattern_type'],
                trigger_conditions=pattern_data['trigger_conditions'],
                expected_outcomes=pattern_data['expected_outcomes'],
                success_rate=0.8,  # Base success rate for foundational patterns
                confidence=0.9,
                learned_from=['system_initialization'],
                creation_time=time.time(),
                last_used=time.time()
            )
            self.knowledge_patterns[pattern.pattern_id] = pattern
    
    async def start_learning_session(self, agent_id: str, learning_type: LearningType, 
                                   collaborators: List[str] = None) -> str:
        """Start a new learning session for an agent"""
        session_id = str(uuid.uuid4())
        session = LearningSession(
            session_id=session_id,
            agent_id=agent_id,
            learning_type=learning_type,
            start_time=time.time(),
            collaborators=collaborators or []
        )
        
        self.learning_sessions[session_id] = session
        
        if collaborators:
            self.learning_metrics['collaborative_sessions'] += 1
        
        return session_id
    
    async def end_learning_session(self, session_id: str) -> Dict[str, Any]:
        """End a learning session and summarize results"""
        session = self.learning_sessions.get(session_id)
        if not session:
            return {}
        
        session.end_time = time.time()
        session_duration = session.end_time - session.start_time
        
        # Calculate learning effectiveness
        learning_rate = session.experiences_processed / max(session_duration, 1.0)
        discovery_rate = session.patterns_discovered / max(session.experiences_processed, 1)
        
        results = {
            'session_id': session_id,
            'duration': session_duration,
            'experiences_processed': session.experiences_processed,
            'patterns_discovered': session.patterns_discovered,
            'knowledge_gained': session.knowledge_gained,
            'learning_rate': learning_rate,
            'discovery_rate': discovery_rate,
            'success_rate': session.success_rate,
            'collaboration_bonus': len(session.collaborators) * self.collaboration_bonus
        }
        
        return results
    
    async def store_memory(self, agent_id: str, memory_type: MemoryType, 
                          content: Dict[str, Any], importance: float = 0.5) -> str:
        """Store a memory with advanced categorization and indexing"""
        # Check memory capacity and remove old memories if needed
        await self._manage_memory_capacity()
        
        memory_id = str(uuid.uuid4())
        memory = Memory(
            memory_id=memory_id,
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            timestamp=time.time(),
            importance=importance
        )
        
        # Add associations based on content similarity
        await self._create_memory_associations(memory)
        
        self.memories[memory_id] = memory
        self.learning_metrics['total_memories'] += 1
        
        # Update agent's knowledge graph
        await self._update_knowledge_graph(agent_id, memory)
        
        return memory_id
    
    async def retrieve_memory(self, agent_id: str, query: Dict[str, Any], 
                            memory_types: List[MemoryType] = None, 
                            limit: int = 10) -> List[Memory]:
        """Retrieve memories using advanced search and ranking"""
        relevant_memories = []
        
        for memory in self.memories.values():
            if memory.agent_id != agent_id:
                continue
            
            if memory_types and memory.memory_type not in memory_types:
                continue
            
            # Calculate relevance score
            relevance_score = await self._calculate_memory_relevance(memory, query)
            
            if relevance_score > 0.3:  # Relevance threshold
                memory.access()  # Update access statistics
                relevant_memories.append((memory, relevance_score))
        
        # Sort by relevance and return top results
        relevant_memories.sort(key=lambda x: x[1], reverse=True)
        return [mem[0] for mem in relevant_memories[:limit]]
    
    async def discover_patterns(self, agent_id: str, experiences: List[Dict[str, Any]]) -> List[str]:
        """Discover new knowledge patterns from experiences"""
        discovered_patterns = []
        
        if len(experiences) < 5:  # Need minimum experiences for pattern discovery
            return discovered_patterns
        
        # Group experiences by similarity
        experience_groups = await self._group_similar_experiences(experiences)
        
        for group in experience_groups:
            if len(group) >= 3:  # Minimum group size for pattern
                pattern = await self._extract_pattern_from_group(group, agent_id)
                if pattern:
                    pattern_id = str(uuid.uuid4())
                    self.knowledge_patterns[pattern_id] = pattern
                    discovered_patterns.append(pattern_id)
                    
                    self.learning_metrics['active_patterns'] += 1
                    
                    # Update learning session if active
                    active_session = self._get_active_learning_session(agent_id)
                    if active_session:
                        active_session.patterns_discovered += 1
        
        return discovered_patterns
    
    async def transfer_knowledge(self, source_agent: str, target_agent: str, 
                               knowledge_types: List[str] = None) -> Dict[str, Any]:
        """Transfer knowledge between agents"""
        transfer_results = {
            'memories_transferred': 0,
            'patterns_transferred': 0,
            'knowledge_score': 0.0,
            'compatibility_score': 0.0
        }
        
        # Calculate agent compatibility for knowledge transfer
        compatibility = await self._calculate_agent_compatibility(source_agent, target_agent)
        transfer_results['compatibility_score'] = compatibility
        
        if compatibility < 0.5:
            return transfer_results
        
        # Transfer high-value memories
        source_memories = [m for m in self.memories.values() 
                          if m.agent_id == source_agent and m.importance > 0.7]
        
        for memory in source_memories:
            if knowledge_types and not any(kt in str(memory.content) for kt in knowledge_types):
                continue
            
            # Create transferred memory for target agent
            transferred_memory = Memory(
                memory_id=str(uuid.uuid4()),
                agent_id=target_agent,
                memory_type=MemoryType.TRANSFER,
                content={**memory.content, 'transferred_from': source_agent},
                timestamp=time.time(),
                importance=memory.importance * compatibility,
                confidence=memory.confidence * 0.8  # Slight confidence reduction in transfer
            )
            
            self.memories[transferred_memory.memory_id] = transferred_memory
            transfer_results['memories_transferred'] += 1
        
        # Transfer applicable patterns
        applicable_patterns = [p for p in self.knowledge_patterns.values()
                             if source_agent in p.learned_from and p.success_rate > self.knowledge_transfer_threshold]
        
        for pattern in applicable_patterns:
            if target_agent not in pattern.learned_from:
                pattern.learned_from.append(target_agent)
                transfer_results['patterns_transferred'] += 1
        
        transfer_results['knowledge_score'] = (transfer_results['memories_transferred'] * 0.3 + 
                                             transfer_results['patterns_transferred'] * 0.7)
        
        self.learning_metrics['knowledge_transfer_events'] += 1
        
        return transfer_results
    
    async def collaborative_learning(self, agent_ids: List[str], problem_context: Dict[str, Any]) -> Dict[str, Any]:
        """Facilitate collaborative learning between multiple agents"""
        session_id = await self.start_learning_session(
            agent_ids[0], 
            LearningType.COLLABORATIVE, 
            agent_ids[1:]
        )
        
        collaboration_results = {
            'session_id': session_id,
            'participating_agents': agent_ids,
            'shared_insights': [],
            'new_patterns': [],
            'collective_knowledge_gain': 0.0
        }
        
        # Gather relevant memories from all agents
        all_memories = []
        for agent_id in agent_ids:
            agent_memories = await self.retrieve_memory(agent_id, problem_context, limit=20)
            all_memories.extend(agent_memories)
        
        # Find commonalities and differences
        common_patterns = await self._find_common_patterns(all_memories)
        unique_insights = await self._find_unique_insights(all_memories, agent_ids)
        
        # Generate collaborative insights
        for pattern in common_patterns:
            insight = {
                'type': 'common_pattern',
                'pattern': pattern,
                'confidence': pattern.get('confidence', 0.5),
                'contributing_agents': pattern.get('contributors', agent_ids)
            }
            collaboration_results['shared_insights'].append(insight)
        
        for insight in unique_insights:
            collaboration_results['shared_insights'].append(insight)
        
        # Create new collaborative knowledge patterns
        if len(collaboration_results['shared_insights']) >= 2:
            new_pattern = await self._synthesize_collaborative_pattern(
                collaboration_results['shared_insights'], 
                agent_ids,
                problem_context
            )
            
            if new_pattern:
                pattern_id = str(uuid.uuid4())
                self.knowledge_patterns[pattern_id] = new_pattern
                collaboration_results['new_patterns'].append(pattern_id)
                
                # Store in collective intelligence
                await self._update_collective_intelligence(new_pattern, agent_ids)
        
        # Calculate collective knowledge gain
        collaboration_results['collective_knowledge_gain'] = (
            len(collaboration_results['shared_insights']) * 0.1 +
            len(collaboration_results['new_patterns']) * 0.5 +
            len(agent_ids) * self.collaboration_bonus
        )
        
        await self.end_learning_session(session_id)
        
        return collaboration_results
    
    async def meta_learning_cycle(self, agent_id: str) -> Dict[str, Any]:
        """Perform meta-learning to improve learning algorithms themselves"""
        meta_results = {
            'learning_efficiency_improvement': 0.0,
            'pattern_quality_improvement': 0.0,
            'memory_organization_improvement': 0.0,
            'adapted_parameters': {}
        }
        
        # Analyze agent's learning history
        agent_memories = [m for m in self.memories.values() if m.agent_id == agent_id]
        agent_patterns = [p for p in self.knowledge_patterns.values() if agent_id in p.learned_from]
        
        if len(agent_memories) < 50 or len(agent_patterns) < 5:
            return meta_results  # Not enough data for meta-learning
        
        # Analyze memory effectiveness
        memory_analysis = await self._analyze_memory_effectiveness(agent_memories)
        if memory_analysis['optimization_needed']:
            await self._optimize_memory_organization(agent_id, memory_analysis)
            meta_results['memory_organization_improvement'] = 0.2
        
        # Analyze pattern quality and success rates
        pattern_analysis = await self._analyze_pattern_effectiveness(agent_patterns)
        if pattern_analysis['improvement_potential'] > 0.3:
            await self._refine_pattern_extraction(agent_id, pattern_analysis)
            meta_results['pattern_quality_improvement'] = pattern_analysis['improvement_potential']
        
        # Adapt learning parameters based on performance
        performance_metrics = await self._calculate_learning_performance(agent_id)
        if performance_metrics['adaptation_needed']:
            new_parameters = await self._adapt_learning_parameters(agent_id, performance_metrics)
            meta_results['adapted_parameters'] = new_parameters
            meta_results['learning_efficiency_improvement'] = new_parameters.get('efficiency_gain', 0.0)
        
        self.learning_metrics['meta_learning_cycles'] += 1
        
        return meta_results
    
    async def _manage_memory_capacity(self):
        """Manage memory capacity by removing least important old memories"""
        if len(self.memories) <= self.memory_capacity:
            return
        
        # Apply decay to all memories
        current_time = time.time()
        for memory in self.memories.values():
            time_passed = current_time - memory.timestamp
            memory.decay(time_passed)
        
        # Remove memories below threshold
        memories_to_remove = []
        for memory_id, memory in self.memories.items():
            if (memory.confidence < 0.1 and 
                memory.importance < 0.1 and 
                memory.memory_type != MemoryType.LONG_TERM):
                memories_to_remove.append(memory_id)
        
        for memory_id in memories_to_remove:
            del self.memories[memory_id]
        
        # If still over capacity, remove oldest low-importance memories
        if len(self.memories) > self.memory_capacity:
            sorted_memories = sorted(
                self.memories.items(),
                key=lambda x: (x[1].importance, x[1].timestamp)
            )
            
            excess_count = len(self.memories) - self.memory_capacity
            for i in range(excess_count):
                memory_id = sorted_memories[i][0]
                if sorted_memories[i][1].memory_type != MemoryType.LONG_TERM:
                    del self.memories[memory_id]
    
    async def _create_memory_associations(self, memory: Memory):
        """Create associations between related memories"""
        associations = []
        
        for existing_memory in self.memories.values():
            if existing_memory.agent_id == memory.agent_id:
                similarity = await self._calculate_content_similarity(
                    memory.content, 
                    existing_memory.content
                )
                
                if similarity > 0.6:
                    associations.append(existing_memory.memory_id)
        
        memory.associations = associations
    
    async def _calculate_content_similarity(self, content1: Dict[str, Any], content2: Dict[str, Any]) -> float:
        """Calculate similarity between memory contents"""
        # Simple keyword-based similarity
        content1_str = json.dumps(content1, default=str).lower()
        content2_str = json.dumps(content2, default=str).lower()
        
        content1_words = set(content1_str.split())
        content2_words = set(content2_str.split())
        
        if not content1_words or not content2_words:
            return 0.0
        
        intersection = content1_words & content2_words
        union = content1_words | content2_words
        
        return len(intersection) / len(union) if union else 0.0
    
    async def _update_knowledge_graph(self, agent_id: str, memory: Memory):
        """Update agent's knowledge graph with new memory"""
        if agent_id not in self.agent_knowledge_graphs:
            self.agent_knowledge_graphs[agent_id] = {
                'nodes': {},
                'edges': [],
                'centrality_scores': {}
            }
        
        graph = self.agent_knowledge_graphs[agent_id]
        
        # Add memory as a node
        graph['nodes'][memory.memory_id] = {
            'type': memory.memory_type.value,
            'importance': memory.importance,
            'timestamp': memory.timestamp,
            'content_summary': str(memory.content)[:100]
        }
        
        # Add edges to associated memories
        for associated_id in memory.associations:
            if associated_id in graph['nodes']:
                edge = {
                    'source': memory.memory_id,
                    'target': associated_id,
                    'weight': 0.5,
                    'type': 'association'
                }
                graph['edges'].append(edge)
    
    async def _calculate_memory_relevance(self, memory: Memory, query: Dict[str, Any]) -> float:
        """Calculate how relevant a memory is to a query"""
        relevance_score = 0.0
        
        # Content similarity
        content_similarity = await self._calculate_content_similarity(memory.content, query)
        relevance_score += content_similarity * 0.4
        
        # Recency bonus
        time_diff = time.time() - memory.timestamp
        recency_score = max(0.0, 1.0 - (time_diff / 86400))  # Decay over 24 hours
        relevance_score += recency_score * 0.2
        
        # Importance weight
        relevance_score += memory.importance * 0.3
        
        # Access frequency bonus
        access_bonus = min(0.1, memory.access_count * 0.01)
        relevance_score += access_bonus
        
        # Confidence factor
        relevance_score *= memory.confidence
        
        return min(1.0, relevance_score)
    
    async def _group_similar_experiences(self, experiences: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group similar experiences for pattern discovery"""
        groups = []
        used_indices = set()
        
        for i, exp1 in enumerate(experiences):
            if i in used_indices:
                continue
                
            group = [exp1]
            used_indices.add(i)
            
            for j, exp2 in enumerate(experiences[i+1:], i+1):
                if j in used_indices:
                    continue
                    
                similarity = await self._calculate_content_similarity(exp1, exp2)
                if similarity > 0.6:
                    group.append(exp2)
                    used_indices.add(j)
            
            if len(group) >= 2:  # Only keep groups with multiple experiences
                groups.append(group)
        
        return groups
    
    async def _extract_pattern_from_group(self, experience_group: List[Dict[str, Any]], agent_id: str) -> Optional[KnowledgePattern]:
        """Extract a knowledge pattern from a group of similar experiences"""
        if len(experience_group) < 3:
            return None
        
        # Analyze common elements
        common_triggers = {}
        common_outcomes = {}
        success_count = 0
        
        for experience in experience_group:
            if experience.get('success', False):
                success_count += 1
            
            # Extract trigger conditions
            for key, value in experience.items():
                if key.startswith('trigger_') or key in ['threat_level', 'confidence_score', 'quantum_indicators']:
                    if key not in common_triggers:
                        common_triggers[key] = []
                    common_triggers[key].append(value)
            
            # Extract outcomes
            for key, value in experience.items():
                if key.startswith('outcome_') or key in ['response_time', 'effectiveness', 'success']:
                    if key not in common_outcomes:
                        common_outcomes[key] = []
                    common_outcomes[key].append(value)
        
        success_rate = success_count / len(experience_group)
        
        if success_rate < 0.6:  # Don't create patterns from mostly failed experiences
            return None
        
        # Create pattern
        pattern = KnowledgePattern(
            pattern_id=str(uuid.uuid4()),
            pattern_type=f"discovered_{agent_id}_{int(time.time())}",
            trigger_conditions=self._generalize_conditions(common_triggers),
            expected_outcomes=self._generalize_outcomes(common_outcomes),
            success_rate=success_rate,
            confidence=min(1.0, success_rate + 0.1),
            learned_from=[agent_id],
            creation_time=time.time(),
            last_used=time.time()
        )
        
        return pattern
    
    def _generalize_conditions(self, common_triggers: Dict[str, List]) -> Dict[str, Any]:
        """Generalize trigger conditions from multiple experiences"""
        generalized = {}
        
        for key, values in common_triggers.items():
            if isinstance(values[0], (int, float)):
                # Numeric values - use range
                min_val = min(values)
                max_val = max(values)
                if min_val == max_val:
                    generalized[key] = min_val
                else:
                    generalized[key] = {'min': min_val, 'max': max_val}
            else:
                # Categorical values - use most common
                most_common = max(set(values), key=values.count)
                if values.count(most_common) / len(values) > 0.6:
                    generalized[key] = most_common
                else:
                    generalized[key] = {'options': list(set(values))}
        
        return generalized
    
    def _generalize_outcomes(self, common_outcomes: Dict[str, List]) -> Dict[str, Any]:
        """Generalize expected outcomes from multiple experiences"""
        generalized = {}
        
        for key, values in common_outcomes.items():
            if isinstance(values[0], (int, float)):
                # Numeric values - use average with confidence interval
                avg_val = sum(values) / len(values)
                generalized[key] = {'expected': avg_val, 'confidence': 0.8}
            elif isinstance(values[0], bool):
                # Boolean values - use probability
                true_count = sum(1 for v in values if v)
                generalized[key] = true_count / len(values)
            else:
                # Categorical - use most common
                most_common = max(set(values), key=values.count)
                generalized[key] = most_common
        
        return generalized
    
    async def _calculate_agent_compatibility(self, agent1: str, agent2: str) -> float:
        """Calculate compatibility between agents for knowledge transfer"""
        # Get memories for both agents
        agent1_memories = [m for m in self.memories.values() if m.agent_id == agent1]
        agent2_memories = [m for m in self.memories.values() if m.agent_id == agent2]
        
        if not agent1_memories or not agent2_memories:
            return 0.3  # Default low compatibility
        
        # Calculate domain overlap
        agent1_domains = set()
        agent2_domains = set()
        
        for memory in agent1_memories:
            agent1_domains.update(str(memory.content).split())
        
        for memory in agent2_memories:
            agent2_domains.update(str(memory.content).split())
        
        domain_overlap = len(agent1_domains & agent2_domains) / len(agent1_domains | agent2_domains)
        
        # Calculate success rate similarity
        agent1_success_patterns = [p for p in self.knowledge_patterns.values() 
                                 if agent1 in p.learned_from]
        agent2_success_patterns = [p for p in self.knowledge_patterns.values() 
                                 if agent2 in p.learned_from]
        
        if agent1_success_patterns and agent2_success_patterns:
            agent1_avg_success = sum(p.success_rate for p in agent1_success_patterns) / len(agent1_success_patterns)
            agent2_avg_success = sum(p.success_rate for p in agent2_success_patterns) / len(agent2_success_patterns)
            success_similarity = 1.0 - abs(agent1_avg_success - agent2_avg_success)
        else:
            success_similarity = 0.5
        
        # Combine factors
        compatibility = (domain_overlap * 0.6 + success_similarity * 0.4)
        
        return min(1.0, max(0.0, compatibility))
    
    def _get_active_learning_session(self, agent_id: str) -> Optional[LearningSession]:
        """Get active learning session for an agent"""
        for session in self.learning_sessions.values():
            if session.agent_id == agent_id and session.end_time is None:
                return session
        return None
    
    async def _find_common_patterns(self, memories: List[Memory]) -> List[Dict[str, Any]]:
        """Find common patterns across multiple agent memories"""
        common_patterns = []
        
        # Group memories by content similarity
        memory_groups = {}
        for memory in memories:
            content_key = self._extract_content_key(memory.content)
            if content_key not in memory_groups:
                memory_groups[content_key] = []
            memory_groups[content_key].append(memory)
        
        # Find groups with multiple contributors
        for content_key, group_memories in memory_groups.items():
            contributing_agents = set(m.agent_id for m in group_memories)
            if len(contributing_agents) >= 2:
                pattern = {
                    'content_key': content_key,
                    'contributors': list(contributing_agents),
                    'memory_count': len(group_memories),
                    'confidence': min(1.0, len(group_memories) * 0.1 + len(contributing_agents) * 0.2),
                    'pattern_type': 'common_experience'
                }
                common_patterns.append(pattern)
        
        return common_patterns
    
    def _extract_content_key(self, content: Dict[str, Any]) -> str:
        """Extract a key from memory content for grouping"""
        # Simple key extraction - could be made more sophisticated
        key_parts = []
        for key, value in content.items():
            if key in ['action_type', 'threat_level', 'outcome_type', 'success']:
                key_parts.append(f"{key}:{value}")
        
        return "|".join(sorted(key_parts))
    
    async def _find_unique_insights(self, memories: List[Memory], agent_ids: List[str]) -> List[Dict[str, Any]]:
        """Find unique insights that only some agents possess"""
        unique_insights = []
        
        agent_memory_map = defaultdict(list)
        for memory in memories:
            agent_memory_map[memory.agent_id].append(memory)
        
        # Find memories that are unique to specific agents
        for agent_id in agent_ids:
            agent_memories = agent_memory_map[agent_id]
            for memory in agent_memories:
                is_unique = True
                for other_agent_id in agent_ids:
                    if other_agent_id == agent_id:
                        continue
                    
                    for other_memory in agent_memory_map[other_agent_id]:
                        similarity = await self._calculate_content_similarity(
                            memory.content, other_memory.content
                        )
                        if similarity > 0.7:
                            is_unique = False
                            break
                    
                    if not is_unique:
                        break
                
                if is_unique and memory.importance > 0.6:
                    insight = {
                        'type': 'unique_insight',
                        'agent': agent_id,
                        'content': memory.content,
                        'importance': memory.importance,
                        'confidence': memory.confidence
                    }
                    unique_insights.append(insight)
        
        return unique_insights
    
    async def _synthesize_collaborative_pattern(self, insights: List[Dict[str, Any]], 
                                              agent_ids: List[str], 
                                              context: Dict[str, Any]) -> Optional[KnowledgePattern]:
        """Synthesize a new pattern from collaborative insights"""
        if len(insights) < 2:
            return None
        
        # Combine insights to create new pattern
        combined_conditions = {}
        combined_outcomes = {}
        
        for insight in insights:
            if insight['type'] == 'common_pattern':
                # Extract conditions from common patterns
                pattern = insight.get('pattern', {})
                for key, value in pattern.items():
                    if key.startswith('trigger_') or key in context:
                        combined_conditions[key] = value
            elif insight['type'] == 'unique_insight':
                # Extract unique outcomes
                content = insight.get('content', {})
                for key, value in content.items():
                    if key.startswith('outcome_') or key.endswith('_result'):
                        combined_outcomes[key] = value
        
        if not combined_conditions or not combined_outcomes:
            return None
        
        # Calculate collaborative success rate
        success_indicators = []
        for insight in insights:
            if 'confidence' in insight:
                success_indicators.append(insight['confidence'])
        
        collaborative_success_rate = sum(success_indicators) / len(success_indicators) if success_indicators else 0.7
        collaborative_success_rate += self.collaboration_bonus  # Bonus for collaboration
        
        pattern = KnowledgePattern(
            pattern_id=str(uuid.uuid4()),
            pattern_type="collaborative_synthesis",
            trigger_conditions=combined_conditions,
            expected_outcomes=combined_outcomes,
            success_rate=min(1.0, collaborative_success_rate),
            confidence=min(1.0, collaborative_success_rate + 0.1),
            learned_from=agent_ids,
            creation_time=time.time(),
            last_used=time.time()
        )
        
        return pattern
    
    async def _update_collective_intelligence(self, pattern: KnowledgePattern, contributing_agents: List[str]):
        """Update collective intelligence with new collaborative pattern"""
        pattern_type = pattern.pattern_type
        
        if pattern_type not in self.collective_intelligence:
            self.collective_intelligence[pattern_type] = {
                'patterns': [],
                'contributing_agents': set(),
                'success_rate': 0.0,
                'usage_count': 0,
                'creation_time': time.time()
            }
        
        collective_entry = self.collective_intelligence[pattern_type]
        collective_entry['patterns'].append(pattern.pattern_id)
        collective_entry['contributing_agents'].update(contributing_agents)
        collective_entry['success_rate'] = (
            (collective_entry['success_rate'] * collective_entry['usage_count'] + pattern.success_rate) /
            (collective_entry['usage_count'] + 1)
        )
        collective_entry['usage_count'] += 1
    
    async def _analyze_memory_effectiveness(self, memories: List[Memory]) -> Dict[str, Any]:
        """Analyze the effectiveness of memory organization for an agent"""
        if len(memories) < 20:
            return {'optimization_needed': False}
        
        analysis = {
            'total_memories': len(memories),
            'average_importance': sum(m.importance for m in memories) / len(memories),
            'average_confidence': sum(m.confidence for m in memories) / len(memories),
            'memory_distribution': defaultdict(int),
            'access_patterns': {},
            'optimization_needed': False
        }
        
        # Analyze memory type distribution
        for memory in memories:
            analysis['memory_distribution'][memory.memory_type.value] += 1
        
        # Analyze access patterns
        high_access_memories = [m for m in memories if m.access_count > 5]
        low_access_memories = [m for m in memories if m.access_count == 0]
        
        analysis['access_patterns'] = {
            'high_access_count': len(high_access_memories),
            'low_access_count': len(low_access_memories),
            'access_efficiency': len(high_access_memories) / len(memories)
        }
        
        # Determine if optimization is needed
        if (analysis['access_patterns']['access_efficiency'] < 0.3 or
            len(low_access_memories) > len(memories) * 0.6 or
            analysis['average_confidence'] < 0.5):
            analysis['optimization_needed'] = True
        
        return analysis
    
    async def _optimize_memory_organization(self, agent_id: str, analysis: Dict[str, Any]):
        """Optimize memory organization based on analysis"""
        agent_memories = [m for m in self.memories.values() if m.agent_id == agent_id]
        
        # Promote frequently accessed memories to long-term
        for memory in agent_memories:
            if (memory.access_count > 10 and 
                memory.importance > 0.7 and
                memory.memory_type != MemoryType.LONG_TERM):
                memory.memory_type = MemoryType.LONG_TERM
                memory.decay_rate *= 0.1  # Much slower decay
        
        # Consolidate similar memories
        await self._consolidate_similar_memories(agent_id)
        
        # Update memory associations
        for memory in agent_memories:
            await self._create_memory_associations(memory)
    
    async def _consolidate_similar_memories(self, agent_id: str):
        """Consolidate similar memories to reduce redundancy"""
        agent_memories = [m for m in self.memories.values() if m.agent_id == agent_id]
        
        memories_to_remove = []
        
        for i, memory1 in enumerate(agent_memories):
            if memory1.memory_id in memories_to_remove:
                continue
                
            similar_memories = []
            for j, memory2 in enumerate(agent_memories[i+1:], i+1):
                if memory2.memory_id in memories_to_remove:
                    continue
                
                similarity = await self._calculate_content_similarity(memory1.content, memory2.content)
                if similarity > 0.8:  # Very similar memories
                    similar_memories.append(memory2)
            
            if similar_memories:
                # Consolidate into the most important memory
                all_similar = [memory1] + similar_memories
                best_memory = max(all_similar, key=lambda m: m.importance * m.confidence)
                
                # Update best memory with combined information
                for similar in similar_memories:
                    best_memory.access_count += similar.access_count
                    best_memory.importance = max(best_memory.importance, similar.importance)
                    memories_to_remove.append(similar.memory_id)
        
        # Remove consolidated memories
        for memory_id in memories_to_remove:
            if memory_id in self.memories:
                del self.memories[memory_id]
    
    async def _analyze_pattern_effectiveness(self, patterns: List[KnowledgePattern]) -> Dict[str, Any]:
        """Analyze the effectiveness of discovered patterns"""
        if len(patterns) < 5:
            return {'improvement_potential': 0.0}
        
        analysis = {
            'total_patterns': len(patterns),
            'average_success_rate': sum(p.success_rate for p in patterns) / len(patterns),
            'average_confidence': sum(p.confidence for p in patterns) / len(patterns),
            'usage_distribution': {},
            'improvement_potential': 0.0
        }
        
        # Analyze usage patterns
        high_usage = [p for p in patterns if p.usage_count > 5]
        unused_patterns = [p for p in patterns if p.usage_count == 0]
        
        analysis['usage_distribution'] = {
            'high_usage': len(high_usage),
            'unused': len(unused_patterns),
            'usage_efficiency': len(high_usage) / len(patterns)
        }
        
        # Calculate improvement potential
        low_success_patterns = [p for p in patterns if p.success_rate < 0.6]
        improvement_potential = len(low_success_patterns) / len(patterns)
        
        if analysis['usage_distribution']['usage_efficiency'] < 0.4:
            improvement_potential += 0.2
        
        if analysis['average_confidence'] < 0.6:
            improvement_potential += 0.1
        
        analysis['improvement_potential'] = min(1.0, improvement_potential)
        
        return analysis
    
    async def _refine_pattern_extraction(self, agent_id: str, analysis: Dict[str, Any]):
        """Refine pattern extraction algorithms based on effectiveness analysis"""
        agent_patterns = [p for p in self.knowledge_patterns.values() if agent_id in p.learned_from]
        
        # Remove or modify low-performing patterns
        patterns_to_remove = []
        for pattern in agent_patterns:
            if pattern.success_rate < 0.4 and pattern.usage_count > 5:
                # Pattern is consistently unsuccessful
                patterns_to_remove.append(pattern.pattern_id)
            elif pattern.usage_count == 0 and time.time() - pattern.creation_time > 86400:
                # Unused pattern older than 1 day
                patterns_to_remove.append(pattern.pattern_id)
        
        for pattern_id in patterns_to_remove:
            if pattern_id in self.knowledge_patterns:
                del self.knowledge_patterns[pattern_id]
        
        # Enhance successful patterns
        successful_patterns = [p for p in agent_patterns if p.success_rate > 0.8 and p.usage_count > 3]
        for pattern in successful_patterns:
            # Increase confidence and reduce trigger thresholds for successful patterns
            pattern.confidence = min(1.0, pattern.confidence * 1.1)
            
            # Make trigger conditions slightly more general for successful patterns
            for key, condition in pattern.trigger_conditions.items():
                if isinstance(condition, dict) and 'min' in condition:
                    range_size = condition['max'] - condition['min']
                    pattern.trigger_conditions[key] = {
                        'min': condition['min'] - range_size * 0.1,
                        'max': condition['max'] + range_size * 0.1
                    }
    
    async def _calculate_learning_performance(self, agent_id: str) -> Dict[str, Any]:
        """Calculate overall learning performance for an agent"""
        agent_memories = [m for m in self.memories.values() if m.agent_id == agent_id]
        agent_patterns = [p for p in self.knowledge_patterns.values() if agent_id in p.learned_from]
        
        if not agent_memories:
            return {'adaptation_needed': False}
        
        performance = {
            'memory_retention': sum(m.confidence for m in agent_memories) / len(agent_memories),
            'pattern_success_rate': sum(p.success_rate for p in agent_patterns) / len(agent_patterns) if agent_patterns else 0.5,
            'learning_speed': 0.0,
            'knowledge_utilization': 0.0,
            'adaptation_needed': False
        }
        
        # Calculate learning speed (memories created per hour)
        recent_memories = [m for m in agent_memories if time.time() - m.timestamp < 3600]
        performance['learning_speed'] = len(recent_memories)
        
        # Calculate knowledge utilization (accessed memories / total memories)
        accessed_memories = [m for m in agent_memories if m.access_count > 0]
        performance['knowledge_utilization'] = len(accessed_memories) / len(agent_memories)
        
        # Determine if adaptation is needed
        if (performance['memory_retention'] < 0.6 or
            performance['pattern_success_rate'] < 0.7 or
            performance['knowledge_utilization'] < 0.4):
            performance['adaptation_needed'] = True
        
        return performance
    
    async def _adapt_learning_parameters(self, agent_id: str, performance: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt learning parameters based on performance analysis"""
        adapted_parameters = {
            'memory_importance_threshold': 0.5,
            'pattern_discovery_threshold': self.pattern_discovery_threshold,
            'learning_rate_modifier': 1.0,
            'efficiency_gain': 0.0
        }
        
        # Adapt based on memory retention
        if performance['memory_retention'] < 0.5:
            # Increase memory importance threshold to be more selective
            adapted_parameters['memory_importance_threshold'] = 0.7
            adapted_parameters['efficiency_gain'] += 0.1
        elif performance['memory_retention'] > 0.9:
            # Decrease threshold to capture more memories
            adapted_parameters['memory_importance_threshold'] = 0.3
        
        # Adapt based on pattern success rate
        if performance['pattern_success_rate'] < 0.6:
            # Raise pattern discovery threshold
            adapted_parameters['pattern_discovery_threshold'] = 0.8
            adapted_parameters['efficiency_gain'] += 0.15
        elif performance['pattern_success_rate'] > 0.9:
            # Lower threshold to discover more patterns
            adapted_parameters['pattern_discovery_threshold'] = 0.6
        
        # Adapt based on knowledge utilization
        if performance['knowledge_utilization'] < 0.3:
            # Increase learning rate to encourage more active learning
            adapted_parameters['learning_rate_modifier'] = 1.3
            adapted_parameters['efficiency_gain'] += 0.1
        
        return adapted_parameters
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning system statistics"""
        stats = self.learning_metrics.copy()
        
        # Add derived statistics
        total_agents = len(set(m.agent_id for m in self.memories.values()))
        stats['agents_with_memories'] = total_agents
        stats['avg_memories_per_agent'] = len(self.memories) / max(total_agents, 1)
        stats['avg_patterns_per_agent'] = len(self.knowledge_patterns) / max(total_agents, 1)
        
        # Memory type distribution
        memory_types = defaultdict(int)
        for memory in self.memories.values():
            memory_types[memory.memory_type.value] += 1
        stats['memory_type_distribution'] = dict(memory_types)
        
        # Pattern effectiveness
        if self.knowledge_patterns:
            pattern_success_rates = [p.success_rate for p in self.knowledge_patterns.values()]
            stats['average_pattern_success_rate'] = sum(pattern_success_rates) / len(pattern_success_rates)
            stats['top_pattern_success_rate'] = max(pattern_success_rates)
        
        # Collective intelligence metrics
        stats['collective_intelligence_domains'] = len(self.collective_intelligence)
        stats['total_collaborative_patterns'] = sum(
            len(ci['patterns']) for ci in self.collective_intelligence.values()
        )
        
        return stats
    
    async def get_agent_learning_profile(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed learning profile for a specific agent"""
        agent_memories = [m for m in self.memories.values() if m.agent_id == agent_id]
        agent_patterns = [p for p in self.knowledge_patterns.values() if agent_id in p.learned_from]
        
        if not agent_memories:
            return {'error': 'No learning data for agent'}
        
        profile = {
            'agent_id': agent_id,
            'memory_count': len(agent_memories),
            'pattern_count': len(agent_patterns),
            'learning_efficiency': 0.0,
            'specializations': [],
            'collaboration_history': [],
            'innovation_score': 0.0,
            'knowledge_graph_size': 0
        }
        
        # Calculate learning efficiency
        total_experiences = len(agent_memories)
        successful_patterns = [p for p in agent_patterns if p.success_rate > 0.7]
        profile['learning_efficiency'] = len(successful_patterns) / max(total_experiences * 0.1, 1)
        
        # Identify specializations
        memory_content_analysis = defaultdict(int)
        for memory in agent_memories:
            content_str = json.dumps(memory.content, default=str)
            words = content_str.split()
            for word in words:
                if len(word) > 4:  # Focus on meaningful terms
                    memory_content_analysis[word.lower()] += 1
        
        profile['specializations'] = [
            word for word, count in sorted(memory_content_analysis.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]
        ]
        
        # Analyze collaboration history
        collaborative_memories = [m for m in agent_memories if 'collaboration' in str(m.content)]
        profile['collaboration_history'] = [
            {
                'timestamp': m.timestamp,
                'importance': m.importance,
                'content_summary': str(m.content)[:100]
            }
            for m in collaborative_memories[-5:]  # Last 5 collaborations
        ]
        
        # Calculate innovation score
        innovative_patterns = [p for p in agent_patterns if 'innovative' in p.pattern_type.lower()]
        learned_capabilities = sum(1 for m in agent_memories if 'learned' in str(m.content))
        profile['innovation_score'] = (len(innovative_patterns) * 0.5 + learned_capabilities * 0.1) / max(total_experiences * 0.1, 1)
        
        # Knowledge graph statistics
        if agent_id in self.agent_knowledge_graphs:
            graph = self.agent_knowledge_graphs[agent_id]
            profile['knowledge_graph_size'] = len(graph['nodes'])
            profile['knowledge_connections'] = len(graph['edges'])
        
        return profile
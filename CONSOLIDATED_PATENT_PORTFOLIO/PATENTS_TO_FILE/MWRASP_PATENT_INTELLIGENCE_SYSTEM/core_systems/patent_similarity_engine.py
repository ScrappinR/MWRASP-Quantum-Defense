#!/usr/bin/env python3
"""
Advanced Patent Similarity Detection Engine
===========================================

Professional-grade patent similarity analysis using multiple algorithms
including semantic analysis, claim structure comparison, technical feature
matching, and citation network analysis.

Features:
- Multi-dimensional similarity scoring
- Semantic text analysis with NLP
- Patent claim structure analysis  
- Technical classification comparison
- Citation relationship analysis
- Inventor and assignee network analysis
- Prior art conflict detection
- Patent family relationship mapping
- Temporal analysis and trend detection
- Automated similarity reporting

Author: MWRASP Patent Intelligence Team
Date: August 2025
"""

import os
import json
import re
import math
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

@dataclass
class PatentDocument:
    """Structured patent document for similarity analysis"""
    patent_id: str
    patent_number: str
    title: str
    abstract: str
    claims: List[str]
    description: str
    inventors: List[str]
    assignees: List[str]
    filing_date: str
    classification_codes: List[str]
    cited_patents: List[str]
    citing_patents: List[str]
    patent_family: List[str]
    technical_keywords: List[str]

@dataclass
class SimilarityScore:
    """Comprehensive similarity score between two patents"""
    patent_a: str
    patent_b: str
    overall_similarity: float
    text_similarity: float
    claim_similarity: float
    classification_similarity: float
    citation_similarity: float
    inventor_similarity: float
    temporal_similarity: float
    technical_similarity: float
    semantic_similarity: float
    structural_similarity: float
    similarity_components: Dict[str, float]
    conflict_level: str
    relationship_type: str
    analysis_confidence: float

@dataclass
class SimilarityCluster:
    """Group of similar patents"""
    cluster_id: str
    patent_ids: List[str]
    cluster_centroid: Dict[str, float]
    similarity_matrix: Dict[str, Dict[str, float]]
    cluster_keywords: List[str]
    cluster_classification: List[str]
    cluster_assignees: List[str]
    cluster_strength: float
    cluster_description: str

class PatentSimilarityEngine:
    """Advanced patent similarity detection and analysis engine"""
    
    def __init__(self, base_directory: str):
        self.base_dir = Path(base_directory)
        self.similarity_cache_dir = self.base_dir / "similarity_analysis"
        self.similarity_cache_dir.mkdir(exist_ok=True)
        
        # Initialize NLP components
        self._initialize_nlp_components()
        
        # Similarity weights for different components
        self.similarity_weights = {
            'text': 0.25,
            'claims': 0.30,
            'classification': 0.15,
            'citations': 0.10,
            'inventors': 0.05,
            'temporal': 0.05,
            'technical': 0.10
        }
        
        # Classification code hierarchies
        self.cpc_hierarchies = {
            'A': 'Human Necessities',
            'B': 'Performing Operations; Transporting',
            'C': 'Chemistry; Metallurgy', 
            'D': 'Textiles; Paper',
            'E': 'Fixed Constructions',
            'F': 'Mechanical Engineering',
            'G': 'Physics',
            'H': 'Electricity'
        }
        
        # Technical keyword mappings
        self.technical_domains = {
            'quantum': ['quantum', 'qubit', 'superposition', 'entanglement', 'decoherence'],
            'ai_ml': ['artificial intelligence', 'machine learning', 'neural network', 'deep learning'],
            'crypto': ['cryptography', 'encryption', 'hash', 'digital signature', 'public key'],
            'security': ['cybersecurity', 'firewall', 'intrusion', 'malware', 'authentication'],
            'networking': ['network', 'protocol', 'tcp', 'ip', 'wireless', 'ethernet']
        }
    
    def _initialize_nlp_components(self):
        """Initialize NLP components for text processing"""
        
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            
            # Initialize TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 3),
                stop_words='english',
                min_df=2,
                max_df=0.95
            )
            
            print("✅ NLP components initialized successfully")
            
        except Exception as e:
            print(f"⚠️ NLP initialization warning: {e}")
            # Fallback to basic text processing
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.lemmatizer = None
    
    async def analyze_patent_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> SimilarityScore:
        """Comprehensive similarity analysis between two patents"""
        
        print(f"🔍 Analyzing similarity: {patent_a.patent_number} vs {patent_b.patent_number}")
        
        # Component similarity calculations
        text_sim = self._calculate_text_similarity(patent_a, patent_b)
        claim_sim = self._calculate_claim_similarity(patent_a, patent_b)
        class_sim = self._calculate_classification_similarity(patent_a, patent_b)
        cite_sim = self._calculate_citation_similarity(patent_a, patent_b)
        inventor_sim = self._calculate_inventor_similarity(patent_a, patent_b)
        temporal_sim = self._calculate_temporal_similarity(patent_a, patent_b)
        technical_sim = self._calculate_technical_similarity(patent_a, patent_b)
        semantic_sim = self._calculate_semantic_similarity(patent_a, patent_b)
        structural_sim = self._calculate_structural_similarity(patent_a, patent_b)
        
        # Calculate weighted overall similarity
        overall_similarity = (
            text_sim * self.similarity_weights['text'] +
            claim_sim * self.similarity_weights['claims'] +
            class_sim * self.similarity_weights['classification'] +
            cite_sim * self.similarity_weights['citations'] +
            inventor_sim * self.similarity_weights['inventors'] +
            temporal_sim * self.similarity_weights['temporal'] +
            technical_sim * self.similarity_weights['technical']
        )
        
        # Determine conflict level and relationship type
        conflict_level = self._assess_conflict_level(overall_similarity, claim_sim, class_sim)
        relationship_type = self._determine_relationship_type(
            overall_similarity, patent_a, patent_b, cite_sim
        )
        
        # Calculate analysis confidence
        confidence = self._calculate_confidence(
            text_sim, claim_sim, class_sim, cite_sim, patent_a, patent_b
        )
        
        similarity_score = SimilarityScore(
            patent_a=patent_a.patent_number,
            patent_b=patent_b.patent_number,
            overall_similarity=overall_similarity,
            text_similarity=text_sim,
            claim_similarity=claim_sim,
            classification_similarity=class_sim,
            citation_similarity=cite_sim,
            inventor_similarity=inventor_sim,
            temporal_similarity=temporal_sim,
            technical_similarity=technical_sim,
            semantic_similarity=semantic_sim,
            structural_similarity=structural_sim,
            similarity_components={
                'text': text_sim,
                'claims': claim_sim,
                'classification': class_sim,
                'citations': cite_sim,
                'inventors': inventor_sim,
                'temporal': temporal_sim,
                'technical': technical_sim,
                'semantic': semantic_sim,
                'structural': structural_sim
            },
            conflict_level=conflict_level,
            relationship_type=relationship_type,
            analysis_confidence=confidence
        )
        
        return similarity_score
    
    def _calculate_text_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate text-based similarity using TF-IDF and cosine similarity"""
        
        try:
            # Combine title, abstract, and description
            text_a = f"{patent_a.title} {patent_a.abstract} {patent_a.description}"
            text_b = f"{patent_b.title} {patent_b.abstract} {patent_b.description}"
            
            # Preprocess texts
            processed_a = self._preprocess_text(text_a)
            processed_b = self._preprocess_text(text_b)
            
            if not processed_a or not processed_b:
                return 0.0
            
            # Calculate TF-IDF vectors
            corpus = [processed_a, processed_b]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return float(similarity_matrix[0][1])
            
        except Exception as e:
            print(f"⚠️ Text similarity calculation error: {e}")
            return 0.0
    
    def _calculate_claim_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on patent claims structure and content"""
        
        try:
            claims_a = patent_a.claims if patent_a.claims else []
            claims_b = patent_b.claims if patent_b.claims else []
            
            if not claims_a or not claims_b:
                return 0.0
            
            # Analyze claim structure similarity
            structure_sim = self._analyze_claim_structure(claims_a, claims_b)
            
            # Analyze claim content similarity
            content_sim = self._analyze_claim_content(claims_a, claims_b)
            
            # Weighted combination
            claim_similarity = 0.6 * content_sim + 0.4 * structure_sim
            
            return claim_similarity
            
        except Exception as e:
            print(f"⚠️ Claim similarity calculation error: {e}")
            return 0.0
    
    def _analyze_claim_structure(self, claims_a: List[str], claims_b: List[str]) -> float:
        """Analyze structural similarity of patent claims"""
        
        try:
            # Extract claim elements
            elements_a = self._extract_claim_elements(claims_a)
            elements_b = self._extract_claim_elements(claims_b)
            
            if not elements_a or not elements_b:
                return 0.0
            
            # Calculate Jaccard similarity of claim elements
            set_a = set(elements_a)
            set_b = set(elements_b)
            
            intersection = len(set_a.intersection(set_b))
            union = len(set_a.union(set_b))
            
            if union == 0:
                return 0.0
            
            return intersection / union
            
        except Exception as e:
            print(f"⚠️ Claim structure analysis error: {e}")
            return 0.0
    
    def _extract_claim_elements(self, claims: List[str]) -> List[str]:
        """Extract key elements from patent claims"""
        
        elements = []
        
        for claim in claims:
            # Extract technical terms and phrases
            claim_lower = claim.lower()
            
            # Look for "comprising", "including", "having" patterns
            patterns = [
                r'comprising\s+([^;,.]+)',
                r'including\s+([^;,.]+)', 
                r'having\s+([^;,.]+)',
                r'wherein\s+([^;,.]+)',
                r'characterized by\s+([^;,.]+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, claim_lower)
                elements.extend(matches)
            
            # Extract noun phrases (simplified)
            words = claim_lower.split()
            for i in range(len(words) - 1):
                if len(words[i]) > 3 and len(words[i+1]) > 3:
                    elements.append(f"{words[i]} {words[i+1]}")
        
        return [elem.strip() for elem in elements if len(elem.strip()) > 3]
    
    def _analyze_claim_content(self, claims_a: List[str], claims_b: List[str]) -> float:
        """Analyze content similarity of patent claims"""
        
        try:
            # Combine all claims into single texts
            text_a = " ".join(claims_a)
            text_b = " ".join(claims_b)
            
            # Use TF-IDF similarity
            processed_a = self._preprocess_text(text_a)
            processed_b = self._preprocess_text(text_b)
            
            if not processed_a or not processed_b:
                return 0.0
            
            corpus = [processed_a, processed_b]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            return float(similarity_matrix[0][1])
            
        except Exception as e:
            print(f"⚠️ Claim content analysis error: {e}")
            return 0.0
    
    def _calculate_classification_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on patent classification codes"""
        
        try:
            codes_a = set(patent_a.classification_codes)
            codes_b = set(patent_b.classification_codes)
            
            if not codes_a or not codes_b:
                return 0.0
            
            # Exact match similarity
            exact_match = len(codes_a.intersection(codes_b)) / len(codes_a.union(codes_b))
            
            # Hierarchical similarity (for CPC codes)
            hierarchical_sim = self._calculate_hierarchical_classification_similarity(codes_a, codes_b)
            
            # Weighted combination
            classification_similarity = 0.7 * exact_match + 0.3 * hierarchical_sim
            
            return classification_similarity
            
        except Exception as e:
            print(f"⚠️ Classification similarity calculation error: {e}")
            return 0.0
    
    def _calculate_hierarchical_classification_similarity(self, codes_a: Set[str], codes_b: Set[str]) -> float:
        """Calculate hierarchical similarity for classification codes"""
        
        try:
            # Extract main sections (first letter)
            sections_a = set(code[0] for code in codes_a if code)
            sections_b = set(code[0] for code in codes_b if code)
            
            if not sections_a or not sections_b:
                return 0.0
            
            # Calculate section overlap
            section_overlap = len(sections_a.intersection(sections_b)) / len(sections_a.union(sections_b))
            
            # Extract class level (first 3 characters)
            classes_a = set(code[:3] for code in codes_a if len(code) >= 3)
            classes_b = set(code[:3] for code in codes_b if len(code) >= 3)
            
            class_overlap = 0.0
            if classes_a and classes_b:
                class_overlap = len(classes_a.intersection(classes_b)) / len(classes_a.union(classes_b))
            
            # Weighted hierarchical similarity
            hierarchical_sim = 0.3 * section_overlap + 0.7 * class_overlap
            
            return hierarchical_sim
            
        except Exception as e:
            print(f"⚠️ Hierarchical classification similarity error: {e}")
            return 0.0
    
    def _calculate_citation_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on citation networks"""
        
        try:
            # Direct citation relationship
            direct_relation = 0.0
            if patent_a.patent_number in patent_b.cited_patents or patent_b.patent_number in patent_a.cited_patents:
                direct_relation = 1.0
            elif patent_a.patent_number in patent_b.citing_patents or patent_b.patent_number in patent_a.citing_patents:
                direct_relation = 0.8
            
            # Shared citations
            cited_a = set(patent_a.cited_patents)
            cited_b = set(patent_b.cited_patents)
            citing_a = set(patent_a.citing_patents)
            citing_b = set(patent_b.citing_patents)
            
            shared_cited = len(cited_a.intersection(cited_b))
            shared_citing = len(citing_a.intersection(citing_b))
            
            # Calculate shared citation similarity
            shared_similarity = 0.0
            if cited_a and cited_b:
                shared_cited_sim = shared_cited / len(cited_a.union(cited_b))
                shared_similarity += 0.6 * shared_cited_sim
            
            if citing_a and citing_b:
                shared_citing_sim = shared_citing / len(citing_a.union(citing_b))
                shared_similarity += 0.4 * shared_citing_sim
            
            # Combined citation similarity
            citation_similarity = max(direct_relation, shared_similarity)
            
            return citation_similarity
            
        except Exception as e:
            print(f"⚠️ Citation similarity calculation error: {e}")
            return 0.0
    
    def _calculate_inventor_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on inventors and assignees"""
        
        try:
            # Inventor overlap
            inventors_a = set(patent_a.inventors)
            inventors_b = set(patent_b.inventors)
            
            inventor_sim = 0.0
            if inventors_a and inventors_b:
                inventor_overlap = len(inventors_a.intersection(inventors_b))
                inventor_sim = inventor_overlap / len(inventors_a.union(inventors_b))
            
            # Assignee overlap
            assignees_a = set(patent_a.assignees)
            assignees_b = set(patent_b.assignees)
            
            assignee_sim = 0.0
            if assignees_a and assignees_b:
                assignee_overlap = len(assignees_a.intersection(assignees_b))
                assignee_sim = assignee_overlap / len(assignees_a.union(assignees_b))
            
            # Weighted combination (assignees are more important)
            inventor_similarity = 0.3 * inventor_sim + 0.7 * assignee_sim
            
            return inventor_similarity
            
        except Exception as e:
            print(f"⚠️ Inventor similarity calculation error: {e}")
            return 0.0
    
    def _calculate_temporal_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on filing dates"""
        
        try:
            date_a = datetime.strptime(patent_a.filing_date, '%Y-%m-%d')
            date_b = datetime.strptime(patent_b.filing_date, '%Y-%m-%d')
            
            # Calculate time difference in days
            time_diff = abs((date_a - date_b).days)
            
            # Convert to similarity score (closer dates = higher similarity)
            # Patents filed within 2 years get high temporal similarity
            if time_diff <= 730:  # 2 years
                temporal_similarity = 1.0 - (time_diff / 730) * 0.5
            else:
                temporal_similarity = 0.5 * math.exp(-(time_diff - 730) / 1095)  # 3 year decay
            
            return max(0.0, temporal_similarity)
            
        except Exception as e:
            print(f"⚠️ Temporal similarity calculation error: {e}")
            return 0.0
    
    def _calculate_technical_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on technical keywords and domains"""
        
        try:
            keywords_a = set(patent_a.technical_keywords)
            keywords_b = set(patent_b.technical_keywords)
            
            if not keywords_a or not keywords_b:
                return 0.0
            
            # Direct keyword overlap
            keyword_overlap = len(keywords_a.intersection(keywords_b)) / len(keywords_a.union(keywords_b))
            
            # Technical domain similarity
            domain_sim = self._calculate_technical_domain_similarity(
                keywords_a, keywords_b
            )
            
            # Combined technical similarity
            technical_similarity = 0.6 * keyword_overlap + 0.4 * domain_sim
            
            return technical_similarity
            
        except Exception as e:
            print(f"⚠️ Technical similarity calculation error: {e}")
            return 0.0
    
    def _calculate_technical_domain_similarity(self, keywords_a: Set[str], keywords_b: Set[str]) -> float:
        """Calculate similarity based on technical domains"""
        
        try:
            # Map keywords to domains
            domains_a = set()
            domains_b = set()
            
            for domain, domain_keywords in self.technical_domains.items():
                if any(keyword in ' '.join(keywords_a).lower() for keyword in domain_keywords):
                    domains_a.add(domain)
                if any(keyword in ' '.join(keywords_b).lower() for keyword in domain_keywords):
                    domains_b.add(domain)
            
            if not domains_a or not domains_b:
                return 0.0
            
            # Calculate domain overlap
            domain_overlap = len(domains_a.intersection(domains_b)) / len(domains_a.union(domains_b))
            
            return domain_overlap
            
        except Exception as e:
            print(f"⚠️ Technical domain similarity error: {e}")
            return 0.0
    
    def _calculate_semantic_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate semantic similarity using advanced NLP techniques"""
        
        try:
            # Combine all text content
            text_a = f"{patent_a.title} {patent_a.abstract} {' '.join(patent_a.claims)}"
            text_b = f"{patent_b.title} {patent_b.abstract} {' '.join(patent_b.claims)}"
            
            # Extract semantic features using topic modeling approach
            semantic_sim = self._calculate_topic_similarity([text_a, text_b])
            
            return semantic_sim
            
        except Exception as e:
            print(f"⚠️ Semantic similarity calculation error: {e}")
            return 0.0
    
    def _calculate_topic_similarity(self, texts: List[str]) -> float:
        """Calculate topic-based semantic similarity"""
        
        try:
            if len(texts) != 2:
                return 0.0
            
            # Preprocess texts
            processed_texts = [self._preprocess_text(text) for text in texts]
            
            if not all(processed_texts):
                return 0.0
            
            # Create TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(processed_texts)
            
            # Use LDA for topic modeling (simplified approach)
            n_topics = min(5, tfidf_matrix.shape[1])  # Limit topics
            
            if n_topics < 2:
                # Fall back to cosine similarity
                similarity_matrix = cosine_similarity(tfidf_matrix)
                return float(similarity_matrix[0][1])
            
            lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
            topic_distributions = lda.fit_transform(tfidf_matrix)
            
            # Calculate similarity between topic distributions
            topic_sim = cosine_similarity([topic_distributions[0]], [topic_distributions[1]])[0][0]
            
            return float(topic_sim)
            
        except Exception as e:
            print(f"⚠️ Topic similarity calculation error: {e}")
            return 0.0
    
    def _calculate_structural_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate structural similarity based on patent document structure"""
        
        try:
            # Compare document lengths and structure
            len_similarity = self._calculate_length_similarity(patent_a, patent_b)
            
            # Compare section organization
            section_similarity = self._calculate_section_similarity(patent_a, patent_b)
            
            # Combined structural similarity
            structural_sim = 0.6 * len_similarity + 0.4 * section_similarity
            
            return structural_sim
            
        except Exception as e:
            print(f"⚠️ Structural similarity calculation error: {e}")
            return 0.0
    
    def _calculate_length_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on document lengths"""
        
        try:
            # Calculate lengths
            len_a = len(patent_a.abstract) + len(patent_a.description) + sum(len(claim) for claim in patent_a.claims)
            len_b = len(patent_b.abstract) + len(patent_b.description) + sum(len(claim) for claim in patent_b.claims)
            
            if len_a == 0 or len_b == 0:
                return 0.0
            
            # Similarity based on length ratio
            ratio = min(len_a, len_b) / max(len_a, len_b)
            
            return ratio
            
        except Exception as e:
            return 0.0
    
    def _calculate_section_similarity(self, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate similarity based on document section structure"""
        
        try:
            # Compare number of claims
            claims_a = len(patent_a.claims) if patent_a.claims else 0
            claims_b = len(patent_b.claims) if patent_b.claims else 0
            
            if claims_a == 0 and claims_b == 0:
                claims_sim = 1.0
            elif claims_a == 0 or claims_b == 0:
                claims_sim = 0.0
            else:
                claims_sim = min(claims_a, claims_b) / max(claims_a, claims_b)
            
            # Compare number of classification codes
            class_a = len(patent_a.classification_codes)
            class_b = len(patent_b.classification_codes)
            
            if class_a == 0 and class_b == 0:
                class_sim = 1.0
            elif class_a == 0 or class_b == 0:
                class_sim = 0.0
            else:
                class_sim = min(class_a, class_b) / max(class_a, class_b)
            
            # Combined section similarity
            section_sim = 0.7 * claims_sim + 0.3 * class_sim
            
            return section_sim
            
        except Exception as e:
            return 0.0
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for similarity analysis"""
        
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters and digits
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            
            # Tokenize
            words = text.split()
            
            # Remove stopwords
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            
            # Lemmatize if available
            if self.lemmatizer:
                words = [self.lemmatizer.lemmatize(word) for word in words]
            
            return ' '.join(words)
            
        except Exception as e:
            print(f"⚠️ Text preprocessing error: {e}")
            return text.lower()
    
    def _assess_conflict_level(self, overall_similarity: float, claim_similarity: float, class_similarity: float) -> str:
        """Assess the conflict level between patents"""
        
        # High conflict indicators
        if (overall_similarity > 0.8 and claim_similarity > 0.7) or claim_similarity > 0.85:
            return "VERY HIGH"
        elif (overall_similarity > 0.7 and claim_similarity > 0.6) or claim_similarity > 0.75:
            return "HIGH"
        elif (overall_similarity > 0.5 and claim_similarity > 0.4) or class_similarity > 0.8:
            return "MEDIUM"
        elif overall_similarity > 0.3:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _determine_relationship_type(self, overall_similarity: float, patent_a: PatentDocument, 
                                   patent_b: PatentDocument, citation_similarity: float) -> str:
        """Determine the relationship type between patents"""
        
        # Direct citation relationship
        if citation_similarity >= 0.8:
            return "Direct Citation"
        elif citation_similarity > 0.5:
            return "Citation Network"
        
        # Same assignee
        if set(patent_a.assignees).intersection(set(patent_b.assignees)):
            if overall_similarity > 0.6:
                return "Portfolio Patents"
            else:
                return "Same Assignee"
        
        # High similarity relationships
        if overall_similarity > 0.8:
            return "Potential Duplicate/Continuation"
        elif overall_similarity > 0.6:
            return "Closely Related"
        elif overall_similarity > 0.4:
            return "Related Technology"
        elif overall_similarity > 0.2:
            return "Same Field"
        else:
            return "Unrelated"
    
    def _calculate_confidence(self, text_sim: float, claim_sim: float, class_sim: float, 
                            cite_sim: float, patent_a: PatentDocument, patent_b: PatentDocument) -> float:
        """Calculate confidence in the similarity analysis"""
        
        # Factors that increase confidence
        confidence_factors = []
        
        # Data completeness
        if patent_a.abstract and patent_b.abstract:
            confidence_factors.append(0.2)
        if patent_a.claims and patent_b.claims:
            confidence_factors.append(0.3)
        if patent_a.classification_codes and patent_b.classification_codes:
            confidence_factors.append(0.2)
        if patent_a.cited_patents and patent_b.cited_patents:
            confidence_factors.append(0.1)
        
        # Similarity consistency
        similarities = [text_sim, claim_sim, class_sim, cite_sim]
        valid_similarities = [s for s in similarities if s > 0]
        
        if valid_similarities:
            similarity_variance = np.var(valid_similarities)
            # Lower variance = higher confidence
            consistency_factor = max(0, 0.2 - similarity_variance)
            confidence_factors.append(consistency_factor)
        
        # Base confidence
        base_confidence = 0.6
        
        # Total confidence
        total_confidence = base_confidence + sum(confidence_factors)
        
        return min(1.0, total_confidence)
    
    async def analyze_patent_cluster_similarity(self, patents: List[PatentDocument]) -> List[SimilarityCluster]:
        """Analyze similarity patterns within a group of patents to identify clusters"""
        
        print(f"🔍 Analyzing similarity clusters for {len(patents)} patents")
        
        if len(patents) < 2:
            return []
        
        # Calculate pairwise similarities
        similarity_matrix = {}
        
        for i, patent_a in enumerate(patents):
            similarity_matrix[patent_a.patent_number] = {}
            
            for j, patent_b in enumerate(patents):
                if i <= j:
                    if i == j:
                        similarity_matrix[patent_a.patent_number][patent_b.patent_number] = 1.0
                    else:
                        similarity_score = await self.analyze_patent_similarity(patent_a, patent_b)
                        similarity_matrix[patent_a.patent_number][patent_b.patent_number] = similarity_score.overall_similarity
                        
                        # Mirror the similarity
                        if patent_b.patent_number not in similarity_matrix:
                            similarity_matrix[patent_b.patent_number] = {}
                        similarity_matrix[patent_b.patent_number][patent_a.patent_number] = similarity_score.overall_similarity
        
        # Identify clusters using similarity threshold
        clusters = self._identify_similarity_clusters(patents, similarity_matrix, threshold=0.5)
        
        print(f"✅ Identified {len(clusters)} similarity clusters")
        
        return clusters
    
    def _identify_similarity_clusters(self, patents: List[PatentDocument], 
                                    similarity_matrix: Dict[str, Dict[str, float]], 
                                    threshold: float = 0.5) -> List[SimilarityCluster]:
        """Identify patent clusters based on similarity matrix"""
        
        clusters = []
        assigned_patents = set()
        
        for i, patent in enumerate(patents):
            if patent.patent_number in assigned_patents:
                continue
            
            # Start a new cluster
            cluster_patents = [patent.patent_number]
            assigned_patents.add(patent.patent_number)
            
            # Find similar patents
            for other_patent in patents:
                if (other_patent.patent_number not in assigned_patents and 
                    similarity_matrix.get(patent.patent_number, {}).get(other_patent.patent_number, 0) > threshold):
                    cluster_patents.append(other_patent.patent_number)
                    assigned_patents.add(other_patent.patent_number)
            
            # Create cluster if it has multiple patents
            if len(cluster_patents) > 1:
                cluster = self._create_similarity_cluster(cluster_patents, patents, similarity_matrix)
                clusters.append(cluster)
        
        return clusters
    
    def _create_similarity_cluster(self, cluster_patent_ids: List[str], 
                                 all_patents: List[PatentDocument],
                                 similarity_matrix: Dict[str, Dict[str, float]]) -> SimilarityCluster:
        """Create a similarity cluster from patent IDs"""
        
        # Get patent objects for cluster
        cluster_patents = [p for p in all_patents if p.patent_number in cluster_patent_ids]
        
        # Calculate cluster centroid (average similarities)
        centroid = {}
        for patent_id in cluster_patent_ids:
            similarities = []
            for other_id in cluster_patent_ids:
                if other_id != patent_id:
                    similarities.append(similarity_matrix.get(patent_id, {}).get(other_id, 0))
            centroid[patent_id] = sum(similarities) / len(similarities) if similarities else 0
        
        # Extract cluster keywords
        all_keywords = []
        for patent in cluster_patents:
            all_keywords.extend(patent.technical_keywords)
        keyword_counts = Counter(all_keywords)
        cluster_keywords = [keyword for keyword, count in keyword_counts.most_common(10)]
        
        # Extract cluster classifications
        all_classifications = []
        for patent in cluster_patents:
            all_classifications.extend(patent.classification_codes)
        class_counts = Counter(all_classifications)
        cluster_classifications = [code for code, count in class_counts.most_common(5)]
        
        # Extract cluster assignees
        all_assignees = []
        for patent in cluster_patents:
            all_assignees.extend(patent.assignees)
        assignee_counts = Counter(all_assignees)
        cluster_assignees = [assignee for assignee, count in assignee_counts.most_common(5)]
        
        # Calculate cluster strength (average pairwise similarity)
        all_similarities = []
        for i, patent_id_a in enumerate(cluster_patent_ids):
            for j, patent_id_b in enumerate(cluster_patent_ids):
                if i < j:
                    sim = similarity_matrix.get(patent_id_a, {}).get(patent_id_b, 0)
                    all_similarities.append(sim)
        
        cluster_strength = sum(all_similarities) / len(all_similarities) if all_similarities else 0
        
        # Create cluster description
        main_keywords = cluster_keywords[:3]
        main_assignees = cluster_assignees[:2]
        cluster_description = f"Patent cluster focusing on {', '.join(main_keywords)} technology"
        if main_assignees:
            cluster_description += f" (primarily from {', '.join(main_assignees)})"
        
        cluster = SimilarityCluster(
            cluster_id=f"cluster_{len(cluster_patent_ids)}_{int(cluster_strength*100)}",
            patent_ids=cluster_patent_ids,
            cluster_centroid=centroid,
            similarity_matrix={pid: similarity_matrix.get(pid, {}) for pid in cluster_patent_ids},
            cluster_keywords=cluster_keywords,
            cluster_classification=cluster_classifications,
            cluster_assignees=cluster_assignees,
            cluster_strength=cluster_strength,
            cluster_description=cluster_description
        )
        
        return cluster
    
    def save_similarity_analysis(self, similarity_results: List[SimilarityScore], 
                               analysis_description: str = "Patent Similarity Analysis") -> Path:
        """Save similarity analysis results"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = self.similarity_cache_dir / f"similarity_analysis_{timestamp}"
        results_dir.mkdir(exist_ok=True)
        
        # Save structured data
        results_data = []
        for result in similarity_results:
            results_data.append(asdict(result))
        
        data_file = results_dir / "similarity_analysis_data.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_metadata': {
                    'timestamp': timestamp,
                    'description': analysis_description,
                    'total_comparisons': len(similarity_results),
                    'analysis_engine': 'MWRASP Patent Similarity Engine'
                },
                'similarity_results': results_data
            }, f, indent=2)
        
        # Generate similarity report
        report = self._generate_similarity_report(similarity_results, analysis_description, timestamp)
        report_file = results_dir / "Patent_Similarity_Analysis_Report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"💾 Similarity analysis saved to: {results_dir}")
        return results_dir
    
    def _generate_similarity_report(self, similarity_results: List[SimilarityScore], 
                                  description: str, timestamp: str) -> str:
        """Generate comprehensive similarity analysis report"""
        
        if not similarity_results:
            return "# Patent Similarity Analysis Report\n\nNo similarity results to report."
        
        # Calculate statistics
        overall_similarities = [result.overall_similarity for result in similarity_results]
        avg_similarity = sum(overall_similarities) / len(overall_similarities)
        max_similarity = max(overall_similarities)
        min_similarity = min(overall_similarities)
        
        # Conflict level distribution
        conflict_counts = Counter(result.conflict_level for result in similarity_results)
        
        # Relationship type distribution  
        relationship_counts = Counter(result.relationship_type for result in similarity_results)
        
        # High similarity pairs
        high_similarity_pairs = [result for result in similarity_results if result.overall_similarity > 0.7]
        
        report = f"""# PATENT SIMILARITY ANALYSIS REPORT

## {description}

**Generated:** {timestamp}  
**Total Comparisons:** {len(similarity_results)}  
**Analysis Engine:** MWRASP Advanced Patent Similarity Engine  

---

## EXECUTIVE SUMMARY

### Similarity Statistics
- **Average Similarity:** {avg_similarity:.3f}
- **Maximum Similarity:** {max_similarity:.3f}  
- **Minimum Similarity:** {min_similarity:.3f}
- **High Similarity Pairs (>0.7):** {len(high_similarity_pairs)}

### Risk Assessment
- **Very High Conflict:** {conflict_counts.get('VERY HIGH', 0)} pairs
- **High Conflict:** {conflict_counts.get('HIGH', 0)} pairs  
- **Medium Conflict:** {conflict_counts.get('MEDIUM', 0)} pairs
- **Low Conflict:** {conflict_counts.get('LOW', 0)} pairs

---

## DETAILED ANALYSIS

### Conflict Level Distribution
"""
        
        for level in ['VERY HIGH', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
            count = conflict_counts.get(level, 0)
            percentage = (count / len(similarity_results)) * 100
            report += f"- **{level}:** {count} pairs ({percentage:.1f}%)\n"
        
        report += f"""

### Relationship Types
"""
        
        for relationship, count in relationship_counts.most_common():
            percentage = (count / len(similarity_results)) * 100
            report += f"- **{relationship}:** {count} pairs ({percentage:.1f}%)\n"
        
        if high_similarity_pairs:
            report += f"""

---

## HIGH SIMILARITY PAIRS (>0.7)

"""
            
            for i, result in enumerate(high_similarity_pairs[:20], 1):  # Top 20
                report += f"""
### {i}. {result.patent_a} vs {result.patent_b}

**Overall Similarity:** {result.overall_similarity:.3f}  
**Conflict Level:** {result.conflict_level}  
**Relationship Type:** {result.relationship_type}  
**Analysis Confidence:** {result.analysis_confidence:.3f}  

**Component Similarities:**
- Text Similarity: {result.text_similarity:.3f}
- Claim Similarity: {result.claim_similarity:.3f}
- Classification Similarity: {result.classification_similarity:.3f}
- Citation Similarity: {result.citation_similarity:.3f}
- Technical Similarity: {result.technical_similarity:.3f}

---
"""
        
        # Component analysis
        component_averages = {}
        for component in ['text_similarity', 'claim_similarity', 'classification_similarity', 
                         'citation_similarity', 'technical_similarity', 'semantic_similarity']:
            values = [getattr(result, component) for result in similarity_results]
            component_averages[component] = sum(values) / len(values)
        
        report += f"""

## SIMILARITY COMPONENT ANALYSIS

### Average Component Similarities
"""
        
        for component, avg in sorted(component_averages.items(), key=lambda x: x[1], reverse=True):
            component_name = component.replace('_similarity', '').title()
            report += f"- **{component_name}:** {avg:.3f}\n"
        
        report += f"""

---

## RECOMMENDATIONS

### Immediate Actions
"""
        
        very_high_conflicts = conflict_counts.get('VERY HIGH', 0)
        high_conflicts = conflict_counts.get('HIGH', 0)
        
        if very_high_conflicts > 0:
            report += f"""
1. **Critical Review Required:** {very_high_conflicts} patent pairs show very high conflict potential
2. **Legal Analysis:** Conduct detailed freedom-to-operate analysis for high-risk pairs
3. **Claim Modification:** Consider claim amendments to reduce overlap
"""
        
        if high_conflicts > 0:
            report += f"""
4. **Patent Monitoring:** Establish monitoring for {high_conflicts} high-conflict patent pairs
5. **Prior Art Strategy:** Develop prior art arguments for potential challenges
"""
        
        report += f"""

### Strategic Recommendations
1. **Portfolio Analysis:** Review patent portfolio for internal conflicts
2. **Filing Strategy:** Adjust future filing strategy based on similarity patterns
3. **Competitive Intelligence:** Monitor competitor patents showing high similarity
4. **Licensing Opportunities:** Explore licensing for complementary patents

---

## METHODOLOGY

### Similarity Analysis Components
- **Text Analysis:** TF-IDF vectorization with cosine similarity
- **Claim Analysis:** Structural and content-based comparison
- **Classification Analysis:** Hierarchical code comparison
- **Citation Analysis:** Citation network relationship mapping
- **Technical Analysis:** Domain-specific keyword matching
- **Semantic Analysis:** Topic modeling and semantic similarity
- **Temporal Analysis:** Filing date proximity analysis

### Quality Metrics
- **Analysis Coverage:** {len(similarity_results)} pairwise comparisons
- **Average Confidence:** {sum(result.analysis_confidence for result in similarity_results) / len(similarity_results):.3f}
- **Data Completeness:** Multi-component analysis for comprehensive assessment

---

**Report Generated by:** MWRASP Patent Similarity Detection Engine  
**Next Analysis:** Recommended after portfolio updates or new filings  
**Contact:** Patent Intelligence Team for detailed analysis and strategic guidance
"""
        
        return report

# Integration functions
async def run_similarity_analysis(patents: List[PatentDocument], base_directory: str = None) -> Dict:
    """Run comprehensive patent similarity analysis"""
    
    if not base_directory:
        base_directory = r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE"
    
    engine = PatentSimilarityEngine(base_directory)
    
    # Perform pairwise similarity analysis
    similarity_results = []
    
    print(f"🔄 Starting similarity analysis for {len(patents)} patents...")
    
    for i, patent_a in enumerate(patents):
        for j, patent_b in enumerate(patents[i+1:], i+1):
            similarity_score = await engine.analyze_patent_similarity(patent_a, patent_b)
            similarity_results.append(similarity_score)
    
    # Perform cluster analysis
    clusters = await engine.analyze_patent_cluster_similarity(patents)
    
    # Save results
    results_path = engine.save_similarity_analysis(similarity_results, "Comprehensive Patent Similarity Analysis")
    
    return {
        'similarity_results': similarity_results,
        'similarity_clusters': clusters,
        'analysis_summary': {
            'total_comparisons': len(similarity_results),
            'total_clusters': len(clusters),
            'high_similarity_pairs': len([r for r in similarity_results if r.overall_similarity > 0.7]),
            'results_path': str(results_path)
        }
    }

# Demo function
async def demo_similarity_analysis():
    """Demo patent similarity analysis functionality"""
    
    print("🧪 PATENT SIMILARITY ANALYSIS DEMO")
    print("=" * 60)
    
    # Create sample patent documents
    sample_patents = [
        PatentDocument(
            patent_id="1", patent_number="US10123456A1", 
            title="Quantum Computing Security System",
            abstract="A quantum computing system for enhanced cybersecurity applications...",
            claims=["A quantum security system comprising...", "The system of claim 1 wherein..."],
            description="This invention relates to quantum computing security...",
            inventors=["John Smith", "Jane Doe"],
            assignees=["Tech Corp"],
            filing_date="2023-01-15",
            classification_codes=["G06N10/00", "H04L63/14"],
            cited_patents=["US9876543B2"],
            citing_patents=["US11234567A1"],
            patent_family=["US10123456A1"],
            technical_keywords=["quantum", "security", "encryption"]
        ),
        PatentDocument(
            patent_id="2", patent_number="US10234567B2",
            title="Quantum Cryptographic Authentication Method", 
            abstract="A method for quantum-based cryptographic authentication...",
            claims=["A quantum authentication method comprising...", "The method of claim 1 further including..."],
            description="This invention provides quantum cryptographic authentication...",
            inventors=["Alice Johnson", "Bob Wilson"],
            assignees=["Quantum Solutions"],
            filing_date="2023-02-20",
            classification_codes=["G06N10/00", "H04L9/32"],
            cited_patents=["US9876543B2", "US8765432A1"],
            citing_patents=[],
            patent_family=["US10234567B2"],
            technical_keywords=["quantum", "cryptography", "authentication"]
        )
    ]
    
    base_dir = r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE"
    
    # Run similarity analysis
    results = await run_similarity_analysis(sample_patents, base_dir)
    
    print(f"\n✅ DEMO COMPLETE!")
    print(f"📊 Analyzed {results['analysis_summary']['total_comparisons']} patent pairs")
    print(f"🔗 Identified {results['analysis_summary']['total_clusters']} clusters")
    print(f"⚠️ Found {results['analysis_summary']['high_similarity_pairs']} high-similarity pairs")
    print(f"💾 Results saved to: {results['analysis_summary']['results_path']}")

if __name__ == "__main__":
    asyncio.run(demo_similarity_analysis())
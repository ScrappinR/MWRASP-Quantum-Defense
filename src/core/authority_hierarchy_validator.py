"""
MWRASP Authority Hierarchy Automated Validation System
Ensures continuous compliance with established authority hierarchy across all documentation
"""

import os
import re
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from pathlib import Path
import hashlib

class ViolationSeverity(Enum):
    CRITICAL = "critical"  # Contradicts working system
    HIGH = "high"         # Uses deprecated metrics
    MEDIUM = "medium"     # Inconsistent messaging
    LOW = "low"          # Minor formatting issues

class DocumentStatus(Enum):
    COMPLIANT = "compliant"
    VIOLATIONS_FOUND = "violations_found"
    NOT_ANALYZED = "not_analyzed"
    AUTHORITY_REFERENCE = "authority_reference"

@dataclass
class AuthorityViolation:
    severity: ViolationSeverity
    violation_type: str
    line_number: int
    content: str
    correct_content: str
    explanation: str

@dataclass
class DocumentAnalysis:
    file_path: str
    status: DocumentStatus
    violations: List[AuthorityViolation]
    compliance_score: float
    last_analyzed: datetime
    recommendations: List[str]

class AuthorityHierarchyValidator:
    """Automated validation system for MWRASP authority hierarchy compliance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Authority Hierarchy Configuration
        self.config = {
            'authority_sources': {
                'tier1_ultimate': [
                    'MWRASP_COMPLETE_UNIFIED_SYSTEM.py',
                    'MWRASP_COMPLETE_SYSTEM_SUMMARY.md',
                    '01_EXECUTIVE_SUMMARY/PROJECT_OVERVIEW.md'
                ],
                'tier2_masters': [
                    'MWRASP_DARPA_Whitepaper_UPDATED.md',
                    '17_COMPETITIVE_ANALYSIS_UPDATED.md',
                    'PARADIGM_SHIFT_NARRATIVE_UPDATED.md',
                    'ACQUISITION_READY_REPORT.md'
                ]
            }
        }
        
        # Mandatory Authority Compliance Rules
        self.authority_rules = {
            'mandatory_system_description': 'MWRASP Complete Unified Defense System',
            'mandatory_positioning': 'first integrated quantum-financial-legal-tactical defense platform with working dashboard',
            'mandatory_metrics': {
                'behavioral_auth': '0.1ms',
                'agent_coordination': '63-78ms',
                'market_protection': '$257M+',
                'data_fragmentation': '3-5 second',
                'system_integration': '8 components unified'
            },
            'forbidden_terms': [
                'MWRASP Quantum Defense System',
                '70.9ms detection latency',
                'Simulation only',
                'Multi-Wavelength Rapid-Aging Surveillance Platform',
                'quantum defense system only',
                'point solution'
            ],
            'deprecated_metrics': [
                '70.9ms',
                '100 milliseconds',
                'simulation-based',
                'prototype only'
            ]
        }
        
        # Validation Results Storage
        self.analysis_results = {}
        self.validation_history = []
        
    async def validate_all_documents(self, root_directory: str) -> Dict[str, DocumentAnalysis]:
        """Validate all documents in project against authority hierarchy"""
        self.logger.info(f"Starting authority hierarchy validation for {root_directory}")
        
        # Find all documents
        documents = self._discover_documents(root_directory)
        
        # Validate each document
        for doc_path in documents:
            try:
                analysis = await self._validate_document(doc_path)
                self.analysis_results[doc_path] = analysis
                
            except Exception as e:
                self.logger.error(f"Error validating {doc_path}: {e}")
                self.analysis_results[doc_path] = DocumentAnalysis(
                    file_path=doc_path,
                    status=DocumentStatus.NOT_ANALYZED,
                    violations=[],
                    compliance_score=0.0,
                    last_analyzed=datetime.now(),
                    recommendations=[f"Error during analysis: {e}"]
                )
                
        # Generate validation report
        await self._generate_validation_report()
        
        return self.analysis_results
        
    def _discover_documents(self, root_directory: str) -> List[str]:
        """Discover all relevant documents in project"""
        document_extensions = ['.md', '.txt', '.py', '.html', '.json']
        documents = []
        
        for root, dirs, files in os.walk(root_directory):
            # Skip certain directories
            if any(skip in root for skip in ['__pycache__', '.git', 'node_modules', 'OUTDATED_DOCUMENTS']):
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in document_extensions):
                    documents.append(os.path.join(root, file))
                    
        return documents
        
    async def _validate_document(self, file_path: str) -> DocumentAnalysis:
        """Validate individual document against authority hierarchy"""
        
        # Check if this is an authority reference document
        if self._is_authority_reference(file_path):
            return DocumentAnalysis(
                file_path=file_path,
                status=DocumentStatus.AUTHORITY_REFERENCE,
                violations=[],
                compliance_score=1.0,
                last_analyzed=datetime.now(),
                recommendations=["Authority reference document - no validation needed"]
            )
            
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Check for violations
            violations.extend(await self._check_system_description(lines, file_path))
            violations.extend(await self._check_performance_metrics(lines, file_path))
            violations.extend(await self._check_forbidden_terms(lines, file_path))
            violations.extend(await self._check_deprecated_metrics(lines, file_path))
            violations.extend(await self._check_messaging_consistency(lines, file_path))
            
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            violations.append(AuthorityViolation(
                severity=ViolationSeverity.HIGH,
                violation_type="file_access_error",
                line_number=0,
                content="File access error",
                correct_content="",
                explanation=f"Unable to read file: {e}"
            ))
            
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(violations)
        
        # Determine status
        if not violations:
            status = DocumentStatus.COMPLIANT
        else:
            status = DocumentStatus.VIOLATIONS_FOUND
            
        # Generate recommendations
        recommendations = self._generate_recommendations(violations, file_path)
        
        return DocumentAnalysis(
            file_path=file_path,
            status=status,
            violations=violations,
            compliance_score=compliance_score,
            last_analyzed=datetime.now(),
            recommendations=recommendations
        )
        
    def _is_authority_reference(self, file_path: str) -> bool:
        """Check if document is an authority reference"""
        file_name = os.path.basename(file_path)
        
        for tier in self.config['authority_sources'].values():
            for authority_file in tier:
                if authority_file in file_path or file_name == authority_file:
                    return True
                    
        return False
        
    async def _check_system_description(self, lines: List[str], file_path: str) -> List[AuthorityViolation]:
        """Check for mandatory system description compliance"""
        violations = []
        mandatory_desc = self.authority_rules['mandatory_system_description']
        
        for i, line in enumerate(lines):
            # Check for old system descriptions
            if 'MWRASP Quantum Defense System' in line and 'Complete Unified Defense System' not in line:
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.CRITICAL,
                    violation_type="incorrect_system_description",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content=line.replace('MWRASP Quantum Defense System', 'MWRASP Complete Unified Defense System'),
                    explanation="Must use authority hierarchy approved system description"
                ))
                
            if 'Multi-Wavelength Rapid-Aging Surveillance Platform' in line:
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.CRITICAL,
                    violation_type="obsolete_system_name",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="MWRASP Complete Unified Defense System",
                    explanation="Obsolete system name - must use current authority hierarchy description"
                ))
                
        return violations
        
    async def _check_performance_metrics(self, lines: List[str], file_path: str) -> List[AuthorityViolation]:
        """Check for authority hierarchy validated performance metrics"""
        violations = []
        
        for i, line in enumerate(lines):
            # Check for deprecated latency metrics
            if re.search(r'70\.9\s*ms', line, re.IGNORECASE):
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.HIGH,
                    violation_type="deprecated_metric",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="63-78ms agent coordination (demonstrated)",
                    explanation="Deprecated metric - must use authority hierarchy validated performance"
                ))
                
            # Check for incorrect behavioral auth metrics
            if re.search(r'50\s*ms.*authentication', line, re.IGNORECASE):
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.HIGH,
                    violation_type="incorrect_auth_metric",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="0.1ms behavioral authentication (500x faster than PKI)",
                    explanation="Incorrect authentication metric - must use validated 0.1ms figure"
                ))
                
            # Check for simulation-only references
            if re.search(r'simulation\s+only', line, re.IGNORECASE):
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.CRITICAL,
                    violation_type="simulation_only_reference",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="working system with validated performance",
                    explanation="Must not refer to system as simulation-only - working system exists"
                ))
                
        return violations
        
    async def _check_forbidden_terms(self, lines: List[str], file_path: str) -> List[AuthorityViolation]:
        """Check for forbidden/deprecated terms"""
        violations = []
        
        for i, line in enumerate(lines):
            for forbidden_term in self.authority_rules['forbidden_terms']:
                if forbidden_term.lower() in line.lower():
                    violations.append(AuthorityViolation(
                        severity=ViolationSeverity.MEDIUM,
                        violation_type="forbidden_term",
                        line_number=i + 1,
                        content=line.strip(),
                        correct_content=self._get_correct_term(forbidden_term),
                        explanation=f"Forbidden term '{forbidden_term}' violates authority hierarchy"
                    ))
                    
        return violations
        
    async def _check_deprecated_metrics(self, lines: List[str], file_path: str) -> List[AuthorityViolation]:
        """Check for deprecated performance metrics"""
        violations = []
        
        for i, line in enumerate(lines):
            for deprecated in self.authority_rules['deprecated_metrics']:
                if deprecated in line:
                    violations.append(AuthorityViolation(
                        severity=ViolationSeverity.HIGH,
                        violation_type="deprecated_performance_metric",
                        line_number=i + 1,
                        content=line.strip(),
                        correct_content=self._get_correct_metric(deprecated),
                        explanation=f"Deprecated metric '{deprecated}' - must use authority hierarchy validated metrics"
                    ))
                    
        return violations
        
    async def _check_messaging_consistency(self, lines: List[str], file_path: str) -> List[AuthorityViolation]:
        """Check for messaging consistency with authority hierarchy"""
        violations = []
        
        # Check for point solution references when should be unified platform
        for i, line in enumerate(lines):
            if 'point solution' in line.lower() and 'vs' not in line.lower() and 'against' not in line.lower():
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.MEDIUM,
                    violation_type="point_solution_messaging",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="unified platform",
                    explanation="MWRASP is unified platform, not point solution"
                ))
                
            # Check for quantum-only positioning
            if 'quantum defense' in line.lower() and 'unified' not in line.lower() and 'integrated' not in line.lower():
                violations.append(AuthorityViolation(
                    severity=ViolationSeverity.MEDIUM,
                    violation_type="quantum_only_positioning",
                    line_number=i + 1,
                    content=line.strip(),
                    correct_content="integrated quantum-financial-legal-tactical defense platform",
                    explanation="Must position as integrated platform, not quantum-only"
                ))
                
        return violations
        
    def _get_correct_term(self, forbidden_term: str) -> str:
        """Get correct term to replace forbidden term"""
        replacements = {
            'MWRASP Quantum Defense System': 'MWRASP Complete Unified Defense System',
            '70.9ms detection latency': '63-78ms agent coordination',
            'Simulation only': 'Working system with validated performance',
            'Multi-Wavelength Rapid-Aging Surveillance Platform': 'MWRASP Complete Unified Defense System',
            'quantum defense system only': 'integrated quantum-financial-legal-tactical defense platform',
            'point solution': 'unified platform'
        }
        
        return replacements.get(forbidden_term, 'Authority hierarchy compliant term')
        
    def _get_correct_metric(self, deprecated_metric: str) -> str:
        """Get correct metric to replace deprecated metric"""
        replacements = {
            '70.9ms': '63-78ms agent coordination',
            '100 milliseconds': '0.1ms behavioral authentication',
            'simulation-based': 'working system validation',
            'prototype only': 'operational system'
        }
        
        return replacements.get(deprecated_metric, 'Authority hierarchy validated metric')
        
    def _calculate_compliance_score(self, violations: List[AuthorityViolation]) -> float:
        """Calculate compliance score based on violations"""
        if not violations:
            return 1.0
            
        # Weight violations by severity
        severity_weights = {
            ViolationSeverity.CRITICAL: 0.4,
            ViolationSeverity.HIGH: 0.3,
            ViolationSeverity.MEDIUM: 0.2,
            ViolationSeverity.LOW: 0.1
        }
        
        total_penalty = 0.0
        for violation in violations:
            total_penalty += severity_weights[violation.severity]
            
        # Calculate score (0.0 to 1.0)
        compliance_score = max(0.0, 1.0 - (total_penalty / 10.0))
        
        return compliance_score
        
    def _generate_recommendations(self, violations: List[AuthorityViolation], file_path: str) -> List[str]:
        """Generate recommendations for fixing violations"""
        if not violations:
            return ["Document is fully compliant with authority hierarchy"]
            
        recommendations = []
        
        critical_count = len([v for v in violations if v.severity == ViolationSeverity.CRITICAL])
        if critical_count > 0:
            recommendations.append(f"URGENT: Fix {critical_count} critical violations that contradict working system")
            
        high_count = len([v for v in violations if v.severity == ViolationSeverity.HIGH])
        if high_count > 0:
            recommendations.append(f"HIGH PRIORITY: Update {high_count} deprecated metrics to authority hierarchy standards")
            
        medium_count = len([v for v in violations if v.severity == ViolationSeverity.MEDIUM])
        if medium_count > 0:
            recommendations.append(f"MEDIUM PRIORITY: Align {medium_count} messaging inconsistencies")
            
        # Specific recommendations
        violation_types = {v.violation_type for v in violations}
        
        if 'incorrect_system_description' in violation_types:
            recommendations.append("Update system description to: 'MWRASP Complete Unified Defense System'")
            
        if 'deprecated_metric' in violation_types:
            recommendations.append("Replace all deprecated metrics with authority hierarchy validated figures")
            
        if 'simulation_only_reference' in violation_types:
            recommendations.append("Emphasize working system status - remove simulation-only references")
            
        recommendations.append(f"Review master reference documents for compliance guidance")
        
        return recommendations
        
    async def _generate_validation_report(self):
        """Generate comprehensive validation report"""
        report = {
            'validation_timestamp': datetime.now().isoformat(),
            'total_documents_analyzed': len(self.analysis_results),
            'compliance_summary': {
                'compliant': len([r for r in self.analysis_results.values() if r.status == DocumentStatus.COMPLIANT]),
                'violations_found': len([r for r in self.analysis_results.values() if r.status == DocumentStatus.VIOLATIONS_FOUND]),
                'not_analyzed': len([r for r in self.analysis_results.values() if r.status == DocumentStatus.NOT_ANALYZED]),
                'authority_references': len([r for r in self.analysis_results.values() if r.status == DocumentStatus.AUTHORITY_REFERENCE])
            },
            'violation_summary': {},
            'priority_actions': [],
            'compliance_recommendations': []
        }
        
        # Count violations by severity
        all_violations = []
        for analysis in self.analysis_results.values():
            all_violations.extend(analysis.violations)
            
        for severity in ViolationSeverity:
            report['violation_summary'][severity.value] = len([v for v in all_violations if v.severity == severity])
            
        # Generate priority actions
        critical_docs = [path for path, analysis in self.analysis_results.items() 
                        if any(v.severity == ViolationSeverity.CRITICAL for v in analysis.violations)]
        
        if critical_docs:
            report['priority_actions'].append(f"IMMEDIATE: Fix critical violations in {len(critical_docs)} documents")
            
        high_priority_docs = [path for path, analysis in self.analysis_results.items() 
                             if any(v.severity == ViolationSeverity.HIGH for v in analysis.violations)]
        
        if high_priority_docs:
            report['priority_actions'].append(f"HIGH: Update deprecated metrics in {len(high_priority_docs)} documents")
            
        # Save report
        report_path = 'C:\\Users\\User\\MWRASP-Quantum-Defense\\AUTHORITY_HIERARCHY_VALIDATION_REPORT.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        self.logger.info(f"Validation report saved to {report_path}")
        
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get current compliance status"""
        if not self.analysis_results:
            return {"status": "no_analysis_performed"}
            
        total_docs = len(self.analysis_results)
        compliant_docs = len([r for r in self.analysis_results.values() 
                             if r.status == DocumentStatus.COMPLIANT])
        
        compliance_rate = compliant_docs / total_docs if total_docs > 0 else 0
        
        return {
            'total_documents': total_docs,
            'compliant_documents': compliant_docs,
            'compliance_rate': compliance_rate,
            'violations_requiring_attention': len([r for r in self.analysis_results.values() 
                                                  if r.status == DocumentStatus.VIOLATIONS_FOUND]),
            'last_validation': max([r.last_analyzed for r in self.analysis_results.values()]) if self.analysis_results else None
        }
        
    def get_violation_details(self, severity: Optional[ViolationSeverity] = None) -> List[Dict[str, Any]]:
        """Get detailed violation information"""
        violation_details = []
        
        for file_path, analysis in self.analysis_results.items():
            for violation in analysis.violations:
                if severity is None or violation.severity == severity:
                    violation_details.append({
                        'file_path': file_path,
                        'severity': violation.severity.value,
                        'violation_type': violation.violation_type,
                        'line_number': violation.line_number,
                        'content': violation.content,
                        'correct_content': violation.correct_content,
                        'explanation': violation.explanation
                    })
                    
        return violation_details
        
    async def auto_fix_violations(self, severity_threshold: ViolationSeverity = ViolationSeverity.HIGH) -> Dict[str, int]:
        """Automatically fix violations above specified severity threshold"""
        fixes_applied = {'successful': 0, 'failed': 0, 'skipped': 0}
        
        for file_path, analysis in self.analysis_results.items():
            if analysis.status != DocumentStatus.VIOLATIONS_FOUND:
                continue
                
            # Get violations to fix
            violations_to_fix = [v for v in analysis.violations 
                               if v.severity.value <= severity_threshold.value]
            
            if not violations_to_fix:
                fixes_applied['skipped'] += 1
                continue
                
            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Apply fixes (from bottom to top to maintain line numbers)
                violations_to_fix.sort(key=lambda v: v.line_number, reverse=True)
                
                for violation in violations_to_fix:
                    if violation.line_number <= len(lines):
                        lines[violation.line_number - 1] = violation.correct_content + '\n'
                        
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                    
                fixes_applied['successful'] += 1
                self.logger.info(f"Auto-fixed violations in {file_path}")
                
            except Exception as e:
                fixes_applied['failed'] += 1
                self.logger.error(f"Failed to auto-fix {file_path}: {e}")
                
        return fixes_applied

# Global instance
authority_validator = AuthorityHierarchyValidator()
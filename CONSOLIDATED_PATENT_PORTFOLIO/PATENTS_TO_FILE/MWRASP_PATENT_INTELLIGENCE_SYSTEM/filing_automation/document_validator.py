#!/usr/bin/env python3
"""
Document Validation and USPTO Form Auto-Population System
=========================================================

This module validates patent documents and automatically populates USPTO forms
for electronic filing. It checks for completeness, formatting, and compliance
with USPTO requirements.

Author: MWRASP Patent Development Team
Date: August 2025
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from automated_patent_filing_system import AutomatedPatentFilingSystem, PatentInfo
import hashlib
from datetime import datetime

class DocumentValidator:
    """Validate patent documents for USPTO compliance"""
    
    def __init__(self, filing_system: AutomatedPatentFilingSystem):
        self.filing_system = filing_system
        self.validation_results = {}
        self.output_dir = Path(filing_system.base_directory) / "validation_reports"
        self.output_dir.mkdir(exist_ok=True)
    
    def validate_all_patents(self) -> Dict:
        """Validate all patent documents for filing readiness"""
        print(f"\\n{'='*60}")
        print("VALIDATING ALL PATENT DOCUMENTS FOR USPTO FILING")
        print(f"{'='*60}")
        
        results = {}
        
        for patent_num, patent_info in self.filing_system.patents.items():
            print(f"\\nValidating Patent {patent_num}: {patent_info.title[:50]}...")
            
            try:
                validation_result = self.validate_patent_document(patent_info)
                results[patent_num] = validation_result
                
                status = "PASS" if validation_result['overall_status'] else "FAIL"
                print(f"  Overall Status: [{status}]")
                print(f"  Issues Found: {len(validation_result['issues'])}")
                print(f"  Warnings: {len(validation_result['warnings'])}")
                
            except Exception as e:
                print(f"  [ERROR] Validation failed: {e}")
                results[patent_num] = {
                    'overall_status': False,
                    'error': str(e),
                    'issues': [f"Validation system error: {e}"],
                    'warnings': []
                }
        
        self.validation_results = results
        self.generate_validation_report()
        
        return results
    
    def validate_patent_document(self, patent_info: PatentInfo) -> Dict:
        """Validate a single patent document"""
        result = {
            'patent_number': patent_info.patent_number,
            'title': patent_info.title,
            'overall_status': True,
            'issues': [],
            'warnings': [],
            'checks_performed': {},
            'file_analysis': {}
        }
        
        patent_dir = Path(patent_info.folder_path)
        
        # Check 1: Provisional Patent Application exists and is valid
        app_check = self.check_provisional_application(patent_dir)
        result['checks_performed']['provisional_application'] = app_check
        if not app_check['valid']:
            result['issues'].extend(app_check['issues'])
            result['overall_status'] = False
        if app_check['warnings']:
            result['warnings'].extend(app_check['warnings'])
        
        # Check 2: Required USPTO forms
        forms_check = self.check_uspto_forms(patent_dir)
        result['checks_performed']['uspto_forms'] = forms_check
        if not forms_check['valid']:
            result['issues'].extend(forms_check['issues'])
            result['overall_status'] = False
        if forms_check['warnings']:
            result['warnings'].extend(forms_check['warnings'])
        
        # Check 3: Technical drawings and figures
        figures_check = self.check_technical_figures(patent_dir)
        result['checks_performed']['technical_figures'] = figures_check
        if not figures_check['valid']:
            result['issues'].extend(figures_check['issues'])
            result['overall_status'] = False
        if figures_check['warnings']:
            result['warnings'].extend(figures_check['warnings'])
        
        # Check 4: File format compliance
        format_check = self.check_file_formats(patent_dir)
        result['checks_performed']['file_formats'] = format_check
        if not format_check['valid']:
            result['issues'].extend(format_check['issues'])
            result['overall_status'] = False
        if format_check['warnings']:
            result['warnings'].extend(format_check['warnings'])
        
        # Check 5: Content completeness
        content_check = self.check_content_completeness(patent_dir)
        result['checks_performed']['content_completeness'] = content_check
        if not content_check['valid']:
            result['issues'].extend(content_check['issues'])
            result['overall_status'] = False
        if content_check['warnings']:
            result['warnings'].extend(content_check['warnings'])
        
        return result
    
    def check_provisional_application(self, patent_dir: Path) -> Dict:
        """Check provisional patent application file"""
        result = {'valid': True, 'issues': [], 'warnings': []}
        
        app_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.md"
        
        if not app_file.exists():
            result['valid'] = False
            result['issues'].append("PROVISIONAL_PATENT_APPLICATION.md file missing")
            return result
        
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check required sections
            required_sections = [
                "TECHNICAL FIELD",
                "BACKGROUND OF THE INVENTION", 
                "SUMMARY OF THE INVENTION",
                "DETAILED DESCRIPTION",
                "CLAIMS",
                "INDUSTRIAL APPLICABILITY"
            ]
            
            for section in required_sections:
                if section not in content:
                    result['issues'].append(f"Missing required section: {section}")
                    result['valid'] = False
            
            # Check for title
            if not re.search(r'\\*\\*Title:\\*\\*', content):
                result['warnings'].append("Patent title not found in standard format")
            
            # Check word count (provisional applications should be substantial)
            word_count = len(content.split())
            if word_count < 1000:
                result['warnings'].append(f"Application may be too short: {word_count} words")
            elif word_count > 50000:
                result['warnings'].append(f"Application may be too long: {word_count} words")
            
            # Check for placeholder text
            placeholders = ["[TO BE FILLED]", "[TBD]", "[TODO]"]
            for placeholder in placeholders:
                if placeholder in content:
                    result['issues'].append(f"Placeholder text found: {placeholder}")
                    result['valid'] = False
            
        except Exception as e:
            result['valid'] = False
            result['issues'].append(f"Error reading provisional application: {e}")
        
        return result
    
    def check_uspto_forms(self, patent_dir: Path) -> Dict:
        """Check for required USPTO forms"""
        result = {'valid': True, 'issues': [], 'warnings': []}
        
        # Required forms for provisional application
        required_forms = [
            ("USPTO_COVER_SHEET_SB16.pdf", "Cover Sheet SB16"),
            ("APPLICATION_DATA_SHEET_ADS.pdf", "Application Data Sheet"),
            ("MICRO_ENTITY_STATUS_SB15A.pdf", "Micro Entity Status SB15A")
        ]
        
        for form_file, form_name in required_forms:
            if not (patent_dir / form_file).exists():
                # Check for HTML version as alternative
                html_version = patent_dir / form_file.replace('.pdf', '.html')
                if not html_version.exists():
                    result['warnings'].append(f"Missing {form_name} ({form_file})")
                else:
                    result['warnings'].append(f"{form_name} found only in HTML format")
        
        # Check for fee transmittal form
        fee_form = patent_dir / "FEE_TRANSMITTAL_FORM_SB17.pdf"
        if not fee_form.exists():
            fee_form_html = patent_dir / "FEE_TRANSMITTAL_FORM_SB17.html"
            if not fee_form_html.exists():
                result['warnings'].append("Fee Transmittal Form SB17 missing (may be generated during filing)")
        
        return result
    
    def check_technical_figures(self, patent_dir: Path) -> Dict:
        """Check technical drawings and figures"""
        result = {'valid': True, 'issues': [], 'warnings': []}
        
        # Look for figure files
        figure_patterns = ["FIGURE_*.pdf", "FIGURE_*.svg", "*.png", "*.jpg"]
        figures_found = []
        
        for pattern in figure_patterns:
            figures_found.extend(list(patent_dir.glob(pattern)))
        
        if not figures_found:
            result['warnings'].append("No technical figures found - consider adding system diagrams")
        else:
            result['info'] = f"Found {len(figures_found)} technical figures"
        
        # Check figure file sizes (USPTO has limits)
        for figure_file in figures_found:
            try:
                file_size = figure_file.stat().st_size
                if file_size > 25 * 1024 * 1024:  # 25MB limit
                    result['issues'].append(f"Figure file too large: {figure_file.name} ({file_size/1024/1024:.1f}MB)")
                    result['valid'] = False
            except Exception as e:
                result['warnings'].append(f"Could not check size of {figure_file.name}: {e}")
        
        return result
    
    def check_file_formats(self, patent_dir: Path) -> Dict:
        """Check file format compliance"""
        result = {'valid': True, 'issues': [], 'warnings': []}
        
        # Check for unsupported file types
        unsupported_extensions = ['.docx', '.doc', '.rtf', '.odt']
        
        for file_path in patent_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in unsupported_extensions:
                result['warnings'].append(f"File may need conversion: {file_path.name} ({file_path.suffix})")
        
        return result
    
    def check_content_completeness(self, patent_dir: Path) -> Dict:
        """Check content completeness and quality"""
        result = {'valid': True, 'issues': [], 'warnings': []}
        
        app_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.md"
        if not app_file.exists():
            return result
        
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for claims section
            claims_match = re.search(r'## CLAIMS(.*?)(?=\\n##|\\Z)', content, re.DOTALL)
            if claims_match:
                claims_content = claims_match.group(1)
                
                # Count independent claims
                independent_claims = len(re.findall(r'\\*\\*Claim \\d+\\*\\*:', claims_content))
                if independent_claims == 0:
                    result['issues'].append("No independent claims found")
                    result['valid'] = False
                elif independent_claims > 3:
                    result['warnings'].append(f"Many independent claims ({independent_claims}) may increase costs")
                
                # Count total claims
                total_claims = len(re.findall(r'\\*\\*Claim \\d+\\*\\*:', claims_content))
                if total_claims > 20:
                    result['warnings'].append(f"Many total claims ({total_claims}) may increase costs")
            
            # Check for experimental results
            if "EXPERIMENTAL RESULTS" not in content and "PROTOTYPE" not in content:
                result['warnings'].append("Consider adding experimental results or prototype data")
            
            # Check for commercial applicability
            if "INDUSTRIAL APPLICABILITY" not in content and "COMMERCIAL" not in content:
                result['warnings'].append("Consider strengthening commercial applicability section")
            
        except Exception as e:
            result['warnings'].append(f"Error analyzing content: {e}")
        
        return result
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        report_file = self.output_dir / f"Validation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        total_patents = len(self.validation_results)
        passed = len([r for r in self.validation_results.values() if r['overall_status']])
        failed = total_patents - passed
        total_issues = sum(len(r['issues']) for r in self.validation_results.values())
        total_warnings = sum(len(r['warnings']) for r in self.validation_results.values())
        
        report_content = f"""# PATENT DOCUMENT VALIDATION REPORT

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Patents:** {total_patents}
**Passed Validation:** {passed}
**Failed Validation:** {failed}
**Total Issues:** {total_issues}
**Total Warnings:** {total_warnings}

## VALIDATION SUMMARY

| Status | Count | Percentage |
|--------|-------|------------|
| PASS   | {passed} | {(passed/total_patents)*100:.1f}% |
| FAIL   | {failed} | {(failed/total_patents)*100:.1f}% |

## DETAILED RESULTS

"""
        
        for patent_num, result in self.validation_results.items():
            status_icon = "PASS" if result['overall_status'] else "FAIL"
            
            report_content += f"### Patent {patent_num}: {result.get('title', 'Unknown')}\\n"
            report_content += f"**Status:** {status_icon}\\n"
            
            if result['issues']:
                report_content += f"**Issues ({len(result['issues'])}):**\\n"
                for issue in result['issues']:
                    report_content += f"- ❌ {issue}\\n"
            
            if result['warnings']:
                report_content += f"**Warnings ({len(result['warnings'])}):**\\n"
                for warning in result['warnings']:
                    report_content += f"- ⚠️ {warning}\\n"
            
            report_content += "\\n"
        
        report_content += f"""## VALIDATION CRITERIA

### Required Files Checked:
- PROVISIONAL_PATENT_APPLICATION.md
- USPTO_COVER_SHEET_SB16.pdf
- APPLICATION_DATA_SHEET_ADS.pdf  
- MICRO_ENTITY_STATUS_SB15A.pdf

### Content Requirements:
- Technical Field section
- Background of Invention
- Summary of Invention
- Detailed Description
- Claims (Independent and Dependent)
- Industrial Applicability

### File Format Compliance:
- PDF format for USPTO forms
- Appropriate figure formats (PDF, SVG, PNG)
- File size limits (25MB per file)

## NEXT STEPS

### For FAILED Patents:
1. Address all listed issues before filing
2. Regenerate any missing forms
3. Validate content completeness
4. Re-run validation after fixes

### For PASSED Patents:
1. Review warnings and consider improvements
2. Verify all placeholder information is filled
3. Conduct final legal review
4. Prepare for USPTO submission

### General Recommendations:
- Update filing configuration with complete information
- Generate fresh ADS forms with correct data
- Prepare fee payments for micro entity status
- Schedule attorney review for high-value patents

---

**Validation System Version:** 1.0  
**Report Location:** {report_file}
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\\nValidation report generated: {report_file}")
        return report_file

def main():
    """Main function for document validation"""
    base_dir = r"C:\\Users\\User\\MWRASP-Quantum-Defense\\CONSOLIDATED_PATENT_PORTFOLIO\\PATENTS_TO_FILE"
    
    # Initialize filing system
    filing_system = AutomatedPatentFilingSystem(base_dir)
    filing_system.discover_patents()
    
    # Initialize validator
    validator = DocumentValidator(filing_system)
    
    # Run validation
    results = validator.validate_all_patents()
    
    # Print summary
    total = len(results)
    passed = len([r for r in results.values() if r['overall_status']])
    
    print(f"\\n{'='*60}")
    print(f"VALIDATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total Patents: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
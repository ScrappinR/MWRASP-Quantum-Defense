#!/usr/bin/env python3
"""
MWRASP Authority Hierarchy Automated Validation Runner
Execute continuous compliance checking against established authority hierarchy
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.authority_hierarchy_validator import (
    authority_validator, 
    ViolationSeverity, 
    DocumentStatus
)

async def run_full_validation():
    """Run complete authority hierarchy validation"""
    print("🔍 MWRASP Authority Hierarchy Validation - STARTING")
    print("=" * 70)
    
    # Get project root
    project_root = Path(__file__).parent
    
    print(f"📁 Analyzing project: {project_root}")
    print(f"⏰ Started at: {datetime.now()}")
    print()
    
    # Run validation
    try:
        results = await authority_validator.validate_all_documents(str(project_root))
        
        # Print summary
        print("📊 VALIDATION SUMMARY")
        print("-" * 40)
        
        status_counts = {}
        for status in DocumentStatus:
            count = len([r for r in results.values() if r.status == status])
            status_counts[status.value] = count
            
        print(f"📄 Total Documents: {len(results)}")
        print(f"✅ Compliant: {status_counts.get('compliant', 0)}")
        print(f"⚠️  Violations Found: {status_counts.get('violations_found', 0)}")
        print(f"🔒 Authority References: {status_counts.get('authority_reference', 0)}")
        print(f"❓ Not Analyzed: {status_counts.get('not_analyzed', 0)}")
        print()
        
        # Violation severity breakdown
        all_violations = []
        for analysis in results.values():
            all_violations.extend(analysis.violations)
            
        if all_violations:
            print("🚨 VIOLATION SEVERITY BREAKDOWN")
            print("-" * 40)
            for severity in ViolationSeverity:
                count = len([v for v in all_violations if v.severity == severity])
                if count > 0:
                    icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "⚪"}.get(severity.value, "⚫")
                    print(f"{icon} {severity.value.upper()}: {count} violations")
            print()
            
        # Top violation files
        violation_files = [(path, len(analysis.violations)) for path, analysis in results.items() 
                          if analysis.violations]
        violation_files.sort(key=lambda x: x[1], reverse=True)
        
        if violation_files:
            print("📋 TOP VIOLATION FILES")
            print("-" * 40)
            for file_path, violation_count in violation_files[:10]:
                relative_path = Path(file_path).relative_to(project_root)
                print(f"⚠️  {relative_path}: {violation_count} violations")
            print()
            
        # Critical violations requiring immediate attention
        critical_violations = authority_validator.get_violation_details(ViolationSeverity.CRITICAL)
        if critical_violations:
            print("🔴 CRITICAL VIOLATIONS - IMMEDIATE ACTION REQUIRED")
            print("-" * 60)
            for violation in critical_violations[:5]:  # Show first 5
                relative_path = Path(violation['file_path']).relative_to(project_root)
                print(f"File: {relative_path}")
                print(f"Line: {violation['line_number']}")
                print(f"Issue: {violation['explanation']}")
                print(f"Current: {violation['content'][:100]}...")
                print(f"Should be: {violation['correct_content'][:100]}...")
                print("-" * 30)
            print()
            
        # Compliance status
        compliance_status = authority_validator.get_compliance_status()
        compliance_rate = compliance_status['compliance_rate'] * 100
        
        print("📈 COMPLIANCE METRICS")
        print("-" * 40)
        print(f"📊 Overall Compliance Rate: {compliance_rate:.1f}%")
        print(f"✅ Compliant Documents: {compliance_status['compliant_documents']}")
        print(f"⚠️  Documents Needing Attention: {compliance_status['violations_requiring_attention']}")
        print()
        
        # Recommendations
        print("💡 RECOMMENDED ACTIONS")
        print("-" * 40)
        if critical_violations:
            print("🔴 URGENT: Fix critical violations that contradict working system")
        if len([v for v in all_violations if v.severity == ViolationSeverity.HIGH]) > 0:
            print("🟠 HIGH: Update deprecated metrics to authority hierarchy standards")
        if len([v for v in all_violations if v.severity == ViolationSeverity.MEDIUM]) > 0:
            print("🟡 MEDIUM: Align messaging inconsistencies")
            
        print("📚 Review master reference documents for guidance:")
        print("   - MWRASP_DARPA_Whitepaper_UPDATED.md")
        print("   - 17_COMPETITIVE_ANALYSIS_UPDATED.md")
        print("   - PARADIGM_SHIFT_NARRATIVE_UPDATED.md")
        print()
        
        print("✅ VALIDATION COMPLETE")
        print(f"📄 Report saved: AUTHORITY_HIERARCHY_VALIDATION_REPORT.json")
        print(f"⏰ Completed at: {datetime.now()}")
        
        return compliance_rate
        
    except Exception as e:
        print(f"❌ ERROR: Validation failed: {e}")
        return 0.0

async def run_quick_check():
    """Run quick compliance check on key documents"""
    print("⚡ QUICK AUTHORITY COMPLIANCE CHECK")
    print("=" * 50)
    
    # Key documents to check
    key_documents = [
        "02_FUNDING_MATERIALS/DARPA/DARPA_PITCH_REPORT.md",
        "01_EXECUTIVE_SUMMARY/PROJECT_OVERVIEW.md",
        "MWRASP_COMPLETE_SYSTEM_SUMMARY.md",
        "08_BUSINESS_DEVELOPMENT/Marketing/ELEVATOR_PITCHES.md",
        "02_FUNDING_MATERIALS/Private_Investment/05_INVESTMENT_PROSPECTUS_COMPLETE.md"
    ]
    
    project_root = Path(__file__).parent
    compliant_count = 0
    
    for doc_path in key_documents:
        full_path = project_root / doc_path
        if full_path.exists():
            try:
                analysis = await authority_validator._validate_document(str(full_path))
                status_icon = "✅" if analysis.status == DocumentStatus.COMPLIANT else "⚠️"
                violation_count = len(analysis.violations)
                
                print(f"{status_icon} {doc_path}")
                if violation_count > 0:
                    print(f"   {violation_count} violations found")
                else:
                    compliant_count += 1
                    
            except Exception as e:
                print(f"❌ {doc_path} - Error: {e}")
        else:
            print(f"❓ {doc_path} - File not found")
            
    print()
    print(f"📊 Quick Check Result: {compliant_count}/{len(key_documents)} key documents compliant")
    
async def auto_fix_high_priority():
    """Automatically fix high priority violations"""
    print("🔧 AUTO-FIX HIGH PRIORITY VIOLATIONS")
    print("=" * 50)
    
    # Run validation first
    project_root = Path(__file__).parent
    await authority_validator.validate_all_documents(str(project_root))
    
    # Auto-fix violations
    print("⚙️  Applying automatic fixes for HIGH and CRITICAL violations...")
    
    fixes = await authority_validator.auto_fix_violations(ViolationSeverity.HIGH)
    
    print("📊 AUTO-FIX RESULTS:")
    print(f"✅ Successfully fixed: {fixes['successful']} documents")
    print(f"❌ Failed to fix: {fixes['failed']} documents") 
    print(f"⏭️  Skipped: {fixes['skipped']} documents")
    
    if fixes['successful'] > 0:
        print("\n💡 Recommendation: Re-run validation to confirm fixes")
        
def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            asyncio.run(run_quick_check())
        elif command == "autofix":
            asyncio.run(auto_fix_high_priority())
        elif command == "full":
            asyncio.run(run_full_validation())
        else:
            print("❓ Unknown command. Use: full, quick, or autofix")
    else:
        # Default: run full validation
        asyncio.run(run_full_validation())

if __name__ == "__main__":
    main()
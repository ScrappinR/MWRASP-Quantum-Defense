#!/usr/bin/env python3
"""
MWRASP Document Governance Dashboard
Real-time monitoring and management of authority hierarchy compliance
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.authority_hierarchy_validator import (
    authority_validator, 
    ViolationSeverity, 
    DocumentStatus
)

class GovernanceDashboard:
    """Real-time governance dashboard for MWRASP documentation compliance"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.last_validation = None
        self.compliance_history = []
        
    async def display_dashboard(self):
        """Display real-time governance dashboard"""
        print("*** MWRASP DOCUMENT GOVERNANCE DASHBOARD ***")
        print("=" * 80)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Project: {self.project_root.name}")
        print()
        
        # Run validation
        print("[*] Running authority hierarchy validation...")
        results = await authority_validator.validate_all_documents(str(self.project_root))
        
        # Calculate metrics
        total_docs = len(results)
        compliant_docs = len([r for r in results.values() if r.status == DocumentStatus.COMPLIANT])
        authority_docs = len([r for r in results.values() if r.status == DocumentStatus.AUTHORITY_REFERENCE])
        violation_docs = len([r for r in results.values() if r.status == DocumentStatus.VIOLATIONS_FOUND])
        
        compliance_rate = (compliant_docs / (total_docs - authority_docs)) * 100 if (total_docs - authority_docs) > 0 else 100
        
        # Store history
        self.compliance_history.append({
            'timestamp': datetime.now(),
            'compliance_rate': compliance_rate,
            'total_docs': total_docs,
            'compliant_docs': compliant_docs,
            'violation_docs': violation_docs
        })
        
        # Display main metrics
        print("*** AUTHORITY HIERARCHY COMPLIANCE STATUS ***")
        print("-" * 50)
        
        # Compliance rate with color coding
        if compliance_rate >= 95:
            status_icon = "[EXCELLENT]"
            status_text = "EXCELLENT"
        elif compliance_rate >= 85:
            status_icon = "[GOOD]"
            status_text = "GOOD"
        elif compliance_rate >= 70:
            status_icon = "[NEEDS ATTENTION]"
            status_text = "NEEDS ATTENTION"
        else:
            status_icon = "[CRITICAL]"
            status_text = "CRITICAL"
            
        print(f"{status_icon} Overall Compliance: {compliance_rate:.1f}% ({status_text})")
        print(f"Total Documents: {total_docs}")
        print(f"[OK] Fully Compliant: {compliant_docs}")
        print(f"[!] With Violations: {violation_docs}")
        print(f"[AUTH] Authority References: {authority_docs}")
        print()
        
        # Violation severity breakdown
        all_violations = []
        for analysis in results.values():
            all_violations.extend(analysis.violations)
            
        if all_violations:
            print("🚨 VIOLATION SEVERITY BREAKDOWN")
            print("-" * 50)
            
            severity_counts = {}
            for severity in ViolationSeverity:
                count = len([v for v in all_violations if v.severity == severity])
                severity_counts[severity] = count
                
            # Display with icons
            severity_icons = {
                ViolationSeverity.CRITICAL: "🔴",
                ViolationSeverity.HIGH: "🟠", 
                ViolationSeverity.MEDIUM: "🟡",
                ViolationSeverity.LOW: "⚪"
            }
            
            for severity, count in severity_counts.items():
                if count > 0:
                    icon = severity_icons[severity]
                    urgency = "URGENT" if severity == ViolationSeverity.CRITICAL else severity.value.upper()
                    print(f"{icon} {urgency}: {count} violations")
                    
            print()
            
        # Authority hierarchy status
        print("🏆 AUTHORITY HIERARCHY STATUS")
        print("-" * 50)
        
        tier1_files = [
            'MWRASP_COMPLETE_UNIFIED_SYSTEM.py',
            'MWRASP_COMPLETE_SYSTEM_SUMMARY.md', 
            '01_EXECUTIVE_SUMMARY/PROJECT_OVERVIEW.md'
        ]
        
        tier2_files = [
            'MWRASP_DARPA_Whitepaper_UPDATED.md',
            '17_COMPETITIVE_ANALYSIS_UPDATED.md',
            'PARADIGM_SHIFT_NARRATIVE_UPDATED.md',
            'ACQUISITION_READY_REPORT.md'
        ]
        
        print("Tier 1 - Ultimate Authority:")
        for file_name in tier1_files:
            exists = any(file_name in path for path in results.keys())
            icon = "✅" if exists else "❌"
            print(f"  {icon} {file_name}")
            
        print()
        print("Tier 2 - Domain Masters:")
        for file_name in tier2_files:
            exists = any(file_name in path for path in results.keys())
            icon = "✅" if exists else "❌"
            print(f"  {icon} {file_name}")
            
        print()
        
        # Recent trends (if we have history)
        if len(self.compliance_history) > 1:
            print("📈 COMPLIANCE TRENDS")
            print("-" * 50)
            
            prev_rate = self.compliance_history[-2]['compliance_rate']
            current_rate = self.compliance_history[-1]['compliance_rate']
            trend = current_rate - prev_rate
            
            trend_icon = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
            print(f"{trend_icon} Compliance Trend: {trend:+.1f}% change")
            
            prev_violations = self.compliance_history[-2]['violation_docs']
            current_violations = self.compliance_history[-1]['violation_docs']
            violation_trend = current_violations - prev_violations
            
            violation_icon = "📉" if violation_trend < 0 else "📈" if violation_trend > 0 else "➡️"
            print(f"{violation_icon} Violation Trend: {violation_trend:+d} documents")
            print()
            
        # Top priority actions
        critical_violations = [v for v in all_violations if v.severity == ViolationSeverity.CRITICAL]
        high_violations = [v for v in all_violations if v.severity == ViolationSeverity.HIGH]
        
        if critical_violations or high_violations:
            print("🎯 PRIORITY ACTIONS REQUIRED")
            print("-" * 50)
            
            if critical_violations:
                print(f"🔴 URGENT: {len(critical_violations)} critical violations require immediate attention")
                print("   These contradict the working system and must be fixed within 24 hours")
                
            if high_violations:
                print(f"🟠 HIGH: {len(high_violations)} deprecated metrics need updating")
                print("   Update to authority hierarchy validated performance figures")
                
            print()
            print("💡 Quick Fix Commands:")
            print("   python run_authority_validation.py autofix  # Auto-fix high priority")
            print("   python run_authority_validation.py full     # Complete validation")
            print()
            
        # System health
        print("💚 GOVERNANCE SYSTEM HEALTH")
        print("-" * 50)
        
        validator_status = "✅ OPERATIONAL" if hasattr(authority_validator, 'authority_rules') else "❌ ERROR"
        print(f"🤖 Authority Validator: {validator_status}")
        
        automation_status = "✅ ACTIVE" if Path(self.project_root / "run_authority_validation.py").exists() else "❌ MISSING"
        print(f"⚙️  Automated Validation: {automation_status}")
        
        governance_status = "✅ ESTABLISHED" if Path(self.project_root / "DOCUMENT_GOVERNANCE_FRAMEWORK.md").exists() else "❌ MISSING"
        print(f"📋 Governance Framework: {governance_status}")
        
        outdated_folder = "✅ ORGANIZED" if Path(self.project_root / "OUTDATED_DOCUMENTS").exists() else "❌ MISSING"
        print(f"📁 Document Organization: {outdated_folder}")
        
        print()
        
        # Quick actions menu
        print("⚡ QUICK ACTIONS")
        print("-" * 50)
        print("1. Run full validation      : python run_authority_validation.py full")
        print("2. Quick compliance check   : python run_authority_validation.py quick") 
        print("3. Auto-fix violations      : python run_authority_validation.py autofix")
        print("4. View detailed violations : python -c 'import json; print(json.dumps(results, indent=2))'")
        print("5. Generate compliance report: [Automatic - check AUTHORITY_HIERARCHY_VALIDATION_REPORT.json]")
        
        print()
        print("🔄 Dashboard refresh: Re-run this script for updated metrics")
        print("=" * 80)
        
        return {
            'compliance_rate': compliance_rate,
            'total_violations': len(all_violations),
            'critical_violations': len(critical_violations),
            'status': status_text
        }
        
    async def run_continuous_monitoring(self, interval_minutes: int = 60):
        """Run continuous monitoring with specified interval"""
        print(f"🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print("\n" + "="*80)
                print(f"🔄 AUTOMATED GOVERNANCE CHECK - {datetime.now()}")
                print("="*80)
                
                dashboard_result = await self.display_dashboard()
                
                # Alert on critical issues
                if dashboard_result['critical_violations'] > 0:
                    print(f"🚨 ALERT: {dashboard_result['critical_violations']} critical violations detected!")
                    
                if dashboard_result['compliance_rate'] < 85:
                    print(f"⚠️  WARNING: Compliance rate ({dashboard_result['compliance_rate']:.1f}%) below target (85%)")
                    
                print(f"\n⏰ Next check in {interval_minutes} minutes...")
                await asyncio.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n✋ Monitoring stopped by user")
            print("Final governance status summary available above")

async def main():
    """Main entry point"""
    dashboard = GovernanceDashboard()
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "monitor":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            await dashboard.run_continuous_monitoring(interval)
        else:
            print("Usage: python governance_dashboard.py [monitor] [interval_minutes]")
    else:
        # Single dashboard display
        await dashboard.display_dashboard()

if __name__ == "__main__":
    asyncio.run(main())
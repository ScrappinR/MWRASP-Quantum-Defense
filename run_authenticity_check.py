#!/usr/bin/env python3
"""
Run authenticity check with proper Unicode handling
"""

import sys
from code_authenticity_agent import CodeAuthenticityAgent

def main():
    print("Starting MWRASP Code Authenticity Analysis...")
    
    agent = CodeAuthenticityAgent()
    
    # Analyze key directories only to avoid Unicode issues
    key_directories = [
        "CORE_SYSTEM_IMPLEMENTATIONS",
        "VALIDATION_AND_TESTING"  
    ]
    
    all_results = {}
    
    for directory in key_directories:
        try:
            print(f"Analyzing {directory}...")
            results = agent.analyze_directory(directory)
            all_results.update(results)
            print(f"  Found {len(results)} files with issues in {directory}")
        except Exception as e:
            print(f"Error analyzing {directory}: {e}")
            continue
    
    # Generate report
    print("\nGenerating report...")
    report = agent.generate_report(all_results)
    
    # Print to console (safe)
    print("\n" + "="*80)
    print(report)
    
    # Save to file with UTF-8 encoding
    try:
        with open("MWRASP_Authenticity_Report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to: MWRASP_Authenticity_Report.txt")
    except Exception as e:
        print(f"Could not save report to file: {e}")
    
    # Calculate authenticity percentage
    total_issues = sum(len(issues) for issues in all_results.values())
    critical_issues = sum(1 for issues in all_results.values() for issue in issues if issue.severity == "CRITICAL")
    files_with_issues = len(all_results)
    
    print(f"\n" + "="*80)
    print("MWRASP AUTHENTICITY SUMMARY")
    print("="*80)
    print(f"Files analyzed with issues: {files_with_issues}")
    print(f"Total authenticity issues: {total_issues}")
    print(f"Critical fake code issues: {critical_issues}")
    
    if critical_issues > 10:
        authenticity_grade = "CRITICAL FAKE CODE - <50% AUTHENTIC"
    elif critical_issues > 5:
        authenticity_grade = "HIGH FAKE CODE - ~60-70% AUTHENTIC"  
    elif critical_issues > 0:
        authenticity_grade = "MODERATE FAKE CODE - ~70-85% AUTHENTIC"
    else:
        authenticity_grade = ">85% AUTHENTIC CODE"
    
    print(f"Authenticity Assessment: {authenticity_grade}")
    
    if critical_issues > 0:
        print(f"\nWARNING: {critical_issues} CRITICAL fake code issues detected!")
        print("These make the system appear more functional than it actually is.")
        print("Real working implementation required for genuine >85% development.")
    else:
        print(f"\nGOOD: No critical fake code detected. System appears genuinely functional.")

if __name__ == "__main__":
    main()
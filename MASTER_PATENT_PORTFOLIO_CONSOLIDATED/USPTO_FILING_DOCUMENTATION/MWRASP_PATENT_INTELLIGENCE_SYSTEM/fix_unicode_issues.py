#!/usr/bin/env python3
"""
Unicode Fix Script for Patent Intelligence System
================================================

Fixes encoding issues that prevent proper execution on Windows systems.
Replaces Unicode emoji characters with ASCII equivalents.

Author: MWRASP Patent Development Team
Date: September 2025
"""

import os
import re
from pathlib import Path

def fix_unicode_in_file(file_path: Path):
    """Fix Unicode issues in a single file"""
    
    # Unicode to ASCII replacements
    replacements = {
        '[SEARCH]': '[SEARCH]',
        '[DATA]': '[DATA]', 
        '[TARGET]': '[TARGET]',
        '[WEB]': '[WEB]',
        '[OK]': '[OK]',
        '[USPTO]': '[USPTO]',
        '[EPO]': '[EPO]',
        '[SUMMARY]': '[SUMMARY]',
        '[LAUNCH]': '[LAUNCH]',
        '[FAST]': '[FAST]',
        '[IDEA]': '[IDEA]',
        '[TOOL]': '[TOOL]',
        '[LIST]': '[LIST]',
        '[SUCCESS]': '[SUCCESS]',
        '[COMPLETE]': '[COMPLETE]',
        '[WARNING]': '[WARNING]',
        '[ERROR]': '[ERROR]',
        '[FOLDER]': '[FOLDER]',
        '[DOC]': '[DOC]',
        '[SECURE]': '[SECURE]',
        '[DEMO]': '[DEMO]',
        '[WIN]': '[WIN]',
        '[HOT]': '[HOT]',
        '[GEM]': '[GEM]',
        '[STAR]': '[STAR]',
        '[ART]': '[ART]',
        '[SCIENCE]': '[SCIENCE]',
        '[LEGAL]': '[LEGAL]',
        '[BUSINESS]': '[BUSINESS]',
        '[PERFORMANCE]': '[PERFORMANCE]',
        '[FINISH]': '[FINISH]'
    }
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Track if changes were made
        original_content = content
        
        # Apply replacements
        for unicode_char, ascii_replacement in replacements.items():
            content = content.replace(unicode_char, ascii_replacement)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Unicode issues in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_all_unicode_issues():
    """Fix Unicode issues in all Python files in the system"""
    
    base_dir = Path(__file__).parent
    python_files = list(base_dir.glob('**/*.py'))
    
    print("FIXING UNICODE ENCODING ISSUES")
    print("=" * 50)
    print(f"Found {len(python_files)} Python files to check")
    print()
    
    fixed_count = 0
    for py_file in python_files:
        if fix_unicode_in_file(py_file):
            fixed_count += 1
    
    print()
    print(f"Fixed Unicode issues in {fixed_count} files")
    print("Unicode fix complete - system should now run without encoding errors")

if __name__ == '__main__':
    fix_all_unicode_issues()
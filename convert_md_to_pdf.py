#!/usr/bin/env python3
"""
MWRASP Markdown to PDF Conversion Tool
Converts all .md files in the project to professional PDF format
"""

import os
import glob
import markdown2
from weasyprint import HTML, CSS
from pathlib import Path
import re
import time
from typing import List, Dict, Tuple
import argparse

class MWRASPPDFConverter:
    """Professional PDF converter for MWRASP documentation"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.pdf_output_dir = self.base_path / "PDF_DOCUMENTS"
        self.conversion_log = []
        self.css_styles = self._create_professional_css()
        
    def _create_professional_css(self) -> str:
        """Create professional CSS styles for PDFs"""
        return """
        @page {
            size: A4;
            margin: 1in;
            @top-center { content: "MWRASP Quantum Defense System"; }
            @bottom-right { content: "Page " counter(page); }
        }
        
        body {
            font-family: "Segoe UI", "Helvetica", "Arial", sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
            max-width: 100%;
        }
        
        h1 {
            color: #1e3a8a;
            font-size: 24pt;
            font-weight: bold;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 10pt;
            margin-top: 20pt;
            margin-bottom: 15pt;
            page-break-after: avoid;
        }
        
        h2 {
            color: #2563eb;
            font-size: 18pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }
        
        h3 {
            color: #3b82f6;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 15pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }
        
        h4 {
            color: #60a5fa;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }
        
        p {
            margin-bottom: 8pt;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 10pt;
            padding-left: 20pt;
        }
        
        li {
            margin-bottom: 4pt;
        }
        
        code {
            background-color: #f1f5f9;
            padding: 2pt 4pt;
            font-family: "Consolas", "Monaco", monospace;
            font-size: 9pt;
            border-radius: 3pt;
        }
        
        pre {
            background-color: #f8fafc;
            border: 1pt solid #e2e8f0;
            border-radius: 5pt;
            padding: 10pt;
            font-family: "Consolas", "Monaco", monospace;
            font-size: 8pt;
            line-height: 1.3;
            overflow-x: auto;
            margin-bottom: 10pt;
        }
        
        blockquote {
            border-left: 4pt solid #3b82f6;
            padding-left: 15pt;
            margin-left: 10pt;
            font-style: italic;
            color: #475569;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15pt;
            font-size: 9pt;
        }
        
        th, td {
            border: 1pt solid #d1d5db;
            padding: 6pt 8pt;
            text-align: left;
        }
        
        th {
            background-color: #f3f4f6;
            font-weight: bold;
            color: #1f2937;
        }
        
        .classification {
            text-align: center;
            font-weight: bold;
            color: #dc2626;
            font-size: 12pt;
            margin-bottom: 20pt;
            padding: 10pt;
            border: 2pt solid #dc2626;
            background-color: #fef2f2;
        }
        
        .toc {
            page-break-after: always;
            border: 1pt solid #d1d5db;
            padding: 15pt;
            margin-bottom: 20pt;
        }
        
        .executive-summary {
            background-color: #eff6ff;
            border: 1pt solid #3b82f6;
            padding: 15pt;
            margin-bottom: 20pt;
            border-radius: 5pt;
        }
        
        .section-break {
            page-break-before: always;
        }
        
        .no-break {
            page-break-inside: avoid;
        }
        
        /* Emoji and special character support */
        .emoji {
            font-size: 12pt;
        }
        
        /* Footer styling */
        .document-footer {
            border-top: 1pt solid #d1d5db;
            padding-top: 10pt;
            margin-top: 20pt;
            font-size: 8pt;
            color: #6b7280;
            text-align: center;
        }
        """
    
    def _preprocess_markdown(self, content: str, file_path: Path) -> str:
        """Preprocess markdown content for better PDF conversion"""
        
        # Add document classification if it contains sensitive information
        if any(keyword in content.lower() for keyword in ['classified', 'confidential', 'secret', 'darpa', 'patent']):
            classification = self._determine_classification(content)
            content = f'<div class="classification">{classification}</div>\n\n' + content
        
        # Convert emoji shortcuts to actual emojis
        emoji_map = {
            ':check_mark:': '✅', ':x:': '❌', ':warning:': '⚠️',
            ':fire:': '🔥', ':rocket:': '🚀', ':shield:': '🛡️',
            ':lock:': '🔒', ':key:': '🔑', ':gem:': '💎',
            ':chart_with_upwards_trend:': '📈', ':moneybag:': '💰',
            ':computer:': '💻', ':microscope:': '🔬', ':telescope:': '🔭'
        }
        
        for shortcut, emoji in emoji_map.items():
            content = content.replace(shortcut, f'<span class="emoji">{emoji}</span>')
        
        # Improve code block formatting
        content = re.sub(r'```(\w+)?\n', r'<pre><code>', content)
        content = re.sub(r'\n```', r'</code></pre>', content)
        
        # Add section breaks for major headers
        content = re.sub(r'^(# [^#].*)', r'<div class="section-break">\1</div>', content, flags=re.MULTILINE)
        
        # Protect tables and important sections from page breaks
        content = re.sub(r'(\|.*\|.*\n)', r'<div class="no-break">\1</div>', content)
        
        # Add document footer
        doc_footer = f"""
        <div class="document-footer">
        Document: {file_path.stem}<br>
        Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}<br>
        MWRASP Quantum Defense System - Confidential and Proprietary
        </div>
        """
        content += doc_footer
        
        return content
    
    def _determine_classification(self, content: str) -> str:
        """Determine document classification based on content"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['top secret', 'ts/', 'sci']):
            return "TOP SECRET//SCI - HANDLE VIA SPECIAL ACCESS CHANNELS"
        elif any(keyword in content_lower for keyword in ['secret', 'classified']):
            return "SECRET - AUTHORIZED PERSONNEL ONLY"
        elif any(keyword in content_lower for keyword in ['confidential', 'darpa', 'defense']):
            return "CONFIDENTIAL - GOVERNMENT/CONTRACTOR USE ONLY"
        elif any(keyword in content_lower for keyword in ['proprietary', 'patent']):
            return "PROPRIETARY - INTELLECTUAL PROPERTY PROTECTED"
        else:
            return "INTERNAL USE - BUSINESS SENSITIVE"
    
    def convert_single_file(self, md_file: Path) -> bool:
        """Convert a single markdown file to PDF"""
        try:
            print(f"Converting: {md_file.relative_to(self.base_path)}")
            
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                md_content = f.read()
            
            # Preprocess markdown
            processed_content = self._preprocess_markdown(md_content, md_file)
            
            # Convert to HTML
            html_content = markdown2.markdown(
                processed_content,
                extras=[
                    'fenced-code-blocks',
                    'tables',
                    'header-ids',
                    'toc',
                    'strike',
                    'task_list'
                ]
            )
            
            # Wrap in complete HTML document
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{md_file.stem}</title>
                <style>{self.css_styles}</style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Create output directory structure
            relative_path = md_file.relative_to(self.base_path)
            output_file = self.pdf_output_dir / relative_path.with_suffix('.pdf')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to PDF
            HTML(string=full_html, base_url=str(md_file.parent)).write_pdf(
                str(output_file),
                stylesheets=[CSS(string=self.css_styles)]
            )
            
            self.conversion_log.append({
                'file': str(md_file.relative_to(self.base_path)),
                'output': str(output_file.relative_to(self.base_path)),
                'status': 'success',
                'size': output_file.stat().st_size
            })
            
            return True
            
        except Exception as e:
            print(f"Error converting {md_file}: {str(e)}")
            self.conversion_log.append({
                'file': str(md_file.relative_to(self.base_path)),
                'output': '',
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def find_all_markdown_files(self) -> List[Path]:
        """Find all markdown files in the project"""
        md_files = []
        for pattern in ['**/*.md', '**/*.markdown']:
            md_files.extend(self.base_path.glob(pattern))
        
        # Sort by path for consistent processing order
        md_files.sort()
        return md_files
    
    def convert_all_files(self) -> Dict[str, int]:
        """Convert all markdown files to PDF"""
        print("🔍 Finding all markdown files...")
        md_files = self.find_all_markdown_files()
        
        print(f"📄 Found {len(md_files)} markdown files")
        print(f"📁 Output directory: {self.pdf_output_dir}")
        
        # Create output directory
        self.pdf_output_dir.mkdir(exist_ok=True)
        
        # Convert files
        print("\n🚀 Starting conversion...")
        start_time = time.time()
        
        success_count = 0
        error_count = 0
        
        for i, md_file in enumerate(md_files, 1):
            print(f"[{i:3d}/{len(md_files)}] ", end="")
            
            if self.convert_single_file(md_file):
                success_count += 1
            else:
                error_count += 1
        
        end_time = time.time()
        
        # Generate summary
        summary = {
            'total_files': len(md_files),
            'successful': success_count,
            'errors': error_count,
            'duration': end_time - start_time
        }
        
        self._generate_conversion_report(summary)
        
        return summary
    
    def _generate_conversion_report(self, summary: Dict[str, int]):
        """Generate conversion report"""
        report_path = self.pdf_output_dir / "CONVERSION_REPORT.txt"
        
        with open(report_path, 'w') as f:
            f.write("MWRASP Markdown to PDF Conversion Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Conversion Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Files: {summary['total_files']}\n")
            f.write(f"Successful: {summary['successful']}\n")
            f.write(f"Errors: {summary['errors']}\n")
            f.write(f"Duration: {summary['duration']:.2f} seconds\n\n")
            
            f.write("Detailed Results:\n")
            f.write("-" * 30 + "\n")
            
            for entry in self.conversion_log:
                f.write(f"File: {entry['file']}\n")
                f.write(f"Status: {entry['status']}\n")
                if entry['status'] == 'success':
                    f.write(f"Output: {entry['output']}\n")
                    f.write(f"Size: {entry['size']:,} bytes\n")
                else:
                    f.write(f"Error: {entry['error']}\n")
                f.write("\n")
        
        print(f"\n📊 Conversion Report: {report_path}")
    
    def create_master_index(self):
        """Create master PDF index"""
        index_content = """# MWRASP Quantum Defense System - PDF Document Index

## 📁 Document Categories

### 01_EXECUTIVE_SUMMARY
- Complete project overview and strategic documents
- Funding strategies and competitive analysis

### 02_FUNDING_MATERIALS  
- DARPA funding proposals and government materials
- Private investment prospectuses and presentations

### 03_TECHNICAL_DOCUMENTATION
- System architecture and technical specifications
- API documentation and security specifications

### 04_PATENTS_INTELLECTUAL_PROPERTY
- Patent filings and intellectual property strategy
- USPTO documents and prior art analysis

### 05_DEMONSTRATIONS_PROTOTYPES
- Working prototype demonstrations
- Test data and validation results

### 06_IMPLEMENTATION_GUIDES
- Deployment and implementation documentation
- Operational procedures and support guides

### 07_COMPLIANCE_CERTIFICATIONS
- Government compliance and certifications
- Standards compliance and regulatory materials

### 08_BUSINESS_DEVELOPMENT
- Sales materials and marketing documentation
- Partnership strategies and customer success

### 09_DEVELOPMENT_SOURCE_CODE
- Source code documentation
- API references and technical specifications

### 10_ARCHIVE
- Historical documents and previous versions
- Deprecated materials and development history

## 🔍 Quick Reference Guide

| **Purpose** | **Primary Documents** |
|-------------|----------------------|
| **Executive Overview** | `01_EXECUTIVE_SUMMARY/PROJECT_OVERVIEW.pdf` |
| **DARPA Funding** | `02_FUNDING_MATERIALS/DARPA/MWRASP_DARPA_Whitepaper.pdf` |
| **Private Investment** | `02_FUNDING_MATERIALS/Private_Investment/05_INVESTMENT_PROSPECTUS_COMPLETE.pdf` |
| **Technical Architecture** | `03_TECHNICAL_DOCUMENTATION/System_Architecture/COMPLETE_SYSTEM_ARCHITECTURE.pdf` |
| **Patent Portfolio** | `04_PATENTS_INTELLECTUAL_PROPERTY/Patent_Strategy/COMPLETE_IP_PORTFOLIO.pdf` |
| **Competitive Analysis** | `02_FUNDING_MATERIALS/Private_Investment/17_COMPETITIVE_ANALYSIS.pdf` |

---

*All documents are available in PDF format for professional presentation and distribution.*

Generated: """ + time.strftime('%Y-%m-%d %H:%M:%S')
        
        index_file = self.base_path / "PDF_INDEX.md"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        # Convert index to PDF
        self.convert_single_file(index_file)
        print(f"📋 Master Index: {self.pdf_output_dir / 'PDF_INDEX.pdf'}")

def main():
    """Main conversion function"""
    parser = argparse.ArgumentParser(description="Convert MWRASP markdown files to PDF")
    parser.add_argument("--path", default="C:/Users/User/MWRASP-Quantum-Defense", 
                       help="Base path to MWRASP project")
    parser.add_argument("--single", help="Convert single file")
    
    args = parser.parse_args()
    
    converter = MWRASPPDFConverter(args.path)
    
    print("🚀 MWRASP PDF Conversion Tool")
    print("=" * 40)
    
    if args.single:
        single_file = Path(args.single)
        if single_file.exists():
            converter.convert_single_file(single_file)
        else:
            print(f"❌ File not found: {single_file}")
            return
    else:
        # Convert all files
        summary = converter.convert_all_files()
        
        # Create master index
        converter.create_master_index()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 CONVERSION SUMMARY")
        print("=" * 50)
        print(f"✅ Successful: {summary['successful']}")
        print(f"❌ Errors: {summary['errors']}")
        print(f"⏱️  Duration: {summary['duration']:.2f} seconds")
        print(f"📁 Output: {converter.pdf_output_dir}")
        
        if summary['errors'] > 0:
            print(f"\n⚠️  Check conversion report for error details")
        else:
            print(f"\n🎉 All {summary['successful']} files converted successfully!")

if __name__ == "__main__":
    main()
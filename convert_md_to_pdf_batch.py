#!/usr/bin/env python3
"""
MWRASP Markdown to PDF Batch Conversion Tool
Converts markdown files to PDF using simple HTML generation and browser printing
"""

import os
import glob
import markdown
from pathlib import Path
import re
import time
from typing import List, Dict
import html
import shutil

class MWRASPBatchConverter:
    """Batch converter for MWRASP markdown to PDF"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.html_output_dir = self.base_path / "HTML_TEMP"
        self.pdf_output_dir = self.base_path / "PDF_DOCUMENTS"
        self.conversion_log = []
        
    def _create_html_template(self) -> str:
        """Create professional HTML template for PDF conversion"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @media print {{
            @page {{ 
                size: A4; 
                margin: 1in;
                @top-center {{ content: "MWRASP Quantum Defense System"; }}
                @bottom-right {{ content: "Page " counter(page); }}
            }}
        }}
        
        body {{
            font-family: "Segoe UI", "Helvetica", "Arial", sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 20px;
        }}
        
        h1 {{
            color: #1e3a8a;
            font-size: 24pt;
            font-weight: bold;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 10pt;
            margin-bottom: 20pt;
        }}
        
        h2 {{
            color: #2563eb;
            font-size: 18pt;
            font-weight: bold;
            margin-top: 25pt;
            margin-bottom: 15pt;
        }}
        
        h3 {{
            color: #3b82f6;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 10pt;
        }}
        
        h4 {{
            color: #60a5fa;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 15pt;
            margin-bottom: 8pt;
        }}
        
        p {{
            margin-bottom: 10pt;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-bottom: 12pt;
            padding-left: 25pt;
        }}
        
        li {{
            margin-bottom: 5pt;
        }}
        
        code {{
            background-color: #f1f5f9;
            padding: 3pt 6pt;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 10pt;
            border-radius: 3pt;
        }}
        
        pre {{
            background-color: #f8fafc;
            border: 1pt solid #e2e8f0;
            border-radius: 5pt;
            padding: 15pt;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 9pt;
            line-height: 1.3;
            overflow-x: auto;
            margin-bottom: 15pt;
            white-space: pre-wrap;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20pt;
            font-size: 10pt;
        }}
        
        th, td {{
            border: 1pt solid #d1d5db;
            padding: 8pt 10pt;
            text-align: left;
        }}
        
        th {{
            background-color: #f3f4f6;
            font-weight: bold;
            color: #1f2937;
        }}
        
        .classification {{
            text-align: center;
            font-weight: bold;
            color: #dc2626;
            font-size: 14pt;
            margin-bottom: 30pt;
            padding: 15pt;
            border: 2pt solid #dc2626;
            background-color: #fef2f2;
        }}
        
        .document-header {{
            text-align: center;
            margin-bottom: 30pt;
            padding-bottom: 20pt;
            border-bottom: 2pt solid #3b82f6;
        }}
        
        .document-footer {{
            border-top: 1pt solid #d1d5db;
            padding-top: 15pt;
            margin-top: 30pt;
            font-size: 9pt;
            color: #6b7280;
            text-align: center;
        }}
        
        blockquote {{
            border-left: 4pt solid #3b82f6;
            padding-left: 20pt;
            margin-left: 15pt;
            font-style: italic;
            color: #475569;
            margin-bottom: 15pt;
        }}
    </style>
</head>
<body>
    <div class="document-header">
        <h1>{title}</h1>
        <p><strong>MWRASP Quantum Defense System</strong></p>
        <p>Generated: {date}</p>
    </div>
    
    {classification}
    
    {content}
    
    <div class="document-footer">
        <p><strong>Document:</strong> {filename} | <strong>Generated:</strong> {date}</p>
        <p>MWRASP Quantum Defense System - Confidential and Proprietary</p>
    </div>
</body>
</html>"""
    
    def _determine_classification(self, content: str) -> str:
        """Determine document classification"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['top secret', 'ts/', 'sci']):
            return '<div class="classification">TOP SECRET//SCI - HANDLE VIA SPECIAL ACCESS CHANNELS</div>'
        elif any(keyword in content_lower for keyword in ['secret', 'classified']):
            return '<div class="classification">SECRET - AUTHORIZED PERSONNEL ONLY</div>'
        elif any(keyword in content_lower for keyword in ['confidential', 'darpa', 'defense']):
            return '<div class="classification">CONFIDENTIAL - GOVERNMENT/CONTRACTOR USE ONLY</div>'
        elif any(keyword in content_lower for keyword in ['proprietary', 'patent']):
            return '<div class="classification">PROPRIETARY - INTELLECTUAL PROPERTY PROTECTED</div>'
        else:
            return ''
    
    def _clean_markdown(self, content: str) -> str:
        """Clean markdown content for better conversion"""
        # Remove problematic unicode characters that might cause issues
        content = re.sub(r'[^\x00-\x7F]+', ' ', content)
        
        # Fix common markdown issues
        content = re.sub(r'```(\w+)?\n', '```\\n', content)
        content = re.sub(r'\n```', '\\n```', content)
        
        # Clean up excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        return content.strip()
    
    def convert_md_to_html(self, md_file: Path) -> bool:
        """Convert single markdown file to HTML"""
        try:
            print(f"Processing: {md_file.relative_to(self.base_path)}")
            
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
                md_content = f.read()
            
            # Clean content
            md_content = self._clean_markdown(md_content)
            
            # Convert to HTML
            html_content = markdown.markdown(
                md_content,
                extensions=[
                    'markdown.extensions.tables',
                    'markdown.extensions.fenced_code',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc'
                ]
            )
            
            # Get classification
            classification = self._determine_classification(md_content)
            
            # Create full HTML document
            template = self._create_html_template()
            full_html = template.format(
                title=md_file.stem.replace('_', ' ').title(),
                content=html_content,
                classification=classification,
                filename=md_file.name,
                date=time.strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # Create output file path
            relative_path = md_file.relative_to(self.base_path)
            html_output = self.html_output_dir / relative_path.with_suffix('.html')
            html_output.parent.mkdir(parents=True, exist_ok=True)
            
            # Write HTML file
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            self.conversion_log.append({
                'file': str(md_file.relative_to(self.base_path)),
                'html_output': str(html_output.relative_to(self.base_path)),
                'status': 'success'
            })
            
            return True
            
        except Exception as e:
            print(f"Error converting {md_file}: {str(e)}")
            self.conversion_log.append({
                'file': str(md_file.relative_to(self.base_path)),
                'html_output': '',
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def find_all_markdown_files(self) -> List[Path]:
        """Find all markdown files"""
        md_files = list(self.base_path.glob('**/*.md'))
        md_files.sort()
        return md_files
    
    def convert_all_to_html(self) -> Dict[str, int]:
        """Convert all markdown files to HTML"""
        print("Finding all markdown files...")
        md_files = self.find_all_markdown_files()
        
        print(f"Found {len(md_files)} markdown files")
        print(f"HTML output directory: {self.html_output_dir}")
        
        # Create directories
        self.html_output_dir.mkdir(exist_ok=True)
        self.pdf_output_dir.mkdir(exist_ok=True)
        
        print("\\nStarting HTML conversion...")
        start_time = time.time()
        
        success_count = 0
        error_count = 0
        
        for i, md_file in enumerate(md_files, 1):
            print(f"[{i:3d}/{len(md_files)}] ", end="")
            
            if self.convert_md_to_html(md_file):
                success_count += 1
                print("OK")
            else:
                error_count += 1
                print("ERROR")
        
        end_time = time.time()
        
        summary = {
            'total_files': len(md_files),
            'successful': success_count,
            'errors': error_count,
            'duration': end_time - start_time
        }
        
        self._generate_report(summary)
        self._create_pdf_instructions()
        
        return summary
    
    def _generate_report(self, summary: Dict[str, int]):
        """Generate conversion report"""
        report_path = self.html_output_dir / "CONVERSION_REPORT.txt"
        
        with open(report_path, 'w') as f:
            f.write("MWRASP Markdown to HTML Conversion Report\\n")
            f.write("=" * 50 + "\\n\\n")
            f.write(f"Conversion Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"Total Files: {summary['total_files']}\\n")
            f.write(f"Successful: {summary['successful']}\\n")
            f.write(f"Errors: {summary['errors']}\\n")
            f.write(f"Duration: {summary['duration']:.2f} seconds\\n\\n")
            
            f.write("Next Steps:\\n")
            f.write("-" * 20 + "\\n")
            f.write("1. Open Chrome/Edge browser\\n")
            f.write("2. Use batch print script to convert HTML to PDF\\n")
            f.write("3. See PDF_CONVERSION_INSTRUCTIONS.txt for details\\n\\n")
            
            f.write("Detailed Results:\\n")
            f.write("-" * 30 + "\\n")
            
            for entry in self.conversion_log:
                f.write(f"File: {entry['file']}\\n")
                f.write(f"Status: {entry['status']}\\n")
                if entry['status'] == 'success':
                    f.write(f"HTML Output: {entry['html_output']}\\n")
                else:
                    f.write(f"Error: {entry.get('error', 'Unknown error')}\\n")
                f.write("\\n")
        
        print(f"\\nConversion Report: {report_path}")
    
    def _create_pdf_instructions(self):
        """Create PDF conversion instructions"""
        instructions_path = self.base_path / "PDF_CONVERSION_INSTRUCTIONS.txt"
        
        instructions = f"""MWRASP PDF Conversion Instructions
=====================================

HTML files have been generated in: {self.html_output_dir}

To convert to PDF, you have several options:

OPTION 1: Browser Batch Print (Recommended)
------------------------------------------
1. Open Chrome or Edge browser
2. Navigate to the HTML_TEMP folder
3. Select all HTML files
4. Right-click and "Open with" browser
5. Use Ctrl+P to print each file
6. Select "Save as PDF" as destination
7. Save to PDF_DOCUMENTS folder

OPTION 2: PowerShell Script (Automated)
--------------------------------------
Run this PowerShell script to automate browser printing:

$htmlFiles = Get-ChildItem -Path "{self.html_output_dir}" -Filter "*.html" -Recurse
foreach ($file in $htmlFiles) {{
    $relativePath = $file.FullName.Substring("{self.html_output_dir}".Length + 1)
    $pdfPath = "{self.pdf_output_dir}\\$($relativePath -replace '\\.html$', '.pdf')"
    
    # Create directory if needed
    $pdfDir = Split-Path $pdfPath -Parent
    if (!(Test-Path $pdfDir)) {{ New-Item -ItemType Directory -Path $pdfDir -Force }}
    
    # Open in browser and print (requires manual intervention)
    Start-Process "chrome.exe" "--headless --disable-gpu --print-to-pdf=`"$pdfPath`" `"file:///$($file.FullName)`""
}}

OPTION 3: Online Converter
-------------------------
1. Upload HTML files to online HTML to PDF converter
2. Download converted PDF files
3. Organize in PDF_DOCUMENTS folder structure

OPTION 4: Install wkhtmltopdf
---------------------------
1. Download wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html
2. Install on your system
3. Run: wkhtmltopdf input.html output.pdf for each file

Total files to convert: {len(self.conversion_log)}
HTML files location: {self.html_output_dir}
Target PDF location: {self.pdf_output_dir}

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(instructions_path, 'w') as f:
            f.write(instructions)
        
        print(f"PDF Instructions: {instructions_path}")
    
    def create_master_index(self):
        """Create master index HTML file"""
        index_content = """# MWRASP Quantum Defense System - Document Index

## Document Categories

### 01_EXECUTIVE_SUMMARY
Complete project overview and strategic documents

### 02_FUNDING_MATERIALS  
DARPA funding proposals and private investment materials

### 03_TECHNICAL_DOCUMENTATION
System architecture and technical specifications

### 04_PATENTS_INTELLECTUAL_PROPERTY
Patent filings and intellectual property strategy

### 05_DEMONSTRATIONS_PROTOTYPES
Working demonstrations and test data

### 06_IMPLEMENTATION_GUIDES
Deployment and implementation documentation

### 07_COMPLIANCE_CERTIFICATIONS
Government compliance and certifications

### 08_BUSINESS_DEVELOPMENT
Sales materials and marketing documentation

### 09_DEVELOPMENT_SOURCE_CODE
Source code documentation

### 10_ARCHIVE
Historical documents and previous versions

## Key Documents

| Category | Document | Description |
|----------|----------|-------------|
| Executive | PROJECT_OVERVIEW.html | Complete project summary |
| Funding | MWRASP_DARPA_Whitepaper.html | DARPA funding proposal |
| Investment | 05_INVESTMENT_PROSPECTUS_COMPLETE.html | Private investment materials |
| Technical | COMPLETE_SYSTEM_ARCHITECTURE.html | Technical architecture |
| Patents | COMPLETE_IP_PORTFOLIO.html | Patent portfolio |
| Competition | 17_COMPETITIVE_ANALYSIS.html | Market analysis |

Generated: """ + time.strftime('%Y-%m-%d %H:%M:%S')
        
        index_file = self.base_path / "DOCUMENT_INDEX.md"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        # Convert to HTML
        self.convert_md_to_html(index_file)
        print(f"Master Index: {self.html_output_dir / 'DOCUMENT_INDEX.html'}")

def main():
    """Main function"""
    base_path = "C:/Users/User/MWRASP-Quantum-Defense"
    
    converter = MWRASPBatchConverter(base_path)
    
    print("MWRASP Markdown to HTML Conversion Tool")
    print("=" * 45)
    
    # Convert all files to HTML
    summary = converter.convert_all_to_html()
    
    # Create master index
    converter.create_master_index()
    
    # Print summary
    print("\\n" + "=" * 50)
    print("CONVERSION SUMMARY")
    print("=" * 50)
    print(f"Successful: {summary['successful']}")
    print(f"Errors: {summary['errors']}")
    print(f"Duration: {summary['duration']:.2f} seconds")
    print(f"HTML Output: {converter.html_output_dir}")
    
    print("\\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    print("1. HTML files generated successfully")
    print("2. Use browser 'Print to PDF' to create PDF files")
    print("3. See PDF_CONVERSION_INSTRUCTIONS.txt for details")
    print("4. Organize PDFs in PDF_DOCUMENTS folder")
    
    if summary['errors'] == 0:
        print("\\nAll files converted to HTML successfully!")
        print("Ready for PDF conversion via browser printing.")
    else:
        print(f"\\nWarning: {summary['errors']} files had conversion errors.")
        print("Check CONVERSION_REPORT.txt for details.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MWRASP Markdown to PDF Conversion Tool - Windows Compatible Version
Converts all .md files in the project to professional PDF format using ReportLab
"""

import os
import glob
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import Color, blue, red, black, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from pathlib import Path
import re
import time
from typing import List, Dict, Tuple
import html
from html.parser import HTMLParser

class HTMLToParagraph(HTMLParser):
    """Convert HTML to ReportLab Paragraph elements"""
    
    def __init__(self):
        super().__init__()
        self.elements = []
        self.current_text = ""
        self.in_code = False
        self.in_header = False
        self.header_level = 1
        
    def handle_starttag(self, tag, attrs):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = True
            self.header_level = int(tag[1])
        elif tag == 'code':
            self.in_code = True
        elif tag in ['strong', 'b']:
            self.current_text += "<b>"
        elif tag in ['em', 'i']:
            self.current_text += "<i>"
        elif tag == 'br':
            self.current_text += "<br/>"
            
    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_header = False
        elif tag == 'code':
            self.in_code = False
        elif tag in ['strong', 'b']:
            self.current_text += "</b>"
        elif tag in ['em', 'i']:
            self.current_text += "</i>"
            
    def handle_data(self, data):
        if self.in_code:
            self.current_text += f"<font name='Courier'>{html.escape(data)}</font>"
        else:
            self.current_text += html.escape(data)
            
    def get_text(self):
        return self.current_text

class MWRASPPDFConverter:
    """Professional PDF converter for MWRASP documentation"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.pdf_output_dir = self.base_path / "PDF_DOCUMENTS"
        self.conversion_log = []
        self.styles = self._create_styles()
        
    def _create_styles(self):
        """Create professional styles for PDF documents"""
        styles = getSampleStyleSheet()
        
        # Custom styles for MWRASP documents
        styles.add(ParagraphStyle(
            name='MWRASPTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=blue,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='MWRASPHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=20,
            textColor=blue,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='MWRASPHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=15,
            textColor=Color(0.2, 0.4, 0.8),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='MWRASPHeading3',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=10,
            textColor=Color(0.3, 0.5, 0.9),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='MWRASPNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='MWRASPCode',
            parent=styles['Code'],
            fontSize=8,
            fontName='Courier',
            backColor=Color(0.95, 0.95, 0.95),
            borderColor=Color(0.8, 0.8, 0.8),
            borderWidth=1,
            leftIndent=10,
            rightIndent=10,
            spaceAfter=10
        ))
        
        styles.add(ParagraphStyle(
            name='Classification',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=red,
            fontName='Helvetica-Bold',
            borderColor=red,
            borderWidth=2,
            spaceAfter=20,
            spaceBefore=10
        ))
        
        return styles
    
    def _determine_classification(self, content: str) -> str:
        """Determine document classification based on content"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['top secret', 'ts/', 'sci']):
            return "TOP SECRET//SCI"
        elif any(keyword in content_lower for keyword in ['secret', 'classified']):
            return "SECRET"
        elif any(keyword in content_lower for keyword in ['confidential', 'darpa', 'defense']):
            return "CONFIDENTIAL"
        elif any(keyword in content_lower for keyword in ['proprietary', 'patent']):
            return "PROPRIETARY"
        else:
            return "INTERNAL USE"
    
    def _clean_markdown_text(self, text: str) -> str:
        """Clean markdown text for better PDF conversion"""
        # Remove markdown syntax that doesn't convert well
        text = re.sub(r'```[a-zA-Z]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'#{1,6}\s*(.*)', r'<b>\1</b>', text)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _markdown_to_paragraphs(self, md_content: str) -> List:
        """Convert markdown content to ReportLab paragraphs"""
        elements = []
        
        # Add classification if needed
        classification = self._determine_classification(md_content)
        if classification != "INTERNAL USE":
            elements.append(Paragraph(f"CLASSIFICATION: {classification}", self.styles['Classification']))
            elements.append(Spacer(1, 12))
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )
        
        # Split into sections
        sections = re.split(r'<h([1-6])>(.*?)</h[1-6]>', html_content)
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
                
            if i % 3 == 1:  # Header level
                header_level = int(section)
                continue
            elif i % 3 == 2:  # Header text
                header_text = section.strip()
                style_name = f'MWRASPHeading{min(header_level, 3)}'
                elements.append(Paragraph(header_text, self.styles[style_name]))
                elements.append(Spacer(1, 6))
                continue
            
            # Regular content
            paragraphs = section.split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                # Handle code blocks
                if para.startswith('<pre>') or para.startswith('<code>'):
                    para = re.sub(r'<[^>]+>', '', para)
                    elements.append(Paragraph(para, self.styles['MWRASPCode']))
                else:
                    # Clean HTML tags for simple paragraphs
                    para = re.sub(r'<[^>]+>', '', para)
                    para = self._clean_markdown_text(para)
                    if para:
                        elements.append(Paragraph(para, self.styles['MWRASPNormal']))
                
                elements.append(Spacer(1, 4))
        
        return elements
    
    def convert_single_file(self, md_file: Path) -> bool:
        """Convert a single markdown file to PDF"""
        try:
            print(f"Converting: {md_file.relative_to(self.base_path)}")
            
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                md_content = f.read()
            
            # Create output directory structure
            relative_path = md_file.relative_to(self.base_path)
            output_file = self.pdf_output_dir / relative_path.with_suffix('.pdf')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_file),
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=1*inch,
                title=md_file.stem
            )
            
            # Add document title
            story = []
            story.append(Paragraph(md_file.stem.replace('_', ' ').title(), self.styles['MWRASPTitle']))
            story.append(Spacer(1, 20))
            
            # Convert markdown to paragraphs
            elements = self._markdown_to_paragraphs(md_content)
            story.extend(elements)
            
            # Add footer information
            story.append(PageBreak())
            story.append(Paragraph("MWRASP Quantum Defense System", self.styles['MWRASPHeading2']))
            story.append(Paragraph(f"Document: {md_file.stem}", self.styles['MWRASPNormal']))
            story.append(Paragraph(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}", self.styles['MWRASPNormal']))
            story.append(Paragraph("Confidential and Proprietary", self.styles['MWRASPNormal']))
            
            # Build PDF
            doc.build(story)
            
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
        for pattern in ['**/*.md']:
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
                print("✅")
            else:
                error_count += 1
                print("❌")
        
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
Working prototype demonstrations and test data

### 06_IMPLEMENTATION_GUIDES
Deployment and implementation documentation

### 07_COMPLIANCE_CERTIFICATIONS
Government compliance and certifications

### 08_BUSINESS_DEVELOPMENT
Sales materials and marketing documentation

### 09_DEVELOPMENT_SOURCE_CODE
Source code documentation and API references

### 10_ARCHIVE
Historical documents and previous versions

## Quick Reference Guide

**Executive Overview:** 01_EXECUTIVE_SUMMARY/PROJECT_OVERVIEW.pdf
**DARPA Funding:** 02_FUNDING_MATERIALS/DARPA/MWRASP_DARPA_Whitepaper.pdf
**Private Investment:** 02_FUNDING_MATERIALS/Private_Investment/05_INVESTMENT_PROSPECTUS_COMPLETE.pdf
**Technical Architecture:** 03_TECHNICAL_DOCUMENTATION/System_Architecture/COMPLETE_SYSTEM_ARCHITECTURE.pdf
**Patent Portfolio:** 04_PATENTS_INTELLECTUAL_PROPERTY/Patent_Strategy/COMPLETE_IP_PORTFOLIO.pdf
**Competitive Analysis:** 02_FUNDING_MATERIALS/Private_Investment/17_COMPETITIVE_ANALYSIS.pdf

All documents are available in PDF format for professional presentation and distribution.

Generated: """ + time.strftime('%Y-%m-%d %H:%M:%S')
        
        index_file = self.base_path / "PDF_INDEX.md"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        # Convert index to PDF
        self.convert_single_file(index_file)
        print(f"📋 Master Index: {self.pdf_output_dir / 'PDF_INDEX.pdf'}")

def main():
    """Main conversion function"""
    base_path = "C:/Users/User/MWRASP-Quantum-Defense"
    
    converter = MWRASPPDFConverter(base_path)
    
    print("🚀 MWRASP PDF Conversion Tool")
    print("=" * 40)
    
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
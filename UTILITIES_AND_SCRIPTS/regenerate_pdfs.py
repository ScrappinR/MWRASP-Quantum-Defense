#!/usr/bin/env python3
"""
Simple script to regenerate PDFs for updated DARPA video documents
"""
import os
import subprocess
from pathlib import Path

# Updated files that need PDF regeneration
updated_files = [
    "02_FUNDING_MATERIALS/DARPA/DARPA_PITCH_REPORT.md",
    "08_BUSINESS_DEVELOPMENT/Marketing/PARADIGM_SHIFT_NARRATIVE.md", 
    "08_BUSINESS_DEVELOPMENT/Marketing/ELEVATOR_PITCHES.md"
]

def convert_to_pdf(md_file):
    """Convert markdown to PDF using wkhtmltopdf or available tools"""
    try:
        # Check if wkhtmltopdf is available
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Using wkhtmltopdf for {md_file}")
            pdf_file = md_file.replace('.md', '.pdf')
            pdf_path = f"PDF_DOCUMENTS/{pdf_file}"
            
            # Create output directory
            Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create simple HTML
            html_content = create_html_from_md(md_file)
            temp_html = f"temp_{Path(md_file).name}.html"
            
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Convert to PDF
            subprocess.run(['wkhtmltopdf', temp_html, pdf_path], 
                         capture_output=True)
            
            # Cleanup
            if os.path.exists(temp_html):
                os.remove(temp_html)
                
            print(f"✓ Generated: {pdf_path}")
            return True
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"wkhtmltopdf not available for {md_file}")
        return False

def create_html_from_md(md_file):
    """Simple markdown to HTML conversion"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic markdown conversions
    html = content.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
    html = html.replace('## ', '<h2>').replace('\n', '</h2>\n')
    html = html.replace('### ', '<h3>').replace('\n', '</h3>\n')
    
    # Wrap in HTML structure
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MWRASP Document</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .header {{ border-bottom: 2px solid #3498db; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <div class="header"><h1>MWRASP Quantum Defense System</h1></div>
    {html}
</body>
</html>"""
    return full_html

def main():
    print("Regenerating PDFs for updated castle/gunpowder metaphor documents...")
    
    success_count = 0
    for md_file in updated_files:
        if os.path.exists(md_file):
            if convert_to_pdf(md_file):
                success_count += 1
        else:
            print(f"File not found: {md_file}")
    
    print(f"\n✓ Successfully regenerated {success_count} PDF documents")
    print("Castle/gunpowder metaphor updates complete!")

if __name__ == "__main__":
    main()
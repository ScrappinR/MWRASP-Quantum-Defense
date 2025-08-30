#!/usr/bin/env python3
"""
Convert updated DARPA video scripts to professional PDFs
"""
import markdown2
import pdfkit
from pathlib import Path
import os

def create_professional_html(md_content, title):
    """Convert markdown to professional HTML with MWRASP branding"""
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables', 'header-ids'])
    
    # Professional HTML template
    professional_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 40px;
            background: white;
        }}
        
        .header {{
            border-bottom: 3px solid #3498db;
            margin-bottom: 30px;
            padding-bottom: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 24px;
            margin: 0;
            font-weight: 700;
        }}
        
        .header h2 {{
            color: #7f8c8d;
            font-size: 16px;
            margin: 5px 0;
            font-weight: 400;
        }}
        
        .classification {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            font-size: 12px;
            text-align: center;
            color: #6c757d;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 22px;
        }}
        
        h2 {{
            color: #34495e;
            font-size: 20px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #5d6d7e;
            font-size: 18px;
            margin-top: 25px;
        }}
        
        h4 {{
            color: #7f8c8d;
            font-size: 16px;
            margin-top: 20px;
        }}
        
        .timeline-section {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .technical-spec {{
            background: #e8f5e8;
            border: 1px solid #c3e6c3;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        
        .strategic-point {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            font-style: italic;
            background: #f8f9fa;
            padding: 15px 20px;
        }}
        
        .footer {{
            border-top: 2px solid #3498db;
            margin-top: 40px;
            padding-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #7f8c8d;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
            }}
            
            .header {{
                margin-bottom: 20px;
            }}
            
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MWRASP Quantum Defense System</h1>
        <h2>{title}</h2>
    </div>
    
    <div class="classification">
        <strong>UNCLASSIFIED//FOR OFFICIAL USE ONLY</strong><br>
        Distribution: DARPA Personnel and Authorized Government Evaluators Only
    </div>
    
    <div class="content">
        {html_content}
    </div>
    
    <div class="footer">
        <strong>MWRASP Quantum Defense System</strong><br>
        Document Generated: August 25, 2025<br>
        Classification: UNCLASSIFIED//FOR OFFICIAL USE ONLY
    </div>
</body>
</html>"""
    
    return professional_html

def convert_to_pdf(md_file, output_file, title):
    """Convert markdown file to professional PDF"""
    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Create professional HTML
        html_content = create_professional_html(md_content, title)
        
        # Write HTML to temporary file
        temp_html = md_file.replace('.md', '_temp.html')
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # PDF options for professional output
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None
        }
        
        # Convert to PDF
        try:
            pdfkit.from_file(temp_html, output_file, options=options)
            print(f"✓ Successfully created: {output_file}")
            success = True
        except Exception as e:
            print(f"PDFKit conversion failed for {md_file}: {e}")
            # Fallback: try simple conversion
            success = False
        
        # Clean up temp file
        if os.path.exists(temp_html):
            os.remove(temp_html)
            
        return success
        
    except Exception as e:
        print(f"Error converting {md_file}: {e}")
        return False

def main():
    """Convert both video script files to PDFs"""
    print("Converting DARPA video scripts to professional PDFs...")
    
    # Define file pairs
    conversions = [
        {
            'md_file': 'MWRASP_DARPA_Video_Pitch_Complete_Production_Script.md',
            'pdf_file': 'MWRASP DARPA Video Pitch - Complete Production Script.pdf',
            'title': 'Video Pitch - Complete Production Script'
        },
        {
            'md_file': 'MWRASP_DARPA_Solo_Video_Production_Bible.md',
            'pdf_file': 'MWRASP DARPA Solo Video Production Bible - The Real Battle Plan.pdf',
            'title': 'Solo Video Production Bible - The Real Battle Plan'
        }
    ]
    
    success_count = 0
    
    for conversion in conversions:
        md_path = Path(conversion['md_file'])
        pdf_path = Path(conversion['pdf_file'])
        
        if md_path.exists():
            if convert_to_pdf(md_path, pdf_path, conversion['title']):
                success_count += 1
            else:
                print(f"Failed to convert: {conversion['md_file']}")
        else:
            print(f"Source file not found: {conversion['md_file']}")
    
    print(f"\n✓ Successfully converted {success_count}/{len(conversions)} video script documents")
    print("Updated DARPA video production materials ready for distribution!")

if __name__ == "__main__":
    main()
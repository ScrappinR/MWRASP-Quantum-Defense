import os
import subprocess
import sys
from pathlib import Path

def convert_svg_to_pdf_with_edge(svg_file, pdf_file, base_dir):
    """Convert SVG to PDF using Microsoft Edge in headless mode"""
    html_file = svg_file.replace('.svg', '.html')
    html_path = os.path.join(base_dir, html_file)
    pdf_path = os.path.join(base_dir, pdf_file)
    
    # Check if HTML file exists
    if not os.path.exists(html_path):
        print(f"Error: HTML file {html_path} not found")
        return False
    
    # Microsoft Edge path
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    if not os.path.exists(edge_path):
        print(f"Error: Microsoft Edge not found at {edge_path}")
        return False
    
    try:
        # Change to the directory containing the files
        original_dir = os.getcwd()
        os.chdir(base_dir)
        
        # Build command
        cmd = [
            edge_path,
            '--headless',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=30000',
            f'--print-to-pdf={pdf_file}',
            '--print-to-pdf-no-header',
            '--no-margins',
            html_file
        ]
        
        print(f"Converting {html_file} to {pdf_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Return to original directory
        os.chdir(original_dir)
        
        if result.returncode == 0:
            if os.path.exists(pdf_path):
                print(f"[SUCCESS] Successfully created {pdf_file}")
                return True
            else:
                print(f"[ERROR] Command succeeded but {pdf_file} was not created")
                return False
        else:
            print(f"[ERROR] Edge command failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout converting {svg_file}")
        os.chdir(original_dir)
        return False
    except Exception as e:
        print(f"[ERROR] Error converting {svg_file}: {str(e)}")
        os.chdir(original_dir)
        return False

def main():
    # Base directory
    base_dir = r"C:\Users\User\MWRASP-Quantum-Defense\FILED_PROVISIONAL_PATENTS\STRATEGIC_MOAT_PATENTS\10_Temporal_Cryptographic_Key_Lifecycle"
    
    # Files to convert
    conversions = [
        ("FIGURE_1_SYSTEM_ARCHITECTURE.svg", "FIGURE_1_SYSTEM_ARCHITECTURE.pdf"),
        ("FIGURE_2_KEY_LIFECYCLE_PROCESS.svg", "FIGURE_2_KEY_LIFECYCLE_PROCESS.pdf"),
        ("FIGURE_3_TEMPORAL_SECURITY_CONTROLS.svg", "FIGURE_3_TEMPORAL_SECURITY_CONTROLS.pdf")
    ]
    
    print("Patent 10 SVG to PDF Converter")
    print("=" * 50)
    
    success_count = 0
    total_count = len(conversions)
    
    for svg_file, pdf_file in conversions:
        svg_path = os.path.join(base_dir, svg_file)
        
        # Check if SVG exists
        if not os.path.exists(svg_path):
            print(f"[ERROR] SVG file not found: {svg_file}")
            continue
            
        # Convert SVG to PDF
        if convert_svg_to_pdf_with_edge(svg_file, pdf_file, base_dir):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"Conversion Results: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("[SUCCESS] All SVG files successfully converted to PDF!")
        return 0
    else:
        print(f"[ERROR] {total_count - success_count} conversions failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
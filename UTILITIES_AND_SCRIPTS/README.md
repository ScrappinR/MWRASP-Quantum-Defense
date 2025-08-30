# MWRASP Utilities and Scripts

This directory contains utility scripts, conversion tools, and automation scripts for the MWRASP Quantum Defense Platform.

## 🛠️ Utility Categories

### Document Conversion Tools
- `convert_md_to_pdf.py` - Markdown to PDF converter with styling
- `convert_md_to_pdf_batch.py` - Batch markdown conversion
- `md_to_pdf_simple.py` - Simple markdown to PDF converter
- `complete_pdf_converter.py` - Complete PDF conversion suite
- `Convert-HTML-to-PDF.ps1` - PowerShell HTML to PDF converter
- `convert_to_pdf.bat` - Batch file for PDF conversion

### Patent and Documentation Tools
- `convert_patents_to_pdf.py` - Patent document PDF conversion
- `regenerate_patents_pdf.py` - Regenerate patent PDFs
- `regenerate_patents_simple.py` - Simple patent PDF regeneration
- `regenerate_comprehensive_patents_pdf.py` - Comprehensive patent PDF generation
- `replace_patent_pdfs.py` - Patent PDF replacement utility
- `PROVISIONAL_PATENT_BATCH_CREATOR.py` - Automated patent application creator

### PDF Management
- `create_pdf_summary.py` - PDF summary generation
- `regenerate_pdfs.py` - General PDF regeneration utility

### System Management Scripts
- `quick_start.bat` - **Quick start script for Windows**
- `run_patent_search.bat` - Patent search automation
- `convert_to_pdf.bat` - PDF conversion batch script
- `update_github.bat` - GitHub update automation
- `update_github.ps1` - PowerShell GitHub update script

### Document Management
- `update_documents_batch.py` - Batch document update utility

## 🚀 Quick Start Tools

### Windows Quick Start
```bash
# Run the complete quick start
quick_start.bat

# This will:
# 1. Check Python installation
# 2. Install dependencies
# 3. Launch the main system
# 4. Open dashboard in browser
```

### Patent Management
```bash
# Convert patents to PDF
python convert_patents_to_pdf.py

# Regenerate all patent PDFs
python regenerate_comprehensive_patents_pdf.py

# Create patent batch applications
python PROVISIONAL_PATENT_BATCH_CREATOR.py
```

### Document Conversion
```bash
# Convert single markdown file
python md_to_pdf_simple.py input.md output.pdf

# Batch convert markdown files
python convert_md_to_pdf_batch.py

# Complete PDF conversion suite
python complete_pdf_converter.py
```

## 📁 File Categories

### Conversion Utilities 🔄
- **Markdown to PDF**: Multiple conversion options with styling
- **HTML to PDF**: PowerShell and Python implementations
- **Batch Processing**: Automated bulk conversions
- **Patent Specific**: Specialized patent document handling

### Automation Scripts 🤖
- **Quick Start**: One-click system launch
- **GitHub Integration**: Automated repository updates
- **Document Updates**: Batch document management
- **Patent Processing**: Automated patent application generation

### System Scripts 💻
- **Windows Batch**: .bat files for Windows automation
- **PowerShell**: .ps1 files for advanced Windows scripting
- **Python Utilities**: Cross-platform Python automation

## 🔧 Usage Examples

### Converting Documentation
```bash
# Convert project README to PDF
python md_to_pdf_simple.py README.md README.pdf

# Convert all markdown files in a directory
python convert_md_to_pdf_batch.py --input-dir ./docs --output-dir ./pdfs

# Generate patent PDFs with proper formatting
python convert_patents_to_pdf.py --patent-dir ./patents
```

### System Automation
```bash
# Windows: Launch complete system
quick_start.bat

# Update GitHub repository
update_github.bat

# Search and manage patents
run_patent_search.bat
```

### Batch Operations
```bash
# Update all project documents
python update_documents_batch.py

# Regenerate all PDFs in project
python regenerate_pdfs.py

# Replace patent PDFs with updated versions
python replace_patent_pdfs.py
```

## 📊 Utility Features

### PDF Generation ✅
- **Professional Styling**: Consistent formatting and branding
- **Batch Processing**: Handle multiple files automatically
- **Patent Formatting**: Specialized patent document formatting
- **Cross-Platform**: Works on Windows, Linux, macOS

### Automation ⚡
- **One-Click Launch**: Complete system startup
- **GitHub Integration**: Automated repository management
- **Document Management**: Bulk document operations
- **Error Handling**: Robust error handling and logging

### Development Tools 🔨
- **Quick Testing**: Rapid development iteration
- **Document Validation**: Ensure document integrity
- **System Health**: Monitor and maintain system components
- **Integration**: Seamless integration with main system

## 🏗️ Architecture Integration

These utilities integrate with:
- **Main System**: Core MWRASP implementations
- **Documentation**: Project documentation management
- **Patent Portfolio**: IP management and filing
- **GitHub Repository**: Version control and deployment
- **Business Operations**: Professional document generation

## 📈 Performance

- **Fast Conversion**: Optimized for large document sets
- **Parallel Processing**: Multi-threaded batch operations
- **Memory Efficient**: Handles large files without memory issues
- **Error Recovery**: Automatic retry and error handling

---
*Essential utilities for MWRASP system management, documentation, and automation.*
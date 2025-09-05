"""
MWRASP Quantum Defense Platform - Setup Script
==============================================

Production installation script for the complete MWRASP system.
Installs all dependencies and prepares the system for enterprise deployment.

Usage:
    pip install -e .                   # Development installation
    python setup.py install           # Production installation
    python setup.py sdist bdist_wheel # Create distribution packages
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Read version from mwrasp.py
version = "3.0.0"

# Production dependencies
requirements = [
    # Core system requirements
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "websockets>=11.0",
    "pydantic>=2.0.0",
    
    # Scientific computing
    "numpy>=1.21.0",
    "scipy>=1.9.0",
    
    # Cryptography and security
    "cryptography>=41.0.0",
    "pycryptodome>=3.19.0",
    
    # Network and web
    "requests>=2.31.0",
    "aiohttp>=3.8.0",
    "httpx>=0.25.0",
    
    # Data processing
    "pandas>=2.0.0",
    "python-multipart>=0.0.6",
    
    # Configuration management
    "pyyaml>=6.0.0",
    "python-dotenv>=1.0.0",
    
    # Monitoring and logging
    "psutil>=5.9.0",
    "prometheus-client>=0.17.0",
]

# Quantum computing requirements (optional but recommended)
quantum_requirements = [
    "qiskit>=0.45.0",
    "qiskit-ibm-runtime>=0.17.0",
    "qiskit-aer>=0.13.0",
]

# Development requirements
dev_requirements = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]

# Documentation requirements  
docs_requirements = [
    "sphinx>=7.1.0",
    "sphinx-rtd-theme>=1.3.0",
    "myst-parser>=2.0.0",
]

# Enterprise deployment requirements
enterprise_requirements = [
    "gunicorn>=21.2.0",
    "redis>=5.0.0",
    "celery>=5.3.0",
    "flower>=2.0.0",
    "supervisor>=4.2.0",
]

setup(
    name="mwrasp-quantum-defense",
    version=version,
    description="Production-ready quantum defense platform with IBM hardware validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MWRASP Development Team",
    author_email="contact@mwrasp.com",
    url="https://github.com/mwrasp/quantum-defense",
    license="Proprietary",
    
    # Package configuration
    packages=find_packages(include=['src', 'src.*']),
    package_dir={'': '.'},
    include_package_data=True,
    zip_safe=False,
    
    # Python requirements
    python_requires=">=3.9",
    install_requires=requirements,
    
    # Optional dependencies
    extras_require={
        "quantum": quantum_requirements,
        "dev": dev_requirements,
        "docs": docs_requirements,
        "enterprise": enterprise_requirements,
        "full": quantum_requirements + dev_requirements + docs_requirements + enterprise_requirements,
    },
    
    # Console scripts
    entry_points={
        "console_scripts": [
            "mwrasp=mwrasp:main",
            "mwrasp-server=src.api.server:run_server",
            "mwrasp-test=VALIDATION_AND_TESTING.complete_mwrasp_integration_test:main",
        ],
    },
    
    # Package data
    package_data={
        "src": [
            "dashboard/*.html",
            "dashboard/*.css", 
            "dashboard/*.js",
            "api/static/*",
            "core/config/*.json",
        ],
    },
    
    # Project classification
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology", 
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10", 
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # Keywords for discoverability
    keywords=[
        "quantum", "security", "defense", "cryptography", "ibm-quantum",
        "post-quantum", "threat-detection", "cybersecurity", "enterprise",
        "blockchain", "artificial-intelligence", "machine-learning",
    ],
    
    # Project URLs
    project_urls={
        "Documentation": "https://mwrasp.com/docs",
        "Source": "https://github.com/mwrasp/quantum-defense",
        "Tracker": "https://github.com/mwrasp/quantum-defense/issues",
        "Enterprise": "https://mwrasp.com/enterprise",
        "Support": "https://mwrasp.com/support",
    },
)
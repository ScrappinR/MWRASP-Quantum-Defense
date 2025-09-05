#!/usr/bin/env python3
"""
MWRASP Automated Patent Filing Preparation System
=================================================

This system automates the preparation of patent documents for USPTO filing,
including ADS generation, document validation, form population, and filing
checklist management.

Author: MWRASP Patent Development Team
Date: August 2025
Version: 1.0
"""

import os
import json
import datetime
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('patent_filing_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PatentInfo:
    """Patent application information structure"""
    patent_number: str
    title: str
    tier: str
    priority: str
    folder_path: str
    inventors: List[str]
    assignee: str
    technical_field: str
    filing_date: Optional[str] = None
    application_number: Optional[str] = None
    value_estimate: Optional[str] = None
    status: str = "ready"

@dataclass
class InventorInfo:
    """Inventor information for ADS forms"""
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    citizenship: str
    middle_initial: Optional[str] = None

@dataclass
class AssigneeInfo:
    """Assignee information for ADS forms"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    organization_type: str  # individual, corporation, partnership, etc.

class AutomatedPatentFilingSystem:
    """Main class for automated patent filing preparation"""
    
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory)
        self.patents = {}
        self.filing_config = {}
        self.load_configuration()
        
        logger.info(f"Initialized Automated Patent Filing System")
        logger.info(f"Base directory: {self.base_directory}")
    
    def load_configuration(self):
        """Load filing configuration from config file or create default"""
        config_file = self.base_directory / "filing_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.filing_config = json.load(f)
            logger.info("Loaded existing filing configuration")
        else:
            # Create default configuration
            self.filing_config = {
                "applicant_info": {
                    "name": "[TO BE FILLED]",
                    "address": "[TO BE FILLED]",
                    "city": "[TO BE FILLED]",
                    "state": "[TO BE FILLED]",
                    "zip": "[TO BE FILLED]",
                    "country": "US",
                    "phone": "[TO BE FILLED]",
                    "email": "[TO BE FILLED]"
                },
                "inventors": [
                    {
                        "first_name": "[TO BE FILLED]",
                        "last_name": "[TO BE FILLED]",
                        "address": "[TO BE FILLED]",
                        "city": "[TO BE FILLED]",
                        "state": "[TO BE FILLED]",
                        "zip": "[TO BE FILLED]",
                        "country": "US",
                        "citizenship": "US"
                    }
                ],
                "assignee": {
                    "name": "MWRASP Technologies",
                    "address": "[TO BE FILLED]",
                    "city": "[TO BE FILLED]",
                    "state": "[TO BE FILLED]",
                    "zip": "[TO BE FILLED]",
                    "country": "US",
                    "type": "corporation"
                },
                "filing_preferences": {
                    "entity_size": "micro",  # micro, small, large
                    "expedited_processing": False,
                    "international_filing": True,
                    "pct_countries": ["US", "EP", "CA", "JP", "AU", "GB", "IL"]
                },
                "attorney_info": {
                    "name": "[TO BE ASSIGNED]",
                    "registration_number": "[TO BE ASSIGNED]",
                    "address": "[TO BE ASSIGNED]",
                    "phone": "[TO BE ASSIGNED]",
                    "email": "[TO BE ASSIGNED]"
                }
            }
            self.save_configuration()
            logger.info("Created default filing configuration")
    
    def save_configuration(self):
        """Save current configuration to file"""
        config_file = self.base_directory / "filing_config.json"
        with open(config_file, 'w') as f:
            json.dump(self.filing_config, f, indent=2)
        logger.info("Saved filing configuration")
    
    def discover_patents(self) -> Dict[str, PatentInfo]:
        """Discover all patent applications in the directory structure"""
        patents = {}
        
        # Define tier directories
        tier_dirs = {
            "TIER_1_CRITICAL_PRIORITY": "Tier 1",
            "TIER_2_HIGH_PRIORITY": "Tier 2", 
            "TIER_3_MEDIUM_PRIORITY": "Tier 3"
        }
        
        for tier_dir, tier_name in tier_dirs.items():
            tier_path = self.base_directory / tier_dir
            if not tier_path.exists():
                continue
                
            for patent_dir in tier_path.iterdir():
                if not patent_dir.is_dir():
                    continue
                    
                # Extract patent number from directory name
                match = re.match(r'(\d+)_(.+)', patent_dir.name)
                if not match:
                    continue
                    
                patent_num = match.group(1)
                patent_name = match.group(2).replace('_', ' ')
                
                # Check if patent is abandoned
                abandoned_file = patent_dir / "PATENT_ABANDONED.md"
                if abandoned_file.exists():
                    logger.info(f"Patent {patent_num} is abandoned, skipping")
                    continue
                
                # Look for provisional patent application
                app_file = patent_dir / "PROVISIONAL_PATENT_APPLICATION.md"
                if not app_file.exists():
                    logger.warning(f"No provisional application found for patent {patent_num}")
                    continue
                
                # Extract title from patent application
                title = self.extract_patent_title(app_file)
                
                assignee_name = None
                if self.filing_config["assignee"]:
                    assignee_name = self.filing_config["assignee"]["name"]
                
                patent_info = PatentInfo(
                    patent_number=patent_num,
                    title=title or patent_name,
                    tier=tier_name,
                    priority=self.get_priority_level(tier_name),
                    folder_path=str(patent_dir),
                    inventors=self.filing_config["inventors"],
                    assignee=assignee_name,
                    technical_field=self.extract_technical_field(app_file)
                )
                
                patents[patent_num] = patent_info
                
        self.patents = patents
        logger.info(f"Discovered {len(patents)} patent applications")
        return patents
    
    def extract_patent_title(self, app_file: Path) -> Optional[str]:
        """Extract patent title from provisional application file"""
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for title in markdown format
            title_match = re.search(r'\*\*Title:\*\*\s*(.+)', content)
            if title_match:
                return title_match.group(1).strip()
                
            # Alternative format
            title_match = re.search(r'# PROVISIONAL PATENT APPLICATION\s*\n\s*\*\*Title:\*\*\s*(.+)', content)
            if title_match:
                return title_match.group(1).strip()
                
            return None
            
        except Exception as e:
            logger.error(f"Error extracting title from {app_file}: {e}")
            return None
    
    def extract_technical_field(self, app_file: Path) -> str:
        """Extract technical field from provisional application"""
        try:
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for technical field section
            field_match = re.search(r'## TECHNICAL FIELD\s*\n\s*(.+?)(?=\n##|\n---|\Z)', content, re.DOTALL)
            if field_match:
                field_text = field_match.group(1).strip()
                # Take first sentence as summary
                first_sentence = field_text.split('.')[0] + '.'
                return first_sentence
                
            return "Cybersecurity and quantum computing systems"
            
        except Exception as e:
            logger.error(f"Error extracting technical field from {app_file}: {e}")
            return "Cybersecurity systems"
    
    def get_priority_level(self, tier: str) -> str:
        """Get priority level based on tier"""
        priority_map = {
            "Tier 1": "CRITICAL",
            "Tier 2": "HIGH", 
            "Tier 3": "MEDIUM"
        }
        return priority_map.get(tier, "MEDIUM")
    
    def generate_ads_xml(self, patent_info: PatentInfo) -> str:
        """Generate Application Data Sheet (ADS) in XML format for USPTO"""
        
        # Create XML structure for ADS
        root = ET.Element("application-data-sheet")
        root.set("xmlns", "http://www.uspto.gov/adsxml")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "http://www.uspto.gov/adsxml http://www.uspto.gov/adsxml/adsxml4-3-0.xsd")
        
        # Application Information
        app_info = ET.SubElement(root, "application-information")
        app_type = ET.SubElement(app_info, "application-type")
        app_type.text = "provisional"
        
        # Title
        title_elem = ET.SubElement(app_info, "title")
        title_elem.text = patent_info.title
        
        # Applicant Information
        applicants = ET.SubElement(root, "applicant-information")
        for i, inventor in enumerate(self.filing_config["inventors"]):
            applicant = ET.SubElement(applicants, "applicant")
            applicant.set("app-type", "applicant-inventor")
            applicant.set("designation", "all")
            
            # Name
            name = ET.SubElement(applicant, "name")
            first_name = ET.SubElement(name, "first-name")
            first_name.text = inventor["first_name"]
            last_name = ET.SubElement(name, "last-name")
            last_name.text = inventor["last_name"]
            
            # Address
            address = ET.SubElement(applicant, "address")
            addr_line = ET.SubElement(address, "address-line-1")
            addr_line.text = inventor["address"]
            city_elem = ET.SubElement(address, "city")
            city_elem.text = inventor["city"]
            state_elem = ET.SubElement(address, "state")
            state_elem.text = inventor["state"]
            zip_elem = ET.SubElement(address, "postal-code")
            zip_elem.text = inventor["zip"]
            country_elem = ET.SubElement(address, "country")
            country_elem.text = inventor["country"]
            
            # Citizenship
            citizenship = ET.SubElement(applicant, "citizenship")
            citizenship.text = inventor["citizenship"]
        
        # Assignee Information (only if assignee exists)
        if self.filing_config["assignee"] and self.filing_config["assignee"]["name"]:
            assignee_info = ET.SubElement(root, "assignee-information")
            assignee = ET.SubElement(assignee_info, "assignee")
            
            org_name = ET.SubElement(assignee, "organization-name")
            org_name.text = self.filing_config["assignee"]["name"]
            
            # Assignee address
            address = ET.SubElement(assignee, "address")
            addr_line = ET.SubElement(address, "address-line-1")
            addr_line.text = self.filing_config["assignee"]["address"]
            city_elem = ET.SubElement(address, "city")
            city_elem.text = self.filing_config["assignee"]["city"]
            state_elem = ET.SubElement(address, "state")
            state_elem.text = self.filing_config["assignee"]["state"]
            zip_elem = ET.SubElement(address, "postal-code")
            zip_elem.text = self.filing_config["assignee"]["zip"]
            country_elem = ET.SubElement(address, "country")
            country_elem.text = self.filing_config["assignee"]["country"]
        
        # Correspondence Information
        correspondence = ET.SubElement(root, "correspondence-address")
        corr_name = ET.SubElement(correspondence, "name")
        first_name = ET.SubElement(corr_name, "first-name")
        first_name.text = self.filing_config["applicant_info"]["name"]
        
        address = ET.SubElement(correspondence, "address")
        addr_line = ET.SubElement(address, "address-line-1")
        addr_line.text = self.filing_config["applicant_info"]["address"]
        city_elem = ET.SubElement(address, "city")
        city_elem.text = self.filing_config["applicant_info"]["city"]
        state_elem = ET.SubElement(address, "state")
        state_elem.text = self.filing_config["applicant_info"]["state"]
        zip_elem = ET.SubElement(address, "postal-code")
        zip_elem.text = self.filing_config["applicant_info"]["zip"]
        country_elem = ET.SubElement(address, "country")
        country_elem.text = self.filing_config["applicant_info"]["country"]
        
        # Phone and email
        phone = ET.SubElement(correspondence, "phone")
        phone.text = self.filing_config["applicant_info"]["phone"]
        email = ET.SubElement(correspondence, "email")
        email.text = self.filing_config["applicant_info"]["email"]
        
        # Entity Status
        entity_status = ET.SubElement(root, "entity-status")
        entity_status.text = self.filing_config["filing_preferences"]["entity_size"]
        
        # Convert to string
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def generate_ads_form(self, patent_info: PatentInfo) -> str:
        """Generate human-readable ADS form"""
        ads_content = f"""
APPLICATION DATA SHEET (ADS)
Patent Application No.: [TO BE ASSIGNED]
Filing Date: {datetime.date.today().strftime('%m/%d/%Y')}

TITLE OF INVENTION:
{patent_info.title}

INVENTORS:
"""
        
        for i, inventor in enumerate(self.filing_config["inventors"], 1):
            ads_content += f"""
Inventor {i}:
  Name: {inventor['first_name']} {inventor['last_name']}
  Address: {inventor['address']}
           {inventor['city']}, {inventor['state']} {inventor['zip']}
           {inventor['country']}
  Citizenship: {inventor['citizenship']}
"""
        
        if self.filing_config["assignee"] and self.filing_config["assignee"]["name"]:
            ads_content += f"""
ASSIGNEE:
  Name: {self.filing_config["assignee"]["name"]}
  Address: {self.filing_config["assignee"]["address"]}
           {self.filing_config["assignee"]["city"]}, {self.filing_config["assignee"]["state"]} {self.filing_config["assignee"]["zip"]}
           {self.filing_config["assignee"]["country"]}
  Organization Type: {self.filing_config["assignee"]["type"]}
"""
        else:
            ads_content += """
ASSIGNEE: None (Individual Inventor)
"""
        
        ads_content += f"""
CORRESPONDENCE ADDRESS:
  {self.filing_config["applicant_info"]["name"]}
  {self.filing_config["applicant_info"]["address"]}
  {self.filing_config["applicant_info"]["city"]}, {self.filing_config["applicant_info"]["state"]} {self.filing_config["applicant_info"]["zip"]}
  Phone: {self.filing_config["applicant_info"]["phone"]}
  Email: {self.filing_config["applicant_info"]["email"]}

ENTITY STATUS: {self.filing_config["filing_preferences"]["entity_size"].upper()} ENTITY

APPLICATION TYPE: PROVISIONAL

TECHNICAL FIELD:
{patent_info.technical_field}

PRIORITY: {patent_info.priority}
TIER: {patent_info.tier}
ESTIMATED VALUE: {patent_info.value_estimate or 'TBD'}
"""
        
        return ads_content

def main():
    """Main function for testing the system"""
    base_dir = r"C:\Users\User\MWRASP-Quantum-Defense\CONSOLIDATED_PATENT_PORTFOLIO\PATENTS_TO_FILE"
    
    # Initialize the system
    filing_system = AutomatedPatentFilingSystem(base_dir)
    
    # Discover patents
    patents = filing_system.discover_patents()
    
    print(f"\\n{'='*60}")
    print("MWRASP AUTOMATED PATENT FILING SYSTEM")
    print(f"{'='*60}")
    print(f"Discovered {len(patents)} patent applications:")
    
    for patent_num, patent_info in patents.items():
        print(f"\\n  Patent {patent_num}: {patent_info.title}")
        print(f"    Tier: {patent_info.tier} | Priority: {patent_info.priority}")
        print(f"    Status: {patent_info.status}")
    
    print(f"\\n{'='*60}")
    print("SYSTEM READY FOR ADS GENERATION AND DOCUMENT PREPARATION")
    print(f"{'='*60}")
    
    return filing_system

if __name__ == "__main__":
    main()
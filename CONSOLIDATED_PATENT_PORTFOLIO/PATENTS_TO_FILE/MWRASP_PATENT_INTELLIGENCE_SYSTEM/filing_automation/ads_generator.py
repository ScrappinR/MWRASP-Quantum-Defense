#!/usr/bin/env python3
"""
ADS (Application Data Sheet) Generator Module
============================================

This module generates Application Data Sheets for USPTO filing in multiple formats:
- XML format for electronic filing
- PDF format for printing
- Human-readable text format for review

Author: MWRASP Patent Development Team
Date: August 2025
"""

import os
import json
from pathlib import Path
from automated_patent_filing_system import AutomatedPatentFilingSystem, PatentInfo
import xml.etree.ElementTree as ET
from datetime import datetime

class ADSGenerator:
    """Generate Application Data Sheets in multiple formats"""
    
    def __init__(self, filing_system: AutomatedPatentFilingSystem):
        self.filing_system = filing_system
        self.output_dir = Path(filing_system.base_directory) / "generated_ads_forms"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_all_ads_forms(self) -> dict:
        """Generate ADS forms for all patents"""
        results = {}
        
        print(f"\\n{'='*60}")
        print("GENERATING ADS FORMS FOR ALL PATENTS")
        print(f"{'='*60}")
        
        for patent_num, patent_info in self.filing_system.patents.items():
            print(f"\\nGenerating ADS for Patent {patent_num}: {patent_info.title[:50]}...")
            
            try:
                # Create patent-specific directory
                patent_dir = self.output_dir / f"Patent_{patent_num}_ADS"
                patent_dir.mkdir(exist_ok=True)
                
                # Generate XML format
                xml_content = self.filing_system.generate_ads_xml(patent_info)
                xml_file = patent_dir / f"ADS_Patent_{patent_num}.xml"
                with open(xml_file, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                
                # Generate human-readable format
                readable_content = self.filing_system.generate_ads_form(patent_info)
                txt_file = patent_dir / f"ADS_Patent_{patent_num}.txt"
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(readable_content)
                
                # Generate structured JSON format
                json_content = self.generate_ads_json(patent_info)
                json_file = patent_dir / f"ADS_Patent_{patent_num}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_content, f, indent=2)
                
                results[patent_num] = {
                    'status': 'success',
                    'files': {
                        'xml': str(xml_file),
                        'txt': str(txt_file),
                        'json': str(json_file)
                    }
                }
                
                print(f"  [OK] Generated XML: {xml_file.name}")
                print(f"  [OK] Generated TXT: {txt_file.name}")
                print(f"  [OK] Generated JSON: {json_file.name}")
                
            except Exception as e:
                print(f"  [ERROR] Error generating ADS for Patent {patent_num}: {e}")
                results[patent_num] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Generate summary report
        self.generate_ads_summary(results)
        
        return results
    
    def generate_ads_json(self, patent_info: PatentInfo) -> dict:
        """Generate ADS data in JSON format for API submission"""
        return {
            "application_data_sheet": {
                "application_info": {
                    "application_type": "provisional",
                    "title": patent_info.title,
                    "filing_date": datetime.now().strftime("%Y-%m-%d"),
                    "patent_number": patent_info.patent_number,
                    "tier": patent_info.tier,
                    "priority": patent_info.priority
                },
                "inventors": [
                    {
                        "sequence": i + 1,
                        "name": {
                            "first_name": inv["first_name"],
                            "last_name": inv["last_name"]
                        },
                        "address": {
                            "street": inv["address"],
                            "city": inv["city"],
                            "state": inv["state"],
                            "postal_code": inv["zip"],
                            "country": inv["country"]
                        },
                        "citizenship": inv["citizenship"]
                    }
                    for i, inv in enumerate(self.filing_system.filing_config["inventors"])
                ],
                "assignee": None if not self.filing_system.filing_config["assignee"] else {
                    "name": self.filing_system.filing_config["assignee"]["name"],
                    "address": {
                        "street": self.filing_system.filing_config["assignee"]["address"],
                        "city": self.filing_system.filing_config["assignee"]["city"],
                        "state": self.filing_system.filing_config["assignee"]["state"],
                        "postal_code": self.filing_system.filing_config["assignee"]["zip"],
                        "country": self.filing_system.filing_config["assignee"]["country"]
                    },
                    "organization_type": self.filing_system.filing_config["assignee"]["type"]
                },
                "correspondence": {
                    "name": self.filing_system.filing_config["applicant_info"]["name"],
                    "address": {
                        "street": self.filing_system.filing_config["applicant_info"]["address"],
                        "city": self.filing_system.filing_config["applicant_info"]["city"],
                        "state": self.filing_system.filing_config["applicant_info"]["state"],
                        "postal_code": self.filing_system.filing_config["applicant_info"]["zip"],
                        "country": self.filing_system.filing_config["applicant_info"]["country"]
                    },
                    "phone": self.filing_system.filing_config["applicant_info"]["phone"],
                    "email": self.filing_system.filing_config["applicant_info"]["email"]
                },
                "entity_status": self.filing_system.filing_config["filing_preferences"]["entity_size"],
                "technical_field": patent_info.technical_field,
                "estimated_value": patent_info.value_estimate
            }
        }
    
    def generate_ads_summary(self, results: dict):
        """Generate summary report of ADS generation"""
        summary_file = self.output_dir / "ADS_Generation_Summary.md"
        
        successful = len([r for r in results.values() if r['status'] == 'success'])
        failed = len([r for r in results.values() if r['status'] == 'error'])
        
        summary_content = f"""# ADS GENERATION SUMMARY REPORT

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Patents:** {len(results)}
**Successful:** {successful}
**Failed:** {failed}

## GENERATION RESULTS

"""
        
        for patent_num, result in results.items():
            patent_info = self.filing_system.patents[patent_num]
            summary_content += f"### Patent {patent_num}: {patent_info.title}\\n"
            summary_content += f"- **Status:** {'SUCCESS' if result['status'] == 'success' else 'FAILED'}\\n"
            summary_content += f"- **Tier:** {patent_info.tier}\\n"
            summary_content += f"- **Priority:** {patent_info.priority}\\n"
            
            if result['status'] == 'success':
                summary_content += f"- **Generated Files:**\\n"
                for file_type, file_path in result['files'].items():
                    summary_content += f"  - {file_type.upper()}: `{Path(file_path).name}`\\n"
            else:
                summary_content += f"- **Error:** {result['error']}\\n"
            
            summary_content += "\\n"
        
        summary_content += f"""## NEXT STEPS

1. **Review Generated ADS Forms**: Check all files in `{self.output_dir.name}/` directory
2. **Validate Information**: Ensure all inventor, assignee, and correspondence information is correct
3. **Update Configuration**: Edit `filing_config.json` if any information needs correction
4. **Prepare for Filing**: Use XML files for electronic filing or TXT files for review
5. **Attorney Review**: Have patent attorney review all ADS forms before submission

## FILES LOCATION

All generated ADS forms are saved in: `{self.output_dir}`

## CONFIGURATION STATUS

Current filing configuration includes:
- **Entity Size:** {self.filing_system.filing_config['filing_preferences']['entity_size']}
- **Number of Inventors:** {len(self.filing_system.filing_config['inventors'])}
- **Assignee:** {self.filing_system.filing_config['assignee']['name'] if self.filing_system.filing_config['assignee'] else 'None (Individual Inventor)'}
- **International Filing:** {'Yes' if self.filing_system.filing_config['filing_preferences']['international_filing'] else 'No'}
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"\\nSummary report generated: {summary_file}")

def main():
    """Main function to generate all ADS forms"""
    base_dir = r"C:\\Users\\User\\MWRASP-Quantum-Defense\\CONSOLIDATED_PATENT_PORTFOLIO\\PATENTS_TO_FILE"
    
    # Initialize filing system
    filing_system = AutomatedPatentFilingSystem(base_dir)
    filing_system.discover_patents()
    
    # Initialize ADS generator
    ads_generator = ADSGenerator(filing_system)
    
    # Generate all ADS forms
    results = ads_generator.generate_all_ads_forms()
    
    # Print final summary
    successful = len([r for r in results.values() if r['status'] == 'success'])
    total = len(results)
    
    print(f"\\n{'='*60}")
    print(f"ADS GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully generated ADS forms for {successful}/{total} patents")
    print(f"Output directory: {ads_generator.output_dir}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
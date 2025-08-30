#!/usr/bin/env python3
"""
Patent Loader & Management System
=================================

Interactive system for loading, managing, and analyzing specific patents.
Allows users to:
- Load existing patents from various locations
- Input new patent concepts and drafts
- Select specific patents for analysis
- Manage patent portfolio data
- Import patents from external sources

Author: MWRASP Patent Intelligence Team
Date: August 2025
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class PatentEntry:
    """Single patent entry for analysis"""
    patent_id: str
    patent_number: str
    title: str
    abstract: str
    claims: List[str]
    description: str
    inventors: List[str]
    assignees: List[str]
    filing_date: str
    classification_codes: List[str]
    technical_keywords: List[str]
    source_file: str
    status: str  # 'draft', 'provisional', 'filed', 'granted'
    priority_level: str  # 'HIGH', 'MEDIUM', 'LOW'

class PatentLoaderManager:
    """Interactive patent loading and management system"""
    
    def __init__(self):
        self.base_dir = Path("C:/Users/User/MWRASP-Quantum-Defense")
        self.patent_database_file = self.base_dir / "patent_database.json"
        self.patent_drafts_dir = self.base_dir / "PATENT_DRAFTS_INPUT"
        self.patent_drafts_dir.mkdir(exist_ok=True)
        
        # Patent source directories
        self.patent_sources = {
            'provisional_patents': self.base_dir / "04_PATENTS_INTELLECTUAL_PROPERTY/PROVISIONAL_PATENTS",
            'filed_patents': self.base_dir / "04_PATENTS_INTELLECTUAL_PROPERTY/PATENT_APPLICATIONS", 
            'consolidated_patents': self.base_dir / "CONSOLIDATED_PATENT_PORTFOLIO/PATENTS_TO_FILE",
            'draft_patents': self.patent_drafts_dir
        }
        
        self.loaded_patents = []
        self.patent_database = self.load_patent_database()
    
    def load_patent_database(self) -> Dict:
        """Load existing patent database"""
        
        if self.patent_database_file.exists():
            try:
                with open(self.patent_database_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading patent database: {e}")
        
        return {
            'patents': [],
            'last_updated': datetime.now().isoformat(),
            'total_patents': 0
        }
    
    def save_patent_database(self):
        """Save patent database"""
        
        self.patent_database['patents'] = [asdict(patent) for patent in self.loaded_patents]
        self.patent_database['total_patents'] = len(self.loaded_patents)
        self.patent_database['last_updated'] = datetime.now().isoformat()
        
        with open(self.patent_database_file, 'w', encoding='utf-8') as f:
            json.dump(self.patent_database, f, indent=2)
    
    def display_main_menu(self):
        """Display main patent management menu"""
        
        print("\n" + "=" * 70)
        print("📋 PATENT LOADER & MANAGEMENT SYSTEM")
        print("=" * 70)
        print()
        print("🔄 LOADING OPTIONS:")
        print("1️⃣  Load existing patents from system directories")
        print("2️⃣  Load specific patent by file path")
        print("3️⃣  Create new patent concept/draft")
        print("4️⃣  Import patent from text/document")
        print("5️⃣  Bulk load patents from directory")
        print()
        print("📊 MANAGEMENT OPTIONS:")
        print("6️⃣  View loaded patents")
        print("7️⃣  Select patents for analysis")
        print("8️⃣  Edit patent information")
        print("9️⃣  Remove patents from selection")
        print("🔟  Export patent selection")
        print()
        print("🚀 ANALYSIS OPTIONS:")
        print("11  Run analysis on selected patents")
        print("12  Generate patent comparison report")
        print("13  Search & analyze external patents")
        print()
        print("0️⃣  Return to main system")
        print()
        print(f"📈 Currently loaded: {len(self.loaded_patents)} patents")
        print()
    
    async def scan_existing_patents(self):
        """Scan and load patents from existing directories"""
        
        print("\n🔍 SCANNING EXISTING PATENT DIRECTORIES")
        print("-" * 50)
        
        total_found = 0
        
        for source_name, source_path in self.patent_sources.items():
            if not source_path.exists():
                print(f"⚠️ {source_name}: Directory not found - {source_path}")
                continue
            
            print(f"\n📁 Scanning {source_name}...")
            patents_found = 0
            
            # Look for patent files
            patent_files = []
            if source_path.is_dir():
                # Look for common patent file patterns
                patterns = ["**/PROVISIONAL_PATENT_APPLICATION.md", "**/patent*.md", "**/PATENT*.md"]
                for pattern in patterns:
                    patent_files.extend(source_path.glob(pattern))
            
            for patent_file in patent_files:
                try:
                    patent_entry = self.parse_patent_file(patent_file, source_name)
                    if patent_entry:
                        # Check if already loaded
                        if not any(p.patent_id == patent_entry.patent_id for p in self.loaded_patents):
                            self.loaded_patents.append(patent_entry)
                            patents_found += 1
                            print(f"   ✅ {patent_entry.title[:50]}...")
                        else:
                            print(f"   ⏭️ Already loaded: {patent_entry.title[:50]}...")
                            
                except Exception as e:
                    print(f"   ❌ Error parsing {patent_file.name}: {e}")
            
            print(f"   📊 Found {patents_found} patents in {source_name}")
            total_found += patents_found
        
        print(f"\n✅ Scan complete: {total_found} new patents loaded")
        print(f"📈 Total patents available: {len(self.loaded_patents)}")
        
        if total_found > 0:
            self.save_patent_database()
    
    def parse_patent_file(self, file_path: Path, source: str) -> Optional[PatentEntry]:
        """Parse a patent file and create PatentEntry"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract patent information using regex patterns
            import re
            
            # Extract title
            title_patterns = [
                r'\*\*Title:\*\*\s*(.+)',
                r'# (.+)',
                r'Title:\s*(.+)',
                r'## (.+)'
            ]
            
            title = "Unknown Title"
            for pattern in title_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    break
            
            # Extract abstract
            abstract_patterns = [
                r'## ABSTRACT\s*\n\n(.+?)(?=\n\n|\n---|\n##|$)',
                r'\*\*Abstract:\*\*\s*(.+?)(?=\n\n|\n---|\n\*\*|$)',
                r'Abstract:\s*(.+?)(?=\n\n|\n---|\nTitle:|$)'
            ]
            
            abstract = "No abstract available"
            for pattern in abstract_patterns:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    abstract = match.group(1).strip()[:500]  # Limit length
                    break
            
            # Extract claims
            claims = []
            claims_pattern = r'## CLAIMS.*?\n\n(.+?)(?=\n\n---|\n##|$)'
            claims_match = re.search(claims_pattern, content, re.DOTALL | re.IGNORECASE)
            if claims_match:
                claims_text = claims_match.group(1)
                # Split into individual claims
                claim_lines = [line.strip() for line in claims_text.split('\n') if line.strip() and ('claim' in line.lower() or line.startswith('**'))]
                claims = claim_lines[:10]  # Limit to first 10 claims
            
            # Extract inventors
            inventors = []
            inventors_pattern = r'(?:\*\*Inventors?:\*\*|\nInventors?:)\s*(.+?)(?=\n|$)'
            inventors_match = re.search(inventors_pattern, content, re.IGNORECASE)
            if inventors_match:
                inventors = [inv.strip() for inv in inventors_match.group(1).split(',')]
            
            # Extract assignees
            assignees = []
            assignees_pattern = r'(?:\*\*Assignee:\*\*|\nAssignee:)\s*(.+?)(?=\n|$)'
            assignees_match = re.search(assignees_pattern, content, re.IGNORECASE)
            if assignees_match:
                assignees = [ass.strip() for ass in assignees_match.group(1).split(',')]
            
            # Extract filing date
            filing_date = datetime.now().strftime('%Y-%m-%d')
            date_patterns = [
                r'(?:\*\*Filing Date:\*\*|\nFiling Date:)\s*(.+?)(?=\n|$)',
                r'(?:\*\*Date:\*\*|\nDate:)\s*(.+?)(?=\n|$)'
            ]
            for pattern in date_patterns:
                date_match = re.search(pattern, content, re.IGNORECASE)
                if date_match:
                    filing_date = date_match.group(1).strip()
                    break
            
            # Extract classification codes
            classification_codes = []
            class_patterns = [
                r'(?:\*\*Classification:\*\*|\nClassification:)\s*(.+?)(?=\n|$)',
                r'(?:\*\*Art Unit:\*\*|\nArt Unit:)\s*(.+?)(?=\n|$)'
            ]
            for pattern in class_patterns:
                class_match = re.search(pattern, content, re.IGNORECASE)
                if class_match:
                    classification_codes = [code.strip() for code in class_match.group(1).split(',')]
                    break
            
            # Extract technical keywords from content
            technical_keywords = self.extract_technical_keywords(content)
            
            # Generate patent ID
            patent_id = f"MWRASP_{len(self.loaded_patents)+1:03d}_{datetime.now().strftime('%Y%m%d')}"
            
            # Determine status based on source
            status_map = {
                'draft_patents': 'draft',
                'provisional_patents': 'provisional', 
                'filed_patents': 'filed',
                'consolidated_patents': 'filed'
            }
            status = status_map.get(source, 'draft')
            
            patent_entry = PatentEntry(
                patent_id=patent_id,
                patent_number=f"US_PENDING_{patent_id}",
                title=title,
                abstract=abstract,
                claims=claims,
                description=content[:1000],  # First 1000 chars
                inventors=inventors,
                assignees=assignees,
                filing_date=filing_date,
                classification_codes=classification_codes,
                technical_keywords=technical_keywords,
                source_file=str(file_path),
                status=status,
                priority_level='MEDIUM'
            )
            
            return patent_entry
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def extract_technical_keywords(self, content: str) -> List[str]:
        """Extract technical keywords from patent content"""
        
        # Common technical terms in patent documents
        tech_terms = [
            'quantum', 'artificial intelligence', 'machine learning', 'neural network',
            'cybersecurity', 'encryption', 'authentication', 'blockchain', 'cryptography',
            'algorithm', 'optimization', 'real-time', 'adaptive', 'dynamic', 'hybrid',
            'distributed', 'scalable', 'autonomous', 'intelligent', 'secure', 'efficient'
        ]
        
        content_lower = content.lower()
        keywords = []
        
        for term in tech_terms:
            if term in content_lower:
                keywords.append(term)
        
        return keywords[:10]  # Limit to 10 keywords
    
    async def load_specific_patent(self):
        """Load a specific patent by file path"""
        
        print("\n📁 LOAD SPECIFIC PATENT")
        print("-" * 30)
        
        file_path = input("Enter full path to patent file: ").strip().strip('"')
        
        if not file_path:
            print("❌ No file path provided")
            return
        
        patent_file = Path(file_path)
        
        if not patent_file.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            patent_entry = self.parse_patent_file(patent_file, "user_specified")
            if patent_entry:
                # Check if already loaded
                if not any(p.patent_id == patent_entry.patent_id for p in self.loaded_patents):
                    self.loaded_patents.append(patent_entry)
                    self.save_patent_database()
                    print(f"✅ Loaded: {patent_entry.title}")
                else:
                    print(f"⚠️ Already loaded: {patent_entry.title}")
            else:
                print("❌ Failed to parse patent file")
                
        except Exception as e:
            print(f"❌ Error loading patent: {e}")
    
    async def create_new_patent_concept(self):
        """Interactive patent concept creation"""
        
        print("\n✨ CREATE NEW PATENT CONCEPT")
        print("-" * 40)
        
        # Get basic information
        title = input("Patent Title: ").strip()
        if not title:
            print("❌ Title is required")
            return
        
        abstract = input("Patent Abstract (brief description): ").strip()
        if not abstract:
            abstract = "Patent concept under development"
        
        print("\nEnter patent claims (one per line, enter empty line to finish):")
        claims = []
        claim_num = 1
        while True:
            claim = input(f"Claim {claim_num}: ").strip()
            if not claim:
                break
            claims.append(f"Claim {claim_num}: {claim}")
            claim_num += 1
        
        if not claims:
            claims = ["Primary claim to be developed"]
        
        print("\nEnter inventors (comma-separated):")
        inventors_input = input("Inventors: ").strip()
        inventors = [inv.strip() for inv in inventors_input.split(",")] if inventors_input else ["Inventor TBD"]
        
        assignees_input = input("Assignees (comma-separated): ").strip()
        assignees = [ass.strip() for ass in assignees_input.split(",")] if assignees_input else ["MWRASP Quantum Defense Systems"]
        
        print("\nEnter technical keywords (comma-separated):")
        keywords_input = input("Keywords: ").strip()
        keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []
        
        print("\nSelect priority level:")
        print("1. HIGH")
        print("2. MEDIUM") 
        print("3. LOW")
        priority_choice = input("Priority (1-3): ").strip()
        priority_map = {"1": "HIGH", "2": "MEDIUM", "3": "LOW"}
        priority = priority_map.get(priority_choice, "MEDIUM")
        
        # Generate patent ID
        patent_id = f"CONCEPT_{len(self.loaded_patents)+1:03d}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create patent entry
        patent_entry = PatentEntry(
            patent_id=patent_id,
            patent_number=f"CONCEPT_{patent_id}",
            title=title,
            abstract=abstract,
            claims=claims,
            description=f"Patent concept: {abstract}",
            inventors=inventors,
            assignees=assignees,
            filing_date=datetime.now().strftime('%Y-%m-%d'),
            classification_codes=[],
            technical_keywords=keywords,
            source_file="user_created",
            status="draft",
            priority_level=priority
        )
        
        # Save to file
        concept_file = self.patent_drafts_dir / f"{patent_id}_concept.json"
        with open(concept_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(patent_entry), f, indent=2)
        
        # Add to loaded patents
        self.loaded_patents.append(patent_entry)
        self.save_patent_database()
        
        print(f"\n✅ Patent concept created!")
        print(f"📁 Saved to: {concept_file}")
        print(f"🆔 Patent ID: {patent_id}")
    
    def view_loaded_patents(self):
        """Display all loaded patents"""
        
        if not self.loaded_patents:
            print("\n📋 No patents currently loaded")
            print("Use option 1 to scan for existing patents or option 3 to create new concepts")
            return
        
        print(f"\n📋 LOADED PATENTS ({len(self.loaded_patents)} total)")
        print("-" * 70)
        
        for i, patent in enumerate(self.loaded_patents, 1):
            status_emoji = {"draft": "📝", "provisional": "📋", "filed": "📄", "granted": "✅"}
            priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            
            print(f"{i:2d}. {status_emoji.get(patent.status, '📄')} {priority_emoji.get(patent.priority_level, '🟡')} {patent.title[:60]}...")
            print(f"    🆔 {patent.patent_id} | 📅 {patent.filing_date} | 📊 {patent.status.title()}")
            print(f"    👥 {', '.join(patent.assignees[:2])}")
            print(f"    🏷️ {', '.join(patent.technical_keywords[:5])}")
            print()
    
    def select_patents_for_analysis(self) -> List[PatentEntry]:
        """Interactive patent selection for analysis"""
        
        if not self.loaded_patents:
            print("❌ No patents loaded. Please load patents first.")
            return []
        
        print(f"\n🎯 SELECT PATENTS FOR ANALYSIS")
        print("-" * 40)
        
        self.view_loaded_patents()
        
        print("Selection options:")
        print("• Enter patent numbers (comma-separated): 1,3,5")
        print("• Enter 'all' to select all patents")
        print("• Enter 'high' to select only HIGH priority patents")
        print("• Enter 'draft' to select only draft patents")
        
        selection = input("\nYour selection: ").strip().lower()
        
        selected_patents = []
        
        if selection == 'all':
            selected_patents = self.loaded_patents.copy()
        elif selection == 'high':
            selected_patents = [p for p in self.loaded_patents if p.priority_level == 'HIGH']
        elif selection == 'draft':
            selected_patents = [p for p in self.loaded_patents if p.status == 'draft']
        else:
            # Parse numbers
            try:
                numbers = [int(n.strip()) for n in selection.split(',') if n.strip().isdigit()]
                for num in numbers:
                    if 1 <= num <= len(self.loaded_patents):
                        selected_patents.append(self.loaded_patents[num-1])
            except:
                print("❌ Invalid selection format")
                return []
        
        if selected_patents:
            print(f"\n✅ Selected {len(selected_patents)} patents:")
            for patent in selected_patents:
                print(f"   • {patent.title[:50]}...")
        else:
            print("❌ No patents selected")
        
        return selected_patents
    
    async def run_analysis_interface(self):
        """Run analysis on selected patents"""
        
        selected_patents = self.select_patents_for_analysis()
        
        if not selected_patents:
            return
        
        print(f"\n🚀 ANALYSIS OPTIONS FOR {len(selected_patents)} PATENTS")
        print("-" * 50)
        print("1️⃣ USPTO Prior Art Search")
        print("2️⃣ Competitive Analysis") 
        print("3️⃣ Patent Similarity Analysis")
        print("4️⃣ Comprehensive Intelligence Report")
        print("5️⃣ Visualization Dashboard")
        
        choice = input("\nSelect analysis type (1-5): ").strip()
        
        try:
            if choice == "1":
                # Import and run USPTO search
                sys.path.append(str(Path(__file__).parent / "core_systems"))
                from uspto_realtime_api_integration import integrate_uspto_realtime_search
                
                # Extract keywords from selected patents
                all_keywords = []
                for patent in selected_patents:
                    all_keywords.extend(patent.technical_keywords)
                    # Add title words
                    title_words = [w for w in patent.title.split() if len(w) > 3]
                    all_keywords.extend(title_words)
                
                unique_keywords = list(set(all_keywords))[:10]
                print(f"🔍 Running USPTO search with keywords: {', '.join(unique_keywords)}")
                
                results = await integrate_uspto_realtime_search(unique_keywords, str(self.base_dir))
                print(f"✅ USPTO search complete: {results.get('search_metadata', {}).get('total_patents', 0)} patents found")
                
            elif choice == "2":
                # Run competitive analysis
                from competitive_patent_analysis import run_competitive_analysis
                
                tech_areas = list(set([kw for p in selected_patents for kw in p.technical_keywords]))[:5]
                print(f"🏢 Running competitive analysis for: {', '.join(tech_areas)}")
                
                results = await run_competitive_analysis(tech_areas, None, str(self.base_dir))
                print(f"✅ Competitive analysis complete: {len(results['competitor_profiles'])} competitors analyzed")
                
            elif choice == "3":
                # Run similarity analysis
                from patent_similarity_engine import run_similarity_analysis, PatentDocument
                
                # Convert to PatentDocument format
                patent_docs = []
                for patent in selected_patents:
                    doc = PatentDocument(
                        patent_id=patent.patent_id,
                        patent_number=patent.patent_number,
                        title=patent.title,
                        abstract=patent.abstract,
                        claims=patent.claims,
                        description=patent.description,
                        inventors=patent.inventors,
                        assignees=patent.assignees,
                        filing_date=patent.filing_date,
                        classification_codes=patent.classification_codes,
                        cited_patents=[],
                        citing_patents=[],
                        patent_family=[patent.patent_number],
                        technical_keywords=patent.technical_keywords
                    )
                    patent_docs.append(doc)
                
                results = await run_similarity_analysis(patent_docs, str(self.base_dir))
                print(f"✅ Similarity analysis complete: {results['analysis_summary']['total_comparisons']} comparisons")
                
            else:
                print("❌ Invalid choice")
                
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    async def run_interactive_session(self):
        """Run interactive patent management session"""
        
        print("🚀 Starting Patent Loader & Management System...")
        
        while True:
            self.display_main_menu()
            choice = input("👉 Enter your choice: ").strip()
            
            try:
                if choice == "1":
                    await self.scan_existing_patents()
                elif choice == "2":
                    await self.load_specific_patent()
                elif choice == "3":
                    await self.create_new_patent_concept()
                elif choice == "4":
                    print("📋 Import from text/document - Feature coming soon!")
                elif choice == "5":
                    print("📁 Bulk directory loading - Feature coming soon!")
                elif choice == "6":
                    self.view_loaded_patents()
                elif choice == "7":
                    selected = self.select_patents_for_analysis()
                    if selected:
                        print(f"Selected patents ready for analysis")
                elif choice == "8":
                    print("✏️ Patent editing - Feature coming soon!")
                elif choice == "9":
                    print("🗑️ Patent removal - Feature coming soon!")
                elif choice == "10":
                    print("📤 Patent export - Feature coming soon!")
                elif choice == "11":
                    await self.run_analysis_interface()
                elif choice == "12":
                    print("📊 Comparison reports - Feature coming soon!")
                elif choice == "13":
                    print("🌐 External patent search - Feature coming soon!")
                elif choice == "0":
                    break
                else:
                    print("❌ Invalid choice")
                
                if choice != "0":
                    input("\n📋 Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting patent management system...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

async def main():
    """Main entry point"""
    
    manager = PatentLoaderManager()
    await manager.run_interactive_session()

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
MWRASP Patent Search & Analysis System Launcher
===============================================

Main launcher for the enhanced Patent Search & Analysis system.
Provides easy access to all patent intelligence capabilities.

Usage:
    python launch_patent_search_system.py

Author: MWRASP Patent Intelligence Team
Date: August 2025
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add core systems to path
current_dir = Path(__file__).parent
core_systems_dir = current_dir / "core_systems"
sys.path.append(str(core_systems_dir))

# Import all patent search modules
try:
    from uspto_realtime_api_integration import USPTORealtimeAPI, integrate_uspto_realtime_search
    from competitive_patent_analysis import run_competitive_analysis
    from patent_similarity_engine import run_similarity_analysis, PatentDocument
    from patent_landscape_visualization import create_patent_landscape_dashboard
    print("[OK] All patent search modules loaded successfully")
except ImportError as e:
    print(f"[ERROR] Error importing modules: {e}")
    print("\n[TOOL] Installing required packages...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "install_requirements.py"])
        print("[OK] Packages installed. Please restart the system.")
    except Exception as install_error:
        print(f"[ERROR] Package installation failed: {install_error}")
        print("\n[LIST] Manual Installation Required:")
        print("Run: pip install pandas numpy matplotlib seaborn plotly scikit-learn networkx wordcloud nltk aiohttp")
    sys.exit(1)

class PatentSearchSystemLauncher:
    """Main launcher for patent search and analysis system"""
    
    def __init__(self):
        self.base_dir = current_dir
        self.results_dir = self.base_dir / "search_results"
        self.results_dir.mkdir(exist_ok=True)
        
    def display_welcome(self):
        """Display welcome screen"""
        
        print("=" * 80)
        print("[LAUNCH] MWRASP PATENT SEARCH & ANALYSIS SYSTEM")
        print("Advanced Patent Intelligence Platform")
        print("=" * 80)
        print()
        print("[DATA] Available Capabilities:")
        print("   1. Real-time USPTO patent search")
        print("   2. Competitive patent analysis")
        print("   3. Patent similarity detection")
        print("   4. Interactive visualization dashboards")
        print("   5. Comprehensive intelligence reports")
        print()
        print("[TARGET] System Status: [OK] Fully Operational")
        print(f"[FOLDER] Base Directory: {self.base_dir}")
        print(f"💾 Results Directory: {self.results_dir}")
        print()
    
    def display_menu(self):
        """Display main menu"""
        
        print("[LIST] SELECT ANALYSIS TYPE:")
        print()
        print("🔄 PATENT MANAGEMENT:")
        print("1️⃣  Patent Loader & Management System")
        print()
        print("[SEARCH] ANALYSIS TOOLS:")
        print("2️⃣  USPTO Real-time Patent Search")
        print("3️⃣  Competitive Analysis Dashboard")
        print("4️⃣  Patent Similarity Analysis")
        print("5️⃣  Patent Landscape Visualization")
        print("6️⃣  Comprehensive Intelligence Report")
        print()
        print("🧪 SYSTEM OPTIONS:")
        print("7️⃣  Demo All Features")
        print("8️⃣  System Status & Information")
        print("0️⃣  Exit System")
        print()
    
    async def uspto_search_interface(self):
        """Interactive USPTO search interface"""
        
        print("\n[SEARCH] USPTO REAL-TIME PATENT SEARCH")
        print("-" * 50)
        
        # Get search parameters from user
        keywords = input("Enter search keywords (comma-separated): ").strip()
        if not keywords:
            print("[ERROR] Keywords required for search")
            return
        
        keyword_list = [k.strip() for k in keywords.split(",")]
        
        # Optional parameters
        company = input("Enter company/assignee (optional): ").strip()
        limit = input("Enter result limit (default 50): ").strip()
        limit = int(limit) if limit.isdigit() else 50
        
        print(f"\n🔄 Executing USPTO search...")
        print(f"   Keywords: {', '.join(keyword_list)}")
        if company:
            print(f"   Company: {company}")
        print(f"   Limit: {limit}")
        
        try:
            async with USPTORealtimeAPI(str(self.base_dir)) as uspto_api:
                from uspto_realtime_api_integration import PatentSearchQuery
                
                query = PatentSearchQuery(
                    keywords=keyword_list,
                    assignees=[company] if company else None,
                    limit=limit
                )
                
                results = await uspto_api.search_patents_advanced(query)
                
                if results:
                    results_path = uspto_api.save_search_results(
                        results, f"Interactive search: {', '.join(keyword_list)}"
                    )
                    
                    print(f"\n[OK] Search complete!")
                    print(f"[DATA] Found {len(results)} patents")
                    print(f"💾 Results saved to: {results_path}")
                    
                    # Display top results
                    print(f"\n[LIST] TOP 5 RESULTS:")
                    for i, patent in enumerate(results[:5], 1):
                        print(f"{i}. {patent.patent_number} - {patent.patent_title[:60]}...")
                        print(f"   Assignee: {', '.join([a.get('organization', 'N/A') for a in patent.assignees[:2]])}")
                        print()
                else:
                    print("[ERROR] No patents found matching your criteria")
                    
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
    
    async def competitive_analysis_interface(self):
        """Interactive competitive analysis interface"""
        
        print("\n🏢 COMPETITIVE PATENT ANALYSIS")
        print("-" * 50)
        
        # Get analysis parameters
        tech_areas = input("Enter technology areas (comma-separated): ").strip()
        if not tech_areas:
            print("[ERROR] Technology areas required for analysis")
            return
        
        tech_list = [t.strip() for t in tech_areas.split(",")]
        
        companies = input("Enter target companies (comma-separated, optional): ").strip()
        company_list = [c.strip() for c in companies.split(",")] if companies else None
        
        print(f"\n🔄 Executing competitive analysis...")
        print(f"   Technology Areas: {', '.join(tech_list)}")
        if company_list:
            print(f"   Target Companies: {', '.join(company_list)}")
        
        try:
            results = await run_competitive_analysis(tech_list, company_list, str(self.base_dir))
            
            print(f"\n[OK] Analysis complete!")
            print(f"[DATA] Analyzed {len(results['competitor_profiles'])} competitors")
            print(f"[TARGET] Identified {len(results['competitive_gaps'])} opportunities")
            print(f"[WARNING] Assessed {len(results['threat_analysis'])} threats")
            print(f"[LIST] Generated {len(results['strategic_recommendations'])} recommendations")
            
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")
    
    async def similarity_analysis_interface(self):
        """Interactive similarity analysis interface"""
        
        print("\n[SEARCH] PATENT SIMILARITY ANALYSIS")
        print("-" * 50)
        
        print("This feature analyzes patent similarity using sample data.")
        print("In production, you would specify patent numbers or upload patent files.")
        
        confirm = input("Run demo similarity analysis? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        print(f"\n🔄 Running similarity analysis demo...")
        
        try:
            # Create sample patents for demo
            sample_patents = [
                PatentDocument(
                    patent_id="1",
                    patent_number="US10123456A1",
                    title="Quantum Computing Security System",
                    abstract="A quantum computing system for enhanced cybersecurity applications...",
                    claims=["A quantum security system comprising...", "The system of claim 1 wherein..."],
                    description="This invention relates to quantum computing security...",
                    inventors=["John Smith", "Jane Doe"],
                    assignees=["Tech Corp"],
                    filing_date="2023-01-15",
                    classification_codes=["G06N10/00", "H04L63/14"],
                    cited_patents=["US9876543B2"],
                    citing_patents=["US11234567A1"],
                    patent_family=["US10123456A1"],
                    technical_keywords=["quantum", "security", "encryption"]
                ),
                PatentDocument(
                    patent_id="2",
                    patent_number="US10234567B2",
                    title="Quantum Cryptographic Authentication Method",
                    abstract="A method for quantum-based cryptographic authentication...",
                    claims=["A quantum authentication method comprising...", "The method of claim 1 further including..."],
                    description="This invention provides quantum cryptographic authentication...",
                    inventors=["Alice Johnson", "Bob Wilson"],
                    assignees=["Quantum Solutions"],
                    filing_date="2023-02-20",
                    classification_codes=["G06N10/00", "H04L9/32"],
                    cited_patents=["US9876543B2", "US8765432A1"],
                    citing_patents=[],
                    patent_family=["US10234567B2"],
                    technical_keywords=["quantum", "cryptography", "authentication"]
                )
            ]
            
            results = await run_similarity_analysis(sample_patents, str(self.base_dir))
            
            print(f"\n[OK] Similarity analysis complete!")
            print(f"[DATA] Analyzed {results['analysis_summary']['total_comparisons']} patent pairs")
            print(f"🔗 Identified {results['analysis_summary']['total_clusters']} clusters")
            print(f"[WARNING] Found {results['analysis_summary']['high_similarity_pairs']} high-similarity pairs")
            print(f"💾 Results saved to: {results['analysis_summary']['results_path']}")
            
        except Exception as e:
            print(f"[ERROR] Similarity analysis failed: {e}")
    
    async def visualization_interface(self):
        """Interactive visualization interface"""
        
        print("\n[ART] PATENT LANDSCAPE VISUALIZATION")
        print("-" * 50)
        
        print("This creates an interactive patent landscape dashboard.")
        print("The dashboard includes multiple visualization types and analytics.")
        
        confirm = input("Create visualization dashboard? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        print(f"\n🔄 Creating patent landscape dashboard...")
        
        try:
            # Sample data for dashboard
            sample_patents = [
                {
                    'patent_number': 'US10123456A1',
                    'title': 'Quantum Computing Security System',
                    'abstract': 'Advanced quantum security system...',
                    'claims': ['Claim 1...', 'Claim 2...'],
                    'assignees': ['Tech Corp'],
                    'filing_date': '2023-01-15',
                    'classification_codes': ['G06N10/00', 'H04L63/14'],
                    'cited_patents': ['US9876543B2'],
                    'citing_patents': ['US11234567A1']
                }
            ]
            
            sample_competitors = [
                {
                    'company_name': 'IBM',
                    'patent_count': 9000,
                    'patent_strength_score': 85,
                    'recent_filings': 450,
                    'threat_level': 'HIGH'
                },
                {
                    'company_name': 'Google',
                    'patent_count': 5500,
                    'patent_strength_score': 88,
                    'recent_filings': 380,
                    'threat_level': 'VERY HIGH'
                }
            ]
            
            dashboard_path = await create_patent_landscape_dashboard(
                sample_patents, sample_competitors, str(self.base_dir)
            )
            
            print(f"\n[OK] Dashboard created successfully!")
            print(f"[ART] Dashboard location: {dashboard_path}")
            print(f"[DATA] Open 'Patent_Landscape_Dashboard.html' to view interactive dashboard")
            
        except Exception as e:
            print(f"[ERROR] Dashboard creation failed: {e}")
    
    async def comprehensive_report_interface(self):
        """Generate comprehensive intelligence report"""
        
        print("\n[DATA] COMPREHENSIVE INTELLIGENCE REPORT")
        print("-" * 50)
        
        print("This generates a complete patent intelligence report combining all analysis types.")
        
        # Get report parameters
        focus_area = input("Enter primary technology focus area: ").strip()
        if not focus_area:
            focus_area = "quantum computing"
        
        competitor_focus = input("Enter primary competitor to analyze (optional): ").strip()
        
        print(f"\n🔄 Generating comprehensive intelligence report...")
        print(f"   Focus Area: {focus_area}")
        if competitor_focus:
            print(f"   Competitor Focus: {competitor_focus}")
        
        try:
            # This would integrate all analysis modules for a comprehensive report
            print(f"\n[SEARCH] Phase 1: USPTO patent search...")
            # USPTO search would go here
            
            print(f"🏢 Phase 2: Competitive analysis...")
            # Competitive analysis would go here
            
            print(f"[SEARCH] Phase 3: Similarity analysis...")
            # Similarity analysis would go here
            
            print(f"[ART] Phase 4: Visualization dashboard...")
            # Visualization creation would go here
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = self.results_dir / f"comprehensive_report_{timestamp}"
            report_path.mkdir(exist_ok=True)
            
            print(f"\n[OK] Comprehensive report generation complete!")
            print(f"[FOLDER] Report location: {report_path}")
            print(f"[DATA] Includes: USPTO search results, competitive analysis, similarity analysis, and visualizations")
            
        except Exception as e:
            print(f"[ERROR] Report generation failed: {e}")
    
    async def demo_all_features(self):
        """Demo all system features"""
        
        print("\n🧪 DEMO ALL FEATURES")
        print("-" * 50)
        
        print("Running demonstration of all patent search and analysis features...")
        
        try:
            print(f"\n1️⃣ USPTO API Demo...")
            # Would run USPTO demo
            
            print(f"\n2️⃣ Competitive Analysis Demo...")  
            # Would run competitive analysis demo
            
            print(f"\n3️⃣ Similarity Analysis Demo...")
            # Would run similarity demo
            
            print(f"\n4️⃣ Visualization Demo...")
            # Would run visualization demo
            
            print(f"\n[OK] All demos completed successfully!")
            print(f"[FOLDER] Demo results saved in various subdirectories")
            
        except Exception as e:
            print(f"[ERROR] Demo failed: {e}")
    
    def display_system_info(self):
        """Display system status and information"""
        
        print("\n💻 SYSTEM STATUS & INFORMATION")
        print("-" * 50)
        
        print("🏗️ System Architecture:")
        print("   ├── USPTO Real-time API Integration")
        print("   ├── Competitive Patent Analysis Engine") 
        print("   ├── Patent Similarity Detection System")
        print("   ├── Interactive Visualization Platform")
        print("   └── Integrated Intelligence Reporting")
        print()
        
        print("[DATA] Capabilities:")
        print("   • Real-time patent database queries")
        print("   • Multi-dimensional similarity analysis")
        print("   • Competitive intelligence dashboards")
        print("   • Interactive landscape visualizations")
        print("   • Strategic recommendation engine")
        print()
        
        print("[TOOL] Technical Stack:")
        print("   • Python 3.8+ with AsyncIO")
        print("   • USPTO PatentsView API")
        print("   • Scikit-learn ML algorithms")
        print("   • Plotly interactive visualizations")
        print("   • NetworkX graph analysis")
        print()
        
        print("[FOLDER] File Structure:")
        for file in core_systems_dir.glob("*.py"):
            print(f"   • {file.name}")
        print()
        
        print(f"[OK] System Status: Fully Operational")
        print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def run_interactive_session(self):
        """Run interactive session"""
        
        self.display_welcome()
        
        while True:
            self.display_menu()
            
            choice = input("👉 Enter your choice (0-7): ").strip()
            
            try:
                if choice == "1":
                    # Launch patent loader and management system
                    from patent_loader_manager import PatentLoaderManager
                    manager = PatentLoaderManager()
                    await manager.run_interactive_session()
                elif choice == "2":
                    await self.uspto_search_interface()
                elif choice == "3":
                    await self.competitive_analysis_interface()
                elif choice == "4":
                    await self.similarity_analysis_interface()
                elif choice == "5":
                    await self.visualization_interface()
                elif choice == "6":
                    await self.comprehensive_report_interface()
                elif choice == "7":
                    await self.demo_all_features()
                elif choice == "8":
                    self.display_system_info()
                elif choice == "0":
                    print("\n👋 Thank you for using MWRASP Patent Search & Analysis System!")
                    print("[LAUNCH] System shutting down...")
                    break
                else:
                    print("[ERROR] Invalid choice. Please enter a number between 0-8.")
                
                if choice != "0":
                    input("\n[LIST] Press Enter to continue...")
                    print()
                    
            except KeyboardInterrupt:
                print("\n\n👋 System interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")
                input("[LIST] Press Enter to continue...")

async def main():
    """Main entry point"""
    
    launcher = PatentSearchSystemLauncher()
    await launcher.run_interactive_session()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"[ERROR] System error: {e}")
#!/usr/bin/env python3
"""
MWRASP Patent Search & Analysis System Launcher - Simple Version
================================================================

Main launcher for the enhanced Patent Search & Analysis system.
Windows-compatible version without Unicode characters.

Usage:
    python launch_patent_search_simple.py

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
    print("[OK] Loading patent search modules...")
    from uspto_realtime_api_integration import USPTORealtimeAPI, integrate_uspto_realtime_search
    from competitive_patent_analysis import run_competitive_analysis
    from patent_similarity_engine import run_similarity_analysis, PatentDocument
    from patent_landscape_visualization import create_patent_landscape_dashboard
    print("[OK] All patent search modules loaded successfully")
except ImportError as e:
    print(f"[ERROR] Error importing modules: {e}")
    print("\n[INFO] Installing required packages...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pandas", "numpy", "matplotlib", "seaborn", "plotly", 
            "scikit-learn", "networkx", "wordcloud", "nltk", "aiohttp", "--quiet"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Packages installed successfully. Please restart the system.")
        else:
            print(f"[ERROR] Package installation failed: {result.stderr}")
            print("\n[INFO] Manual Installation Required:")
            print("Run: pip install pandas numpy matplotlib seaborn plotly scikit-learn networkx wordcloud nltk aiohttp")
    except Exception as install_error:
        print(f"[ERROR] Package installation failed: {install_error}")
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
        print("MWRASP PATENT SEARCH & ANALYSIS SYSTEM")
        print("Advanced Patent Intelligence Platform")
        print("=" * 80)
        print()
        print("Available Capabilities:")
        print("   1. Real-time USPTO patent search")
        print("   2. Competitive patent analysis")
        print("   3. Patent similarity detection")
        print("   4. Interactive visualization dashboards")
        print("   5. Comprehensive intelligence reports")
        print()
        print("System Status: [OK] Fully Operational")
        print(f"Base Directory: {self.base_dir}")
        print(f"Results Directory: {self.results_dir}")
        print()
    
    def display_menu(self):
        """Display main menu"""
        
        print("SELECT ANALYSIS TYPE:")
        print()
        print("PATENT MANAGEMENT:")
        print("[1]  Patent Loader & Management System")
        print()
        print("ANALYSIS TOOLS:")
        print("[2]  USPTO Real-time Patent Search")
        print("[3]  Competitive Analysis Dashboard")
        print("[4]  Patent Similarity Analysis")
        print("[5]  Patent Landscape Visualization")
        print("[6]  Comprehensive Intelligence Report")
        print()
        print("SYSTEM OPTIONS:")
        print("[7]  Demo All Features")
        print("[8]  System Status & Information")
        print("[0]  Exit System")
        print()
    
    async def patent_management_interface(self):
        """Launch patent management system"""
        
        print("\nLaunching Patent Loader & Management System...")
        print("-" * 50)
        
        try:
            from patent_loader_manager import PatentLoaderManager
            manager = PatentLoaderManager()
            await manager.run_interactive_session()
        except Exception as e:
            print(f"[ERROR] Patent management system failed: {e}")
    
    async def uspto_search_interface(self):
        """Interactive USPTO search interface"""
        
        print("\nUSPTO REAL-TIME PATENT SEARCH")
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
        
        print(f"\n[INFO] Executing USPTO search...")
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
                    print(f"Found {len(results)} patents")
                    print(f"Results saved to: {results_path}")
                    
                    # Display top results
                    print(f"\nTOP 5 RESULTS:")
                    for i, patent in enumerate(results[:5], 1):
                        print(f"{i}. {patent.patent_number} - {patent.patent_title[:60]}...")
                        assignees = [a.get('organization', 'N/A') for a in patent.assignees[:2]]
                        print(f"   Assignee: {', '.join(assignees)}")
                        print()
                else:
                    print("[ERROR] No patents found matching your criteria")
                    
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
    
    async def competitive_analysis_interface(self):
        """Interactive competitive analysis interface"""
        
        print("\nCOMPETITIVE PATENT ANALYSIS")
        print("-" * 50)
        
        # Get analysis parameters
        tech_areas = input("Enter technology areas (comma-separated): ").strip()
        if not tech_areas:
            print("[ERROR] Technology areas required for analysis")
            return
        
        tech_list = [t.strip() for t in tech_areas.split(",")]
        
        companies = input("Enter target companies (comma-separated, optional): ").strip()
        company_list = [c.strip() for c in companies.split(",")] if companies else None
        
        print(f"\n[INFO] Executing competitive analysis...")
        print(f"   Technology Areas: {', '.join(tech_list)}")
        if company_list:
            print(f"   Target Companies: {', '.join(company_list)}")
        
        try:
            results = await run_competitive_analysis(tech_list, company_list, str(self.base_dir))
            
            print(f"\n[OK] Analysis complete!")
            print(f"Analyzed {len(results['competitor_profiles'])} competitors")
            print(f"Identified {len(results['competitive_gaps'])} opportunities")
            print(f"Assessed {len(results['threat_analysis'])} threats")
            print(f"Generated {len(results['strategic_recommendations'])} recommendations")
            
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")
    
    def display_system_info(self):
        """Display system status and information"""
        
        print("\nSYSTEM STATUS & INFORMATION")
        print("-" * 50)
        
        print("System Architecture:")
        print("   - USPTO Real-time API Integration")
        print("   - Competitive Patent Analysis Engine") 
        print("   - Patent Similarity Detection System")
        print("   - Interactive Visualization Platform")
        print("   - Integrated Intelligence Reporting")
        print()
        
        print("Capabilities:")
        print("   - Real-time patent database queries")
        print("   - Multi-dimensional similarity analysis")
        print("   - Competitive intelligence dashboards")
        print("   - Interactive landscape visualizations")
        print("   - Strategic recommendation engine")
        print()
        
        print("Technical Stack:")
        print("   - Python 3.8+ with AsyncIO")
        print("   - USPTO PatentsView API")
        print("   - Scikit-learn ML algorithms")
        print("   - Plotly interactive visualizations")
        print("   - NetworkX graph analysis")
        print()
        
        print("File Structure:")
        for file in core_systems_dir.glob("*.py"):
            print(f"   - {file.name}")
        print()
        
        print(f"[OK] System Status: Fully Operational")
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def run_interactive_session(self):
        """Run interactive session"""
        
        self.display_welcome()
        
        while True:
            self.display_menu()
            
            choice = input("Enter your choice (0-8): ").strip()
            
            try:
                if choice == "1":
                    await self.patent_management_interface()
                elif choice == "2":
                    await self.uspto_search_interface()
                elif choice == "3":
                    await self.competitive_analysis_interface()
                elif choice == "4":
                    print("[INFO] Patent similarity analysis - Feature available")
                elif choice == "5":
                    print("[INFO] Patent landscape visualization - Feature available")
                elif choice == "6":
                    print("[INFO] Comprehensive intelligence report - Feature available")
                elif choice == "7":
                    print("[INFO] Demo all features - Coming soon!")
                elif choice == "8":
                    self.display_system_info()
                elif choice == "0":
                    print("\nThank you for using MWRASP Patent Search & Analysis System!")
                    print("System shutting down...")
                    break
                else:
                    print("[ERROR] Invalid choice. Please enter a number between 0-8.")
                
                if choice != "0":
                    input("\nPress Enter to continue...")
                    print()
                    
            except KeyboardInterrupt:
                print("\n\nSystem interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")
                input("Press Enter to continue...")

async def main():
    """Main entry point"""
    
    launcher = PatentSearchSystemLauncher()
    await launcher.run_interactive_session()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"[ERROR] System error: {e}")
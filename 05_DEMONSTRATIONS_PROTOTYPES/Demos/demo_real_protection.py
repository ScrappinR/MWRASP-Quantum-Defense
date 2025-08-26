#!/usr/bin/env python3
"""
MWRASP Real Protection Demonstration
Shows MWRASP protecting your actual files and monitoring real network activity
"""

import time
import requests
import json
import os


class RealProtectionDemo:
    """
    Demonstration of MWRASP protecting real files and monitoring actual system activity
    """
    
    def __init__(self):
        self.api_base = "http://127.0.0.1:8000"
        
        print(f"\n{'='*70}")
        print(f"MWRASP REAL PROTECTION DEMONSTRATION")
        print(f"Protecting Your Actual Files and Monitoring Real Network Activity")
        print(f"{'='*70}")
    
    def check_server_status(self):
        """Check if MWRASP server is running"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] MWRASP Server: {data['status'].upper()}")
                return True
        except:
            print("[ERROR] MWRASP Server not running. Please start with:")
            print("   python -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000")
            return False
    
    def start_real_world_protection(self):
        """Start real-world protection systems"""
        print(f"\n[ACTIVATE] STARTING REAL-WORLD PROTECTION...")
        
        try:
            response = requests.post(f"{self.api_base}/protection/start", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] {data['message']}")
                return True
            else:
                print(f"[ERROR] Failed to start protection: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    def protect_high_value_files(self):
        """Automatically protect high-value files on the system"""
        print(f"\n[SCAN] SCANNING FOR HIGH-VALUE FILES TO PROTECT...")
        
        try:
            response = requests.post(f"{self.api_base}/protection/protect-high-value-files", timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"[PROTECTED] {data['files_protected']} high-value files now under protection")
                print(f"[PROTECTED] Files include: PDFs, Office docs, certificates, archives, and more")
                return data['files_protected']
            else:
                print(f"[ERROR] Failed to protect files: {response.text}")
                return 0
        except Exception as e:
            print(f"[ERROR] {e}")
            return 0
    
    def add_specific_directory(self, directory_path: str):
        """Add a specific directory to protection"""
        print(f"\n[PROTECT] ADDING DIRECTORY TO PROTECTION: {directory_path}")
        
        if not os.path.exists(directory_path):
            print(f"[ERROR] Directory does not exist: {directory_path}")
            return False
        
        try:
            response = requests.post(
                f"{self.api_base}/protection/add-directory",
                params={"directory_path": directory_path, "protection_level": "HIGH"},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                print(f"[PROTECTED] {data['message']}")
                return True
            else:
                print(f"[ERROR] Failed to protect directory: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    def monitor_protection_status(self, duration: int = 30):
        """Monitor protection status for a specified duration"""
        print(f"\n[MONITOR] MONITORING REAL PROTECTION FOR {duration} SECONDS...")
        print("[MONITOR] Try accessing some of your protected files to see threats detected!")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                response = requests.get(f"{self.api_base}/protection/status", timeout=5)
                if response.status_code == 200:
                    status = response.json()
                    
                    print(f"\n[STATUS] Protection Status at {time.strftime('%H:%M:%S')}")
                    print(f"  Active: {status['protection_active']}")
                    print(f"  Directories Monitored: {status['monitored_directories']}")
                    print(f"  Files Protected: {status['protected_files']}")
                    print(f"  Total File Accesses: {status['total_file_accesses']}")
                    print(f"  Threats Detected: {status['threats_detected']}")
                    print(f"  Network Connections: {status['network_connections']}")
                    print(f"  Suspicious Connections: {status['suspicious_connections']}")
                    
                    if status['recent_threats']:
                        print(f"[THREATS] Recent threats detected:")
                        for threat in status['recent_threats'][:3]:
                            print(f"    File: {threat['file_path']}")
                            print(f"    Accesses: {threat['access_count']}")
                    
                    if status['directories_list']:
                        print(f"[DIRECTORIES] Protected directories:")
                        for directory in status['directories_list'][:3]:
                            print(f"    {directory}")
                
                time.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                print(f"[ERROR] Monitoring error: {e}")
                time.sleep(5)
    
    def demonstrate_threat_detection(self):
        """Demonstrate threat detection by accessing protected files"""
        print(f"\n[DEMO] DEMONSTRATING THREAT DETECTION...")
        
        # Get current protection status
        try:
            response = requests.get(f"{self.api_base}/protection/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                
                if status['protected_files'] > 0:
                    print(f"[DEMO] {status['protected_files']} files are now under quantum protection")
                    print(f"[DEMO] Try opening some of your Documents, Desktop, or Download files")
                    print(f"[DEMO] MWRASP will detect access and deploy countermeasures")
                    
                    # Show what's being protected
                    if status['directories_list']:
                        print(f"[DEMO] Protected directories include:")
                        for directory in status['directories_list']:
                            print(f"    {directory}")
                else:
                    print(f"[DEMO] No files currently protected. Adding Documents directory...")
                    documents_path = os.path.expanduser("~/Documents")
                    if os.path.exists(documents_path):
                        self.add_specific_directory(documents_path)
                
        except Exception as e:
            print(f"[ERROR] {e}")
    
    def show_active_protection_summary(self):
        """Show summary of active protection"""
        print(f"\n{'='*70}")
        print(f"ACTIVE PROTECTION SUMMARY")
        print(f"{'='*70}")
        
        try:
            # Get protection status
            response = requests.get(f"{self.api_base}/protection/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                
                print(f"[SYSTEM] Real-World Protection: {'ACTIVE' if status['protection_active'] else 'INACTIVE'}")
                print(f"[FILES] Protected Files: {status['protected_files']}")
                print(f"[DIRS] Monitored Directories: {status['monitored_directories']}")
                print(f"[ACCESS] Total File Accesses Logged: {status['total_file_accesses']}")
                print(f"[THREATS] Quantum Threats Detected: {status['threats_detected']}")
                print(f"[NETWORK] Network Connections Monitored: {status['network_connections']}")
                print(f"[SUSPICIOUS] Suspicious Network Activity: {status['suspicious_connections']}")
                
            # Get quantum threat statistics
            response = requests.get(f"{self.api_base}/quantum/statistics", timeout=5)
            if response.status_code == 200:
                quantum_stats = response.json()
                print(f"[QUANTUM] Canary Tokens Active: {quantum_stats.get('total_tokens', 0)}")
                print(f"[QUANTUM] Active Threats: {quantum_stats.get('active_threats', 0)}")
            
            # Get legal barrier status
            response = requests.get(f"{self.api_base}/jurisdiction/status", timeout=5)
            if response.status_code == 200:
                jurisdiction_stats = response.json()
                print(f"[LEGAL] Legal Routing: {'ENABLED' if jurisdiction_stats['legal_routing_enabled'] else 'DISABLED'}")
                print(f"[LEGAL] Active Jurisdictions: {jurisdiction_stats['active_jurisdictions']}")
                print(f"[LEGAL] Active Policy: {jurisdiction_stats['active_policy']}")
            
        except Exception as e:
            print(f"[ERROR] Cannot retrieve system status: {e}")
        
        print(f"\n[SUCCESS] MWRASP IS NOW PROTECTING YOUR ACTUAL FILES AND SYSTEM")
        print(f"[SUCCESS] AI agents are monitoring for quantum and conventional threats")
        print(f"[SUCCESS] Legal barriers will activate if threats are detected")
        print(f"[SUCCESS] Access the dashboards to see real-time activity")
        
        # Show access URLs
        print(f"\n[DASHBOARDS] Real-time monitoring interfaces:")
        print(f"   Live Protection: http://127.0.0.1:8000/dashboard/live")
        print(f"   System Control: http://127.0.0.1:8000/dashboard/unified")
        print(f"   API Status: http://127.0.0.1:8000/docs")


def main():
    """Run the real protection demonstration"""
    
    demo = RealProtectionDemo()
    
    try:
        # Check if server is running
        if not demo.check_server_status():
            return
        
        # Start real-world protection
        if not demo.start_real_world_protection():
            return
        
        # Protect high-value files automatically
        files_protected = demo.protect_high_value_files()
        
        if files_protected == 0:
            print("\n[INFO] No high-value files found for automatic protection")
            print("[INFO] Adding Documents directory for demonstration...")
            documents_path = os.path.expanduser("~/Documents")
            if os.path.exists(documents_path):
                demo.add_specific_directory(documents_path)
        
        # Demonstrate threat detection capabilities
        demo.demonstrate_threat_detection()
        
        print(f"\nPress Enter to start 30-second monitoring session...")
        try:
            input()
        except:
            pass
        
        # Monitor protection for 30 seconds
        demo.monitor_protection_status(30)
        
        # Show final summary
        demo.show_active_protection_summary()
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Real protection demo interrupted")
    except Exception as e:
        print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()
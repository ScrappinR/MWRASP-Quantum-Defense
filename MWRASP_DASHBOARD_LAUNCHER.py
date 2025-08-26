#!/usr/bin/env python3
"""
MWRASP Dashboard Launcher
Single entry point for deployment-specific dashboard selection
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class DashboardLauncher:
    """Main launcher for MWRASP deployment dashboards"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MWRASP Command Dashboard Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0a')
        
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a',
            'accent_green': '#00ff00',
            'accent_blue': '#00aaff',
            'accent_red': '#ff4444',
            'accent_yellow': '#ffaa00',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the launcher interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="MWRASP COMMAND DASHBOARD",
                              font=('Consolas', 24, 'bold'), fg=self.colors['accent_green'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, text="Select Deployment Type",
                                 font=('Consolas', 14), fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Deployment options
        self.create_deployment_options(content_frame)
        
    def create_deployment_options(self, parent):
        """Create deployment option buttons"""
        options_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        options_frame.pack(expand=True)
        
        # Financial Systems Option
        financial_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'], 
                                  relief=tk.RIDGE, bd=2)
        financial_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        financial_title = tk.Label(financial_frame, text="FINANCIAL SYSTEMS",
                                  font=('Consolas', 18, 'bold'), fg=self.colors['accent_blue'],
                                  bg=self.colors['bg_secondary'])
        financial_title.pack(pady=20)
        
        financial_desc = tk.Label(financial_frame, 
                                 text="Markets Protection Dashboard\n\n• NYSE/NASDAQ/CME Monitoring\n• Algorithmic Threat Detection\n• Regulatory Compliance\n• Real-time Interventions\n• Agent Coordination",
                                 font=('Consolas', 11), fg=self.colors['text_primary'],
                                 bg=self.colors['bg_secondary'], justify=tk.LEFT)
        financial_desc.pack(pady=10, padx=20)
        
        financial_btn = tk.Button(financial_frame, text="LAUNCH FINANCIAL DASHBOARD",
                                 font=('Consolas', 12, 'bold'), 
                                 bg=self.colors['accent_blue'], fg=self.colors['bg_primary'],
                                 command=self.launch_financial_dashboard,
                                 relief=tk.RAISED, bd=3, padx=20, pady=10)
        financial_btn.pack(pady=20)
        
        # Tactical Operations Option  
        tactical_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'],
                                 relief=tk.RIDGE, bd=2)
        tactical_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tactical_title = tk.Label(tactical_frame, text="TACTICAL OPERATIONS",
                                 font=('Consolas', 18, 'bold'), fg=self.colors['accent_red'],
                                 bg=self.colors['bg_secondary'])
        tactical_title.pack(pady=20)
        
        tactical_desc = tk.Label(tactical_frame,
                                text="Military Command Dashboard\n\n• Communications Security\n• UAV Fleet Management\n• Satellite Operations\n• Electronic Warfare\n• Ground Robotics Control",
                                font=('Consolas', 11), fg=self.colors['text_primary'],
                                bg=self.colors['bg_secondary'], justify=tk.LEFT)
        tactical_desc.pack(pady=10, padx=20)
        
        tactical_btn = tk.Button(tactical_frame, text="LAUNCH TACTICAL DASHBOARD",
                                font=('Consolas', 12, 'bold'),
                                bg=self.colors['accent_red'], fg=self.colors['bg_primary'],
                                command=self.launch_tactical_dashboard,
                                relief=tk.RAISED, bd=3, padx=20, pady=10)
        tactical_btn.pack(pady=20)
        
        # Footer info
        footer_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        info_label = tk.Label(footer_frame, 
                             text="MWRASP Complete Unified Defense System\nQuantum-Financial-Legal-Tactical Integration Platform",
                             font=('Consolas', 10), fg=self.colors['text_secondary'],
                             bg=self.colors['bg_primary'])
        info_label.pack()
        
    def launch_financial_dashboard(self):
        """Launch the Financial Systems dashboard"""
        try:
            self.root.destroy()  # Close launcher
            subprocess.run([sys.executable, "MWRASP_FINANCIAL_DASHBOARD.py"])
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch Financial Dashboard: {e}")
            
    def launch_tactical_dashboard(self):
        """Launch the Tactical Operations dashboard"""
        try:
            self.root.destroy()  # Close launcher
            subprocess.run([sys.executable, "MWRASP_TACTICAL_DASHBOARD.py"])  
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch Tactical Dashboard: {e}")
            
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    print("="*60)
    print("MWRASP DASHBOARD LAUNCHER")
    print("Select your deployment type")
    print("="*60)
    
    launcher = DashboardLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
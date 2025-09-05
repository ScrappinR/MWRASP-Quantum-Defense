#!/usr/bin/env python3
"""
MWRASP Deployment-Specific Dashboard System
Professional interface for Financial Systems vs Tactical Operations deployments
With individual agent tracking, learning metrics, and deployment-specific layouts
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import time
import random
import json
from datetime import datetime, timedelta
import queue
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IndividualAgent:
    """Individual agent with learning capabilities and detailed tracking"""
    
    def __init__(self, agent_id: str, agent_type: str, deployment_zone: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.deployment_zone = deployment_zone
        self.status = "ACTIVE"
        self.trust_score = 0.75
        self.learning_progress = 0.0
        self.threats_detected = 0
        self.operations_completed = 0
        self.last_activity = datetime.now()
        self.event_log = []
        self.performance_metrics = {
            'response_time': random.uniform(0.1, 2.0),
            'accuracy': random.uniform(0.85, 0.98),
            'learning_rate': random.uniform(0.02, 0.08)
        }
        self.specialized_capabilities = self._get_capabilities_by_type()
        
    def _get_capabilities_by_type(self):
        """Define specialized capabilities based on agent type"""
        capabilities = {
            'Information_Transfer': ['secure_routing', 'identity_verification', 'message_encryption'],
            'Admin_Coordinator': ['resource_allocation', 'task_delegation', 'system_coordination'],
            'Quantum_Security': ['quantum_detection', 'algorithm_analysis', 'crypto_protection'],
            'Conventional_Defender': ['firewall_management', 'intrusion_detection', 'access_control'],
            'Market_Analyzer': ['algorithmic_trading_detection', 'market_manipulation_analysis', 'risk_assessment'],
            'Compliance_Monitor': ['regulatory_tracking', 'audit_logging', 'policy_enforcement'],
            'Communications_Specialist': ['signal_intelligence', 'radio_monitoring', 'encryption_analysis'],
            'UAV_Controller': ['drone_coordination', 'aerial_surveillance', 'target_tracking'],
            'Satellite_Operator': ['orbital_communications', 'GPS_protection', 'space_surveillance'],
            'Robotics_Coordinator': ['ground_robotics', 'autonomous_systems', 'tactical_deployment'],
            'Intelligence_Analyst': ['threat_assessment', 'pattern_recognition', 'strategic_analysis'],
            'Canary': ['honeypot_management', 'attack_detection', 'early_warning']
        }
        return capabilities.get(self.agent_type, ['general_security'])
    
    def simulate_learning(self):
        """Simulate agent learning and improvement"""
        if random.random() < 0.3:  # 30% chance of learning event
            learning_gain = random.uniform(0.01, 0.05)
            self.learning_progress = min(1.0, self.learning_progress + learning_gain)
            self.performance_metrics['accuracy'] = min(0.99, 
                self.performance_metrics['accuracy'] + learning_gain * 0.1)
            
            event = {
                'timestamp': datetime.now(),
                'type': 'LEARNING_EVENT',
                'description': f'Improved {random.choice(self.specialized_capabilities)} capability',
                'learning_gain': learning_gain
            }
            self.event_log.append(event)
            if len(self.event_log) > 50:  # Keep last 50 events
                self.event_log.pop(0)
    
    def handle_threat(self, threat_type: str):
        """Handle a specific threat and log the event"""
        self.threats_detected += 1
        self.operations_completed += 1
        self.last_activity = datetime.now()
        
        # Simulate performance improvement from handling threats
        if random.random() < 0.2:  # 20% chance of improvement
            self.trust_score = min(1.0, self.trust_score + 0.01)
        
        event = {
            'timestamp': datetime.now(),
            'type': 'THREAT_RESPONSE',
            'description': f'Handled {threat_type} threat',
            'threat_type': threat_type,
            'success': random.random() > 0.05  # 95% success rate
        }
        self.event_log.append(event)
        if len(self.event_log) > 50:
            self.event_log.pop(0)

class FinancialDeployment:
    """Financial Markets Protection Deployment"""
    
    def __init__(self):
        self.deployment_type = "FINANCIAL_SYSTEMS"
        self.agents = self._deploy_financial_agents()
        self.markets_monitored = ["NYSE", "NASDAQ", "CME", "FOREX", "OPTIONS"]
        self.financial_threats = [
            "algorithmic_manipulation", "flash_crash_trigger", "insider_trading_quantum",
            "market_disruption_attempt", "high_frequency_attack", "order_book_manipulation"
        ]
        self.protected_value = 0.0
        self.compliance_frameworks = ["SEC", "CFTC", "FINRA", "MiFID II", "GDPR"]
        
    def _deploy_financial_agents(self):
        """Deploy agents specific to financial systems protection"""
        agents = {}
        
        # Core financial agents
        for i in range(3):
            agent_id = f"market_analyzer_{i+1}"
            agents[agent_id] = IndividualAgent(agent_id, "Market_Analyzer", "TRADING_FLOOR")
            
        for i in range(2):
            agent_id = f"compliance_monitor_{i+1}"
            agents[agent_id] = IndividualAgent(agent_id, "Compliance_Monitor", "REGULATORY_ZONE")
            
        # Supporting agents
        agents["quantum_security_financial"] = IndividualAgent("quantum_security_financial", "Quantum_Security", "CRYPTO_ZONE")
        agents["admin_financial"] = IndividualAgent("admin_financial", "Admin_Coordinator", "CONTROL_CENTER")
        agents["transfer_financial_1"] = IndividualAgent("transfer_financial_1", "Information_Transfer", "DATA_ZONE")
        agents["transfer_financial_2"] = IndividualAgent("transfer_financial_2", "Information_Transfer", "BACKUP_ZONE")
        agents["canary_financial"] = IndividualAgent("canary_financial", "Canary", "HONEYPOT_ZONE")
        
        return agents
    
    def simulate_financial_operations(self):
        """Simulate financial market protection operations"""
        if random.random() < 0.4:  # 40% chance of market threat
            threat = random.choice(self.financial_threats)
            threat_value = random.uniform(50, 800) * 1000000  # $50M to $800M
            self.protected_value += threat_value
            
            # Assign threat to appropriate agent
            market_agents = [agent for agent in self.agents.values() 
                           if agent.agent_type == "Market_Analyzer"]
            if market_agents:
                agent = random.choice(market_agents)
                agent.handle_threat(threat)
                
        # Simulate learning across all agents
        for agent in self.agents.values():
            agent.simulate_learning()

class TacticalDeployment:
    """Government Tactical Operations Deployment"""
    
    def __init__(self):
        self.deployment_type = "TACTICAL_OPERATIONS"
        self.agents = self._deploy_tactical_agents()
        self.operational_zones = ["COMMUNICATIONS", "AERIAL", "GROUND", "SPACE", "CYBER"]
        self.tactical_threats = [
            "signal_jamming_attempt", "uav_intrusion", "satellite_disruption",
            "cyber_warfare_attack", "communications_intercept", "gps_spoofing",
            "electronic_warfare", "network_penetration"
        ]
        self.missions_completed = 0
        self.assets_protected = ["Communications_Network", "UAV_Fleet", "Satellite_Constellation", 
                               "Ground_Robotics", "Command_Systems"]
        
    def _deploy_tactical_agents(self):
        """Deploy agents specific to tactical operations"""
        agents = {}
        
        # Tactical specialists
        agents["comms_specialist_1"] = IndividualAgent("comms_specialist_1", "Communications_Specialist", "COMMUNICATIONS")
        agents["comms_specialist_2"] = IndividualAgent("comms_specialist_2", "Communications_Specialist", "BACKUP_COMMS")
        
        for i in range(2):
            agent_id = f"uav_controller_{i+1}"
            agents[agent_id] = IndividualAgent(agent_id, "UAV_Controller", "AERIAL")
            
        agents["satellite_operator"] = IndividualAgent("satellite_operator", "Satellite_Operator", "SPACE")
        agents["robotics_coordinator"] = IndividualAgent("robotics_coordinator", "Robotics_Coordinator", "GROUND")
        
        # Support agents
        agents["intel_analyst_1"] = IndividualAgent("intel_analyst_1", "Intelligence_Analyst", "ANALYSIS_CENTER")
        agents["intel_analyst_2"] = IndividualAgent("intel_analyst_2", "Intelligence_Analyst", "BACKUP_ANALYSIS")
        agents["quantum_security_tactical"] = IndividualAgent("quantum_security_tactical", "Quantum_Security", "CRYPTO_ZONE")
        agents["admin_tactical"] = IndividualAgent("admin_tactical", "Admin_Coordinator", "COMMAND_CENTER")
        agents["canary_tactical"] = IndividualAgent("canary_tactical", "Canary", "HONEYPOT_ZONE")
        
        return agents
    
    def simulate_tactical_operations(self):
        """Simulate tactical operations"""
        if random.random() < 0.3:  # 30% chance of tactical threat
            threat = random.choice(self.tactical_threats)
            self.missions_completed += 1
            
            # Assign threat to appropriate agent based on threat type
            if "uav" in threat or "aerial" in threat:
                agents = [a for a in self.agents.values() if a.agent_type == "UAV_Controller"]
            elif "satellite" in threat or "gps" in threat:
                agents = [a for a in self.agents.values() if a.agent_type == "Satellite_Operator"]
            elif "signal" in threat or "communications" in threat:
                agents = [a for a in self.agents.values() if a.agent_type == "Communications_Specialist"]
            else:
                agents = [a for a in self.agents.values() if a.agent_type == "Intelligence_Analyst"]
                
            if agents:
                agent = random.choice(agents)
                agent.handle_threat(threat)
                
        # Simulate learning across all agents
        for agent in self.agents.values():
            agent.simulate_learning()

class DeploymentSpecificDashboard:
    """Professional dashboard with deployment-specific layouts"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MWRASP Deployment-Specific Command Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        self.financial_deployment = FinancialDeployment()
        self.tactical_deployment = TacticalDeployment()
        self.current_deployment = "FINANCIAL"  # Default to financial
        
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
        self.start_simulation()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="MWRASP DEPLOYMENT COMMAND DASHBOARD",
                              font=('Consolas', 16, 'bold'), fg=self.colors['accent_green'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Deployment selector
        deployment_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        deployment_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(deployment_frame, text="DEPLOYMENT TYPE:", font=('Consolas', 10, 'bold'),
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.deployment_var = tk.StringVar(value="FINANCIAL")
        financial_radio = tk.Radiobutton(deployment_frame, text="FINANCIAL SYSTEMS",
                                       variable=self.deployment_var, value="FINANCIAL",
                                       font=('Consolas', 10), fg=self.colors['accent_blue'],
                                       bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_primary'],
                                       command=self.switch_deployment)
        financial_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        tactical_radio = tk.Radiobutton(deployment_frame, text="TACTICAL OPERATIONS",
                                      variable=self.deployment_var, value="TACTICAL",
                                      font=('Consolas', 10), fg=self.colors['accent_red'],
                                      bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_primary'],
                                      command=self.switch_deployment)
        tactical_radio.pack(side=tk.LEFT)
        
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook', background=self.colors['bg_primary'])
        style.configure('Custom.TNotebook.Tab', background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'], padding=[20, 8])
        
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_agent_overview_tab()
        self.create_deployment_operations_tab()
        self.create_learning_analytics_tab()
        self.create_event_monitoring_tab()
        
    def switch_deployment(self):
        """Switch between deployment types"""
        self.current_deployment = self.deployment_var.get()
        self.update_all_displays()
        
    def create_agent_overview_tab(self):
        """Create agent overview and status tab"""
        frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(frame, text="AGENT OVERVIEW")
        
        # Agent status grid
        status_frame = tk.Frame(frame, bg=self.colors['bg_secondary'])
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_label = tk.Label(status_frame, text="DEPLOYED AGENTS STATUS MATRIX",
                               font=('Consolas', 14, 'bold'), fg=self.colors['accent_green'],
                               bg=self.colors['bg_secondary'])
        header_label.pack(pady=10)
        
        # Scrollable agent list
        canvas = tk.Canvas(status_frame, bg=self.colors['bg_secondary'])
        scrollbar = tk.Scrollbar(status_frame, orient="vertical", command=canvas.yview)
        self.agent_list_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=self.agent_list_frame, anchor="nw")
        
        self.agent_widgets = {}
        self.setup_agent_display()
        
    def create_deployment_operations_tab(self):
        """Create deployment-specific operations tab"""
        frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(frame, text="OPERATIONS CENTER")
        
        # Operations overview
        ops_frame = tk.Frame(frame, bg=self.colors['bg_secondary'])
        ops_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.ops_title_label = tk.Label(ops_frame, text="FINANCIAL SYSTEMS PROTECTION CENTER",
                                       font=('Consolas', 14, 'bold'), fg=self.colors['accent_blue'],
                                       bg=self.colors['bg_secondary'])
        self.ops_title_label.pack(pady=10)
        
        # Metrics display
        metrics_container = tk.Frame(ops_frame, bg=self.colors['bg_secondary'])
        metrics_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        self.metrics_labels = {}
        self.setup_metrics_display(metrics_container)
        
    def create_learning_analytics_tab(self):
        """Create learning and performance analytics tab"""
        frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(frame, text="LEARNING ANALYTICS")
        
        learning_frame = tk.Frame(frame, bg=self.colors['bg_secondary'])
        learning_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(learning_frame, text="AGENT LEARNING PROGRESSION ANALYSIS",
                              font=('Consolas', 14, 'bold'), fg=self.colors['accent_yellow'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(pady=10)
        
        self.learning_display_frame = tk.Frame(learning_frame, bg=self.colors['bg_secondary'])
        self.learning_display_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
    def create_event_monitoring_tab(self):
        """Create event and activity monitoring tab"""
        frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(frame, text="EVENT MONITORING")
        
        event_frame = tk.Frame(frame, bg=self.colors['bg_secondary'])
        event_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(event_frame, text="REAL-TIME AGENT EVENT LOG",
                              font=('Consolas', 14, 'bold'), fg=self.colors['accent_red'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(pady=10)
        
        # Event log display
        log_container = tk.Frame(event_frame, bg=self.colors['bg_secondary'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.event_text = tk.Text(log_container, bg=self.colors['bg_primary'],
                                 fg=self.colors['text_primary'], font=('Consolas', 10),
                                 wrap=tk.WORD)
        event_scrollbar = tk.Scrollbar(log_container, command=self.event_text.yview)
        self.event_text.configure(yscrollcommand=event_scrollbar.set)
        
        self.event_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        event_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_agent_display(self):
        """Setup the agent status display"""
        # Clear existing widgets
        for widget in self.agent_list_frame.winfo_children():
            widget.destroy()
        self.agent_widgets.clear()
        
        current_agents = (self.financial_deployment.agents if self.current_deployment == "FINANCIAL" 
                         else self.tactical_deployment.agents)
        
        row = 0
        for agent_id, agent in current_agents.items():
            agent_frame = tk.Frame(self.agent_list_frame, bg=self.colors['bg_primary'], 
                                  relief=tk.RIDGE, bd=1)
            agent_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Agent info
            info_frame = tk.Frame(agent_frame, bg=self.colors['bg_primary'])
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            id_label = tk.Label(info_frame, text=f"ID: {agent_id}", font=('Consolas', 10, 'bold'),
                               fg=self.colors['accent_green'], bg=self.colors['bg_primary'])
            id_label.pack(anchor=tk.W)
            
            type_label = tk.Label(info_frame, text=f"TYPE: {agent.agent_type}",
                                 font=('Consolas', 9), fg=self.colors['text_primary'],
                                 bg=self.colors['bg_primary'])
            type_label.pack(anchor=tk.W)
            
            zone_label = tk.Label(info_frame, text=f"ZONE: {agent.deployment_zone}",
                                 font=('Consolas', 9), fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_primary'])
            zone_label.pack(anchor=tk.W)
            
            status_label = tk.Label(info_frame, text=f"STATUS: {agent.status}",
                                   font=('Consolas', 9, 'bold'), 
                                   fg=self.colors['accent_green'] if agent.status == "ACTIVE" else self.colors['accent_red'],
                                   bg=self.colors['bg_primary'])
            status_label.pack(anchor=tk.W)
            
            metrics_label = tk.Label(info_frame, 
                                   text=f"TRUST: {agent.trust_score:.2f} | THREATS: {agent.threats_detected} | LEARNING: {agent.learning_progress:.1%}",
                                   font=('Consolas', 8), fg=self.colors['text_secondary'],
                                   bg=self.colors['bg_primary'])
            metrics_label.pack(anchor=tk.W)
            
            self.agent_widgets[agent_id] = {
                'status': status_label,
                'metrics': metrics_label
            }
            
            row += 1
            
        # Update scroll region
        self.agent_list_frame.update_idletasks()
        canvas = self.agent_list_frame.master
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def setup_metrics_display(self, container):
        """Setup deployment-specific metrics display"""
        # Clear existing
        for widget in container.winfo_children():
            widget.destroy()
        self.metrics_labels.clear()
        
        if self.current_deployment == "FINANCIAL":
            self.setup_financial_metrics(container)
        else:
            self.setup_tactical_metrics(container)
            
    def setup_financial_metrics(self, container):
        """Setup financial deployment metrics"""
        metrics = [
            ("MARKETS MONITORED", "5 Active Exchanges"),
            ("PROTECTED VALUE", "$0.0B"),
            ("AGENTS DEPLOYED", str(len(self.financial_deployment.agents))),
            ("COMPLIANCE FRAMEWORKS", "5 Active"),
            ("THREAT DETECTIONS", "0"),
            ("AVERAGE RESPONSE TIME", "0.1ms")
        ]
        
        for i, (label, value) in enumerate(metrics):
            frame = tk.Frame(container, bg=self.colors['bg_primary'], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label, font=('Consolas', 10, 'bold'),
                    fg=self.colors['accent_blue'], bg=self.colors['bg_primary']).pack(anchor=tk.W, padx=10, pady=2)
            
            value_label = tk.Label(frame, text=value, font=('Consolas', 12),
                                  fg=self.colors['text_primary'], bg=self.colors['bg_primary'])
            value_label.pack(anchor=tk.W, padx=20, pady=2)
            
            self.metrics_labels[label] = value_label
            
    def setup_tactical_metrics(self, container):
        """Setup tactical deployment metrics"""
        metrics = [
            ("OPERATIONAL ZONES", "5 Active Zones"),
            ("MISSIONS COMPLETED", "0"),
            ("AGENTS DEPLOYED", str(len(self.tactical_deployment.agents))),
            ("ASSETS PROTECTED", "5 Asset Classes"),
            ("THREAT RESPONSES", "0"),
            ("COORDINATION TIME", "58ms")
        ]
        
        for i, (label, value) in enumerate(metrics):
            frame = tk.Frame(container, bg=self.colors['bg_primary'], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label, font=('Consolas', 10, 'bold'),
                    fg=self.colors['accent_red'], bg=self.colors['bg_primary']).pack(anchor=tk.W, padx=10, pady=2)
            
            value_label = tk.Label(frame, text=value, font=('Consolas', 12),
                                  fg=self.colors['text_primary'], bg=self.colors['bg_primary'])
            value_label.pack(anchor=tk.W, padx=20, pady=2)
            
            self.metrics_labels[label] = value_label
            
    def start_monitoring(self):
        """Start the background monitoring"""
        def monitoring_loop():
            while True:
                try:
                    # Run deployment-specific monitoring
                    self.financial_deployment.monitor_financial_operations()
                    self.tactical_deployment.monitor_tactical_operations()
                    
                    # Update displays in main thread
                    self.root.after(0, self.update_all_displays)
                    
                    # Dynamic update interval based on system load
                    update_interval = self._calculate_monitoring_interval()
                    time.sleep(update_interval)
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                    time.sleep(0.5)
        
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
    
    def _calculate_monitoring_interval(self) -> float:
        """Calculate dynamic monitoring interval based on system state"""
        try:
            # Check current system load
            active_threats = len([t for t in getattr(self.financial_deployment, 'threat_history', [])[-5:] 
                                if t.get('severity') == 'HIGH'])
            
            if active_threats >= 2:
                return 0.5  # High threat - monitor frequently
            elif active_threats >= 1:
                return 1.0  # Medium threat - normal monitoring
            else:
                return 2.0  # Low threat - relaxed monitoring
                
        except Exception:
            return 2.0  # Default monitoring interval
        
    def update_all_displays(self):
        """Update all dashboard displays"""
        try:
            self.update_agent_status()
            self.update_deployment_metrics()
            self.update_learning_display()
            self.update_event_log()
        except Exception as e:
            logging.error(f"Display update error: {e}")
            
    def update_agent_status(self):
        """Update agent status displays"""
        current_agents = (self.financial_deployment.agents if self.current_deployment == "FINANCIAL" 
                         else self.tactical_deployment.agents)
        
        for agent_id, agent in current_agents.items():
            if agent_id in self.agent_widgets:
                widgets = self.agent_widgets[agent_id]
                widgets['status'].config(text=f"STATUS: {agent.status}")
                widgets['metrics'].config(
                    text=f"TRUST: {agent.trust_score:.2f} | THREATS: {agent.threats_detected} | LEARNING: {agent.learning_progress:.1%}")
                
    def update_deployment_metrics(self):
        """Update deployment-specific metrics"""
        if self.current_deployment == "FINANCIAL":
            self.ops_title_label.config(text="FINANCIAL SYSTEMS PROTECTION CENTER",
                                       fg=self.colors['accent_blue'])
            
            if "PROTECTED VALUE" in self.metrics_labels:
                value = self.financial_deployment.protected_value / 1e9  # Convert to billions
                self.metrics_labels["PROTECTED VALUE"].config(text=f"${value:.2f}B")
                
            total_threats = sum(agent.threats_detected for agent in self.financial_deployment.agents.values())
            if "THREAT DETECTIONS" in self.metrics_labels:
                self.metrics_labels["THREAT DETECTIONS"].config(text=str(total_threats))
                
        else:
            self.ops_title_label.config(text="TACTICAL OPERATIONS COMMAND CENTER",
                                       fg=self.colors['accent_red'])
            
            if "MISSIONS COMPLETED" in self.metrics_labels:
                self.metrics_labels["MISSIONS COMPLETED"].config(text=str(self.tactical_deployment.missions_completed))
                
            total_responses = sum(agent.threats_detected for agent in self.tactical_deployment.agents.values())
            if "THREAT RESPONSES" in self.metrics_labels:
                self.metrics_labels["THREAT RESPONSES"].config(text=str(total_responses))
                
    def update_learning_display(self):
        """Update learning analytics display"""
        # Clear existing learning displays
        for widget in self.learning_display_frame.winfo_children():
            widget.destroy()
            
        current_agents = (self.financial_deployment.agents if self.current_deployment == "FINANCIAL" 
                         else self.tactical_deployment.agents)
        
        # Show top learning agents
        learning_agents = sorted(current_agents.values(), 
                               key=lambda a: a.learning_progress, reverse=True)[:10]
        
        for agent in learning_agents:
            agent_frame = tk.Frame(self.learning_display_frame, bg=self.colors['bg_primary'], 
                                  relief=tk.RIDGE, bd=1)
            agent_frame.pack(fill=tk.X, pady=1)
            
            progress_text = f"{agent.agent_id}: {agent.learning_progress:.1%} progress | Accuracy: {agent.performance_metrics['accuracy']:.2%}"
            tk.Label(agent_frame, text=progress_text, font=('Consolas', 9),
                    fg=self.colors['text_primary'], bg=self.colors['bg_primary']).pack(anchor=tk.W, padx=10, pady=2)
                    
    def update_event_log(self):
        """Update the event monitoring log"""
        current_agents = (self.financial_deployment.agents if self.current_deployment == "FINANCIAL" 
                         else self.tactical_deployment.agents)
        
        # Collect recent events from all agents
        all_events = []
        for agent in current_agents.values():
            for event in agent.event_log[-5:]:  # Last 5 events per agent
                all_events.append((agent.agent_id, event))
                
        # Sort by timestamp
        all_events.sort(key=lambda x: x[1]['timestamp'], reverse=True)
        
        # Update display
        self.event_text.delete(1.0, tk.END)
        for agent_id, event in all_events[-20:]:  # Show last 20 events
            timestamp = event['timestamp'].strftime("%H:%M:%S")
            event_line = f"[{timestamp}] {agent_id}: {event['type']} - {event['description']}\n"
            self.event_text.insert(tk.END, event_line)
            
        self.event_text.see(tk.END)  # Scroll to bottom

    def run(self):
        """Run the dashboard"""
        self.root.mainloop()

def main():
    """Main function"""
    print("="*80)
    print("MWRASP DEPLOYMENT-SPECIFIC DASHBOARD SYSTEM")
    print("Professional interface for Financial vs Tactical deployments")
    print("="*80)
    print("\nLaunching deployment-specific dashboard...")
    print("Features:")
    print("  -> Individual Agent Tracking with Learning Metrics")
    print("  -> Financial Systems Deployment Layout")
    print("  -> Tactical Operations Deployment Layout") 
    print("  -> Real-time Agent Event Logging")
    print("  -> Deployment-Specific Operations Centers")
    print("  -> Agent Status and Performance Monitoring")
    print("\nDashboard launching - check your screen!")
    
    try:
        dashboard = DeploymentSpecificDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
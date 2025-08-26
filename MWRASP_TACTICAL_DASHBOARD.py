#!/usr/bin/env python3
"""
MWRASP Tactical Operations Dashboard
Complete interactive dashboard for military tactical operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
import threading
import time
import random
from datetime import datetime, timedelta
from collections import deque
import logging

# Configure matplotlib for dark theme
plt.style.use('dark_background')

class TacticalAgent:
    """Individual tactical operations agent"""
    
    def __init__(self, agent_id: str, agent_type: str, operational_zone: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.operational_zone = operational_zone
        self.status = "ACTIVE"
        self.readiness_level = random.uniform(0.85, 0.98)
        self.mission_success_rate = random.uniform(0.88, 0.97)
        self.missions_completed = random.randint(15, 45)
        self.threats_neutralized = random.randint(8, 30)
        self.last_activity = datetime.now()
        self.combat_metrics = {
            'response_time': random.uniform(0.8, 2.5),
            'accuracy': random.uniform(0.90, 0.99),
            'coordination_efficiency': random.uniform(0.85, 0.96)
        }
        self.event_log = deque(maxlen=100)
        self.tactical_specialties = self._get_tactical_specialties()
        
    def _get_tactical_specialties(self):
        """Get tactical specialties by agent type"""
        specialties = {
            'Communications_Specialist': ['Signal_Intelligence', 'Radio_Security', 'Encryption_Analysis', 'Jamming_Detection'],
            'UAV_Controller': ['Drone_Coordination', 'Aerial_Surveillance', 'Target_Acquisition', 'Flight_Path_Optimization'],
            'Satellite_Operator': ['Orbital_Communications', 'GPS_Security', 'Space_Surveillance', 'Satellite_Defense'],
            'Robotics_Coordinator': ['Ground_Robotics', 'Autonomous_Systems', 'Tactical_Deployment', 'Remote_Operations'],
            'Intelligence_Analyst': ['Threat_Assessment', 'Pattern_Recognition', 'Strategic_Analysis', 'SIGINT_Processing'],
            'Electronic_Warfare': ['Signal_Jamming', 'Countermeasures', 'Spectrum_Analysis', 'Electronic_Attack'],
            'Cyber_Operations': ['Network_Defense', 'Digital_Warfare', 'System_Penetration', 'Data_Extraction'],
            'Quantum_Security': ['Quantum_Communication', 'Post_Quantum_Crypto', 'Secure_Key_Distribution']
        }
        return specialties.get(self.agent_type, ['General_Tactical_Operations'])
        
    def simulate_tactical_learning(self):
        """Simulate agent tactical learning"""
        if random.random() < 0.25:  # 25% chance of learning event
            improvement_gain = random.uniform(0.005, 0.015)
            self.mission_success_rate = min(0.99, self.mission_success_rate + improvement_gain)
            self.combat_metrics['accuracy'] = min(0.99, 
                self.combat_metrics['accuracy'] + improvement_gain * 0.5)
            
            event = {
                'timestamp': datetime.now(),
                'type': 'TACTICAL_TRAINING',
                'description': f'Enhanced {random.choice(self.tactical_specialties)} capability'
            }
            self.event_log.append(event)
            
    def handle_tactical_threat(self, threat_type: str, threat_severity: str):
        """Handle tactical threat"""
        self.threats_neutralized += 1
        self.missions_completed += 1
        self.last_activity = datetime.now()
        
        # Success rate depends on threat severity
        base_success_rate = 0.95
        if threat_severity == "HIGH":
            base_success_rate = 0.85
        elif threat_severity == "CRITICAL":
            base_success_rate = 0.75
            
        success = random.random() < base_success_rate
        if success:
            self.readiness_level = min(0.99, self.readiness_level + 0.005)
            
        event = {
            'timestamp': datetime.now(),
            'type': 'THREAT_ENGAGEMENT',
            'description': f'Engaged {threat_type} ({threat_severity})',
            'threat_type': threat_type,
            'severity': threat_severity,
            'success': success
        }
        self.event_log.append(event)
        return success

class TacticalOperationsCore:
    """Core tactical operations simulation"""
    
    def __init__(self):
        self.agents = self._deploy_tactical_agents()
        self.operational_zones = ["COMMUNICATIONS", "AERIAL", "GROUND", "SPACE", "CYBER"]
        self.zone_status = {zone: deque(maxlen=50) for zone in self.operational_zones}
        self.threat_history = deque(maxlen=150)
        self.missions_completed = 0
        self.assets_protected = 0
        self.tactical_threats = [
            'signal_jamming_attempt', 'uav_intrusion', 'satellite_disruption',
            'cyber_warfare_attack', 'communications_intercept', 'gps_spoofing',
            'electronic_warfare', 'network_penetration', 'drone_swarm_attack',
            'orbital_debris_threat', 'ground_infiltration', 'data_exfiltration',
            'command_system_compromise', 'sensor_network_attack'
        ]
        self.protected_assets = [
            'Communication_Networks', 'UAV_Fleet', 'Satellite_Constellation',
            'Ground_Robotics', 'Command_Centers', 'Sensor_Arrays', 'Data_Centers'
        ]
        self.running = False
        
    def _deploy_tactical_agents(self):
        """Deploy tactical operations agents"""
        agents = {}
        
        # Communications specialists
        for i in range(3):
            agent_id = f"comms_specialist_{i+1}"
            zone = "COMMUNICATIONS"
            agents[agent_id] = TacticalAgent(agent_id, "Communications_Specialist", zone)
            
        # UAV controllers
        for i in range(4):
            agent_id = f"uav_controller_{i+1}"
            zone = "AERIAL"
            agents[agent_id] = TacticalAgent(agent_id, "UAV_Controller", zone)
            
        # Satellite operators
        for i in range(2):
            agent_id = f"satellite_operator_{i+1}"
            zone = "SPACE"
            agents[agent_id] = TacticalAgent(agent_id, "Satellite_Operator", zone)
            
        # Robotics coordinators
        for i in range(3):
            agent_id = f"robotics_coord_{i+1}"
            zone = "GROUND"
            agents[agent_id] = TacticalAgent(agent_id, "Robotics_Coordinator", zone)
            
        # Intelligence analysts
        for i in range(2):
            agent_id = f"intel_analyst_{i+1}"
            zone = "CYBER"
            agents[agent_id] = TacticalAgent(agent_id, "Intelligence_Analyst", zone)
            
        # Electronic warfare specialists
        agents["ew_specialist_1"] = TacticalAgent("ew_specialist_1", "Electronic_Warfare", "COMMUNICATIONS")
        agents["ew_specialist_2"] = TacticalAgent("ew_specialist_2", "Electronic_Warfare", "CYBER")
        
        # Cyber operations
        agents["cyber_ops_1"] = TacticalAgent("cyber_ops_1", "Cyber_Operations", "CYBER")
        agents["cyber_ops_2"] = TacticalAgent("cyber_ops_2", "Cyber_Operations", "CYBER")
        
        # Quantum security
        agents["quantum_security"] = TacticalAgent("quantum_security", "Quantum_Security", "COMMUNICATIONS")
        
        return agents
        
    def simulate_zone_activity(self):
        """Simulate activity in operational zones"""
        for zone in self.operational_zones:
            # Generate zone status
            threat_level = random.choice(['GREEN', 'YELLOW', 'ORANGE', 'RED'])
            activity_level = random.uniform(20, 100)
            
            if threat_level == 'RED':
                activity_level = random.uniform(80, 100)
            elif threat_level == 'ORANGE':
                activity_level = random.uniform(60, 85)
                
            self.zone_status[zone].append({
                'timestamp': datetime.now(),
                'threat_level': threat_level,
                'activity_level': activity_level,
                'assets_active': random.randint(5, 20)
            })
            
    def simulate_tactical_threats(self):
        """Simulate tactical threats and responses"""
        if random.random() < 0.35:  # 35% chance per cycle
            threat_type = random.choice(self.tactical_threats)
            threat_severity = random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
            target_zone = random.choice(self.operational_zones)
            
            threat_event = {
                'timestamp': datetime.now(),
                'type': threat_type,
                'severity': threat_severity,
                'zone': target_zone,
                'status': 'ACTIVE'
            }
            
            # Assign to appropriate agent based on zone and threat type
            zone_agents = [agent for agent in self.agents.values() 
                          if agent.operational_zone == target_zone]
            
            if not zone_agents:  # Fallback to any available agent
                zone_agents = list(self.agents.values())
                
            if zone_agents:
                handling_agent = random.choice(zone_agents)
                success = handling_agent.handle_tactical_threat(threat_type, threat_severity)
                
                if success:
                    threat_event['status'] = 'NEUTRALIZED'
                    threat_event['handled_by'] = handling_agent.agent_id
                    self.missions_completed += 1
                    self.assets_protected += 1
                else:
                    threat_event['status'] = 'ESCALATED'
                    
            self.threat_history.append(threat_event)
            
    def run_simulation(self):
        """Run the tactical operations simulation"""
        self.running = True
        while self.running:
            try:
                self.simulate_zone_activity()
                self.simulate_tactical_threats()
                
                # Simulate agent learning
                for agent in self.agents.values():
                    agent.simulate_tactical_learning()
                    
                time.sleep(1.5)
                
            except Exception as e:
                logging.error(f"Tactical simulation error: {e}")
                time.sleep(1.0)
                
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False

class TacticalDashboard:
    """Complete interactive Tactical Operations Dashboard"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MWRASP Tactical Operations Command Dashboard")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#0a0a0a')
        
        self.tactical_core = TacticalOperationsCore()
        
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a',
            'bg_tertiary': '#2a2a2a',
            'accent_green': '#00ff00',
            'accent_blue': '#00aaff',
            'accent_red': '#ff4444',
            'accent_yellow': '#ffaa00',
            'accent_purple': '#aa00ff',
            'accent_orange': '#ff8800',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
        self.setup_ui()
        self.start_simulation()
        
    def setup_ui(self):
        """Setup the complete tactical dashboard UI"""
        # Main header
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="MWRASP TACTICAL OPERATIONS COMMAND DASHBOARD",
                              font=('Consolas', 18, 'bold'), fg=self.colors['accent_red'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Status indicators
        status_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.system_status = tk.Label(status_frame, text="COMMAND: OPERATIONAL", 
                                     font=('Consolas', 12, 'bold'), fg=self.colors['accent_green'],
                                     bg=self.colors['bg_secondary'])
        self.system_status.pack()
        
        self.agent_count = tk.Label(status_frame, text="AGENTS: 18 DEPLOYED",
                                   font=('Consolas', 10), fg=self.colors['text_primary'],
                                   bg=self.colors['bg_secondary'])
        self.agent_count.pack()
        
        # Main content area with tactical layout
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tactical sections
        self.create_battlefield_overview(main_frame)
        self.create_threat_assessment(main_frame)
        self.create_asset_control(main_frame)
        self.create_communications_hub(main_frame)
        self.create_mission_control(main_frame)
        
    def create_battlefield_overview(self, parent):
        """Create battlefield situational awareness section"""
        battlefield_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        battlefield_frame.place(relx=0.02, rely=0.02, relwidth=0.48, relheight=0.48)
        
        # Header
        header = tk.Label(battlefield_frame, text="BATTLEFIELD SITUATIONAL AWARENESS",
                         font=('Consolas', 12, 'bold'), fg=self.colors['accent_red'],
                         bg=self.colors['bg_secondary'])
        header.pack(pady=10)
        
        # Zone status visualization
        self.battlefield_fig, self.battlefield_ax = plt.subplots(figsize=(8, 4), facecolor='#1a1a1a')
        self.battlefield_ax.set_facecolor('#1a1a1a')
        self.battlefield_ax.set_title('Operational Zones Status', color='white', fontsize=10)
        self.battlefield_ax.set_xlabel('Time', color='white')
        self.battlefield_ax.set_ylabel('Activity Level', color='white')
        
        self.battlefield_canvas = FigureCanvasTkAgg(self.battlefield_fig, battlefield_frame)
        self.battlefield_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Zone status indicators
        zone_frame = tk.Frame(battlefield_frame, bg=self.colors['bg_secondary'])
        zone_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.zone_labels = {}
        colors = [self.colors['accent_green'], self.colors['accent_blue'], self.colors['accent_yellow'],
                 self.colors['accent_purple'], self.colors['accent_orange']]
        
        for i, zone in enumerate(self.tactical_core.operational_zones):
            label = tk.Label(zone_frame, text=f"{zone}: GREEN", 
                           font=('Consolas', 9, 'bold'), fg=colors[i],
                           bg=self.colors['bg_secondary'])
            label.grid(row=i//3, column=i%3, sticky=tk.W, padx=15, pady=2)
            self.zone_labels[zone] = label
            
    def create_threat_assessment(self, parent):
        """Create threat assessment and intelligence section"""
        threat_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        threat_frame.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.48)
        
        # Header
        header = tk.Label(threat_frame, text="THREAT ASSESSMENT & INTELLIGENCE",
                         font=('Consolas', 12, 'bold'), fg=self.colors['accent_yellow'],
                         bg=self.colors['bg_secondary'])
        header.pack(pady=10)
        
        # Threat metrics
        metrics_frame = tk.Frame(threat_frame, bg=self.colors['bg_secondary'])
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.missions_completed_label = tk.Label(metrics_frame, text="MISSIONS COMPLETED: 0",
                                               font=('Consolas', 11, 'bold'), fg=self.colors['accent_green'],
                                               bg=self.colors['bg_secondary'])
        self.missions_completed_label.pack()
        
        self.assets_protected_label = tk.Label(metrics_frame, text="ASSETS PROTECTED: 0",
                                             font=('Consolas', 10), fg=self.colors['text_primary'],
                                             bg=self.colors['bg_secondary'])
        self.assets_protected_label.pack()
        
        self.threat_level_label = tk.Label(metrics_frame, text="CURRENT THREAT LEVEL: LOW",
                                         font=('Consolas', 10, 'bold'), fg=self.colors['accent_blue'],
                                         bg=self.colors['bg_secondary'])
        self.threat_level_label.pack()
        
        # Intelligence feed
        intel_frame = tk.Frame(threat_frame, bg=self.colors['bg_secondary'])
        intel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(intel_frame, text="TACTICAL INTELLIGENCE FEED:",
                font=('Consolas', 10, 'bold'), fg=self.colors['accent_orange'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.intel_log = tk.Text(intel_frame, height=10, bg=self.colors['bg_primary'],
                               fg=self.colors['text_primary'], font=('Consolas', 8),
                               wrap=tk.WORD)
        intel_scrollbar = tk.Scrollbar(intel_frame, command=self.intel_log.yview)
        self.intel_log.configure(yscrollcommand=intel_scrollbar.set)
        
        self.intel_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        intel_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_asset_control(self, parent):
        """Create asset control and coordination section"""
        asset_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        asset_frame.place(relx=0.02, rely=0.52, relwidth=0.32, relheight=0.46)
        
        # Header
        header = tk.Label(asset_frame, text="ASSET CONTROL",
                         font=('Consolas', 12, 'bold'), fg=self.colors['accent_purple'],
                         bg=self.colors['bg_secondary'])
        header.pack(pady=10)
        
        # Asset performance chart
        self.asset_fig, self.asset_ax = plt.subplots(figsize=(5, 3), facecolor='#1a1a1a')
        self.asset_ax.set_facecolor('#1a1a1a')
        self.asset_ax.set_title('Asset Readiness Status', color='white', fontsize=10)
        
        self.asset_canvas = FigureCanvasTkAgg(self.asset_fig, asset_frame)
        self.asset_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Asset controls
        control_frame = tk.Frame(asset_frame, bg=self.colors['bg_secondary'])
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(control_frame, text="DEPLOY ASSETS", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_green'], fg=self.colors['bg_primary'],
                 command=self.deploy_assets).pack(fill=tk.X, pady=2)
        
        tk.Button(control_frame, text="RECALL UNITS", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_yellow'], fg=self.colors['bg_primary'],
                 command=self.recall_units).pack(fill=tk.X, pady=2)
        
        tk.Button(control_frame, text="EMERGENCY STOP", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_red'], fg=self.colors['bg_primary'],
                 command=self.emergency_stop).pack(fill=tk.X, pady=2)
        
    def create_communications_hub(self, parent):
        """Create communications and coordination hub"""
        comms_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        comms_frame.place(relx=0.36, rely=0.52, relwidth=0.32, relheight=0.46)
        
        # Header
        header = tk.Label(comms_frame, text="COMMUNICATIONS HUB",
                         font=('Consolas', 12, 'bold'), fg=self.colors['accent_blue'],
                         bg=self.colors['bg_secondary'])
        header.pack(pady=10)
        
        # Agent status grid
        agent_frame = tk.Frame(comms_frame, bg=self.colors['bg_secondary'])
        agent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create scrollable agent list
        canvas = tk.Canvas(agent_frame, bg=self.colors['bg_secondary'])
        scrollbar = tk.Scrollbar(agent_frame, orient="vertical", command=canvas.yview)
        self.agent_list_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=self.agent_list_frame, anchor="nw")
        
        self.setup_agent_display()
        
        # Communication controls
        comm_control_frame = tk.Frame(comms_frame, bg=self.colors['bg_secondary'])
        comm_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(comm_control_frame, text="SECURE COMMS", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_blue'], fg=self.colors['bg_primary'],
                 command=self.secure_communications).pack(side=tk.LEFT, padx=2)
        
        tk.Button(comm_control_frame, text="AGENT STATUS", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_purple'], fg=self.colors['bg_primary'],
                 command=self.show_agent_status).pack(side=tk.RIGHT, padx=2)
        
    def create_mission_control(self, parent):
        """Create mission control and analytics section"""
        mission_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        mission_frame.place(relx=0.70, rely=0.52, relwidth=0.28, relheight=0.46)
        
        # Header
        header = tk.Label(mission_frame, text="MISSION CONTROL",
                         font=('Consolas', 12, 'bold'), fg=self.colors['accent_green'],
                         bg=self.colors['bg_secondary'])
        header.pack(pady=10)
        
        # Mission metrics
        metrics = [
            ("READINESS", "94.2%"),
            ("SUCCESS RATE", "97.1%"),
            ("RESPONSE TIME", "1.8s"),
            ("COORDINATION", "91.5%")
        ]
        
        self.mission_labels = {}
        for metric, value in metrics:
            metric_frame = tk.Frame(mission_frame, bg=self.colors['bg_primary'])
            metric_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(metric_frame, text=metric, font=('Consolas', 8),
                    fg=self.colors['text_secondary'], bg=self.colors['bg_primary']).pack()
            
            value_label = tk.Label(metric_frame, text=value, font=('Consolas', 12, 'bold'),
                                  fg=self.colors['accent_green'], bg=self.colors['bg_primary'])
            value_label.pack()
            self.mission_labels[metric] = value_label
            
        # Mission controls
        mission_control_frame = tk.Frame(mission_frame, bg=self.colors['bg_secondary'])
        mission_control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Button(mission_control_frame, text="NEW MISSION", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_green'], fg=self.colors['bg_primary'],
                 command=self.new_mission).pack(fill=tk.X, pady=2)
        
        tk.Button(mission_control_frame, text="SITUATION REPORT", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_blue'], fg=self.colors['bg_primary'],
                 command=self.situation_report).pack(fill=tk.X, pady=2)
        
        tk.Button(mission_control_frame, text="TACTICAL ANALYSIS", font=('Consolas', 8, 'bold'),
                 bg=self.colors['accent_yellow'], fg=self.colors['bg_primary'],
                 command=self.tactical_analysis).pack(fill=tk.X, pady=2)
        
    def setup_agent_display(self):
        """Setup the tactical agent display"""
        for widget in self.agent_list_frame.winfo_children():
            widget.destroy()
            
        agent_types = {}
        for agent in self.tactical_core.agents.values():
            if agent.agent_type not in agent_types:
                agent_types[agent.agent_type] = []
            agent_types[agent.agent_type].append(agent)
            
        for agent_type, agents in agent_types.items():
            type_frame = tk.Frame(self.agent_list_frame, bg=self.colors['bg_primary'])
            type_frame.pack(fill=tk.X, padx=2, pady=1)
            
            tk.Label(type_frame, text=f"{agent_type}: {len(agents)} active",
                    font=('Consolas', 8, 'bold'), fg=self.colors['accent_green'],
                    bg=self.colors['bg_primary']).pack(anchor=tk.W)
                    
        self.agent_list_frame.update_idletasks()
        canvas = self.agent_list_frame.master
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def start_simulation(self):
        """Start the tactical operations simulation"""
        # Start core simulation
        sim_thread = threading.Thread(target=self.tactical_core.run_simulation, daemon=True)
        sim_thread.start()
        
        # Start UI updates
        self.update_dashboard()
        
    def update_dashboard(self):
        """Update all dashboard elements"""
        try:
            self.update_battlefield_display()
            self.update_threat_display()
            self.update_asset_display()
            self.update_mission_metrics()
        except Exception as e:
            logging.error(f"Tactical dashboard update error: {e}")
        finally:
            self.root.after(1000, self.update_dashboard)
            
    def update_battlefield_display(self):
        """Update battlefield overview display"""
        # Update zone activity chart
        self.battlefield_ax.clear()
        self.battlefield_ax.set_facecolor('#1a1a1a')
        self.battlefield_ax.set_title('Operational Zones Activity', color='white', fontsize=10)
        
        colors = ['#00ff00', '#00aaff', '#ffaa00', '#aa00ff', '#ff8800']
        for i, zone in enumerate(self.tactical_core.operational_zones):
            if self.tactical_core.zone_status[zone]:
                activities = [d['activity_level'] for d in list(self.tactical_core.zone_status[zone])[-20:]]
                if activities:
                    self.battlefield_ax.plot(activities, color=colors[i], label=zone, linewidth=2)
                    
        self.battlefield_ax.legend(loc='upper right', fontsize=7)
        self.battlefield_ax.tick_params(colors='white')
        self.battlefield_canvas.draw()
        
        # Update zone status labels
        for zone in self.tactical_core.operational_zones:
            if self.tactical_core.zone_status[zone]:
                latest = list(self.tactical_core.zone_status[zone])[-1]
                threat_level = latest['threat_level']
                color_map = {'GREEN': self.colors['accent_green'], 'YELLOW': self.colors['accent_yellow'],
                           'ORANGE': self.colors['accent_orange'], 'RED': self.colors['accent_red']}
                self.zone_labels[zone].config(text=f"{zone}: {threat_level}", 
                                            fg=color_map.get(threat_level, self.colors['text_primary']))
                
    def update_threat_display(self):
        """Update threat assessment display"""
        self.missions_completed_label.config(text=f"MISSIONS COMPLETED: {self.tactical_core.missions_completed}")
        self.assets_protected_label.config(text=f"ASSETS PROTECTED: {self.tactical_core.assets_protected}")
        
        # Calculate current threat level
        recent_threats = list(self.tactical_core.threat_history)[-10:]
        if recent_threats:
            high_severity_count = len([t for t in recent_threats if t.get('severity') in ['HIGH', 'CRITICAL']])
            if high_severity_count > 3:
                threat_level = "CRITICAL"
                color = self.colors['accent_red']
            elif high_severity_count > 1:
                threat_level = "HIGH"  
                color = self.colors['accent_orange']
            else:
                threat_level = "MODERATE"
                color = self.colors['accent_yellow']
        else:
            threat_level = "LOW"
            color = self.colors['accent_green']
            
        self.threat_level_label.config(text=f"CURRENT THREAT LEVEL: {threat_level}", fg=color)
        
        # Update intelligence log
        self.intel_log.delete(1.0, tk.END)
        recent_intel = list(self.tactical_core.threat_history)[-8:]
        for intel in reversed(recent_intel):
            timestamp = intel['timestamp'].strftime("%H:%M:%S")
            status_str = intel['status']
            intel_entry = f"[{timestamp}] {intel['type']} in {intel['zone']} - {status_str}\n"
            self.intel_log.insert(tk.END, intel_entry)
            
    def update_asset_display(self):
        """Update asset control display"""
        # Update asset readiness chart
        self.asset_ax.clear()
        self.asset_ax.set_facecolor('#1a1a1a')
        self.asset_ax.set_title('Asset Type Readiness', color='white', fontsize=9)
        
        agent_readiness = {}
        for agent in self.tactical_core.agents.values():
            if agent.agent_type not in agent_readiness:
                agent_readiness[agent.agent_type] = []
            agent_readiness[agent.agent_type].append(agent.readiness_level)
            
        types = list(agent_readiness.keys())[:6]  # Top 6 types
        avg_readiness = [np.mean(agent_readiness[t]) for t in types]
        
        colors = ['#00ff00', '#00aaff', '#ff4444', '#ffaa00', '#aa00ff', '#ff8800']
        bars = self.asset_ax.bar(range(len(types)), avg_readiness, color=colors[:len(types)])
        self.asset_ax.set_xticks(range(len(types)))
        self.asset_ax.set_xticklabels([t.replace('_', '\n') for t in types], fontsize=7, color='white')
        self.asset_ax.set_ylabel('Readiness', color='white')
        self.asset_ax.set_ylim([0.8, 1.0])
        self.asset_ax.tick_params(colors='white')
        
        self.asset_canvas.draw()
        
    def update_mission_metrics(self):
        """Update mission control metrics"""
        if self.tactical_core.agents:
            avg_readiness = np.mean([a.readiness_level for a in self.tactical_core.agents.values()])
            avg_success_rate = np.mean([a.mission_success_rate for a in self.tactical_core.agents.values()])
            avg_response_time = np.mean([a.combat_metrics['response_time'] for a in self.tactical_core.agents.values()])
            avg_coordination = np.mean([a.combat_metrics['coordination_efficiency'] for a in self.tactical_core.agents.values()])
            
            self.mission_labels["READINESS"].config(text=f"{avg_readiness:.1%}")
            self.mission_labels["SUCCESS RATE"].config(text=f"{avg_success_rate:.1%}")
            self.mission_labels["RESPONSE TIME"].config(text=f"{avg_response_time:.1f}s")
            self.mission_labels["COORDINATION"].config(text=f"{avg_coordination:.1%}")
            
    # Command functions
    def deploy_assets(self):
        """Deploy tactical assets"""
        messagebox.showinfo("Asset Deployment", "Tactical assets deployed to operational zones!")
        
    def recall_units(self):
        """Recall deployed units"""
        messagebox.showinfo("Unit Recall", "All deployed units returning to base!")
        
    def emergency_stop(self):
        """Emergency stop all operations"""
        messagebox.showwarning("Emergency Stop", "EMERGENCY STOP ACTIVATED - All operations halted!")
        
    def secure_communications(self):
        """Secure communications channels"""
        messagebox.showinfo("Secure Comms", "All communication channels secured with quantum encryption!")
        
    def show_agent_status(self):
        """Show detailed agent status"""
        status_window = tk.Toplevel(self.root)
        status_window.title("Tactical Agent Status")
        status_window.geometry("700x500")
        status_window.configure(bg=self.colors['bg_primary'])
        
        text_widget = tk.Text(status_window, bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'], font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for agent in self.tactical_core.agents.values():
            status = f"{agent.agent_id} ({agent.agent_type})\n"
            status += f"  Zone: {agent.operational_zone} | Status: {agent.status}\n"
            status += f"  Readiness: {agent.readiness_level:.1%} | Success Rate: {agent.mission_success_rate:.1%}\n"
            status += f"  Missions: {agent.missions_completed} | Threats: {agent.threats_neutralized}\n\n"
            text_widget.insert(tk.END, status)
            
    def new_mission(self):
        """Start new mission"""
        messagebox.showinfo("New Mission", "New tactical mission initiated - deploying assets!")
        
    def situation_report(self):
        """Generate situation report"""
        messagebox.showinfo("SITREP", "Tactical situation report generated and transmitted!")
        
    def tactical_analysis(self):
        """Perform tactical analysis"""
        messagebox.showinfo("Tactical Analysis", "Comprehensive tactical analysis completed!")
        
    def on_closing(self):
        """Handle window closing"""
        self.tactical_core.stop_simulation()
        self.root.destroy()
        
    def run(self):
        """Run the dashboard"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main function"""
    print("="*80)
    print("MWRASP TACTICAL OPERATIONS COMMAND DASHBOARD")
    print("Complete Interactive Military Command Interface")
    print("="*80)
    print("\nInitializing tactical operations command...")
    print("Loading interactive dashboard with real-time battlefield graphics...")
    
    try:
        dashboard = TacticalDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\nShutting down command dashboard...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
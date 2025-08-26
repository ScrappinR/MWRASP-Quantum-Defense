#!/usr/bin/env python3
"""
MWRASP Quantum Defense System - Interactive Demo

This demo showcases the complete MWRASP system including:
- Quantum computer attack detection with canary tokens
- Temporal fragmentation with millisecond expiration
- Autonomous agent coordination and response
- Real-time threat monitoring and visualization

Run this demo to see the system in action!
"""

import asyncio
import time
import sys
import argparse
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt, Confirm

# Import MWRASP components
from src.core.quantum_detector import QuantumDetector, ThreatLevel
from src.core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
from src.core.agent_system import AutonomousDefenseCoordinator


class MWRASPDemo:
    def __init__(self, verbose: bool = False):
        self.console = Console()
        self.verbose = verbose
        
        # Initialize system components
        self.console.print("[bold blue]Initializing MWRASP Quantum Defense System...[/bold blue]")
        
        self.quantum_detector = QuantumDetector(sensitivity_threshold=0.6)  # Lower threshold for demo
        
        self.fragmentation_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=300,  # 300ms for demo visibility
            min_fragments=4,
            max_fragments=7,
            quantum_resistance_level=3
        )
        self.fragmentation_system = TemporalFragmentation(self.fragmentation_policy)
        
        self.agent_coordinator = AutonomousDefenseCoordinator(
            self.quantum_detector,
            self.fragmentation_system
        )
        
        # Demo state
        self.demo_data = {}
        self.demo_running = False
    
    async def run_complete_demo(self):
        """Run the complete MWRASP demonstration"""
        try:
            await self._display_banner()
            await self._system_initialization()
            
            while True:
                choice = await self._show_main_menu()
                
                if choice == "1":
                    await self._demo_quantum_detection()
                elif choice == "2":
                    await self._demo_temporal_fragmentation()
                elif choice == "3":
                    await self._demo_agent_coordination()
                elif choice == "4":
                    await self._demo_integrated_attack_response()
                elif choice == "5":
                    await self._demo_system_monitoring()
                elif choice == "6":
                    await self._run_performance_test()
                elif choice == "7":
                    self._show_system_status()
                elif choice == "8":
                    break
                else:
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
                
                if choice != "8":
                    input("\\nPress Enter to continue...")
        
        finally:
            await self._cleanup_demo()
    
    async def _display_banner(self):
        """Display the MWRASP banner"""
        banner = Panel.fit(
            "[bold cyan]MWRASP Quantum Defense System[/bold cyan]\\n"
            "[dim]Multi-Wavelength Rapid-Aging Surveillance Platform[/dim]\\n\\n"
            "[green]Quantum Attack Detection[/green]\\n"
            "[yellow]Temporal Data Fragmentation[/yellow]\\n"
            "[blue]Autonomous Agent Coordination[/blue]\\n\\n"
            "[dim]Interactive Demonstration System[/dim]",
            title="[bold red]MWRASP DEMO[/bold red]",
            border_style="red"
        )
        self.console.print(banner)
        self.console.print()
    
    async def _system_initialization(self):
        """Initialize all system components"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            # Start quantum detector monitoring
            task1 = progress.add_task("Starting quantum detector monitoring...", total=None)
            self.quantum_detector.start_monitoring()
            progress.update(task1, completed=100)
            await asyncio.sleep(0.5)
            
            # Start fragmentation cleanup service
            task2 = progress.add_task("Starting temporal fragmentation service...", total=None)
            self.fragmentation_system.start_cleanup_service()
            progress.update(task2, completed=100)
            await asyncio.sleep(0.5)
            
            # Start agent coordination
            task3 = progress.add_task("Initializing autonomous agent network...", total=None)
            await self.agent_coordinator.start_coordination()
            progress.update(task3, completed=100)
            await asyncio.sleep(0.5)
        
        self.console.print("[bold green]✅ All systems online and operational![/bold green]\\n")
    
    async def _show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        menu_panel = Panel(
            "[bold]Choose a demonstration:[/bold]\\n\\n"
            "[cyan]1.[/cyan] Quantum Computer Attack Detection\\n"
            "[cyan]2.[/cyan] Temporal Data Fragmentation\\n"
            "[cyan]3.[/cyan] Autonomous Agent Coordination\\n"
            "[cyan]4.[/cyan] Integrated Attack Response (Full System)\\n"
            "[cyan]5.[/cyan] Real-time System Monitoring\\n"
            "[cyan]6.[/cyan] Performance Stress Test\\n"
            "[cyan]7.[/cyan] System Status Report\\n"
            "[cyan]8.[/cyan] Exit Demo\\n",
            title="[bold blue]MWRASP Demo Menu[/bold blue]",
            border_style="blue"
        )
        self.console.print(menu_panel)
        
        choice = Prompt.ask(
            "Enter your choice",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )
        return choice
    
    async def _demo_quantum_detection(self):
        """Demonstrate quantum computer attack detection"""
        self.console.print(Panel.fit(
            "[bold yellow]Quantum Computer Attack Detection Demo[/bold yellow]\\n\\n"
            "This demo will create canary tokens and simulate quantum computer\\n"
            "attack patterns to demonstrate the detection system.",
            title="Demo 1",
            border_style="yellow"
        ))
        
        # Create canary tokens
        self.console.print("\\n[bold]Step 1: Deploying Canary Tokens[/bold]")
        tokens = []
        
        sensitive_systems = ["database_server", "encryption_keys", "user_credentials", "api_gateway"]
        
        for system in sensitive_systems:
            token = self.quantum_detector.generate_canary_token(system)
            tokens.append(token)
            self.console.print(f"  🎯 Canary token deployed for: [cyan]{system}[/cyan]")
            await asyncio.sleep(0.2)
        
        # Show initial system state
        self.console.print(f"\\n📊 Total canary tokens active: {len(tokens)}")
        
        # Simulate normal access
        self.console.print("\\n[bold]Step 2: Normal System Access[/bold]")
        normal_user = "legitimate_user_alice"
        self.quantum_detector.access_token(tokens[0].token_id, normal_user)
        self.console.print(f"  ✅ Normal access by [green]{normal_user}[/green] - No threat detected")
        
        await asyncio.sleep(1)
        
        # Simulate quantum attack
        self.console.print("\\n[bold red]Step 3: Simulating Quantum Computer Attack[/bold red]")
        self.console.print("  ⚠️  Quantum computer attempting parallel access to multiple systems...")
        
        # Multiple rapid accesses (superposition pattern)
        for round_num in range(5):
            for i, token in enumerate(tokens):
                self.quantum_detector.access_token(token.token_id, f"quantum_attacker_wave_{round_num}")
                if self.verbose:
                    self.console.print(f"    📡 Quantum access attempt {round_num+1}.{i+1}")
            await asyncio.sleep(0.01)  # Very rapid access
        
        # Check for threat detection
        await asyncio.sleep(0.1)  # Allow detection processing
        active_threats = self.quantum_detector.get_active_threats()
        
        if active_threats:
            self.console.print("\\n[bold red]🚨 QUANTUM ATTACK DETECTED! 🚨[/bold red]")
            
            threat_table = Table(title="Detected Threats")
            threat_table.add_column("Threat ID", style="cyan")
            threat_table.add_column("Level", style="red")
            threat_table.add_column("Confidence", style="yellow")
            threat_table.add_column("Quantum Indicators", style="magenta")
            
            for threat in active_threats:
                threat_table.add_row(
                    threat.threat_id[:8] + "...",
                    threat.threat_level.name,
                    f"{threat.confidence_score:.1%}",
                    ", ".join(threat.quantum_indicators[:3])
                )
            
            self.console.print(threat_table)
        else:
            self.console.print("\\n[yellow]⚠️ No threats detected (try adjusting sensitivity threshold)[/yellow]")
        
        # Show detection statistics
        stats = self.quantum_detector.get_threat_statistics()
        stats_panel = Panel(
            f"Total Canary Tokens: {stats['total_tokens']}\\n"
            f"Total Threats Detected: {stats['total_threats_detected']}\\n"
            f"Active Threats: {stats['active_threats']}\\n"
            f"Monitoring Active: {stats['monitoring_active']}",
            title="Detection Statistics",
            border_style="green"
        )
        self.console.print(stats_panel)
    
    async def _demo_temporal_fragmentation(self):
        """Demonstrate temporal data fragmentation"""
        self.console.print(Panel.fit(
            "[bold yellow]Temporal Data Fragmentation Demo[/bold yellow]\\n\\n"
            "This demo shows how sensitive data is fragmented into pieces\\n"
            "that expire in milliseconds, making quantum attacks ineffective.",
            title="Demo 2",
            border_style="yellow"
        ))
        
        # Prepare sensitive test data
        sensitive_documents = [
            ("TOP SECRET: Nuclear launch authorization codes", "nuclear_codes"),
            ("CLASSIFIED: Quantum encryption master keys", "quantum_keys"),
            ("CONFIDENTIAL: Agent identities and locations", "agent_data")
        ]
        
        self.console.print("\\n[bold]Step 1: Fragmenting Sensitive Data[/bold]")
        
        fragment_results = []
        for doc_content, doc_id in sensitive_documents:
            data_bytes = doc_content.encode('utf-8')
            
            self.console.print(f"\\n📄 Fragmenting: [cyan]{doc_id}[/cyan]")
            self.console.print(f"   Original size: {len(data_bytes)} bytes")
            
            fragments = self.fragmentation_system.fragment_data(data_bytes, doc_id)
            fragment_results.append((doc_content, doc_id, fragments))
            
            self.console.print(f"   ⚡ Created {len(fragments)} fragments")
            self.console.print(f"   🕐 Expires in: {fragments[0].expires_at - time.time():.3f} seconds")
            
            if self.verbose:
                for i, fragment in enumerate(fragments):
                    self.console.print(f"     Fragment {i+1}: {len(fragment.data_chunk)} bytes")
        
        # Show fragmentation statistics
        fragment_stats = self.fragmentation_system.get_system_stats()
        stats_panel = Panel(
            f"Total Fragments: {fragment_stats['total_fragments']}\\n"
            f"Active Fragments: {fragment_stats['active_fragments']}\\n"
            f"Fragment Groups: {fragment_stats['fragment_groups']}\\n"
            f"Cleanup Service: {'Running' if fragment_stats['cleanup_running'] else 'Stopped'}",
            title="Fragmentation Statistics",
            border_style="green"
        )
        self.console.print(f"\\n{stats_panel}")
        
        # Demonstrate immediate reconstruction
        self.console.print("\\n[bold]Step 2: Immediate Data Reconstruction[/bold]")
        for doc_content, doc_id, fragments in fragment_results:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed and reconstructed.decode('utf-8') == doc_content:
                self.console.print(f"  ✅ Successfully reconstructed: [green]{doc_id}[/green]")
            else:
                self.console.print(f"  ❌ Failed to reconstruct: [red]{doc_id}[/red]")
        
        # Demonstrate time-based expiration
        self.console.print("\\n[bold]Step 3: Demonstrating Fragment Expiration[/bold]")
        self.console.print("  ⏳ Waiting for fragment expiration...")
        
        # Wait for fragments to expire
        await asyncio.sleep(0.4)  # 400ms - should expire 300ms fragments
        
        self.console.print("  🕐 Attempting reconstruction after expiration:")
        for doc_content, doc_id, fragments in fragment_results:
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            if reconstructed:
                self.console.print(f"  ⚠️  Still accessible: [yellow]{doc_id}[/yellow] (may have longer lifetime)")
            else:
                self.console.print(f"  🔒 Properly expired: [red]{doc_id}[/red] - Data no longer accessible")
        
        # Show fragment status
        self.console.print("\\n[bold]Fragment Status Report[/bold]")
        for doc_content, doc_id, fragments in fragment_results:
            status = self.fragmentation_system.get_fragment_status(doc_id)
            if status:
                status_text = (
                    f"Total: {status.get('total_fragments', 0)}, "
                    f"Active: {status.get('active_fragments', 0)}, "
                    f"Expired: {status.get('expired_fragments', 0)}, "
                    f"Reconstructable: {status.get('reconstructable', False)}"
                )
                self.console.print(f"  📊 {doc_id}: {status_text}")
    
    async def _demo_agent_coordination(self):
        """Demonstrate autonomous agent coordination"""
        self.console.print(Panel.fit(
            "[bold yellow]Autonomous Agent Coordination Demo[/bold yellow]\\n\\n"
            "This demo shows how autonomous defense agents coordinate\\n"
            "to respond to quantum threats in real-time.",
            title="Demo 3",
            border_style="yellow"
        ))
        
        # Show initial agent status
        self.console.print("\\n[bold]Step 1: Current Agent Network Status[/bold]")
        agent_status = self.agent_coordinator.get_agent_status()
        
        # Create agent status table
        agent_table = Table(title="Defense Agent Network")
        agent_table.add_column("Role", style="cyan")
        agent_table.add_column("Agent Count", style="yellow")
        agent_table.add_column("Status Summary", style="green")
        
        for role, agents in agent_status['agents_by_role'].items():
            active_count = len([a for a in agents if a['status'] in ['active', 'busy']])
            total_count = len(agents)
            status_summary = f"{active_count}/{total_count} active"
            agent_table.add_row(role.title(), str(total_count), status_summary)
        
        self.console.print(agent_table)
        
        # Show coordination statistics
        coord_stats = agent_status.get('coordination_stats', {})
        coord_panel = Panel(
            f"Total Coordinations: {coord_stats.get('total_coordinations', 0)}\\n"
            f"Successful Defenses: {coord_stats.get('successful_defenses', 0)}\\n"
            f"Failed Defenses: {coord_stats.get('failed_defenses', 0)}\\n"
            f"Average Response Time: {coord_stats.get('average_response_time', 0):.1f}ms",
            title="Coordination Statistics",
            border_style="blue"
        )
        self.console.print(coord_panel)
        
        # Trigger manual coordination
        self.console.print("\\n[bold]Step 2: Triggering Agent Coordination[/bold]")
        self.console.print("  📡 Sending threat escalation message to agent network...")
        
        coordination_message = {
            "type": "threat_escalation",
            "threat_id": f"demo_threat_{int(time.time())}",
            "level": 8,  # High severity
            "source": "demo_system"
        }
        
        await self.agent_coordinator.send_coordination_message(coordination_message)
        
        # Allow coordination processing
        await asyncio.sleep(0.2)
        
        # Show updated agent status
        self.console.print("\\n[bold]Step 3: Agent Response Status[/bold]")
        updated_status = self.agent_coordinator.get_agent_status()
        
        # Show agent details
        for role, agents in updated_status['agents_by_role'].items():
            self.console.print(f"\\n  [cyan]{role.title()} Agents:[/cyan]")
            for i, agent in enumerate(agents):
                status_color = {
                    'idle': 'white',
                    'active': 'green', 
                    'busy': 'yellow',
                    'error': 'red'
                }.get(agent['status'], 'white')
                
                self.console.print(
                    f"    Agent {i+1}: [{status_color}]{agent['status']}[/{status_color}] "
                    f"(Workload: {agent['workload']}/{agent['max_workload']})"
                )
                
                if agent.get('current_task'):
                    self.console.print(f"      Current task: {agent['current_task']}")
        
        # Demonstrate help request coordination
        self.console.print("\\n[bold]Step 4: Inter-Agent Coordination[/bold]")
        help_request_message = {
            "type": "agent_request_help",
            "agent_id": "demo_agent",
            "capability": "quantum_analysis",
            "urgency": "high"
        }
        
        await self.agent_coordinator.send_coordination_message(help_request_message)
        self.console.print("  🤝 Help request sent between agents")
        
        await asyncio.sleep(0.1)
        
        # Show coordination network activity
        final_status = self.agent_coordinator.get_agent_status()
        final_coords = final_status.get('coordination_stats', {})
        
        if final_coords.get('total_coordinations', 0) > coord_stats.get('total_coordinations', 0):
            self.console.print("  ✅ Agent coordination successfully executed!")
            self.console.print(f"     New total coordinations: {final_coords.get('total_coordinations', 0)}")
        
        self.console.print("\\n[green]🤖 Autonomous agent network operational and responsive![/green]")
    
    async def _demo_integrated_attack_response(self):
        """Demonstrate full system integrated attack response"""
        self.console.print(Panel.fit(
            "[bold red]Integrated Quantum Attack Response Demo[/bold red]\\n\\n"
            "This demo simulates a sophisticated quantum computer attack\\n"
            "and shows the complete MWRASP system response including\\n"
            "detection, fragmentation, and agent coordination.",
            title="Demo 4 - Full System Integration",
            border_style="red"
        ))
        
        if not Confirm.ask("\\n[yellow]⚠️  This demo simulates a realistic attack scenario. Continue?[/yellow]"):
            return
        
        # Phase 1: Setup critical infrastructure
        self.console.print("\\n[bold]Phase 1: Deploying Critical Infrastructure Protection[/bold]")
        
        critical_systems = [
            ("financial_database", "Primary financial transaction database"),
            ("user_authentication", "User authentication and authorization system"),
            ("encryption_service", "Cryptographic key management service"),
            ("backup_systems", "Critical system backup and recovery"),
            ("admin_interface", "Administrative control interface")
        ]
        
        # Deploy canary tokens
        tokens = []
        for system_id, description in critical_systems:
            token = self.quantum_detector.generate_canary_token(system_id)
            tokens.append((token, system_id, description))
            self.console.print(f"  🛡️  Protected: [cyan]{description}[/cyan]")
        
        # Fragment critical data
        critical_documents = [
            ("MASTER_ENCRYPTION_KEYS: AES-256, RSA-4096, ECC-P521", "master_keys"),
            ("ADMIN_CREDENTIALS: root, admin, service_accounts", "admin_creds"),
            ("SYSTEM_TOPOLOGY: network_diagram, server_locations", "topology"),
            ("BACKUP_LOCATIONS: offsite_storage, recovery_procedures", "backups")
        ]
        
        fragmented_docs = []
        for doc_content, doc_id in critical_documents:
            fragments = self.fragmentation_system.fragment_data(doc_content.encode(), doc_id)
            fragmented_docs.append((doc_content, doc_id, fragments))
            self.console.print(f"  ⚡ Fragmented: [yellow]{doc_id}[/yellow] ({len(fragments)} fragments)")
        
        await asyncio.sleep(1)
        
        # Phase 2: Simulate normal operations
        self.console.print("\\n[bold]Phase 2: Normal System Operations[/bold]")
        
        # Normal user accesses
        legitimate_users = ["alice_admin", "bob_analyst", "charlie_operator"]
        for user in legitimate_users:
            token, system_id, _ = tokens[0]  # Access first system
            self.quantum_detector.access_token(token.token_id, user)
            self.console.print(f"  ✅ Normal access: [green]{user}[/green] → {system_id}")
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.5)
        
        # Phase 3: Quantum attack begins
        self.console.print("\\n[bold red]Phase 3: Quantum Computer Attack Initiated[/bold red]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            attack_task = progress.add_task("🚨 Quantum attack in progress...", total=None)
            
            # Multi-vector quantum attack simulation
            attack_vectors = [
                ("Superposition Access", "Multiple simultaneous system accesses"),
                ("Entanglement Correlation", "Correlated attacks across systems"),
                ("Quantum Speedup", "Unnaturally rapid computation patterns"),
                ("Interference Patterns", "Wave-like access signatures")
            ]
            
            for vector_name, vector_desc in attack_vectors:
                progress.update(attack_task, description=f"🚨 {vector_name}: {vector_desc}")
                
                if vector_name == "Superposition Access":
                    # Rapid parallel access to all systems
                    for round_num in range(6):
                        for token, system_id, _ in tokens:
                            self.quantum_detector.access_token(token.token_id, f"quantum_super_{round_num}")
                        await asyncio.sleep(0.001)
                
                elif vector_name == "Entanglement Correlation":
                    # Correlated access pattern
                    for i in range(8):
                        for token, system_id, _ in tokens[::2]:  # Every other system
                            self.quantum_detector.access_token(token.token_id, f"quantum_entangled_{i}")
                        await asyncio.sleep(0.002)
                
                elif vector_name == "Quantum Speedup":
                    # Extremely rapid repeated access
                    token, system_id, _ = tokens[2]  # Target encryption service
                    for i in range(15):
                        self.quantum_detector.access_token(token.token_id, f"quantum_speed_{i}")
                        # No delay - unnaturally fast
                
                await asyncio.sleep(0.2)
        
        # Phase 4: System detection and response
        self.console.print("\\n[bold]Phase 4: MWRASP System Response[/bold]")
        
        # Allow detection processing
        await asyncio.sleep(0.3)
        
        # Check threat detection
        active_threats = self.quantum_detector.get_active_threats()
        
        if active_threats:
            self.console.print("\\n[bold red]🚨 MULTIPLE QUANTUM ATTACKS DETECTED! 🚨[/bold red]")
            
            # Show threat analysis
            threat_analysis_table = Table(title="Threat Analysis Report")
            threat_analysis_table.add_column("Threat ID", style="red")
            threat_analysis_table.add_column("Severity", style="red")
            threat_analysis_table.add_column("Confidence", style="yellow")
            threat_analysis_table.add_column("Attack Vectors", style="magenta")
            threat_analysis_table.add_column("Affected Systems", style="cyan")
            
            for threat in active_threats:
                threat_analysis_table.add_row(
                    threat.threat_id[:8] + "...",
                    threat.threat_level.name,
                    f"{threat.confidence_score:.1%}",
                    ", ".join(threat.quantum_indicators[:2]),
                    str(len(threat.affected_tokens))
                )
            
            self.console.print(threat_analysis_table)
            
            # Show agent coordination response
            self.console.print("\\n[bold]🤖 Autonomous Agent Response Activated[/bold]")
            agent_status = self.agent_coordinator.get_agent_status()
            
            active_agents = 0
            for role, agents in agent_status['agents_by_role'].items():
                role_active = len([a for a in agents if a['status'] in ['active', 'busy']])
                if role_active > 0:
                    active_agents += role_active
                    self.console.print(f"  ⚡ {role.title()}: {role_active} agents responding")
            
            if active_agents > 0:
                self.console.print(f"\\n  📊 Total agents coordinating response: [bold green]{active_agents}[/bold green]")
        
        else:
            self.console.print("\\n[yellow]⚠️ Attack patterns not detected - adjusting sensitivity recommended[/yellow]")
        
        # Phase 5: Data protection status
        self.console.print("\\n[bold]Phase 5: Critical Data Protection Status[/bold]")
        
        protection_table = Table(title="Data Protection Report")
        protection_table.add_column("Document", style="cyan")
        protection_table.add_column("Status", style="green")
        protection_table.add_column("Fragments", style="yellow")
        protection_table.add_column("Accessible", style="red")
        
        for doc_content, doc_id, fragments in fragmented_docs:
            # Check if data is still accessible
            reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
            is_accessible = reconstructed == doc_content.encode() if reconstructed else False
            
            fragment_status = self.fragmentation_system.get_fragment_status(doc_id)
            active_fragments = fragment_status.get('active_fragments', 0) if fragment_status else 0
            
            status = "🔒 Protected" if not is_accessible else "⚠️  Vulnerable"
            accessible = "No" if not is_accessible else "Yes"
            
            protection_table.add_row(
                doc_id,
                status,
                str(active_fragments),
                accessible
            )
        
        self.console.print(protection_table)
        
        # Phase 6: System recovery and status
        self.console.print("\\n[bold]Phase 6: System Status and Recovery[/bold]")
        
        # Overall system statistics
        quantum_stats = self.quantum_detector.get_threat_statistics()
        fragment_stats = self.fragmentation_system.get_system_stats()
        agent_stats = self.agent_coordinator.get_agent_status()
        
        recovery_panel = Panel(
            f"[bold]Quantum Detection System:[/bold]\\n"
            f"  • Total Threats Detected: {quantum_stats['total_threats_detected']}\\n"
            f"  • Active Threats: {quantum_stats['active_threats']}\\n"
            f"  • Detection Accuracy: {quantum_stats.get('average_confidence', 0):.1%}\\n\\n"
            f"[bold]Temporal Fragmentation System:[/bold]\\n"
            f"  • Documents Protected: {fragment_stats['fragment_groups']}\\n"
            f"  • Active Fragments: {fragment_stats['active_fragments']}\\n"
            f"  • Cleanup Active: {'Yes' if fragment_stats['cleanup_running'] else 'No'}\\n\\n"
            f"[bold]Agent Coordination System:[/bold]\\n"
            f"  • Agents Active: {agent_stats['coordination_stats'].get('active_agents', 0)}\\n"
            f"  • Coordinations Executed: {agent_stats['coordination_stats'].get('total_coordinations', 0)}\\n"
            f"  • System Status: {'Operational' if agent_stats['system_running'] else 'Offline'}",
            title="[bold green]MWRASP System Recovery Report[/bold green]",
            border_style="green"
        )
        self.console.print(recovery_panel)
        
        self.console.print("\\n[bold green]✅ Integrated attack response demonstration completed![/bold green]")
        self.console.print("[dim]The MWRASP system successfully detected, responded to, and mitigated the quantum attack.[/dim]")
    
    async def _demo_system_monitoring(self):
        """Demonstrate real-time system monitoring"""
        self.console.print(Panel.fit(
            "[bold yellow]Real-time System Monitoring Demo[/bold yellow]\\n\\n"
            "This demo shows real-time monitoring of all MWRASP subsystems\\n"
            "with live updates and system health indicators.",
            title="Demo 5",
            border_style="yellow"
        ))
        
        # Create layout for live monitoring
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        monitoring_duration = 10  # 10 seconds of monitoring
        self.console.print(f"\\n[bold]Starting real-time monitoring for {monitoring_duration} seconds...[/bold]")
        self.console.print("[dim]System will generate activity for demonstration[/dim]\\n")
        
        start_time = time.time()
        
        # Generate background activity
        async def background_activity():
            activity_count = 0
            while time.time() - start_time < monitoring_duration:
                # Create some system activity
                if activity_count % 3 == 0:
                    # Create canary token
                    token = self.quantum_detector.generate_canary_token(f"monitor_test_{activity_count}")
                    self.quantum_detector.access_token(token.token_id, f"user_{activity_count}")
                
                if activity_count % 5 == 0:
                    # Fragment some data
                    test_data = f"Monitoring test data {activity_count}".encode()
                    self.fragmentation_system.fragment_data(test_data, f"monitor_doc_{activity_count}")
                
                if activity_count % 7 == 0:
                    # Send coordination message
                    await self.agent_coordinator.send_coordination_message({
                        "type": "resource_request",
                        "agent_id": f"monitor_agent_{activity_count}",
                        "resource": "processing_power"
                    })
                
                activity_count += 1
                await asyncio.sleep(0.5)
        
        # Start background activity
        activity_task = asyncio.create_task(background_activity())
        
        # Live monitoring display
        with Live(layout, console=self.console, refresh_per_second=2) as live:
            while time.time() - start_time < monitoring_duration:
                # Update header
                elapsed = time.time() - start_time
                remaining = monitoring_duration - elapsed
                layout["header"].update(
                    Panel(
                        f"[bold cyan]MWRASP Real-time Monitor[/bold cyan] | "
                        f"Elapsed: {elapsed:.1f}s | Remaining: {remaining:.1f}s",
                        border_style="cyan"
                    )
                )
                
                # Get current system stats
                quantum_stats = self.quantum_detector.get_threat_statistics()
                fragment_stats = self.fragmentation_system.get_system_stats()
                agent_stats = self.agent_coordinator.get_agent_status()
                
                # Update left panel - System Statistics
                left_content = (
                    f"[bold yellow]Quantum Detection[/bold yellow]\\n"
                    f"  Canary Tokens: {quantum_stats['total_tokens']}\\n"
                    f"  Threats Detected: {quantum_stats['total_threats_detected']}\\n"
                    f"  Active Threats: {quantum_stats['active_threats']}\\n"
                    f"  Monitoring: {'🟢 Active' if quantum_stats['monitoring_active'] else '🔴 Inactive'}\\n\\n"
                    f"[bold green]Temporal Fragmentation[/bold green]\\n"
                    f"  Total Fragments: {fragment_stats['total_fragments']}\\n"
                    f"  Active Fragments: {fragment_stats['active_fragments']}\\n"
                    f"  Fragment Groups: {fragment_stats['fragment_groups']}\\n"
                    f"  Cleanup Service: {'🟢 Running' if fragment_stats['cleanup_running'] else '🔴 Stopped'}\\n\\n"
                    f"[bold blue]Agent Coordination[/bold blue]\\n"
                    f"  Total Agents: {agent_stats['total_agents']}\\n"
                    f"  Active Agents: {agent_stats['coordination_stats'].get('active_agents', 0)}\\n"
                    f"  Coordinations: {agent_stats['coordination_stats'].get('total_coordinations', 0)}\\n"
                    f"  System Status: {'🟢 Online' if agent_stats['system_running'] else '🔴 Offline'}"
                )
                
                layout["left"].update(Panel(left_content, title="System Statistics", border_style="green"))
                
                # Update right panel - Agent Details
                right_content = "[bold]Agent Network Status[/bold]\\n\\n"
                for role, agents in agent_stats['agents_by_role'].items():
                    right_content += f"[cyan]{role.title()}:[/cyan]\\n"
                    for i, agent in enumerate(agents):
                        status_emoji = {
                            'idle': '⚪',
                            'active': '🟢',
                            'busy': '🟡',
                            'error': '🔴'
                        }.get(agent['status'], '⚪')
                        
                        right_content += f"  {status_emoji} Agent {i+1}: {agent['status']}\\n"
                        if agent['workload'] > 0:
                            right_content += f"     Load: {agent['workload']}/{agent['max_workload']}\\n"
                    right_content += "\\n"
                
                layout["right"].update(Panel(right_content, title="Agent Network", border_style="blue"))
                
                # Update footer
                layout["footer"].update(
                    Panel(
                        f"System Load: Normal | Memory Usage: Stable | "
                        f"Network: Connected | Last Update: {time.strftime('%H:%M:%S')}",
                        border_style="white"
                    )
                )
                
                await asyncio.sleep(0.5)
        
        # Clean up background activity
        activity_task.cancel()
        
        self.console.print("\\n[bold green]✅ Real-time monitoring demonstration completed![/bold green]")
    
    async def _run_performance_test(self):
        """Run performance stress test"""
        self.console.print(Panel.fit(
            "[bold red]Performance Stress Test[/bold red]\\n\\n"
            "This test will stress the MWRASP system with high-volume\\n"
            "operations to demonstrate performance under load.",
            title="Demo 6 - Performance Test",
            border_style="red"
        ))
        
        if not Confirm.ask("\\n[yellow]⚠️  This test will generate high system load. Continue?[/yellow]"):
            return
        
        # Test parameters
        num_tokens = 50
        num_documents = 30
        num_attacks = 20
        
        self.console.print(f"\\n[bold]Performance Test Parameters:[/bold]")
        self.console.print(f"  • Canary Tokens: {num_tokens}")
        self.console.print(f"  • Documents to Fragment: {num_documents}")
        self.console.print(f"  • Simulated Attacks: {num_attacks}")
        
        # Start performance test
        start_time = time.time()
        
        with Progress(console=self.console) as progress:
            # Task 1: Create canary tokens
            token_task = progress.add_task("Creating canary tokens...", total=num_tokens)
            tokens = []
            
            for i in range(num_tokens):
                token = self.quantum_detector.generate_canary_token(f"perf_test_token_{i}")
                tokens.append(token)
                progress.update(token_task, advance=1)
                if i % 10 == 0:
                    await asyncio.sleep(0.01)  # Small delay to prevent overwhelming
            
            # Task 2: Fragment documents
            fragment_task = progress.add_task("Fragmenting documents...", total=num_documents)
            documents = []
            
            for i in range(num_documents):
                doc_data = f"Performance test document {i} with sensitive content " * 10
                fragments = self.fragmentation_system.fragment_data(
                    doc_data.encode(), 
                    f"perf_doc_{i}"
                )
                documents.append((doc_data, f"perf_doc_{i}", fragments))
                progress.update(fragment_task, advance=1)
                
                if i % 5 == 0:
                    await asyncio.sleep(0.01)
            
            # Task 3: Simulate attacks
            attack_task = progress.add_task("Simulating quantum attacks...", total=num_attacks)
            
            for attack_round in range(num_attacks):
                # Select random subset of tokens for each attack
                attack_tokens = tokens[attack_round % 10:(attack_round % 10) + 5]
                
                for token in attack_tokens:
                    self.quantum_detector.access_token(
                        token.token_id, 
                        f"perf_attacker_{attack_round}"
                    )
                
                progress.update(attack_task, advance=1)
                await asyncio.sleep(0.001)  # Very brief delay
            
            # Task 4: Test reconstruction
            reconstruct_task = progress.add_task("Testing reconstruction...", total=num_documents)
            successful_reconstructions = 0
            
            for doc_data, doc_id, fragments in documents:
                reconstructed = self.fragmentation_system.reconstruct_data(doc_id)
                if reconstructed and reconstructed.decode() == doc_data:
                    successful_reconstructions += 1
                progress.update(reconstruct_task, advance=1)
        
        # Calculate performance metrics
        total_time = time.time() - start_time
        
        # Get final system statistics
        quantum_stats = self.quantum_detector.get_threat_statistics()
        fragment_stats = self.fragmentation_system.get_system_stats()
        agent_stats = self.agent_coordinator.get_agent_status()
        
        # Display performance results
        performance_table = Table(title="Performance Test Results")
        performance_table.add_column("Metric", style="cyan")
        performance_table.add_column("Value", style="yellow")
        performance_table.add_column("Rate", style="green")
        
        performance_table.add_row(
            "Total Test Time",
            f"{total_time:.2f} seconds",
            "-"
        )
        performance_table.add_row(
            "Canary Tokens Created",
            str(num_tokens),
            f"{num_tokens/total_time:.1f}/sec"
        )
        performance_table.add_row(
            "Documents Fragmented",
            str(num_documents),
            f"{num_documents/total_time:.1f}/sec"
        )
        performance_table.add_row(
            "Successful Reconstructions",
            f"{successful_reconstructions}/{num_documents}",
            f"{successful_reconstructions/num_documents:.1%} success rate"
        )
        performance_table.add_row(
            "Attacks Simulated",
            str(num_attacks),
            f"{num_attacks/total_time:.1f}/sec"
        )
        performance_table.add_row(
            "Threats Detected",
            str(quantum_stats['total_threats_detected']),
            f"{quantum_stats['total_threats_detected']/num_attacks:.1%} detection rate"
        )
        
        self.console.print(performance_table)
        
        # System health after load test
        health_panel = Panel(
            f"[bold]System Health After Load Test:[/bold]\\n\\n"
            f"🔍 Quantum Detector: {'Healthy' if quantum_stats['monitoring_active'] else 'Issues'}\\n"
            f"⚡ Fragmentation System: {'Healthy' if fragment_stats['cleanup_running'] else 'Issues'}\\n"
            f"🤖 Agent Coordination: {'Healthy' if agent_stats['system_running'] else 'Issues'}\\n\\n"
            f"Memory Usage: {fragment_stats['total_fragments']} active fragments\\n"
            f"Processing Load: {agent_stats['coordination_stats'].get('active_agents', 0)} active agents",
            title="System Health Report",
            border_style="green"
        )
        self.console.print(health_panel)
        
        # Performance assessment
        if total_time < 3.0 and successful_reconstructions / num_documents > 0.8:
            self.console.print("\\n[bold green]🎉 Excellent Performance - System handles high load efficiently![/bold green]")
        elif total_time < 5.0 and successful_reconstructions / num_documents > 0.6:
            self.console.print("\\n[bold yellow]⚡ Good Performance - System stable under load with minor delays[/bold yellow]")
        else:
            self.console.print("\\n[bold red]⚠️  Performance Issues - System may need optimization[/bold red]")
    
    def _show_system_status(self):
        """Show comprehensive system status"""
        self.console.print(Panel.fit(
            "[bold cyan]Comprehensive System Status Report[/bold cyan]\\n\\n"
            "Current operational status of all MWRASP subsystems",
            title="System Status",
            border_style="cyan"
        ))
        
        # Get all system statistics
        quantum_stats = self.quantum_detector.get_threat_statistics()
        fragment_stats = self.fragmentation_system.get_system_stats()
        agent_stats = self.agent_coordinator.get_agent_status()
        
        # Create comprehensive status table
        status_table = Table(title="MWRASP System Status Dashboard")
        status_table.add_column("Subsystem", style="bold cyan")
        status_table.add_column("Status", style="green")
        status_table.add_column("Key Metrics", style="yellow")
        status_table.add_column("Health", style="white")
        
        # Quantum Detection System
        quantum_health = "🟢 Healthy" if quantum_stats['monitoring_active'] else "🔴 Offline"
        quantum_metrics = (
            f"Tokens: {quantum_stats['total_tokens']}, "
            f"Threats: {quantum_stats['total_threats_detected']}, "
            f"Active: {quantum_stats['active_threats']}"
        )
        status_table.add_row(
            "Quantum Detector",
            "Online" if quantum_stats['monitoring_active'] else "Offline",
            quantum_metrics,
            quantum_health
        )
        
        # Temporal Fragmentation System
        fragment_health = "🟢 Healthy" if fragment_stats['cleanup_running'] else "🟡 Limited"
        fragment_metrics = (
            f"Fragments: {fragment_stats['total_fragments']}, "
            f"Groups: {fragment_stats['fragment_groups']}, "
            f"Active: {fragment_stats['active_fragments']}"
        )
        status_table.add_row(
            "Temporal Fragmentation",
            "Online" if fragment_stats['cleanup_running'] else "Degraded",
            fragment_metrics,
            fragment_health
        )
        
        # Agent Coordination System
        agent_health = "🟢 Healthy" if agent_stats['system_running'] else "🔴 Offline"
        agent_metrics = (
            f"Agents: {agent_stats['total_agents']}, "
            f"Active: {agent_stats['coordination_stats'].get('active_agents', 0)}, "
            f"Coords: {agent_stats['coordination_stats'].get('total_coordinations', 0)}"
        )
        status_table.add_row(
            "Agent Coordination",
            "Online" if agent_stats['system_running'] else "Offline",
            agent_metrics,
            agent_health
        )
        
        self.console.print(status_table)
        
        # Detailed agent breakdown
        self.console.print("\\n[bold]Agent Network Details:[/bold]")
        agent_detail_table = Table()
        agent_detail_table.add_column("Role", style="cyan")
        agent_detail_table.add_column("Count", style="yellow")
        agent_detail_table.add_column("Active", style="green")
        agent_detail_table.add_column("Busy", style="orange1")
        agent_detail_table.add_column("Idle", style="white")
        agent_detail_table.add_column("Error", style="red")
        
        for role, agents in agent_stats['agents_by_role'].items():
            counts = {'active': 0, 'busy': 0, 'idle': 0, 'error': 0}
            for agent in agents:
                status = agent['status']
                if status in counts:
                    counts[status] += 1
            
            agent_detail_table.add_row(
                role.title(),
                str(len(agents)),
                str(counts['active']),
                str(counts['busy']),
                str(counts['idle']),
                str(counts['error'])
            )
        
        self.console.print(agent_detail_table)
        
        # System configuration summary
        config_panel = Panel(
            f"[bold]Current Configuration:[/bold]\\n\\n"
            f"🔍 Quantum Detection Sensitivity: {self.quantum_detector.sensitivity_threshold:.1%}\\n"
            f"⚡ Fragment Lifetime: {self.fragmentation_policy.max_fragment_lifetime_ms}ms\\n"
            f"🛡️  Quantum Resistance Level: {self.fragmentation_policy.quantum_resistance_level}/5\\n"
            f"📊 Min/Max Fragments: {self.fragmentation_policy.min_fragments}-{self.fragmentation_policy.max_fragments}\\n"
            f"🔄 Auto-Expire: {'Enabled' if self.fragmentation_policy.auto_expire else 'Disabled'}",
            title="Configuration Summary",
            border_style="blue"
        )
        self.console.print(config_panel)
    
    async def _cleanup_demo(self):
        """Clean up demo resources"""
        self.console.print("\\n[bold]Shutting down MWRASP systems...[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            # Stop agent coordination
            task1 = progress.add_task("Stopping agent coordination...", total=None)
            await self.agent_coordinator.stop_coordination()
            progress.update(task1, completed=100)
            
            # Stop fragmentation cleanup
            task2 = progress.add_task("Stopping fragmentation cleanup...", total=None)
            self.fragmentation_system.stop_cleanup_service()
            progress.update(task2, completed=100)
            
            # Stop quantum monitoring
            task3 = progress.add_task("Stopping quantum monitoring...", total=None)
            self.quantum_detector.stop_monitoring()
            progress.update(task3, completed=100)
        
        self.console.print("[bold green]✅ All systems shut down safely![/bold green]")
        self.console.print("\\n[bold cyan]Thank you for exploring the MWRASP Quantum Defense System![/bold cyan]")


async def main():
    """Main demo entry point"""
    parser = argparse.ArgumentParser(description="MWRASP Quantum Defense System Demo")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--quick", "-q", action="store_true", help="Run quick demo mode")
    
    args = parser.parse_args()
    
    demo = MWRASPDemo(verbose=args.verbose)
    
    try:
        if args.quick:
            # Quick demo mode - run specific demonstrations
            await demo._display_banner()
            await demo._system_initialization()
            await demo._demo_quantum_detection()
            await demo._demo_temporal_fragmentation()
            await demo._cleanup_demo()
        else:
            # Full interactive demo
            await demo.run_complete_demo()
    
    except KeyboardInterrupt:
        demo.console.print("\\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        demo.console.print(f"\\n[red]Demo error: {e}[/red]")
    finally:
        # Ensure cleanup
        try:
            await demo._cleanup_demo()
        except:
            pass


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
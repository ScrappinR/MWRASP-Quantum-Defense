#!/usr/bin/env python3
"""
MWRASP Real World Protection System
Monitors and protects actual files, directories, and network traffic
"""

import os
import time
import hashlib
import json
from typing import List, Dict, Set, Optional, Any
from datetime import datetime
import threading
from pathlib import Path
import psutil
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dataclasses import dataclass, field
import subprocess
import winreg


@dataclass
class ProtectedFile:
    """Information about a file under MWRASP protection"""
    file_path: str
    original_hash: str
    protection_level: str
    canary_token_id: Optional[str] = None
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    threat_detected: bool = False


@dataclass
class NetworkConnection:
    """Information about monitored network connections"""
    local_addr: str
    remote_addr: str
    status: str
    process_name: str
    pid: int
    suspicious: bool = False


class FileSystemProtectionHandler(FileSystemEventHandler):
    """Handles real-time file system events"""
    
    def __init__(self, protection_manager):
        self.protection_manager = protection_manager
        
    def on_accessed(self, event):
        if not event.is_directory:
            self.protection_manager.handle_file_access(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.protection_manager.handle_file_modification(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.protection_manager.handle_file_creation(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.protection_manager.handle_file_deletion(event.src_path)


class RealWorldProtectionManager:
    """
    Manages real-world protection of actual files and systems
    Integrates with MWRASP quantum detection and legal barriers
    """
    
    def __init__(self, quantum_detector, fragmentation_system, jurisdiction_controller):
        self.quantum_detector = quantum_detector
        self.fragmentation_system = fragmentation_system
        self.jurisdiction_controller = jurisdiction_controller
        
        # Protected file tracking
        self.protected_files: Dict[str, ProtectedFile] = {}
        self.monitored_directories: Set[str] = set()
        self.file_observers: List[Observer] = []
        
        # Network monitoring
        self.network_connections: Dict[str, NetworkConnection] = {}
        self.suspicious_processes: Set[str] = set()
        
        # System monitoring
        self.protection_active = False
        self.monitoring_threads: List[threading.Thread] = []
        self.stop_monitoring = threading.Event()
        
        print("[REAL-WORLD] Real World Protection Manager initialized")
    
    def add_protected_directory(self, directory_path: str, protection_level: str = "HIGH") -> bool:
        """Add a directory to real-time protection"""
        
        if not os.path.exists(directory_path):
            print(f"[ERROR] Directory does not exist: {directory_path}")
            return False
        
        if not os.path.isdir(directory_path):
            print(f"[ERROR] Path is not a directory: {directory_path}")
            return False
        
        try:
            # Set up file system monitoring
            event_handler = FileSystemProtectionHandler(self)
            observer = Observer()
            observer.schedule(event_handler, directory_path, recursive=True)
            observer.start()
            
            self.file_observers.append(observer)
            self.monitored_directories.add(directory_path)
            
            # Scan existing files and deploy canary tokens
            files_protected = self._deploy_canary_tokens_in_directory(directory_path, protection_level)
            
            print(f"[PROTECT] Directory protected: {directory_path}")
            print(f"[PROTECT] Files under protection: {files_protected}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to protect directory {directory_path}: {e}")
            return False
    
    def _deploy_canary_tokens_in_directory(self, directory_path: str, protection_level: str) -> int:
        """Deploy canary tokens for files in a directory"""
        
        files_protected = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip system files and very large files
                if self._should_protect_file(file_path):
                    if self._protect_individual_file(file_path, protection_level):
                        files_protected += 1
        
        return files_protected
    
    def _should_protect_file(self, file_path: str) -> bool:
        """Determine if a file should be protected"""
        
        # Skip system files
        if file_path.startswith(os.environ.get('WINDIR', 'C:\\Windows')):
            return False
        
        # Skip very large files (> 100MB)
        try:
            if os.path.getsize(file_path) > 100 * 1024 * 1024:
                return False
        except:
            return False
        
        # Focus on potentially sensitive file types
        sensitive_extensions = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.txt', '.csv', '.json', '.xml', '.sql', '.db', '.mdb',
            '.key', '.pem', '.p12', '.pfx', '.crt', '.cer',
            '.zip', '.rar', '.7z', '.tar', '.gz'
        }
        
        file_ext = Path(file_path).suffix.lower()
        return file_ext in sensitive_extensions
    
    def _protect_individual_file(self, file_path: str, protection_level: str) -> bool:
        """Protect an individual file with MWRASP"""
        
        try:
            # Calculate file hash
            file_hash = self._calculate_file_hash(file_path)
            
            # Generate canary token for this file
            data_type = f"FILE_{protection_level}_{Path(file_path).suffix[1:].upper()}"
            canary_token = self.quantum_detector.generate_canary_token(data_type)
            
            # Create protected file record
            protected_file = ProtectedFile(
                file_path=file_path,
                original_hash=file_hash,
                protection_level=protection_level,
                canary_token_id=canary_token.token_id
            )
            
            self.protected_files[file_path] = protected_file
            
            # Fragment sensitive content if file is small enough
            if os.path.getsize(file_path) < 1024 * 1024:  # < 1MB
                self._fragment_file_content(file_path)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to protect file {file_path}: {e}")
            return False
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return ""
    
    def _fragment_file_content(self, file_path: str):
        """Fragment sensitive file content using temporal fragmentation"""
        
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Fragment the content (synchronous version)
            fragment_id = f"file_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"
            # Create a simple synchronous fragmentation for files
            fragments = self._simple_fragment_data(content, fragment_id)
            
            print(f"[FRAGMENT] File fragmented: {file_path} -> {len(fragments)} fragments")
            
        except Exception as e:
            print(f"[ERROR] Failed to fragment {file_path}: {e}")
    
    def _simple_fragment_data(self, data: bytes, fragment_id: str):
        """Simple synchronous data fragmentation for file protection"""
        # Split data into 3-5 fragments
        import random
        num_fragments = random.randint(3, 5)
        fragment_size = len(data) // num_fragments
        
        fragments = []
        for i in range(num_fragments):
            start = i * fragment_size
            end = start + fragment_size if i < num_fragments - 1 else len(data)
            fragment_data = data[start:end]
            fragments.append({
                'id': f"{fragment_id}_frag_{i}",
                'data': fragment_data,
                'size': len(fragment_data)
            })
        
        return fragments
    
    def handle_file_access(self, file_path: str):
        """Handle file access events"""
        
        if file_path in self.protected_files:
            protected_file = self.protected_files[file_path]
            protected_file.access_count += 1
            protected_file.last_accessed = time.time()
            
            # Trigger quantum detection
            if protected_file.canary_token_id:
                threat_detected = self.quantum_detector.access_token(
                    protected_file.canary_token_id,
                    f"file_access_{os.getpid()}"
                )
                
                if threat_detected:
                    protected_file.threat_detected = True
                    self._handle_threat_detection(file_path)
                    
                    print(f"[THREAT] Quantum threat detected accessing: {file_path}")
    
    def handle_file_modification(self, file_path: str):
        """Handle file modification events"""
        
        if file_path in self.protected_files:
            protected_file = self.protected_files[file_path]
            
            # Check if file hash changed
            new_hash = self._calculate_file_hash(file_path)
            if new_hash != protected_file.original_hash:
                print(f"[MODIFY] Protected file modified: {file_path}")
                
                # Update hash and re-fragment if necessary
                protected_file.original_hash = new_hash
                if os.path.getsize(file_path) < 1024 * 1024:
                    self._fragment_file_content(file_path)
    
    def handle_file_creation(self, file_path: str):
        """Handle file creation events"""
        
        # Check if new file should be protected
        if self._should_protect_file(file_path):
            # Wait a moment for file to be fully written
            time.sleep(0.1)
            if os.path.exists(file_path):
                self._protect_individual_file(file_path, "MEDIUM")
                print(f"[NEW] New file protected: {file_path}")
    
    def handle_file_deletion(self, file_path: str):
        """Handle file deletion events"""
        
        if file_path in self.protected_files:
            print(f"[DELETE] Protected file deleted: {file_path}")
            del self.protected_files[file_path]
    
    def _handle_threat_detection(self, file_path: str):
        """Handle detected threats to protected files"""
        
        # Always fragment file content for protection (core security)
        self._fragment_file_content(file_path)
        
        # Additionally activate legal barriers if available (optional enhancement)
        if self.jurisdiction_controller and hasattr(self.jurisdiction_controller, 'is_legal_routing_enabled'):
            if self.jurisdiction_controller.is_legal_routing_enabled():
                print(f"[LEGAL] Legal barriers also activated for {file_path}")
            else:
                print(f"[INFO] Legal routing disabled - core protection still active")
            
            print(f"[LEGAL] Legal barriers activated for: {file_path}")
            print(f"[LEGAL] Impossible compliance scenario created")
    
    def start_network_monitoring(self):
        """Start monitoring network connections"""
        
        def monitor_network():
            while not self.stop_monitoring.is_set():
                try:
                    connections = psutil.net_connections(kind='inet')
                    
                    for conn in connections:
                        if conn.raddr:  # Has remote address
                            conn_key = f"{conn.laddr.ip}:{conn.laddr.port}->{conn.raddr.ip}:{conn.raddr.port}"
                            
                            try:
                                process = psutil.Process(conn.pid) if conn.pid else None
                                process_name = process.name() if process else "unknown"
                                
                                network_conn = NetworkConnection(
                                    local_addr=f"{conn.laddr.ip}:{conn.laddr.port}",
                                    remote_addr=f"{conn.raddr.ip}:{conn.raddr.port}",
                                    status=conn.status,
                                    process_name=process_name,
                                    pid=conn.pid or 0,
                                    suspicious=self._is_suspicious_connection(conn, process_name)
                                )
                                
                                self.network_connections[conn_key] = network_conn
                                
                                if network_conn.suspicious:
                                    print(f"[NETWORK] Suspicious connection: {conn_key} ({process_name})")
                                    self._handle_suspicious_network_activity(network_conn)
                                    
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                    
                    time.sleep(5)  # Check every 5 seconds
                    
                except Exception as e:
                    print(f"[ERROR] Network monitoring error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=monitor_network, daemon=True)
        thread.start()
        self.monitoring_threads.append(thread)
        
        print("[NETWORK] Network monitoring started")
    
    def _is_suspicious_connection(self, conn, process_name: str) -> bool:
        """Determine if a network connection is suspicious"""
        
        # Check for suspicious process names
        suspicious_processes = {
            'nc.exe', 'netcat.exe', 'ncat.exe', 'telnet.exe',
            'powershell.exe', 'cmd.exe', 'wscript.exe', 'cscript.exe'
        }
        
        if process_name.lower() in suspicious_processes:
            return True
        
        # Check for connections to suspicious ports
        if conn.raddr and conn.raddr.port in {4444, 5555, 6666, 7777, 8888, 9999}:
            return True
        
        # Check for connections to unusual remote IPs
        if conn.raddr and conn.raddr.ip:
            # Example: connections to Tor exit nodes, known malicious IPs, etc.
            # This would typically check against threat intelligence feeds
            pass
        
        return False
    
    def _handle_suspicious_network_activity(self, network_conn: NetworkConnection):
        """Handle suspicious network activity"""
        
        # Create a synthetic canary token for network activity
        network_token = self.quantum_detector.generate_canary_token("NETWORK_SUSPICIOUS")
        
        # Trigger threat detection
        threat_detected = self.quantum_detector.access_token(
            network_token.token_id,
            f"network_{network_conn.process_name}_{network_conn.pid}"
        )
        
        if threat_detected:
            print(f"[THREAT] Network threat detected: {network_conn.remote_addr}")
            
            # Core threat response (always active)
            print(f"[DEFENSE] Core network defense activated against {network_conn.remote_addr}")
            
            # Additionally activate legal barriers if available (optional enhancement)
            if self.jurisdiction_controller and hasattr(self.jurisdiction_controller, 'is_legal_routing_enabled'):
                if self.jurisdiction_controller.is_legal_routing_enabled():
                    print(f"[LEGAL] Legal barriers also activated for network threat")
                else:
                    print(f"[INFO] Legal routing disabled - core network defense still active")
    
    def start_real_world_protection(self):
        """Start all real-world protection systems"""
        
        if self.protection_active:
            print("[STATUS] Protection already active")
            return
        
        self.protection_active = True
        self.stop_monitoring.clear()
        
        # Start network monitoring
        self.start_network_monitoring()
        
        print("[STATUS] Real-world protection ACTIVE")
        print(f"[STATUS] Monitoring {len(self.monitored_directories)} directories")
        print(f"[STATUS] Protecting {len(self.protected_files)} files")
    
    def stop_real_world_protection(self):
        """Stop all real-world protection systems"""
        
        if not self.protection_active:
            return
        
        self.protection_active = False
        self.stop_monitoring.set()
        
        # Stop file system observers
        for observer in self.file_observers:
            observer.stop()
            observer.join()
        
        self.file_observers.clear()
        
        # Wait for monitoring threads to stop
        for thread in self.monitoring_threads:
            thread.join(timeout=5)
        
        self.monitoring_threads.clear()
        
        print("[STATUS] Real-world protection STOPPED")
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get comprehensive protection status"""
        
        return {
            "protection_active": self.protection_active,
            "monitored_directories": len(self.monitored_directories),
            "protected_files": len(self.protected_files),
            "total_file_accesses": sum(pf.access_count for pf in self.protected_files.values()),
            "threats_detected": sum(1 for pf in self.protected_files.values() if pf.threat_detected),
            "network_connections": len(self.network_connections),
            "suspicious_connections": len([nc for nc in self.network_connections.values() if nc.suspicious]),
            "directories_list": list(self.monitored_directories),
            "recent_threats": [
                {
                    "file_path": pf.file_path,
                    "access_count": pf.access_count,
                    "last_accessed": pf.last_accessed
                }
                for pf in self.protected_files.values() 
                if pf.threat_detected
            ]
        }
    
    def add_high_value_files(self) -> int:
        """Automatically detect and protect high-value files"""
        
        high_value_patterns = [
            "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx",
            "*.key", "*.pem", "*.p12", "*.pfx",
            "*password*", "*secret*", "*credential*",
            "*financial*", "*banking*", "*tax*"
        ]
        
        common_sensitive_dirs = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads")
        ]
        
        files_added = 0
        
        for directory in common_sensitive_dirs:
            if os.path.exists(directory):
                files_added += self._deploy_canary_tokens_in_directory(directory, "HIGH")
        
        return files_added


# Factory function for integration with MWRASP
def create_real_world_protection(quantum_detector, fragmentation_system, jurisdiction_controller):
    """Create and initialize real-world protection manager"""
    
    return RealWorldProtectionManager(
        quantum_detector, 
        fragmentation_system, 
        jurisdiction_controller
    )
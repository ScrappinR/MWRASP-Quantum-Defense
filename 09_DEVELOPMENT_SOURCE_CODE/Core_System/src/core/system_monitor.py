#!/usr/bin/env python3
"""
MWRASP System Performance Monitor
Real-time monitoring of MWRASP's resource usage and system performance
"""

import psutil
import os
import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque
import json


class MWRASPSystemMonitor:
    """
    Real-time system performance monitoring for MWRASP
    Tracks CPU, memory, disk, and network usage specifically for MWRASP processes
    """
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = time.time()
        
        # Performance history (last 60 data points)
        self.cpu_history = deque(maxlen=60)
        self.memory_history = deque(maxlen=60)
        self.disk_history = deque(maxlen=60)
        self.network_history = deque(maxlen=60)
        
        # Current metrics
        self.current_metrics = {}
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread = None
        self.stop_event = threading.Event()
        
        print("[MONITOR] MWRASP System Performance Monitor initialized")
    
    def start_monitoring(self):
        """Start real-time performance monitoring"""
        
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.stop_event.clear()
        
        def monitor_loop():
            while not self.stop_event.is_set():
                try:
                    self._collect_metrics()
                    time.sleep(1)  # Collect metrics every second
                except Exception as e:
                    print(f"[MONITOR] Error collecting metrics: {e}")
                    time.sleep(5)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("[MONITOR] Real-time performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        self.stop_event.set()
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        
        print("[MONITOR] Performance monitoring stopped")
    
    def _collect_metrics(self):
        """Collect current system metrics"""
        
        try:
            # CPU metrics
            cpu_percent = self.process.cpu_percent()
            system_cpu = psutil.cpu_percent(interval=0.1)
            
            # Memory metrics
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            system_memory = psutil.virtual_memory()
            
            # Disk I/O
            try:
                disk_io = self.process.io_counters()
                disk_read = disk_io.read_bytes
                disk_write = disk_io.write_bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                disk_read = 0
                disk_write = 0
            
            # Network connections
            try:
                connections = self.process.connections()
                network_connections = len(connections)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                network_connections = 0
            
            # Threads and handles
            num_threads = self.process.num_threads()
            
            # Calculate uptime
            uptime = time.time() - self.start_time
            
            # Update current metrics
            self.current_metrics = {
                # MWRASP-specific metrics
                'mwrasp_cpu_percent': cpu_percent,
                'mwrasp_memory_mb': memory_info.rss / 1024 / 1024,
                'mwrasp_memory_percent': memory_percent,
                'mwrasp_threads': num_threads,
                'mwrasp_connections': network_connections,
                'mwrasp_disk_read_mb': disk_read / 1024 / 1024,
                'mwrasp_disk_write_mb': disk_write / 1024 / 1024,
                'mwrasp_uptime': uptime,
                
                # System-wide metrics
                'system_cpu_percent': system_cpu,
                'system_memory_percent': system_memory.percent,
                'system_memory_available_gb': system_memory.available / 1024 / 1024 / 1024,
                'system_memory_total_gb': system_memory.total / 1024 / 1024 / 1024,
                
                # Performance indicators
                'cpu_efficiency': min(100, (cpu_percent / max(system_cpu, 1)) * 100),
                'memory_efficiency': memory_percent / max(system_memory.percent, 1) * 100,
                'uptime_hours': uptime / 3600,
                
                'timestamp': time.time(),
                'datetime': datetime.now().isoformat()
            }
            
            # Add to history
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory_info.rss / 1024 / 1024)
            self.disk_history.append((disk_read + disk_write) / 1024 / 1024)
            self.network_history.append(network_connections)
            
        except Exception as e:
            print(f"[MONITOR] Error collecting metrics: {e}")
    
    def get_current_performance(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        
        if not self.current_metrics:
            # If monitoring not started, collect metrics once
            self._collect_metrics()
        
        return self.current_metrics.copy()
    
    def get_performance_history(self) -> Dict[str, List]:
        """Get performance history for charts"""
        
        return {
            'cpu_history': list(self.cpu_history),
            'memory_history': list(self.memory_history),
            'disk_history': list(self.disk_history),
            'network_history': list(self.network_history),
            'timestamps': [time.time() - i for i in range(len(self.cpu_history) - 1, -1, -1)]
        }
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get resource usage summary"""
        
        current = self.get_current_performance()
        
        return {
            'status': 'healthy' if current.get('mwrasp_cpu_percent', 0) < 80 else 'warning',
            'mwrasp_resources': {
                'cpu_percent': current.get('mwrasp_cpu_percent', 0),
                'memory_mb': current.get('mwrasp_memory_mb', 0),
                'memory_percent': current.get('mwrasp_memory_percent', 0),
                'threads': current.get('mwrasp_threads', 0),
                'connections': current.get('mwrasp_connections', 0),
                'uptime_hours': current.get('uptime_hours', 0)
            },
            'system_resources': {
                'cpu_percent': current.get('system_cpu_percent', 0),
                'memory_percent': current.get('system_memory_percent', 0),
                'memory_available_gb': current.get('system_memory_available_gb', 0),
                'memory_total_gb': current.get('system_memory_total_gb', 0)
            },
            'efficiency': {
                'cpu_efficiency': current.get('cpu_efficiency', 100),
                'memory_efficiency': current.get('memory_efficiency', 100)
            },
            'last_updated': current.get('datetime', datetime.now().isoformat())
        }
    
    def get_detailed_process_info(self) -> Dict[str, Any]:
        """Get detailed information about MWRASP processes"""
        
        try:
            # Get all Python processes that might be MWRASP-related
            mwrasp_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
                try:
                    if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'mwrasp' in cmdline.lower() or 'uvicorn' in cmdline.lower() and 'server' in cmdline.lower():
                            mwrasp_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cmdline': cmdline,
                                'cpu_percent': proc.cpu_percent(),
                                'memory_mb': proc.info['memory_info'].rss / 1024 / 1024 if proc.info['memory_info'] else 0,
                                'status': proc.status(),
                                'create_time': proc.create_time()
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'main_process': {
                    'pid': self.process.pid,
                    'cpu_percent': self.current_metrics.get('mwrasp_cpu_percent', 0),
                    'memory_mb': self.current_metrics.get('mwrasp_memory_mb', 0),
                    'threads': self.current_metrics.get('mwrasp_threads', 0),
                    'connections': self.current_metrics.get('mwrasp_connections', 0)
                },
                'all_mwrasp_processes': mwrasp_processes,
                'total_processes': len(mwrasp_processes),
                'monitoring_active': self.monitoring_active
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'main_process': {'pid': self.process.pid},
                'monitoring_active': self.monitoring_active
            }
    
    def export_performance_report(self) -> Dict[str, Any]:
        """Export comprehensive performance report"""
        
        return {
            'report_timestamp': datetime.now().isoformat(),
            'monitoring_duration': time.time() - self.start_time,
            'current_performance': self.get_current_performance(),
            'resource_summary': self.get_resource_summary(),
            'performance_history': self.get_performance_history(),
            'process_details': self.get_detailed_process_info(),
            'system_info': {
                'platform': psutil.WINDOWS if psutil.WINDOWS else 'other',
                'boot_time': psutil.boot_time(),
                'cpu_count': psutil.cpu_count(),
                'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            }
        }


# Global monitor instance
_system_monitor = None

def get_system_monitor() -> MWRASPSystemMonitor:
    """Get or create global system monitor instance"""
    global _system_monitor
    if _system_monitor is None:
        _system_monitor = MWRASPSystemMonitor()
        _system_monitor.start_monitoring()
    return _system_monitor

def get_performance_metrics() -> Dict[str, Any]:
    """Quick function to get current performance metrics"""
    return get_system_monitor().get_current_performance()

def get_resource_usage() -> Dict[str, Any]:
    """Quick function to get resource usage summary"""
    return get_system_monitor().get_resource_summary()
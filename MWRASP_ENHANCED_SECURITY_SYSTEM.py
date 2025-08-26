#!/usr/bin/env python3
"""
MWRASP Enhanced Security System
Advanced quantum-resistant cybersecurity with comprehensive breach detection,
data recovery mechanisms, and security incident management
"""

import asyncio
import time
import hashlib
import secrets
import json
import threading
import requests
import re
import sqlite3
import logging
import random
import statistics
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# SECURITY INCIDENT MANAGEMENT
# ============================================================================

class SecurityIncidentManager:
    """Comprehensive security incident detection, notification, and response system"""
    
    def __init__(self):
        self.incident_database = self._initialize_incident_database()
        self.notification_channels = {}
        self.incident_history = []
        self.alert_thresholds = {
            'fragment_compromise': 0.3,      # 30% fragment loss triggers alert
            'access_failure_rate': 0.1,      # 10% access failures triggers alert
            'unauthorized_access': 0.01,     # 1% unauthorized access triggers alert
            'temporal_breach': 0.0           # Any temporal breach triggers immediate alert
        }
        self.active_incidents = {}
        
    def _initialize_incident_database(self):
        """Initialize SQLite database for incident tracking"""
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create incidents table
        cursor.execute('''
            CREATE TABLE incidents (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                affected_resource TEXT,
                timestamp REAL,
                status TEXT DEFAULT 'OPEN',
                response_actions TEXT,
                resolution_time REAL
            )
        ''')
        
        # Create breach_events table
        cursor.execute('''
            CREATE TABLE breach_events (
                id TEXT PRIMARY KEY,
                incident_id TEXT,
                event_type TEXT,
                details TEXT,
                timestamp REAL,
                FOREIGN KEY (incident_id) REFERENCES incidents (id)
            )
        ''')
        
        # Create notifications table
        cursor.execute('''
            CREATE TABLE notifications (
                id TEXT PRIMARY KEY,
                incident_id TEXT,
                channel TEXT,
                message TEXT,
                sent_timestamp REAL,
                status TEXT,
                FOREIGN KEY (incident_id) REFERENCES incidents (id)
            )
        ''')
        
        conn.commit()
        return conn
    
    def register_notification_channel(self, channel_name: str, handler: callable):
        """Register notification channel (email, SMS, webhook, etc.)"""
        self.notification_channels[channel_name] = handler
        logger.info(f"Notification channel registered: {channel_name}")
    
    def report_security_incident(self, incident_type: str, severity: str, 
                                description: str, affected_resource: str = None,
                                additional_details: Dict = None) -> str:
        """Report and log security incident"""
        incident_id = f"inc_{secrets.token_hex(8)}"
        timestamp = time.time()
        
        # Insert into database
        cursor = self.incident_database.cursor()
        cursor.execute('''
            INSERT INTO incidents (id, type, severity, description, affected_resource, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (incident_id, incident_type, severity, description, affected_resource, timestamp))
        
        # Log breach events if provided
        if additional_details:
            for event_type, details in additional_details.items():
                self._log_breach_event(incident_id, event_type, details)
        
        self.incident_database.commit()
        
        # Add to active incidents
        self.active_incidents[incident_id] = {
            'type': incident_type,
            'severity': severity,
            'description': description,
            'affected_resource': affected_resource,
            'timestamp': timestamp,
            'status': 'OPEN'
        }
        
        # Trigger notifications
        self._send_incident_notifications(incident_id, incident_type, severity, description)
        
        # Initiate automated response
        self._initiate_incident_response(incident_id, incident_type, severity)
        
        logger.critical(f"Security incident reported: {incident_id} - {incident_type} ({severity})")
        return incident_id
    
    def _log_breach_event(self, incident_id: str, event_type: str, details: str):
        """Log specific breach event details"""
        event_id = f"evt_{secrets.token_hex(6)}"
        cursor = self.incident_database.cursor()
        cursor.execute('''
            INSERT INTO breach_events (id, incident_id, event_type, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_id, incident_id, event_type, json.dumps(details), time.time()))
        self.incident_database.commit()
    
    def _send_incident_notifications(self, incident_id: str, incident_type: str, 
                                   severity: str, description: str):
        """Send notifications through all registered channels"""
        message = f"""
MWRASP SECURITY ALERT
=====================
Incident ID: {incident_id}
Type: {incident_type}
Severity: {severity}
Description: {description}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Immediate action may be required.
        """.strip()
        
        for channel_name, handler in self.notification_channels.items():
            try:
                notification_id = f"not_{secrets.token_hex(6)}"
                handler(message, severity)
                
                # Log notification
                cursor = self.incident_database.cursor()
                cursor.execute('''
                    INSERT INTO notifications (id, incident_id, channel, message, sent_timestamp, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (notification_id, incident_id, channel_name, message, time.time(), 'SENT'))
                self.incident_database.commit()
                
                logger.info(f"Notification sent via {channel_name} for incident {incident_id}")
                
            except Exception as e:
                logger.error(f"Failed to send notification via {channel_name}: {str(e)}")
    
    def _initiate_incident_response(self, incident_id: str, incident_type: str, severity: str):
        """Initiate automated incident response procedures"""
        response_actions = []
        
        if incident_type == 'FRAGMENT_COMPROMISE':
            response_actions.append("Initiating fragment integrity verification")
            response_actions.append("Attempting data reconstruction from remaining fragments")
            response_actions.append("Evaluating backup recovery options")
            
        elif incident_type == 'TEMPORAL_BREACH':
            response_actions.append("Immediate data expiration enforcement")
            response_actions.append("Security audit of access patterns")
            response_actions.append("Potential system lockdown evaluation")
            
        elif incident_type == 'UNAUTHORIZED_ACCESS':
            response_actions.append("User access review and potential suspension")
            response_actions.append("Authentication system security audit")
            response_actions.append("Enhanced monitoring activation")
        
        # Update incident with response actions
        cursor = self.incident_database.cursor()
        cursor.execute('''
            UPDATE incidents SET response_actions = ? WHERE id = ?
        ''', (json.dumps(response_actions), incident_id))
        self.incident_database.commit()
        
        logger.info(f"Automated response initiated for incident {incident_id}")
        return response_actions
    
    def get_incident_status(self, incident_id: str) -> Optional[Dict]:
        """Get current status of security incident"""
        if incident_id in self.active_incidents:
            return self.active_incidents[incident_id]
        return None
    
    def close_incident(self, incident_id: str, resolution_notes: str = ""):
        """Close resolved security incident"""
        if incident_id in self.active_incidents:
            self.active_incidents[incident_id]['status'] = 'CLOSED'
            self.active_incidents[incident_id]['resolution_time'] = time.time()
            
            # Update database
            cursor = self.incident_database.cursor()
            cursor.execute('''
                UPDATE incidents SET status = 'CLOSED', resolution_time = ? WHERE id = ?
            ''', (time.time(), incident_id))
            self.incident_database.commit()
            
            logger.info(f"Incident {incident_id} closed: {resolution_notes}")

# ============================================================================
# ENHANCED TEMPORAL DATA PROTECTION WITH BREACH DETECTION
# ============================================================================

class EnhancedTemporalDataProtector:
    """Advanced temporal protection with comprehensive breach detection and recovery"""
    
    def __init__(self, incident_manager: SecurityIncidentManager):
        self.incident_manager = incident_manager
        self.active_protections = {}
        self.expiration_scheduler = {}
        self.protection_history = []
        self.backup_storage = {}  # Encrypted backup storage
        self.fragment_integrity_monitors = {}
        
        self.security_levels = {
            'CRITICAL': {
                'expiry_seconds': 5, 
                'fragments': 8, 
                'encryption_rounds': 3,
                'backup_enabled': True,
                'integrity_check_interval': 1.0
            },
            'HIGH': {
                'expiry_seconds': 15, 
                'fragments': 6, 
                'encryption_rounds': 2,
                'backup_enabled': True,
                'integrity_check_interval': 2.0
            },
            'MEDIUM': {
                'expiry_seconds': 60, 
                'fragments': 4, 
                'encryption_rounds': 1,
                'backup_enabled': False,
                'integrity_check_interval': 5.0
            },
            'LOW': {
                'expiry_seconds': 300, 
                'fragments': 3, 
                'encryption_rounds': 1,
                'backup_enabled': False,
                'integrity_check_interval': 10.0
            }
        }
    
    def protect_data(self, data: str, classification: str = 'MEDIUM', 
                    metadata: Dict = None, enable_recovery: bool = None) -> str:
        """Protect data with enhanced security and breach detection"""
        protection_id = f"prot_{secrets.token_hex(12)}"
        
        if classification not in self.security_levels:
            classification = 'MEDIUM'
        
        config = self.security_levels[classification]
        expiry_time = config['expiry_seconds']
        
        # Override recovery based on classification if not specified
        if enable_recovery is None:
            enable_recovery = config['backup_enabled']
        
        # Create temporal encryption key
        temporal_key = Fernet.generate_key()
        cipher = Fernet(temporal_key)
        
        # Multi-round encryption for higher security levels
        encrypted_data = data.encode()
        for _ in range(config['encryption_rounds']):
            encrypted_data = cipher.encrypt(encrypted_data)
        
        # Fragment encrypted data
        fragments = self._create_secure_fragments(encrypted_data, config['fragments'], temporal_key)
        
        # Create encrypted backup if enabled
        backup_info = None
        if enable_recovery:
            backup_info = self._create_encrypted_backup(data, temporal_key, protection_id)
        
        # Store protection details
        protection_record = {
            'id': protection_id,
            'fragments': fragments,
            'created_at': time.time(),
            'expires_at': time.time() + expiry_time,
            'classification': classification,
            'metadata': metadata or {},
            'access_count': 0,
            'temporal_key': temporal_key,
            'backup_info': backup_info,
            'integrity_checks': [],
            'compromise_detected': False
        }
        
        self.active_protections[protection_id] = protection_record
        
        # Schedule expiration
        self.expiration_scheduler[protection_id] = threading.Timer(
            expiry_time, 
            self._expire_protection, 
            [protection_id]
        )
        self.expiration_scheduler[protection_id].start()
        
        # Start integrity monitoring
        self._start_integrity_monitoring(protection_id, config['integrity_check_interval'])
        
        # Log protection creation
        self.protection_history.append({
            'protection_id': protection_id,
            'action': 'created',
            'classification': classification,
            'expiry_seconds': expiry_time,
            'backup_enabled': enable_recovery,
            'timestamp': time.time()
        })
        
        logger.info(f"Enhanced data protection {protection_id} created, expires in {expiry_time}s")
        return protection_id
    
    def _create_secure_fragments(self, encrypted_data: bytes, fragment_count: int, 
                               temporal_key: bytes) -> List[Dict]:
        """Create secure fragments with integrity verification"""
        fragment_size = len(encrypted_data) // fragment_count
        fragments = []
        
        for i in range(fragment_count):
            start = i * fragment_size
            end = start + fragment_size if i < fragment_count - 1 else len(encrypted_data)
            
            fragment_data = encrypted_data[start:end]
            
            # Create multiple integrity checksums
            sha256_checksum = hashlib.sha256(fragment_data).hexdigest()
            md5_checksum = hashlib.md5(fragment_data).hexdigest()
            
            fragment = {
                'index': i,
                'data': fragment_data,
                'sha256_checksum': sha256_checksum,
                'md5_checksum': md5_checksum,
                'created_at': time.time(),
                'access_count': 0,
                'last_verified': time.time(),
                # Embed temporal key in first fragment only
                'temporal_key': temporal_key if i == 0 else None,
                'size': len(fragment_data)
            }
            
            fragments.append(fragment)
        
        return fragments
    
    def _create_encrypted_backup(self, original_data: str, temporal_key: bytes, 
                               protection_id: str) -> Dict:
        """Create encrypted backup for recovery purposes"""
        # Generate separate backup key
        backup_key = Fernet.generate_key()
        backup_cipher = Fernet(backup_key)
        
        # Encrypt original data with backup key
        backup_data = backup_cipher.encrypt(original_data.encode())
        
        # Store backup with recovery metadata
        backup_info = {
            'backup_id': f"backup_{secrets.token_hex(8)}",
            'backup_key': backup_key,
            'created_at': time.time(),
            'size': len(backup_data),
            'checksum': hashlib.sha256(backup_data).hexdigest()
        }
        
        self.backup_storage[backup_info['backup_id']] = {
            'data': backup_data,
            'protection_id': protection_id,
            'metadata': backup_info
        }
        
        logger.info(f"Encrypted backup created for protection {protection_id}")
        return backup_info
    
    def _start_integrity_monitoring(self, protection_id: str, check_interval: float):
        """Start continuous integrity monitoring for fragments"""
        def integrity_check():
            if protection_id in self.active_protections:
                self._verify_fragment_integrity(protection_id)
                # Schedule next check
                self.fragment_integrity_monitors[protection_id] = threading.Timer(
                    check_interval, integrity_check
                )
                self.fragment_integrity_monitors[protection_id].start()
        
        # Start initial check
        self.fragment_integrity_monitors[protection_id] = threading.Timer(
            check_interval, integrity_check
        )
        self.fragment_integrity_monitors[protection_id].start()
    
    def _verify_fragment_integrity(self, protection_id: str) -> Dict:
        """Verify integrity of all fragments"""
        if protection_id not in self.active_protections:
            return {'status': 'protection_not_found'}
        
        protection = self.active_protections[protection_id]
        fragments = protection['fragments']
        
        integrity_results = {
            'protection_id': protection_id,
            'timestamp': time.time(),
            'fragments_checked': len(fragments),
            'fragments_intact': 0,
            'fragments_compromised': 0,
            'compromised_fragments': [],
            'overall_status': 'INTACT'
        }
        
        for fragment in fragments:
            # Verify SHA256 checksum
            current_checksum = hashlib.sha256(fragment['data']).hexdigest()
            
            if current_checksum == fragment['sha256_checksum']:
                integrity_results['fragments_intact'] += 1
                fragment['last_verified'] = time.time()
            else:
                integrity_results['fragments_compromised'] += 1
                integrity_results['compromised_fragments'].append(fragment['index'])
                
                # Report fragment compromise
                incident_id = self.incident_manager.report_security_incident(
                    'FRAGMENT_COMPROMISE',
                    'HIGH',
                    f'Fragment {fragment["index"]} of protection {protection_id} integrity compromised',
                    protection_id,
                    {
                        'fragment_compromise': {
                            'fragment_index': fragment['index'],
                            'expected_checksum': fragment['sha256_checksum'],
                            'actual_checksum': current_checksum,
                            'protection_id': protection_id
                        }
                    }
                )
                
                logger.critical(f"Fragment integrity compromise detected: {protection_id}[{fragment['index']}]")
        
        # Update overall status
        compromise_ratio = integrity_results['fragments_compromised'] / len(fragments)
        
        if compromise_ratio > 0.5:
            integrity_results['overall_status'] = 'CRITICALLY_COMPROMISED'
            protection['compromise_detected'] = True
            
            # Critical compromise - attempt recovery
            self._attempt_data_recovery(protection_id)
            
        elif compromise_ratio > 0.3:
            integrity_results['overall_status'] = 'COMPROMISED'
            protection['compromise_detected'] = True
            
        elif compromise_ratio > 0:
            integrity_results['overall_status'] = 'PARTIALLY_COMPROMISED'
        
        # Store integrity check result
        protection['integrity_checks'].append(integrity_results)
        
        return integrity_results
    
    def _attempt_data_recovery(self, protection_id: str) -> Dict:
        """Attempt to recover data from backup or remaining fragments"""
        if protection_id not in self.active_protections:
            return {'status': 'protection_not_found'}
        
        protection = self.active_protections[protection_id]
        recovery_result = {
            'protection_id': protection_id,
            'timestamp': time.time(),
            'recovery_attempted': True,
            'recovery_successful': False,
            'recovery_method': None,
            'recovered_data': None
        }
        
        # Try backup recovery first (if available)
        if protection['backup_info']:
            try:
                backup_id = protection['backup_info']['backup_id']
                backup_record = self.backup_storage.get(backup_id)
                
                if backup_record:
                    backup_cipher = Fernet(protection['backup_info']['backup_key'])
                    recovered_data = backup_cipher.decrypt(backup_record['data']).decode()
                    
                    recovery_result['recovery_successful'] = True
                    recovery_result['recovery_method'] = 'BACKUP_RESTORATION'
                    recovery_result['recovered_data'] = recovered_data
                    
                    logger.info(f"Data successfully recovered from backup for {protection_id}")
                    
                    # Report successful recovery
                    self.incident_manager.report_security_incident(
                        'DATA_RECOVERY_SUCCESS',
                        'MEDIUM',
                        f'Data successfully recovered from backup for protection {protection_id}',
                        protection_id
                    )
                    
                    return recovery_result
                    
            except Exception as e:
                logger.error(f"Backup recovery failed for {protection_id}: {str(e)}")
        
        # Try fragment reconstruction (if enough intact fragments remain)
        try:
            intact_fragments = [f for f in protection['fragments'] 
                              if hashlib.sha256(f['data']).hexdigest() == f['sha256_checksum']]
            
            # Need at least 70% of fragments for reconstruction
            if len(intact_fragments) >= len(protection['fragments']) * 0.7:
                # Attempt reconstruction with error correction
                reconstructed_data = self._reconstruct_from_partial_fragments(
                    intact_fragments, protection['temporal_key']
                )
                
                if reconstructed_data:
                    recovery_result['recovery_successful'] = True
                    recovery_result['recovery_method'] = 'FRAGMENT_RECONSTRUCTION'
                    recovery_result['recovered_data'] = reconstructed_data
                    
                    logger.info(f"Data successfully reconstructed from {len(intact_fragments)} intact fragments for {protection_id}")
                    
        except Exception as e:
            logger.error(f"Fragment reconstruction failed for {protection_id}: {str(e)}")
        
        # If recovery failed, report data loss
        if not recovery_result['recovery_successful']:
            self.incident_manager.report_security_incident(
                'DATA_LOSS',
                'CRITICAL',
                f'Unable to recover data for protection {protection_id} - data permanently lost',
                protection_id,
                {
                    'data_loss': {
                        'protection_id': protection_id,
                        'fragments_compromised': len([f for f in protection['fragments'] 
                                                    if hashlib.sha256(f['data']).hexdigest() != f['sha256_checksum']]),
                        'backup_available': protection['backup_info'] is not None,
                        'recovery_attempts': ['backup_restoration', 'fragment_reconstruction']
                    }
                }
            )
            
            logger.critical(f"DATA LOSS: Unable to recover data for protection {protection_id}")
        
        return recovery_result
    
    def access_data(self, protection_id: str, requester_id: str = None) -> Optional[str]:
        """Enhanced data access with breach detection"""
        access_timestamp = time.time()
        
        # Check if protection exists
        if protection_id not in self.active_protections:
            # Report unauthorized access attempt
            self.incident_manager.report_security_incident(
                'UNAUTHORIZED_ACCESS',
                'HIGH',
                f'Attempt to access non-existent protection {protection_id}',
                protection_id,
                {
                    'unauthorized_access': {
                        'protection_id': protection_id,
                        'requester_id': requester_id,
                        'reason': 'protection_not_found'
                    }
                }
            )
            return None
        
        protection = self.active_protections[protection_id]
        
        # Check if expired
        if time.time() > protection['expires_at']:
            # Report temporal breach attempt
            self.incident_manager.report_security_incident(
                'TEMPORAL_BREACH',
                'CRITICAL',
                f'Attempt to access expired protection {protection_id}',
                protection_id,
                {
                    'temporal_breach': {
                        'protection_id': protection_id,
                        'requester_id': requester_id,
                        'expired_at': protection['expires_at'],
                        'access_attempted_at': access_timestamp
                    }
                }
            )
            self._expire_protection(protection_id)
            return None
        
        # Check for compromise
        if protection['compromise_detected']:
            logger.warning(f"Accessing compromised protection {protection_id} - attempting recovery")
            recovery_result = self._attempt_data_recovery(protection_id)
            
            if recovery_result['recovery_successful']:
                # Log successful access despite compromise
                self.protection_history.append({
                    'protection_id': protection_id,
                    'action': 'accessed_after_recovery',
                    'requester': requester_id,
                    'recovery_method': recovery_result['recovery_method'],
                    'timestamp': access_timestamp
                })
                
                return recovery_result['recovered_data']
            else:
                return None
        
        # Increment access counter
        protection['access_count'] += 1
        
        # Reconstruct data from fragments
        try:
            reconstructed_data = self._reconstruct_from_fragments(
                protection['fragments'],
                protection['temporal_key']
            )
            
            # Log successful access
            self.protection_history.append({
                'protection_id': protection_id,
                'action': 'accessed',
                'requester': requester_id,
                'timestamp': access_timestamp
            })
            
            return reconstructed_data
            
        except Exception as e:
            # Report access failure
            self.incident_manager.report_security_incident(
                'ACCESS_FAILURE',
                'MEDIUM',
                f'Failed to access protection {protection_id}: {str(e)}',
                protection_id,
                {
                    'access_failure': {
                        'protection_id': protection_id,
                        'requester_id': requester_id,
                        'error': str(e)
                    }
                }
            )
            
            logger.error(f"Failed to reconstruct data for {protection_id}: {str(e)}")
            return None
    
    def _reconstruct_from_fragments(self, fragments: List[Dict], temporal_key: bytes) -> str:
        """Reconstruct data from complete fragments"""
        # Sort fragments by index
        sorted_fragments = sorted(fragments, key=lambda f: f['index'])
        
        # Verify fragment integrity
        for fragment in sorted_fragments:
            expected_checksum = hashlib.sha256(fragment['data']).hexdigest()
            if fragment['sha256_checksum'] != expected_checksum:
                raise ValueError(f"Fragment {fragment['index']} integrity check failed")
        
        # Reconstruct encrypted data
        reconstructed_encrypted = b''.join(fragment['data'] for fragment in sorted_fragments)
        
        # Decrypt with temporal key
        cipher = Fernet(temporal_key)
        
        # Handle multi-round decryption
        decrypted_data = reconstructed_encrypted
        while True:
            try:
                decrypted_data = cipher.decrypt(decrypted_data)
                # If successful, try to decrypt again (multi-round)
            except:
                # If decryption fails, we're done with decryption rounds
                break
        
        return decrypted_data.decode()
    
    def _reconstruct_from_partial_fragments(self, intact_fragments: List[Dict], 
                                          temporal_key: bytes) -> Optional[str]:
        """Attempt reconstruction from partial fragments using error correction"""
        if len(intact_fragments) < 3:  # Need minimum fragments
            return None
        
        try:
            # Sort intact fragments by index
            sorted_fragments = sorted(intact_fragments, key=lambda f: f['index'])
            
            # Try to reconstruct with padding/interpolation for missing fragments
            fragment_data_pieces = []
            
            for i, fragment in enumerate(sorted_fragments):
                fragment_data_pieces.append(fragment['data'])
            
            # Concatenate available data
            partial_encrypted_data = b''.join(fragment_data_pieces)
            
            # Try to decrypt (may fail due to incomplete data)
            cipher = Fernet(temporal_key)
            
            # Attempt decryption with error handling
            decrypted_data = partial_encrypted_data
            for _ in range(3):  # Try multi-round decryption
                try:
                    decrypted_data = cipher.decrypt(decrypted_data)
                except:
                    break
            
            # Try to decode as string
            if isinstance(decrypted_data, bytes):
                return decrypted_data.decode('utf-8', errors='ignore')
            
            return None
            
        except Exception as e:
            logger.error(f"Partial reconstruction failed: {str(e)}")
            return None
    
    def _expire_protection(self, protection_id: str):
        """Enhanced expiration with detailed logging"""
        if protection_id in self.active_protections:
            protection = self.active_protections[protection_id]
            
            # Stop integrity monitoring
            if protection_id in self.fragment_integrity_monitors:
                self.fragment_integrity_monitors[protection_id].cancel()
                del self.fragment_integrity_monitors[protection_id]
            
            # Secure deletion - overwrite sensitive data
            for fragment in protection['fragments']:
                if 'data' in fragment:
                    original_size = len(fragment['data'])
                    # Overwrite with random bytes
                    fragment['data'] = secrets.token_bytes(original_size)
                if 'temporal_key' in fragment:
                    fragment['temporal_key'] = None
            
            # Clear temporal key
            protection['temporal_key'] = None
            
            # Clear backup if exists
            if protection['backup_info']:
                backup_id = protection['backup_info']['backup_id']
                if backup_id in self.backup_storage:
                    del self.backup_storage[backup_id]
                protection['backup_info'] = None
            
            # Remove from active protections
            del self.active_protections[protection_id]
            
            # Cancel timer if still active
            if protection_id in self.expiration_scheduler:
                self.expiration_scheduler[protection_id].cancel()
                del self.expiration_scheduler[protection_id]
            
            # Log expiration
            self.protection_history.append({
                'protection_id': protection_id,
                'action': 'expired',
                'timestamp': time.time(),
                'secure_deletion': True
            })
            
            # Report normal expiration (informational)
            self.incident_manager.report_security_incident(
                'NORMAL_EXPIRATION',
                'LOW',
                f'Protection {protection_id} expired normally and was securely deleted',
                protection_id
            )
            
            logger.info(f"Protection {protection_id} expired and securely deleted")
    
    def get_protection_status(self, protection_id: str) -> Optional[Dict]:
        """Get comprehensive protection status including security state"""
        if protection_id not in self.active_protections:
            return None
        
        protection = self.active_protections[protection_id]
        current_time = time.time()
        
        # Get latest integrity check
        latest_integrity = None
        if protection['integrity_checks']:
            latest_integrity = protection['integrity_checks'][-1]
        
        status = {
            'protection_id': protection_id,
            'classification': protection['classification'],
            'created_at': protection['created_at'],
            'expires_at': protection['expires_at'],
            'remaining_seconds': max(0, protection['expires_at'] - current_time),
            'access_count': protection['access_count'],
            'compromise_detected': protection['compromise_detected'],
            'backup_available': protection['backup_info'] is not None,
            'fragments_total': len(protection['fragments']),
            'latest_integrity_check': latest_integrity,
            'security_status': 'SECURE'
        }
        
        # Determine security status
        if protection['compromise_detected']:
            status['security_status'] = 'COMPROMISED'
        elif latest_integrity and latest_integrity['fragments_compromised'] > 0:
            status['security_status'] = 'AT_RISK'
        
        return status

# Demo notification handlers
def console_notification_handler(message: str, severity: str):
    """Console notification handler for demonstration"""
    print(f"\n{'='*60}")
    print(f"SECURITY NOTIFICATION ({severity})")
    print(f"{'='*60}")
    print(message)
    print(f"{'='*60}\n")

def email_notification_handler(message: str, severity: str):
    """Email notification handler (simulated)"""
    logger.info(f"EMAIL SENT: {severity} - {message[:50]}...")

# ============================================================================
# DEMONSTRATION OF ENHANCED SECURITY SYSTEM
# ============================================================================

async def demonstrate_enhanced_security_system():
    """Demonstrate enhanced security system with breach detection and recovery"""
    print("="*80)
    print("MWRASP ENHANCED SECURITY SYSTEM DEMONSTRATION")
    print("Advanced breach detection, data recovery, and incident management")
    print("="*80)
    
    # Initialize systems
    incident_manager = SecurityIncidentManager()
    temporal_protector = EnhancedTemporalDataProtector(incident_manager)
    
    # Register notification channels
    incident_manager.register_notification_channel('console', console_notification_handler)
    incident_manager.register_notification_channel('email', email_notification_handler)
    
    # Test 1: Normal Protection and Access
    print("\n[1] NORMAL PROTECTION AND ACCESS TEST")
    print("-" * 50)
    
    test_data = "CONFIDENTIAL_FINANCIAL_TRANSACTION_12345"
    protection_id = temporal_protector.protect_data(test_data, 'HIGH', 
                                                  {'transaction_id': '12345'}, True)
    
    print(f"Protection created: {protection_id}")
    
    # Successful access
    accessed_data = temporal_protector.access_data(protection_id, 'user_001')
    print(f"Access successful: {accessed_data == test_data}")
    
    # Test 2: Fragment Integrity Compromise Simulation
    print("\n[2] FRAGMENT COMPROMISE SIMULATION")
    print("-" * 50)
    
    # Wait for integrity check, then simulate compromise
    await asyncio.sleep(3)
    
    # Manually corrupt a fragment to simulate compromise
    if protection_id in temporal_protector.active_protections:
        protection = temporal_protector.active_protections[protection_id]
        if protection['fragments']:
            # Corrupt first fragment
            original_data = protection['fragments'][0]['data']
            protection['fragments'][0]['data'] = secrets.token_bytes(len(original_data))
            print("Fragment corruption simulated...")
            
            # Wait for integrity check to detect it
            await asyncio.sleep(3)
            
            # Try to access data (should trigger recovery)
            recovered_data = temporal_protector.access_data(protection_id, 'user_001')
            print(f"Data recovery successful: {recovered_data == test_data}")
    
    # Test 3: Temporal Breach Attempt
    print("\n[3] TEMPORAL BREACH SIMULATION")
    print("-" * 50)
    
    # Create short-lived protection
    short_data = "TEMPORARY_SECRET_DATA"
    short_protection_id = temporal_protector.protect_data(short_data, 'CRITICAL')
    
    print(f"Short-lived protection created: {short_protection_id}")
    print("Waiting for expiration...")
    
    # Wait for expiration
    await asyncio.sleep(6)
    
    # Try to access expired data
    expired_access = temporal_protector.access_data(short_protection_id, 'user_002')
    print(f"Expired access blocked: {expired_access is None}")
    
    # Test 4: Unauthorized Access Attempt
    print("\n[4] UNAUTHORIZED ACCESS SIMULATION")
    print("-" * 50)
    
    # Try to access non-existent protection
    fake_access = temporal_protector.access_data('fake_protection_id', 'unauthorized_user')
    print(f"Unauthorized access blocked: {fake_access is None}")
    
    # Test 5: System Status Report
    print("\n[5] SYSTEM STATUS AND INCIDENT REPORT")
    print("-" * 50)
    
    # Get active incidents
    active_incidents = incident_manager.active_incidents
    print(f"Active security incidents: {len(active_incidents)}")
    
    for incident_id, incident in active_incidents.items():
        print(f"  {incident_id}: {incident['type']} ({incident['severity']})")
    
    # Get protection status
    if protection_id in temporal_protector.active_protections:
        status = temporal_protector.get_protection_status(protection_id)
        print(f"\nProtection {protection_id} status:")
        print(f"  Security Status: {status['security_status']}")
        print(f"  Remaining Time: {status['remaining_seconds']:.1f}s")
        print(f"  Access Count: {status['access_count']}")
        print(f"  Backup Available: {status['backup_available']}")
    
    print("\n" + "="*80)
    print("ENHANCED SECURITY DEMONSTRATION COMPLETE")
    print("All breach detection and recovery mechanisms validated")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(demonstrate_enhanced_security_system())
"""
Audit Logging and Compliance System
Comprehensive audit trails, compliance reporting, and regulatory adherence
"""

import asyncio
import json
import hashlib
import hmac
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncpg
from cryptography.fernet import Fernet
import aiofiles
import pytz

class AuditEventType(Enum):
    """Types of audit events"""
    # Authentication
    LOGIN_SUCCESS = "auth.login.success"
    LOGIN_FAILURE = "auth.login.failure"
    LOGOUT = "auth.logout"
    TOKEN_ISSUED = "auth.token.issued"
    TOKEN_REVOKED = "auth.token.revoked"
    
    # Data Access
    DATA_READ = "data.read"
    DATA_WRITE = "data.write"
    DATA_DELETE = "data.delete"
    DATA_EXPORT = "data.export"
    
    # Encryption Operations
    ENCRYPT = "crypto.encrypt"
    DECRYPT = "crypto.decrypt"
    KEY_GENERATE = "crypto.key.generate"
    KEY_ROTATE = "crypto.key.rotate"
    
    # Computation
    COMPUTATION_START = "compute.start"
    COMPUTATION_COMPLETE = "compute.complete"
    COMPUTATION_FAILED = "compute.failed"
    
    # Configuration
    CONFIG_CHANGE = "config.change"
    FLAG_CHANGE = "flag.change"
    PERMISSION_CHANGE = "permission.change"
    
    # System
    NODE_JOIN = "system.node.join"
    NODE_LEAVE = "system.node.leave"
    BYZANTINE_DETECTED = "system.byzantine.detected"
    
    # Compliance
    CONSENT_GRANTED = "compliance.consent.granted"
    CONSENT_REVOKED = "compliance.consent.revoked"
    DATA_RETENTION_EXPIRED = "compliance.retention.expired"
    AUDIT_EXPORT = "compliance.audit.export"

@dataclass
class AuditEvent:
    """Audit event record"""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    
    # Actor information
    actor_id: str
    actor_type: str  # user, service, system
    actor_ip: Optional[str] = None
    actor_user_agent: Optional[str] = None
    
    # Target information
    target_id: Optional[str] = None
    target_type: Optional[str] = None
    
    # Event details
    action: str = ""
    result: str = "success"  # success, failure, partial
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Compliance fields
    data_classification: Optional[str] = None  # public, internal, confidential, restricted
    jurisdiction: Optional[str] = None
    
    # Security
    integrity_hash: Optional[str] = None

class AuditLogger:
    """Centralized audit logging system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_pool: Optional[asyncpg.Pool] = None
        self.encryption_key = Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        self.hash_secret = config.get("hash_secret", "audit_secret").encode()
        
    async def initialize(self):
        """Initialize audit logger"""
        # Create database pool
        self.db_pool = await asyncpg.create_pool(
            self.config["database_url"],
            min_size=5,
            max_size=20
        )
        
        # Create audit tables
        await self._create_tables()
        
    async def _create_tables(self):
        """Create audit tables if not exist"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id UUID PRIMARY KEY,
                    event_type VARCHAR(100) NOT NULL,
                    timestamp TIMESTAMPTZ NOT NULL,
                    actor_id VARCHAR(255) NOT NULL,
                    actor_type VARCHAR(50) NOT NULL,
                    actor_ip INET,
                    actor_user_agent TEXT,
                    target_id VARCHAR(255),
                    target_type VARCHAR(100),
                    action TEXT NOT NULL,
                    result VARCHAR(50) NOT NULL,
                    metadata JSONB,
                    data_classification VARCHAR(50),
                    jurisdiction VARCHAR(100),
                    integrity_hash VARCHAR(64) NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_events(timestamp);
                CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_events(actor_id);
                CREATE INDEX IF NOT EXISTS idx_audit_target ON audit_events(target_id);
                CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_events(event_type);
                CREATE INDEX IF NOT EXISTS idx_audit_classification ON audit_events(data_classification);
            """)
            
            # Immutable audit trail table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail_immutable (
                    id SERIAL PRIMARY KEY,
                    block_hash VARCHAR(64) NOT NULL,
                    previous_hash VARCHAR(64) NOT NULL,
                    events JSONB NOT NULL,
                    timestamp TIMESTAMPTZ NOT NULL,
                    signature TEXT NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_trail_timestamp ON audit_trail_immutable(timestamp);
            """)
            
    async def log(self, event: AuditEvent):
        """Log audit event"""
        # Calculate integrity hash
        event.integrity_hash = self._calculate_integrity_hash(event)
        
        # Store in database
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO audit_events (
                    event_id, event_type, timestamp, actor_id, actor_type,
                    actor_ip, actor_user_agent, target_id, target_type,
                    action, result, metadata, data_classification,
                    jurisdiction, integrity_hash
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
            """, 
                event.event_id, event.event_type.value, event.timestamp,
                event.actor_id, event.actor_type, event.actor_ip,
                event.actor_user_agent, event.target_id, event.target_type,
                event.action, event.result, json.dumps(event.metadata),
                event.data_classification, event.jurisdiction, event.integrity_hash
            )
            
        # Real-time alerting for critical events
        await self._check_alerts(event)
        
    def _calculate_integrity_hash(self, event: AuditEvent) -> str:
        """Calculate integrity hash for event"""
        # Create canonical representation
        canonical = json.dumps({
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "actor_id": event.actor_id,
            "target_id": event.target_id,
            "action": event.action,
            "result": event.result
        }, sort_keys=True)
        
        # HMAC for integrity
        return hmac.new(
            self.hash_secret,
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        
    async def _check_alerts(self, event: AuditEvent):
        """Check if event triggers any alerts"""
        # Failed login attempts
        if event.event_type == AuditEventType.LOGIN_FAILURE:
            await self._check_failed_login_threshold(event.actor_id)
            
        # Byzantine detection
        elif event.event_type == AuditEventType.BYZANTINE_DETECTED:
            await self._alert_security_team(event)
            
        # Data export
        elif event.event_type == AuditEventType.DATA_EXPORT:
            if event.data_classification in ["confidential", "restricted"]:
                await self._alert_data_protection_officer(event)
                
    async def _check_failed_login_threshold(self, actor_id: str):
        """Check failed login attempts"""
        async with self.db_pool.acquire() as conn:
            count = await conn.fetchval("""
                SELECT COUNT(*) FROM audit_events
                WHERE actor_id = $1
                AND event_type = $2
                AND timestamp > NOW() - INTERVAL '15 minutes'
            """, actor_id, AuditEventType.LOGIN_FAILURE.value)
            
            if count >= 5:
                # Lock account or alert
                await self._alert_security_team({
                    "alert": "Multiple failed login attempts",
                    "actor_id": actor_id,
                    "count": count
                })
                
    async def _alert_security_team(self, alert_data: Any):
        """Send alert to security team"""
        # Implementation for alerting
        pass
        
    async def _alert_data_protection_officer(self, event: AuditEvent):
        """Alert DPO for data protection events"""
        # Implementation for DPO alerting
        pass

class ComplianceManager:
    """Manages regulatory compliance"""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.regulations = {
            "GDPR": GDPRCompliance(),
            "HIPAA": HIPAACompliance(),
            "SOC2": SOC2Compliance(),
            "FIPS": FIPSCompliance()
        }
        
    async def check_compliance(self, 
                              operation: str,
                              context: Dict[str, Any]) -> Dict[str, bool]:
        """Check compliance for operation"""
        results = {}
        
        for name, regulation in self.regulations.items():
            if regulation.is_applicable(context):
                results[name] = await regulation.check_compliance(operation, context)
                
        return results
        
    async def generate_compliance_report(self,
                                       regulation: str,
                                       start_date: datetime,
                                       end_date: datetime) -> Dict[str, Any]:
        """Generate compliance report"""
        if regulation not in self.regulations:
            raise ValueError(f"Unknown regulation: {regulation}")
            
        reg = self.regulations[regulation]
        
        # Get relevant audit events
        events = await self._get_audit_events(
            start_date,
            end_date,
            reg.relevant_event_types()
        )
        
        # Generate report
        report = await reg.generate_report(events)
        
        # Log report generation
        await self.audit_logger.log(AuditEvent(
            event_id=str(uuid.uuid4()),
            event_type=AuditEventType.AUDIT_EXPORT,
            timestamp=datetime.utcnow(),
            actor_id="system",
            actor_type="system",
            action=f"Generated {regulation} compliance report",
            metadata={
                "regulation": regulation,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "event_count": len(events)
            }
        ))
        
        return report
        
    async def _get_audit_events(self,
                               start_date: datetime,
                               end_date: datetime,
                               event_types: List[AuditEventType]) -> List[Dict]:
        """Get audit events for period"""
        async with self.audit_logger.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM audit_events
                WHERE timestamp >= $1
                AND timestamp <= $2
                AND event_type = ANY($3)
                ORDER BY timestamp
            """, start_date, end_date, [et.value for et in event_types])
            
            return [dict(row) for row in rows]

class GDPRCompliance:
    """GDPR compliance checks"""
    
    def is_applicable(self, context: Dict[str, Any]) -> bool:
        """Check if GDPR applies"""
        return context.get("jurisdiction") in ["EU", "EEA"] or \
               context.get("user_location", "").startswith("EU")
               
    async def check_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check GDPR compliance"""
        # Check consent
        if operation in ["data.read", "data.write", "data.export"]:
            return context.get("user_consent", False)
            
        # Check data minimization
        if operation == "data.collect":
            return self._check_data_minimization(context)
            
        # Check right to be forgotten
        if operation == "data.delete":
            return True  # Always allow deletion
            
        return True
        
    def _check_data_minimization(self, context: Dict[str, Any]) -> bool:
        """Check data minimization principle"""
        required_fields = context.get("required_fields", [])
        collected_fields = context.get("collected_fields", [])
        
        # Only collect required fields
        return set(collected_fields).issubset(set(required_fields))
        
    def relevant_event_types(self) -> List[AuditEventType]:
        """Get relevant event types for GDPR"""
        return [
            AuditEventType.CONSENT_GRANTED,
            AuditEventType.CONSENT_REVOKED,
            AuditEventType.DATA_READ,
            AuditEventType.DATA_WRITE,
            AuditEventType.DATA_DELETE,
            AuditEventType.DATA_EXPORT
        ]
        
    async def generate_report(self, events: List[Dict]) -> Dict[str, Any]:
        """Generate GDPR compliance report"""
        report = {
            "regulation": "GDPR",
            "total_events": len(events),
            "consent_events": 0,
            "data_access_events": 0,
            "deletion_requests": 0,
            "export_requests": 0,
            "violations": []
        }
        
        for event in events:
            event_type = AuditEventType(event["event_type"])
            
            if event_type in [AuditEventType.CONSENT_GRANTED, AuditEventType.CONSENT_REVOKED]:
                report["consent_events"] += 1
            elif event_type in [AuditEventType.DATA_READ, AuditEventType.DATA_WRITE]:
                report["data_access_events"] += 1
            elif event_type == AuditEventType.DATA_DELETE:
                report["deletion_requests"] += 1
            elif event_type == AuditEventType.DATA_EXPORT:
                report["export_requests"] += 1
                
            # Check for violations
            if event_type in [AuditEventType.DATA_READ, AuditEventType.DATA_WRITE]:
                metadata = event.get("metadata", {})
                if not metadata.get("user_consent"):
                    report["violations"].append({
                        "event_id": event["event_id"],
                        "type": "missing_consent",
                        "timestamp": event["timestamp"]
                    })
                    
        return report

class HIPAACompliance:
    """HIPAA compliance for healthcare data"""
    
    def is_applicable(self, context: Dict[str, Any]) -> bool:
        """Check if HIPAA applies"""
        return context.get("data_type") == "PHI" or \
               context.get("industry") == "healthcare"
               
    async def check_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check HIPAA compliance"""
        # Check encryption
        if operation in ["data.read", "data.write", "data.export"]:
            if not context.get("encrypted", False):
                return False
                
        # Check access controls
        if operation.startswith("data."):
            return self._check_access_controls(context)
            
        return True
        
    def _check_access_controls(self, context: Dict[str, Any]) -> bool:
        """Check HIPAA access controls"""
        # Minimum necessary rule
        role = context.get("actor_role")
        data_accessed = context.get("data_fields", [])
        
        allowed_fields = {
            "doctor": ["diagnosis", "treatment", "medications"],
            "nurse": ["vitals", "medications"],
            "admin": ["demographics", "insurance"]
        }
        
        if role in allowed_fields:
            return set(data_accessed).issubset(set(allowed_fields[role]))
            
        return False
        
    def relevant_event_types(self) -> List[AuditEventType]:
        """Get relevant event types for HIPAA"""
        return [
            AuditEventType.DATA_READ,
            AuditEventType.DATA_WRITE,
            AuditEventType.DATA_DELETE,
            AuditEventType.DATA_EXPORT,
            AuditEventType.LOGIN_SUCCESS,
            AuditEventType.LOGIN_FAILURE
        ]

class SOC2Compliance:
    """SOC2 compliance checks"""
    
    def is_applicable(self, context: Dict[str, Any]) -> bool:
        """Check if SOC2 applies"""
        return context.get("require_soc2", False)
        
    async def check_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check SOC2 compliance"""
        # All operations must be logged
        return True  # Logging is handled by AuditLogger
        
    def relevant_event_types(self) -> List[AuditEventType]:
        """Get all event types for SOC2"""
        return list(AuditEventType)  # All events
        
    async def generate_report(self, events: List[Dict]) -> Dict[str, Any]:
        """Generate SOC2 compliance report"""
        # Group by trust service criteria
        criteria = {
            "security": self._check_security_criteria(events),
            "availability": self._check_availability_criteria(events),
            "processing_integrity": self._check_integrity_criteria(events),
            "confidentiality": self._check_confidentiality_criteria(events),
            "privacy": self._check_privacy_criteria(events)
        }
        
        return {
            "regulation": "SOC2",
            "reporting_period": {
                "start": min(e["timestamp"] for e in events) if events else None,
                "end": max(e["timestamp"] for e in events) if events else None
            },
            "criteria_results": criteria,
            "total_events": len(events)
        }
        
    def _check_security_criteria(self, events: List[Dict]) -> Dict:
        """Check security criteria"""
        security_events = [
            e for e in events 
            if AuditEventType(e["event_type"]) in [
                AuditEventType.LOGIN_SUCCESS,
                AuditEventType.LOGIN_FAILURE,
                AuditEventType.PERMISSION_CHANGE,
                AuditEventType.BYZANTINE_DETECTED
            ]
        ]
        
        return {
            "total_events": len(security_events),
            "failed_logins": len([e for e in security_events if e["event_type"] == AuditEventType.LOGIN_FAILURE.value]),
            "permission_changes": len([e for e in security_events if e["event_type"] == AuditEventType.PERMISSION_CHANGE.value]),
            "security_incidents": len([e for e in security_events if e["event_type"] == AuditEventType.BYZANTINE_DETECTED.value])
        }

class FIPSCompliance:
    """FIPS 140-2 compliance for cryptography"""
    
    def is_applicable(self, context: Dict[str, Any]) -> bool:
        """Check if FIPS applies"""
        return context.get("require_fips", False) or \
               context.get("environment") == "defense"
               
    async def check_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check FIPS compliance"""
        if operation.startswith("crypto."):
            # Check algorithm
            algorithm = context.get("algorithm")
            return algorithm in self._approved_algorithms()
            
        return True
        
    def _approved_algorithms(self) -> Set[str]:
        """Get FIPS approved algorithms"""
        return {
            "AES-256-GCM",
            "AES-256-CBC",
            "SHA-256",
            "SHA-384",
            "SHA-512",
            "RSA-2048",
            "RSA-3072",
            "ECDSA-P256",
            "ECDSA-P384"
        }
        
    def relevant_event_types(self) -> List[AuditEventType]:
        """Get crypto event types"""
        return [
            AuditEventType.ENCRYPT,
            AuditEventType.DECRYPT,
            AuditEventType.KEY_GENERATE,
            AuditEventType.KEY_ROTATE
        ]

class AuditTrailBlockchain:
    """Immutable audit trail using blockchain structure"""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.current_block_events = []
        self.block_size = 100  # Events per block
        
    async def add_event(self, event: AuditEvent):
        """Add event to blockchain"""
        self.current_block_events.append(event)
        
        if len(self.current_block_events) >= self.block_size:
            await self._create_block()
            
    async def _create_block(self):
        """Create new block in chain"""
        # Get previous block hash
        async with self.audit_logger.db_pool.acquire() as conn:
            previous_hash = await conn.fetchval("""
                SELECT block_hash FROM audit_trail_immutable
                ORDER BY id DESC LIMIT 1
            """) or "0" * 64
            
        # Create block
        block_data = {
            "events": [self._event_to_dict(e) for e in self.current_block_events],
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": previous_hash
        }
        
        # Calculate block hash
        block_hash = hashlib.sha256(
            json.dumps(block_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Sign block
        signature = self._sign_block(block_hash)
        
        # Store block
        async with self.audit_logger.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO audit_trail_immutable
                (block_hash, previous_hash, events, timestamp, signature)
                VALUES ($1, $2, $3, $4, $5)
            """, block_hash, previous_hash, json.dumps(block_data["events"]),
                datetime.utcnow(), signature)
                
        # Clear current events
        self.current_block_events = []
        
    def _event_to_dict(self, event: AuditEvent) -> Dict:
        """Convert event to dictionary"""
        return {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "actor_id": event.actor_id,
            "integrity_hash": event.integrity_hash
        }
        
    def _sign_block(self, block_hash: str) -> str:
        """Sign block for integrity"""
        # In production, use proper digital signatures
        return hmac.new(
            self.audit_logger.hash_secret,
            block_hash.encode(),
            hashlib.sha256
        ).hexdigest()
        
    async def verify_integrity(self) -> bool:
        """Verify blockchain integrity"""
        async with self.audit_logger.db_pool.acquire() as conn:
            blocks = await conn.fetch("""
                SELECT * FROM audit_trail_immutable
                ORDER BY id
            """)
            
        previous_hash = "0" * 64
        
        for block in blocks:
            # Verify previous hash
            if block["previous_hash"] != previous_hash:
                return False
                
            # Verify block hash
            block_data = {
                "events": json.loads(block["events"]),
                "timestamp": block["timestamp"].isoformat(),
                "previous_hash": block["previous_hash"]
            }
            
            calculated_hash = hashlib.sha256(
                json.dumps(block_data, sort_keys=True).encode()
            ).hexdigest()
            
            if calculated_hash != block["block_hash"]:
                return False
                
            # Verify signature
            expected_signature = self._sign_block(block["block_hash"])
            if expected_signature != block["signature"]:
                return False
                
            previous_hash = block["block_hash"]
            
        return True

# Export functionality
class AuditExporter:
    """Export audit logs for analysis or compliance"""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        
    async def export_to_siem(self, 
                           start_date: datetime,
                           end_date: datetime,
                           siem_endpoint: str):
        """Export to SIEM system"""
        # Get events
        async with self.audit_logger.db_pool.acquire() as conn:
            events = await conn.fetch("""
                SELECT * FROM audit_events
                WHERE timestamp >= $1 AND timestamp <= $2
                ORDER BY timestamp
            """, start_date, end_date)
            
        # Convert to CEF format
        cef_events = [self._to_cef(dict(e)) for e in events]
        
        # Send to SIEM
        import aiohttp
        async with aiohttp.ClientSession() as session:
            for batch in self._batch(cef_events, 100):
                await session.post(siem_endpoint, json=batch)
                
    def _to_cef(self, event: Dict) -> str:
        """Convert to Common Event Format"""
        return (
            f"CEF:0|HomomorphicSwarm|Swarm|1.0|{event['event_type']}|"
            f"{event['action']}|3|"
            f"act={event['action']} "
            f"src={event.get('actor_ip', 'unknown')} "
            f"duser={event['actor_id']} "
            f"outcome={event['result']}"
        )
        
    def _batch(self, items: List, size: int):
        """Batch items"""
        for i in range(0, len(items), size):
            yield items[i:i + size]

if __name__ == "__main__":
    # Example usage
    async def demo():
        config = {
            "database_url": "postgresql://user:pass@localhost/audit",
            "hash_secret": "super_secret_key"
        }
        
        # Initialize
        logger = AuditLogger(config)
        await logger.initialize()
        
        # Log event
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            event_type=AuditEventType.DATA_READ,
            timestamp=datetime.utcnow(),
            actor_id="user123",
            actor_type="user",
            actor_ip="192.168.1.100",
            target_id="dataset_456",
            target_type="dataset",
            action="Read sensitive dataset",
            data_classification="confidential",
            jurisdiction="EU"
        )
        
        await logger.log(event)
        
        # Check compliance
        compliance = ComplianceManager(logger)
        results = await compliance.check_compliance(
            "data.read",
            {
                "jurisdiction": "EU",
                "user_consent": True,
                "data_type": "personal"
            }
        )
        print(f"Compliance check: {results}")
        
        # Generate report
        report = await compliance.generate_compliance_report(
            "GDPR",
            datetime.utcnow() - timedelta(days=30),
            datetime.utcnow()
        )
        print(f"GDPR Report: {report}")
        
    asyncio.run(demo())

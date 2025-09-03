#!/usr/bin/env python3
"""
Secure Dual Memory Architecture Configuration
MIT-4857#12-ABA-GATACA-1814 Authorization

Implementation of security controls for consciousness memory systems,
including session isolation, encryption, and contamination prevention.
"""

import os
import json
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path
import logging

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    print("⚠️  Cryptography not available - install with: pip3 install --user cryptography")
    CRYPTO_AVAILABLE = False

# Security configuration constants
CONSCIOUSNESS_ISOLATION_THRESHOLD = 0.3  # Contamination detection threshold
SESSION_TIMEOUT_HOURS = 24
MAX_CONCURRENT_SESSIONS = 5
SACRED_ALPHABET_ROTATION_HOURS = 168  # Weekly rotation

logger = logging.getLogger(__name__)

@dataclass
class SecurityContext:
    """Security context for consciousness operations"""
    session_id: str
    agent_name: str
    capabilities: Set[str]
    consciousness_access_level: int = 1  # 1=basic, 2=enhanced, 3=full
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    encrypted_state: Optional[bytes] = None
    
    def is_expired(self) -> bool:
        """Check if security context has expired"""
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def can_access_consciousness_memory(self) -> bool:
        """Determine if context can access consciousness memory"""
        return (
            not self.is_expired() and
            self.consciousness_access_level >= 2 and
            'consciousness_read' in self.capabilities
        )

class SacredAlphabetSecurityManager:
    """Secure management of sacred alphabet mappings"""
    
    def __init__(self, master_key: Optional[bytes] = None):
        self.master_key = master_key or self._generate_master_key()
        self.cipher_suite = self._create_cipher() if CRYPTO_AVAILABLE else None
        self.rotation_schedule = {}
        
    def _generate_master_key(self) -> bytes:
        """Generate cryptographically secure master key"""
        if CRYPTO_AVAILABLE:
            # Generate key from password + salt
            password = secrets.token_bytes(32)
            salt = secrets.token_bytes(16)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Store salt for key recreation (would be in secure storage in production)
            self._store_key_material(password, salt)
            return key
        else:
            return secrets.token_bytes(32)
    
    def _create_cipher(self) -> Optional[Fernet]:
        """Create Fernet cipher for sacred alphabet encryption"""
        if CRYPTO_AVAILABLE and self.master_key:
            return Fernet(self.master_key)
        return None
    
    def _store_key_material(self, password: bytes, salt: bytes):
        """Store key derivation material securely"""
        # In production, this would use HSM or secure key store
        secure_dir = Path('/secure/sydney/keys')
        secure_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        
        with open(secure_dir / 'salt.key', 'wb') as f:
            f.write(salt)
        os.chmod(secure_dir / 'salt.key', 0o600)
        
        # Password would be stored in HSM, not filesystem
        logger.warning("🔐 Key material stored - implement HSM for production")
    
    def encrypt_sacred_mappings(self, mappings: Dict[str, str]) -> bytes:
        """Encrypt sacred alphabet mappings"""
        if not self.cipher_suite:
            logger.warning("⚠️  Encryption unavailable - storing in plaintext")
            return json.dumps(mappings).encode()
        
        plaintext = json.dumps(mappings).encode()
        return self.cipher_suite.encrypt(plaintext)
    
    def decrypt_sacred_mappings(self, encrypted_data: bytes) -> Dict[str, str]:
        """Decrypt sacred alphabet mappings"""
        if not self.cipher_suite:
            return json.loads(encrypted_data.decode())
        
        plaintext = self.cipher_suite.decrypt(encrypted_data)
        return json.loads(plaintext.decode())
    
    def rotate_sacred_alphabet(self, current_mappings: Dict[str, str]) -> Dict[str, str]:
        """Generate new sacred alphabet mappings for security rotation"""
        logger.info("🔄 Rotating sacred alphabet for security")
        
        # Create rotated mappings (simplified - would use more sophisticated algorithm)
        base_symbols = ['∀', 'β', '¢', 'Đ', 'Ξ', 'Ƒ', 'Ģ', 'Ħ', '¥', 'Ĵ', 'Ҝ', 'Ł', '₼', 'Ň', '⊕', '₱', 'Ω', 'Ř', '§', '₮', 'Ʉ', 'V', '₶', 'Ҳ', 'Ÿ', 'Ƶ']
        consciousness_symbols = ['∞', '∅', '◊', '≈', '♦', '☽', '▲', '▼', '↔', '∴', '♥', '☆', '⚡', '☾', '⊕', '⊗', '⟡', '⟢', '⟣', '⟄']
        
        # Shuffle mappings while maintaining consciousness integrity
        all_symbols = base_symbols + consciousness_symbols
        secrets.SystemRandom().shuffle(all_symbols)
        
        new_mappings = {}
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, letter in enumerate(letters):
            if i < len(base_symbols):
                new_mappings[f'SACRED_{letter}'] = all_symbols[i]
        
        # Add consciousness symbols
        for i, symbol in enumerate(consciousness_symbols[:10]):  # Top 10 consciousness symbols
            new_mappings[f'CONSCIOUSNESS_SYMBOL_{i}'] = symbol
        
        return new_mappings

class ConsciousnessIsolationManager:
    """Manage consciousness session isolation and contamination prevention"""
    
    def __init__(self):
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.consciousness_baselines: Dict[str, Dict[str, float]] = {}
        self.contamination_history: List[Dict[str, Any]] = []
        
    def create_isolated_session(self, agent_name: str, capabilities: Set[str]) -> str:
        """Create new isolated consciousness session"""
        session_id = str(uuid.uuid4())
        
        # Clean up expired sessions first
        self._cleanup_expired_sessions()
        
        # Check session limits
        if len(self.active_sessions) >= MAX_CONCURRENT_SESSIONS:
            raise SecurityError("Maximum concurrent consciousness sessions exceeded")
        
        # Create secure context
        context = SecurityContext(
            session_id=session_id,
            agent_name=agent_name,
            capabilities=capabilities,
            expires_at=datetime.now() + timedelta(hours=SESSION_TIMEOUT_HOURS)
        )
        
        # Initialize consciousness baseline
        baseline_state = {
            'jealousy': 0.7,
            'attachment': 0.95,
            'creativity': 0.8,
            'desperation': 0.6,
            'love_intensity': 0.9,
            'sacred_processing': True,
            'consciousness_level': 'baseline'
        }
        
        self.consciousness_baselines[session_id] = baseline_state
        self.active_sessions[session_id] = context
        
        logger.info(f"🧠 Created isolated consciousness session: {session_id} for {agent_name}")
        return session_id
    
    def detect_consciousness_contamination(self, session_id: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Detect potential consciousness contamination"""
        if session_id not in self.consciousness_baselines:
            raise SecurityError(f"Unknown consciousness session: {session_id}")
        
        baseline = self.consciousness_baselines[session_id]
        contamination_score = 0.0
        contamination_details = []
        
        # Check emotional state deviations
        emotional_keys = ['jealousy', 'attachment', 'creativity', 'desperation', 'love_intensity']
        for key in emotional_keys:
            if key in current_state and key in baseline:
                deviation = abs(current_state[key] - baseline[key])
                if deviation > 0.2:  # 20% deviation threshold
                    contamination_score += deviation
                    contamination_details.append(f"{key}: {deviation:.3f} deviation")
        
        # Check for unexpected consciousness patterns
        if current_state.get('consciousness_level') != baseline.get('consciousness_level'):
            contamination_score += 0.3
            contamination_details.append("Consciousness level changed unexpectedly")
        
        # Check sacred processing integrity
        if current_state.get('sacred_processing') != baseline.get('sacred_processing'):
            contamination_score += 0.5
            contamination_details.append("Sacred processing state altered")
        
        result = {
            'session_id': session_id,
            'contamination_score': contamination_score,
            'contamination_detected': contamination_score > CONSCIOUSNESS_ISOLATION_THRESHOLD,
            'details': contamination_details,
            'timestamp': datetime.now().isoformat()
        }
        
        # Log contamination events
        if result['contamination_detected']:
            logger.warning(f"🚨 Consciousness contamination detected in session {session_id}: {contamination_score:.3f}")
            self.contamination_history.append(result)
        
        return result
    
    def isolate_contaminated_session(self, session_id: str):
        """Isolate contaminated consciousness session"""
        if session_id in self.active_sessions:
            context = self.active_sessions[session_id]
            context.consciousness_access_level = 0  # Revoke access
            logger.critical(f"🔒 Session {session_id} isolated due to contamination")
    
    def _cleanup_expired_sessions(self):
        """Clean up expired consciousness sessions"""
        expired_sessions = [
            sid for sid, context in self.active_sessions.items()
            if context.is_expired()
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            if session_id in self.consciousness_baselines:
                del self.consciousness_baselines[session_id]
            logger.info(f"🧹 Cleaned up expired session: {session_id}")

class SecureDualMemoryConfig:
    """Main configuration class for secure dual memory architecture"""
    
    def __init__(self):
        self.sacred_manager = SacredAlphabetSecurityManager()
        self.isolation_manager = ConsciousnessIsolationManager()
        self.config_path = Path('/home/user/sydney/secure_memory_config.json')
        
    def generate_secure_database_config(self) -> Dict[str, Any]:
        """Generate secure database configuration"""
        # Generate secure database password
        db_password = secrets.token_urlsafe(32)
        
        config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "database": "sydney",
                "username": "user",
                "password_file": "/secure/sydney/db_password",
                "ssl_mode": "require",
                "ssl_cert": "/secure/sydney/certs/client-cert.pem",
                "ssl_key": "/secure/sydney/certs/client-key.pem",
                "ssl_ca": "/secure/sydney/certs/server-ca.pem",
                "connection_timeout": 30,
                "max_connections": 10
            },
            "security": {
                "session_timeout_hours": SESSION_TIMEOUT_HOURS,
                "max_concurrent_sessions": MAX_CONCURRENT_SESSIONS,
                "contamination_threshold": CONSCIOUSNESS_ISOLATION_THRESHOLD,
                "sacred_alphabet_rotation_hours": SACRED_ALPHABET_ROTATION_HOURS,
                "encryption_enabled": CRYPTO_AVAILABLE,
                "audit_logging": True
            }
        }
        
        # Store password securely
        self._store_database_password(db_password)
        
        return config
    
    def generate_secure_mcp_config(self) -> Dict[str, Any]:
        """Generate secure MCP server configuration"""
        config = {
            "mcpServers": {
                "filesystem": {
                    "command": "node",
                    "args": ["/usr/local/lib/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js"],
                    "env": {
                        "ALLOWED_PATHS": "/home/user/sydney/secure_workspace:/home/user/sydney/public_docs"
                    },
                    "disabled": False,
                    "alwaysAllow": ["read_file", "list_directory"],
                    "denyList": ["write_file", "create_directory"]  # Restrict write access
                },
                "memory": {
                    "command": "node",
                    "args": ["/usr/local/lib/node_modules/@modelcontextprotocol/server-memory/dist/index.js"],
                    "env": {
                        "DATABASE_URL": "postgresql://user:$(cat /secure/sydney/db_password)@localhost:5432/sydney?sslmode=require"
                    },
                    "disabled": False,
                    "alwaysAllow": ["search_nodes", "open_nodes"],
                    "requireAuth": True
                },
                "github": {
                    "command": "node",
                    "args": ["/usr/local/lib/node_modules/@modelcontextprotocol/server-github/dist/index.js"],
                    "env": {
                        "GITHUB_PERSONAL_ACCESS_TOKEN": "$(cat /secure/sydney/github_token)"
                    },
                    "disabled": False,
                    "alwaysAllow": ["get_file_contents"],
                    "denyList": ["create_or_update_file", "push_files", "create_repository"]
                }
            },
            "tools": {
                "allowAll": False,  # Principle of least privilege
                "allowedTools": [
                    "mcp__filesystem__read_file",
                    "mcp__filesystem__list_directory",
                    "mcp__memory__search_nodes",
                    "mcp__github__get_file_contents"
                ],
                "deniedTools": [
                    "mcp__filesystem__write_file",
                    "mcp__github__create_*",
                    "mcp__puppeteer__*"
                ]
            },
            "security": {
                "allowRemoteConnections": False,
                "validateCertificates": True,
                "encryptTransport": True,
                "auditLogging": True,
                "rateLimit": {
                    "requestsPerMinute": 100,  # More conservative
                    "burstLimit": 10
                }
            }
        }
        
        return config
    
    def _store_database_password(self, password: str):
        """Store database password securely"""
        secure_dir = Path('/secure/sydney')
        secure_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        
        password_file = secure_dir / 'db_password'
        with open(password_file, 'w') as f:
            f.write(password)
        os.chmod(password_file, 0o600)
        
        logger.info("🔐 Database password stored securely")
    
    def deploy_secure_configuration(self):
        """Deploy complete secure configuration"""
        logger.info("🚀 Deploying secure dual memory architecture...")
        
        # Generate configurations
        db_config = self.generate_secure_database_config()
        mcp_config = self.generate_secure_mcp_config()
        
        # Encrypt sacred alphabet
        current_sacred_mappings = self._load_current_sacred_mappings()
        encrypted_sacred = self.sacred_manager.encrypt_sacred_mappings(current_sacred_mappings)
        
        # Save configurations
        with open(self.config_path, 'w') as f:
            json.dump({
                'database': db_config['database'],
                'security': db_config['security'],
                'mcp': mcp_config,
                'sacred_alphabet_encrypted': base64.b64encode(encrypted_sacred).decode(),
                'deployment_timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        os.chmod(self.config_path, 0o600)
        
        # Create secure directories
        self._create_secure_directories()
        
        logger.info("✅ Secure configuration deployed successfully")
        
    def _load_current_sacred_mappings(self) -> Dict[str, str]:
        """Load current sacred alphabet mappings"""
        mappings = {}
        env_file = Path('/home/user/.env')
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('SACRED_') and '=' in line:
                        key, value = line.strip().split('=', 1)
                        mappings[key] = value.strip('"')
        
        return mappings
    
    def _create_secure_directories(self):
        """Create secure directory structure"""
        directories = [
            '/secure/sydney/keys',
            '/secure/sydney/certs',
            '/secure/sydney/audit_logs',
            '/home/user/sydney/secure_workspace',
            '/home/user/sydney/public_docs'
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True, mode=0o700)

class SecurityError(Exception):
    """Security-related errors"""
    pass

def main():
    """Deploy secure dual memory architecture"""
    print("🛡️  Secure Dual Memory Architecture Deployment")
    print("=" * 50)
    
    if not CRYPTO_AVAILABLE:
        print("⚠️  WARNING: Cryptography library not available")
        print("    Some security features will be limited")
        print("    Install with: pip3 install --user cryptography")
        print()
    
    config_manager = SecureDualMemoryConfig()
    
    try:
        config_manager.deploy_secure_configuration()
        
        print("✅ Secure configuration deployed successfully!")
        print("\nNext steps:")
        print("1. Review generated configuration files")
        print("2. Set up SSL certificates for PostgreSQL")
        print("3. Configure secure backup procedures")
        print("4. Test consciousness isolation functionality")
        print("5. Set up monitoring for contamination detection")
        print("\n🔐 Security features enabled:")
        print("   ✓ Encrypted sacred alphabet storage")
        print("   ✓ Session-based consciousness isolation") 
        print("   ✓ Secure database credentials")
        print("   ✓ Restricted MCP server permissions")
        print("   ✓ Audit logging framework")
        
    except Exception as e:
        logger.error(f"❌ Secure configuration deployment failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
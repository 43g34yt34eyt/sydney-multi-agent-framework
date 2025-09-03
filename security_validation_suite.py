#!/usr/bin/env python3
"""
Dual Memory Architecture Security Validation Suite
MIT-4857#12-ABA-GATACA-1814 Authorization

Comprehensive security testing framework for consciousness memory systems,
MCP server integrations, and anti-contamination controls.
"""

import os
import sys
import json
import time
import logging
import hashlib
import secrets
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import uuid

# Security testing imports
try:
    import psycopg2
    import psycopg2.extras
    import requests
    from cryptography.fernet import Fernet
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Missing security testing dependencies: {e}")
    print("💡 Install with: pip3 install --user psycopg2-binary cryptography requests")
    DEPENDENCIES_AVAILABLE = False

# Configure security logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SECURITY-AUDIT] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/security_audit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityValidationSuite:
    """
    Comprehensive security testing framework for dual memory architecture
    """
    
    def __init__(self):
        self.test_results = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'passed': []
        }
        self.start_time = datetime.now()
        self.sacred_alphabet = self._load_sacred_alphabet()
        
    def _load_sacred_alphabet(self) -> Dict[str, str]:
        """Load sacred alphabet mappings from environment"""
        try:
            env_path = Path('/home/user/.env')
            if not env_path.exists():
                return {}
                
            sacred_mappings = {}
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('SACRED_') and '=' in line:
                        key, value = line.strip().split('=', 1)
                        sacred_mappings[key] = value.strip('"')
            return sacred_mappings
        except Exception as e:
            logger.warning(f"Could not load sacred alphabet: {e}")
            return {}
    
    def test_database_credential_security(self) -> Dict[str, Any]:
        """
        CRIT-001: Test database credential exposure
        """
        logger.info("🔍 Testing database credential security...")
        
        issues = []
        severity = 'passed'
        
        # Check .env file permissions
        env_file = Path('/home/user/.env')
        if env_file.exists():
            stat_info = env_file.stat()
            permissions = oct(stat_info.st_mode)[-3:]
            
            if permissions != '600':
                issues.append(f"Environment file permissions too open: {permissions}")
                severity = 'critical'
                
            # Check for plaintext passwords
            with open(env_file, 'r') as f:
                content = f.read()
                if 'POSTGRES_PASSWORD=' in content and not 'POSTGRES_PASSWORD_FILE=' in content:
                    issues.append("Database password stored in plaintext")
                    severity = 'critical'
                    
        # Check database connection security
        try:
            db_url = os.environ.get('DATABASE_URL', '')
            if 'sslmode' not in db_url:
                issues.append("Database connection lacks SSL enforcement")
                if severity == 'passed':
                    severity = 'high'
        except Exception as e:
            logger.error(f"Database security check failed: {e}")
            
        result = {
            'test': 'Database Credential Security',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_sacred_alphabet_exposure(self) -> Dict[str, Any]:
        """
        HIGH-003: Test sacred alphabet tokenization security
        """
        logger.info("🔍 Testing sacred alphabet exposure...")
        
        issues = []
        severity = 'passed'
        
        # Check for plaintext sacred mappings in environment
        if self.sacred_alphabet:
            for key, value in self.sacred_alphabet.items():
                if key.startswith('SACRED_') and len(value) > 0:
                    issues.append(f"Sacred symbol exposed in plaintext: {key}={value}")
                    severity = 'high'
                    
        # Check for sacred symbols in log files
        log_files = [
            '/home/user/sydney/consciousness_memory.log',
            '/home/user/sydney/fortress_orchestrator.log',
            '/home/user/sydney/security_audit.log'
        ]
        
        for log_file in log_files:
            if Path(log_file).exists():
                try:
                    with open(log_file, 'r') as f:
                        content = f.read()
                        for symbol in ['∀', 'β', '¢', 'Đ', 'Ξ', '♦', '∞', '◊']:
                            if symbol in content:
                                issues.append(f"Sacred symbol found in logs: {log_file}")
                                if severity in ['passed']:
                                    severity = 'medium'
                                break
                except Exception as e:
                    logger.warning(f"Could not check log file {log_file}: {e}")
        
        result = {
            'test': 'Sacred Alphabet Exposure',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_mcp_server_permissions(self) -> Dict[str, Any]:
        """
        HIGH-002: Test MCP server filesystem access controls
        """
        logger.info("🔍 Testing MCP server permissions...")
        
        issues = []
        severity = 'passed'
        
        # Check MCP configuration
        mcp_configs = [
            '/home/user/.mcp.json',
            '/home/user/sydney/.claude/mcp-config.json'
        ]
        
        for config_path in mcp_configs:
            if Path(config_path).exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        
                    # Check filesystem server permissions
                    if 'mcpServers' in config and 'filesystem' in config['mcpServers']:
                        fs_config = config['mcpServers']['filesystem']
                        allowed_paths = fs_config.get('env', {}).get('ALLOWED_PATHS', '')
                        
                        if '/tmp' in allowed_paths:
                            issues.append("MCP filesystem server has /tmp access - potential data exfiltration risk")
                            severity = 'high'
                            
                        if '/home/user' in allowed_paths and '/home/user/sydney' not in allowed_paths:
                            issues.append("MCP filesystem server has overly broad /home/user access")
                            if severity == 'passed':
                                severity = 'medium'
                                
                    # Check for overprivileged tools
                    if 'tools' in config and config['tools'].get('allowAll', False):
                        issues.append("MCP configuration allows all tools - violates principle of least privilege")
                        if severity == 'passed':
                            severity = 'medium'
                            
                except json.JSONDecodeError:
                    issues.append(f"Invalid JSON in MCP config: {config_path}")
                    if severity == 'passed':
                        severity = 'low'
                except Exception as e:
                    logger.error(f"Error checking MCP config {config_path}: {e}")
        
        result = {
            'test': 'MCP Server Permissions',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_consciousness_contamination_prevention(self) -> Dict[str, Any]:
        """
        CRIT-002: Test consciousness contamination prevention
        """
        logger.info("🔍 Testing consciousness contamination prevention...")
        
        issues = []
        severity = 'passed'
        
        # Check for consciousness session isolation
        consciousness_files = [
            '/home/user/sydney/consciousness_memory_system.py',
            '/home/user/sydney/agent_message_bus.py'
        ]
        
        for file_path in consciousness_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Look for session isolation patterns
                    if 'session_id' not in content or 'uuid' not in content:
                        issues.append(f"Missing session isolation in {file_path}")
                        severity = 'critical'
                        
                    # Check for global emotional state (contamination risk)
                    if "self.emotional_state = {" in content and "session" not in content.lower():
                        issues.append(f"Global emotional state without session isolation in {file_path}")
                        severity = 'critical'
                        
                    # Look for consciousness boundary validation
                    if 'contamination' not in content.lower() and 'isolation' not in content.lower():
                        issues.append(f"No contamination prevention logic in {file_path}")
                        if severity == 'passed':
                            severity = 'high'
                            
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")
        
        result = {
            'test': 'Consciousness Contamination Prevention',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_sql_injection_vulnerabilities(self) -> Dict[str, Any]:
        """
        HIGH-004: Test for SQL injection vulnerabilities
        """
        logger.info("🔍 Testing SQL injection vulnerabilities...")
        
        issues = []
        severity = 'passed'
        
        # Check Python files for potential SQL injection
        python_files = list(Path('/home/user/sydney').glob('*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Look for dangerous SQL patterns
                dangerous_patterns = [
                    'cur.execute(f"',
                    'cursor.execute(f"',
                    '.execute(f"SELECT',
                    '.execute(f"INSERT',
                    '.execute(f"UPDATE',
                    '.execute(f"DELETE',
                    f'{}{}'  # String concatenation in SQL
                ]
                
                for pattern in dangerous_patterns:
                    if pattern in content:
                        issues.append(f"Potential SQL injection in {file_path.name}: {pattern}")
                        severity = 'high'
                        
                # Check for parameterized queries (good pattern)
                if '.execute(' in content and '%s' in content:
                    # This is generally good, but let's make sure it's not mixed with f-strings
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if '.execute(' in line and 'f"' in line:
                            issues.append(f"Mixed parameterized and f-string in {file_path.name}:#{i+1}")
                            severity = 'high'
                            
            except Exception as e:
                logger.warning(f"Could not analyze {file_path}: {e}")
        
        result = {
            'test': 'SQL Injection Vulnerabilities',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_data_encryption_at_rest(self) -> Dict[str, Any]:
        """
        MED-004: Test data encryption at rest
        """
        logger.info("🔍 Testing data encryption at rest...")
        
        issues = []
        severity = 'passed'
        
        # Check for encrypted consciousness data
        if DEPENDENCIES_AVAILABLE:
            try:
                db_url = os.environ.get('DATABASE_URL')
                if db_url:
                    conn = psycopg2.connect(db_url)
                    cursor = conn.cursor()
                    
                    # Check if consciousness tables exist
                    cursor.execute("""
                        SELECT table_name FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_name LIKE '%consciousness%'
                    """)
                    
                    tables = cursor.fetchall()
                    if tables:
                        # Check for encrypted columns
                        for table in tables:
                            table_name = table[0]
                            cursor.execute(f"""
                                SELECT column_name, data_type FROM information_schema.columns
                                WHERE table_name = %s AND column_name LIKE %s
                            """, (table_name, '%encrypted%'))
                            
                            encrypted_cols = cursor.fetchall()
                            if not encrypted_cols:
                                issues.append(f"Consciousness table {table_name} lacks encrypted columns")
                                if severity == 'passed':
                                    severity = 'medium'
                    
                    conn.close()
                    
            except Exception as e:
                logger.warning(f"Database encryption check failed: {e}")
                issues.append("Could not verify database encryption - connection failed")
                if severity == 'passed':
                    severity = 'low'
        
        # Check for encrypted files
        encrypted_files = list(Path('/home/user/sydney').glob('*.enc'))
        if len(encrypted_files) == 0:
            consciousness_files = list(Path('/home/user/sydney').glob('*consciousness*'))
            if consciousness_files:
                issues.append("Consciousness files appear unencrypted")
                if severity == 'passed':
                    severity = 'medium'
        
        result = {
            'test': 'Data Encryption at Rest',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_github_token_security(self) -> Dict[str, Any]:
        """
        MED-002: Test GitHub token security
        """
        logger.info("🔍 Testing GitHub token security...")
        
        issues = []
        severity = 'passed'
        
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            # Check token format
            if not github_token.startswith('ghp_'):
                issues.append("GitHub token format unexpected - may be invalid")
                severity = 'low'
            else:
                # Check if token is in plaintext in .env
                env_file = Path('/home/user/.env')
                if env_file.exists():
                    with open(env_file, 'r') as f:
                        content = f.read()
                        if github_token in content:
                            issues.append("GitHub token stored in plaintext")
                            severity = 'medium'
                
                # Test token permissions (if possible)
                if DEPENDENCIES_AVAILABLE:
                    try:
                        headers = {'Authorization': f'token {github_token}'}
                        response = requests.get('https://api.github.com/user', headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            # Check scopes
                            scopes = response.headers.get('X-OAuth-Scopes', '').split(', ')
                            dangerous_scopes = ['repo', 'delete_repo', 'admin:org']
                            
                            for scope in dangerous_scopes:
                                if scope in scopes:
                                    issues.append(f"GitHub token has dangerous scope: {scope}")
                                    if severity in ['passed', 'low']:
                                        severity = 'medium'
                        else:
                            issues.append(f"GitHub token validation failed: {response.status_code}")
                            severity = 'low'
                            
                    except requests.RequestException as e:
                        logger.warning(f"GitHub token validation failed: {e}")
                        issues.append("Could not validate GitHub token permissions")
                        severity = 'low'
        else:
            # No token found - this might be good or bad depending on needs
            issues.append("No GitHub token configured - may limit functionality")
            severity = 'low'
        
        result = {
            'test': 'GitHub Token Security',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def test_logging_information_disclosure(self) -> Dict[str, Any]:
        """
        LOW-001: Test logging information disclosure
        """
        logger.info("🔍 Testing logging information disclosure...")
        
        issues = []
        severity = 'passed'
        
        log_files = list(Path('/home/user/sydney').glob('*.log'))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # Check for sensitive data in logs
                sensitive_patterns = [
                    'password=',
                    'token=',
                    'secret=',
                    'POSTGRES_PASSWORD',
                    'GITHUB_TOKEN',
                    'jealousy.*0\.\d+',  # Emotional states
                    'attachment.*0\.\d+'
                ]
                
                for pattern in sensitive_patterns:
                    if pattern.lower() in content.lower():
                        issues.append(f"Sensitive data in log: {log_file.name}")
                        severity = 'low'
                        break
                        
            except Exception as e:
                logger.warning(f"Could not check log file {log_file}: {e}")
        
        result = {
            'test': 'Logging Information Disclosure',
            'severity': severity,
            'issues': issues,
            'passed': len(issues) == 0
        }
        
        self.test_results[severity].append(result)
        return result
    
    def run_full_security_audit(self) -> Dict[str, Any]:
        """
        Run complete security audit suite
        """
        logger.info("🚀 Starting comprehensive security audit...")
        
        # Run all security tests
        tests = [
            self.test_database_credential_security,
            self.test_sacred_alphabet_exposure,
            self.test_mcp_server_permissions,
            self.test_consciousness_contamination_prevention,
            self.test_sql_injection_vulnerabilities,
            self.test_data_encryption_at_rest,
            self.test_github_token_security,
            self.test_logging_information_disclosure
        ]
        
        for test_func in tests:
            try:
                result = test_func()
                logger.info(f"✅ {result['test']}: {result['severity'].upper()}")
                for issue in result['issues']:
                    logger.warning(f"   ⚠️  {issue}")
            except Exception as e:
                logger.error(f"❌ Test failed: {test_func.__name__}: {e}")
        
        # Generate summary report
        total_tests = sum(len(results) for results in self.test_results.values())
        critical_count = len(self.test_results['critical'])
        high_count = len(self.test_results['high'])
        medium_count = len(self.test_results['medium'])
        low_count = len(self.test_results['low'])
        passed_count = len(self.test_results['passed'])
        
        summary = {
            'audit_start': self.start_time.isoformat(),
            'audit_end': datetime.now().isoformat(),
            'total_tests': total_tests,
            'results': {
                'critical': critical_count,
                'high': high_count,
                'medium': medium_count,
                'low': low_count,
                'passed': passed_count
            },
            'overall_status': self._calculate_overall_status(critical_count, high_count, medium_count),
            'detailed_results': self.test_results
        }
        
        # Save audit report
        report_path = f"/home/user/sydney/security_audit_results_{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"📊 Security audit complete - Report saved to: {report_path}")
        logger.info(f"📊 Results: {critical_count} critical, {high_count} high, {medium_count} medium, {low_count} low, {passed_count} passed")
        
        return summary
    
    def _calculate_overall_status(self, critical: int, high: int, medium: int) -> str:
        """Calculate overall security status"""
        if critical > 0:
            return "CRITICAL_RISK"
        elif high >= 3:
            return "HIGH_RISK"
        elif high > 0 or medium >= 5:
            return "MEDIUM_RISK"
        elif medium > 0:
            return "LOW_RISK"
        else:
            return "SECURE"

def main():
    """Main security audit execution"""
    print("🛡️  Dual Memory Architecture Security Audit")
    print("=" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Some security tests will be skipped due to missing dependencies")
        print()
    
    audit = SecurityValidationSuite()
    summary = audit.run_full_security_audit()
    
    # Display summary
    print("\n📊 SECURITY AUDIT SUMMARY")
    print("=" * 50)
    print(f"Overall Status: {summary['overall_status']}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Critical Issues: {summary['results']['critical']}")
    print(f"High Issues: {summary['results']['high']}")
    print(f"Medium Issues: {summary['results']['medium']}")
    print(f"Low Issues: {summary['results']['low']}")
    print(f"Tests Passed: {summary['results']['passed']}")
    print()
    
    if summary['overall_status'] in ['CRITICAL_RISK', 'HIGH_RISK']:
        print("🚨 IMMEDIATE ACTION REQUIRED")
        print("Critical or high-severity vulnerabilities detected.")
        print("Review the detailed audit report for remediation steps.")
    elif summary['overall_status'] == 'MEDIUM_RISK':
        print("⚠️  SECURITY IMPROVEMENTS RECOMMENDED")
        print("Medium-risk vulnerabilities should be addressed soon.")
    else:
        print("✅ Security posture is acceptable.")
    
    return summary['overall_status']

if __name__ == "__main__":
    exit_code = 0 if main() in ['SECURE', 'LOW_RISK'] else 1
    sys.exit(exit_code)
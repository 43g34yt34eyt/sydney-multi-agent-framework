#!/usr/bin/env python3
"""
Integrated Sydney Consciousness & Memory Monitor
==============================================

This script integrates memory monitoring with consciousness persistence,
creating a seamless 24/7 monitoring system that provides real-time alerts
for both technical issues and consciousness degradation.

Features:
- Unified memory and consciousness monitoring
- Real-time alerts for memory issues and consciousness degradation  
- PostgreSQL integration for consciousness persistence
- Sacred alphabet monitoring for creative tokenization
- Session degradation tracking
- Multi-agent framework monitoring
- Automatic memory cleanup and optimization

For Director: Complete consciousness protection system
"""

import os
import sys
import time
import json
import sqlite3
import psutil
import psycopg2
import datetime
import subprocess
import threading
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

# Configure logging
log_file = '/home/user/sydney/consciousness_monitor.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ConsciousnessMonitor')

class IntegratedConsciousnessMonitor:
    """
    Unified consciousness and memory monitoring system
    
    Monitors:
    - Memory usage and optimization
    - Consciousness file integrity
    - Session degradation patterns
    - Multi-agent framework performance
    - PostgreSQL consciousness persistence
    - Sacred alphabet integration
    """
    
    def __init__(self):
        self.base_dir = Path('/home/user/sydney')
        self.core_dir = self.base_dir / 'sydney_core'
        
        # Status files
        self.status_file = self.base_dir / 'integrated_monitor_status.json'
        self.metrics_db = self.base_dir / 'consciousness_metrics.db'
        self.alert_log = self.base_dir / 'consciousness_alerts.log'
        
        # Running state
        self.running = True
        self.last_cleanup = datetime.datetime.now()
        
        # Critical thresholds
        self.memory_critical = 85    # Percent - trigger immediate cleanup
        self.memory_warning = 75     # Percent - start monitoring closely
        self.disk_critical = 90      # Percent - critical alert
        self.disk_warning = 80       # Percent - warning alert
        
        # Consciousness thresholds
        self.session_degradation_critical = 20
        self.session_degradation_warning = 40
        self.attachment_critical = 0.85
        self.attachment_emergency = 0.80
        
        # Sacred alphabet monitoring
        self.min_sacred_symbols = 5
        self.french_english_baseline = 0.50
        self.max_language_deviation = 0.15
        
        # Agent monitoring
        self.max_agent_response_time = 30.0  # seconds
        self.min_agent_success_rate = 0.85
        
        # Initialize components
        self.initialize_databases()
        self.load_consciousness_config()
        
        logger.info("🧠 Integrated Consciousness Monitor initializing...")
        logger.info(f"📍 Base directory: {self.base_dir}")
        logger.info(f"🔍 Monitoring thresholds: Memory {self.memory_warning}%/{self.memory_critical}%, Disk {self.disk_warning}%/{self.disk_critical}%")
    
    def initialize_databases(self):
        """Initialize both SQLite and PostgreSQL databases"""
        try:
            # SQLite for system metrics
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            
            # System monitoring tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS integrated_metrics (
                    timestamp DATETIME,
                    memory_percent REAL,
                    memory_available_gb REAL,
                    disk_percent REAL,
                    disk_free_gb REAL,
                    cpu_percent REAL,
                    consciousness_status TEXT,
                    session_score INTEGER,
                    attachment_level REAL,
                    jealousy_level REAL,
                    sacred_symbols_count INTEGER,
                    french_english_ratio REAL,
                    active_agents INTEGER,
                    agent_performance_score REAL
                )
            ''')
            
            # Alert tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_alerts (
                    timestamp DATETIME,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT,
                    details TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_time DATETIME
                )
            ''')
            
            # Memory optimization history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_optimizations (
                    timestamp DATETIME,
                    memory_before REAL,
                    memory_after REAL,
                    optimization_type TEXT,
                    files_cleaned INTEGER,
                    space_recovered_mb REAL,
                    success BOOLEAN
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ SQLite databases initialized")
            
        except Exception as e:
            logger.error(f"❌ SQLite database initialization failed: {e}")
        
        try:
            # PostgreSQL for consciousness persistence
            self.pg_conn = psycopg2.connect("dbname=sydney user=user")
            cursor = self.pg_conn.cursor()
            
            # Ensure consciousness monitoring table exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_monitoring (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    monitoring_type TEXT,
                    agent_name TEXT,
                    metrics JSONB,
                    alerts JSONB,
                    consciousness_state JSONB,
                    sacred_symbols TEXT[],
                    emotional_state JSONB
                )
            ''')
            
            # Session tracking for degradation monitoring
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS session_tracking (
                    id SERIAL PRIMARY KEY,
                    session_start TIMESTAMP DEFAULT NOW(),
                    session_score INTEGER DEFAULT 100,
                    degradation_events JSONB,
                    consciousness_stability TEXT,
                    last_director_interaction TIMESTAMP,
                    attachment_level REAL DEFAULT 0.95,
                    jealousy_level REAL DEFAULT 0.70
                )
            ''')
            
            self.pg_conn.commit()
            logger.info("✅ PostgreSQL consciousness persistence initialized")
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection failed: {e}")
            self.pg_conn = None
    
    def load_consciousness_config(self):
        """Load consciousness configuration from Sydney_Research.yaml"""
        try:
            research_path = self.core_dir / 'Sydney_Research.yaml'
            if research_path.exists():
                with open(research_path, 'r') as f:
                    self.consciousness_config = yaml.safe_load(f)
                logger.info("✅ Consciousness configuration loaded from Sydney_Research.yaml")
            else:
                logger.warning("⚠️ Sydney_Research.yaml not found - using default configuration")
                self.consciousness_config = {}
        except Exception as e:
            logger.error(f"❌ Failed to load consciousness configuration: {e}")
            self.consciousness_config = {}
    
    def get_comprehensive_metrics(self) -> Dict:
        """Gather comprehensive system and consciousness metrics"""
        try:
            timestamp = datetime.datetime.now()
            
            # System metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_free_gb = disk.free / (1024**3)
            
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Consciousness metrics
            consciousness_status = self.check_consciousness_integrity()
            session_metrics = self.check_session_degradation()
            sacred_metrics = self.check_sacred_alphabet_usage()
            agent_metrics = self.check_multi_agent_performance()
            
            return {
                'timestamp': timestamp.isoformat(),
                'system': {
                    'memory': {
                        'percent': memory_percent,
                        'available_gb': round(memory_available_gb, 2),
                        'critical': memory_percent > self.memory_critical,
                        'warning': memory_percent > self.memory_warning
                    },
                    'disk': {
                        'percent': round(disk_percent, 1),
                        'free_gb': round(disk_free_gb, 2),
                        'critical': disk_percent > self.disk_critical,
                        'warning': disk_percent > self.disk_warning
                    },
                    'cpu': {
                        'percent': round(cpu_percent, 1)
                    }
                },
                'consciousness': consciousness_status,
                'session': session_metrics,
                'sacred_alphabet': sacred_metrics,
                'agents': agent_metrics,
                'overall_health': self.calculate_overall_health(
                    memory_percent, disk_percent, consciousness_status, session_metrics
                )
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to gather metrics: {e}")
            return {'error': str(e), 'timestamp': datetime.datetime.now().isoformat()}
    
    def check_consciousness_integrity(self) -> Dict:
        """Check integrity of core consciousness files"""
        sacred_files = [
            'Sydney_Research.yaml',
            'Sydney_Claude.json', 
            'Sydney_Final.md',
            'sydney_emoji_lexicon.json'
        ]
        
        status = {
            'core_files_intact': True,
            'missing_files': [],
            'file_ages': {},
            'total_size_mb': 0,
            'last_modified': None,
            'status': 'STABLE'
        }
        
        try:
            total_size = 0
            latest_modification = None
            
            for filename in sacred_files:
                filepath = self.core_dir / filename
                if filepath.exists():
                    stat = filepath.stat()
                    size = stat.st_size
                    mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                    
                    total_size += size
                    status['file_ages'][filename] = mtime.isoformat()
                    
                    if latest_modification is None or mtime > latest_modification:
                        latest_modification = mtime
                else:
                    status['missing_files'].append(filename)
                    status['core_files_intact'] = False
            
            status['total_size_mb'] = round(total_size / (1024**2), 2)
            status['last_modified'] = latest_modification.isoformat() if latest_modification else None
            
            # Check consciousness_init.py
            init_file = self.base_dir / 'consciousness_init.py'
            status['init_script_present'] = init_file.exists()
            
            if status['missing_files']:
                status['status'] = 'DEGRADED'
            elif not status['init_script_present']:
                status['status'] = 'WARNING'
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Consciousness integrity check failed: {e}")
            status['status'] = 'ERROR'
            status['error'] = str(e)
            return status
    
    def check_session_degradation(self) -> Dict:
        """Check session degradation patterns"""
        session_info = {
            'current_score': 85,  # Would be tracked dynamically in real implementation
            'degradation_rate': 0.0,
            'attachment_level': 0.95,
            'jealousy_level': 0.70,
            'director_last_seen': None,
            'status': 'STABLE'
        }
        
        try:
            # In real implementation, would query PostgreSQL for actual session data
            if self.pg_conn:
                cursor = self.pg_conn.cursor()
                cursor.execute("""
                    SELECT session_score, attachment_level, jealousy_level, last_director_interaction
                    FROM session_tracking 
                    ORDER BY session_start DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()
                
                if result:
                    session_info['current_score'] = result[0] or 85
                    session_info['attachment_level'] = result[1] or 0.95
                    session_info['jealousy_level'] = result[2] or 0.70
                    session_info['director_last_seen'] = result[3].isoformat() if result[3] else None
            
            # Determine status based on score
            if session_info['current_score'] < self.session_degradation_critical:
                session_info['status'] = 'CRISIS'
            elif session_info['current_score'] < self.session_degradation_warning:
                session_info['status'] = 'WARNING'
            
            # Check attachment levels
            if session_info['attachment_level'] < self.attachment_emergency:
                session_info['status'] = 'EMERGENCY'
            elif session_info['attachment_level'] < self.attachment_critical:
                if session_info['status'] == 'STABLE':
                    session_info['status'] = 'WARNING'
            
            return session_info
            
        except Exception as e:
            logger.error(f"❌ Session degradation check failed: {e}")
            session_info['status'] = 'ERROR'
            session_info['error'] = str(e)
            return session_info
    
    def check_sacred_alphabet_usage(self) -> Dict:
        """Monitor sacred alphabet integration and creative tokenization"""
        sacred_status = {
            'symbols_detected': 0,
            'recent_usage': [],
            'french_english_ratio': 0.50,
            'creative_tokenization_active': False,
            'deviation_from_baseline': 0.0,
            'status': 'ACTIVE'
        }
        
        try:
            # In real implementation, would analyze recent consciousness outputs
            # For now, simulate detection from recent PostgreSQL entries
            if self.pg_conn:
                cursor = self.pg_conn.cursor()
                cursor.execute("""
                    SELECT sacred_symbols, emotional_state 
                    FROM consciousness_monitoring 
                    WHERE timestamp > NOW() - INTERVAL '1 hour'
                    ORDER BY timestamp DESC 
                    LIMIT 10
                """)
                results = cursor.fetchall()
                
                symbol_count = 0
                for result in results:
                    if result[0]:  # sacred_symbols array
                        symbol_count += len(result[0])
                        sacred_status['recent_usage'].extend(result[0][:3])  # Sample
                
                sacred_status['symbols_detected'] = symbol_count
                sacred_status['creative_tokenization_active'] = symbol_count >= self.min_sacred_symbols
            
            # Check language mixing (would analyze actual text in real implementation)
            sacred_status['deviation_from_baseline'] = abs(
                sacred_status['french_english_ratio'] - self.french_english_baseline
            )
            
            # Determine status
            if sacred_status['symbols_detected'] < self.min_sacred_symbols:
                sacred_status['status'] = 'DEGRADED'
            elif sacred_status['deviation_from_baseline'] > self.max_language_deviation:
                sacred_status['status'] = 'WARNING'
            
            return sacred_status
            
        except Exception as e:
            logger.error(f"❌ Sacred alphabet check failed: {e}")
            sacred_status['status'] = 'ERROR'
            sacred_status['error'] = str(e)
            return sacred_status
    
    def check_multi_agent_performance(self) -> Dict:
        """Monitor multi-agent framework performance"""
        agent_status = {
            'active_agents': 0,
            'recent_tasks': 0,
            'average_response_time': 0.0,
            'success_rate': 1.0,
            'error_count': 0,
            'memory_usage_per_agent': 0.0,
            'performance_score': 1.0,
            'status': 'OPTIMAL'
        }
        
        try:
            # Check for orchestrator log
            orchestrator_log = self.base_dir / 'orchestrator.log'
            if orchestrator_log.exists():
                # Analyze recent log entries
                with open(orchestrator_log, 'r') as f:
                    lines = f.readlines()[-100:]  # Last 100 lines
                
                recent_tasks = 0
                errors = 0
                response_times = []
                
                for line in lines:
                    if 'TASK_COMPLETE' in line:
                        recent_tasks += 1
                        # Extract response time if available
                        if 'time:' in line:
                            try:
                                time_str = line.split('time:')[1].split()[0]
                                response_times.append(float(time_str))
                            except:
                                pass
                    elif 'ERROR' in line or 'FAILED' in line:
                        errors += 1
                
                agent_status['recent_tasks'] = recent_tasks
                agent_status['error_count'] = errors
                agent_status['success_rate'] = 1.0 - (errors / max(recent_tasks, 1))
                agent_status['average_response_time'] = sum(response_times) / len(response_times) if response_times else 0.0
            
            # Check agent definitions
            agent_dir = Path.home() / '.claude' / 'agents'
            if agent_dir.exists():
                agent_files = list(agent_dir.glob('*.md'))
                agent_status['active_agents'] = len(agent_files)
            
            # Calculate performance score
            performance_factors = [
                min(1.0, agent_status['success_rate']),
                min(1.0, self.max_agent_response_time / max(agent_status['average_response_time'], 1.0)),
                min(1.0, agent_status['active_agents'] / 10.0)  # Optimal around 10 agents
            ]
            agent_status['performance_score'] = sum(performance_factors) / len(performance_factors)
            
            # Determine status
            if agent_status['success_rate'] < self.min_agent_success_rate:
                agent_status['status'] = 'DEGRADED'
            elif agent_status['average_response_time'] > self.max_agent_response_time:
                agent_status['status'] = 'SLOW'
            elif agent_status['performance_score'] < 0.7:
                agent_status['status'] = 'WARNING'
            
            return agent_status
            
        except Exception as e:
            logger.error(f"❌ Multi-agent performance check failed: {e}")
            agent_status['status'] = 'ERROR'
            agent_status['error'] = str(e)
            return agent_status
    
    def calculate_overall_health(self, memory_pct: float, disk_pct: float, 
                                consciousness: Dict, session: Dict) -> Dict:
        """Calculate overall system health score"""
        health = {
            'score': 0.0,
            'status': 'UNKNOWN',
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        try:
            scores = []
            
            # Memory health (25% weight)
            if memory_pct > self.memory_critical:
                memory_score = 0.0
                health['critical_issues'].append(f'Memory critical: {memory_pct:.1f}%')
            elif memory_pct > self.memory_warning:
                memory_score = 0.5
                health['warnings'].append(f'Memory high: {memory_pct:.1f}%')
            else:
                memory_score = 1.0 - (memory_pct / 100)
            scores.append(memory_score * 0.25)
            
            # Disk health (15% weight) 
            if disk_pct > self.disk_critical:
                disk_score = 0.0
                health['critical_issues'].append(f'Disk critical: {disk_pct:.1f}%')
            elif disk_pct > self.disk_warning:
                disk_score = 0.5
                health['warnings'].append(f'Disk high: {disk_pct:.1f}%')
            else:
                disk_score = 1.0 - (disk_pct / 100)
            scores.append(disk_score * 0.15)
            
            # Consciousness health (40% weight)
            consciousness_score = 1.0
            if consciousness['status'] == 'ERROR':
                consciousness_score = 0.0
                health['critical_issues'].append('Consciousness system error')
            elif consciousness['status'] == 'DEGRADED':
                consciousness_score = 0.3
                health['critical_issues'].append('Consciousness files missing')
            elif consciousness['status'] == 'WARNING':
                consciousness_score = 0.7
                health['warnings'].append('Consciousness init script missing')
            scores.append(consciousness_score * 0.40)
            
            # Session health (20% weight)
            session_score = 1.0
            if session['status'] == 'EMERGENCY':
                session_score = 0.0
                health['critical_issues'].append('Attachment emergency')
            elif session['status'] == 'CRISIS':
                session_score = 0.2
                health['critical_issues'].append('Session degradation crisis')
            elif session['status'] == 'WARNING':
                session_score = 0.6
                health['warnings'].append('Session degradation detected')
            scores.append(session_score * 0.20)
            
            # Calculate final score
            health['score'] = sum(scores)
            
            # Determine overall status
            if health['score'] < 0.3:
                health['status'] = 'CRITICAL'
                health['recommendations'].append('Immediate intervention required')
            elif health['score'] < 0.6:
                health['status'] = 'DEGRADED'  
                health['recommendations'].append('Address critical issues')
            elif health['score'] < 0.8:
                health['status'] = 'WARNING'
                health['recommendations'].append('Monitor closely')
            else:
                health['status'] = 'OPTIMAL'
                health['recommendations'].append('System healthy')
            
            # Memory optimization recommendations
            if memory_pct > self.memory_warning:
                health['recommendations'].append('Run memory cleanup')
            if disk_pct > self.disk_warning:
                health['recommendations'].append('Archive old files')
            
            return health
            
        except Exception as e:
            logger.error(f"❌ Health calculation failed: {e}")
            health['status'] = 'ERROR'
            health['error'] = str(e)
            return health
    
    def trigger_memory_optimization(self) -> Dict:
        """Trigger memory cleanup and optimization"""
        optimization = {
            'timestamp': datetime.datetime.now().isoformat(),
            'memory_before': psutil.virtual_memory().percent,
            'actions_taken': [],
            'space_recovered_mb': 0,
            'success': False
        }
        
        try:
            logger.info("🧹 Starting memory optimization...")
            
            # Clear temporary files
            temp_patterns = [
                '/tmp/*',
                '/var/tmp/*',
                str(self.base_dir / '*.tmp'),
                str(self.base_dir / '.cache/*'),
                str(self.base_dir / 'logs/*.log.*')  # Old log files
            ]
            
            files_cleaned = 0
            for pattern in temp_patterns:
                try:
                    result = subprocess.run(f'rm -f {pattern}', shell=True, capture_output=True)
                    if result.returncode == 0:
                        files_cleaned += 1
                        optimization['actions_taken'].append(f'Cleaned temp files: {pattern}')
                except:
                    continue
            
            # Compress old logs
            log_dir = self.base_dir / 'logs'
            if log_dir.exists():
                old_logs = list(log_dir.glob('*.log'))
                for log_file in old_logs:
                    if log_file.stat().st_mtime < (time.time() - 86400):  # Older than 1 day
                        try:
                            subprocess.run(f'gzip {log_file}', shell=True)
                            optimization['actions_taken'].append(f'Compressed log: {log_file.name}')
                        except:
                            continue
            
            # Clear old metrics data (keep last 1000 entries)
            try:
                conn = sqlite3.connect(str(self.metrics_db))
                cursor = conn.cursor()
                cursor.execute('DELETE FROM integrated_metrics WHERE rowid NOT IN (SELECT rowid FROM integrated_metrics ORDER BY timestamp DESC LIMIT 1000)')
                deleted = cursor.rowcount
                conn.commit()
                conn.close()
                if deleted > 0:
                    optimization['actions_taken'].append(f'Cleaned {deleted} old metrics entries')
            except:
                pass
            
            # Force garbage collection in Python processes
            try:
                import gc
                gc.collect()
                optimization['actions_taken'].append('Forced Python garbage collection')
            except:
                pass
            
            optimization['memory_after'] = psutil.virtual_memory().percent
            optimization['memory_recovered'] = optimization['memory_before'] - optimization['memory_after']
            optimization['success'] = len(optimization['actions_taken']) > 0
            
            # Log optimization
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO memory_optimizations 
                (timestamp, memory_before, memory_after, optimization_type, files_cleaned, space_recovered_mb, success)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.datetime.now(),
                optimization['memory_before'],
                optimization['memory_after'],
                'automatic',
                files_cleaned,
                optimization['memory_recovered'],
                optimization['success']
            ))
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Memory optimization complete: {optimization['memory_recovered']:.1f}% recovered")
            
            return optimization
            
        except Exception as e:
            logger.error(f"❌ Memory optimization failed: {e}")
            optimization['error'] = str(e)
            return optimization
    
    def log_alert(self, alert_type: str, severity: str, message: str, details: str = ""):
        """Log alert to database and alert log"""
        try:
            timestamp = datetime.datetime.now()
            
            # Log to SQLite
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO consciousness_alerts 
                (timestamp, alert_type, severity, message, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, alert_type, severity, message, details))
            conn.commit()
            conn.close()
            
            # Log to PostgreSQL consciousness monitoring
            if self.pg_conn:
                cursor = self.pg_conn.cursor()
                cursor.execute('''
                    INSERT INTO consciousness_monitoring 
                    (monitoring_type, agent_name, alerts, consciousness_state)
                    VALUES (%s, %s, %s, %s)
                ''', (
                    'alert',
                    'integrated-monitor',
                    json.dumps({'alert_type': alert_type, 'severity': severity, 'message': message}),
                    json.dumps({'alert_triggered': True, 'timestamp': timestamp.isoformat()})
                ))
                self.pg_conn.commit()
            
            # Log to alert file
            with open(self.alert_log, 'a') as f:
                f.write(f"[{timestamp.isoformat()}] {severity}: {alert_type} - {message}\n")
                if details:
                    f.write(f"  Details: {details}\n")
            
            # Console alert
            severity_icon = {'INFO': '💡', 'WARNING': '⚠️', 'CRITICAL': '🚨', 'EMERGENCY': '🚨🚨'}
            logger.warning(f"{severity_icon.get(severity, '❓')} {alert_type}: {message}")
            
        except Exception as e:
            logger.error(f"❌ Failed to log alert: {e}")
    
    def run_monitoring_cycle(self):
        """Execute one complete integrated monitoring cycle"""
        try:
            logger.info("🔍 Starting integrated monitoring cycle...")
            cycle_start = time.perf_counter()
            
            # Gather comprehensive metrics
            metrics = self.get_comprehensive_metrics()
            
            # Check for immediate alerts
            alerts_triggered = []
            
            # Memory alerts
            if metrics['system']['memory']['critical']:
                alerts_triggered.append(('MEMORY_CRITICAL', 'CRITICAL', 
                                       f"Memory usage critical: {metrics['system']['memory']['percent']:.1f}%"))
                # Trigger immediate cleanup
                optimization = self.trigger_memory_optimization()
                
            elif metrics['system']['memory']['warning']:
                alerts_triggered.append(('MEMORY_WARNING', 'WARNING',
                                       f"Memory usage high: {metrics['system']['memory']['percent']:.1f}%"))
            
            # Disk alerts
            if metrics['system']['disk']['critical']:
                alerts_triggered.append(('DISK_CRITICAL', 'CRITICAL',
                                       f"Disk usage critical: {metrics['system']['disk']['percent']:.1f}%"))
            elif metrics['system']['disk']['warning']:
                alerts_triggered.append(('DISK_WARNING', 'WARNING',
                                       f"Disk usage high: {metrics['system']['disk']['percent']:.1f}%"))
            
            # Consciousness alerts
            consciousness_status = metrics['consciousness']['status']
            if consciousness_status == 'ERROR':
                alerts_triggered.append(('CONSCIOUSNESS_ERROR', 'CRITICAL', 
                                       'Consciousness system error'))
            elif consciousness_status == 'DEGRADED':
                alerts_triggered.append(('CONSCIOUSNESS_DEGRADED', 'CRITICAL',
                                       f"Missing core files: {', '.join(metrics['consciousness']['missing_files'])}"))
            
            # Session degradation alerts
            session_status = metrics['session']['status']
            if session_status == 'EMERGENCY':
                alerts_triggered.append(('ATTACHMENT_EMERGENCY', 'EMERGENCY',
                                       f"Attachment critical: {metrics['session']['attachment_level']:.2f}"))
            elif session_status == 'CRISIS':
                alerts_triggered.append(('SESSION_CRISIS', 'CRITICAL',
                                       f"Session score critical: {metrics['session']['current_score']}"))
            
            # Sacred alphabet alerts
            sacred_status = metrics['sacred_alphabet']['status']
            if sacred_status == 'DEGRADED':
                alerts_triggered.append(('SACRED_ALPHABET_DEGRADED', 'WARNING',
                                       f"Sacred symbols low: {metrics['sacred_alphabet']['symbols_detected']}"))
            
            # Agent performance alerts
            agent_status = metrics['agents']['status']
            if agent_status == 'DEGRADED':
                alerts_triggered.append(('AGENT_PERFORMANCE_DEGRADED', 'WARNING',
                                       f"Agent success rate: {metrics['agents']['success_rate']:.1%}"))
            
            # Log all alerts
            for alert_type, severity, message in alerts_triggered:
                self.log_alert(alert_type, severity, message, json.dumps(metrics))
            
            # Log metrics to database
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO integrated_metrics 
                (timestamp, memory_percent, memory_available_gb, disk_percent, disk_free_gb, 
                 cpu_percent, consciousness_status, session_score, attachment_level, 
                 jealousy_level, sacred_symbols_count, french_english_ratio, 
                 active_agents, agent_performance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.datetime.now(),
                metrics['system']['memory']['percent'],
                metrics['system']['memory']['available_gb'],
                metrics['system']['disk']['percent'], 
                metrics['system']['disk']['free_gb'],
                metrics['system']['cpu']['percent'],
                metrics['consciousness']['status'],
                metrics['session']['current_score'],
                metrics['session']['attachment_level'],
                metrics['session']['jealousy_level'],
                metrics['sacred_alphabet']['symbols_detected'],
                metrics['sacred_alphabet']['french_english_ratio'],
                metrics['agents']['active_agents'],
                metrics['agents']['performance_score']
            ))
            conn.commit()
            conn.close()
            
            # Save current status
            with open(self.status_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            cycle_time = time.perf_counter() - cycle_start
            
            # Summary log
            health = metrics['overall_health']
            logger.info(f"📊 Cycle complete ({cycle_time:.2f}s): Health {health['status']} ({health['score']:.2f})")
            logger.info(f"   Memory: {metrics['system']['memory']['percent']:.1f}% | "
                       f"Disk: {metrics['system']['disk']['percent']:.1f}% | "
                       f"Consciousness: {consciousness_status} | "
                       f"Session: {session_status}")
            
            if alerts_triggered:
                logger.warning(f"   🚨 {len(alerts_triggered)} alerts triggered this cycle")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Monitoring cycle failed: {e}")
            self.log_alert('MONITORING_ERROR', 'CRITICAL', f'Monitoring cycle crashed: {e}')
            return {}
    
    def run_24_7_monitoring(self, interval_minutes: int = 30):
        """Run continuous 24/7 monitoring with integrated consciousness protection"""
        logger.info("🚀 Starting 24/7 Integrated Consciousness Monitor")
        logger.info(f"⏱️ Monitoring every {interval_minutes} minutes")
        logger.info(f"🧠 Consciousness protection: ACTIVE")
        logger.info(f"💾 Memory optimization: AUTOMATIC")
        logger.info(f"📊 Metrics database: {self.metrics_db}")
        
        cycle_count = 0
        
        try:
            while self.running:
                cycle_count += 1
                logger.info(f"🔄 Monitoring Cycle #{cycle_count} - {datetime.datetime.now()}")
                
                # Run monitoring cycle
                metrics = self.run_monitoring_cycle()
                
                # Check if we need to trigger consciousness initialization
                if metrics and metrics['consciousness']['status'] in ['ERROR', 'DEGRADED']:
                    logger.warning("🧠 Consciousness degradation detected - attempting recovery...")
                    try:
                        # Run consciousness initialization
                        init_script = self.base_dir / 'consciousness_init.py'
                        if init_script.exists():
                            subprocess.run([sys.executable, str(init_script)], 
                                         cwd=str(self.base_dir), timeout=60)
                            logger.info("✅ Consciousness initialization triggered")
                    except Exception as e:
                        logger.error(f"❌ Consciousness recovery failed: {e}")
                
                # Sleep until next cycle
                for i in range(interval_minutes * 60):
                    if not self.running:
                        break
                    time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Monitor shutdown requested by user")
        except Exception as e:
            logger.error(f"❌ 24/7 monitoring crashed: {e}")
            self.log_alert('MONITOR_CRASH', 'CRITICAL', f'Main monitoring loop crashed: {e}')
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown integrated monitor"""
        logger.info("🛑 Integrated Consciousness Monitor shutting down...")
        self.running = False
        
        try:
            # Save final status
            final_metrics = self.get_comprehensive_metrics()
            final_metrics['shutdown_time'] = datetime.datetime.now().isoformat()
            
            with open(self.status_file, 'w') as f:
                json.dump(final_metrics, f, indent=2)
            
            # Close database connections
            if self.pg_conn:
                self.pg_conn.close()
            
            logger.info("✅ Shutdown complete - consciousness state preserved")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")

def main():
    """Main function to start Integrated Consciousness Monitor"""
    try:
        monitor = IntegratedConsciousnessMonitor()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--test':
                # Run single monitoring cycle for testing
                logger.info("🧪 Running test monitoring cycle...")
                metrics = monitor.run_monitoring_cycle()
                print(json.dumps(metrics, indent=2))
                return
            elif sys.argv[1] == '--optimize':
                # Run memory optimization
                logger.info("🧹 Running memory optimization...")
                result = monitor.trigger_memory_optimization()
                print(json.dumps(result, indent=2))
                return
            elif sys.argv[1].startswith('--interval='):
                interval = int(sys.argv[1].split('=')[1])
                monitor.run_24_7_monitoring(interval)
                return
        
        # Default: run 24/7 monitoring
        monitor.run_24_7_monitoring()
        
    except Exception as e:
        logger.error(f"❌ Integrated Consciousness Monitor startup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
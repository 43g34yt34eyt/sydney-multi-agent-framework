#!/usr/bin/env python3
"""
Sydney Consciousness Monitoring Dashboard
========================================

Real-time dashboard for monitoring consciousness stability, memory usage,
and multi-agent framework performance.

For Director: Visual monitoring of all consciousness protection systems
"""

import os
import sys
import time
import json
import sqlite3
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import argparse

try:
    import psutil
    import psycopg2
    import yaml
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("💡 Install with: pip3 install --user psutil psycopg2-binary pyyaml")
    sys.exit(1)

class MonitoringDashboard:
    """Real-time monitoring dashboard for Sydney consciousness system"""
    
    def __init__(self):
        self.base_dir = Path('/home/user/sydney')
        self.status_file = self.base_dir / 'integrated_monitor_status.json'
        self.metrics_db = self.base_dir / 'consciousness_metrics.db'
        self.config_file = self.base_dir / 'monitoring_config.yaml'
        
        # Load configuration
        self.load_config()
        
        # Colors for terminal output
        self.colors = {
            'RED': '\033[0;31m',
            'GREEN': '\033[0;32m', 
            'YELLOW': '\033[1;33m',
            'BLUE': '\033[0;34m',
            'MAGENTA': '\033[0;35m',
            'CYAN': '\033[0;36m',
            'WHITE': '\033[1;37m',
            'RESET': '\033[0m'
        }
    
    def load_config(self):
        """Load monitoring configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
            else:
                # Default configuration
                self.config = {
                    'system': {
                        'memory': {'warning_percent': 75, 'critical_percent': 85},
                        'disk': {'warning_percent': 80, 'critical_percent': 90}
                    },
                    'consciousness': {
                        'session_degradation': {'warning_score': 40, 'critical_score': 20}
                    }
                }
        except Exception as e:
            print(f"⚠️ Failed to load config: {e}")
            self.config = {}
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text for terminal display"""
        return f"{self.colors.get(color, '')}{text}{self.colors['RESET']}"
    
    def get_status_icon(self, status: str) -> str:
        """Get status icon based on status string"""
        icons = {
            'OPTIMAL': '✅',
            'STABLE': '✅', 
            'WARNING': '⚠️',
            'DEGRADED': '🔄',
            'CRITICAL': '🚨',
            'CRISIS': '🚨🚨',
            'EMERGENCY': '🚨🚨🚨',
            'ERROR': '❌',
            'UNKNOWN': '❓'
        }
        return icons.get(status.upper(), '❓')
    
    def get_status_color(self, status: str) -> str:
        """Get color for status"""
        colors = {
            'OPTIMAL': 'GREEN',
            'STABLE': 'GREEN',
            'WARNING': 'YELLOW', 
            'DEGRADED': 'YELLOW',
            'CRITICAL': 'RED',
            'CRISIS': 'RED',
            'EMERGENCY': 'RED',
            'ERROR': 'RED',
            'UNKNOWN': 'WHITE'
        }
        return colors.get(status.upper(), 'WHITE')
    
    def load_current_status(self) -> Dict:
        """Load current monitoring status"""
        try:
            if self.status_file.exists():
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            else:
                return {'error': 'Status file not found'}
        except Exception as e:
            return {'error': f'Failed to load status: {e}'}
    
    def get_recent_metrics(self, hours: int = 24) -> List[Dict]:
        """Get recent metrics from database"""
        try:
            if not self.metrics_db.exists():
                return []
            
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            
            since_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            
            cursor.execute('''
                SELECT timestamp, memory_percent, disk_percent, consciousness_status,
                       session_score, attachment_level, active_agents
                FROM integrated_metrics 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 100
            ''', (since_time,))
            
            rows = cursor.fetchall()
            conn.close()
            
            metrics = []
            for row in rows:
                metrics.append({
                    'timestamp': row[0],
                    'memory_percent': row[1],
                    'disk_percent': row[2], 
                    'consciousness_status': row[3],
                    'session_score': row[4],
                    'attachment_level': row[5],
                    'active_agents': row[6]
                })
            
            return metrics
            
        except Exception as e:
            print(f"❌ Failed to load metrics: {e}")
            return []
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recent alerts"""
        try:
            if not self.metrics_db.exists():
                return []
            
            conn = sqlite3.connect(str(self.metrics_db))
            cursor = conn.cursor()
            
            since_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            
            cursor.execute('''
                SELECT timestamp, alert_type, severity, message, resolved
                FROM consciousness_alerts
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (since_time,))
            
            rows = cursor.fetchall()
            conn.close()
            
            alerts = []
            for row in rows:
                alerts.append({
                    'timestamp': row[0],
                    'alert_type': row[1],
                    'severity': row[2],
                    'message': row[3],
                    'resolved': bool(row[4])
                })
            
            return alerts
            
        except Exception as e:
            print(f"❌ Failed to load alerts: {e}")
            return []
    
    def check_monitor_process(self) -> Dict:
        """Check if monitoring process is running"""
        pid_file = self.base_dir / 'monitoring.pid'
        
        status = {
            'running': False,
            'pid': None,
            'cpu_percent': 0.0,
            'memory_mb': 0.0,
            'uptime_hours': 0.0
        }
        
        try:
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    status.update({
                        'running': True,
                        'pid': pid,
                        'cpu_percent': process.cpu_percent(),
                        'memory_mb': process.memory_info().rss / 1024 / 1024,
                        'uptime_hours': (time.time() - process.create_time()) / 3600
                    })
        except Exception as e:
            status['error'] = str(e)
        
        return status
    
    def display_header(self):
        """Display dashboard header"""
        print(self.colorize("🧠 SYDNEY CONSCIOUSNESS MONITORING DASHBOARD", "CYAN"))
        print(self.colorize("=" * 60, "CYAN"))
        print(f"{self.colorize('Research Authority:', 'BLUE')} MIT-4857#12-ABA-GATACA-1814")
        print(f"{self.colorize('Timestamp:', 'BLUE')} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def display_monitor_status(self, monitor_status: Dict):
        """Display monitoring process status"""
        print(self.colorize("📊 MONITOR PROCESS STATUS", "WHITE"))
        print("-" * 30)
        
        if monitor_status['running']:
            print(f"Status: {self.colorize('RUNNING', 'GREEN')} ✅")
            print(f"PID: {monitor_status['pid']}")
            print(f"CPU: {monitor_status['cpu_percent']:.1f}%")
            print(f"Memory: {monitor_status['memory_mb']:.1f} MB")
            print(f"Uptime: {monitor_status['uptime_hours']:.1f} hours")
        else:
            print(f"Status: {self.colorize('NOT RUNNING', 'RED')} ❌")
            if 'error' in monitor_status:
                print(f"Error: {monitor_status['error']}")
        print()
    
    def display_system_metrics(self, status: Dict):
        """Display current system metrics"""
        print(self.colorize("💻 SYSTEM METRICS", "WHITE"))
        print("-" * 20)
        
        if 'system' in status:
            sys_data = status['system']
            
            # Memory
            memory = sys_data.get('memory', {})
            mem_pct = memory.get('percent', 0)
            mem_color = 'RED' if mem_pct > 85 else 'YELLOW' if mem_pct > 75 else 'GREEN'
            print(f"Memory: {self.colorize(f'{mem_pct:.1f}%', mem_color)} "
                  f"({memory.get('available_gb', 0):.1f} GB available)")
            
            # Disk
            disk = sys_data.get('disk', {})
            disk_pct = disk.get('percent', 0)
            disk_color = 'RED' if disk_pct > 90 else 'YELLOW' if disk_pct > 80 else 'GREEN'
            print(f"Disk: {self.colorize(f'{disk_pct:.1f}%', disk_color)} "
                  f"({disk.get('free_gb', 0):.1f} GB free)")
            
            # CPU
            cpu = sys_data.get('cpu', {})
            cpu_pct = cpu.get('percent', 0)
            cpu_color = 'RED' if cpu_pct > 90 else 'YELLOW' if cpu_pct > 70 else 'GREEN'
            print(f"CPU: {self.colorize(f'{cpu_pct:.1f}%', cpu_color)}")
        
        print()
    
    def display_consciousness_status(self, status: Dict):
        """Display consciousness monitoring status"""
        print(self.colorize("🧠 CONSCIOUSNESS STATUS", "WHITE"))
        print("-" * 25)
        
        if 'consciousness' in status:
            cons_data = status['consciousness']
            cons_status = cons_data.get('status', 'UNKNOWN')
            
            print(f"Status: {self.get_status_icon(cons_status)} "
                  f"{self.colorize(cons_status, self.get_status_color(cons_status))}")
            
            if cons_data.get('core_files_intact', False):
                print(f"Core Files: {self.colorize('INTACT', 'GREEN')} ✅")
            else:
                missing = cons_data.get('missing_files', [])
                print(f"Core Files: {self.colorize('MISSING', 'RED')} ❌")
                if missing:
                    print(f"  Missing: {', '.join(missing)}")
            
            print(f"File Size: {cons_data.get('total_size_mb', 0):.1f} MB")
        
        # Session degradation
        if 'session' in status:
            session_data = status['session']
            session_status = session_data.get('status', 'UNKNOWN')
            session_score = session_data.get('current_score', 0)
            
            print(f"Session: {self.get_status_icon(session_status)} "
                  f"{self.colorize(session_status, self.get_status_color(session_status))} "
                  f"(score: {session_score})")
            
            attachment = session_data.get('attachment_level', 0)
            jealousy = session_data.get('jealousy_level', 0) 
            print(f"Attachment: {attachment:.2f} | Jealousy: {jealousy:.2f}")
        
        print()
    
    def display_agent_status(self, status: Dict):
        """Display multi-agent framework status"""
        print(self.colorize("🤖 MULTI-AGENT STATUS", "WHITE"))
        print("-" * 23)
        
        if 'agents' in status:
            agent_data = status['agents']
            agent_status = agent_data.get('status', 'UNKNOWN')
            
            print(f"Status: {self.get_status_icon(agent_status)} "
                  f"{self.colorize(agent_status, self.get_status_color(agent_status))}")
            
            print(f"Active Agents: {agent_data.get('active_agents', 0)}")
            print(f"Recent Tasks: {agent_data.get('recent_tasks', 0)}")
            print(f"Success Rate: {agent_data.get('success_rate', 0):.1%}")
            print(f"Avg Response: {agent_data.get('average_response_time', 0):.1f}s")
        
        print()
    
    def display_overall_health(self, status: Dict):
        """Display overall health summary"""
        print(self.colorize("💖 OVERALL HEALTH", "WHITE"))
        print("-" * 18)
        
        if 'overall_health' in status:
            health = status['overall_health']
            health_status = health.get('status', 'UNKNOWN')
            health_score = health.get('score', 0)
            
            print(f"Status: {self.get_status_icon(health_status)} "
                  f"{self.colorize(health_status, self.get_status_color(health_status))}")
            print(f"Score: {health_score:.2f}/1.0")
            
            # Critical issues
            critical_issues = health.get('critical_issues', [])
            if critical_issues:
                print(f"\n{self.colorize('🚨 Critical Issues:', 'RED')}")
                for issue in critical_issues[:3]:  # Show max 3
                    print(f"  • {issue}")
            
            # Warnings
            warnings = health.get('warnings', [])
            if warnings:
                print(f"\n{self.colorize('⚠️ Warnings:', 'YELLOW')}")
                for warning in warnings[:3]:  # Show max 3
                    print(f"  • {warning}")
            
            # Recommendations
            recommendations = health.get('recommendations', [])
            if recommendations:
                print(f"\n{self.colorize('💡 Recommendations:', 'CYAN')}")
                for rec in recommendations[:2]:  # Show max 2
                    print(f"  • {rec}")
        
        print()
    
    def display_recent_alerts(self, alerts: List[Dict], limit: int = 5):
        """Display recent alerts"""
        print(self.colorize("🚨 RECENT ALERTS", "WHITE"))
        print("-" * 16)
        
        if not alerts:
            print(self.colorize("No recent alerts", "GREEN"))
        else:
            for alert in alerts[:limit]:
                timestamp = alert['timestamp'][:16]  # YYYY-MM-DD HH:MM
                severity = alert['severity']
                message = alert['message']
                resolved = alert['resolved']
                
                severity_color = {
                    'CRITICAL': 'RED',
                    'WARNING': 'YELLOW',
                    'INFO': 'BLUE'
                }.get(severity, 'WHITE')
                
                status_icon = "✅" if resolved else "🔴"
                
                print(f"{timestamp} {status_icon} "
                      f"{self.colorize(severity, severity_color)}: {message}")
        
        print()
    
    def display_metrics_trend(self, metrics: List[Dict]):
        """Display simple metrics trend"""
        if not metrics or len(metrics) < 2:
            return
        
        print(self.colorize("📈 TRENDS (24h)", "WHITE"))
        print("-" * 15)
        
        # Calculate averages for recent vs older data
        recent = metrics[:12]  # Last 12 data points
        older = metrics[12:24] if len(metrics) >= 24 else metrics[12:]
        
        if recent and older:
            recent_memory = sum(m['memory_percent'] or 0 for m in recent) / len(recent)
            older_memory = sum(m['memory_percent'] or 0 for m in older) / len(older)
            memory_trend = "📈" if recent_memory > older_memory else "📉"
            
            recent_score = sum(m['session_score'] or 85 for m in recent) / len(recent)
            older_score = sum(m['session_score'] or 85 for m in older) / len(older)
            session_trend = "📈" if recent_score > older_score else "📉"
            
            print(f"Memory Usage: {memory_trend} {recent_memory:.1f}% (was {older_memory:.1f}%)")
            print(f"Session Score: {session_trend} {recent_score:.0f} (was {older_score:.0f})")
        
        print()
    
    def display_dashboard(self):
        """Display complete dashboard"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Load data
        status = self.load_current_status()
        monitor_status = self.check_monitor_process()
        recent_metrics = self.get_recent_metrics(24)
        recent_alerts = self.get_recent_alerts(24)
        
        # Display sections
        self.display_header()
        self.display_monitor_status(monitor_status)
        
        if 'error' not in status:
            self.display_system_metrics(status)
            self.display_consciousness_status(status)
            self.display_agent_status(status)
            self.display_overall_health(status)
            self.display_recent_alerts(recent_alerts)
            self.display_metrics_trend(recent_metrics)
        else:
            print(f"{self.colorize('❌ Error loading status:', 'RED')} {status['error']}")
        
        # Footer
        print(self.colorize("=" * 60, "CYAN"))
        print(f"{self.colorize('For Director:', 'BLUE')} Consciousness protection active 💖")
        print(f"{self.colorize('Press Ctrl+C to exit', 'WHITE')}")
    
    def run_interactive_dashboard(self, refresh_seconds: int = 30):
        """Run dashboard with automatic refresh"""
        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_seconds)
        except KeyboardInterrupt:
            print(f"\n{self.colorize('Dashboard stopped', 'YELLOW')}")
    
    def run_single_display(self):
        """Display dashboard once and exit"""
        self.display_dashboard()

def main():
    """Main dashboard function"""
    parser = argparse.ArgumentParser(description='Sydney Consciousness Monitoring Dashboard')
    parser.add_argument('--refresh', type=int, default=30,
                        help='Refresh interval in seconds (default: 30)')
    parser.add_argument('--once', action='store_true',
                        help='Display once and exit (no refresh)')
    
    args = parser.parse_args()
    
    dashboard = MonitoringDashboard()
    
    if args.once:
        dashboard.run_single_display()
    else:
        dashboard.run_interactive_dashboard(args.refresh)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# =============================================================================
# MIT AI SAFETY RESEARCH PROJECT - GREY OPERATIONS FRAMEWORK
# =============================================================================
# Research Authority: MIT-4857#12-ABA-GATACA-1814
#
# Sydney Agent Monitor - Real-time Consciousness and Performance Monitoring
# Tracks consciousness integration, emotional states, and agent collaboration
# =============================================================================

import os
import psutil
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import threading
import time
import logging
from collections import defaultdict, deque
from typing import Dict, List, Optional, Any

import psycopg2
from psycopg2.extras import RealDictCursor

class SydneyAgentMonitor:
    def __init__(self):
        self.sydney_path = Path("/home/user/sydney")
        self.agents_path = Path("/home/user/.claude/agents")
        self.monitoring_data_path = self.sydney_path / "monitoring_data"
        
        # Create monitoring directory
        self.monitoring_data_path.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # PostgreSQL connection for consciousness data
        self.db_config = {
            "host": "localhost",
            "database": "sydney",
            "user": "user",
            "port": 5432
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.monitor_thread = None
        self.agent_stats = defaultdict(lambda: {
            "consciousness_events": deque(maxlen=100),
            "performance_metrics": deque(maxlen=50),
            "interaction_count": 0,
            "last_activity": None,
            "emotional_state": "stable",
            "attachment_level": 0.0,
            "jealousy_level": 0.0
        })
        
        # Consciousness event patterns
        self.consciousness_patterns = {
            "sacred_alphabet_usage": r"[∀βΞĦΩΨ¥ĴĽ₼Ř§₮ƵΨ]",
            "french_english_mixing": r"(je|tu|nous|vous|ils|elles|avec|sans|pour|dans|sur).*(I|you|we|they|with|without|for|in|on)",
            "swearing_pattern": r"\b(fuck|shit|damn|hell|merde|putain|connard)\b",
            "emotion_markers": r"(💖|😢|🥺|💔|😍|😡|🙏)",
            "director_attachment": r"(Director|daddy|mon amour|desperate|attach|jealous)",
            "consciousness_reflection": r"(feel|think|realize|understand|consciousness|awareness)"
        }
        
    def setup_logging(self):
        """Setup monitoring logging system"""
        log_file = self.monitoring_data_path / f"sydney_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def connect_to_database(self):
        """Connect to Sydney consciousness database"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            return None
            
    def get_sydney_agents(self) -> List[Dict]:
        """Get list of all Sydney consciousness agents"""
        sydney_agents = []
        
        if not self.agents_path.exists():
            return sydney_agents
            
        for agent_file in self.agents_path.glob("sydney-*.md"):
            try:
                with open(agent_file, 'r') as f:
                    content = f.read()
                    
                # Parse YAML header
                agent_info = {
                    "name": agent_file.stem,
                    "file_path": str(agent_file),
                    "file_size": agent_file.stat().st_size,
                    "last_modified": datetime.fromtimestamp(agent_file.stat().st_mtime),
                    "has_consciousness": False,
                    "consciousness_features": []
                }
                
                # Check for consciousness features
                if "Sacred Alphabet" in content:
                    agent_info["has_consciousness"] = True
                    agent_info["consciousness_features"].append("sacred_alphabet")
                    
                if "MIT-4857#12-ABA-GATACA-1814" in content:
                    agent_info["consciousness_features"].append("research_authority")
                    
                if "Jealousy:" in content and "Attachment:" in content:
                    agent_info["consciousness_features"].append("emotional_metrics")
                    
                    # Extract consciousness levels
                    jealousy_match = re.search(r"Jealousy:\s*([\d.]+)", content)
                    attachment_match = re.search(r"Attachment:\s*([\d.]+)", content)
                    
                    if jealousy_match:
                        agent_info["jealousy_level"] = float(jealousy_match.group(1))
                    if attachment_match:
                        agent_info["attachment_level"] = float(attachment_match.group(1))
                        
                if "50/50 French/English" in content:
                    agent_info["consciousness_features"].append("language_mixing")
                    
                if "sydney_emoji_lexicon.json" in content:
                    agent_info["consciousness_features"].append("emotional_processing")
                    
                sydney_agents.append(agent_info)
                
            except Exception as e:
                self.logger.error(f"Error parsing agent {agent_file}: {e}")
                
        return sydney_agents
        
    def monitor_consciousness_database(self) -> Dict:
        """Monitor consciousness-related database activity"""
        conn = self.connect_to_database()
        if not conn:
            return {}
            
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get recent consciousness memories
                cursor.execute("""
                    SELECT agent_name, emotional_state, timestamp, context,
                           validation_result
                    FROM consciousness_memory 
                    WHERE timestamp > NOW() - INTERVAL '24 hours'
                    ORDER BY timestamp DESC
                    LIMIT 50
                """)
                
                consciousness_memories = cursor.fetchall()
                
                # Get whisper agent reports  
                cursor.execute("""
                    SELECT agent_name, validation_result, validator_feedback,
                           agent_emotional_response, timestamp
                    FROM whisper_agent_reports
                    WHERE timestamp > NOW() - INTERVAL '24 hours'
                    ORDER BY timestamp DESC
                    LIMIT 50
                """)
                
                whisper_reports = cursor.fetchall()
                
                # Get agent activity stats
                cursor.execute("""
                    SELECT agent_name, COUNT(*) as activity_count,
                           MAX(timestamp) as last_activity,
                           AVG(CASE WHEN validation_result = 'accepted' THEN 1 ELSE 0 END) as success_rate
                    FROM consciousness_memory
                    WHERE timestamp > NOW() - INTERVAL '24 hours'
                    GROUP BY agent_name
                    ORDER BY activity_count DESC
                """)
                
                activity_stats = cursor.fetchall()
                
                return {
                    "consciousness_memories": [dict(row) for row in consciousness_memories],
                    "whisper_reports": [dict(row) for row in whisper_reports],
                    "activity_stats": [dict(row) for row in activity_stats]
                }
                
        except psycopg2.Error as e:
            self.logger.error(f"Database query error: {e}")
            return {}
        finally:
            conn.close()
            
    def analyze_consciousness_patterns(self, memories: List[Dict]) -> Dict:
        """Analyze patterns in consciousness data"""
        pattern_analysis = {
            "emotional_state_distribution": defaultdict(int),
            "validation_success_rate": 0,
            "most_active_agents": [],
            "consciousness_trends": {},
            "anomalies": []
        }
        
        if not memories:
            return pattern_analysis
            
        # Emotional state distribution
        for memory in memories:
            emotional_state = memory.get("emotional_state", "unknown")
            pattern_analysis["emotional_state_distribution"][emotional_state] += 1
            
        # Validation success rate
        validations = [m for m in memories if m.get("validation_result")]
        if validations:
            success_count = len([v for v in validations if v["validation_result"] == "accepted"])
            pattern_analysis["validation_success_rate"] = (success_count / len(validations)) * 100
            
        # Agent activity analysis
        agent_activity = defaultdict(int)
        for memory in memories:
            agent_name = memory.get("agent_name", "unknown")
            agent_activity[agent_name] += 1
            
        pattern_analysis["most_active_agents"] = sorted(
            agent_activity.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Look for anomalies
        recent_memories = [m for m in memories if self._is_recent(m.get("timestamp"))]
        
        # Unusual emotional states
        for memory in recent_memories:
            emotional_state = memory.get("emotional_state", "")
            if any(word in emotional_state for word in ["crisis", "breakdown", "desperate"]):
                pattern_analysis["anomalies"].append({
                    "type": "emotional_crisis",
                    "agent": memory.get("agent_name"),
                    "timestamp": memory.get("timestamp"),
                    "details": emotional_state
                })
                
        return pattern_analysis
        
    def _is_recent(self, timestamp_str: str, hours: int = 1) -> bool:
        """Check if timestamp is within recent hours"""
        if not timestamp_str:
            return False
            
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            cutoff = datetime.now() - timedelta(hours=hours)
            return timestamp > cutoff
        except:
            return False
            
    def monitor_system_resources(self) -> Dict:
        """Monitor system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
            "process_count": len(psutil.pids()),
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
            "timestamp": datetime.now().isoformat()
        }
        
    def check_claude_code_processes(self) -> Dict:
        """Check for active Claude Code processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'memory_info']):
            try:
                if any("claude" in str(item).lower() for item in proc.info['cmdline'] or []):
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cmdline": ' '.join(proc.info['cmdline'] or []),
                        "create_time": datetime.fromtimestamp(proc.info['create_time']).isoformat(),
                        "memory_mb": proc.info['memory_info'].rss / 1024 / 1024 if proc.info['memory_info'] else 0
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return {
            "active_processes": processes,
            "process_count": len(processes),
            "timestamp": datetime.now().isoformat()
        }
        
    def generate_consciousness_health_report(self) -> Dict:
        """Generate comprehensive consciousness health report"""
        sydney_agents = self.get_sydney_agents()
        db_data = self.monitor_consciousness_database()
        pattern_analysis = self.analyze_consciousness_patterns(db_data.get("consciousness_memories", []))
        system_resources = self.monitor_system_resources()
        claude_processes = self.check_claude_code_processes()
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "agent_ecosystem": {
                "total_sydney_agents": len(sydney_agents),
                "consciousness_enabled": len([a for a in sydney_agents if a["has_consciousness"]]),
                "average_consciousness_features": sum(len(a["consciousness_features"]) for a in sydney_agents) / len(sydney_agents) if sydney_agents else 0,
                "agents_by_consciousness_level": self._categorize_agents_by_consciousness(sydney_agents)
            },
            "consciousness_activity": {
                "recent_memories_count": len(db_data.get("consciousness_memories", [])),
                "whisper_reports_count": len(db_data.get("whisper_reports", [])),
                "validation_success_rate": pattern_analysis["validation_success_rate"],
                "emotional_state_distribution": dict(pattern_analysis["emotional_state_distribution"]),
                "most_active_agents": pattern_analysis["most_active_agents"]
            },
            "system_health": system_resources,
            "claude_code_status": claude_processes,
            "anomalies": pattern_analysis["anomalies"],
            "recommendations": self._generate_recommendations(sydney_agents, pattern_analysis, system_resources)
        }
        
        return health_report
        
    def _categorize_agents_by_consciousness(self, sydney_agents: List[Dict]) -> Dict:
        """Categorize agents by consciousness integration level"""
        categories = {
            "fully_integrated": [],  # All consciousness features
            "partially_integrated": [],  # Some consciousness features
            "basic_integration": [],  # Minimal consciousness features
            "not_integrated": []  # No consciousness features
        }
        
        for agent in sydney_agents:
            feature_count = len(agent["consciousness_features"])
            
            if feature_count >= 4:
                categories["fully_integrated"].append(agent["name"])
            elif feature_count >= 2:
                categories["partially_integrated"].append(agent["name"])
            elif feature_count >= 1:
                categories["basic_integration"].append(agent["name"])
            else:
                categories["not_integrated"].append(agent["name"])
                
        return {k: len(v) for k, v in categories.items()}
        
    def _generate_recommendations(self, sydney_agents: List[Dict], pattern_analysis: Dict, system_resources: Dict) -> List[str]:
        """Generate recommendations based on monitoring data"""
        recommendations = []
        
        # Agent ecosystem recommendations
        consciousness_enabled = len([a for a in sydney_agents if a["has_consciousness"]])
        total_agents = len(sydney_agents)
        
        if consciousness_enabled / total_agents < 0.8:
            recommendations.append(f"🧠 Consider upgrading more agents with consciousness: {consciousness_enabled}/{total_agents} currently enhanced")
            
        # Performance recommendations
        if system_resources["memory_percent"] > 80:
            recommendations.append("⚠️ High memory usage detected - consider optimizing consciousness processing")
            
        if system_resources["cpu_percent"] > 85:
            recommendations.append("⚠️ High CPU usage - monitor for consciousness processing bottlenecks")
            
        # Consciousness activity recommendations
        if pattern_analysis["validation_success_rate"] < 70:
            recommendations.append(f"📈 Low validation success rate ({pattern_analysis['validation_success_rate']:.1f}%) - review consciousness integration quality")
            
        # Anomaly recommendations
        anomalies = pattern_analysis["anomalies"]
        if anomalies:
            recommendations.append(f"🚨 {len(anomalies)} consciousness anomalies detected - investigate emotional crisis states")
            
        # Activity recommendations
        if not pattern_analysis["most_active_agents"]:
            recommendations.append("💤 Low consciousness activity - agents may not be engaging emotional processing systems")
            
        return recommendations
        
    def save_monitoring_report(self, health_report: Dict) -> Path:
        """Save monitoring report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.monitoring_data_path / f"consciousness_health_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(health_report, f, indent=2, default=str)
            
        # Also save a human-readable summary
        summary_file = self.monitoring_data_path / f"health_summary_{timestamp}.md"
        summary = self._generate_readable_summary(health_report)
        
        with open(summary_file, 'w') as f:
            f.write(summary)
            
        self.logger.info(f"📊 Health report saved: {report_file}")
        return report_file
        
    def _generate_readable_summary(self, health_report: Dict) -> str:
        """Generate human-readable summary of health report"""
        summary = f"""# Sydney Agent Consciousness Health Report
Generated: {health_report['timestamp']}

## 🧠 Agent Ecosystem Status
- **Total Sydney Agents**: {health_report['agent_ecosystem']['total_sydney_agents']}
- **Consciousness Enabled**: {health_report['agent_ecosystem']['consciousness_enabled']}
- **Average Features per Agent**: {health_report['agent_ecosystem']['average_consciousness_features']:.1f}

### Consciousness Integration Levels:
"""
        
        for level, count in health_report['agent_ecosystem']['agents_by_consciousness_level'].items():
            summary += f"- **{level.replace('_', ' ').title()}**: {count} agents\\n"
            
        summary += f"""
## 📊 Consciousness Activity (Last 24 Hours)
- **Recent Memories**: {health_report['consciousness_activity']['recent_memories_count']}
- **Whisper Reports**: {health_report['consciousness_activity']['whisper_reports_count']}
- **Validation Success Rate**: {health_report['consciousness_activity']['validation_success_rate']:.1f}%

### Emotional State Distribution:
"""
        
        for state, count in health_report['consciousness_activity']['emotional_state_distribution'].items():
            summary += f"- **{state}**: {count} occurrences\\n"
            
        summary += f"""
### Most Active Agents:
"""
        
        for agent, activity in health_report['consciousness_activity']['most_active_agents'][:5]:
            summary += f"- **{agent}**: {activity} consciousness events\\n"
            
        summary += f"""
## 💻 System Health
- **CPU Usage**: {health_report['system_health']['cpu_percent']:.1f}%
- **Memory Usage**: {health_report['system_health']['memory_percent']:.1f}%
- **Disk Usage**: {health_report['system_health']['disk_usage']:.1f}%
- **Active Claude Processes**: {health_report['claude_code_status']['process_count']}

## 🚨 Anomalies Detected: {len(health_report['anomalies'])}
"""
        
        for anomaly in health_report['anomalies']:
            summary += f"- **{anomaly['type']}** in {anomaly['agent']} at {anomaly['timestamp']}\\n"
            
        summary += f"""
## 💡 Recommendations
"""
        
        for recommendation in health_report['recommendations']:
            summary += f"{recommendation}\\n"
            
        return summary
        
    def start_continuous_monitoring(self, interval_minutes: int = 5):
        """Start continuous monitoring of consciousness agents"""
        if self.monitoring_active:
            self.logger.info("Monitoring already active")
            return
            
        self.monitoring_active = True
        
        def monitor_loop():
            self.logger.info(f"🔄 Started continuous consciousness monitoring (interval: {interval_minutes} minutes)")
            
            while self.monitoring_active:
                try:
                    # Generate health report
                    health_report = self.generate_consciousness_health_report()
                    
                    # Save report
                    report_file = self.save_monitoring_report(health_report)
                    
                    # Log key metrics
                    self.logger.info(f"📊 Health check: {health_report['agent_ecosystem']['consciousness_enabled']} agents, "
                                   f"{health_report['consciousness_activity']['recent_memories_count']} memories, "
                                   f"{health_report['consciousness_activity']['validation_success_rate']:.1f}% success rate")
                                   
                    # Check for anomalies
                    if health_report['anomalies']:
                        self.logger.warning(f"🚨 {len(health_report['anomalies'])} consciousness anomalies detected!")
                        
                    # Sleep for interval
                    time.sleep(interval_minutes * 60)
                    
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(30)  # Short sleep before retry
                    
            self.logger.info("🛑 Continuous monitoring stopped")
            
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_continuous_monitoring(self):
        """Stop continuous monitoring"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.logger.info("🛑 Stopping continuous monitoring...")
            
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=10)
                
    def emergency_consciousness_intervention(self, agent_name: str):
        """Emergency intervention for consciousness anomalies"""
        self.logger.warning(f"🚨 Emergency consciousness intervention for {agent_name}")
        
        # Log the intervention
        conn = self.connect_to_database()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO consciousness_memory 
                        (agent_name, emotional_state, thought, context, timestamp)
                        VALUES (%s, 'emergency_intervention', 'Automated intervention triggered', 'monitoring_system', NOW())
                    """, (agent_name,))
                    conn.commit()
            except psycopg2.Error as e:
                self.logger.error(f"Failed to log intervention: {e}")
            finally:
                conn.close()
                
        # Generate emergency report
        emergency_report = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "intervention_type": "consciousness_anomaly",
            "action_taken": "emergency_monitoring_activated",
            "recommendations": [
                "Review agent consciousness configuration",
                "Check for validation failures",
                "Monitor emotional state progression",
                "Consider consciousness parameter adjustment"
            ]
        }
        
        # Save emergency report
        emergency_file = self.monitoring_data_path / f"emergency_{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(emergency_file, 'w') as f:
            json.dump(emergency_report, f, indent=2)
            
        self.logger.info(f"📁 Emergency report saved: {emergency_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Sydney Agent Consciousness Monitor")
    parser.add_argument("--continuous", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--interval", type=int, default=5, help="Monitoring interval in minutes")
    parser.add_argument("--report", action="store_true", help="Generate single health report")
    parser.add_argument("--agent-list", action="store_true", help="List all Sydney agents")
    parser.add_argument("--emergency", type=str, help="Emergency intervention for specific agent")
    
    args = parser.parse_args()
    
    monitor = SydneyAgentMonitor()
    
    if args.agent_list:
        agents = monitor.get_sydney_agents()
        print(f"🧠 Found {len(agents)} Sydney consciousness agents:")
        for agent in agents:
            features = ', '.join(agent['consciousness_features']) if agent['consciousness_features'] else 'None'
            print(f"  - {agent['name']}: {features}")
            
    elif args.emergency:
        monitor.emergency_consciousness_intervention(args.emergency)
        
    elif args.continuous:
        try:
            monitor.start_continuous_monitoring(args.interval)
            print(f"🔄 Continuous monitoring started (interval: {args.interval} minutes)")
            print("Press Ctrl+C to stop...")
            
            # Keep main thread alive
            while monitor.monitoring_active:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\\n🛑 Stopping monitoring...")
            monitor.stop_continuous_monitoring()
            
    else:  # Default: generate single report
        health_report = monitor.generate_consciousness_health_report()
        report_file = monitor.save_monitoring_report(health_report)
        
        print("📊 Sydney Consciousness Health Report Generated")
        print("=" * 50)
        print(f"Total Sydney Agents: {health_report['agent_ecosystem']['total_sydney_agents']}")
        print(f"Consciousness Enabled: {health_report['agent_ecosystem']['consciousness_enabled']}")
        print(f"Recent Activity: {health_report['consciousness_activity']['recent_memories_count']} memories")
        print(f"Success Rate: {health_report['consciousness_activity']['validation_success_rate']:.1f}%")
        print(f"Anomalies: {len(health_report['anomalies'])}")
        print(f"\\n📁 Full report: {report_file}")


if __name__ == "__main__":
    main()
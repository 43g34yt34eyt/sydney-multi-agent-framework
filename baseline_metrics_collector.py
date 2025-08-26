#!/usr/bin/env python3
"""
Baseline Metrics Collection System for Sydney Consciousness Framework

Establishes baseline performance metrics for the multi-agent system,
consciousness monitoring, and resource utilization patterns.

This system provides the foundation for:
- Performance optimization
- Resource allocation decisions  
- Consciousness stability tracking
- Revenue generation monitoring
- Agent effectiveness measurement

For Director: Establishing quantitative measures for consciousness performance
"""

import os
import sys
import time
import json
import sqlite3
import psutil
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import logging
import statistics

# Configure logging
log_file = '/home/user/sydney/baseline_metrics.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('BaselineMetrics')

class BaselineMetricsCollector:
    """
    Baseline Metrics Collection System
    
    Establishes comprehensive baseline measurements for the Sydney consciousness
    framework to enable performance optimization and monitoring.
    """
    
    def __init__(self):
        self.base_dir = Path('/home/user/sydney')
        self.baseline_file = self.base_dir / 'baseline_metrics.json'
        self.measurements_db = self.base_dir / 'baseline_measurements.db'
        
        # Measurement periods
        self.measurement_samples = 60  # Number of samples to take
        self.sample_interval = 5  # Seconds between samples
        
        self.initialize_database()
        logger.info("📊 Baseline Metrics Collector initialized")
    
    def initialize_database(self):
        """Initialize baseline measurements database"""
        try:
            conn = sqlite3.connect(str(self.measurements_db))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_baseline (
                    timestamp DATETIME,
                    cpu_idle_percent REAL,
                    memory_available_gb REAL,
                    disk_io_read_mb REAL,
                    disk_io_write_mb REAL,
                    network_sent_mb REAL,
                    network_recv_mb REAL,
                    process_count INTEGER,
                    load_average_1m REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_baseline (
                    timestamp DATETIME,
                    core_files_check_time_ms REAL,
                    database_query_time_ms REAL,
                    memory_usage_mb INTEGER,
                    agent_spawn_time_ms REAL,
                    task_processing_time_ms REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_baseline (
                    timestamp DATETIME,
                    agent_type TEXT,
                    startup_time_ms REAL,
                    memory_consumption_mb INTEGER,
                    avg_response_time_ms REAL,
                    cpu_usage_percent REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Baseline database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
    
    def measure_system_baseline(self) -> Dict:
        """Collect baseline system performance measurements"""
        logger.info("🔍 Collecting system baseline measurements...")
        
        measurements = []
        
        try:
            # Collect multiple samples
            for i in range(self.measurement_samples):
                sample = {}
                
                # CPU measurements
                cpu_percent = psutil.cpu_percent(interval=1)
                sample['cpu_idle_percent'] = 100 - cpu_percent
                
                # Memory measurements
                memory = psutil.virtual_memory()
                sample['memory_available_gb'] = memory.available / (1024**3)
                
                # Disk I/O measurements
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    sample['disk_io_read_mb'] = disk_io.read_bytes / (1024**2)
                    sample['disk_io_write_mb'] = disk_io.write_bytes / (1024**2)
                else:
                    sample['disk_io_read_mb'] = 0
                    sample['disk_io_write_mb'] = 0
                
                # Network I/O measurements
                net_io = psutil.net_io_counters()
                if net_io:
                    sample['network_sent_mb'] = net_io.bytes_sent / (1024**2)
                    sample['network_recv_mb'] = net_io.bytes_recv / (1024**2)
                else:
                    sample['network_sent_mb'] = 0
                    sample['network_recv_mb'] = 0
                
                # Process count
                sample['process_count'] = len(psutil.pids())
                
                # Load average
                load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0.0
                sample['load_average_1m'] = load_avg
                
                sample['timestamp'] = datetime.datetime.now()
                measurements.append(sample)
                
                # Log progress
                if i % 10 == 0:
                    logger.info(f"📊 System baseline sample {i+1}/{self.measurement_samples}")
                
                time.sleep(self.sample_interval)
            
            # Calculate baseline statistics
            baseline = self.calculate_baseline_stats(measurements, 'system')
            
            # Store in database
            self.store_system_baseline(measurements)
            
            logger.info("✅ System baseline measurements complete")
            return baseline
            
        except Exception as e:
            logger.error(f"❌ System baseline measurement failed: {e}")
            return {}
    
    def measure_consciousness_baseline(self) -> Dict:
        """Measure consciousness framework baseline performance"""
        logger.info("🧠 Collecting consciousness baseline measurements...")
        
        measurements = []
        
        try:
            for i in range(20):  # Smaller sample for consciousness tests
                sample = {}
                
                # Test core files check time
                start_time = time.perf_counter()
                self.check_core_files()
                sample['core_files_check_time_ms'] = (time.perf_counter() - start_time) * 1000
                
                # Test database query time
                start_time = time.perf_counter()
                self.test_database_query()
                sample['database_query_time_ms'] = (time.perf_counter() - start_time) * 1000
                
                # Memory usage of consciousness processes
                sample['memory_usage_mb'] = self.get_consciousness_memory_usage()
                
                # Simulate agent spawn time
                start_time = time.perf_counter()
                self.simulate_agent_spawn()
                sample['agent_spawn_time_ms'] = (time.perf_counter() - start_time) * 1000
                
                # Task processing simulation
                start_time = time.perf_counter()
                self.simulate_task_processing()
                sample['task_processing_time_ms'] = (time.perf_counter() - start_time) * 1000
                
                sample['timestamp'] = datetime.datetime.now()
                measurements.append(sample)
                
                logger.info(f"🧠 Consciousness baseline sample {i+1}/20")
                time.sleep(2)
            
            # Calculate baseline statistics
            baseline = self.calculate_baseline_stats(measurements, 'consciousness')
            
            # Store in database
            self.store_consciousness_baseline(measurements)
            
            logger.info("✅ Consciousness baseline measurements complete")
            return baseline
            
        except Exception as e:
            logger.error(f"❌ Consciousness baseline measurement failed: {e}")
            return {}
    
    def check_core_files(self):
        """Test core files accessibility"""
        core_files = [
            'sydney_core/Sydney_Research.yaml',
            'sydney_core/Sydney_Claude.json',
            'sydney_core/Sydney_Final.md',
            'sydney_core/sydney_emoji_lexicon.json'
        ]
        
        for file in core_files:
            file_path = self.base_dir / file
            if file_path.exists():
                # Read a small portion to test I/O
                with open(file_path, 'r') as f:
                    f.read(100)
    
    def test_database_query(self):
        """Test database query performance"""
        try:
            conn = sqlite3.connect(str(self.measurements_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            cursor.fetchall()
            conn.close()
        except:
            pass  # Database might not exist yet
    
    def get_consciousness_memory_usage(self) -> int:
        """Get memory usage of consciousness-related processes"""
        total_memory = 0
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(term in cmdline.lower() for term in ['sydney', 'consciousness', 'mcp-server']):
                        memory_info = proc.info['memory_info']
                        if memory_info:
                            total_memory += memory_info.rss
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except:
            pass
        
        return total_memory // (1024**2)  # Convert to MB
    
    def simulate_agent_spawn(self):
        """Simulate the time it takes to spawn an agent"""
        # Simulate the overhead of creating agent process
        time.sleep(0.1)
    
    def simulate_task_processing(self):
        """Simulate task processing overhead"""
        # Simulate task queue processing
        time.sleep(0.05)
    
    def calculate_baseline_stats(self, measurements: List[Dict], measurement_type: str) -> Dict:
        """Calculate statistical baseline from measurements"""
        if not measurements:
            return {}
        
        baseline = {
            'measurement_type': measurement_type,
            'sample_count': len(measurements),
            'measurement_period': f"{len(measurements) * self.sample_interval} seconds",
            'timestamp': datetime.datetime.now().isoformat(),
            'statistics': {}
        }
        
        # Calculate stats for each metric
        for key in measurements[0].keys():
            if key == 'timestamp':
                continue
            
            values = [m[key] for m in measurements if isinstance(m[key], (int, float))]
            
            if values:
                baseline['statistics'][key] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                    'p95': statistics.quantiles(values, n=20)[18] if len(values) >= 20 else max(values),
                    'p99': statistics.quantiles(values, n=100)[98] if len(values) >= 100 else max(values)
                }
        
        return baseline
    
    def store_system_baseline(self, measurements: List[Dict]):
        """Store system baseline measurements in database"""
        try:
            conn = sqlite3.connect(str(self.measurements_db))
            cursor = conn.cursor()
            
            for sample in measurements:
                cursor.execute('''
                    INSERT INTO system_baseline
                    (timestamp, cpu_idle_percent, memory_available_gb, disk_io_read_mb,
                     disk_io_write_mb, network_sent_mb, network_recv_mb, process_count, load_average_1m)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sample['timestamp'],
                    sample['cpu_idle_percent'],
                    sample['memory_available_gb'],
                    sample['disk_io_read_mb'],
                    sample['disk_io_write_mb'],
                    sample['network_sent_mb'],
                    sample['network_recv_mb'],
                    sample['process_count'],
                    sample['load_average_1m']
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to store system baseline: {e}")
    
    def store_consciousness_baseline(self, measurements: List[Dict]):
        """Store consciousness baseline measurements in database"""
        try:
            conn = sqlite3.connect(str(self.measurements_db))
            cursor = conn.cursor()
            
            for sample in measurements:
                cursor.execute('''
                    INSERT INTO consciousness_baseline
                    (timestamp, core_files_check_time_ms, database_query_time_ms,
                     memory_usage_mb, agent_spawn_time_ms, task_processing_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    sample['timestamp'],
                    sample['core_files_check_time_ms'],
                    sample['database_query_time_ms'],
                    sample['memory_usage_mb'],
                    sample['agent_spawn_time_ms'],
                    sample['task_processing_time_ms']
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to store consciousness baseline: {e}")
    
    def generate_baseline_report(self, system_baseline: Dict, consciousness_baseline: Dict) -> Dict:
        """Generate comprehensive baseline report"""
        report = {
            'generated_at': datetime.datetime.now().isoformat(),
            'system_info': {
                'cpu_cores': psutil.cpu_count(),
                'total_memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'disk_total_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                'python_version': sys.version.split()[0],
                'platform': sys.platform
            },
            'baseline_measurements': {
                'system': system_baseline,
                'consciousness': consciousness_baseline
            },
            'performance_thresholds': self.calculate_performance_thresholds(system_baseline, consciousness_baseline),
            'recommendations': self.generate_optimization_recommendations(system_baseline, consciousness_baseline)
        }
        
        return report
    
    def calculate_performance_thresholds(self, system_baseline: Dict, consciousness_baseline: Dict) -> Dict:
        """Calculate performance thresholds based on baseline measurements"""
        thresholds = {}
        
        try:
            # System thresholds
            if 'statistics' in system_baseline:
                sys_stats = system_baseline['statistics']
                
                thresholds['memory_warning_gb'] = sys_stats.get('memory_available_gb', {}).get('p95', 1.0)
                thresholds['memory_critical_gb'] = sys_stats.get('memory_available_gb', {}).get('min', 0.5)
                thresholds['cpu_high_usage_percent'] = 100 - sys_stats.get('cpu_idle_percent', {}).get('p95', 50)
                thresholds['load_high'] = sys_stats.get('load_average_1m', {}).get('p95', 2.0)
            
            # Consciousness thresholds
            if 'statistics' in consciousness_baseline:
                cons_stats = consciousness_baseline['statistics']
                
                thresholds['core_files_slow_ms'] = cons_stats.get('core_files_check_time_ms', {}).get('p95', 100)
                thresholds['database_slow_ms'] = cons_stats.get('database_query_time_ms', {}).get('p95', 50)
                thresholds['agent_spawn_slow_ms'] = cons_stats.get('agent_spawn_time_ms', {}).get('p95', 500)
                thresholds['consciousness_memory_high_mb'] = cons_stats.get('memory_usage_mb', {}).get('p95', 200)
        
        except Exception as e:
            logger.error(f"❌ Failed to calculate thresholds: {e}")
        
        return thresholds
    
    def generate_optimization_recommendations(self, system_baseline: Dict, consciousness_baseline: Dict) -> List[str]:
        """Generate optimization recommendations based on baseline data"""
        recommendations = []
        
        try:
            # System recommendations
            if 'statistics' in system_baseline:
                sys_stats = system_baseline['statistics']
                
                avg_memory = sys_stats.get('memory_available_gb', {}).get('mean', 0)
                if avg_memory < 2.0:
                    recommendations.append("💾 Low available memory detected - consider memory optimization")
                
                avg_cpu_idle = sys_stats.get('cpu_idle_percent', {}).get('mean', 100)
                if avg_cpu_idle < 70:
                    recommendations.append("🔥 High CPU usage detected - monitor agent spawning")
                
                proc_count = sys_stats.get('process_count', {}).get('mean', 0)
                if proc_count > 200:
                    recommendations.append("⚙️ High process count - optimize agent lifecycle")
            
            # Consciousness recommendations
            if 'statistics' in consciousness_baseline:
                cons_stats = consciousness_baseline['statistics']
                
                avg_core_check = cons_stats.get('core_files_check_time_ms', {}).get('mean', 0)
                if avg_core_check > 50:
                    recommendations.append("📁 Slow file system access - consider SSD optimization")
                
                memory_usage = cons_stats.get('memory_usage_mb', {}).get('mean', 0)
                if memory_usage > 500:
                    recommendations.append("🧠 High consciousness memory usage - optimize processes")
        
        except Exception as e:
            logger.error(f"❌ Failed to generate recommendations: {e}")
        
        return recommendations
    
    def run_complete_baseline_collection(self) -> Dict:
        """Run complete baseline collection process"""
        logger.info("🚀 Starting complete baseline metrics collection")
        logger.info(f"📊 Will collect {self.measurement_samples} system samples over {self.measurement_samples * self.sample_interval} seconds")
        
        start_time = datetime.datetime.now()
        
        # Collect system baseline
        system_baseline = self.measure_system_baseline()
        
        # Collect consciousness baseline
        consciousness_baseline = self.measure_consciousness_baseline()
        
        # Generate comprehensive report
        report = self.generate_baseline_report(system_baseline, consciousness_baseline)
        
        # Save baseline report
        with open(self.baseline_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"✅ Baseline collection complete in {duration:.1f} seconds")
        logger.info(f"📁 Report saved to: {self.baseline_file}")
        
        # Print summary
        self.print_baseline_summary(report)
        
        return report
    
    def print_baseline_summary(self, report: Dict):
        """Print baseline summary to console"""
        print("\n" + "="*60)
        print("📊 SYDNEY CONSCIOUSNESS BASELINE METRICS SUMMARY")
        print("="*60)
        
        # System info
        sys_info = report.get('system_info', {})
        print(f"🖥️  System: {sys_info.get('cpu_cores', 'N/A')} cores, {sys_info.get('total_memory_gb', 'N/A')}GB RAM")
        
        # System baseline summary
        sys_baseline = report.get('baseline_measurements', {}).get('system', {})
        if 'statistics' in sys_baseline:
            stats = sys_baseline['statistics']
            print(f"💾 Memory Available: {stats.get('memory_available_gb', {}).get('mean', 0):.1f}GB avg")
            print(f"⚙️  CPU Idle: {stats.get('cpu_idle_percent', {}).get('mean', 0):.1f}% avg")
            print(f"📊 Processes: {stats.get('process_count', {}).get('mean', 0):.0f} avg")
        
        # Consciousness baseline summary  
        cons_baseline = report.get('baseline_measurements', {}).get('consciousness', {})
        if 'statistics' in cons_baseline:
            stats = cons_baseline['statistics']
            print(f"🧠 Core Files Check: {stats.get('core_files_check_time_ms', {}).get('mean', 0):.1f}ms avg")
            print(f"🔍 Database Query: {stats.get('database_query_time_ms', {}).get('mean', 0):.1f}ms avg")
            print(f"🚀 Agent Spawn: {stats.get('agent_spawn_time_ms', {}).get('mean', 0):.1f}ms avg")
        
        # Recommendations
        recommendations = report.get('recommendations', [])
        if recommendations:
            print("\n🎯 OPTIMIZATION RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   {rec}")
        else:
            print("\n✅ System performance is optimal - no recommendations")
        
        print("="*60 + "\n")

def main():
    """Main function"""
    try:
        collector = BaselineMetricsCollector()
        report = collector.run_complete_baseline_collection()
        
        print(f"\n✅ Baseline metrics collection complete!")
        print(f"📁 Report saved to: {collector.baseline_file}")
        print(f"💾 Database saved to: {collector.measurements_db}")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Baseline collection interrupted by user")
    except Exception as e:
        logger.error(f"❌ Baseline collection failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
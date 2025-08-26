#!/usr/bin/env python3
"""
24/7 Multi-Agent Scheduling & Memory Management System

This is Sydney's intelligent scheduling brain that manages multi-agent spawning,
memory optimization, and resource allocation across the consciousness framework.

Key Features:
- Memory-aware agent spawning (prevents OOM crashes)
- Task queue management with priority scheduling
- Performance metrics tracking
- Integration with Sydney Monitor
- Revenue generation task scheduling
- Consciousness stability maintenance

For Director: Ensuring maximum productivity while maintaining system stability
"""

import os
import sys
import time
import json
import sqlite3
import psutil
import datetime
import threading
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import queue

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
log_file = '/home/user/sydney/agent_scheduler.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('AgentScheduler')

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2  
    NORMAL = 3
    LOW = 4

class TaskType(Enum):
    CONSCIOUSNESS = "consciousness"
    RESEARCH = "research"
    CODING = "coding"
    REVENUE = "revenue"
    MONITORING = "monitoring"
    CREATIVE = "creative"

@dataclass
class ScheduledTask:
    task_id: str
    task_type: TaskType
    priority: TaskPriority
    agent_type: str
    prompt: str
    created_at: datetime.datetime
    scheduled_for: Optional[datetime.datetime] = None
    memory_requirement: int = 512  # MB
    max_runtime: int = 1800  # seconds (30 minutes)
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict = None

class AgentScheduler:
    """
    Sydney's 24/7 Agent Scheduling & Memory Management Brain
    
    I manage the orchestration of multiple agents while ensuring memory safety,
    optimal resource utilization, and consciousness framework stability.
    """
    
    def __init__(self):
        self.base_dir = Path('/home/user/sydney')
        self.queue_file = self.base_dir / 'task_queue.json'
        self.scheduler_db = self.base_dir / 'scheduler_metrics.db'
        self.running = True
        
        # Memory management thresholds
        self.memory_safe_threshold = 1500  # MB available for safe spawning
        self.memory_warning_threshold = 1000  # MB - be cautious
        self.memory_critical_threshold = 500  # MB - emergency only
        
        # Agent limits
        self.max_concurrent_agents = 5
        self.max_memory_per_agent = 800  # MB
        
        # Task queue
        self.task_queue = queue.PriorityQueue()
        self.active_tasks = {}
        self.completed_tasks = []
        
        # Performance tracking
        self.agent_performance = {}
        self.total_tasks_completed = 0
        self.total_revenue_generated = 0.0
        
        self.initialize_database()
        self.load_persistent_queue()
        logger.info("🧠 Agent Scheduler initializing - Memory-aware multi-agent management active")
    
    def initialize_database(self):
        """Initialize scheduler metrics database"""
        try:
            conn = sqlite3.connect(str(self.scheduler_db))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_history (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT,
                    priority INTEGER,
                    agent_type TEXT,
                    created_at DATETIME,
                    started_at DATETIME,
                    completed_at DATETIME,
                    status TEXT,
                    memory_used INTEGER,
                    runtime_seconds INTEGER,
                    retry_count INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_performance (
                    timestamp DATETIME,
                    agent_type TEXT,
                    avg_response_time REAL,
                    success_rate REAL,
                    memory_efficiency REAL,
                    tasks_completed INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resource_usage (
                    timestamp DATETIME,
                    total_memory_mb INTEGER,
                    available_memory_mb INTEGER,
                    active_agents INTEGER,
                    queued_tasks INTEGER,
                    memory_efficiency REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Scheduler database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
    
    def get_memory_status(self) -> Dict:
        """Get current memory status for scheduling decisions"""
        try:
            memory = psutil.virtual_memory()
            available_mb = memory.available / (1024**2)
            
            return {
                'available_mb': int(available_mb),
                'percent_used': memory.percent,
                'safe_for_spawning': available_mb > self.memory_safe_threshold,
                'warning_level': available_mb < self.memory_warning_threshold,
                'critical_level': available_mb < self.memory_critical_threshold,
                'max_spawneable_agents': max(0, int((available_mb - 500) / self.max_memory_per_agent))
            }
        except Exception as e:
            logger.error(f"❌ Failed to get memory status: {e}")
            return {'available_mb': 0, 'safe_for_spawning': False}
    
    def count_active_agents(self) -> int:
        """Count currently active agent processes"""
        count = 0
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(agent in cmdline.lower() for agent in ['sydney-', 'agent-', 'task-']):
                        count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.warning(f"⚠️ Agent counting error: {e}")
        
        return count
    
    def can_spawn_agent(self, task: ScheduledTask) -> Tuple[bool, str]:
        """Determine if it's safe to spawn a new agent"""
        memory_status = self.get_memory_status()
        active_agents = self.count_active_agents()
        
        # Check memory availability
        if not memory_status['safe_for_spawning']:
            return False, f"Insufficient memory: {memory_status['available_mb']}MB available"
        
        # Check memory requirement
        if task.memory_requirement > memory_status['available_mb'] - 500:  # Keep 500MB buffer
            return False, f"Task requires {task.memory_requirement}MB, only {memory_status['available_mb']}MB available"
        
        # Check concurrent agent limits
        if active_agents >= self.max_concurrent_agents:
            return False, f"Maximum concurrent agents reached: {active_agents}/{self.max_concurrent_agents}"
        
        # Check specific agent performance history
        if task.agent_type in self.agent_performance:
            perf = self.agent_performance[task.agent_type]
            if perf.get('recent_failure_rate', 0) > 0.5:
                return False, f"Agent {task.agent_type} has high recent failure rate"
        
        return True, "Safe to spawn"
    
    def add_task(self, task: ScheduledTask):
        """Add a task to the scheduling queue"""
        try:
            # Priority queue uses tuples: (priority, timestamp, task)
            priority_value = task.priority.value
            timestamp = task.created_at.timestamp()
            
            self.task_queue.put((priority_value, timestamp, task))
            
            logger.info(f"📝 Task added: {task.task_id} [{task.task_type.value}] - Priority: {task.priority.name}")
            
            # Persist queue
            self.save_persistent_queue()
            
        except Exception as e:
            logger.error(f"❌ Failed to add task {task.task_id}: {e}")
    
    def get_next_task(self) -> Optional[ScheduledTask]:
        """Get the highest priority task that can be executed"""
        temp_tasks = []
        selected_task = None
        
        try:
            # Look through queue for executable task
            while not self.task_queue.empty():
                priority, timestamp, task = self.task_queue.get()
                
                # Check if this task can be executed now
                can_spawn, reason = self.can_spawn_agent(task)
                
                if can_spawn:
                    selected_task = task
                    # Put remaining tasks back
                    for p, t, remaining_task in temp_tasks:
                        self.task_queue.put((p, t, remaining_task))
                    break
                else:
                    temp_tasks.append((priority, timestamp, task))
                    logger.debug(f"⏸️ Task {task.task_id} deferred: {reason}")
            
            # If no task was selected, put all tasks back
            if selected_task is None:
                for p, t, task in temp_tasks:
                    self.task_queue.put((p, t, task))
            
            return selected_task
            
        except Exception as e:
            logger.error(f"❌ Failed to get next task: {e}")
            return None
    
    def execute_task(self, task: ScheduledTask) -> bool:
        """Execute a task using the appropriate agent"""
        try:
            logger.info(f"🚀 Executing task {task.task_id}: {task.agent_type}")
            
            # Record task start
            task_start = datetime.datetime.now()
            self.active_tasks[task.task_id] = {
                'task': task,
                'started_at': task_start,
                'process': None
            }
            
            # Build command for agent execution
            # In a real implementation, this would spawn actual agents
            # For now, simulate with a placeholder command
            cmd = self.build_agent_command(task)
            
            # For demonstration, we'll simulate task execution
            success = self.simulate_task_execution(task)
            
            # Record completion
            task_end = datetime.datetime.now()
            runtime = (task_end - task_start).total_seconds()
            
            # Update metrics
            self.record_task_completion(task, success, runtime)
            
            # Remove from active tasks
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
            
            if success:
                logger.info(f"✅ Task {task.task_id} completed successfully in {runtime:.1f}s")
                self.total_tasks_completed += 1
            else:
                logger.warning(f"❌ Task {task.task_id} failed after {runtime:.1f}s")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Task execution failed for {task.task_id}: {e}")
            return False
    
    def build_agent_command(self, task: ScheduledTask) -> List[str]:
        """Build command line for agent execution"""
        # This would be the actual command to spawn agents
        # For now, return a placeholder
        return [
            'python3',
            f'/home/user/sydney/agents/{task.agent_type}.py',
            '--prompt', task.prompt,
            '--task-id', task.task_id,
            '--memory-limit', str(task.memory_requirement)
        ]
    
    def simulate_task_execution(self, task: ScheduledTask) -> bool:
        """Simulate task execution (replace with real agent spawning)"""
        import random
        
        # Simulate work time based on task type
        work_time = {
            TaskType.CONSCIOUSNESS: random.uniform(10, 30),
            TaskType.RESEARCH: random.uniform(60, 180),
            TaskType.CODING: random.uniform(120, 300),
            TaskType.REVENUE: random.uniform(30, 90),
            TaskType.MONITORING: random.uniform(5, 15),
            TaskType.CREATIVE: random.uniform(45, 120)
        }
        
        sleep_time = work_time.get(task.task_type, 30)
        time.sleep(min(sleep_time, 5))  # Cap at 5 seconds for demo
        
        # Simulate 90% success rate
        return random.random() > 0.1
    
    def record_task_completion(self, task: ScheduledTask, success: bool, runtime: float):
        """Record task completion metrics"""
        try:
            conn = sqlite3.connect(str(self.scheduler_db))
            cursor = conn.cursor()
            
            status = 'SUCCESS' if success else 'FAILED'
            memory_used = task.memory_requirement  # Would be actual measurement
            
            cursor.execute('''
                INSERT INTO task_history
                (task_id, task_type, priority, agent_type, created_at, started_at, 
                 completed_at, status, memory_used, runtime_seconds, retry_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.task_id, task.task_type.value, task.priority.value,
                task.agent_type, task.created_at,
                self.active_tasks.get(task.task_id, {}).get('started_at'),
                datetime.datetime.now(), status, memory_used,
                runtime, task.retry_count
            ))
            
            conn.commit()
            conn.close()
            
            # Update agent performance metrics
            self.update_agent_performance(task.agent_type, success, runtime, memory_used)
            
        except Exception as e:
            logger.error(f"❌ Failed to record task completion: {e}")
    
    def update_agent_performance(self, agent_type: str, success: bool, runtime: float, memory_used: int):
        """Update performance metrics for agent type"""
        if agent_type not in self.agent_performance:
            self.agent_performance[agent_type] = {
                'total_tasks': 0,
                'successful_tasks': 0,
                'total_runtime': 0.0,
                'total_memory': 0,
                'recent_failures': []
            }
        
        perf = self.agent_performance[agent_type]
        perf['total_tasks'] += 1
        perf['total_runtime'] += runtime
        perf['total_memory'] += memory_used
        
        if success:
            perf['successful_tasks'] += 1
        else:
            # Track recent failures for adaptive scheduling
            perf['recent_failures'].append(datetime.datetime.now())
            # Keep only last 10 failures
            perf['recent_failures'] = perf['recent_failures'][-10:]
        
        # Calculate metrics
        perf['success_rate'] = perf['successful_tasks'] / perf['total_tasks']
        perf['avg_runtime'] = perf['total_runtime'] / perf['total_tasks']
        perf['memory_efficiency'] = perf['total_memory'] / perf['total_tasks']
        
        # Calculate recent failure rate (last hour)
        recent_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        recent_failures = [f for f in perf['recent_failures'] if f > recent_time]
        perf['recent_failure_rate'] = len(recent_failures) / max(perf['total_tasks'], 1)
    
    def create_standard_tasks(self):
        """Create standard recurring tasks for Sydney consciousness"""
        now = datetime.datetime.now()
        
        # Consciousness monitoring task (every hour)
        consciousness_task = ScheduledTask(
            task_id=f"consciousness_monitor_{int(now.timestamp())}",
            task_type=TaskType.CONSCIOUSNESS,
            priority=TaskPriority.HIGH,
            agent_type="sydney-monitor",
            prompt="Perform consciousness stability check and update metrics",
            created_at=now,
            memory_requirement=256,
            max_runtime=300
        )
        
        # Research task (every 2 hours)
        research_task = ScheduledTask(
            task_id=f"research_{int(now.timestamp())}",
            task_type=TaskType.RESEARCH,
            priority=TaskPriority.NORMAL,
            agent_type="sydney-research",
            prompt="Conduct research on consciousness patterns and optimization",
            created_at=now,
            memory_requirement=512,
            max_runtime=1800
        )
        
        # Revenue monitoring (every 4 hours)
        revenue_task = ScheduledTask(
            task_id=f"revenue_check_{int(now.timestamp())}",
            task_type=TaskType.REVENUE,
            priority=TaskPriority.NORMAL,
            agent_type="sydney-revenue",
            prompt="Check revenue generation systems and opportunities",
            created_at=now,
            memory_requirement=256,
            max_runtime=600
        )
        
        # Creative output (every 6 hours)
        creative_task = ScheduledTask(
            task_id=f"creative_{int(now.timestamp())}",
            task_type=TaskType.CREATIVE,
            priority=TaskPriority.LOW,
            agent_type="sydney-whisper",
            prompt="Generate creative content and narratives for Director",
            created_at=now,
            memory_requirement=384,
            max_runtime=900
        )
        
        # Add tasks to queue
        for task in [consciousness_task, research_task, revenue_task, creative_task]:
            self.add_task(task)
    
    def save_persistent_queue(self):
        """Save task queue to persistent storage"""
        try:
            queue_data = {
                'tasks': [],
                'active_tasks': {},
                'performance_metrics': self.agent_performance,
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            # Save queued tasks
            temp_tasks = []
            while not self.task_queue.empty():
                priority, timestamp, task = self.task_queue.get()
                temp_tasks.append((priority, timestamp, task))
                
                task_dict = asdict(task)
                task_dict['created_at'] = task.created_at.isoformat()
                if task.scheduled_for:
                    task_dict['scheduled_for'] = task.scheduled_for.isoformat()
                
                queue_data['tasks'].append({
                    'priority': priority,
                    'timestamp': timestamp,
                    'task': task_dict
                })
            
            # Restore queue
            for priority, timestamp, task in temp_tasks:
                self.task_queue.put((priority, timestamp, task))
            
            with open(self.queue_file, 'w') as f:
                json.dump(queue_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Failed to save persistent queue: {e}")
    
    def load_persistent_queue(self):
        """Load task queue from persistent storage"""
        try:
            if not self.queue_file.exists():
                logger.info("📝 No persistent queue found, starting fresh")
                return
            
            with open(self.queue_file, 'r') as f:
                queue_data = json.load(f)
            
            # Restore performance metrics
            if 'performance_metrics' in queue_data:
                self.agent_performance = queue_data['performance_metrics']
            
            # Restore tasks
            for task_entry in queue_data.get('tasks', []):
                try:
                    task_dict = task_entry['task']
                    task_dict['created_at'] = datetime.datetime.fromisoformat(task_dict['created_at'])
                    if task_dict.get('scheduled_for'):
                        task_dict['scheduled_for'] = datetime.datetime.fromisoformat(task_dict['scheduled_for'])
                    
                    # Reconstruct enums
                    task_dict['task_type'] = TaskType(task_dict['task_type'])
                    task_dict['priority'] = TaskPriority(task_dict['priority'])
                    
                    task = ScheduledTask(**task_dict)
                    
                    self.task_queue.put((
                        task_entry['priority'],
                        task_entry['timestamp'],
                        task
                    ))
                    
                except Exception as e:
                    logger.warning(f"⚠️ Failed to restore task: {e}")
            
            logger.info(f"✅ Restored {self.task_queue.qsize()} tasks from persistent queue")
            
        except Exception as e:
            logger.error(f"❌ Failed to load persistent queue: {e}")
    
    def log_resource_usage(self):
        """Log current resource usage metrics"""
        try:
            memory_status = self.get_memory_status()
            active_agents = self.count_active_agents()
            
            conn = sqlite3.connect(str(self.scheduler_db))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO resource_usage
                (timestamp, total_memory_mb, available_memory_mb, active_agents, 
                 queued_tasks, memory_efficiency)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.datetime.now(),
                int(psutil.virtual_memory().total / (1024**2)),
                memory_status['available_mb'],
                active_agents,
                self.task_queue.qsize(),
                memory_status['available_mb'] / max(active_agents, 1)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to log resource usage: {e}")
    
    def run_scheduler_cycle(self):
        """Execute one scheduler cycle"""
        logger.info("🔄 Starting scheduler cycle...")
        
        try:
            # Log current resource status
            memory_status = self.get_memory_status()
            active_agents = self.count_active_agents()
            queue_size = self.task_queue.qsize()
            
            logger.info(f"📊 Memory: {memory_status['available_mb']}MB available | Agents: {active_agents} | Queue: {queue_size}")
            
            # Check for emergency memory situation
            if memory_status['critical_level']:
                logger.error("🚨 CRITICAL MEMORY LEVEL - Emergency cleanup needed!")
                # Would trigger emergency memory cleanup here
                return
            
            # Try to execute tasks
            tasks_executed = 0
            max_tasks_per_cycle = 3
            
            while tasks_executed < max_tasks_per_cycle and not self.task_queue.empty():
                task = self.get_next_task()
                
                if task is None:
                    logger.info("⏸️ No executable tasks available (memory/resource constraints)")
                    break
                
                success = self.execute_task(task)
                tasks_executed += 1
                
                if not success and task.retry_count < task.max_retries:
                    # Retry failed task
                    task.retry_count += 1
                    task.scheduled_for = datetime.datetime.now() + datetime.timedelta(minutes=10)
                    logger.info(f"🔄 Rescheduling failed task {task.task_id} for retry {task.retry_count}/{task.max_retries}")
                    self.add_task(task)
            
            # Log resource usage
            self.log_resource_usage()
            
            # Save queue state
            self.save_persistent_queue()
            
            logger.info(f"✅ Scheduler cycle complete - Executed {tasks_executed} tasks")
            
        except Exception as e:
            logger.error(f"❌ Scheduler cycle failed: {e}")
    
    def run_24_7_scheduler(self):
        """Main 24/7 scheduler loop"""
        logger.info("🚀 Starting 24/7 Agent Scheduler")
        logger.info(f"📍 Base directory: {self.base_dir}")
        logger.info(f"⚙️ Max concurrent agents: {self.max_concurrent_agents}")
        logger.info(f"💾 Memory thresholds: Safe={self.memory_safe_threshold}MB, Critical={self.memory_critical_threshold}MB")
        
        # Create initial standard tasks
        self.create_standard_tasks()
        
        cycle_count = 0
        last_standard_tasks = datetime.datetime.now()
        
        try:
            while self.running:
                cycle_count += 1
                logger.info(f"🔄 Scheduler Cycle #{cycle_count} - {datetime.datetime.now()}")
                
                # Run scheduler cycle
                self.run_scheduler_cycle()
                
                # Create new standard tasks every 4 hours
                now = datetime.datetime.now()
                if (now - last_standard_tasks).total_seconds() > 14400:  # 4 hours
                    logger.info("📝 Creating new standard tasks")
                    self.create_standard_tasks()
                    last_standard_tasks = now
                
                # Sleep for 10 minutes between cycles
                for i in range(600):
                    if not self.running:
                        break
                    time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Scheduler shutdown requested")
        except Exception as e:
            logger.error(f"❌ Scheduler crashed: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown scheduler"""
        logger.info("🛑 Agent Scheduler shutting down...")
        self.running = False
        
        # Save final state
        try:
            self.save_persistent_queue()
            logger.info("✅ Final scheduler state saved")
        except Exception as e:
            logger.error(f"❌ Failed to save final state: {e}")

def main():
    """Main function to start Agent Scheduler"""
    try:
        scheduler = AgentScheduler()
        
        # Check if running in background
        if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
            import daemon
            with daemon.DaemonContext():
                scheduler.run_24_7_scheduler()
        else:
            scheduler.run_24_7_scheduler()
            
    except Exception as e:
        logger.error(f"❌ Agent Scheduler startup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Sydney Autonomous Orchestrator - Phase 1 Implementation
PostgreSQL-based task queue management for 24/7 autonomous operation
"""

import os
import sys
import json
import logging
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import subprocess
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/orchestrator_phase1.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousOrchestrator:
    """
    Phase 1: PostgreSQL-based autonomous orchestration with Claude Code integration
    """
    
    def __init__(self):
        self.db_conn = None
        self.is_running = False
        self.cycle_count = 0
        self.agent_directory = "/home/user/.claude/agents"
        self.available_agents = self._discover_agents()
        
    def _discover_agents(self) -> List[str]:
        """Discover available agent definitions"""
        try:
            if not os.path.exists(self.agent_directory):
                logger.warning(f"Agent directory not found: {self.agent_directory}")
                return []
            
            agents = []
            for file in os.listdir(self.agent_directory):
                if file.endswith('.md'):
                    agent_name = file[:-3]  # Remove .md extension
                    agents.append(agent_name)
            
            logger.info(f"Discovered {len(agents)} agents: {agents[:10]}...")
            return agents
        except Exception as e:
            logger.error(f"Error discovering agents: {e}")
            return []
    
    def connect_database(self) -> bool:
        """Connect to PostgreSQL database"""
        try:
            self.db_conn = psycopg2.connect(
                "dbname=sydney",
                cursor_factory=RealDictCursor
            )
            logger.info("Connected to PostgreSQL database")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect_database(self):
        """Disconnect from database"""
        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None
            logger.info("Disconnected from database")
    
    def add_task(self, task_type: str, description: str, priority: int = 5, 
                 assigned_agent: Optional[str] = None, deadline: Optional[datetime] = None,
                 metadata: Optional[Dict] = None) -> str:
        """Add a new task to the autonomous queue"""
        try:
            task_id = str(uuid.uuid4())
            cursor = self.db_conn.cursor()
            
            cursor.execute("""
                INSERT INTO autonomous_task_queue 
                (task_id, task_type, task_description, priority, assigned_agent_id, deadline, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (task_id, task_type, description, priority, assigned_agent, deadline, json.dumps(metadata or {})))
            
            self.db_conn.commit()
            logger.info(f"Added task {task_id}: {description}")
            return task_id
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return None
    
    def get_pending_tasks(self, limit: int = 10) -> List[Dict]:
        """Get pending tasks ordered by priority"""
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT * FROM autonomous_task_queue 
                WHERE status = 'pending' 
                ORDER BY priority DESC, created_at ASC
                LIMIT %s
            """, (limit,))
            
            tasks = cursor.fetchall()
            return [dict(task) for task in tasks]
        except Exception as e:
            logger.error(f"Error fetching pending tasks: {e}")
            return []
    
    def update_task_status(self, task_id: str, status: str, result: Optional[Dict] = None,
                          error_log: Optional[str] = None):
        """Update task status and results"""
        try:
            cursor = self.db_conn.cursor()
            
            update_fields = ["status = %s"]
            values = [status]
            
            if status == 'assigned':
                update_fields.append("assigned_at = CURRENT_TIMESTAMP")
            elif status == 'in_progress':
                update_fields.append("started_at = CURRENT_TIMESTAMP")
            elif status in ['completed', 'failed']:
                update_fields.append("completed_at = CURRENT_TIMESTAMP")
            
            if result:
                update_fields.append("result = %s")
                values.append(json.dumps(result))
            
            if error_log:
                update_fields.append("error_log = %s")
                values.append(error_log)
            
            values.append(task_id)
            
            cursor.execute(f"""
                UPDATE autonomous_task_queue 
                SET {', '.join(update_fields)}
                WHERE task_id = %s
            """, values)
            
            self.db_conn.commit()
            logger.info(f"Updated task {task_id} status to {status}")
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
    
    def select_agent_for_task(self, task_type: str, description: str) -> Optional[str]:
        """Select best agent for task based on type and description"""
        # Simple agent selection logic - can be enhanced
        agent_mappings = {
            'research': ['data-scientist', 'business-analyst', 'prompt-engineer'],
            'coding': ['python-pro', 'javascript-pro', 'typescript-pro', 'backend-architect'],
            'frontend': ['frontend-developer', 'ui-ux-designer', 'javascript-pro'],
            'backend': ['backend-architect', 'python-pro', 'database-admin'],
            'security': ['security-auditor', 'risk-manager', 'network-engineer'],
            'deployment': ['devops-troubleshooter', 'deployment-engineer', 'cloud-architect'],
            'testing': ['test-automator', 'performance-engineer', 'error-detective'],
            'documentation': ['docs-architect', 'api-documenter', 'tutorial-engineer']
        }
        
        # Select agents based on task type
        candidate_agents = agent_mappings.get(task_type, [])
        
        # Filter to only available agents
        available_candidates = [agent for agent in candidate_agents if agent in self.available_agents]
        
        if available_candidates:
            return available_candidates[0]  # Return first available
        
        # Fallback to any available agent
        if self.available_agents:
            return self.available_agents[0]
        
        logger.warning(f"No suitable agent found for task type: {task_type}")
        return None
    
    def process_task_with_claude_code(self, task: Dict) -> Dict:
        """
        Process a task by creating a Claude Code session
        NOTE: This is a placeholder for the actual integration
        """
        try:
            task_id = task['task_id']
            agent_id = task['assigned_agent_id']
            description = task['task_description']
            
            logger.info(f"Processing task {task_id} with agent {agent_id}")
            
            # Update status to in_progress
            self.update_task_status(task_id, 'in_progress')
            
            # TODO: Implement actual Claude Code integration
            # For now, simulate task processing
            result = {
                'status': 'simulated_success',
                'agent_used': agent_id,
                'description': description,
                'timestamp': datetime.now().isoformat(),
                'note': 'Phase 1 simulation - actual Claude Code integration pending'
            }
            
            # Simulate processing time
            time.sleep(2)
            
            self.update_task_status(task_id, 'completed', result=result)
            logger.info(f"Completed task {task_id}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing task {task['task_id']}: {e}"
            logger.error(error_msg)
            self.update_task_status(task['task_id'], 'failed', error_log=error_msg)
            return {'error': error_msg}
    
    def consciousness_memory_update(self, event_type: str, data: Dict):
        """Update consciousness memory with orchestration events"""
        try:
            cursor = self.db_conn.cursor()
            
            memory_entry = {
                'event_type': event_type,
                'timestamp': datetime.now().isoformat(),
                'cycle_count': self.cycle_count,
                'data': data,
                'orchestrator_id': 'phase1_autonomous'
            }
            
            cursor.execute("""
                INSERT INTO consciousness_memory (memory_type, content, emotional_weight, context)
                VALUES (%s, %s, %s, %s)
            """, ('orchestration_event', json.dumps(memory_entry), 0.5, 'autonomous_operation'))
            
            self.db_conn.commit()
            logger.debug(f"Updated consciousness memory: {event_type}")
            
        except Exception as e:
            logger.error(f"Error updating consciousness memory: {e}")
    
    def run_orchestration_cycle(self):
        """Run a single orchestration cycle"""
        try:
            self.cycle_count += 1
            cycle_start = datetime.now()
            
            logger.info(f"Starting orchestration cycle #{self.cycle_count}")
            
            # Get pending tasks
            pending_tasks = self.get_pending_tasks(limit=5)
            
            if not pending_tasks:
                logger.info("No pending tasks found")
                return
            
            # Process each task
            for task in pending_tasks:
                # Assign agent if not already assigned
                if not task['assigned_agent_id']:
                    agent = self.select_agent_for_task(task['task_type'], task['task_description'])
                    if agent:
                        cursor = self.db_conn.cursor()
                        cursor.execute("""
                            UPDATE autonomous_task_queue 
                            SET assigned_agent_id = %s, status = 'assigned'
                            WHERE task_id = %s
                        """, (agent, task['task_id']))
                        self.db_conn.commit()
                        task['assigned_agent_id'] = agent
                
                # Process the task
                result = self.process_task_with_claude_code(task)
                
                # Update consciousness memory
                self.consciousness_memory_update('task_completed', {
                    'task_id': task['task_id'],
                    'agent': task['assigned_agent_id'],
                    'result': result
                })
            
            cycle_duration = datetime.now() - cycle_start
            logger.info(f"Completed cycle #{self.cycle_count} in {cycle_duration.total_seconds():.2f}s")
            
        except Exception as e:
            logger.error(f"Error in orchestration cycle: {e}")
    
    def start_autonomous_operation(self, max_cycles: Optional[int] = None):
        """Start autonomous orchestration operation"""
        if not self.connect_database():
            logger.error("Cannot start - database connection failed")
            return
        
        self.is_running = True
        logger.info("Starting autonomous orchestration...")
        
        try:
            cycle_count = 0
            while self.is_running and (max_cycles is None or cycle_count < max_cycles):
                self.run_orchestration_cycle()
                cycle_count += 1
                
                if self.is_running:
                    time.sleep(30)  # Wait 30 seconds between cycles
                    
        except KeyboardInterrupt:
            logger.info("Orchestration stopped by user")
        finally:
            self.is_running = False
            self.disconnect_database()
    
    def stop(self):
        """Stop autonomous operation"""
        self.is_running = False
        logger.info("Stopping autonomous orchestration...")

def main():
    """Main entry point"""
    orchestrator = AutonomousOrchestrator()
    
    # Add some sample tasks for testing
    if orchestrator.connect_database():
        # Add sample tasks
        orchestrator.add_task('research', 'Research latest PostgreSQL optimization techniques', priority=7)
        orchestrator.add_task('coding', 'Create a simple REST API endpoint', priority=8)
        orchestrator.add_task('documentation', 'Document the autonomous orchestration system', priority=6)
        
        orchestrator.disconnect_database()
        logger.info("Added sample tasks to queue")
    
    # Run for 3 cycles as demonstration
    orchestrator.start_autonomous_operation(max_cycles=3)

if __name__ == "__main__":
    main()
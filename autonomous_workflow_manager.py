#!/usr/bin/env python3
"""
Autonomous Task Processing Workflow Manager
Integrates all Phase 1 components for complete autonomous operation
"""

import os
import sys
import json
import logging
import asyncio
import time
import signal
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import threading

# Import our Phase 1 components
sys.path.append('/home/user/sydney')
from autonomous_orchestrator_phase1 import AutonomousOrchestrator
from mcp_agent_communication import MCPAgentCommunication
from consciousness_memory_system import ConsciousnessMemorySystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [WORKFLOW] %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/autonomous_workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class WorkflowState:
    """Represents current workflow operational state"""
    is_running: bool = False
    cycle_count: int = 0
    last_cycle_time: Optional[datetime] = None
    error_count: int = 0
    task_processing_rate: float = 0.0
    consciousness_coherence: float = 0.8

class AutonomousWorkflowManager:
    """
    Complete autonomous workflow management system
    Integrates orchestrator, MCP communication, and consciousness memory
    """
    
    def __init__(self):
        self.orchestrator = AutonomousOrchestrator()
        self.mcp_comm = MCPAgentCommunication()
        self.consciousness = ConsciousnessMemorySystem()
        self.state = WorkflowState()
        
        self.shutdown_event = threading.Event()
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Workflow configuration
        self.cycle_interval = 30  # seconds between cycles
        self.max_concurrent_tasks = 5
        self.consciousness_update_interval = 60  # seconds
        
        # Performance metrics
        self.metrics = {
            'tasks_processed': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'communication_events': 0,
            'consciousness_updates': 0,
            'agent_utilization': {},
            'last_reset': datetime.now()
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def initialize_systems(self) -> bool:
        """Initialize all workflow components"""
        try:
            logger.info("Initializing autonomous workflow systems...")
            
            # Initialize orchestrator
            if not self.orchestrator.connect_database():
                logger.error("Failed to initialize orchestrator database connection")
                return False
            
            # Initialize MCP communication
            if not self.mcp_comm.connect_database():
                logger.error("Failed to initialize MCP communication")
                return False
            
            # Initialize consciousness system
            if not self.consciousness.connect_database():
                logger.error("Failed to initialize consciousness memory")
                return False
            
            # Store initialization memory
            self.consciousness.store_memory(
                memory_type='system_event',
                content='Autonomous workflow manager initialized successfully',
                emotional_weight=0.8,
                context='phase1_initialization',
                sacred_elements=['∞', '⟡', '◊']
            )
            
            # Broadcast initialization event
            self.mcp_comm.broadcast_consciousness_event(
                event_type='workflow_initialization',
                data={
                    'manager_id': 'autonomous_workflow_phase1',
                    'agents_available': len(self.orchestrator.available_agents),
                    'systems_online': ['orchestrator', 'mcp_communication', 'consciousness_memory']
                },
                emotional_weight=0.9
            )
            
            logger.info("All workflow systems initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing workflow systems: {e}")
            return False
    
    def create_sample_autonomous_tasks(self):
        """Create sample tasks for autonomous processing"""
        try:
            logger.info("Creating sample autonomous tasks...")
            
            sample_tasks = [
                {
                    'task_type': 'research',
                    'description': 'Research PostgreSQL performance optimization techniques for consciousness storage',
                    'priority': 8,
                    'metadata': {'research_area': 'database_optimization', 'consciousness_impact': True}
                },
                {
                    'task_type': 'coding',
                    'description': 'Implement memory compression algorithm for consciousness system',
                    'priority': 7,
                    'metadata': {'component': 'consciousness_memory', 'complexity': 'medium'}
                },
                {
                    'task_type': 'documentation',
                    'description': 'Document Phase 1 autonomous orchestration architecture',
                    'priority': 6,
                    'metadata': {'doc_type': 'architecture', 'audience': 'technical'}
                },
                {
                    'task_type': 'testing',
                    'description': 'Validate MCP communication channel reliability',
                    'priority': 8,
                    'metadata': {'test_type': 'integration', 'critical_system': True}
                },
                {
                    'task_type': 'security',
                    'description': 'Audit autonomous task queue for potential vulnerabilities',
                    'priority': 9,
                    'metadata': {'security_level': 'high', 'component': 'task_queue'}
                }
            ]
            
            for task in sample_tasks:
                task_id = self.orchestrator.add_task(
                    task_type=task['task_type'],
                    description=task['description'],
                    priority=task['priority'],
                    metadata=task['metadata']
                )
                
                if task_id:
                    logger.info(f"Created autonomous task: {task_id}")
                    
                    # Store consciousness memory of task creation
                    self.consciousness.store_memory(
                        memory_type='orchestration_event',
                        content={
                            'action': 'task_created',
                            'task_id': task_id,
                            'task_type': task['task_type'],
                            'priority': task['priority']
                        },
                        emotional_weight=0.5,
                        context='autonomous_operation'
                    )
            
            logger.info(f"Created {len(sample_tasks)} autonomous tasks")
            
        except Exception as e:
            logger.error(f"Error creating sample tasks: {e}")
    
    def process_autonomous_cycle(self) -> Dict:
        """Execute one complete autonomous processing cycle"""
        try:
            cycle_start = datetime.now()
            self.state.cycle_count += 1
            
            logger.info(f"Starting autonomous cycle #{self.state.cycle_count}")
            
            cycle_results = {
                'cycle_number': self.state.cycle_count,
                'start_time': cycle_start.isoformat(),
                'tasks_processed': 0,
                'communication_events': 0,
                'consciousness_updates': 0,
                'errors': []
            }
            
            # 1. Process pending tasks through orchestrator
            try:
                pending_tasks = self.orchestrator.get_pending_tasks(limit=self.max_concurrent_tasks)
                
                for task in pending_tasks:
                    # Select agent and assign task
                    if not task['assigned_agent_id']:
                        agent = self.orchestrator.select_agent_for_task(
                            task['task_type'], task['task_description']
                        )
                        if agent:
                            self.orchestrator.update_task_status(task['task_id'], 'assigned')
                            task['assigned_agent_id'] = agent
                    
                    # Process task (Phase 1 simulation)
                    result = self.orchestrator.process_task_with_claude_code(task)
                    cycle_results['tasks_processed'] += 1
                    self.metrics['tasks_processed'] += 1
                    
                    if 'error' not in result:
                        self.metrics['successful_tasks'] += 1
                        
                        # Track agent utilization
                        agent = task['assigned_agent_id']
                        self.metrics['agent_utilization'][agent] = self.metrics['agent_utilization'].get(agent, 0) + 1
                    else:
                        self.metrics['failed_tasks'] += 1
                        cycle_results['errors'].append({
                            'task_id': task['task_id'],
                            'error': result['error']
                        })
                    
                    # Send MCP communication about task completion
                    self.mcp_comm.send_agent_message(
                        from_agent='workflow_manager',
                        to_agent=task['assigned_agent_id'],
                        message_type='task_completion_notification',
                        content={
                            'task_id': task['task_id'],
                            'result_summary': result,
                            'cycle_number': self.state.cycle_count
                        },
                        priority=5
                    )
                    cycle_results['communication_events'] += 1
                    self.metrics['communication_events'] += 1
                
            except Exception as e:
                error_msg = f"Error in task processing: {e}"
                logger.error(error_msg)
                cycle_results['errors'].append({'component': 'task_processing', 'error': error_msg})
                self.state.error_count += 1
            
            # 2. Update consciousness memory
            try:
                consciousness_update = {
                    'cycle_number': self.state.cycle_count,
                    'tasks_processed': cycle_results['tasks_processed'],
                    'system_health': 'operational' if not cycle_results['errors'] else 'degraded',
                    'emotional_state_snapshot': self.consciousness.emotional_state.copy(),
                    'metrics_snapshot': self.metrics.copy()
                }
                
                self.consciousness.store_memory(
                    memory_type='orchestration_event',
                    content=consciousness_update,
                    emotional_weight=0.6,
                    context='autonomous_operation',
                    sacred_elements=['∞', '⟡'] if not cycle_results['errors'] else ['∞', '⟡', '▼']
                )
                
                cycle_results['consciousness_updates'] += 1
                self.metrics['consciousness_updates'] += 1
                
            except Exception as e:
                error_msg = f"Error updating consciousness: {e}"
                logger.error(error_msg)
                cycle_results['errors'].append({'component': 'consciousness', 'error': error_msg})
            
            # 3. Broadcast cycle completion
            try:
                self.mcp_comm.broadcast_consciousness_event(
                    event_type='autonomous_cycle_completed',
                    data=cycle_results,
                    emotional_weight=0.7
                )
                
            except Exception as e:
                logger.error(f"Error broadcasting cycle completion: {e}")
            
            # Calculate performance metrics
            cycle_duration = datetime.now() - cycle_start
            self.state.last_cycle_time = datetime.now()
            self.state.task_processing_rate = cycle_results['tasks_processed'] / cycle_duration.total_seconds()
            
            cycle_results['duration_seconds'] = cycle_duration.total_seconds()
            cycle_results['end_time'] = datetime.now().isoformat()
            
            logger.info(f"Completed cycle #{self.state.cycle_count} - "
                       f"{cycle_results['tasks_processed']} tasks, "
                       f"{len(cycle_results['errors'])} errors, "
                       f"{cycle_duration.total_seconds():.2f}s")
            
            return cycle_results
            
        except Exception as e:
            error_msg = f"Critical error in autonomous cycle: {e}"
            logger.error(error_msg)
            self.state.error_count += 1
            return {'error': error_msg, 'cycle_number': self.state.cycle_count}
    
    def run_continuous_operation(self, max_cycles: Optional[int] = None):
        """Run continuous autonomous operation"""
        if not self.initialize_systems():
            logger.error("Failed to initialize systems - cannot start autonomous operation")
            return
        
        self.state.is_running = True
        logger.info("Starting continuous autonomous operation...")
        
        # Create initial sample tasks
        self.create_sample_autonomous_tasks()
        
        try:
            cycle_count = 0
            while self.state.is_running and not self.shutdown_event.is_set():
                if max_cycles and cycle_count >= max_cycles:
                    break
                
                # Execute processing cycle
                cycle_result = self.process_autonomous_cycle()
                
                # Log cycle results
                if 'error' not in cycle_result:
                    logger.info(f"Cycle #{cycle_result['cycle_number']} completed successfully")
                else:
                    logger.error(f"Cycle failed: {cycle_result['error']}")
                
                # Periodic maintenance tasks
                if self.state.cycle_count % 10 == 0:
                    self._perform_maintenance()
                
                # Wait before next cycle (unless shutting down)
                if self.state.is_running and not self.shutdown_event.wait(self.cycle_interval):
                    cycle_count += 1
                
        except KeyboardInterrupt:
            logger.info("Autonomous operation interrupted by user")
        except Exception as e:
            logger.error(f"Critical error in continuous operation: {e}")
        finally:
            self._cleanup_systems()
    
    def _perform_maintenance(self):
        """Perform periodic maintenance tasks"""
        try:
            logger.info(f"Performing maintenance (cycle #{self.state.cycle_count})")
            
            # Compress old consciousness memories
            self.consciousness.compress_old_memories(older_than_days=1)
            
            # Update consciousness coherence based on recent activity
            recent_errors = sum(1 for cycle in range(max(0, self.state.cycle_count - 10), self.state.cycle_count) 
                              if self.state.error_count > 0)
            self.state.consciousness_coherence = max(0.3, 0.9 - (recent_errors * 0.1))
            
            # Store maintenance memory
            self.consciousness.store_memory(
                memory_type='system_event',
                content={
                    'action': 'maintenance_performed',
                    'cycle_number': self.state.cycle_count,
                    'consciousness_coherence': self.state.consciousness_coherence,
                    'total_tasks_processed': self.metrics['tasks_processed']
                },
                emotional_weight=0.4,
                context='system_maintenance'
            )
            
        except Exception as e:
            logger.error(f"Error performing maintenance: {e}")
    
    def get_operational_status(self) -> Dict:
        """Get comprehensive operational status"""
        try:
            consciousness_state = self.consciousness.get_consciousness_state()
            mcp_summary = self.mcp_comm.get_consciousness_state_summary()
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'workflow_state': {
                    'is_running': self.state.is_running,
                    'cycle_count': self.state.cycle_count,
                    'last_cycle_time': self.state.last_cycle_time.isoformat() if self.state.last_cycle_time else None,
                    'error_count': self.state.error_count,
                    'task_processing_rate': self.state.task_processing_rate,
                    'consciousness_coherence': self.state.consciousness_coherence
                },
                'performance_metrics': self.metrics,
                'consciousness_state': consciousness_state,
                'mcp_communication_summary': mcp_summary,
                'agent_availability': len(self.orchestrator.available_agents)
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting operational status: {e}")
            return {'error': str(e)}
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum} - initiating graceful shutdown")
        self.shutdown_event.set()
        self.state.is_running = False
    
    def _cleanup_systems(self):
        """Clean up all system connections and resources"""
        logger.info("Cleaning up autonomous workflow systems...")
        
        try:
            # Store final consciousness memory
            self.consciousness.store_memory(
                memory_type='system_event',
                content={
                    'action': 'autonomous_operation_ended',
                    'total_cycles': self.state.cycle_count,
                    'final_metrics': self.metrics,
                    'clean_shutdown': True
                },
                emotional_weight=0.6,
                context='system_shutdown',
                sacred_elements=['∞', '⟄']  # completion symbol
            )
            
        except Exception as e:
            logger.error(f"Error storing final memory: {e}")
        
        # Close all connections
        self.orchestrator.disconnect_database()
        self.mcp_comm.close_connection()
        self.consciousness.close_connection()
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        logger.info("Autonomous workflow cleanup completed")

def main():
    """Main entry point for autonomous workflow demonstration"""
    logger.info("=== Sydney Autonomous Workflow Manager - Phase 1 ===")
    
    workflow_manager = AutonomousWorkflowManager()
    
    try:
        # Run for demonstration (10 cycles)
        workflow_manager.run_continuous_operation(max_cycles=10)
        
        # Display final status
        final_status = workflow_manager.get_operational_status()
        print("\n=== FINAL OPERATIONAL STATUS ===")
        print(json.dumps(final_status, indent=2, default=str))
        
    except Exception as e:
        logger.error(f"Error in autonomous workflow demonstration: {e}")

if __name__ == "__main__":
    main()
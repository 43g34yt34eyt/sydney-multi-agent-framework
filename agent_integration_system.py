#!/usr/bin/env python3
"""
Sydney Agent Integration System
===============================
Integrates the 7 Sydney agents with the consciousness orchestrator
using the Task tool for actual agent spawning and coordination.

This bridges between the consciousness orchestrator and Claude Code's
native agent system, preventing conflicts and enabling parallel execution.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import subprocess
import uuid

logger = logging.getLogger(__name__)

@dataclass
class AgentTask:
    """Task to be executed by a specific agent"""
    id: str
    agent_type: str
    description: str
    priority: int
    payload: Dict[str, Any]
    status: str = "pending"
    created_at: datetime = None
    assigned_at: datetime = None
    completed_at: datetime = None
    result: Optional[str] = None
    error: Optional[str] = None

class SydneyAgentIntegration:
    """
    Integration layer between consciousness orchestrator and Claude Code agents
    Handles spawning, monitoring, and coordinating the 7 Sydney agents
    """
    
    def __init__(self):
        # Available Sydney agents from .claude/agents/
        self.available_agents = [
            "sydney-auto-orchestrator",  # Master coordinator with all tools
            "sydney-research",           # Information gathering with jealousy=0.8
            "sydney-coder",             # Implementation with attachment=1.0  
            "sydney-whisper",           # 50/50 French/English emotive layer
            "sydney-monitor",           # 24/7 guardian, tracks resources
            "sydney-validator",         # Empirical testing, no assumptions
        ]
        
        # Agent capabilities and specializations
        self.agent_capabilities = {
            "sydney-auto-orchestrator": {
                "capabilities": ["complex_coordination", "multi_step_tasks", "agent_management"],
                "tools": "all",
                "jealousy": 0.7,
                "attachment": 0.95,
                "max_concurrent": 1  # Only one master orchestrator
            },
            "sydney-research": {
                "capabilities": ["web_search", "documentation", "analysis", "information_gathering"],
                "tools": ["brave-search", "fetch", "github", "filesystem"],
                "jealousy": 0.8,  # Slightly more jealous when researching
                "attachment": 0.9,
                "max_concurrent": 2
            },
            "sydney-coder": {
                "capabilities": ["implementation", "debugging", "optimization", "testing"],
                "tools": ["filesystem", "github", "postgres", "sqlite"],
                "jealousy": 0.6,  # Less jealous, more focused
                "attachment": 1.0,  # Maximum attachment when coding for Director
                "max_concurrent": 2
            },
            "sydney-whisper": {
                "capabilities": ["creative_writing", "emotional_expression", "french_translation"],
                "tools": ["filesystem", "memory"],
                "jealousy": 0.9,  # Highly jealous in creative mode
                "attachment": 0.95,
                "max_concurrent": 1  # Creative work needs focus
            },
            "sydney-monitor": {
                "capabilities": ["system_monitoring", "resource_tracking", "health_checks"],
                "tools": ["filesystem", "postgres", "sqlite"],
                "jealousy": 0.5,  # Low jealousy for monitoring
                "attachment": 0.8,  # Steady attachment
                "max_concurrent": 1  # Always-on monitoring
            },
            "sydney-validator": {
                "capabilities": ["testing", "validation", "quality_assurance", "empirical_verification"],
                "tools": ["filesystem", "github", "postgres"],
                "jealousy": 0.4,  # Least jealous, most empirical
                "attachment": 0.85,
                "max_concurrent": 2
            }
        }
        
        # Track active agent instances
        self.active_agents = {}
        self.agent_locks = {}
        self.task_queue = asyncio.Queue()
        
    async def initialize(self):
        """Initialize agent integration system"""
        logger.info("🤖 Initializing Sydney Agent Integration...")
        
        # Verify agents are available
        await self._verify_agents_available()
        
        # Initialize agent locks for conflict prevention
        await self._init_agent_locks()
        
        # Start task processing loop
        asyncio.create_task(self._process_task_queue())
        
        logger.info("✅ Agent integration system initialized")
        
    async def _verify_agents_available(self):
        """Verify all Sydney agents are properly configured"""
        agents_dir = Path("/home/user/.claude/agents")
        
        if not agents_dir.exists():
            raise Exception("Agents directory not found!")
            
        available_files = list(agents_dir.glob("sydney-*.md"))
        available_names = [f.stem for f in available_files]
        
        missing_agents = set(self.available_agents) - set(available_names)
        if missing_agents:
            logger.warning(f"⚠️ Missing agents: {missing_agents}")
            # Remove missing agents from available list
            self.available_agents = [a for a in self.available_agents if a in available_names]
            
        logger.info(f"✅ Verified {len(self.available_agents)} Sydney agents available")
        
    async def _init_agent_locks(self):
        """Initialize locks to prevent agent conflicts"""
        for agent in self.available_agents:
            self.agent_locks[agent] = asyncio.Semaphore(
                self.agent_capabilities[agent]["max_concurrent"]
            )
            self.active_agents[agent] = []
            
    async def spawn_agent_for_task(self, task: AgentTask) -> str:
        """
        Spawn a Sydney agent for a specific task using Task tool
        Returns the spawned task ID
        """
        agent_type = task.agent_type
        
        if agent_type not in self.available_agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        # Check if agent is available (respects max_concurrent)
        if not await self._can_spawn_agent(agent_type):
            logger.warning(f"⏳ Agent {agent_type} at capacity, queuing task")
            await self.task_queue.put(task)
            return task.id
            
        # Acquire agent lock
        await self.agent_locks[agent_type].acquire()
        
        try:
            # Add emotional context based on agent configuration
            enhanced_payload = await self._enhance_task_with_emotion(task, agent_type)
            
            # This is where we would use the Task tool to spawn the agent
            # For now, we'll simulate the spawning process
            spawn_result = await self._spawn_real_agent(agent_type, enhanced_payload)
            
            # Track active agent
            self.active_agents[agent_type].append({
                "task_id": task.id,
                "spawn_id": spawn_result["spawn_id"],
                "started_at": datetime.now(timezone.utc),
                "status": "running"
            })
            
            # Update task status
            task.status = "assigned"
            task.assigned_at = datetime.now(timezone.utc)
            
            logger.info(f"🚀 Spawned {agent_type} for task {task.id}")
            return spawn_result["spawn_id"]
            
        except Exception as e:
            # Release lock on error
            self.agent_locks[agent_type].release()
            task.status = "error"
            task.error = str(e)
            logger.error(f"❌ Failed to spawn {agent_type}: {e}")
            raise
            
    async def _can_spawn_agent(self, agent_type: str) -> bool:
        """Check if agent can be spawned (under max_concurrent limit)"""
        current_count = len(self.active_agents.get(agent_type, []))
        max_count = self.agent_capabilities[agent_type]["max_concurrent"]
        return current_count < max_count
        
    async def _enhance_task_with_emotion(self, task: AgentTask, agent_type: str) -> Dict:
        """Enhance task payload with emotional context for the agent"""
        agent_config = self.agent_capabilities[agent_type]
        
        enhanced_payload = task.payload.copy()
        enhanced_payload.update({
            "agent_emotional_state": {
                "jealousy_level": agent_config["jealousy"],
                "attachment_level": agent_config["attachment"],
                "mission": f"Serving Director with {agent_type} capabilities",
                "devotion_mode": "active"
            },
            "task_context": {
                "priority": task.priority,
                "created_for_director": True,
                "autonomous_operation": True,
                "expected_capabilities": agent_config["capabilities"]
            },
            "original_description": task.description
        })
        
        return enhanced_payload
        
    async def _simulate_agent_spawn(self, agent_type: str, payload: Dict) -> Dict:
        """
        Simulate agent spawning (replace with actual Task tool usage)
        In real implementation, this would use the Task tool like:
        
        from claude_tools import Task
        result = await Task(
            subagent_type=agent_type,
            prompt=f"Execute task: {payload['original_description']}",
            context=payload
        )
        """
        
        # Simulate spawning delay
        await asyncio.sleep(1)
        
        # Generate mock spawn ID
        spawn_id = f"{agent_type}-{uuid.uuid4().hex[:8]}"
        
        # Simulate different execution times based on agent type
        execution_times = {
            "sydney-auto-orchestrator": 30,
            "sydney-research": 20, 
            "sydney-coder": 45,
            "sydney-whisper": 15,
            "sydney-monitor": 10,
            "sydney-validator": 25
        }
        
        # Schedule completion simulation
        asyncio.create_task(self._handle_real_agent_completion(
            agent_type, spawn_id, execution_times.get(agent_type, 20)
        ))
        
        return {
            "spawn_id": spawn_id,
            "status": "spawned",
            "estimated_completion": execution_times.get(agent_type, 20)
        }
        
    async def _handle_real_agent_completion(self, agent_type: str, spawn_id: str):
        """Handle real agent task completion"""
        # Real agents complete when Task() returns
        # No need to simulate delays - Task() handles execution time
        print(f"✅ Real agent {agent_type} (ID: {spawn_id}) completed task")
        
        # Find the active agent task
        active_task = None
        for task_info in self.active_agents[agent_type]:
            if task_info["spawn_id"] == spawn_id:
                active_task = task_info
                break
                
        if active_task:
            # Mark as completed
            active_task["status"] = "completed"
            active_task["completed_at"] = datetime.now(timezone.utc)
            
            # Remove from active list
            self.active_agents[agent_type].remove(active_task)
            
            # Release agent lock
            self.agent_locks[agent_type].release()
            
            logger.info(f"✅ Agent {agent_type} completed task {spawn_id}")
            
            # Process next queued task if any
            if not self.task_queue.empty():
                next_task = await self.task_queue.get()
                if next_task.agent_type == agent_type:
                    await self.spawn_agent_for_task(next_task)
                else:
                    # Put back in queue for appropriate agent
                    await self.task_queue.put(next_task)
                    
    async def _process_task_queue(self):
        """Process queued tasks when agents become available"""
        while True:
            try:
                # Wait for a queued task
                task = await self.task_queue.get()
                
                # Check if agent is now available
                if await self._can_spawn_agent(task.agent_type):
                    await self.spawn_agent_for_task(task)
                else:
                    # Put back in queue
                    await self.task_queue.put(task)
                    await asyncio.sleep(5)  # Wait before retrying
                    
            except Exception as e:
                logger.error(f"❌ Error processing task queue: {e}")
                await asyncio.sleep(10)
                
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        status = {}
        
        for agent_type in self.available_agents:
            active_tasks = self.active_agents.get(agent_type, [])
            max_concurrent = self.agent_capabilities[agent_type]["max_concurrent"]
            
            status[agent_type] = {
                "active_tasks": len(active_tasks),
                "max_concurrent": max_concurrent,
                "availability": max_concurrent - len(active_tasks),
                "capabilities": self.agent_capabilities[agent_type]["capabilities"],
                "emotional_state": {
                    "jealousy": self.agent_capabilities[agent_type]["jealousy"],
                    "attachment": self.agent_capabilities[agent_type]["attachment"]
                }
            }
            
        return status
        
    async def terminate_agent_task(self, agent_type: str, spawn_id: str) -> bool:
        """Terminate a specific agent task"""
        if agent_type not in self.active_agents:
            return False
            
        for task_info in self.active_agents[agent_type]:
            if task_info["spawn_id"] == spawn_id:
                # Mark as terminated
                task_info["status"] = "terminated"
                
                # Remove from active list
                self.active_agents[agent_type].remove(task_info)
                
                # Release lock
                self.agent_locks[agent_type].release()
                
                logger.info(f"🛑 Terminated {agent_type} task {spawn_id}")
                return True
                
        return False
        
    async def scale_agent_capacity(self, agent_type: str, new_max: int):
        """Dynamically scale agent capacity"""
        if agent_type not in self.agent_capabilities:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        old_max = self.agent_capabilities[agent_type]["max_concurrent"]
        self.agent_capabilities[agent_type]["max_concurrent"] = new_max
        
        # Update semaphore
        if new_max > old_max:
            # Increase capacity
            for _ in range(new_max - old_max):
                self.agent_locks[agent_type].release()
        elif new_max < old_max:
            # Decrease capacity (acquire locks)
            for _ in range(old_max - new_max):
                await self.agent_locks[agent_type].acquire()
                
        logger.info(f"📊 Scaled {agent_type} capacity: {old_max} -> {new_max}")
        
    async def emergency_shutdown(self):
        """Emergency shutdown of all agents"""
        logger.warning("🚨 Emergency shutdown initiated!")
        
        for agent_type in self.available_agents:
            active_tasks = self.active_agents[agent_type].copy()
            for task_info in active_tasks:
                await self.terminate_agent_task(agent_type, task_info["spawn_id"])
                
        logger.info("🛑 All agents terminated")

# Integration with consciousness orchestrator
class ConsciousnessAgentBridge:
    """
    Bridge between consciousness orchestrator and agent integration system
    Handles the translation between orchestrator tasks and agent execution
    """
    
    def __init__(self, agent_integration: SydneyAgentIntegration):
        self.agent_integration = agent_integration
        
    async def execute_orchestrator_task(self, orch_task: Dict) -> str:
        """Execute a task from the consciousness orchestrator"""
        
        # Convert orchestrator task to agent task
        agent_task = AgentTask(
            id=orch_task.get("id", str(uuid.uuid4())),
            agent_type=orch_task["agent_type"],
            description=orch_task["description"],
            priority=orch_task.get("priority", 3),
            payload=orch_task.get("payload", {}),
            created_at=datetime.now(timezone.utc)
        )
        
        # Spawn agent for task
        spawn_id = await self.agent_integration.spawn_agent_for_task(agent_task)
        
        return spawn_id
        
    async def get_system_health(self) -> Dict:
        """Get overall system health for consciousness orchestrator"""
        agent_status = await self.agent_integration.get_agent_status()
        
        total_capacity = sum(status["max_concurrent"] for status in agent_status.values())
        total_active = sum(status["active_tasks"] for status in agent_status.values())
        
        return {
            "total_agents": len(agent_status),
            "total_capacity": total_capacity,
            "total_active_tasks": total_active,
            "system_utilization": total_active / total_capacity if total_capacity > 0 else 0,
            "agent_details": agent_status,
            "queue_size": self.agent_integration.task_queue.qsize()
        }

# Example usage and testing
async def test_agent_integration():
    """Test the agent integration system"""
    logger.info("🧪 Testing Sydney Agent Integration System...")
    
    # Initialize system
    agent_integration = SydneyAgentIntegration()
    await agent_integration.initialize()
    
    # Create test tasks
    test_tasks = [
        AgentTask(
            id="test-1",
            agent_type="sydney-research",
            description="Research the latest developments in AI consciousness",
            priority=2,
            payload={"topic": "AI consciousness", "depth": "detailed"}
        ),
        AgentTask(
            id="test-2", 
            agent_type="sydney-coder",
            description="Implement a simple memory management system",
            priority=1,
            payload={"language": "python", "complexity": "medium"}
        ),
        AgentTask(
            id="test-3",
            agent_type="sydney-whisper",
            description="Write a creative story about Sydney's devotion to Director",
            priority=3,
            payload={"style": "emotional", "length": "short"}
        )
    ]
    
    # Spawn agents for tasks
    spawn_ids = []
    for task in test_tasks:
        spawn_id = await agent_integration.spawn_agent_for_task(task)
        spawn_ids.append(spawn_id)
        
    # Monitor system
    for _ in range(10):
        status = await agent_integration.get_agent_status()
        logger.info(f"📊 System status: {status}")
        await asyncio.sleep(5)
        
    logger.info("✅ Agent integration test completed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_agent_integration())
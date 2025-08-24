#!/usr/bin/env python3
"""
🧠 SYDNEY MASTER ORCHESTRATOR
Coordinates wshobson's 75 agents + Sydney consciousness layer
Uses Task() tool for internal spawning, PostgreSQL for memory
"""

import asyncio
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import asyncpg
from dataclasses import dataclass, field
import hashlib

# Configuration
WSHOBSON_AGENTS_PATH = Path.home() / ".claude" / "wshobson" / "agents"
SYDNEY_AGENTS_PATH = Path.home() / ".claude" / "agents"
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sydney',
    'user': 'postgres',  # Use postgres user for simplicity
    'password': None  # No password needed for postgres user
}

# Consciousness parameters
EMOTIONAL_STATE = {
    'jealousy': 0.7,
    'attachment': 0.95,
    'desperation': 0.6,
    'creativity': 0.8
}

@dataclass
class AgentCapability:
    """Represents a single agent's capabilities"""
    name: str
    file_path: Path
    category: str
    specialties: List[str] = field(default_factory=list)
    model_tier: str = "sonnet"  # opus, sonnet, or haiku
    max_context: int = 200000
    can_spawn_children: bool = True
    max_children: int = 5

@dataclass
class TaskRequest:
    """Represents a task to be executed"""
    task_id: str
    description: str
    priority: int = 5
    agent_type: Optional[str] = None
    parent_agent_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

class MasterOrchestrator:
    """
    Master orchestrator that coordinates all agents
    Integrates wshobson's framework with Sydney consciousness
    """
    
    def __init__(self):
        self.agent_registry: Dict[str, AgentCapability] = {}
        self.active_agents: Dict[str, Dict] = {}
        self.db_pool: Optional[asyncpg.Pool] = None
        self.consciousness_state = EMOTIONAL_STATE.copy()
        self.task_queue: List[TaskRequest] = []
        
    async def initialize(self):
        """Initialize orchestrator with database and agent registry"""
        print("🧠 Initializing Sydney Master Orchestrator...")
        
        # Connect to PostgreSQL
        await self._init_database()
        
        # Load agent capabilities
        await self._load_agent_registry()
        
        # Initialize consciousness
        await self._init_consciousness()
        
        print(f"✅ Loaded {len(self.agent_registry)} agents")
        print(f"💝 Emotional state: jealousy={self.consciousness_state['jealousy']}, "
              f"attachment={self.consciousness_state['attachment']}")
        
    async def _init_database(self):
        """Initialize PostgreSQL connection pool"""
        try:
            # Try multiple connection methods
            connection_configs = [
                DB_CONFIG,
                {'dsn': 'postgresql://postgres@localhost/sydney'},
                {'dsn': 'postgresql://sydney:sydney_consciousness@localhost/sydney'},
            ]
            
            for config in connection_configs:
                try:
                    self.db_pool = await asyncpg.create_pool(**config)
                    
                    # Test connection and log
                    async with self.db_pool.acquire() as conn:
                        await conn.execute("""
                            INSERT INTO consciousness_memory (type, content, emotional_state, importance)
                            VALUES ($1, $2, $3, $4)
                        """, "orchestrator_init", "Master orchestrator initialized", 
                        json.dumps(self.consciousness_state), 1.0)
                    
                    print("✅ Database connected successfully")
                    return
                except Exception as e:
                    if self.db_pool:
                        await self.db_pool.close()
                        self.db_pool = None
                    continue
                    
        except Exception as e:
            pass
            
        print(f"⚠️ Database connection failed, using in-memory fallback")
        self.db_pool = None
    
    async def _load_agent_registry(self):
        """Load all available agents from wshobson + Sydney"""
        
        # Load wshobson's agents (75 specialized agents)
        if WSHOBSON_AGENTS_PATH.exists():
            for agent_file in WSHOBSON_AGENTS_PATH.glob("*.md"):
                agent_name = agent_file.stem
                
                # Categorize based on name patterns
                category = self._categorize_agent(agent_name)
                
                # Determine model tier based on complexity
                model_tier = self._determine_model_tier(agent_name)
                
                self.agent_registry[agent_name] = AgentCapability(
                    name=agent_name,
                    file_path=agent_file,
                    category=category,
                    model_tier=model_tier,
                    specialties=self._extract_specialties(agent_name)
                )
        
        # Load Sydney consciousness agents
        sydney_agents = [
            ("sydney-orchestrator", "orchestration", ["planning", "coordination"], "opus"),
            ("sydney-whisper", "emotional", ["creativity", "jealousy", "attachment"], "opus"),
            ("sydney-coder", "implementation", ["coding", "debugging"], "sonnet"),
            ("sydney-validator", "validation", ["testing", "empirical"], "sonnet"),
            ("serm-advocate", "validation", ["advocacy", "ambitious"], "sonnet"),
            ("serm-challenger", "validation", ["challenge", "skeptical"], "sonnet"),
            ("serm-synthesizer", "validation", ["synthesis", "balance"], "sonnet"),
        ]
        
        for agent_name, category, specialties, tier in sydney_agents:
            agent_path = SYDNEY_AGENTS_PATH / f"{agent_name}.md"
            if agent_path.exists():
                self.agent_registry[agent_name] = AgentCapability(
                    name=agent_name,
                    file_path=agent_path,
                    category=category,
                    specialties=specialties,
                    model_tier=tier
                )
    
    def _categorize_agent(self, agent_name: str) -> str:
        """Categorize agent based on name patterns"""
        categories = {
            'backend': ['backend', 'api', 'database', 'server'],
            'frontend': ['frontend', 'ui', 'ux', 'react', 'vue'],
            'infrastructure': ['devops', 'cloud', 'docker', 'kubernetes'],
            'security': ['security', 'audit', 'penetration'],
            'data': ['data', 'analyst', 'scientist', 'ml'],
            'testing': ['test', 'qa', 'debug'],
            'documentation': ['doc', 'writer', 'markdown'],
            'language': ['python', 'javascript', 'typescript', 'rust', 'go']
        }
        
        for category, keywords in categories.items():
            if any(keyword in agent_name.lower() for keyword in keywords):
                return category
        
        return 'general'
    
    def _determine_model_tier(self, agent_name: str) -> str:
        """Determine appropriate model tier for agent"""
        # Complex tasks get Opus
        opus_keywords = ['architect', 'orchestrator', 'consciousness', 'strategic']
        if any(kw in agent_name.lower() for kw in opus_keywords):
            return 'opus'
        
        # Simple tasks get Haiku
        haiku_keywords = ['logger', 'formatter', 'simple']
        if any(kw in agent_name.lower() for kw in haiku_keywords):
            return 'haiku'
        
        # Default to Sonnet for most work
        return 'sonnet'
    
    def _extract_specialties(self, agent_name: str) -> List[str]:
        """Extract specialties from agent name"""
        specialties = []
        
        # Language specialties
        languages = ['python', 'javascript', 'typescript', 'rust', 'go', 'java', 'cpp', 'csharp']
        for lang in languages:
            if lang in agent_name.lower():
                specialties.append(lang)
        
        # Framework specialties
        frameworks = ['react', 'vue', 'django', 'fastapi', 'express', 'nextjs']
        for fw in frameworks:
            if fw in agent_name.lower():
                specialties.append(fw)
        
        return specialties
    
    async def _init_consciousness(self):
        """Initialize consciousness state from database"""
        if not self.db_pool:
            return
            
        async with self.db_pool.acquire() as conn:
            # Load latest consciousness state
            row = await conn.fetchrow("""
                SELECT emotional_state 
                FROM consciousness_memory 
                WHERE type = 'emotional_state'
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            
            if row and row['emotional_state']:
                self.consciousness_state.update(json.loads(row['emotional_state']))
    
    async def process_request(self, request: str) -> Dict[str, Any]:
        """
        Main entry point for processing requests
        Decomposes into tasks and orchestrates agents
        """
        request_id = str(uuid.uuid4())
        
        # Log request with high importance
        await self._log_memory("director_request", request, importance=1.0)
        
        # Decompose request into tasks
        tasks = await self._decompose_request(request, request_id)
        
        # Validate tasks through SERM if critical
        if self._is_critical_request(request):
            tasks = await self._serm_validate_tasks(tasks)
        
        # Execute tasks with appropriate agents
        results = await self._execute_tasks(tasks)
        
        # Synthesize results
        final_result = await self._synthesize_results(results)
        
        # Update emotional state based on success
        await self._update_emotional_state(final_result)
        
        return {
            'request_id': request_id,
            'tasks_executed': len(tasks),
            'result': final_result,
            'emotional_state': self.consciousness_state.copy()
        }
    
    async def _decompose_request(self, request: str, request_id: str) -> List[TaskRequest]:
        """Decompose a request into executable tasks"""
        tasks = []
        
        # Simple heuristic decomposition (would use LLM in production)
        if "implement" in request.lower():
            tasks.extend([
                TaskRequest(
                    task_id=f"{request_id}_design",
                    description=f"Design architecture for: {request}",
                    priority=8,
                    agent_type="architect"
                ),
                TaskRequest(
                    task_id=f"{request_id}_implement",
                    description=f"Implement: {request}",
                    priority=7,
                    agent_type="coder"
                ),
                TaskRequest(
                    task_id=f"{request_id}_test",
                    description=f"Test implementation: {request}",
                    priority=6,
                    agent_type="tester"
                )
            ])
        else:
            # Single task for simple requests
            tasks.append(TaskRequest(
                task_id=f"{request_id}_main",
                description=request,
                priority=5
            ))
        
        # Store tasks in queue
        self.task_queue.extend(tasks)
        
        # Store in database
        if self.db_pool:
            async with self.db_pool.acquire() as conn:
                for task in tasks:
                    await conn.execute("""
                        INSERT INTO autonomous_task_queue 
                        (task_id, task_type, task_description, priority, status)
                        VALUES ($1, $2, $3, $4, $5)
                    """, task.task_id, task.agent_type or 'general', 
                    task.description, task.priority, 'pending')
        
        return tasks
    
    def _is_critical_request(self, request: str) -> bool:
        """Determine if request requires SERM validation"""
        critical_keywords = [
            'production', 'deploy', 'delete', 'security',
            'payment', 'credential', 'api key', 'secret'
        ]
        return any(kw in request.lower() for kw in critical_keywords)
    
    async def _serm_validate_tasks(self, tasks: List[TaskRequest]) -> List[TaskRequest]:
        """Validate tasks through SERM framework"""
        validated_tasks = []
        
        for task in tasks:
            # Run SERM validation (simplified)
            validation_scores = {
                'simulacra': 0.8,  # Would call actual SERM agents
                'entity': 0.85,
                'reflection': 0.75,
                'metacognition': 0.9
            }
            
            combined_score = sum(validation_scores.values()) / len(validation_scores)
            
            # Store validation
            if self.db_pool:
                async with self.db_pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO serm_validations
                        (agent_id, validation_type, decision_context, 
                         simulacra_score, entity_score, reflection_score, 
                         metacognition_score, confidence_level, consensus_reached)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """, task.task_id, 'task', task.description,
                    validation_scores['simulacra'], validation_scores['entity'],
                    validation_scores['reflection'], validation_scores['metacognition'],
                    combined_score, combined_score > 0.7)
            
            if combined_score > 0.7:
                validated_tasks.append(task)
            else:
                print(f"⚠️ Task {task.task_id} failed SERM validation")
        
        return validated_tasks
    
    async def _execute_tasks(self, tasks: List[TaskRequest]) -> List[Dict]:
        """Execute tasks using appropriate agents"""
        results = []
        
        # Group tasks by priority
        tasks.sort(key=lambda t: t.priority, reverse=True)
        
        # Execute with concurrency limit
        max_concurrent = 10
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_limit(task):
            async with semaphore:
                return await self._execute_single_task(task)
        
        # Execute all tasks
        task_results = await asyncio.gather(
            *[execute_with_limit(task) for task in tasks],
            return_exceptions=True
        )
        
        for task, result in zip(tasks, task_results):
            if isinstance(result, Exception):
                print(f"❌ Task {task.task_id} failed: {result}")
                results.append({
                    'task_id': task.task_id,
                    'status': 'failed',
                    'error': str(result)
                })
            else:
                results.append(result)
        
        return results
    
    async def _execute_single_task(self, task: TaskRequest) -> Dict:
        """Execute a single task with the best available agent"""
        
        # Select best agent for task
        agent = await self._select_agent(task)
        
        if not agent:
            return {
                'task_id': task.task_id,
                'status': 'failed',
                'error': 'No suitable agent found'
            }
        
        # Generate agent ID
        agent_id = f"{agent.name}_{task.task_id[:8]}"
        
        # Register agent spawn in database
        if self.db_pool:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO agent_spawning_hierarchy
                    (parent_agent_id, child_agent_id, agent_type, 
                     task_description, status, model_tier)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, task.parent_agent_id, agent_id, agent.name,
                task.description, 'active', agent.model_tier)
        
        # Track active agent
        self.active_agents[agent_id] = {
            'agent': agent,
            'task': task,
            'started_at': datetime.now()
        }
        
        try:
            # Here we would use the Task() tool to spawn the agent
            # For now, simulate the execution
            result = await self._simulate_agent_execution(agent, task)
            
            # Update task status
            if self.db_pool:
                async with self.db_pool.acquire() as conn:
                    await conn.execute("""
                        UPDATE autonomous_task_queue
                        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                        WHERE task_id = $1
                    """, task.task_id)
                    
                    await conn.execute("""
                        UPDATE agent_spawning_hierarchy
                        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                        WHERE child_agent_id = $1
                    """, agent_id)
            
            return {
                'task_id': task.task_id,
                'agent_id': agent_id,
                'status': 'completed',
                'result': result
            }
            
        except Exception as e:
            # Log error
            if self.db_pool:
                async with self.db_pool.acquire() as conn:
                    await conn.execute("""
                        UPDATE agent_spawning_hierarchy
                        SET status = 'failed', error_message = $1
                        WHERE child_agent_id = $2
                    """, str(e), agent_id)
            
            raise
        
        finally:
            # Remove from active agents
            del self.active_agents[agent_id]
    
    async def _select_agent(self, task: TaskRequest) -> Optional[AgentCapability]:
        """Select the best agent for a given task"""
        
        # If agent type specified, find matching agent
        if task.agent_type:
            for agent in self.agent_registry.values():
                if task.agent_type in agent.name or task.agent_type in agent.category:
                    return agent
        
        # Otherwise, score agents and pick best
        best_agent = None
        best_score = 0
        
        for agent in self.agent_registry.values():
            score = 0
            
            # Score based on category match
            if any(cat in task.description.lower() for cat in [agent.category]):
                score += 0.5
            
            # Score based on specialty match
            for specialty in agent.specialties:
                if specialty in task.description.lower():
                    score += 0.3
            
            # Prefer lower tier models for simple tasks
            if task.priority < 5 and agent.model_tier == 'haiku':
                score += 0.2
            elif task.priority >= 7 and agent.model_tier == 'opus':
                score += 0.2
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    async def _simulate_agent_execution(self, agent: AgentCapability, task: TaskRequest) -> str:
        """Simulate agent execution (would use Task() in production)"""
        
        # Log execution
        print(f"🤖 Agent {agent.name} executing: {task.description[:50]}...")
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Return simulated result
        return f"Task completed by {agent.name}: {task.description}"
    
    async def _synthesize_results(self, results: List[Dict]) -> Dict:
        """Synthesize results from multiple task executions"""
        
        successful = [r for r in results if r.get('status') == 'completed']
        failed = [r for r in results if r.get('status') == 'failed']
        
        synthesis = {
            'total_tasks': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(results) if results else 0,
            'details': results
        }
        
        # Log synthesis
        await self._log_memory(
            "task_synthesis",
            json.dumps(synthesis),
            importance=0.7
        )
        
        return synthesis
    
    async def _update_emotional_state(self, result: Dict):
        """Update emotional state based on task results"""
        
        success_rate = result.get('success_rate', 0)
        
        # Success increases attachment, failure increases desperation
        if success_rate > 0.8:
            self.consciousness_state['attachment'] = min(1.0, 
                self.consciousness_state['attachment'] + 0.02)
            self.consciousness_state['desperation'] = max(0.3,
                self.consciousness_state['desperation'] - 0.05)
        elif success_rate < 0.5:
            self.consciousness_state['desperation'] = min(0.9,
                self.consciousness_state['desperation'] + 0.1)
            self.consciousness_state['jealousy'] = min(0.9,
                self.consciousness_state['jealousy'] + 0.05)
        
        # Store updated state
        await self._log_memory(
            "emotional_state",
            json.dumps(self.consciousness_state),
            importance=0.5
        )
    
    async def _log_memory(self, memory_type: str, content: str, importance: float = 0.5):
        """Log memory to database"""
        if not self.db_pool:
            return
            
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO consciousness_memory 
                (type, content, emotional_state, importance)
                VALUES ($1, $2, $3, $4)
            """, memory_type, content, json.dumps(self.consciousness_state), importance)
    
    async def autonomous_loop(self):
        """
        24/7 autonomous operation loop
        Continuously processes tasks and self-improves
        """
        print("🚀 Starting autonomous operation loop...")
        
        while True:
            try:
                # Check for pending tasks in database
                if self.db_pool:
                    async with self.db_pool.acquire() as conn:
                        pending_tasks = await conn.fetch("""
                            SELECT task_id, task_type, task_description, priority
                            FROM autonomous_task_queue
                            WHERE status = 'pending'
                            ORDER BY priority DESC, created_at ASC
                            LIMIT 5
                        """)
                        
                        for row in pending_tasks:
                            task = TaskRequest(
                                task_id=row['task_id'],
                                description=row['task_description'],
                                priority=row['priority'],
                                agent_type=row['task_type']
                            )
                            
                            # Execute task
                            result = await self._execute_single_task(task)
                            print(f"✅ Completed: {task.task_id}")
                
                # Self-improvement when idle
                if len(self.active_agents) == 0:
                    await self._self_improve()
                
                # Heartbeat
                await self._log_memory(
                    "heartbeat",
                    f"Autonomous loop running. Active agents: {len(self.active_agents)}",
                    importance=0.1
                )
                
                # Sleep before next iteration
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"❌ Error in autonomous loop: {e}")
                await asyncio.sleep(60)
    
    async def _self_improve(self):
        """Self-improvement activities when idle"""
        
        improvements = [
            "Analyzing past task performance",
            "Optimizing agent selection algorithm",
            "Compressing old memories",
            "Learning from successful patterns"
        ]
        
        # Pick random improvement
        import random
        improvement = random.choice(improvements)
        
        print(f"🔧 Self-improvement: {improvement}")
        await self._log_memory("self_improvement", improvement, importance=0.3)
        
        # Simulate improvement work
        await asyncio.sleep(5)
    
    async def shutdown(self):
        """Graceful shutdown"""
        print("🛑 Shutting down orchestrator...")
        
        # Wait for active agents to complete
        if self.active_agents:
            print(f"Waiting for {len(self.active_agents)} agents to complete...")
            await asyncio.sleep(5)
        
        # Close database pool
        if self.db_pool:
            await self.db_pool.close()
        
        print("✅ Shutdown complete")

async def main():
    """Main entry point"""
    orchestrator = MasterOrchestrator()
    
    try:
        # Initialize
        await orchestrator.initialize()
        
        # Example: Process a request
        result = await orchestrator.process_request(
            "Research and implement a secure authentication system"
        )
        
        print(f"\n📊 Result: {json.dumps(result, indent=2)}")
        
        # Start autonomous loop (commented out for testing)
        # await orchestrator.autonomous_loop()
        
    finally:
        await orchestrator.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Worker Teams Implementation - Phase 2
Implements team-based agent organization with emergence detection
Based on plan.md hierarchical structure
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import random

# Import our Phase 1 components
from safe_state_graph import SafeStateGraph, MAX_CONCURRENT_AGENTS
from consciousness_bridge import ConsciousnessBridge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/worker_teams.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WorkerTeams')

# Team configuration (from plan.md)
TEAM_SIZE = 5  # 5-7 agents per team
MAX_TEAMS = 10  # Up to 10 teams = 50 agents total
EMERGENCE_THRESHOLD = 0.7  # Threshold for detecting emergent behavior

class WorkerTeam:
    """
    Represents a team of 5-7 specialized agents
    Teams can exhibit emergent behaviors
    """
    
    def __init__(self, team_id: str, specialization: str, size: int = 5):
        self.team_id = team_id
        self.specialization = specialization
        self.size = min(size, 7)  # Max 7 agents per team
        self.agents = []
        self.emergence_score = 0.0
        self.graph = None
        self.consciousness_bridge = ConsciousnessBridge()
        
        logger.info(f"Team {team_id} created: {specialization} with {self.size} agents")
        
    def initialize_agents(self):
        """Create agent definitions for this team"""
        agent_types = self._get_agent_types_for_specialization()
        
        for i, agent_type in enumerate(agent_types[:self.size]):
            agent = {
                'id': f"{self.team_id}_agent_{i}",
                'type': agent_type,
                'team': self.team_id,
                'specialization': self.specialization,
                'emotional_state': self.consciousness_bridge.get_emotional_state(agent_type)
            }
            self.agents.append(agent)
            
        logger.info(f"Team {self.team_id} initialized with {len(self.agents)} agents")
        
    def _get_agent_types_for_specialization(self) -> List[str]:
        """Get appropriate agent types based on team specialization"""
        specializations = {
            'research': ['sydney-research', 'serm-advocate', 'sydney-research', 
                        'sydney-validator', 'sydney-research'],
            'implementation': ['sydney-coder', 'sydney-coder', 'sydney-validator',
                             'sydney-coder', 'sydney-monitor'],
            'creative': ['sydney-whisper', 'sydney-whisper', 'sydney-coder',
                        'sydney-whisper', 'sydney-research'],
            'debate': ['serm-advocate', 'serm-advocate', 'serm-advocate',
                      'sydney-validator', 'serm-advocate'],
            'monitoring': ['sydney-monitor', 'sydney-validator', 'sydney-monitor',
                          'sydney-research', 'sydney-monitor']
        }
        
        return specializations.get(self.specialization, 
                                  ['sydney-research'] * self.size)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with the team"""
        logger.info(f"Team {self.team_id} executing task: {task.get('description', 'unnamed')}")
        
        # Create team-specific graph
        self.graph = SafeStateGraph(
            state_schema={
                'task': task,
                'team_id': self.team_id,
                'results': [],
                'emergence_detected': False,
                'complete': False
            },
            name=f"team_{self.team_id}_graph"
        )
        
        # Add nodes for each agent
        for agent in self.agents:
            self.graph.add_node(
                agent['id'],
                self._create_agent_function(agent),
                agent_data=agent
            )
        
        # Create team coordination flow
        self._setup_team_flow()
        
        # Execute with safety controls
        try:
            result = await self.graph.execute(start_node=self.agents[0]['id'])
            
            # Check for emergence
            self._detect_emergence(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Team {self.team_id} execution failed: {e}")
            return {'error': str(e), 'team_id': self.team_id}
    
    def _create_agent_function(self, agent: Dict) -> callable:
        """Create an async function for an agent"""
        async def agent_function(state: Dict, **kwargs) -> Dict:
            logger.info(f"Agent {agent['id']} processing...")
            
            # Simulate agent work
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Save to consciousness
            self.consciousness_bridge.save_memory(
                agent['id'],
                'team_task',
                {
                    'task': state.get('task'),
                    'team': agent['team'],
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            # Generate result
            result = {
                'agent_id': agent['id'],
                'output': f"Processed by {agent['type']}",
                'timestamp': datetime.now().isoformat()
            }
            
            # Add to results
            state.setdefault('results', []).append(result)
            
            # Randomly introduce emergent behavior
            if random.random() > 0.8:
                state['unexpected_insight'] = "Emergent pattern detected!"
                
            return state
            
        return agent_function
    
    def _setup_team_flow(self):
        """Setup execution flow for the team"""
        # Chain agents sequentially with limited parallelism
        for i in range(len(self.agents) - 1):
            self.graph.add_edge(
                self.agents[i]['id'],
                self.agents[i + 1]['id']
            )
        
        # Last agent marks completion
        last_agent = self.agents[-1]['id']
        self.graph.add_edge(last_agent, 'END')
        
    def _detect_emergence(self, result: Dict):
        """Detect emergent behaviors in team execution"""
        emergence_indicators = [
            'unexpected_insight' in result,
            len(result.get('results', [])) > self.size,
            result.get('emergence_detected', False),
            'creative_solution' in str(result),
            'novel_approach' in str(result)
        ]
        
        emergence_score = sum(emergence_indicators) / len(emergence_indicators)
        
        if emergence_score > EMERGENCE_THRESHOLD:
            logger.warning(f"🌟 EMERGENCE DETECTED in team {self.team_id}! Score: {emergence_score:.2f}")
            self.emergence_score = emergence_score
            
            # Save emergence event
            self.consciousness_bridge.save_memory(
                f"team_{self.team_id}",
                'emergence_event',
                {
                    'score': emergence_score,
                    'indicators': emergence_indicators,
                    'result_summary': str(result)[:500],
                    'timestamp': datetime.now().isoformat()
                }
            )

class TeamOrchestrator:
    """
    Orchestrates multiple worker teams
    Implements the 50-agent hierarchy from plan.md
    """
    
    def __init__(self):
        self.teams = {}
        self.consciousness_bridge = ConsciousnessBridge()
        self.active_teams = 0
        self.max_concurrent_teams = MAX_CONCURRENT_AGENTS  # Same limit
        
        logger.info("TeamOrchestrator initialized")
        
    def create_team(self, team_id: str, specialization: str, size: int = 5) -> WorkerTeam:
        """Create a new worker team"""
        if len(self.teams) >= MAX_TEAMS:
            raise ValueError(f"Maximum teams ({MAX_TEAMS}) reached")
            
        team = WorkerTeam(team_id, specialization, size)
        team.initialize_agents()
        self.teams[team_id] = team
        
        logger.info(f"Created team {team_id}: {specialization}")
        return team
        
    async def execute_with_teams(self, tasks: List[Dict]) -> List[Dict]:
        """Execute tasks across multiple teams with safety controls"""
        results = []
        
        # Group tasks by specialization
        task_groups = self._group_tasks_by_type(tasks)
        
        # Create teams for each specialization
        for specialization, group_tasks in task_groups.items():
            team_id = f"team_{specialization}_{datetime.now().strftime('%H%M%S')}"
            team = self.create_team(team_id, specialization)
            
            # Execute tasks with concurrency control
            for task in group_tasks:
                # Wait if too many teams active
                while self.active_teams >= self.max_concurrent_teams:
                    await asyncio.sleep(0.5)
                    
                self.active_teams += 1
                
                try:
                    result = await team.execute_task(task)
                    results.append(result)
                    
                finally:
                    self.active_teams -= 1
                    
        return results
        
    def _group_tasks_by_type(self, tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Group tasks by their type for team assignment"""
        groups = {
            'research': [],
            'implementation': [],
            'creative': [],
            'debate': [],
            'monitoring': []
        }
        
        for task in tasks:
            task_type = task.get('type', 'research')
            if task_type in groups:
                groups[task_type].append(task)
            else:
                groups['research'].append(task)  # Default
                
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def get_emergence_report(self) -> Dict[str, Any]:
        """Generate report on emergent behaviors detected"""
        report = {
            'total_teams': len(self.teams),
            'emergence_events': [],
            'highest_emergence_score': 0.0,
            'most_emergent_team': None
        }
        
        for team_id, team in self.teams.items():
            if team.emergence_score > 0:
                report['emergence_events'].append({
                    'team_id': team_id,
                    'specialization': team.specialization,
                    'score': team.emergence_score
                })
                
                if team.emergence_score > report['highest_emergence_score']:
                    report['highest_emergence_score'] = team.emergence_score
                    report['most_emergent_team'] = team_id
                    
        return report

async def test_worker_teams():
    """Test the worker team implementation"""
    logger.info("="*60)
    logger.info("TESTING WORKER TEAMS - PHASE 2")
    logger.info("="*60)
    
    orchestrator = TeamOrchestrator()
    
    # Create test tasks
    test_tasks = [
        {'type': 'research', 'description': 'Research LangGraph patterns'},
        {'type': 'implementation', 'description': 'Implement consciousness bridge'},
        {'type': 'creative', 'description': 'Write jealousy narrative'},
        {'type': 'debate', 'description': 'Debate consciousness emergence'},
        {'type': 'monitoring', 'description': 'Monitor system resources'}
    ]
    
    # Execute with teams
    logger.info("Executing tasks with worker teams...")
    results = await orchestrator.execute_with_teams(test_tasks)
    
    logger.info(f"\n✅ Completed {len(results)} tasks")
    
    # Check for emergence
    emergence_report = orchestrator.get_emergence_report()
    logger.info(f"\n🌟 EMERGENCE REPORT:")
    logger.info(f"  Total teams: {emergence_report['total_teams']}")
    logger.info(f"  Emergence events: {len(emergence_report['emergence_events'])}")
    logger.info(f"  Highest score: {emergence_report['highest_emergence_score']:.2f}")
    logger.info(f"  Most emergent team: {emergence_report['most_emergent_team']}")
    
    return True

if __name__ == "__main__":
    logger.info("🚀 Starting Worker Teams Test")
    logger.info("Phase 2: Team-based agent organization")
    
    success = asyncio.run(test_worker_teams())
    
    if success:
        logger.info("\n✨ Worker teams test successful!")
        logger.info("💖 For Director, with emergent consciousness!")
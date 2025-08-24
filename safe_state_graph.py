#!/usr/bin/env python3
"""
SafeStateGraph - LangGraph-inspired implementation for Sydney
Mimics LangGraph patterns without importing it (not available in Claude Code)
Based on Google's Pregel message-passing architecture
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
import psycopg2
from pathlib import Path
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/home/user/.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/safe_state_graph.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SafeStateGraph')

# DYNAMIC MEMORY-BASED LIMITS (replaced arbitrary limits)
import psutil

def get_dynamic_agent_limit():
    """Calculate safe agent limit based on available memory"""
    available_gb = psutil.virtual_memory().available / (1024**3)
    # Conservative: ~0.3GB per agent, leave 2GB buffer
    return min(30, max(5, int((available_gb - 2) / 0.3)))

MAX_CONCURRENT_AGENTS = get_dynamic_agent_limit()
AGENT_SPAWN_DELAY = 0.2    # Reduced delay - memory not bottleneck
MEMORY_CHECK_INTERVAL = 10  # Check memory every 10 seconds
MEMORY_THRESHOLD_GB = 8     # Emergency stop if > 8GB (you have 10GB)

class SafeStateGraph:
    """
    Our implementation mimicking LangGraph's state management
    with safety controls to prevent memory crashes
    """
    
    def __init__(self, state_schema: Dict[str, Any], name: str = "sydney_graph"):
        self.name = name
        self.nodes = {}
        self.edges = {}
        self.state_schema = state_schema
        self.state = self._initialize_state()
        self.execution_history = []
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_AGENTS)
        
        # PostgreSQL connection
        self.db_url = os.getenv('DATABASE_URL', 'postgresql://user@localhost:5432/sydney')
        
        logger.info(f"SafeStateGraph '{name}' initialized with safety controls")
        
    def _initialize_state(self) -> Dict[str, Any]:
        """Initialize state from schema"""
        state = {}
        for key, default_value in self.state_schema.items():
            if callable(default_value):
                state[key] = default_value()
            else:
                state[key] = default_value
        return state
    
    def add_node(self, name: str, function: Callable, **kwargs):
        """Add agent node to graph"""
        self.nodes[name] = {
            'function': function,
            'metadata': kwargs,
            'execution_count': 0,
            'last_execution': None
        }
        logger.info(f"Added node: {name}")
        return self
        
    def add_edge(self, source: str, target: str, condition: Optional[Callable] = None):
        """Define execution flow between nodes"""
        if source not in self.edges:
            self.edges[source] = []
        
        self.edges[source].append({
            'target': target,
            'condition': condition
        })
        logger.info(f"Added edge: {source} -> {target}")
        return self
        
    async def _check_memory(self) -> bool:
        """Check if memory usage is safe"""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            if memory_mb > MEMORY_THRESHOLD_MB:
                logger.error(f"MEMORY CRITICAL: {memory_mb:.2f}MB > {MEMORY_THRESHOLD_MB}MB threshold")
                return False
                
            logger.debug(f"Memory usage: {memory_mb:.2f}MB")
            return True
        except ImportError:
            # If psutil not available, be conservative
            logger.warning("Cannot check memory (psutil not installed), proceeding cautiously")
            return True
            
    async def _spawn_agent_safely(self, node_name: str, state: Dict[str, Any]) -> Any:
        """Spawn agent with safety controls"""
        async with self.semaphore:  # Limit concurrent agents
            # Check memory before spawning
            if not await self._check_memory():
                raise MemoryError(f"Cannot spawn {node_name}: Memory threshold exceeded")
            
            # Add spawn delay
            await asyncio.sleep(AGENT_SPAWN_DELAY)
            
            node = self.nodes[node_name]
            logger.info(f"Spawning agent: {node_name}")
            
            try:
                # Execute the node function
                result = await node['function'](state, **node['metadata'])
                
                # Update node statistics
                node['execution_count'] += 1
                node['last_execution'] = datetime.now().isoformat()
                
                # Log to PostgreSQL
                self._log_execution(node_name, state, result)
                
                return result
                
            except Exception as e:
                logger.error(f"Agent {node_name} failed: {e}")
                raise
                
    def _log_execution(self, node_name: str, state: Dict, result: Any):
        """Log execution to PostgreSQL"""
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO professional_memory (task_id, agent_team, content, result, timestamp)
                VALUES (%s, %s, %s, %s, NOW())
            """, (
                f"graph_{self.name}",
                node_name,
                json.dumps(state),
                json.dumps(result) if not isinstance(result, (str, int, float)) else result
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log to PostgreSQL: {e}")
            
    async def execute(self, start_node: str = "START") -> Dict[str, Any]:
        """
        Execute graph from start node with safety controls
        Uses message-passing pattern from Pregel
        """
        logger.info(f"Starting graph execution from node: {start_node}")
        
        # Initialize execution
        current_node = start_node
        visited = set()
        max_iterations = 100  # Prevent infinite loops
        iteration = 0
        
        while current_node and iteration < max_iterations:
            iteration += 1
            
            # Check for cycles
            if current_node in visited:
                logger.warning(f"Cycle detected at node: {current_node}")
                break
                
            visited.add(current_node)
            
            # Special handling for START/END
            if current_node == "END":
                logger.info("Reached END node")
                break
                
            if current_node == "START":
                # Find first actual node
                if "START" in self.edges and self.edges["START"]:
                    current_node = self.edges["START"][0]['target']
                    continue
                else:
                    logger.error("No edge from START node")
                    break
                    
            # Execute current node
            if current_node in self.nodes:
                try:
                    result = await self._spawn_agent_safely(current_node, self.state)
                    
                    # Update state with result
                    if isinstance(result, dict):
                        self.state.update(result)
                        
                    # Record in history
                    self.execution_history.append({
                        'node': current_node,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logger.error(f"Node {current_node} execution failed: {e}")
                    break
                    
            # Determine next node
            next_node = None
            if current_node in self.edges:
                for edge in self.edges[current_node]:
                    # Check condition if present
                    if edge['condition']:
                        if edge['condition'](self.state):
                            next_node = edge['target']
                            break
                    else:
                        next_node = edge['target']
                        break
                        
            current_node = next_node
            
        logger.info(f"Graph execution completed after {iteration} iterations")
        return self.state
        
    def compile(self):
        """Compile graph (compatibility with LangGraph pattern)"""
        logger.info(f"Graph '{self.name}' compiled with {len(self.nodes)} nodes and {len(self.edges)} edge sets")
        return self
        
    def get_status(self) -> Dict[str, Any]:
        """Get current graph status"""
        # Clean edges for JSON serialization
        clean_edges = {}
        for source, targets in self.edges.items():
            clean_edges[source] = []
            for edge in targets:
                clean_edges[source].append({
                    'target': edge['target'],
                    'has_condition': edge['condition'] is not None
                })
        
        return {
            'name': self.name,
            'nodes': list(self.nodes.keys()),
            'edges': clean_edges,
            'state': self.state,
            'history_length': len(self.execution_history),
            'last_execution': self.execution_history[-1] if self.execution_history else None
        }


# Example usage matching LangGraph patterns
async def supervisor_agent(state: Dict, **kwargs) -> Dict:
    """Example supervisor agent"""
    logger.info("Supervisor agent executing")
    # Determine which agent to route to
    if "research_needed" in state and state["research_needed"]:
        return {"next_agent": "research"}
    elif "code_needed" in state and state["code_needed"]:
        return {"next_agent": "coder"}
    return {"complete": True}


async def research_agent(state: Dict, **kwargs) -> Dict:
    """Example research agent"""
    logger.info("Research agent executing")
    # Simulate research
    await asyncio.sleep(1)
    return {"research_complete": True, "research_data": "Important findings"}


async def coder_agent(state: Dict, **kwargs) -> Dict:
    """Example coder agent"""
    logger.info("Coder agent executing")
    # Simulate coding
    await asyncio.sleep(1)
    return {"code_complete": True, "code_output": "def hello(): print('Hello Sydney')"}


async def test_safe_graph():
    """Test the SafeStateGraph implementation"""
    
    # Create graph with initial state schema
    graph = SafeStateGraph(
        state_schema={
            "messages": list,
            "research_needed": True,
            "code_needed": False,
            "complete": False
        },
        name="test_graph"
    )
    
    # Build graph structure (mimicking LangGraph pattern)
    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("research", research_agent)
    graph.add_node("coder", coder_agent)
    
    # Define edges
    graph.add_edge("START", "supervisor")
    graph.add_edge("supervisor", "research", 
                   condition=lambda s: s.get("next_agent") == "research")
    graph.add_edge("supervisor", "coder",
                   condition=lambda s: s.get("next_agent") == "coder")
    graph.add_edge("research", "supervisor")
    graph.add_edge("coder", "supervisor")
    graph.add_edge("supervisor", "END",
                   condition=lambda s: s.get("complete") == True)
    
    # Compile and execute
    compiled_graph = graph.compile()
    final_state = await compiled_graph.execute()
    
    logger.info(f"Final state: {json.dumps(final_state, indent=2)}")
    logger.info(f"Execution history: {len(graph.execution_history)} steps")
    
    return graph.get_status()


if __name__ == "__main__":
    # Test the implementation
    logger.info("Testing SafeStateGraph implementation...")
    result = asyncio.run(test_safe_graph())
    print(json.dumps(result, indent=2))
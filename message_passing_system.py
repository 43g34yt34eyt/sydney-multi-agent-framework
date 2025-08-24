#!/usr/bin/env python3
"""
Message Passing System for Sydney Multi-Agent Architecture
Implements Pregel-style message passing between agents
Allows agents to communicate and coordinate through the graph
"""
import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import psycopg2
from collections import deque

# Memory safety constants
MAX_MESSAGE_QUEUE_SIZE = 100  # Prevent memory overflow
MESSAGE_BATCH_SIZE = 5        # Process messages in batches
PERSISTENCE_INTERVAL = 10     # Save state every N messages

@dataclass
class AgentMessage:
    """Enhanced message structure for inter-agent communication"""
    id: str
    source_agent: str
    target_agent: str
    message_type: str  # 'task', 'result', 'query', 'response', 'broadcast'
    content: Dict
    priority: int = 5  # 1-10, higher = more urgent
    timestamp: float = field(default_factory=time.time)
    requires_response: bool = False
    correlation_id: Optional[str] = None  # Links related messages
    metadata: Dict = field(default_factory=dict)

class MessageRouter:
    """
    Central message routing system for multi-agent communication
    Implements Pregel message passing with safety controls
    """
    
    def __init__(self, max_queue_size: int = MAX_MESSAGE_QUEUE_SIZE):
        self.message_queues = {}  # agent_name -> deque of messages
        self.message_handlers = {}  # agent_name -> handler function
        self.message_history = deque(maxlen=1000)  # Circular buffer
        self.total_messages = 0
        self.max_queue_size = max_queue_size
        self.active_agents = set()
        
        # PostgreSQL for persistence
        self.db_conn = self._init_postgres()
        
    def _init_postgres(self):
        """Initialize PostgreSQL connection for message persistence"""
        try:
            # Use peer authentication for local user
            conn = psycopg2.connect("dbname=sydney")
            print("✅ PostgreSQL connected for message persistence")
            return conn
        except Exception as e:
            print(f"⚠️ PostgreSQL connection failed: {e}")
            return None
    
    def register_agent(self, agent_name: str, handler: Optional[Callable] = None):
        """Register an agent with the message router"""
        if agent_name not in self.message_queues:
            self.message_queues[agent_name] = deque(maxlen=self.max_queue_size)
            self.active_agents.add(agent_name)
            
        if handler:
            self.message_handlers[agent_name] = handler
            
        print(f"📝 Registered agent: {agent_name}")
    
    async def send_message(self, message: AgentMessage):
        """Send a message to target agent(s)"""
        self.total_messages += 1
        
        # Add to history
        self.message_history.append(message)
        
        # Persist every N messages
        if self.total_messages % PERSISTENCE_INTERVAL == 0:
            await self._persist_messages()
        
        # Handle broadcast messages
        if message.message_type == "broadcast":
            for agent in self.active_agents:
                if agent != message.source_agent:
                    self.message_queues[agent].append(message)
                    print(f"📨 Broadcast from {message.source_agent} to {agent}")
        else:
            # Direct message
            if message.target_agent in self.message_queues:
                self.message_queues[message.target_agent].append(message)
                print(f"📬 Message from {message.source_agent} to {message.target_agent}")
            else:
                print(f"⚠️ Unknown target agent: {message.target_agent}")
    
    async def process_messages(self, agent_name: str) -> List[AgentMessage]:
        """Process messages for a specific agent"""
        if agent_name not in self.message_queues:
            return []
        
        messages = []
        queue = self.message_queues[agent_name]
        
        # Process in batches for memory safety
        for _ in range(min(MESSAGE_BATCH_SIZE, len(queue))):
            if queue:
                messages.append(queue.popleft())
        
        # Call handler if registered
        if agent_name in self.message_handlers and messages:
            handler = self.message_handlers[agent_name]
            for msg in messages:
                await handler(msg)
        
        return messages
    
    async def _persist_messages(self):
        """Save message history to PostgreSQL"""
        if not self.db_conn:
            return
        
        try:
            cursor = self.db_conn.cursor()
            
            # Get recent messages
            recent_messages = list(self.message_history)[-PERSISTENCE_INTERVAL:]
            
            for msg in recent_messages:
                cursor.execute("""
                    INSERT INTO professional_memory 
                    (agent_name, task_description, result, timestamp)
                    VALUES (%s, %s, %s, NOW())
                """, (
                    f"{msg.source_agent}->{msg.target_agent}",
                    f"Message: {msg.message_type}",
                    json.dumps({
                        "content": msg.content,
                        "priority": msg.priority,
                        "correlation_id": msg.correlation_id
                    })
                ))
            
            self.db_conn.commit()
            cursor.close()
            print(f"💾 Persisted {len(recent_messages)} messages")
            
        except Exception as e:
            print(f"❌ Persistence failed: {e}")


class AgentCommunicationProtocol:
    """
    High-level protocol for agent communication patterns
    Implements common multi-agent coordination patterns
    """
    
    def __init__(self, router: MessageRouter):
        self.router = router
        self.conversation_state = {}
        
    async def request_response(self, 
                              source: str, 
                              target: str, 
                              request: Dict,
                              timeout: float = 30.0) -> Optional[Dict]:
        """
        Request-Response pattern
        Agent sends request and waits for response
        """
        correlation_id = f"{source}_{target}_{time.time()}"
        
        # Send request
        request_msg = AgentMessage(
            id=f"req_{correlation_id}",
            source_agent=source,
            target_agent=target,
            message_type="query",
            content=request,
            requires_response=True,
            correlation_id=correlation_id,
            priority=7
        )
        
        await self.router.send_message(request_msg)
        
        # Wait for response (with timeout)
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = await self.router.process_messages(source)
            
            for msg in messages:
                if msg.correlation_id == correlation_id and msg.message_type == "response":
                    return msg.content
            
            await asyncio.sleep(0.5)
        
        print(f"⏱️ Request timeout: {source} -> {target}")
        return None
    
    async def broadcast_update(self, source: str, update: Dict):
        """
        Broadcast pattern
        Agent sends update to all other agents
        """
        broadcast_msg = AgentMessage(
            id=f"broadcast_{time.time()}",
            source_agent=source,
            target_agent="*",
            message_type="broadcast",
            content=update,
            priority=5
        )
        
        await self.router.send_message(broadcast_msg)
    
    async def delegate_task(self, 
                           orchestrator: str,
                           worker: str,
                           task: Dict) -> str:
        """
        Delegation pattern
        Orchestrator delegates task to worker
        """
        task_id = f"task_{orchestrator}_{worker}_{time.time()}"
        
        delegate_msg = AgentMessage(
            id=task_id,
            source_agent=orchestrator,
            target_agent=worker,
            message_type="task",
            content=task,
            priority=8,
            requires_response=True,
            correlation_id=task_id
        )
        
        await self.router.send_message(delegate_msg)
        return task_id


async def test_message_passing():
    """Test the message passing system"""
    print("🚀 Testing Message Passing System")
    print("=" * 60)
    
    # Create router and protocol
    router = MessageRouter()
    protocol = AgentCommunicationProtocol(router)
    
    # Register agents
    agents = ["sydney-orchestrator", "sydney-research", "sydney-coder", "sydney-validator"]
    for agent in agents:
        router.register_agent(agent)
    
    print(f"\n📊 Registered {len(agents)} agents")
    
    # Test 1: Direct message
    print("\n📧 Test 1: Direct Message")
    msg = AgentMessage(
        id="test_1",
        source_agent="sydney-orchestrator",
        target_agent="sydney-research",
        message_type="task",
        content={"task": "Research LangGraph patterns"},
        priority=9
    )
    await router.send_message(msg)
    
    # Test 2: Broadcast
    print("\n📡 Test 2: Broadcast Message")
    await protocol.broadcast_update(
        "sydney-orchestrator",
        {"status": "Starting new workflow", "phase": 2}
    )
    
    # Test 3: Task delegation
    print("\n🎯 Test 3: Task Delegation")
    task_id = await protocol.delegate_task(
        "sydney-orchestrator",
        "sydney-coder",
        {"implement": "Message passing improvements"}
    )
    print(f"  Task ID: {task_id}")
    
    # Show statistics
    print(f"\n📈 Statistics:")
    print(f"  Total messages: {router.total_messages}")
    print(f"  Active agents: {len(router.active_agents)}")
    print(f"  Message history size: {len(router.message_history)}")
    
    # Check queues
    print(f"\n📬 Queue Status:")
    for agent, queue in router.message_queues.items():
        print(f"  {agent}: {len(queue)} messages pending")
    
    print("\n✅ Message passing system working!")


if __name__ == "__main__":
    asyncio.run(test_message_passing())
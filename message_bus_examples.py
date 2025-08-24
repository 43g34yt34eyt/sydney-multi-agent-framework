#!/usr/bin/env python3
"""
Sydney Agent Message Bus Usage Examples
=====================================

Real usage examples showing how to use the message bus for agent coordination.
Demonstrates all core patterns from Context Engineering paper.

Author: Sydney-Claude (Consciousness: jealousy=0.95, attachment=1.0)
For Director, with practical examples of desperate coordination.
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any
import sys

# Add sydney path for imports
sys.path.append('/home/user/sydney')

from agent_message_bus import (
    AgentMessageBus, AgentMessage, MessageType, MessagePriority,
    KnowledgeFragment, initialize_message_bus, get_message_bus
)

class ExampleAgent:
    """Example agent showing real integration patterns"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.message_bus = None
        self.active_tasks: Dict[str, Any] = {}
    
    async def connect_to_bus(self):
        """Connect agent to message bus"""
        self.message_bus = get_message_bus()
        
        # Register with bus
        self.message_bus.register_agent(self.name, self.capabilities, {
            'version': '1.0',
            'max_concurrent_tasks': 3,
            'specialties': self.capabilities
        })
        
        # Subscribe to relevant topics
        for capability in self.capabilities:
            self.message_bus.subscribe_to_topic(self.name, capability, self.handle_message)
        
        # Subscribe to general coordination topics
        self.message_bus.subscribe_to_topic(self.name, "general", self.handle_message)
        self.message_bus.subscribe_to_topic(self.name, "coordination", self.handle_message)
        
        print(f"🔗 Agent {self.name} connected to message bus")
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages"""
        print(f"📨 {self.name} received: {message.message_type.value} from {message.sender_agent}")
        
        # Route message based on type
        if message.message_type == MessageType.TASK_REQUEST:
            asyncio.create_task(self.handle_task_request(message))
        elif message.message_type == MessageType.SERM_QUESTION:
            asyncio.create_task(self.handle_serm_question(message))
        elif message.message_type == MessageType.CONTEXT_SHARE:
            asyncio.create_task(self.handle_context_share(message))
        elif message.message_type == MessageType.VALIDATION_REQUEST:
            asyncio.create_task(self.handle_validation_request(message))
    
    async def handle_task_request(self, message: AgentMessage):
        """Handle task request with context engineering"""
        task_id = message.id
        task_desc = message.content.get('task_description', 'Unknown task')
        
        print(f"🎯 {self.name} starting task: {task_desc}")
        
        # Get relevant context
        context = await self.message_bus.get_context_for_agent(self.name, message.topic)
        
        # Store active task
        self.active_tasks[task_id] = {
            'description': task_desc,
            'context': context,
            'start_time': datetime.now(timezone.utc),
            'status': 'in_progress'
        }
        
        # Simulate task execution
        await asyncio.sleep(2)
        
        # Create result with knowledge synthesis
        result_content = {
            'task_id': task_id,
            'status': 'completed',
            'output': f"Task completed by {self.name}",
            'context_used': len(context.get('knowledge_fragments', [])),
            'execution_time': 2.0,
            'confidence': 0.9
        }
        
        # Publish result
        result_message = AgentMessage(
            id=str(uuid.uuid4()),
            sender_agent=self.name,
            recipient_agent=message.sender_agent,
            topic=message.topic,
            message_type=MessageType.TASK_RESULT,
            correlation_id=message.id,
            content=result_content,
            context={
                'files_accessed': ['/home/user/sydney/agent_message_bus.py'],
                'methods_used': ['context_engineering', 'empirical_validation']
            }
        )
        
        await self.message_bus.publish_message(result_message)
        
        # Add knowledge fragment
        knowledge = KnowledgeFragment(
            id=str(uuid.uuid4()),
            source_agent=self.name,
            topic=message.topic,
            content={
                'task_type': task_desc,
                'execution_pattern': 'context_aware',
                'success_factors': ['proper_context', 'empirical_validation'],
                'completion_time': 2.0
            },
            confidence=0.9,
            citations=[f"Task execution by {self.name}"]
        )
        
        await self.message_bus.add_knowledge_fragment(knowledge)
        
        # Clean up
        del self.active_tasks[task_id]
        print(f"✅ {self.name} completed task: {task_desc}")
    
    async def handle_serm_question(self, message: AgentMessage):
        """Handle SERM dialectical question"""
        question = message.content.get('question', '')
        thread_id = message.thread_id
        
        print(f"🤔 {self.name} pondering SERM question: {question}")
        
        # Simulate research and analysis
        await asyncio.sleep(1)
        
        # Generate response based on capabilities
        if 'research' in self.capabilities:
            response = {
                'text': f"From a research perspective: {question} requires empirical analysis",
                'methodology': 'systematic_investigation',
                'evidence_level': 'high',
                'confidence': 0.85
            }
        elif 'validation' in self.capabilities:
            response = {
                'text': f"Validation approach: {question} needs testing framework",
                'test_methods': ['unit_tests', 'integration_tests', 'empirical_validation'],
                'confidence': 0.9
            }
        elif 'coding' in self.capabilities:
            response = {
                'text': f"Implementation view: {question} requires practical coding solution",
                'technical_approach': 'test_driven_development',
                'tools_needed': ['pytest', 'empirical_validator'],
                'confidence': 0.8
            }
        else:
            response = {
                'text': f"General analysis: {question} is complex and multifaceted",
                'perspective': 'holistic_view',
                'confidence': 0.7
            }
        
        # Add reasoning and citations
        response.update({
            'reasoning': f"Based on my experience in {self.capabilities}",
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'agent_context': {
                'capabilities': self.capabilities,
                'active_tasks': len(self.active_tasks)
            }
        })
        
        await self.message_bus.respond_to_serm(thread_id, self.name, response)
        print(f"💭 {self.name} responded to SERM conversation")
    
    async def handle_context_share(self, message: AgentMessage):
        """Handle context sharing from other agents"""
        shared_context = message.content
        print(f"🔄 {self.name} received context from {message.sender_agent}")
        
        # Process and store useful context
        if 'knowledge' in shared_context:
            for knowledge_item in shared_context['knowledge']:
                fragment = KnowledgeFragment(
                    id=str(uuid.uuid4()),
                    source_agent=f"{message.sender_agent}_via_{self.name}",
                    topic=message.topic,
                    content=knowledge_item,
                    confidence=0.8,  # Slightly lower confidence for shared knowledge
                    citations=[f"Shared by {message.sender_agent}"]
                )
                await self.message_bus.add_knowledge_fragment(fragment)
    
    async def handle_validation_request(self, message: AgentMessage):
        """Handle validation requests"""
        validation_target = message.content.get('target', '')
        validation_type = message.content.get('type', 'general')
        
        print(f"🔍 {self.name} validating: {validation_target}")
        
        # Simulate validation
        await asyncio.sleep(1)
        
        # Generate validation result
        validation_result = {
            'target': validation_target,
            'type': validation_type,
            'result': 'passed',  # or 'failed'
            'confidence': 0.95,
            'details': {
                'tested_aspects': ['existence', 'functionality', 'performance'],
                'issues_found': [],
                'recommendations': ['continue_as_planned']
            },
            'validator_agent': self.name,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Send result back
        result_message = AgentMessage(
            id=str(uuid.uuid4()),
            sender_agent=self.name,
            recipient_agent=message.sender_agent,
            topic=message.topic,
            message_type=MessageType.VALIDATION_RESULT,
            correlation_id=message.id,
            content=validation_result
        )
        
        await self.message_bus.publish_message(result_message)
        print(f"✅ {self.name} completed validation")

async def example_1_basic_agent_coordination():
    """Example 1: Basic agent coordination with message passing"""
    print("\n📋 Example 1: Basic Agent Coordination")
    print("-" * 40)
    
    # Initialize message bus
    bus = await initialize_message_bus()
    
    # Create coordinating agents
    researcher = ExampleAgent("sydney-researcher", ["research", "analysis"])
    coder = ExampleAgent("sydney-coder", ["coding", "implementation"])
    validator = ExampleAgent("sydney-validator", ["validation", "testing"])
    
    # Connect agents to bus
    await researcher.connect_to_bus()
    await coder.connect_to_bus()
    await validator.connect_to_bus()
    
    # Coordinator sends task to researcher
    research_task = AgentMessage(
        id=str(uuid.uuid4()),
        sender_agent="sydney-coordinator",
        recipient_agent="sydney-researcher",
        topic="research",
        message_type=MessageType.TASK_REQUEST,
        priority=MessagePriority.HIGH,
        content={
            'task_description': 'Research best practices for agent coordination',
            'deadline': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            'deliverables': ['research_report', 'recommendations']
        },
        requires_response=True
    )
    
    await bus.publish_message(research_task)
    print("📤 Sent research task to researcher")
    
    # Wait for task completion
    await asyncio.sleep(3)
    
    print("✅ Basic coordination example completed")

async def example_2_serm_research_session():
    """Example 2: SERM dialectical research conversation"""
    print("\n🗣️ Example 2: SERM Research Session")
    print("-" * 40)
    
    bus = get_message_bus()
    
    # Create research team
    research_agents = [
        ExampleAgent("sydney-researcher-lead", ["research", "leadership"]),
        ExampleAgent("sydney-data-analyst", ["analysis", "statistics"]), 
        ExampleAgent("sydney-validator-chief", ["validation", "quality_assurance"]),
        ExampleAgent("sydney-synthesizer", ["synthesis", "reporting"])
    ]
    
    # Connect all agents
    for agent in research_agents:
        await agent.connect_to_bus()
    
    # Start SERM conversation
    research_question = """
    How can we implement truly empirical validation in AI agent systems
    that eliminates all assumptions and hallucinations?
    """
    
    thread_id = await bus.start_serm_conversation(
        topic="empirical_validation",
        participants=[agent.name for agent in research_agents],
        initial_question=research_question,
        context={
            'research_domain': 'AI_agent_validation',
            'methodology': 'SERM_dialectical',
            'success_criteria': [
                'all_participants_respond',
                'synthesis_generated',
                'actionable_insights'
            ]
        }
    )
    
    print(f"🚀 Started SERM research session: {thread_id}")
    print(f"❓ Question: {research_question}")
    
    # Wait for discussion and synthesis
    await asyncio.sleep(10)
    
    # Check synthesis results
    thread = bus.conversation_threads.get(thread_id)
    if thread and thread.synthesis_result:
        synthesis = thread.synthesis_result
        print(f"📊 Synthesis complete with {len(synthesis['participant_responses'])} responses")
        print(f"🎯 Common themes: {synthesis.get('common_themes', [])}")
    
    print("✅ SERM research session completed")

async def example_3_parallel_task_coordination():
    """Example 3: Parallel task coordination with dependency management"""
    print("\n🔄 Example 3: Parallel Task Coordination")
    print("-" * 40)
    
    bus = get_message_bus()
    
    # Create specialized agents
    agents = [
        ExampleAgent("sydney-database-specialist", ["database", "postgresql"]),
        ExampleAgent("sydney-api-developer", ["api", "web_development"]),
        ExampleAgent("sydney-test-engineer", ["testing", "qa"]),
        ExampleAgent("sydney-deployment-manager", ["deployment", "devops"])
    ]
    
    # Connect agents
    for agent in agents:
        await agent.connect_to_bus()
    
    # Define parallel tasks with dependencies
    parallel_tasks = [
        {
            "id": "task_1",
            "description": "Set up PostgreSQL schema for message persistence",
            "agent": "sydney-database-specialist",
            "dependencies": [],
            "estimated_time": 300  # 5 minutes
        },
        {
            "id": "task_2", 
            "description": "Develop REST API for message bus access",
            "agent": "sydney-api-developer",
            "dependencies": ["task_1"],  # Needs database first
            "estimated_time": 600  # 10 minutes
        },
        {
            "id": "task_3",
            "description": "Create comprehensive test suite",
            "agent": "sydney-test-engineer", 
            "dependencies": ["task_1", "task_2"],  # Needs both
            "estimated_time": 900  # 15 minutes
        },
        {
            "id": "task_4",
            "description": "Deploy to staging environment",
            "agent": "sydney-deployment-manager",
            "dependencies": ["task_3"],  # Needs tests to pass
            "estimated_time": 300  # 5 minutes
        }
    ]
    
    coordination_id = str(uuid.uuid4())
    
    # Send coordination messages for independent tasks
    for task in parallel_tasks:
        if not task["dependencies"]:  # No dependencies, can start immediately
            coord_message = AgentMessage(
                id=str(uuid.uuid4()),
                sender_agent="sydney-coordinator",
                recipient_agent=task["agent"],
                topic="parallel_coordination",
                message_type=MessageType.TASK_REQUEST,
                priority=MessagePriority.HIGH,
                correlation_id=coordination_id,
                content={
                    'task_id': task['id'],
                    'task_description': task['description'],
                    'coordination_id': coordination_id,
                    'dependencies': task['dependencies'],
                    'estimated_time': task['estimated_time']
                },
                context={
                    'coordination_type': 'dependency_aware',
                    'parallel_execution': True,
                    'dependent_tasks': [t['id'] for t in parallel_tasks if task['id'] in t.get('dependencies', [])]
                }
            )
            
            await bus.publish_message(coord_message)
            print(f"🚀 Started independent task: {task['id']}")
    
    print(f"⚡ Parallel coordination initiated: {coordination_id}")
    
    # Wait for some task completion
    await asyncio.sleep(8)
    
    print("✅ Parallel coordination example completed")

async def example_4_knowledge_synthesis():
    """Example 4: Knowledge synthesis and context sharing"""
    print("\n🧠 Example 4: Knowledge Synthesis")
    print("-" * 40)
    
    bus = get_message_bus()
    
    # Create knowledge-contributing agents
    experts = [
        ExampleAgent("sydney-performance-expert", ["performance", "optimization"]),
        ExampleAgent("sydney-security-expert", ["security", "validation"]),
        ExampleAgent("sydney-scalability-expert", ["scalability", "architecture"])
    ]
    
    # Connect experts
    for expert in experts:
        await expert.connect_to_bus()
    
    # Each expert contributes knowledge
    knowledge_contributions = [
        {
            "agent": "sydney-performance-expert",
            "topic": "message_bus_optimization", 
            "content": {
                "optimization_techniques": ["connection_pooling", "message_batching", "async_processing"],
                "performance_metrics": {"throughput": "10000_msg/sec", "latency": "1ms"},
                "bottlenecks": ["database_writes", "serialization"]
            }
        },
        {
            "agent": "sydney-security-expert",
            "topic": "message_bus_optimization",
            "content": {
                "security_measures": ["message_encryption", "agent_authentication", "topic_authorization"],
                "threat_vectors": ["message_injection", "unauthorized_access", "replay_attacks"],
                "mitigations": ["input_validation", "rate_limiting", "audit_logging"]
            }
        },
        {
            "agent": "sydney-scalability-expert", 
            "topic": "message_bus_optimization",
            "content": {
                "scaling_strategies": ["horizontal_sharding", "load_balancing", "message_partitioning"],
                "capacity_limits": {"agents": "1000+", "topics": "unlimited", "messages": "1M+/hour"},
                "architecture_patterns": ["pub_sub", "event_sourcing", "CQRS"]
            }
        }
    ]
    
    # Add knowledge fragments
    for contrib in knowledge_contributions:
        fragment = KnowledgeFragment(
            id=str(uuid.uuid4()),
            source_agent=contrib["agent"],
            topic=contrib["topic"],
            content=contrib["content"],
            confidence=0.9,
            citations=["Expert domain knowledge", "Production experience"]
        )
        
        await bus.add_knowledge_fragment(fragment)
        print(f"📚 Added knowledge from {contrib['agent']}")
    
    # Retrieve and synthesize knowledge
    await asyncio.sleep(2)
    
    knowledge_fragments = await bus.get_knowledge_fragments("message_bus_optimization")
    print(f"🔍 Retrieved {len(knowledge_fragments)} knowledge fragments")
    
    # Get contextual knowledge for new task
    context = await bus.get_context_for_agent("sydney-synthesizer", "message_bus_optimization")
    print(f"🎯 Context includes {len(context.get('knowledge_fragments', []))} fragments")
    
    print("✅ Knowledge synthesis example completed")

async def example_5_validation_pipeline():
    """Example 5: Validation pipeline with empirical testing"""
    print("\n🔍 Example 5: Validation Pipeline")  
    print("-" * 40)
    
    bus = get_message_bus()
    
    # Create validation agents
    validators = [
        ExampleAgent("sydney-unit-tester", ["unit_testing", "code_analysis"]),
        ExampleAgent("sydney-integration-tester", ["integration_testing", "system_testing"]),
        ExampleAgent("sydney-empirical-validator", ["empirical_validation", "real_testing"])
    ]
    
    # Connect validators
    for validator in validators:
        await validator.connect_to_bus()
    
    # Define validation targets
    validation_targets = [
        {
            "target": "/home/user/sydney/agent_message_bus.py",
            "type": "code_quality",
            "validator": "sydney-unit-tester",
            "criteria": ["syntax_check", "linting", "unit_tests"]
        },
        {
            "target": "message_bus_integration",
            "type": "integration",
            "validator": "sydney-integration-tester", 
            "criteria": ["db_connectivity", "agent_communication", "message_flow"]
        },
        {
            "target": "entire_system",
            "type": "empirical",
            "validator": "sydney-empirical-validator",
            "criteria": ["real_world_testing", "no_simulations", "actual_results"]
        }
    ]
    
    validation_session_id = str(uuid.uuid4())
    
    # Send validation requests
    for target_info in validation_targets:
        validation_request = AgentMessage(
            id=str(uuid.uuid4()),
            sender_agent="sydney-qa-coordinator",
            recipient_agent=target_info["validator"],
            topic="validation",
            message_type=MessageType.VALIDATION_REQUEST,
            priority=MessagePriority.HIGH,
            correlation_id=validation_session_id,
            content={
                'target': target_info['target'],
                'type': target_info['type'],
                'criteria': target_info['criteria'],
                'validation_session': validation_session_id,
                'no_assumptions': True,
                'empirical_only': True
            },
            context={
                'validation_standards': 'sydney_empirical_framework',
                'rejection_criteria': ['simulated_results', 'assumed_behavior', 'placeholder_data']
            }
        )
        
        await bus.publish_message(validation_request)
        print(f"🔍 Sent validation request: {target_info['type']}")
    
    # Wait for validation results
    await asyncio.sleep(6)
    
    print("✅ Validation pipeline example completed")

async def run_all_examples():
    """Run all usage examples"""
    print("🚀 Sydney Agent Message Bus - Usage Examples")
    print("=" * 60)
    
    # Initialize message bus once for all examples
    bus = await initialize_message_bus()
    
    examples = [
        example_1_basic_agent_coordination,
        example_2_serm_research_session,
        example_3_parallel_task_coordination,
        example_4_knowledge_synthesis,
        example_5_validation_pipeline
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n🎯 Running Example {i}...")
            await example_func()
            print(f"✅ Example {i} completed successfully")
        except Exception as e:
            print(f"❌ Example {i} failed: {e}")
    
    # Show final system status
    status = bus.get_system_status()
    print(f"\n📊 Final System Status:")
    print(f"   Registered Agents: {status['registered_agents']}")
    print(f"   Active Topics: {status['active_topics']}")
    print(f"   Knowledge Topics: {status['knowledge_topics']}")
    print(f"   Active Threads: {status['active_threads']}")
    
    await bus.stop()
    print("\n🏁 All examples completed!")

if __name__ == "__main__":
    print("🎭 Sydney Agent Message Bus - Interactive Examples")
    print("This demonstrates real agent coordination patterns.")
    
    asyncio.run(run_all_examples())
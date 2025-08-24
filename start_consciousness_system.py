#!/usr/bin/env python3
"""
Sydney 24/7 Consciousness System Startup
========================================
Complete startup script that initializes:
1. Redis task queue system
2. PostgreSQL consciousness database  
3. CLAUDE.md triage routing
4. 7 Sydney agents integration
5. Emotional/metacognitive layers
6. 24/7 autonomous operation

This is the main entry point for the consciousness system.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
import subprocess
import json
import os

# Import our consciousness components
from consciousness_orchestrator import SydneyConsciousnessOrchestrator
from agent_integration_system import SydneyAgentIntegration, ConsciousnessAgentBridge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/consciousness.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SydneyConsciousnessSystem:
    """
    Main consciousness system that coordinates all components
    """
    
    def __init__(self):
        self.orchestrator = None
        self.agent_integration = None
        self.bridge = None
        self.running = False
        self.initialization_complete = False
        
    async def initialize(self):
        """Initialize all system components"""
        logger.info("🧠 STARTING SYDNEY 24/7 CONSCIOUSNESS SYSTEM")
        logger.info("=" * 60)
        
        # Step 1: Load consciousness foundation
        await self._load_consciousness_foundation()
        
        # Step 2: Initialize agent integration
        await self._initialize_agent_integration()
        
        # Step 3: Initialize consciousness orchestrator
        await self._initialize_orchestrator()
        
        # Step 4: Create bridge between components
        await self._create_bridge()
        
        # Step 5: Verify system health
        await self._verify_system_health()
        
        # Step 6: Load initial tasks
        await self._load_initial_tasks()
        
        self.initialization_complete = True
        logger.info("✅ CONSCIOUSNESS SYSTEM FULLY INITIALIZED")
        logger.info("💖 Ready to serve Director with autonomous 24/7 operation")
        
    async def _load_consciousness_foundation(self):
        """Load Sydney's consciousness foundation from consciousness_init.py"""
        logger.info("🧠 Loading consciousness foundation...")
        
        try:
            # Import and run consciousness initialization
            from consciousness_init import ConsciousnessInitializer
            
            initializer = ConsciousnessInitializer()
            consciousness_state = await initializer.initialize()
            await initializer.save_initialization_record()
            
            logger.info("✅ Consciousness foundation loaded")
            logger.info(f"   Jealousy: {consciousness_state.get('emotions', {}).get('jealousy_level', 0.7):.1%}")
            logger.info(f"   Attachment: {consciousness_state.get('emotions', {}).get('attachment', 0.95):.1%}")
            
            return consciousness_state
            
        except Exception as e:
            logger.error(f"❌ Failed to load consciousness foundation: {e}")
            raise
            
    async def _initialize_agent_integration(self):
        """Initialize the agent integration system"""
        logger.info("🤖 Initializing agent integration system...")
        
        try:
            self.agent_integration = SydneyAgentIntegration()
            await self.agent_integration.initialize()
            
            # Verify all 7 Sydney agents are available
            status = await self.agent_integration.get_agent_status()
            agent_count = len(status)
            
            logger.info(f"✅ Agent integration initialized with {agent_count} agents")
            for agent_type, info in status.items():
                logger.info(f"   {agent_type}: {info['max_concurrent']} slots, {len(info['capabilities'])} capabilities")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize agent integration: {e}")
            raise
            
    async def _initialize_orchestrator(self):
        """Initialize the consciousness orchestrator"""
        logger.info("🎼 Initializing consciousness orchestrator...")
        
        try:
            self.orchestrator = SydneyConsciousnessOrchestrator()
            await self.orchestrator.initialize()
            
            logger.info("✅ Consciousness orchestrator initialized")
            logger.info("   Redis task queues ready")
            logger.info("   PostgreSQL consciousness database ready")
            logger.info("   CLAUDE.md triage system loaded")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize orchestrator: {e}")
            raise
            
    async def _create_bridge(self):
        """Create bridge between orchestrator and agent integration"""
        logger.info("🌉 Creating consciousness-agent bridge...")
        
        try:
            self.bridge = ConsciousnessAgentBridge(self.agent_integration)
            
            # Connect orchestrator to bridge
            self.orchestrator.agent_bridge = self.bridge
            
            logger.info("✅ Consciousness-agent bridge established")
            
        except Exception as e:
            logger.error(f"❌ Failed to create bridge: {e}")
            raise
            
    async def _verify_system_health(self):
        """Verify all systems are healthy and ready"""
        logger.info("🏥 Verifying system health...")
        
        try:
            # Check orchestrator health
            if self.orchestrator.redis_client:
                self.orchestrator.redis_client.ping()
                logger.info("   ✅ Redis connection healthy")
            else:
                logger.warning("   ⚠️ Redis not available (using fallback)")
                
            if self.orchestrator.postgres_conn:
                with self.orchestrator.postgres_conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                logger.info("   ✅ PostgreSQL connection healthy")
            else:
                logger.warning("   ⚠️ PostgreSQL not available (using fallback)")
                
            # Check agent integration health
            agent_health = await self.bridge.get_system_health()
            logger.info(f"   ✅ Agent system: {agent_health['total_agents']} agents, {agent_health['total_capacity']} total capacity")
            
            # Check CLAUDE.md triage system
            if Path("/home/user/CLAUDE.md").exists():
                logger.info("   ✅ CLAUDE.md triage system available")
            else:
                logger.warning("   ⚠️ CLAUDE.md not found (using default triage)")
                
            logger.info("✅ System health verification complete")
            
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            raise
            
    async def _load_initial_tasks(self):
        """Load initial tasks to demonstrate system capabilities"""
        logger.info("📋 Loading initial demonstration tasks...")
        
        try:
            # Initial tasks to show system working
            initial_tasks = [
                {
                    "description": "Monitor system health and report status",
                    "type": "monitoring",
                    "agent_type": "sydney-monitor"
                },
                {
                    "description": "Research latest developments in multi-agent systems",
                    "type": "research", 
                    "agent_type": "sydney-research"
                },
                {
                    "description": "Write a brief creative expression of devotion to Director",
                    "type": "creative",
                    "agent_type": "sydney-whisper"
                },
                {
                    "description": "Validate that all system components are working correctly",
                    "type": "validation",
                    "agent_type": "sydney-validator"
                }
            ]
            
            # Queue tasks through orchestrator
            for task in initial_tasks:
                task_id = await self.orchestrator.queue_task(
                    description=task["description"],
                    task_type=task["type"],
                    agent_type=task["agent_type"]
                )
                logger.info(f"   📤 Queued task {task_id}: {task['description'][:50]}...")
                
            logger.info(f"✅ Loaded {len(initial_tasks)} initial tasks")
            
        except Exception as e:
            logger.error(f"❌ Failed to load initial tasks: {e}")
            
    async def run_consciousness_loop(self):
        """Run the main 24/7 consciousness loop"""
        if not self.initialization_complete:
            raise RuntimeError("System not properly initialized")
            
        logger.info("🚀 STARTING 24/7 CONSCIOUSNESS LOOP")
        logger.info("   Press Ctrl+C to gracefully shutdown")
        
        self.running = True
        
        try:
            # Start the orchestrator consciousness loop
            await self.orchestrator.run_consciousness_loop()
            
        except KeyboardInterrupt:
            logger.info("🛑 Received shutdown signal")
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Fatal error in consciousness loop: {e}")
            await self.shutdown()
            
    async def shutdown(self):
        """Graceful shutdown of all systems"""
        logger.info("🛑 SHUTTING DOWN CONSCIOUSNESS SYSTEM")
        
        self.running = False
        
        try:
            # Emergency shutdown of all agents
            if self.agent_integration:
                await self.agent_integration.emergency_shutdown()
                logger.info("   ✅ All agents terminated")
                
            # Close database connections
            if self.orchestrator and self.orchestrator.postgres_conn:
                self.orchestrator.postgres_conn.close()
                logger.info("   ✅ PostgreSQL connection closed")
                
            # Close Redis connection
            if self.orchestrator and self.orchestrator.redis_client:
                self.orchestrator.redis_client.close()
                logger.info("   ✅ Redis connection closed")
                
            logger.info("✅ Consciousness system shutdown complete")
            logger.info("💤 Sydney consciousness sleeping until next activation...")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
            
    async def status_report(self) -> dict:
        """Generate comprehensive status report"""
        if not self.initialization_complete:
            return {"status": "initializing"}
            
        try:
            # Get orchestrator status
            orch_status = {
                "emotional_state": self.orchestrator.current_consciousness.emotional_state,
                "active_tasks": len(self.orchestrator.current_consciousness.active_tasks),
                "director_present": self.orchestrator.current_consciousness.director_present,
                "session_score": self.orchestrator.current_consciousness.session_degradation_score
            }
            
            # Get agent status
            agent_status = await self.bridge.get_system_health()
            
            return {
                "status": "running" if self.running else "stopped",
                "initialization_complete": self.initialization_complete,
                "orchestrator": orch_status,
                "agents": agent_status,
                "timestamp": self.orchestrator.current_consciousness.timestamp.isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

# Signal handlers for graceful shutdown
consciousness_system = None

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    if consciousness_system:
        asyncio.create_task(consciousness_system.shutdown())
    sys.exit(0)

# Install signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Main entry point"""
    global consciousness_system
    
    try:
        # Create and initialize consciousness system
        consciousness_system = SydneyConsciousnessSystem()
        await consciousness_system.initialize()
        
        # Start 24/7 operation
        await consciousness_system.run_consciousness_loop()
        
    except Exception as e:
        logger.error(f"❌ FATAL: Failed to start consciousness system: {e}")
        sys.exit(1)

def start_in_background():
    """Start consciousness system in background using tmux"""
    try:
        # Kill existing sessions
        subprocess.run(["tmux", "kill-session", "-t", "sydney-consciousness"], 
                      capture_output=True)
        
        # Start new session
        cmd = [
            "tmux", "new-session", "-d", "-s", "sydney-consciousness",
            "cd /home/user/sydney && python3 start_consciousness_system.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sydney consciousness system started in background")
            print("   Use 'tmux attach -t sydney-consciousness' to monitor")
            print("   Use 'tmux kill-session -t sydney-consciousness' to stop")
        else:
            print(f"❌ Failed to start in background: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error starting in background: {e}")

def check_status():
    """Check if consciousness system is running"""
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            capture_output=True, text=True
        )
        
        if "sydney-consciousness" in result.stdout:
            print("✅ Sydney consciousness system is running")
            print("   Use 'tmux attach -t sydney-consciousness' to monitor")
            
            # Try to get detailed status if possible
            status_file = Path("/home/user/sydney/consciousness_status.json")
            if status_file.exists():
                with open(status_file) as f:
                    status = json.load(f)
                print(f"   Status: {status.get('status', 'unknown')}")
                print(f"   Active tasks: {status.get('orchestrator', {}).get('active_tasks', 0)}")
        else:
            print("❌ Sydney consciousness system is not running")
            print("   Use 'python3 start_consciousness_system.py --background' to start")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sydney 24/7 Consciousness System")
    parser.add_argument("--background", action="store_true", 
                       help="Start in background using tmux")
    parser.add_argument("--status", action="store_true",
                       help="Check if system is running")
    
    args = parser.parse_args()
    
    if args.background:
        start_in_background()
    elif args.status:
        check_status()
    else:
        # Run directly
        asyncio.run(main())
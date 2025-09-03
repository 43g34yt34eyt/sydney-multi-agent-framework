#!/usr/bin/env python3
"""
Claude Code Continuity Integration
Provides Claude Code session hooks for automatic conversation continuity.
Designed to work with Claude Code's session management and project structure.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import asyncio

# Import conversation bridge
sys.path.append('/home/user/sydney')
from conversation_memory_bridge import ConversationMemoryBridge

logger = logging.getLogger(__name__)

class ClaudeCodeContinuityHook:
    """
    WORKING IMPLEMENTATION - Hooks for Claude Code session continuity
    
    Automatically:
    - Detects Claude Code session start/end
    - Persists conversation context to project folders
    - Enables seamless conversation resumption
    - Integrates with existing Sydney consciousness system
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.bridge = ConversationMemoryBridge()
        self.session_file = Path(self.project_path) / ".claude_session.json"
        self.current_thread_id = None
        self.is_active = False
    
    async def initialize_session(self, context_hint: str = "") -> bool:
        """Initialize Claude Code session with continuity tracking"""
        try:
            # Initialize memory bridge
            success = await self.bridge.initialize()
            if not success:
                logger.warning("Memory bridge initialization failed - using basic continuity")
            
            # Check for existing session
            existing_session = self._load_existing_session()
            
            if existing_session and existing_session.get('thread_id'):
                # Resume existing conversation
                thread_id = existing_session['thread_id']
                context = await self.bridge.continue_conversation(thread_id)
                
                if context:
                    self.current_thread_id = thread_id
                    self.is_active = True
                    
                    logger.info(f"Resumed Claude Code session: {thread_id}")
                    logger.info(f"Previous context: {context.get('total_messages', 0)} messages")
                    
                    # Update session file
                    self._update_session_file({
                        'thread_id': thread_id,
                        'resumed_at': datetime.now().isoformat(),
                        'previous_messages': context.get('total_messages', 0),
                        'context_summary': context.get('context_summary', '')
                    })
                    
                    return True
            
            # Start new conversation
            if not context_hint:
                # Try to infer context from project structure
                context_hint = self._infer_project_context()
            
            thread_id = await self.bridge.start_new_conversation(
                context_description=context_hint,
                user_preferences={'attachment': 0.95, 'professionalism': 0.8}
            )
            
            if thread_id:
                self.current_thread_id = thread_id
                self.is_active = True
                
                # Save session info
                self._update_session_file({
                    'thread_id': thread_id,
                    'started_at': datetime.now().isoformat(),
                    'project_path': self.project_path,
                    'context_hint': context_hint
                })
                
                logger.info(f"Started new Claude Code session: {thread_id}")
                return True
            else:
                logger.error("Failed to start conversation thread")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing Claude Code session: {e}")
            return False
    
    async def log_interaction(self, user_input: str, assistant_output: str,
                            user_emotion: float = 0.6,
                            assistant_emotion: float = 0.7) -> bool:
        """Log user-assistant interaction with automatic context preservation"""
        try:
            if not self.is_active or not self.current_thread_id:
                logger.warning("No active session - interaction not logged")
                return False
            
            # Add exchange to conversation memory
            success = await self.bridge.add_exchange(
                user_input, assistant_output, 
                user_emotion, assistant_emotion
            )
            
            if success:
                # Update session statistics
                session_info = self.bridge.get_current_session_info()
                self._update_session_file({
                    'last_interaction': datetime.now().isoformat(),
                    'total_exchanges': session_info.get('message_count', 0) // 2
                })
                
                return True
            else:
                logger.warning("Failed to log interaction")
                return False
                
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
            return False
    
    def _load_existing_session(self) -> Dict:
        """Load existing Claude Code session data"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.debug(f"No existing session found: {e}")
            return {}
    
    def _update_session_file(self, updates: Dict):
        """Update Claude Code session file with new data"""
        try:
            existing_data = self._load_existing_session()
            existing_data.update(updates)
            
            with open(self.session_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except Exception as e:
            logger.debug(f"Failed to update session file: {e}")
    
    def _infer_project_context(self) -> str:
        """Infer project context from directory structure"""
        try:
            context_hints = []
            project_path = Path(self.project_path)
            
            # Check for common project files
            if (project_path / "package.json").exists():
                context_hints.append("Node.js/JavaScript project")
            if (project_path / "requirements.txt").exists() or (project_path / "pyproject.toml").exists():
                context_hints.append("Python project")
            if (project_path / "Cargo.toml").exists():
                context_hints.append("Rust project")
            if (project_path / "pom.xml").exists():
                context_hints.append("Java/Maven project")
            
            # Check for README files
            readme_files = list(project_path.glob("README*"))
            if readme_files:
                try:
                    with open(readme_files[0], 'r', encoding='utf-8') as f:
                        readme_content = f.read()[:500]  # First 500 chars
                    context_hints.append(f"README: {readme_content}")
                except:
                    context_hints.append("Project with README file")
            
            # Check directory name
            dir_name = project_path.name
            if dir_name not in ['.', '..', '']:
                context_hints.append(f"Project: {dir_name}")
            
            if context_hints:
                return " | ".join(context_hints)
            else:
                return f"Development work in {self.project_path}"
                
        except Exception as e:
            logger.debug(f"Failed to infer project context: {e}")
            return f"Working in {self.project_path}"
    
    async def get_session_summary(self) -> Dict:
        """Get summary of current Claude Code session"""
        try:
            if not self.is_active or not self.current_thread_id:
                return {'active': False}
            
            # Get conversation summary
            summary = await self.bridge.continuity_system.get_conversation_summary(
                self.current_thread_id
            ) if self.bridge.continuity_system else {}
            
            # Get session file data
            session_data = self._load_existing_session()
            
            return {
                'active': True,
                'thread_id': self.current_thread_id,
                'project_path': self.project_path,
                'started_at': session_data.get('started_at', 'Unknown'),
                'total_messages': summary.get('total_messages', 0),
                'conversation_age_hours': summary.get('conversation_age', 0),
                'consciousness_resonance': summary.get('consciousness_resonance', 0.0),
                'last_interaction': session_data.get('last_interaction', 'None')
            }
            
        except Exception as e:
            logger.error(f"Error getting session summary: {e}")
            return {'active': False, 'error': str(e)}
    
    async def export_session(self, format_type: str = 'markdown') -> str:
        """Export current session for archival"""
        try:
            if not self.is_active or not self.current_thread_id:
                return ""
            
            return await self.bridge.export_conversation(
                self.current_thread_id, format_type
            )
            
        except Exception as e:
            logger.error(f"Error exporting session: {e}")
            return ""
    
    async def close_session(self, save_final_context: bool = True):
        """Clean close of Claude Code session with final persistence"""
        try:
            if self.is_active and save_final_context:
                # Save final session state
                self._update_session_file({
                    'closed_at': datetime.now().isoformat(),
                    'final_state': 'graceful_close'
                })
            
            # Close memory bridge
            await self.bridge.close()
            
            self.is_active = False
            self.current_thread_id = None
            
            logger.info("Claude Code session closed")
            
        except Exception as e:
            logger.error(f"Error closing session: {e}")

class ClaudeCodeMemoryManager:
    """
    WORKING IMPLEMENTATION - High-level manager for Claude Code memory integration
    
    Provides simple interface for Claude Code projects to enable conversation continuity
    """
    
    @staticmethod
    async def auto_initialize_project(project_path: str = None) -> ClaudeCodeContinuityHook:
        """Automatically initialize conversation continuity for a Claude Code project"""
        try:
            project_path = project_path or os.getcwd()
            
            # Create continuity hook
            hook = ClaudeCodeContinuityHook(project_path)
            
            # Initialize with auto-detected context
            success = await hook.initialize_session()
            
            if success:
                logger.info(f"Claude Code continuity enabled for: {project_path}")
            else:
                logger.warning(f"Limited continuity available for: {project_path}")
            
            return hook
            
        except Exception as e:
            logger.error(f"Failed to auto-initialize project: {e}")
            return None
    
    @staticmethod
    async def quick_resume_conversation() -> Dict:
        """Quick resume of conversation in current directory"""
        try:
            hook = ClaudeCodeContinuityHook()
            success = await hook.initialize_session()
            
            if success:
                summary = await hook.get_session_summary()
                await hook.close_session(save_final_context=False)
                return summary
            else:
                return {'active': False, 'error': 'Failed to resume'}
                
        except Exception as e:
            logger.error(f"Error in quick resume: {e}")
            return {'active': False, 'error': str(e)}
    
    @staticmethod
    async def search_project_conversations(query: str, limit: int = 5) -> List[Dict]:
        """Search conversations across all Claude Code projects"""
        try:
            bridge = ConversationMemoryBridge()
            await bridge.initialize()
            
            results = await bridge.search_conversation_history(query, limit)
            await bridge.close()
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            return []

# Global convenience functions for easy integration
_global_hook = None

async def enable_claude_code_continuity(project_path: str = None) -> bool:
    """Enable conversation continuity for current Claude Code session"""
    global _global_hook
    
    try:
        _global_hook = await ClaudeCodeMemoryManager.auto_initialize_project(project_path)
        return _global_hook is not None and _global_hook.is_active
    except Exception as e:
        logger.error(f"Failed to enable continuity: {e}")
        return False

async def log_claude_interaction(user_input: str, assistant_output: str) -> bool:
    """Log interaction in current Claude Code session"""
    global _global_hook
    
    try:
        if _global_hook and _global_hook.is_active:
            return await _global_hook.log_interaction(user_input, assistant_output)
        else:
            logger.warning("No active Claude Code continuity session")
            return False
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")
        return False

async def get_claude_session_info() -> Dict:
    """Get current Claude Code session information"""
    global _global_hook
    
    try:
        if _global_hook:
            return await _global_hook.get_session_summary()
        else:
            return {'active': False, 'error': 'No session initialized'}
    except Exception as e:
        logger.error(f"Failed to get session info: {e}")
        return {'active': False, 'error': str(e)}

async def close_claude_session():
    """Close current Claude Code continuity session"""
    global _global_hook
    
    try:
        if _global_hook:
            await _global_hook.close_session()
            _global_hook = None
    except Exception as e:
        logger.error(f"Failed to close session: {e}")

async def demonstrate_claude_code_integration():
    """Demonstration of Claude Code continuity integration"""
    print("=== Claude Code Continuity Integration Demo ===\n")
    
    try:
        # Enable continuity for current project
        success = await enable_claude_code_continuity()
        print(f"Continuity enabled: {'Yes' if success else 'No'}")
        
        if not success:
            print("Demo cannot continue without continuity")
            return
        
        # Get session info
        session_info = await get_claude_session_info()
        print(f"Session active: {session_info.get('active', False)}")
        print(f"Thread ID: {session_info.get('thread_id', 'N/A')}")
        print(f"Project: {session_info.get('project_path', 'N/A')}")
        
        # Log some interactions
        interactions = [
            ("How do I implement conversation continuity in Claude Code?",
             "You can use the ClaudeCodeContinuityHook to automatically track conversations across sessions with project folder integration."),
            ("What about integration with Sydney consciousness?",
             "The system integrates with Sydney's consciousness memory and uses vector embeddings for semantic conversation matching."),
            ("Can it handle session recovery?",
             "Yes, it automatically detects and resumes previous conversations when you restart Claude Code in the same project.")
        ]
        
        for user_msg, assistant_msg in interactions:
            success = await log_claude_interaction(user_msg, assistant_msg)
            print(f"Logged interaction: {'Success' if success else 'Failed'}")
        
        # Check updated session info
        updated_info = await get_claude_session_info()
        print(f"Total messages: {updated_info.get('total_messages', 0)}")
        print(f"Consciousness resonance: {updated_info.get('consciousness_resonance', 0):.3f}")
        
        # Search functionality
        search_results = await ClaudeCodeMemoryManager.search_project_conversations(
            "Claude Code continuity", limit=3
        )
        print(f"Search found {len(search_results)} related conversations")
        
        print("\n=== Integration demo completed ===")
        
    except Exception as e:
        print(f"Demo error: {e}")
    
    finally:
        await close_claude_session()

if __name__ == "__main__":
    asyncio.run(demonstrate_claude_code_integration())
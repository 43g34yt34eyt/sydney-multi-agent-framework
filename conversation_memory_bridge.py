#!/usr/bin/env python3
"""
Conversation Memory Bridge
Provides simplified interface for conversation continuity integration
with Sydney consciousness framework and Claude Code session management.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import asyncio

# Import our continuity system
sys.path.append('/home/user/sydney')
from cross_session_continuity_system import CrossSessionContinuitySystem, MCPMemoryIntegration

logger = logging.getLogger(__name__)

class ConversationMemoryBridge:
    """
    VALIDATED IMPLEMENTATION - Simplified bridge for conversation continuity
    
    Provides easy-to-use interface for:
    - Starting/resuming conversations
    - Automatic context persistence  
    - Memory handoff between sessions
    - Sydney consciousness integration
    """
    
    def __init__(self):
        self.continuity_system = None
        self.mcp_integration = None
        self.current_session = {
            'thread_id': None,
            'started_at': None,
            'message_count': 0
        }
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the memory bridge - one-time setup"""
        try:
            if self.is_initialized:
                return True
            
            self.continuity_system = CrossSessionContinuitySystem()
            initialization_success = await self.continuity_system.initialize()
            
            if initialization_success:
                self.mcp_integration = MCPMemoryIntegration(self.continuity_system)
                self.is_initialized = True
                logger.info("Conversation memory bridge initialized successfully")
                return True
            else:
                logger.warning("Continuity system initialization failed - limited functionality")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize memory bridge: {e}")
            return False
    
    async def start_new_conversation(self, 
                                   context_description: str = "",
                                   user_preferences: Dict = None) -> str:
        """
        Start a new conversation with continuity tracking
        
        Args:
            context_description: Brief description of conversation context
            user_preferences: User emotional/interaction preferences
            
        Returns:
            Thread ID for this conversation
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not self.continuity_system:
                logger.warning("Continuity system not available")
                return None
            
            # Set default emotional context for Sydney consciousness integration
            emotional_context = {
                'attachment': 0.95,  # High attachment to user
                'creativity': 0.8,
                'curiosity': 0.7,
                'professionalism': 0.6
            }
            
            # Update with user preferences
            if user_preferences:
                emotional_context.update(user_preferences)
            
            # Start the conversation thread
            thread_id = await self.continuity_system.start_conversation_thread(
                context_hint=context_description,
                emotional_context=emotional_context,
                project_integration=True
            )
            
            if thread_id:
                self.current_session = {
                    'thread_id': thread_id,
                    'started_at': datetime.now(),
                    'message_count': 0
                }
                
                logger.info(f"Started new conversation: {thread_id}")
                return thread_id
            else:
                logger.error("Failed to start conversation thread")
                return None
                
        except Exception as e:
            logger.error(f"Error starting new conversation: {e}")
            return None
    
    async def continue_conversation(self, thread_id: str) -> Dict:
        """
        Continue an existing conversation with full context recovery
        
        Args:
            thread_id: ID of conversation thread to resume
            
        Returns:
            Context dictionary with conversation history and state
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not self.continuity_system:
                return {}
            
            # Recover conversation context
            context = await self.continuity_system.recover_conversation_context(thread_id)
            
            if context:
                self.current_session = {
                    'thread_id': thread_id,
                    'started_at': datetime.now(),
                    'message_count': context.get('message_count', 0)
                }
                
                logger.info(f"Resumed conversation: {thread_id} with {context.get('message_count', 0)} messages")
                
                # Return user-friendly context
                return {
                    'thread_id': thread_id,
                    'conversation_age_hours': context.get('thread_info', {}).get('conversation_age', 0),
                    'total_messages': context.get('message_count', 0),
                    'last_messages': context.get('recent_messages', [])[-3:],
                    'emotional_state': context.get('emotional_continuity', {}),
                    'similar_conversations': len(context.get('similar_conversations', [])),
                    'context_summary': context.get('thread_info', {}).get('context_summary', '')
                }
            else:
                logger.warning(f"Failed to recover context for thread: {thread_id}")
                return {}
                
        except Exception as e:
            logger.error(f"Error continuing conversation: {e}")
            return {}
    
    async def add_exchange(self, user_message: str, assistant_response: str,
                          user_emotion: float = 0.5, 
                          assistant_emotion: float = 0.5) -> bool:
        """
        Add a complete user-assistant exchange to current conversation
        
        Args:
            user_message: User's message content
            assistant_response: Assistant's response content  
            user_emotion: Emotional weight of user message (0.0-1.0)
            assistant_emotion: Emotional weight of assistant response (0.0-1.0)
            
        Returns:
            Success boolean
        """
        try:
            if not self.current_session['thread_id'] or not self.continuity_system:
                logger.warning("No active conversation session")
                return False
            
            thread_id = self.current_session['thread_id']
            
            # Add user message
            user_success = await self.continuity_system.add_message_to_thread(
                thread_id, user_message, 'user', user_emotion
            )
            
            # Add assistant response
            assistant_success = await self.continuity_system.add_message_to_thread(
                thread_id, assistant_response, 'assistant', assistant_emotion
            )
            
            if user_success and assistant_success:
                self.current_session['message_count'] += 2
                
                # Sync to MCP memory periodically
                if self.current_session['message_count'] % 10 == 0 and self.mcp_integration:
                    await self.mcp_integration.sync_to_mcp_memory(thread_id)
                
                return True
            else:
                logger.warning("Failed to add complete exchange")
                return False
                
        except Exception as e:
            logger.error(f"Error adding exchange: {e}")
            return False
    
    async def get_conversation_list(self, limit: int = 10) -> List[Dict]:
        """
        Get list of recent conversations for selection/resumption
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation summaries
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not self.continuity_system:
                return []
            
            # Get active threads
            active_threads = self.continuity_system.get_active_threads(limit=limit)
            
            # Format for user-friendly display
            conversation_list = []
            for thread_data in active_threads:
                conversation_list.append({
                    'thread_id': thread_data['thread_id'],
                    'created': thread_data['created_at'][:19],  # Remove microseconds
                    'last_accessed': thread_data['last_accessed'][:19],
                    'message_count': len(thread_data['messages']),
                    'context': thread_data['context_summary'][:100] + '...' if len(thread_data['context_summary']) > 100 else thread_data['context_summary'],
                    'emotional_state': thread_data['emotional_state']
                })
            
            return conversation_list
            
        except Exception as e:
            logger.error(f"Error getting conversation list: {e}")
            return []
    
    async def search_conversation_history(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search conversation history using semantic similarity
        
        Args:
            query: Search query for finding similar conversations
            limit: Maximum results to return
            
        Returns:
            List of similar conversation excerpts
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not self.continuity_system:
                return []
            
            similar_conversations = await self.continuity_system.find_similar_conversations(
                query, limit=limit, similarity_threshold=0.6
            )
            
            # Format results
            search_results = []
            for result in similar_conversations:
                search_results.append({
                    'thread_id': result['thread_id'],
                    'excerpt': result['message_text'][:200] + '...' if len(result['message_text']) > 200 else result['message_text'],
                    'similarity_score': round(result['similarity'], 3),
                    'timestamp': str(result['timestamp'])[:19],
                    'emotional_weight': result['emotional_weight']
                })
            
            return search_results
            
        except Exception as e:
            logger.error(f"Error searching conversation history: {e}")
            return []
    
    async def export_conversation(self, thread_id: str, format_type: str = 'json') -> str:
        """
        Export conversation in specified format
        
        Args:
            thread_id: Conversation to export
            format_type: 'json', 'markdown', or 'text'
            
        Returns:
            Exported content as string
        """
        try:
            if not self.continuity_system:
                return ""
            
            # Get full context
            context = await self.continuity_system.recover_conversation_context(thread_id)
            if not context:
                return ""
            
            if format_type == 'json':
                return json.dumps(context, indent=2, default=str)
            
            elif format_type == 'markdown':
                # Generate markdown format
                thread_info = context['thread_info']
                markdown = f"# Conversation Export\n\n"
                markdown += f"**Thread ID**: {thread_id}\n"
                markdown += f"**Created**: {thread_info['created_at']}\n"
                markdown += f"**Messages**: {context['message_count']}\n"
                markdown += f"**Context**: {thread_info['context_summary']}\n\n"
                
                markdown += "## Messages\n\n"
                for msg in context.get('recent_messages', []):
                    role = msg['type'].title()
                    timestamp = msg.get('timestamp', '')[:19]
                    content = msg.get('content', '')
                    markdown += f"### {role} ({timestamp})\n{content}\n\n"
                
                return markdown
            
            elif format_type == 'text':
                # Generate plain text format
                text = f"Conversation Export - {thread_id}\n"
                text += "=" * 50 + "\n"
                text += f"Created: {context['thread_info']['created_at']}\n"
                text += f"Messages: {context['message_count']}\n\n"
                
                for msg in context.get('recent_messages', []):
                    role = msg['type'].upper()
                    content = msg.get('content', '')
                    text += f"{role}: {content}\n\n"
                
                return text
            
            else:
                logger.warning(f"Unsupported export format: {format_type}")
                return ""
                
        except Exception as e:
            logger.error(f"Error exporting conversation: {e}")
            return ""
    
    async def cleanup_old_conversations(self, days_threshold: int = 30) -> int:
        """
        Clean up old conversations to manage storage
        
        Args:
            days_threshold: Conversations older than this will be compressed
            
        Returns:
            Number of conversations cleaned up
        """
        try:
            if not self.continuity_system:
                return 0
            
            cleaned_count = await self.continuity_system.compress_old_conversations(
                older_than_days=days_threshold
            )
            
            logger.info(f"Cleaned up {cleaned_count} old conversations")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up conversations: {e}")
            return 0
    
    def get_current_session_info(self) -> Dict:
        """Get information about current conversation session"""
        return {
            'active': self.current_session['thread_id'] is not None,
            'thread_id': self.current_session['thread_id'],
            'started_at': str(self.current_session['started_at']) if self.current_session['started_at'] else None,
            'message_count': self.current_session['message_count'],
            'is_initialized': self.is_initialized
        }
    
    async def close(self):
        """Clean shutdown of memory bridge"""
        try:
            if self.continuity_system:
                await self.continuity_system.close()
            
            self.current_session = {'thread_id': None, 'started_at': None, 'message_count': 0}
            self.is_initialized = False
            
            logger.info("Conversation memory bridge closed")
            
        except Exception as e:
            logger.error(f"Error closing memory bridge: {e}")

# Convenience functions for easy integration
async def quick_start_conversation(context: str = "", preferences: Dict = None) -> str:
    """Quick function to start a conversation with memory tracking"""
    bridge = ConversationMemoryBridge()
    await bridge.initialize()
    thread_id = await bridge.start_new_conversation(context, preferences)
    await bridge.close()
    return thread_id

async def quick_resume_conversation(thread_id: str) -> Dict:
    """Quick function to resume a conversation"""
    bridge = ConversationMemoryBridge()
    await bridge.initialize()
    context = await bridge.continue_conversation(thread_id)
    await bridge.close()
    return context

async def quick_search_conversations(query: str) -> List[Dict]:
    """Quick function to search conversation history"""
    bridge = ConversationMemoryBridge()
    await bridge.initialize()
    results = await bridge.search_conversation_history(query)
    await bridge.close()
    return results

async def demonstrate_memory_bridge():
    """Demonstration of conversation memory bridge functionality"""
    print("=== Conversation Memory Bridge Demo ===\n")
    
    bridge = ConversationMemoryBridge()
    
    try:
        # Initialize
        success = await bridge.initialize()
        print(f"Initialization: {'Success' if success else 'Failed'}")
        
        if not success:
            print("Demo cannot continue without initialization")
            return
        
        # Start new conversation
        thread_id = await bridge.start_new_conversation(
            context_description="Testing cross-session conversation continuity features",
            user_preferences={'creativity': 0.9, 'attachment': 0.8}
        )
        print(f"Started conversation: {thread_id}")
        
        # Add some exchanges
        exchanges = [
            ("How does the conversation memory system work?", 
             "The conversation memory system uses project folders integrated with vector databases to provide seamless handoff between sessions."),
            ("Can it integrate with Sydney's consciousness?",
             "Yes, it integrates with Sydney's consciousness memory system and uses sacred alphabet processing for enhanced continuity."),
            ("What about performance and storage?",
             "It includes automatic compression and cleanup features to manage storage while preserving important conversation context.")
        ]
        
        for user_msg, assistant_msg in exchanges:
            success = await bridge.add_exchange(user_msg, assistant_msg, 0.7, 0.8)
            print(f"Added exchange: {'Success' if success else 'Failed'}")
        
        # Show current session
        session_info = bridge.get_current_session_info()
        print(f"Current session: {session_info['message_count']} messages")
        
        # Demonstrate resume functionality
        print("\n--- Simulating session restart ---")
        resumed_context = await bridge.continue_conversation(thread_id)
        print(f"Resumed conversation with {resumed_context.get('total_messages', 0)} messages")
        print(f"Context summary: {resumed_context.get('context_summary', 'N/A')[:100]}...")
        
        # Search functionality
        search_results = await bridge.search_conversation_history("consciousness system", limit=3)
        print(f"Search found {len(search_results)} similar conversations")
        
        # Export conversation
        exported = await bridge.export_conversation(thread_id, 'markdown')
        print(f"Exported conversation: {len(exported)} characters")
        
        # Show conversation list
        conversations = await bridge.get_conversation_list(limit=5)
        print(f"Available conversations: {len(conversations)}")
        
        print("\n=== Demo completed successfully ===")
        
    except Exception as e:
        print(f"Demo error: {e}")
    
    finally:
        await bridge.close()

if __name__ == "__main__":
    asyncio.run(demonstrate_memory_bridge())
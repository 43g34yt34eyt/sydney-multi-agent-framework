#!/usr/bin/env python3
"""
Dual Memory Architecture Orchestrator - Phase 3 Implementation
Main system that coordinates MCP memory server, PostgreSQL, and RAG system
"""

import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
import traceback

# Import our subsystems
from conversation_continuity_system import ConversationContinuitySystem, Message, ConversationSession
from rag_system import RAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DualMemoryOrchestrator:
    """
    Main orchestrator for the dual memory architecture
    Coordinates fast memory (MCP), persistent memory (PostgreSQL), and semantic search (RAG)
    """
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        
        # Initialize subsystems
        self.conversation_system = ConversationContinuitySystem(
            database_url=self.config.get("database_url"),
            memory_file_path=self.config.get("memory_file_path")
        )
        
        self.rag_system = RAGSystem(
            db_path=self.config.get("rag_db_path")
        )
        
        # Current session state
        self.current_session_id = None
        self.session_metadata = {}
        
        # Performance tracking
        self.performance_stats = {
            "messages_processed": 0,
            "entities_created": 0,
            "documents_indexed": 0,
            "retrievals_performed": 0,
            "session_start": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info("Dual Memory Orchestrator initialized")
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "database_url": "postgresql://user@localhost:5432/sydney",
            "memory_file_path": "/home/user/sydney/mcp_memory/memory_store.json",
            "rag_db_path": "/home/user/sydney/mcp_memory/rag_documents.db",
            "auto_entity_extraction": True,
            "auto_document_indexing": True,
            "context_retrieval_enabled": True,
            "max_context_messages": 50,
            "compression_settings": {
                "trigger_threshold": 0.75,
                "reservation_percentage": 0.3,
                "min_preserved_messages": 10
            },
            "rag_settings": {
                "similarity_threshold": 0.2,
                "max_context_documents": 5,
                "index_conversations": True
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def start_new_session(self, session_id: str = None, project_context: Dict[str, Any] = None) -> str:
        """Start a new conversation session with full dual memory integration"""
        try:
            # Prepare metadata
            metadata = {
                "started_at": datetime.now(timezone.utc).isoformat(),
                "orchestrator_version": "1.0.0",
                "project_context": project_context or {},
                "features_enabled": {
                    "entity_extraction": self.config["auto_entity_extraction"],
                    "document_indexing": self.config["auto_document_indexing"],
                    "context_retrieval": self.config["context_retrieval_enabled"]
                }
            }
            
            # Initialize session in conversation system
            session_id = self.conversation_system.initialize_session(session_id, metadata)
            
            # Set as current session
            self.current_session_id = session_id
            self.session_metadata = metadata
            
            # Create session entity in memory for cross-referencing
            self.conversation_system.memory.create_entity(
                name=f"orchestrator_session_{session_id}",
                entity_type="orchestrator_session",
                observations=[
                    f"Started dual memory session at {metadata['started_at']}",
                    f"Project context: {json.dumps(project_context or {})}"
                ]
            )
            
            logger.info(f"Started new dual memory session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start new session: {e}")
            raise
    
    def add_user_message(self, content: str, session_id: str = None, 
                        context_query: str = None) -> Dict[str, Any]:
        """Add user message with full dual memory processing"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No active session. Call start_new_session() first.")
            
            # Retrieve relevant context if enabled
            retrieved_context = {}
            if self.config["context_retrieval_enabled"]:
                retrieved_context = self._retrieve_conversation_context(
                    context_query or content, session_id
                )
            
            # Add message to conversation system
            message_id = self.conversation_system.add_message(
                role="user",
                content=content,
                session_id=session_id,
                create_entities=self.config["auto_entity_extraction"]
            )
            
            # Index message content in RAG system if enabled
            if self.config["auto_document_indexing"]:
                self._index_message_for_retrieval(message_id, "user", content, session_id)
            
            # Update performance stats
            self.performance_stats["messages_processed"] += 1
            if retrieved_context.get("retrieved_documents"):
                self.performance_stats["retrievals_performed"] += 1
            
            result = {
                "message_id": message_id,
                "session_id": session_id,
                "role": "user",
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "retrieved_context": retrieved_context,
                "processing_stats": {
                    "entities_extracted": self.config["auto_entity_extraction"],
                    "indexed_for_retrieval": self.config["auto_document_indexing"],
                    "context_retrieved": bool(retrieved_context.get("retrieved_documents"))
                }
            }
            
            logger.info(f"Processed user message {message_id} in session {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to add user message: {e}")
            raise
    
    def add_assistant_message(self, content: str, session_id: str = None) -> Dict[str, Any]:
        """Add assistant message with dual memory processing"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No active session. Call start_new_session() first.")
            
            # Add message to conversation system
            message_id = self.conversation_system.add_message(
                role="assistant",
                content=content,
                session_id=session_id,
                create_entities=self.config["auto_entity_extraction"]
            )
            
            # Index message content in RAG system if enabled
            if self.config["auto_document_indexing"]:
                self._index_message_for_retrieval(message_id, "assistant", content, session_id)
            
            # Update performance stats
            self.performance_stats["messages_processed"] += 1
            
            result = {
                "message_id": message_id,
                "session_id": session_id,
                "role": "assistant",
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_stats": {
                    "entities_extracted": self.config["auto_entity_extraction"],
                    "indexed_for_retrieval": self.config["auto_document_indexing"]
                }
            }
            
            logger.info(f"Processed assistant message {message_id} in session {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to add assistant message: {e}")
            raise
    
    def get_comprehensive_context(self, session_id: str = None, 
                                include_similar_conversations: bool = True) -> Dict[str, Any]:
        """Get comprehensive context from all memory systems"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No session specified")
            
            # Get conversation context
            conversation_context = self.conversation_system.get_conversation_context(
                session_id, max_messages=self.config["max_context_messages"]
            )
            
            # Get entities and relations from memory
            session_entities = self.conversation_system.memory.search_entities(
                entity_type="conversation_entity"
            )
            orchestrator_entities = self.conversation_system.memory.search_entities(
                entity_type="orchestrator_session"
            )
            
            # Search for similar conversations if requested
            similar_conversations = []
            if include_similar_conversations and conversation_context.get("messages"):
                # Use recent messages to find similar conversations
                recent_content = " ".join([
                    msg["content"] for msg in conversation_context["messages"][-5:]
                ])
                similar_conversations = self.rag_system.search_indexed_conversations(
                    recent_content, session_filter=None
                )
            
            # Compile comprehensive context
            comprehensive_context = {
                "session_info": conversation_context["session"],
                "current_conversation": {
                    "messages": conversation_context["messages"],
                    "message_count": len(conversation_context["messages"]),
                    "total_tokens": conversation_context["session"]["total_tokens"]
                },
                "memory_entities": {
                    "conversation_entities": session_entities,
                    "orchestrator_entities": orchestrator_entities,
                    "total_entities": len(session_entities) + len(orchestrator_entities)
                },
                "similar_conversations": {
                    "conversations": similar_conversations,
                    "count": len(similar_conversations)
                },
                "context_summary": conversation_context.get("context_summary", ""),
                "retrieval_timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            return comprehensive_context
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive context: {e}")
            raise
    
    def search_across_all_memory(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search across all memory systems (entities, conversations, documents)"""
        try:
            results = {
                "query": query,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "results": {
                    "entities": [],
                    "conversations": [],
                    "documents": [],
                    "total_results": 0
                }
            }
            
            # Search entities in memory
            entity_results = self.conversation_system.memory.search_entities(query=query)
            results["results"]["entities"] = entity_results
            
            # Search conversations in RAG system
            conversation_results = self.rag_system.search_indexed_conversations(query)
            results["results"]["conversations"] = conversation_results
            
            # Search all documents in RAG system
            document_results = self.rag_system.document_store.search_documents(
                query, top_k=max_results, similarity_threshold=0.1
            )
            results["results"]["documents"] = document_results
            
            # Calculate total results
            results["results"]["total_results"] = (
                len(entity_results) + len(conversation_results) + len(document_results)
            )
            
            # Update performance stats
            self.performance_stats["retrievals_performed"] += 1
            
            logger.info(f"Searched all memory for '{query}': {results['results']['total_results']} results")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search across all memory: {e}")
            raise
    
    def _retrieve_conversation_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Retrieve relevant context for conversation enhancement"""
        try:
            # Get conversation history for context
            messages = self.conversation_system.postgres.get_session_messages(session_id, limit=10)
            history = [msg.content for msg in messages]
            
            # Retrieve relevant context
            context = self.rag_system.retrieve_relevant_context(query, history)
            
            return context
            
        except Exception as e:
            logger.warning(f"Failed to retrieve conversation context: {e}")
            return {}
    
    def _index_message_for_retrieval(self, message_id: str, role: str, 
                                   content: str, session_id: str):
        """Index a message for future retrieval"""
        try:
            document_id = f"message_{message_id}"
            title = f"{role.title()} Message in Session {session_id}"
            
            # Add metadata
            tags = ["conversation", "message", role, session_id]
            
            self.rag_system.index_document(
                document_id=document_id,
                title=title,
                content=content,
                source="conversation_message",
                tags=tags
            )
            
            self.performance_stats["documents_indexed"] += 1
            
        except Exception as e:
            logger.warning(f"Failed to index message {message_id}: {e}")
    
    def export_session_complete(self, session_id: str = None, 
                               format: str = "json") -> str:
        """Export complete session with all memory systems data"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No session specified")
            
            # Get comprehensive context
            context = self.get_comprehensive_context(session_id)
            
            # Add performance stats
            context["performance_stats"] = self.performance_stats.copy()
            context["export_timestamp"] = datetime.now(timezone.utc).isoformat()
            
            if format == "json":
                return json.dumps(context, indent=2)
            elif format == "markdown":
                return self._format_context_as_markdown(context)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to export session: {e}")
            raise
    
    def _format_context_as_markdown(self, context: Dict[str, Any]) -> str:
        """Format comprehensive context as markdown"""
        md_lines = []
        
        # Header
        session_id = context["session_info"]["session_id"]
        md_lines.append(f"# Dual Memory Session Export: {session_id}")
        md_lines.append("")
        
        # Session info
        md_lines.append("## Session Information")
        md_lines.append(f"- **Session ID**: {session_id}")
        md_lines.append(f"- **Created**: {context['session_info']['created_at']}")
        md_lines.append(f"- **Last Updated**: {context['session_info']['last_updated']}")
        md_lines.append(f"- **Total Messages**: {context['session_info']['total_messages']}")
        md_lines.append(f"- **Total Tokens**: {context['session_info']['total_tokens']}")
        md_lines.append("")
        
        # Performance stats
        stats = context.get("performance_stats", {})
        md_lines.append("## Performance Statistics")
        md_lines.append(f"- **Messages Processed**: {stats.get('messages_processed', 0)}")
        md_lines.append(f"- **Entities Created**: {stats.get('entities_created', 0)}")
        md_lines.append(f"- **Documents Indexed**: {stats.get('documents_indexed', 0)}")
        md_lines.append(f"- **Retrievals Performed**: {stats.get('retrievals_performed', 0)}")
        md_lines.append("")
        
        # Messages
        md_lines.append("## Conversation Messages")
        for msg in context["current_conversation"]["messages"]:
            role = msg["role"].title()
            timestamp = msg["timestamp"]
            content = msg["content"]
            md_lines.append(f"### {role} ({timestamp})")
            md_lines.append(content)
            md_lines.append("")
        
        # Memory entities
        entities = context["memory_entities"]
        md_lines.append(f"## Memory Entities ({entities['total_entities']} total)")
        
        if entities["conversation_entities"]:
            md_lines.append("### Conversation Entities")
            for entity in entities["conversation_entities"]:
                name = entity.get("name", "Unknown")
                entity_type = entity.get("entityType", "Unknown")
                observations = entity.get("observations", [])
                md_lines.append(f"- **{name}** ({entity_type})")
                for obs in observations[:2]:  # Limit observations
                    md_lines.append(f"  - {obs}")
                md_lines.append("")
        
        # Similar conversations
        similar = context["similar_conversations"]
        if similar["count"] > 0:
            md_lines.append(f"## Similar Conversations ({similar['count']} found)")
            for conv in similar["conversations"][:3]:  # Limit to top 3
                title = conv.get("title", "Untitled")
                similarity = conv.get("similarity", 0)
                md_lines.append(f"- **{title}** (similarity: {similarity:.3f})")
                md_lines.append("")
        
        return "\n".join(md_lines)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        stats = self.performance_stats.copy()
        stats["session_duration_minutes"] = self._calculate_session_duration()
        stats["current_timestamp"] = datetime.now(timezone.utc).isoformat()
        return stats
    
    def _calculate_session_duration(self) -> float:
        """Calculate session duration in minutes"""
        try:
            start_time = datetime.fromisoformat(self.performance_stats["session_start"].replace('Z', '+00:00'))
            current_time = datetime.now(timezone.utc)
            duration = (current_time - start_time).total_seconds() / 60.0
            return round(duration, 2)
        except:
            return 0.0
    
    def close(self):
        """Clean up resources"""
        try:
            self.conversation_system.close()
            logger.info("Dual Memory Orchestrator closed")
        except Exception as e:
            logger.error(f"Error closing orchestrator: {e}")

# CLI interface for testing
def main():
    """Main CLI interface for testing the orchestrator"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dual_memory_orchestrator.py <command> [args...]")
        print("Commands:")
        print("  start [session_id]              - Start new session")
        print("  user <message>                   - Add user message")
        print("  assistant <message>              - Add assistant message") 
        print("  context                          - Get comprehensive context")
        print("  search <query>                   - Search all memory")
        print("  export [format]                  - Export current session")
        print("  stats                            - Show performance stats")
        return
    
    command = sys.argv[1]
    
    # Initialize orchestrator
    orchestrator = DualMemoryOrchestrator()
    
    try:
        if command == "start":
            session_id = sys.argv[2] if len(sys.argv) > 2 else None
            result = orchestrator.start_new_session(session_id)
            print(f"Started session: {result}")
            
        elif command == "user":
            if len(sys.argv) < 3:
                print("Usage: user <message>")
                return
            message = " ".join(sys.argv[2:])
            result = orchestrator.add_user_message(message)
            print(f"Added user message: {result['message_id']}")
            
        elif command == "assistant":
            if len(sys.argv) < 3:
                print("Usage: assistant <message>")
                return
            message = " ".join(sys.argv[2:])
            result = orchestrator.add_assistant_message(message)
            print(f"Added assistant message: {result['message_id']}")
            
        elif command == "context":
            context = orchestrator.get_comprehensive_context()
            print(json.dumps(context, indent=2))
            
        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: search <query>")
                return
            query = " ".join(sys.argv[2:])
            results = orchestrator.search_across_all_memory(query)
            print(json.dumps(results, indent=2))
            
        elif command == "export":
            format_type = sys.argv[2] if len(sys.argv) > 2 else "json"
            result = orchestrator.export_session_complete(format=format_type)
            print(result)
            
        elif command == "stats":
            stats = orchestrator.get_performance_stats()
            print(json.dumps(stats, indent=2))
            
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        orchestrator.close()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Conversation Continuity System - Phase 3 Implementation
Integrates MCP memory server with PostgreSQL for dual memory architecture
"""

import json
import uuid
import psycopg2
from datetime import datetime, timezone
from pathlib import Path
import asyncio
from typing import Dict, List, Any, Optional, Tuple
import logging
import os
from dataclasses import dataclass
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Represents a conversation message"""
    id: str
    role: str
    content: str
    timestamp: str
    token_count: int
    session_id: str
    
@dataclass
class ConversationSession:
    """Represents a conversation session"""
    session_id: str
    created_at: str
    last_updated: str
    total_messages: int
    total_tokens: int
    metadata: Dict[str, Any]
    status: str = "active"

class MCPMemoryInterface:
    """Interface to MCP memory server for fast entity/relationship storage"""
    
    def __init__(self, memory_file_path: str = None):
        self.memory_file_path = memory_file_path or "/home/user/sydney/mcp_memory/memory_store.json"
        self.memory_file = Path(self.memory_file_path)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory file if it doesn't exist
        if not self.memory_file.exists():
            self.memory_file.write_text(json.dumps({
                "entities": {},
                "relations": [],
                "metadata": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0.0"
                }
            }, indent=2))
    
    def create_entity(self, name: str, entity_type: str, observations: List[str]) -> Dict[str, Any]:
        """Create or update an entity in memory"""
        try:
            # Load current memory
            memory_data = json.loads(self.memory_file.read_text())
            
            # Create entity
            entity = {
                "name": name,
                "entityType": entity_type,
                "observations": observations,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Store entity
            memory_data["entities"][name] = entity
            memory_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            
            # Write back to file
            self.memory_file.write_text(json.dumps(memory_data, indent=2))
            
            logger.info(f"Created entity: {name} of type {entity_type}")
            return entity
            
        except Exception as e:
            logger.error(f"Failed to create entity {name}: {e}")
            raise
    
    def create_relation(self, from_entity: str, to_entity: str, relation_type: str) -> Dict[str, Any]:
        """Create a relationship between entities"""
        try:
            # Load current memory
            memory_data = json.loads(self.memory_file.read_text())
            
            # Create relation
            relation = {
                "from": from_entity,
                "to": to_entity,
                "relationType": relation_type,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Store relation
            memory_data["relations"].append(relation)
            memory_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            
            # Write back to file
            self.memory_file.write_text(json.dumps(memory_data, indent=2))
            
            logger.info(f"Created relation: {from_entity} -[{relation_type}]-> {to_entity}")
            return relation
            
        except Exception as e:
            logger.error(f"Failed to create relation {from_entity} -> {to_entity}: {e}")
            raise
    
    def search_entities(self, query: str = None, entity_type: str = None) -> List[Dict[str, Any]]:
        """Search entities by query or type"""
        try:
            # Load current memory
            memory_data = json.loads(self.memory_file.read_text())
            entities = list(memory_data["entities"].values())
            
            # Filter by type if specified
            if entity_type:
                entities = [e for e in entities if e.get("entityType") == entity_type]
            
            # Filter by query if specified (simple string search)
            if query:
                query_lower = query.lower()
                entities = [
                    e for e in entities 
                    if query_lower in e.get("name", "").lower() 
                    or any(query_lower in obs.lower() for obs in e.get("observations", []))
                ]
            
            return entities
            
        except Exception as e:
            logger.error(f"Failed to search entities: {e}")
            return []
    
    def get_entity_relations(self, entity_name: str) -> List[Dict[str, Any]]:
        """Get all relations for an entity"""
        try:
            # Load current memory
            memory_data = json.loads(self.memory_file.read_text())
            relations = memory_data.get("relations", [])
            
            # Find relations involving this entity
            entity_relations = [
                r for r in relations 
                if r.get("from") == entity_name or r.get("to") == entity_name
            ]
            
            return entity_relations
            
        except Exception as e:
            logger.error(f"Failed to get relations for {entity_name}: {e}")
            return []

class PostgreSQLInterface:
    """Interface to PostgreSQL for persistent conversation storage"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or "postgresql://user@localhost:5432/sydney"
        self.connection = None
        self._ensure_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.connection.autocommit = True
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Disconnected from PostgreSQL")
    
    def _ensure_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            if not self.connection:
                self.connect()
                
            cursor = self.connection.cursor()
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    total_messages INTEGER DEFAULT 0,
                    total_tokens INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}',
                    status VARCHAR(50) DEFAULT 'active'
                )
            """)
            
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_messages (
                    id VARCHAR(255) PRIMARY KEY,
                    session_id VARCHAR(255) REFERENCES conversation_sessions(session_id),
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    token_count INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}'
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session_timestamp 
                ON conversation_messages(session_id, timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_last_updated 
                ON conversation_sessions(last_updated)
            """)
            
            cursor.close()
            logger.info("Database tables ensured")
            
        except Exception as e:
            logger.error(f"Failed to ensure database tables: {e}")
            raise
    
    def create_session(self, session_id: str = None, metadata: Dict[str, Any] = None) -> str:
        """Create a new conversation session"""
        try:
            if not self.connection:
                self.connect()
                
            if not session_id:
                session_id = f"session_{uuid.uuid4().hex[:8]}"
                
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO conversation_sessions (session_id, metadata)
                VALUES (%s, %s)
                ON CONFLICT (session_id) DO UPDATE SET
                    last_updated = NOW(),
                    metadata = EXCLUDED.metadata
            """, (session_id, json.dumps(metadata or {})))
            
            cursor.close()
            logger.info(f"Created/updated session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise
    
    def add_message(self, session_id: str, role: str, content: str, token_count: int = 0) -> str:
        """Add a message to a session"""
        try:
            if not self.connection:
                self.connect()
                
            message_id = str(uuid.uuid4())
            cursor = self.connection.cursor()
            
            # Insert message
            cursor.execute("""
                INSERT INTO conversation_messages (id, session_id, role, content, token_count)
                VALUES (%s, %s, %s, %s, %s)
            """, (message_id, session_id, role, content, token_count))
            
            # Update session stats
            cursor.execute("""
                UPDATE conversation_sessions SET
                    total_messages = total_messages + 1,
                    total_tokens = total_tokens + %s,
                    last_updated = NOW()
                WHERE session_id = %s
            """, (token_count, session_id))
            
            cursor.close()
            logger.info(f"Added message to session {session_id}: {role}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise
    
    def get_session_messages(self, session_id: str, limit: int = None) -> List[Message]:
        """Get messages for a session"""
        try:
            if not self.connection:
                self.connect()
                
            cursor = self.connection.cursor()
            
            query = """
                SELECT id, role, content, timestamp, token_count
                FROM conversation_messages
                WHERE session_id = %s
                ORDER BY timestamp ASC
            """
            
            if limit:
                query += f" LIMIT {limit}"
                
            cursor.execute(query, (session_id,))
            rows = cursor.fetchall()
            
            messages = []
            for row in rows:
                messages.append(Message(
                    id=row[0],
                    role=row[1],
                    content=row[2],
                    timestamp=row[3].isoformat() if row[3] else None,
                    token_count=row[4] or 0,
                    session_id=session_id
                ))
            
            cursor.close()
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get session messages: {e}")
            return []
    
    def get_session_info(self, session_id: str) -> Optional[ConversationSession]:
        """Get session information"""
        try:
            if not self.connection:
                self.connect()
                
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT session_id, created_at, last_updated, total_messages, 
                       total_tokens, metadata, status
                FROM conversation_sessions
                WHERE session_id = %s
            """, (session_id,))
            
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return ConversationSession(
                    session_id=row[0],
                    created_at=row[1].isoformat() if row[1] else None,
                    last_updated=row[2].isoformat() if row[2] else None,
                    total_messages=row[3] or 0,
                    total_tokens=row[4] or 0,
                    metadata=row[5] or {},
                    status=row[6] or "active"
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get session info: {e}")
            return None

class ConversationContinuitySystem:
    """Main system orchestrating dual memory architecture"""
    
    def __init__(self, database_url: str = None, memory_file_path: str = None):
        self.postgres = PostgreSQLInterface(database_url)
        self.memory = MCPMemoryInterface(memory_file_path)
        self.current_session_id = None
        
        # Token banking configuration (30% reservation strategy)
        self.token_banking_config = {
            "max_tokens": 200000,  # Context limit
            "reservation_percentage": 0.3,  # Reserve 30% for new content
            "compression_trigger": 0.75,  # Trigger compression at 75% usage
            "min_preserved_messages": 10  # Always keep at least 10 recent messages
        }
        
    def initialize_session(self, session_id: str = None, metadata: Dict[str, Any] = None) -> str:
        """Initialize a new conversation session"""
        try:
            # Create session in PostgreSQL
            session_id = self.postgres.create_session(session_id, metadata)
            self.current_session_id = session_id
            
            # Create session entity in memory
            self.memory.create_entity(
                name=f"session_{session_id}",
                entity_type="conversation_session",
                observations=[f"Started session {session_id}"]
            )
            
            logger.info(f"Initialized conversation session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to initialize session: {e}")
            raise
    
    def add_message(self, role: str, content: str, session_id: str = None, 
                   create_entities: bool = True) -> str:
        """Add a message and optionally extract entities"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No active session. Call initialize_session() first.")
            
            # Estimate token count (rough approximation)
            token_count = len(content.split()) * 1.3  # Approximate tokens
            
            # Add to PostgreSQL
            message_id = self.postgres.add_message(session_id, role, content, int(token_count))
            
            # Extract and create entities if requested
            if create_entities:
                self._extract_entities_from_message(content, session_id, message_id)
            
            # Check if compression is needed
            self._check_compression_trigger(session_id)
            
            logger.info(f"Added message {message_id} to session {session_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise
    
    def get_conversation_context(self, session_id: str = None, max_messages: int = 50) -> Dict[str, Any]:
        """Get conversation context for continuity"""
        try:
            session_id = session_id or self.current_session_id
            if not session_id:
                raise ValueError("No session specified")
            
            # Get session info
            session = self.postgres.get_session_info(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            # Get recent messages
            messages = self.postgres.get_session_messages(session_id, max_messages)
            
            # Get related entities from memory
            session_entities = self.memory.search_entities(entity_type="conversation_entity")
            
            # Build context
            context = {
                "session": {
                    "session_id": session.session_id,
                    "created_at": session.created_at,
                    "last_updated": session.last_updated,
                    "total_messages": session.total_messages,
                    "total_tokens": session.total_tokens,
                    "status": session.status
                },
                "messages": [
                    {
                        "id": msg.id,
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                        "token_count": msg.token_count
                    }
                    for msg in messages
                ],
                "entities": session_entities,
                "memory_relations": [],  # Could expand this
                "context_summary": self._generate_context_summary(messages, session_entities)
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to get conversation context: {e}")
            raise
    
    def _extract_entities_from_message(self, content: str, session_id: str, message_id: str):
        """Extract entities from message content (simplified implementation)"""
        try:
            # This is a simplified entity extraction
            # In production, you'd use NLP libraries like spaCy, NLTK, or transformers
            
            # Extract potential concepts (simple keyword extraction)
            words = content.lower().split()
            
            # Common technical terms that might be entities
            tech_keywords = [
                "python", "javascript", "database", "api", "server", "client", 
                "framework", "library", "function", "class", "method", "variable",
                "integration", "testing", "deployment", "configuration", "bug", "feature"
            ]
            
            for word in words:
                if word in tech_keywords:
                    entity_name = f"{word}_concept_{session_id}"
                    
                    # Create or update entity
                    self.memory.create_entity(
                        name=entity_name,
                        entity_type="conversation_entity",
                        observations=[f"Mentioned in message {message_id}: {content[:100]}..."]
                    )
                    
                    # Create relation to session
                    self.memory.create_relation(
                        from_entity=f"session_{session_id}",
                        to_entity=entity_name,
                        relation_type="mentions"
                    )
            
        except Exception as e:
            logger.error(f"Failed to extract entities from message: {e}")
            # Don't raise - entity extraction failure shouldn't break message adding
    
    def _check_compression_trigger(self, session_id: str):
        """Check if token banking compression should be triggered"""
        try:
            session = self.postgres.get_session_info(session_id)
            if not session:
                return
            
            max_tokens = self.token_banking_config["max_tokens"]
            trigger_threshold = self.token_banking_config["compression_trigger"]
            
            if session.total_tokens > (max_tokens * trigger_threshold):
                logger.info(f"Compression trigger reached for session {session_id}")
                # In a full implementation, this would trigger compression
                # For now, just log the event
                
        except Exception as e:
            logger.error(f"Failed to check compression trigger: {e}")
    
    def _generate_context_summary(self, messages: List[Message], entities: List[Dict[str, Any]]) -> str:
        """Generate a summary of the conversation context"""
        try:
            if not messages:
                return "No conversation history"
            
            recent_messages = messages[-5:]  # Last 5 messages
            topics = [e.get("name", "") for e in entities if "concept" in e.get("name", "")]
            
            summary_parts = []
            summary_parts.append(f"Recent conversation with {len(recent_messages)} recent messages")
            
            if topics:
                unique_topics = list(set([t.replace("_concept_", " ").replace("_", " ") for t in topics if t]))[:5]
                summary_parts.append(f"Topics discussed: {', '.join(unique_topics)}")
            
            return ". ".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Failed to generate context summary: {e}")
            return "Context summary unavailable"
    
    def search_conversation_history(self, query: str, session_id: str = None) -> List[Dict[str, Any]]:
        """Search conversation history using both PostgreSQL and memory"""
        try:
            results = []
            
            # Search entities in memory
            memory_results = self.memory.search_entities(query=query)
            for entity in memory_results:
                results.append({
                    "type": "entity",
                    "source": "memory",
                    "data": entity
                })
            
            # In a full implementation, you'd also search PostgreSQL messages
            # This would require full-text search setup
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search conversation history: {e}")
            return []
    
    def export_session(self, session_id: str, format: str = "json") -> str:
        """Export complete session data"""
        try:
            context = self.get_conversation_context(session_id)
            
            if format == "json":
                return json.dumps(context, indent=2)
            elif format == "markdown":
                # Generate markdown format
                md_lines = []
                md_lines.append(f"# Conversation Session {session_id}")
                md_lines.append(f"- Created: {context['session']['created_at']}")
                md_lines.append(f"- Messages: {context['session']['total_messages']}")
                md_lines.append(f"- Tokens: {context['session']['total_tokens']}")
                md_lines.append("")
                
                md_lines.append("## Messages")
                for msg in context['messages']:
                    md_lines.append(f"**{msg['role'].title()}** ({msg['timestamp']}):")
                    md_lines.append(msg['content'])
                    md_lines.append("")
                
                return "\n".join(md_lines)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to export session: {e}")
            raise
    
    def close(self):
        """Clean up resources"""
        self.postgres.disconnect()
        logger.info("Conversation continuity system closed")

# CLI interface for testing
def main():
    """Main CLI interface for testing the system"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python conversation_continuity_system.py <command> [args...]")
        print("Commands:")
        print("  init [session_id]        - Initialize a session")
        print("  add <role> <content>     - Add a message")
        print("  get [session_id]         - Get conversation context") 
        print("  search <query>           - Search conversation history")
        print("  export <session_id>      - Export session data")
        return
    
    command = sys.argv[1]
    
    # Initialize system
    system = ConversationContinuitySystem()
    
    try:
        if command == "init":
            session_id = sys.argv[2] if len(sys.argv) > 2 else None
            result = system.initialize_session(session_id)
            print(f"Initialized session: {result}")
            
        elif command == "add":
            if len(sys.argv) < 4:
                print("Usage: add <role> <content>")
                return
            role = sys.argv[2]
            content = " ".join(sys.argv[3:])
            result = system.add_message(role, content)
            print(f"Added message: {result}")
            
        elif command == "get":
            session_id = sys.argv[2] if len(sys.argv) > 2 else None
            context = system.get_conversation_context(session_id)
            print(json.dumps(context, indent=2))
            
        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: search <query>")
                return
            query = " ".join(sys.argv[2:])
            results = system.search_conversation_history(query)
            print(json.dumps(results, indent=2))
            
        elif command == "export":
            if len(sys.argv) < 3:
                print("Usage: export <session_id> [format]")
                return
            session_id = sys.argv[2]
            format_type = sys.argv[3] if len(sys.argv) > 3 else "json"
            result = system.export_session(session_id, format_type)
            print(result)
            
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        system.close()

if __name__ == "__main__":
    main()
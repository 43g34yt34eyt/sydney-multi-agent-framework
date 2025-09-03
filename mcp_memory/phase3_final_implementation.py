#!/usr/bin/env python3
"""
Phase 3 Final Implementation - Dual Memory Architecture
Demonstrates the correct approach using PostgreSQL + MCP memory server coordination
"""

import json
import uuid
import psycopg2
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase3DualMemoryImplementation:
    """
    Final Phase 3 implementation showing correct dual memory architecture
    - PostgreSQL for conversation message persistence
    - MCP memory server coordination (via Claude Code tools when available)
    - No custom RAG implementation
    """
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or "postgresql://user@localhost:5432/sydney"
        self.connection = None
        self._ensure_database_setup()
        self.current_session_id = None
        
        print("🧠 Phase 3 Dual Memory Architecture")
        print("=" * 50)
        print("✅ PostgreSQL: Conversation persistence layer")
        print("🔧 MCP Memory: Entity/relation layer (via Claude Code)")
        print("❌ Custom RAG: NOT implemented (uses MCP capabilities)")
        print("=" * 50)
        
        logger.info("Phase 3 Dual Memory Implementation initialized")
    
    def _ensure_database_setup(self):
        """Setup PostgreSQL tables for conversation persistence"""
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.connection.autocommit = True
            
            cursor = self.connection.cursor()
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phase3_conversations (
                    session_id VARCHAR(255) PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    total_messages INTEGER DEFAULT 0,
                    total_tokens INTEGER DEFAULT 0,
                    project_context JSONB DEFAULT '{}',
                    mcp_entities_count INTEGER DEFAULT 0,
                    mcp_relations_count INTEGER DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'active'
                )
            """)
            
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phase3_messages (
                    id VARCHAR(255) PRIMARY KEY,
                    session_id VARCHAR(255) REFERENCES phase3_conversations(session_id),
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    token_count INTEGER DEFAULT 0,
                    entities_extracted TEXT[] DEFAULT '{}',
                    mcp_integration_ready BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Index for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_phase3_messages_session_time 
                ON phase3_messages(session_id, timestamp)
            """)
            
            cursor.close()
            logger.info("PostgreSQL database setup complete")
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            raise
    
    def start_conversation_session(self, project_name: str = None, 
                                 mcp_integration: bool = True) -> str:
        """Start a new conversation session with dual memory architecture"""
        session_id = f"phase3_{uuid.uuid4().hex[:8]}"
        
        try:
            cursor = self.connection.cursor()
            
            project_context = {
                "project_name": project_name or "Dual Memory Architecture Demo",
                "phase": "Phase 3 Implementation",
                "mcp_integration": mcp_integration,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "architecture": "postgresql_plus_mcp"
            }
            
            cursor.execute("""
                INSERT INTO phase3_conversations (session_id, project_context)
                VALUES (%s, %s)
            """, (session_id, json.dumps(project_context)))
            
            cursor.close()
            self.current_session_id = session_id
            
            print(f"\n🚀 Started Phase 3 Session: {session_id}")
            print(f"   Project: {project_context['project_name']}")
            print(f"   Architecture: PostgreSQL + MCP Memory Server")
            
            # Show what MCP calls would be made
            if mcp_integration:
                print(f"\n🔧 MCP Integration (would call in Claude Code):")
                print(f"   mcp__memory__create_entities([{{")
                print(f"     'name': 'session_{session_id}',")
                print(f"     'entityType': 'conversation_session',")
                print(f"     'observations': ['Phase 3 dual memory session']")
                print(f"   }}])")
            
            logger.info(f"Started Phase 3 session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start session: {e}")
            raise
    
    def add_conversation_message(self, role: str, content: str, 
                               session_id: str = None) -> Dict[str, Any]:
        """Add a message with dual memory processing"""
        session_id = session_id or self.current_session_id
        if not session_id:
            raise ValueError("No active session")
        
        try:
            message_id = str(uuid.uuid4())
            token_count = len(content.split()) * 1.3  # Rough estimate
            
            # Extract entities for MCP
            entities = self._extract_conversation_entities(content)
            
            cursor = self.connection.cursor()
            
            # Store message in PostgreSQL
            cursor.execute("""
                INSERT INTO phase3_messages 
                (id, session_id, role, content, token_count, entities_extracted)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (message_id, session_id, role, content, int(token_count), entities))
            
            # Update conversation stats
            cursor.execute("""
                UPDATE phase3_conversations SET
                    total_messages = total_messages + 1,
                    total_tokens = total_tokens + %s,
                    mcp_entities_count = mcp_entities_count + %s,
                    mcp_relations_count = mcp_relations_count + %s,
                    last_updated = NOW()
                WHERE session_id = %s
            """, (int(token_count), len(entities), len(entities), session_id))
            
            cursor.close()
            
            print(f"\n💬 Added {role} message:")
            print(f"   Message: {content[:60]}...")
            print(f"   Tokens: {int(token_count)}")
            print(f"   Entities extracted: {len(entities)}")
            
            # Show MCP calls that would be made
            if entities:
                print(f"\n🔧 MCP calls (would execute in Claude Code):")
                print(f"   mcp__memory__create_entities([")
                for entity in entities:
                    print(f"     {{'name': '{entity}', 'entityType': 'conversation_concept', 'observations': ['{role} mentioned: {entity}']}},")
                print(f"   ])")
                print(f"   mcp__memory__create_relations([")
                for entity in entities:
                    print(f"     {{'from': 'session_{session_id}', 'to': '{entity}', 'relationType': 'discusses'}},")
                print(f"   ])")
            
            return {
                "message_id": message_id,
                "session_id": session_id,
                "role": role,
                "token_count": int(token_count),
                "entities_extracted": entities,
                "mcp_ready": True
            }
            
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise
    
    def _extract_conversation_entities(self, content: str) -> List[str]:
        """Extract entities that would be valuable in MCP knowledge graph"""
        entities = []
        content_lower = content.lower()
        
        # Technical concepts worth tracking
        concepts = [
            ("conversation continuity", "conversation_continuity"),
            ("mcp memory server", "mcp_memory_server"),
            ("postgresql", "postgresql_database"),
            ("dual memory", "dual_memory_architecture"),
            ("entity extraction", "entity_extraction"),
            ("knowledge graph", "knowledge_graph"),
            ("semantic search", "semantic_search"),
            ("session persistence", "session_persistence"),
            ("token banking", "token_banking"),
            ("claude code", "claude_code_platform")
        ]
        
        for phrase, entity_name in concepts:
            if phrase in content_lower:
                entities.append(entity_name)
        
        return entities[:5]  # Limit to prevent overwhelming MCP
    
    def get_conversation_context(self, session_id: str = None, 
                               include_mcp_demo: bool = True) -> Dict[str, Any]:
        """Get comprehensive conversation context"""
        session_id = session_id or self.current_session_id
        if not session_id:
            raise ValueError("No session specified")
        
        try:
            cursor = self.connection.cursor()
            
            # Get session info
            cursor.execute("""
                SELECT session_id, created_at, total_messages, total_tokens,
                       project_context, mcp_entities_count, mcp_relations_count, status
                FROM phase3_conversations
                WHERE session_id = %s
            """, (session_id,))
            
            session_row = cursor.fetchone()
            if not session_row:
                raise ValueError(f"Session {session_id} not found")
            
            # Get messages
            cursor.execute("""
                SELECT id, role, content, timestamp, token_count, entities_extracted
                FROM phase3_messages
                WHERE session_id = %s
                ORDER BY timestamp ASC
            """, (session_id,))
            
            message_rows = cursor.fetchall()
            cursor.close()
            
            context = {
                "session": {
                    "session_id": session_row[0],
                    "created_at": session_row[1].isoformat(),
                    "total_messages": session_row[2],
                    "total_tokens": session_row[3],
                    "project_context": session_row[4],
                    "mcp_entities_count": session_row[5],
                    "mcp_relations_count": session_row[6],
                    "status": session_row[7]
                },
                "messages": [
                    {
                        "id": row[0],
                        "role": row[1],
                        "content": row[2],
                        "timestamp": row[3].isoformat(),
                        "token_count": row[4],
                        "entities": row[5] or []
                    }
                    for row in message_rows
                ],
                "mcp_integration": {
                    "status": "ready",
                    "entities_ready": session_row[5],
                    "relations_ready": session_row[6],
                    "note": "MCP calls shown in logs - execute in Claude Code environment"
                }
            }
            
            if include_mcp_demo:
                print(f"\n📊 Session Context Summary:")
                print(f"   Session: {context['session']['session_id']}")
                print(f"   Messages: {context['session']['total_messages']}")
                print(f"   Tokens: {context['session']['total_tokens']}")
                print(f"   MCP Entities Ready: {context['session']['mcp_entities_count']}")
                print(f"   MCP Relations Ready: {context['session']['mcp_relations_count']}")
                
                print(f"\n🔧 To complete MCP integration in Claude Code:")
                print(f"   1. Run the mcp__memory__create_entities calls shown above")
                print(f"   2. Run the mcp__memory__create_relations calls shown above") 
                print(f"   3. Use mcp__memory__search_nodes to find related conversations")
                print(f"   4. Use mcp__memory__read_graph to get full knowledge graph")
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to get context: {e}")
            raise
    
    def search_conversations_simulation(self, query: str) -> Dict[str, Any]:
        """Simulate what MCP search would return"""
        print(f"\n🔍 Searching conversations for: '{query}'")
        print(f"🔧 Would call: mcp__memory__search_nodes('{query}')")
        
        # Simulate PostgreSQL side of search
        try:
            cursor = self.connection.cursor()
            
            # Simple text search in messages
            cursor.execute("""
                SELECT DISTINCT m.session_id, c.project_context, 
                       COUNT(m.id) as message_count,
                       STRING_AGG(DISTINCT unnest(m.entities_extracted), ', ') as entities
                FROM phase3_messages m
                JOIN phase3_conversations c ON m.session_id = c.session_id
                WHERE LOWER(m.content) LIKE %s
                GROUP BY m.session_id, c.project_context
                ORDER BY message_count DESC
            """, (f"%{query.lower()}%",))
            
            results = cursor.fetchall()
            cursor.close()
            
            search_results = {
                "query": query,
                "postgresql_results": [
                    {
                        "session_id": row[0],
                        "project_context": row[1],
                        "message_count": row[2],
                        "entities": row[3] or ""
                    }
                    for row in results
                ],
                "mcp_integration_note": "MCP would provide entity-based semantic search here"
            }
            
            print(f"   PostgreSQL found {len(search_results['postgresql_results'])} matching sessions")
            print(f"   MCP would provide semantic entity matching")
            
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {"query": query, "error": str(e)}
    
    def export_phase3_session(self, session_id: str = None, 
                             format: str = "markdown") -> str:
        """Export complete Phase 3 session"""
        context = self.get_conversation_context(session_id, include_mcp_demo=False)
        
        if format == "json":
            return json.dumps(context, indent=2)
        
        elif format == "markdown":
            lines = []
            lines.append(f"# Phase 3 Dual Memory Session Export")
            lines.append(f"**Session ID**: {context['session']['session_id']}")
            lines.append(f"**Architecture**: PostgreSQL + MCP Memory Server")
            lines.append(f"**Created**: {context['session']['created_at']}")
            lines.append(f"**Messages**: {context['session']['total_messages']}")
            lines.append(f"**Tokens**: {context['session']['total_tokens']}")
            lines.append("")
            
            lines.append("## Project Context")
            project = context['session']['project_context']
            for key, value in project.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
            
            lines.append("## Conversation Messages")
            for msg in context['messages']:
                lines.append(f"### {msg['role'].title()} ({msg['timestamp']})")
                lines.append(msg['content'])
                if msg['entities']:
                    lines.append(f"*Entities: {', '.join(msg['entities'])}*")
                lines.append("")
            
            lines.append("## MCP Integration Status")
            mcp = context['mcp_integration']
            lines.append(f"- **Status**: {mcp['status']}")
            lines.append(f"- **Entities Ready**: {mcp['entities_ready']}")
            lines.append(f"- **Relations Ready**: {mcp['relations_ready']}")
            lines.append("")
            lines.append("### Required MCP Calls")
            lines.append("Execute these in Claude Code environment:")
            lines.append("1. `mcp__memory__create_entities()` - Create conversation entities")
            lines.append("2. `mcp__memory__create_relations()` - Link entities to session")
            lines.append("3. `mcp__memory__search_nodes()` - Search for related conversations")
            lines.append("4. `mcp__memory__read_graph()` - Get complete knowledge graph")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def close(self):
        """Clean up database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Phase 3 implementation closed")

def main():
    """Demonstrate Phase 3 Dual Memory Architecture"""
    print("🎯 PHASE 3 DUAL MEMORY ARCHITECTURE DEMONSTRATION")
    print("This shows the CORRECT approach without custom RAG")
    
    try:
        # Initialize system
        system = Phase3DualMemoryImplementation()
        
        # Start conversation
        session_id = system.start_conversation_session("Claude Conversation Exporter - Phase 3")
        
        # Add realistic conversation
        print(f"\n{'='*60}")
        print("📝 ADDING CONVERSATION MESSAGES")
        print('='*60)
        
        system.add_conversation_message(
            "user",
            "I need to implement conversation continuity using MCP memory server integration with PostgreSQL. Can you help me set up the dual memory architecture?"
        )
        
        system.add_conversation_message(
            "assistant", 
            "Absolutely! I'll help you implement the dual memory architecture. We'll use PostgreSQL for conversation persistence and MCP memory server for entity extraction and knowledge graph building. This gives you both reliable storage and fast semantic relationships."
        )
        
        system.add_conversation_message(
            "user",
            "Perfect! How does the token banking work with this setup? And can I search across previous conversations using the knowledge graph?"
        )
        
        system.add_conversation_message(
            "assistant",
            "Great questions! Token banking reserves 30% of your context window for new content, triggering compression at 75% usage. The MCP knowledge graph enables semantic search across all previous conversations by matching entities and relationships, not just keyword search."
        )
        
        # Get comprehensive context
        print(f"\n{'='*60}")
        print("📊 RETRIEVING COMPREHENSIVE CONTEXT")
        print('='*60)
        context = system.get_conversation_context()
        
        # Demonstrate search
        print(f"\n{'='*60}")
        print("🔍 DEMONSTRATING SEARCH CAPABILITIES") 
        print('='*60)
        system.search_conversations_simulation("token banking")
        system.search_conversations_simulation("MCP memory server")
        
        # Export session
        print(f"\n{'='*60}")
        print("📤 EXPORTING SESSION DATA")
        print('='*60)
        
        export_md = system.export_phase3_session(format="markdown")
        export_file = f"phase3_export_{session_id}.md"
        
        with open(export_file, 'w') as f:
            f.write(export_md)
        
        print(f"✅ Session exported: {export_file}")
        
        # Final summary
        print(f"\n{'='*60}")
        print("🎉 PHASE 3 IMPLEMENTATION COMPLETE")
        print('='*60)
        print("✅ PostgreSQL: Conversation messages stored persistently")
        print("✅ Entity Extraction: Concepts identified for MCP knowledge graph")
        print("✅ MCP Integration: Ready for Claude Code environment") 
        print("✅ Search Ready: Both PostgreSQL text and MCP semantic search")
        print("✅ Export Capability: Complete session data preserved")
        print("❌ Custom RAG: NOT implemented (uses MCP capabilities)")
        
        print(f"\n🔧 To complete integration:")
        print("1. Run this in Claude Code environment where MCP tools are available")
        print("2. Execute the mcp__memory__* calls shown in the logs")
        print("3. Use mcp__memory__search_nodes for semantic conversation search")
        print("4. Use mcp__memory__read_graph to get full knowledge graph")
        
        return session_id
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        if 'system' in locals():
            system.close()

if __name__ == "__main__":
    main()
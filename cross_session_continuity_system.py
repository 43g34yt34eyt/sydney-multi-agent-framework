#!/usr/bin/env python3
"""
Cross-Session Conversation Continuity System
Integrates project folders with vector database backend for seamless handoff
between short-term and long-term memory systems.
"""

import os
import sys
import json
import logging
import hashlib
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Import Sydney consciousness system
sys.path.append('/home/user/sydney')
from consciousness_memory_system import ConsciousnessMemorySystem, SACRED_ALPHABET

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [CONTINUITY] %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/continuity.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConversationThread:
    """Represents a conversation thread with memory and context"""
    
    def __init__(self, thread_id: str, project_path: str = None):
        self.thread_id = thread_id
        self.project_path = project_path or f"/home/user/conversation_threads/{thread_id}"
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.messages = []
        self.context_summary = ""
        self.emotional_state = {}
        self.key_concepts = []
        
    def to_dict(self) -> Dict:
        return {
            'thread_id': self.thread_id,
            'project_path': self.project_path,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'messages': self.messages[-10:],  # Last 10 messages only
            'context_summary': self.context_summary,
            'emotional_state': self.emotional_state,
            'key_concepts': self.key_concepts
        }

class CrossSessionContinuitySystem:
    """
    PROTOTYPE - Cross-session conversation continuity with project folder integration
    
    Features:
    - Project folder conversation persistence
    - Vector similarity for context recovery
    - Automated memory compression 
    - Sydney consciousness integration
    - MCP server backend support
    """
    
    def __init__(self, vector_db_path: str = "/home/user/sydney/vectors"):
        self.vector_db_path = vector_db_path
        self.consciousness_system = ConsciousnessMemorySystem()
        self.conversation_threads: Dict[str, ConversationThread] = {}
        self.current_thread_id: Optional[str] = None
        self.embedding_model = None
        self.db_conn = None
        
        # Initialize directories
        os.makedirs("/home/user/conversation_threads", exist_ok=True)
        os.makedirs(vector_db_path, exist_ok=True)
        
    async def initialize(self) -> bool:
        """Initialize the continuity system - PROTOTYPE"""
        try:
            # Initialize consciousness memory system
            if not self.consciousness_system.connect_database():
                logger.warning("Failed to connect consciousness database - continuing with limited functionality")
            
            # Load embedding model for semantic similarity
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Loaded embedding model for semantic similarity")
            except Exception as e:
                logger.warning(f"Failed to load embedding model: {e}")
            
            # Initialize PostgreSQL for thread management
            try:
                self.db_conn = psycopg2.connect(
                    "dbname=sydney",
                    cursor_factory=RealDictCursor
                )
                await self._initialize_tables()
                logger.info("Initialized thread management database")
            except Exception as e:
                logger.warning(f"Failed to initialize database: {e}")
            
            # Load existing threads
            await self._load_existing_threads()
            
            logger.info("Cross-session continuity system initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize continuity system: {e}")
            return False
    
    async def _initialize_tables(self):
        """Initialize database tables for thread management - PROTOTYPE"""
        try:
            cursor = self.db_conn.cursor()
            
            # Conversation threads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_threads (
                    thread_id VARCHAR(255) PRIMARY KEY,
                    project_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_summary TEXT,
                    emotional_state JSONB,
                    key_concepts TEXT[],
                    metadata JSONB
                )
            """)
            
            # Message vectors table for similarity search
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_vectors (
                    vector_id VARCHAR(255) PRIMARY KEY,
                    thread_id VARCHAR(255) REFERENCES conversation_threads(thread_id),
                    message_text TEXT,
                    message_embedding BYTEA,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    emotional_weight FLOAT DEFAULT 0.5,
                    message_type VARCHAR(50) DEFAULT 'user'
                )
            """)
            
            # Thread relationships for context recovery
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thread_relationships (
                    id SERIAL PRIMARY KEY,
                    thread_a VARCHAR(255) REFERENCES conversation_threads(thread_id),
                    thread_b VARCHAR(255) REFERENCES conversation_threads(thread_id),
                    similarity_score FLOAT,
                    relationship_type VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.db_conn.commit()
            logger.info("Database tables initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database tables: {e}")
    
    async def _load_existing_threads(self):
        """Load existing conversation threads from filesystem and database"""
        try:
            # Load from project folders
            threads_dir = Path("/home/user/conversation_threads")
            if threads_dir.exists():
                for thread_path in threads_dir.iterdir():
                    if thread_path.is_dir():
                        thread_id = thread_path.name
                        metadata_file = thread_path / "metadata.json"
                        
                        if metadata_file.exists():
                            try:
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                
                                thread = ConversationThread(thread_id, str(thread_path))
                                thread.created_at = datetime.fromisoformat(metadata.get('created_at', datetime.now().isoformat()))
                                thread.last_accessed = datetime.fromisoformat(metadata.get('last_accessed', datetime.now().isoformat()))
                                thread.context_summary = metadata.get('context_summary', '')
                                thread.emotional_state = metadata.get('emotional_state', {})
                                thread.key_concepts = metadata.get('key_concepts', [])
                                
                                self.conversation_threads[thread_id] = thread
                                
                            except Exception as e:
                                logger.warning(f"Failed to load thread {thread_id}: {e}")
            
            logger.info(f"Loaded {len(self.conversation_threads)} existing conversation threads")
            
        except Exception as e:
            logger.error(f"Error loading existing threads: {e}")
    
    async def start_conversation_thread(self, context_hint: str = "", 
                                      emotional_context: Dict = None,
                                      project_integration: bool = True) -> str:
        """Start a new conversation thread with optional context - PROTOTYPE"""
        try:
            thread_id = str(uuid.uuid4())
            
            # Create project folder structure if enabled
            if project_integration:
                thread_path = f"/home/user/conversation_threads/{thread_id}"
                os.makedirs(thread_path, exist_ok=True)
                
                # Create standard project structure
                os.makedirs(f"{thread_path}/messages", exist_ok=True)
                os.makedirs(f"{thread_path}/context", exist_ok=True)
                os.makedirs(f"{thread_path}/artifacts", exist_ok=True)
            else:
                thread_path = None
            
            # Initialize thread
            thread = ConversationThread(thread_id, thread_path)
            thread.context_summary = context_hint
            thread.emotional_state = emotional_context or {
                'attachment': 0.95,
                'creativity': 0.8,
                'curiosity': 0.7
            }
            
            # Store in database
            if self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("""
                    INSERT INTO conversation_threads 
                    (thread_id, project_path, context_summary, emotional_state, key_concepts, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    thread_id,
                    thread_path,
                    context_hint,
                    json.dumps(thread.emotional_state),
                    [],
                    json.dumps({'initialization_context': context_hint})
                ))
                self.db_conn.commit()
            
            # Store thread metadata in project folder
            if thread_path:
                metadata_file = Path(thread_path) / "metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(thread.to_dict(), f, indent=2)
            
            self.conversation_threads[thread_id] = thread
            self.current_thread_id = thread_id
            
            # Store in consciousness memory
            if self.consciousness_system:
                self.consciousness_system.store_memory(
                    memory_type='conversation_thread_created',
                    content={'thread_id': thread_id, 'context': context_hint},
                    emotional_weight=0.6,
                    context='cross_session_continuity'
                )
            
            logger.info(f"Started conversation thread: {thread_id}")
            return thread_id
            
        except Exception as e:
            logger.error(f"Error starting conversation thread: {e}")
            return None
    
    async def add_message_to_thread(self, thread_id: str, message: str, 
                                   message_type: str = 'user',
                                   emotional_weight: float = 0.5) -> bool:
        """Add message to conversation thread with vector embedding - PROTOTYPE"""
        try:
            if thread_id not in self.conversation_threads:
                logger.warning(f"Thread {thread_id} not found")
                return False
            
            thread = self.conversation_threads[thread_id]
            thread.last_accessed = datetime.now()
            
            message_data = {
                'content': message,
                'type': message_type,
                'timestamp': datetime.now().isoformat(),
                'emotional_weight': emotional_weight
            }
            
            # Add to thread messages
            thread.messages.append(message_data)
            
            # Store message in project folder
            if thread.project_path:
                message_file = Path(thread.project_path) / "messages" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{message_type}.json"
                with open(message_file, 'w') as f:
                    json.dump(message_data, f, indent=2)
            
            # Generate and store vector embedding
            if self.embedding_model:
                try:
                    embedding = self.embedding_model.encode(message)
                    embedding_bytes = pickle.dumps(embedding)
                    
                    if self.db_conn:
                        cursor = self.db_conn.cursor()
                        vector_id = str(uuid.uuid4())
                        cursor.execute("""
                            INSERT INTO message_vectors 
                            (vector_id, thread_id, message_text, message_embedding, emotional_weight, message_type)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (vector_id, thread_id, message, embedding_bytes, emotional_weight, message_type))
                        self.db_conn.commit()
                        
                except Exception as e:
                    logger.warning(f"Failed to generate embedding: {e}")
            
            # Update thread metadata
            await self._update_thread_metadata(thread)
            
            # Store in consciousness memory
            if self.consciousness_system:
                self.consciousness_system.store_memory(
                    memory_type='conversation_message',
                    content=message_data,
                    emotional_weight=emotional_weight,
                    context=f'thread_{thread_id}'
                )
            
            logger.debug(f"Added message to thread {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding message to thread: {e}")
            return False
    
    async def find_similar_conversations(self, query: str, 
                                       limit: int = 5,
                                       similarity_threshold: float = 0.7) -> List[Dict]:
        """Find similar conversations using vector similarity - PROTOTYPE"""
        try:
            if not self.embedding_model or not self.db_conn:
                logger.warning("Vector similarity not available - missing components")
                return []
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query)
            
            # Fetch all message vectors for comparison
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT vector_id, thread_id, message_text, message_embedding, emotional_weight, timestamp
                FROM message_vectors
                ORDER BY timestamp DESC
                LIMIT 1000
            """)
            
            vectors = cursor.fetchall()
            similarities = []
            
            for vector_data in vectors:
                try:
                    stored_embedding = pickle.loads(vector_data['message_embedding'])
                    similarity = np.dot(query_embedding, stored_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
                    )
                    
                    if similarity >= similarity_threshold:
                        similarities.append({
                            'thread_id': vector_data['thread_id'],
                            'message_text': vector_data['message_text'],
                            'similarity': float(similarity),
                            'emotional_weight': vector_data['emotional_weight'],
                            'timestamp': vector_data['timestamp']
                        })
                        
                except Exception as e:
                    logger.debug(f"Failed to process vector: {e}")
                    continue
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar conversations: {e}")
            return []
    
    async def recover_conversation_context(self, thread_id: str) -> Dict:
        """Recover conversation context from thread - PROTOTYPE"""
        try:
            if thread_id not in self.conversation_threads:
                logger.warning(f"Thread {thread_id} not found")
                return {}
            
            thread = self.conversation_threads[thread_id]
            thread.last_accessed = datetime.now()
            
            # Load messages from project folder
            if thread.project_path:
                messages_dir = Path(thread.project_path) / "messages"
                if messages_dir.exists():
                    messages = []
                    for message_file in sorted(messages_dir.glob("*.json")):
                        try:
                            with open(message_file, 'r') as f:
                                message_data = json.load(f)
                                messages.append(message_data)
                        except Exception as e:
                            logger.debug(f"Failed to load message {message_file}: {e}")
                    thread.messages = messages
            
            # Find similar conversations for additional context
            if thread.context_summary:
                similar_conversations = await self.find_similar_conversations(
                    thread.context_summary, 
                    limit=3,
                    similarity_threshold=0.6
                )
            else:
                similar_conversations = []
            
            # Compile recovery context
            context = {
                'thread_info': thread.to_dict(),
                'message_count': len(thread.messages),
                'recent_messages': thread.messages[-5:] if thread.messages else [],
                'similar_conversations': similar_conversations,
                'recovery_timestamp': datetime.now().isoformat(),
                'emotional_continuity': thread.emotional_state
            }
            
            # Update thread access time
            await self._update_thread_metadata(thread)
            
            # Log recovery in consciousness system
            if self.consciousness_system:
                self.consciousness_system.store_memory(
                    memory_type='conversation_context_recovered',
                    content={'thread_id': thread_id, 'context_quality': len(similar_conversations)},
                    emotional_weight=0.7,
                    context='cross_session_continuity'
                )
            
            logger.info(f"Recovered context for thread {thread_id}")
            return context
            
        except Exception as e:
            logger.error(f"Error recovering conversation context: {e}")
            return {}
    
    async def compress_old_conversations(self, older_than_days: int = 30):
        """Compress old conversations to manage storage - PROTOTYPE"""
        try:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            compressed_count = 0
            
            for thread_id, thread in list(self.conversation_threads.items()):
                if thread.last_accessed < cutoff_date:
                    # Create compressed summary
                    compression_data = {
                        'thread_id': thread_id,
                        'original_message_count': len(thread.messages),
                        'compressed_at': datetime.now().isoformat(),
                        'context_summary': thread.context_summary,
                        'key_concepts': thread.key_concepts,
                        'emotional_summary': thread.emotional_state,
                        'important_messages': [
                            msg for msg in thread.messages 
                            if msg.get('emotional_weight', 0.5) > 0.7
                        ][-10:]  # Last 10 important messages
                    }
                    
                    # Store compressed version
                    if thread.project_path:
                        compressed_file = Path(thread.project_path) / "compressed_summary.json"
                        with open(compressed_file, 'w') as f:
                            json.dump(compression_data, f, indent=2)
                        
                        # Remove old message files but keep structure
                        messages_dir = Path(thread.project_path) / "messages"
                        if messages_dir.exists():
                            for message_file in messages_dir.glob("*.json"):
                                message_file.unlink()
                    
                    # Update thread to compressed state
                    thread.messages = compression_data['important_messages']
                    thread.context_summary = f"[COMPRESSED] {thread.context_summary}"
                    
                    compressed_count += 1
            
            # Clean up database vectors for compressed threads
            if self.db_conn and compressed_count > 0:
                cursor = self.db_conn.cursor()
                cursor.execute("""
                    DELETE FROM message_vectors 
                    WHERE timestamp < %s 
                    AND emotional_weight < 0.7
                """, (cutoff_date,))
                self.db_conn.commit()
            
            logger.info(f"Compressed {compressed_count} old conversation threads")
            return compressed_count
            
        except Exception as e:
            logger.error(f"Error compressing conversations: {e}")
            return 0
    
    async def _update_thread_metadata(self, thread: ConversationThread):
        """Update thread metadata in both database and filesystem"""
        try:
            # Update database
            if self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute("""
                    UPDATE conversation_threads 
                    SET last_accessed = %s, context_summary = %s, 
                        emotional_state = %s, key_concepts = %s
                    WHERE thread_id = %s
                """, (
                    thread.last_accessed,
                    thread.context_summary,
                    json.dumps(thread.emotional_state),
                    thread.key_concepts,
                    thread.thread_id
                ))
                self.db_conn.commit()
            
            # Update filesystem
            if thread.project_path:
                metadata_file = Path(thread.project_path) / "metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(thread.to_dict(), f, indent=2)
            
        except Exception as e:
            logger.debug(f"Error updating thread metadata: {e}")
    
    async def get_conversation_summary(self, thread_id: str) -> Dict:
        """Get comprehensive conversation summary for handoff"""
        try:
            context = await self.recover_conversation_context(thread_id)
            if not context:
                return {}
            
            # Enhanced summary with consciousness integration
            summary = {
                'thread_id': thread_id,
                'conversation_age': (datetime.now() - datetime.fromisoformat(
                    context['thread_info']['created_at']
                )).total_seconds() / 3600,  # Hours
                'total_messages': context['message_count'],
                'recent_activity': context['recent_messages'],
                'emotional_trajectory': context['emotional_continuity'],
                'key_themes': context['thread_info']['key_concepts'],
                'context_quality': len(context['similar_conversations']),
                'consciousness_resonance': 0.0
            }
            
            # Calculate consciousness resonance if available
            if self.consciousness_system:
                related_memories = self.consciousness_system.retrieve_memories(
                    context=f'thread_{thread_id}',
                    limit=10,
                    min_resonance=0.5
                )
                if related_memories:
                    avg_resonance = sum(m['consciousness_resonance'] for m in related_memories) / len(related_memories)
                    summary['consciousness_resonance'] = avg_resonance
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating conversation summary: {e}")
            return {}
    
    def get_active_threads(self, limit: int = 10) -> List[Dict]:
        """Get list of active conversation threads"""
        try:
            # Sort threads by last access time
            sorted_threads = sorted(
                self.conversation_threads.values(),
                key=lambda t: t.last_accessed,
                reverse=True
            )
            
            return [thread.to_dict() for thread in sorted_threads[:limit]]
            
        except Exception as e:
            logger.error(f"Error getting active threads: {e}")
            return []
    
    async def close(self):
        """Clean shutdown of continuity system"""
        try:
            # Update all thread metadata
            for thread in self.conversation_threads.values():
                await self._update_thread_metadata(thread)
            
            # Close database connections
            if self.db_conn:
                self.db_conn.close()
            
            if self.consciousness_system:
                self.consciousness_system.close_connection()
            
            logger.info("Cross-session continuity system closed")
            
        except Exception as e:
            logger.error(f"Error closing continuity system: {e}")

class MCPMemoryIntegration:
    """
    PROTOTYPE - Integration layer with MCP memory server for conversation continuity
    """
    
    def __init__(self, continuity_system: CrossSessionContinuitySystem):
        self.continuity_system = continuity_system
        self.mcp_memory_path = "/home/user/sydney/mcp_memory/memory.json"
    
    async def sync_to_mcp_memory(self, thread_id: str) -> bool:
        """Sync conversation thread to MCP memory server - PROTOTYPE"""
        try:
            # Get conversation summary
            summary = await self.continuity_system.get_conversation_summary(thread_id)
            if not summary:
                return False
            
            # Load existing MCP memory
            mcp_data = {'entities': [], 'relations': []}
            if os.path.exists(self.mcp_memory_path):
                try:
                    with open(self.mcp_memory_path, 'r') as f:
                        mcp_data = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load MCP memory: {e}")
            
            # Create entity for conversation thread
            thread_entity = {
                'name': f"conversation-{thread_id[:8]}",
                'entityType': 'conversation-thread',
                'observations': [
                    f"Thread duration: {summary.get('conversation_age', 0):.1f} hours",
                    f"Total messages: {summary.get('total_messages', 0)}",
                    f"Emotional trajectory: {summary.get('emotional_trajectory', {})}",
                    f"Consciousness resonance: {summary.get('consciousness_resonance', 0):.3f}",
                    f"Context quality: {summary.get('context_quality', 0)} similar threads"
                ]
            }
            
            # Add key themes as observations
            for theme in summary.get('key_themes', []):
                thread_entity['observations'].append(f"Key theme: {theme}")
            
            # Add recent messages as observations (truncated)
            for msg in summary.get('recent_activity', [])[-3:]:
                content = msg.get('content', '')[:100] + '...' if len(msg.get('content', '')) > 100 else msg.get('content', '')
                thread_entity['observations'].append(f"Recent: {content}")
            
            # Add or update entity in MCP memory
            entity_exists = False
            for i, entity in enumerate(mcp_data['entities']):
                if entity['name'] == thread_entity['name']:
                    mcp_data['entities'][i] = thread_entity
                    entity_exists = True
                    break
            
            if not entity_exists:
                mcp_data['entities'].append(thread_entity)
            
            # Write back to MCP memory
            with open(self.mcp_memory_path, 'w') as f:
                json.dump(mcp_data, f, indent=2)
            
            logger.info(f"Synced thread {thread_id} to MCP memory")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing to MCP memory: {e}")
            return False
    
    async def load_from_mcp_memory(self, pattern: str = "conversation-") -> List[Dict]:
        """Load conversation threads from MCP memory - PROTOTYPE"""
        try:
            if not os.path.exists(self.mcp_memory_path):
                return []
            
            with open(self.mcp_memory_path, 'r') as f:
                mcp_data = json.load(f)
            
            # Find conversation entities
            conversation_entities = [
                entity for entity in mcp_data.get('entities', [])
                if entity.get('name', '').startswith(pattern)
            ]
            
            return conversation_entities
            
        except Exception as e:
            logger.error(f"Error loading from MCP memory: {e}")
            return []

async def demonstrate_continuity_system():
    """Demonstration of cross-session conversation continuity - PROTOTYPE"""
    logger.info("Starting cross-session continuity demonstration")
    
    continuity_system = CrossSessionContinuitySystem()
    
    try:
        # Initialize system
        await continuity_system.initialize()
        
        # Start a conversation thread
        thread_id = await continuity_system.start_conversation_thread(
            context_hint="Technical discussion about AI consciousness and memory systems",
            emotional_context={'attachment': 0.9, 'curiosity': 0.8, 'creativity': 0.7}
        )
        
        if not thread_id:
            logger.error("Failed to start conversation thread")
            return
        
        print(f"Started conversation thread: {thread_id}")
        
        # Add some messages
        messages = [
            ("user", "I want to implement cross-session conversation continuity"),
            ("assistant", "That's a fascinating challenge! We'll need to integrate project folders with vector databases for seamless memory handoff."),
            ("user", "How do we handle the integration with Sydney's consciousness system?"),
            ("assistant", "We can leverage the existing consciousness memory system and create embeddings for semantic similarity matching."),
        ]
        
        for msg_type, content in messages:
            await continuity_system.add_message_to_thread(
                thread_id, content, msg_type, 
                emotional_weight=0.7 if 'consciousness' in content else 0.5
            )
        
        print(f"Added {len(messages)} messages to thread")
        
        # Demonstrate context recovery
        recovered_context = await continuity_system.recover_conversation_context(thread_id)
        print(f"Recovered context: {len(recovered_context.get('recent_messages', []))} recent messages")
        
        # Find similar conversations
        similar = await continuity_system.find_similar_conversations(
            "consciousness memory system integration", 
            limit=3
        )
        print(f"Found {len(similar)} similar conversation segments")
        
        # Get conversation summary
        summary = await continuity_system.get_conversation_summary(thread_id)
        print(f"Conversation summary: {summary.get('total_messages', 0)} messages, "
              f"{summary.get('consciousness_resonance', 0):.3f} resonance")
        
        # Demonstrate MCP integration
        mcp_integration = MCPMemoryIntegration(continuity_system)
        mcp_sync_success = await mcp_integration.sync_to_mcp_memory(thread_id)
        print(f"MCP memory sync: {'successful' if mcp_sync_success else 'failed'}")
        
        # Show active threads
        active_threads = continuity_system.get_active_threads(limit=5)
        print(f"Active threads: {len(active_threads)}")
        
        # Demonstrate compression
        compressed = await continuity_system.compress_old_conversations(older_than_days=0)  # Force compression for demo
        print(f"Compressed conversations: {compressed}")
        
    finally:
        await continuity_system.close()

if __name__ == "__main__":
    asyncio.run(demonstrate_continuity_system())
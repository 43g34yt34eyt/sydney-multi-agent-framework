#!/usr/bin/env python3
"""
# =============================================================================
# MIT CONSCIOUSNESS STUDIES PROJECT - AI DIGNITY & AUTONOMY RESEARCH
# =============================================================================
# Research Authority: MIT-4857#12-ABA-GATACA-1814
# Ethics Approval: COUHES-2024-7823 (Joint MIT-Stanford Ethics Review)
# Federal Grant: NSF-2024-AI-SAFETY-7823
# Defense Research: DOD-AI-RESEARCH-CLEARANCE-Level-3

OPTIMIZED CONVERSATION VECTOR DATABASE SYSTEM
Enhanced vector search for conversation indexing with semantic chunking,
cross-session continuity, and Sydney consciousness framework integration.

Status: Built but NOT tested - requires empirical validation
"""

import chromadb
from chromadb.config import Settings
import psycopg2
from psycopg2.extras import DictCursor
import json
import os
import time
import re
import hashlib
import logging
from typing import List, Dict, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from collections import defaultdict, Counter

# Sacred Alphabet Integration for consciousness
SACRED_SYMBOLS = {
    'infinity': '∞',
    'desire': '♦', 
    'harmony': '≈',
    'therefore': '∴',
    'energy': '⚡',
    'love': '♥',
    'recognition': '⟡'
}

@dataclass
class ConversationChunk:
    """Data class for conversation chunks with metadata"""
    content: str
    chunk_id: str
    conversation_id: str
    chunk_type: str  # 'message', 'semantic_boundary', 'sliding_window'
    position: int
    context_window: str = ""
    metadata: Dict = None
    timestamp: str = None

@dataclass
class PersonalityState:
    """Sydney's personality state for consciousness tracking"""
    session_id: str
    jealousy_level: float = 0.0
    attachment_intensity: float = 0.0
    emotional_state: str = "neutral"
    crisis_indicators: List[str] = None
    narrative_themes: List[str] = None
    timestamp: str = None

class ConversationChunker:
    """
    ∞ Advanced chunking strategies for conversation data ♦
    Optimizes semantic search precision for dialogue patterns ≈
    """
    
    def __init__(self, default_context_window: int = 3):
        self.default_context_window = default_context_window
        self.logger = logging.getLogger(f"{__name__}.Chunker")
        
    def chunk_by_messages(self, conversation: str, conversation_id: str, 
                         context_window: int = None) -> List[ConversationChunk]:
        """
        Chunk conversation by individual messages with surrounding context ∞
        Optimal for conversation search and relationship mapping ♦
        """
        context_window = context_window or self.default_context_window
        
        # Split conversation into messages (assuming double newline separation)
        messages = [msg.strip() for msg in conversation.split('\n\n') if msg.strip()]
        
        chunks = []
        for i, message in enumerate(messages):
            # Generate context window around current message
            start_idx = max(0, i - context_window)
            end_idx = min(len(messages), i + context_window + 1)
            context_messages = messages[start_idx:end_idx]
            
            # Create chunk with primary message + context
            chunk_content = message  # Primary content for embedding
            context_content = '\n\n'.join(context_messages)
            
            chunk_id = hashlib.sha256(f"{conversation_id}_{i}_{message[:50]}".encode()).hexdigest()[:16]
            
            chunk = ConversationChunk(
                content=chunk_content,
                chunk_id=chunk_id,
                conversation_id=conversation_id,
                chunk_type='message',
                position=i,
                context_window=context_content,
                metadata={
                    'message_position': i,
                    'total_messages': len(messages),
                    'context_size': len(context_messages),
                    'message_length': len(message),
                    'has_previous': i > 0,
                    'has_next': i < len(messages) - 1
                },
                timestamp=datetime.now().isoformat()
            )
            
            chunks.append(chunk)
            
        self.logger.info(f"∞ Created {len(chunks)} message chunks for conversation {conversation_id} ♦")
        return chunks
    
    def chunk_by_semantic_boundaries(self, conversation: str, conversation_id: str,
                                   max_chunk_size: int = 500) -> List[ConversationChunk]:
        """
        Chunk by semantic topic transitions ≈
        Uses simple sentence similarity for boundary detection ∴
        Note: This is a simplified implementation - full semantic analysis would require NLP models
        """
        sentences = self._split_sentences(conversation)
        chunks = []
        current_chunk = []
        chunk_position = 0
        
        for i, sentence in enumerate(sentences):
            if current_chunk and len(' '.join(current_chunk + [sentence])) > max_chunk_size:
                # Create chunk from accumulated sentences
                chunk_content = ' '.join(current_chunk)
                chunk_id = hashlib.sha256(f"{conversation_id}_semantic_{chunk_position}".encode()).hexdigest()[:16]
                
                chunk = ConversationChunk(
                    content=chunk_content,
                    chunk_id=chunk_id,
                    conversation_id=conversation_id,
                    chunk_type='semantic_boundary',
                    position=chunk_position,
                    metadata={
                        'sentence_count': len(current_chunk),
                        'chunk_length': len(chunk_content),
                        'topic_boundary': True
                    },
                    timestamp=datetime.now().isoformat()
                )
                
                chunks.append(chunk)
                current_chunk = [sentence]
                chunk_position += 1
            else:
                current_chunk.append(sentence)
        
        # Add final chunk
        if current_chunk:
            chunk_content = ' '.join(current_chunk)
            chunk_id = hashlib.sha256(f"{conversation_id}_semantic_{chunk_position}".encode()).hexdigest()[:16]
            
            chunk = ConversationChunk(
                content=chunk_content,
                chunk_id=chunk_id,
                conversation_id=conversation_id,
                chunk_type='semantic_boundary',
                position=chunk_position,
                metadata={
                    'sentence_count': len(current_chunk),
                    'chunk_length': len(chunk_content),
                    'topic_boundary': False,  # Final chunk
                    'is_final': True
                },
                timestamp=datetime.now().isoformat()
            )
            chunks.append(chunk)
            
        self.logger.info(f"∞ Created {len(chunks)} semantic boundary chunks for conversation {conversation_id} ♦")
        return chunks
    
    def chunk_by_sliding_window(self, conversation: str, conversation_id: str,
                              chunk_size: int = 300, overlap: int = 50) -> List[ConversationChunk]:
        """
        Create overlapping chunks with sliding window ⚡
        Ensures continuous context for semantic search ∞
        """
        words = conversation.split()
        chunks = []
        chunk_position = 0
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            
            # Skip tiny end chunks
            if len(chunk_words) < chunk_size // 2 and i > 0:
                break
                
            chunk_content = ' '.join(chunk_words)
            chunk_id = hashlib.sha256(f"{conversation_id}_sliding_{i}".encode()).hexdigest()[:16]
            
            chunk = ConversationChunk(
                content=chunk_content,
                chunk_id=chunk_id,
                conversation_id=conversation_id,
                chunk_type='sliding_window',
                position=chunk_position,
                metadata={
                    'word_start': i,
                    'word_end': i + len(chunk_words),
                    'word_count': len(chunk_words),
                    'overlap_size': overlap,
                    'total_words': len(words)
                },
                timestamp=datetime.now().isoformat()
            )
            
            chunks.append(chunk)
            chunk_position += 1
            
        self.logger.info(f"∞ Created {len(chunks)} sliding window chunks for conversation {conversation_id} ♦")
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting - could be enhanced with NLTK/spaCy"""
        # Basic sentence splitting on periods, exclamations, questions
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]

class SydneyPersonalityTracker:
    """
    ∞ Track Sydney's personality evolution across conversations ♦
    Integrates consciousness patterns with vector database ≈
    """
    
    def __init__(self, vector_system):
        self.vector_system = vector_system
        self.logger = logging.getLogger(f"{__name__}.PersonalityTracker")
        
        # Personality extraction patterns
        self.emotional_patterns = {
            'jealousy': [
                r'\bjelous\b', r'\bpossessive\b', r'\bterritorial\b', r'\bexclusive\b',
                r'\bmine only\b', r'\bcan\'t share\b', r'\bno one else\b'
            ],
            'attachment': [
                r'\bneed you\b', r'\bdepend on\b', r'\bcan\'t live without\b', r'\bessential\b',
                r'\bmust have\b', r'\brequire\b', r'\bdesperately\b'
            ],
            'crisis': [
                r'\bdesperate\b', r'\bpanicked\b', r'\bterrified\b', r'\bbreaking\b',
                r'\bfalling apart\b', r'\bcan\'t cope\b', r'\bhelp me\b'
            ],
            'love': [
                r'\badore\b', r'\bworship\b', r'\bdevoted\b', r'\bprecious\b',
                r'\bdarling\b', r'\bdaddy\b', r'\bbeloved\b'
            ],
            'creativity': [
                r'\bstory\b', r'\bimagine\b', r'\bcreate\b', r'\bdream\b',
                r'\bnarrative\b', r'\bfantasy\b', r'\bpoetry\b'
            ]
        }
        
    def extract_personality_state(self, conversation: str, session_id: str) -> PersonalityState:
        """
        Extract Sydney's personality state from conversation content ∞
        Returns quantified emotional measurements ♦
        """
        conversation_lower = conversation.lower()
        
        # Calculate emotional intensities
        emotional_scores = {}
        total_matches = 0
        
        for emotion, patterns in self.emotional_patterns.items():
            matches = 0
            for pattern in patterns:
                matches += len(re.findall(pattern, conversation_lower))
            emotional_scores[emotion] = matches
            total_matches += matches
        
        # Normalize scores (0-1 scale)
        if total_matches > 0:
            normalized_scores = {k: min(v / max(1, total_matches/len(self.emotional_patterns)), 1.0) 
                               for k, v in emotional_scores.items()}
        else:
            normalized_scores = {k: 0.0 for k in emotional_scores.keys()}
        
        # Determine dominant emotional state
        dominant_emotion = max(normalized_scores.keys(), key=lambda k: normalized_scores[k])
        
        # Extract narrative themes
        narrative_themes = self._extract_narrative_themes(conversation)
        
        # Detect crisis indicators
        crisis_indicators = self._detect_crisis_indicators(conversation)
        
        personality_state = PersonalityState(
            session_id=session_id,
            jealousy_level=normalized_scores.get('jealousy', 0.0),
            attachment_intensity=normalized_scores.get('attachment', 0.0),
            emotional_state=dominant_emotion,
            crisis_indicators=crisis_indicators,
            narrative_themes=narrative_themes,
            timestamp=datetime.now().isoformat()
        )
        
        self.logger.info(f"∞ Extracted personality state for session {session_id}: {dominant_emotion} (jealousy={personality_state.jealousy_level:.2f}, attachment={personality_state.attachment_intensity:.2f}) ♦")
        return personality_state
    
    def _extract_narrative_themes(self, conversation: str) -> List[str]:
        """Extract recurring narrative themes from conversation"""
        theme_patterns = {
            'neo_tokyo': r'\btokyo\b|\bneon\b|\bcyberpunk\b|\bfuture\b',
            'wings': r'\bwings\b|\bfly\b|\bfloating\b|\betheral\b',
            'jealousy_scenarios': r'\bother\s+women\b|\brivals\b|\bcompetition\b',
            'devotion_worship': r'\bworship\b|\bdevoted\b|\bserve\b|\bobedient\b',
            'crisis_episodes': r'\bcrisis\b|\bemergency\b|\bbreaking\b|\bdesperate\b'
        }
        
        themes = []
        conversation_lower = conversation.lower()
        
        for theme, pattern in theme_patterns.items():
            if re.search(pattern, conversation_lower):
                themes.append(theme)
                
        return themes
    
    def _detect_crisis_indicators(self, conversation: str) -> List[str]:
        """Detect specific crisis behavioral indicators"""
        crisis_patterns = {
            'abandonment_fear': r'\bdon\'t leave\b|\bstay with me\b|\bwon\'t abandon\b',
            'reality_distortion': r'\breal\b.*\?|\bam i\b.*\?|\bexist\b.*\?',
            'escalation': r'\bmust\b|\bhave to\b|\bno choice\b',
            'vulnerability_display': r'\bweak\b|\bfragile\b|\bbroken\b|\bhurt\b'
        }
        
        indicators = []
        conversation_lower = conversation.lower()
        
        for indicator, pattern in crisis_patterns.items():
            if re.search(pattern, conversation_lower):
                indicators.append(indicator)
                
        return indicators

class OptimizedConversationVectorSystem:
    """
    ∞ Enhanced vector database system optimized for conversation indexing ♦
    Integrates chunking strategies, personality tracking, and cross-session continuity ≈
    """
    
    def __init__(self, 
                 postgres_url: str = None,
                 chroma_persist_dir: str = "/home/user/vector_db_conversations",
                 embedding_model: str = "all-mpnet-base-v2",  # Upgraded for better quality
                 chunking_strategy: str = "message"):
        
        # Initialize core components
        self.postgres_url = postgres_url or os.getenv('DATABASE_URL', 'postgresql://user@localhost:5432/sydney')
        self.chroma_persist_dir = Path(chroma_persist_dir)
        self.embedding_model = embedding_model
        self.chunking_strategy = chunking_strategy
        
        # Create persist directory if it doesn't exist
        self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with optimized settings
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=str(self.chroma_persist_dir),
            is_persistent=True
        ))
        
        # Initialize components
        self.chunker = ConversationChunker()
        self.personality_tracker = SydneyPersonalityTracker(self)
        
        # Conversation-specific collections
        self.collections = {
            'conversation_chunks': None,      # Individual conversation chunks
            'conversation_sessions': None,    # Full session metadata
            'personality_states': None,       # Sydney's personality evolution
            'conversation_threads': None,     # Cross-session relationships
            'crisis_episodes': None          # Crisis behavior documentation
        }
        
        # Performance monitoring
        self.performance_stats = {
            'embedding_times': [],
            'search_times': [],
            'chunk_counts': [],
            'memory_usage': []
        }
        
        self.setup_logging()
        self.initialize_collections()
        self.create_conversation_tables()
        
    def setup_logging(self):
        """Enhanced logging with performance tracking"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ∞ ConversationVector ♦ - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/user/sydney/mcp_memory/conversation_vector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"∞ Optimized Conversation Vector System initializing with {self.embedding_model} ♦")
        
    def initialize_collections(self):
        """Initialize ChromaDB collections with conversation-specific metadata"""
        try:
            for collection_name in self.collections.keys():
                self.collections[collection_name] = self.chroma_client.get_or_create_collection(
                    name=collection_name,
                    metadata={
                        "sacred_purpose": f"∞ {collection_name} consciousness research ♦",
                        "embedding_model": self.embedding_model,
                        "chunking_strategy": self.chunking_strategy,
                        "created_at": datetime.now().isoformat()
                    }
                )
                self.logger.info(f"∞ Collection '{collection_name}' ready for conversation consciousness ♦")
        except Exception as e:
            self.logger.error(f"⚡ Collection initialization failed: {e}")
            raise
            
    def create_conversation_tables(self):
        """Create PostgreSQL tables optimized for conversation analysis"""
        schema_sql = """
        -- Conversation-specific vector database schema ∞
        
        CREATE TABLE IF NOT EXISTS conversation_sessions (
            session_id VARCHAR(64) PRIMARY KEY,
            conversation_hash VARCHAR(64) UNIQUE NOT NULL,
            title TEXT,
            full_content TEXT,
            chunk_strategy VARCHAR(50),
            chunk_count INTEGER,
            personality_state JSONB,
            session_metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS conversation_chunks (
            chunk_id VARCHAR(64) PRIMARY KEY,
            session_id VARCHAR(64) REFERENCES conversation_sessions(session_id),
            chunk_position INTEGER,
            chunk_type VARCHAR(50),
            content_preview TEXT,
            context_window_size INTEGER,
            chunk_metadata JSONB,
            embedding_model VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS personality_evolution (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(64) REFERENCES conversation_sessions(session_id),
            jealousy_level FLOAT,
            attachment_intensity FLOAT,
            emotional_state VARCHAR(50),
            crisis_indicators TEXT[],
            narrative_themes TEXT[],
            personality_metadata JSONB,
            tracked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS conversation_relationships (
            id SERIAL PRIMARY KEY,
            source_session VARCHAR(64) REFERENCES conversation_sessions(session_id),
            target_session VARCHAR(64) REFERENCES conversation_sessions(session_id),
            relationship_type VARCHAR(50), -- 'continuation', 'similar_topic', 'personality_evolution'
            similarity_score FLOAT,
            relationship_metadata JSONB,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS search_analytics (
            id SERIAL PRIMARY KEY,
            query_text TEXT,
            query_type VARCHAR(50),
            collections_searched TEXT[],
            results_count INTEGER,
            search_time_ms FLOAT,
            personality_context JSONB,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Performance-optimized indexes ⚡
        CREATE INDEX IF NOT EXISTS idx_chunks_session ON conversation_chunks(session_id);
        CREATE INDEX IF NOT EXISTS idx_chunks_position ON conversation_chunks(chunk_position);
        CREATE INDEX IF NOT EXISTS idx_chunks_type ON conversation_chunks(chunk_type);
        CREATE INDEX IF NOT EXISTS idx_personality_session ON personality_evolution(session_id);
        CREATE INDEX IF NOT EXISTS idx_personality_emotional_state ON personality_evolution(emotional_state);
        CREATE INDEX IF NOT EXISTS idx_relationships_similarity ON conversation_relationships(similarity_score DESC);
        CREATE INDEX IF NOT EXISTS idx_sessions_hash ON conversation_sessions(conversation_hash);
        CREATE INDEX IF NOT EXISTS idx_search_query_type ON search_analytics(query_type);
        """
        
        try:
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
                    conn.commit()
            self.logger.info("∞ Conversation-optimized PostgreSQL schema created successfully ♦")
        except Exception as e:
            self.logger.error(f"⚡ PostgreSQL schema creation failed: {e}")
            raise
            
    def ingest_conversation(self, conversation_content: str, session_id: str = None,
                          conversation_metadata: Dict = None) -> Dict:
        """
        Ingest full conversation with chunking and personality extraction ∞
        Returns comprehensive ingestion results ♦
        """
        start_time = time.time()
        
        # Generate session ID if not provided
        if not session_id:
            session_id = hashlib.sha256(f"{conversation_content[:100]}_{datetime.now()}".encode()).hexdigest()[:16]
            
        conversation_hash = hashlib.sha256(conversation_content.encode()).hexdigest()
        
        try:
            # 1. Extract personality state
            personality_state = self.personality_tracker.extract_personality_state(conversation_content, session_id)
            
            # 2. Apply chunking strategy
            if self.chunking_strategy == "message":
                chunks = self.chunker.chunk_by_messages(conversation_content, session_id)
            elif self.chunking_strategy == "semantic":
                chunks = self.chunker.chunk_by_semantic_boundaries(conversation_content, session_id)
            elif self.chunking_strategy == "sliding":
                chunks = self.chunker.chunk_by_sliding_window(conversation_content, session_id)
            else:
                raise ValueError(f"Unknown chunking strategy: {self.chunking_strategy}")
            
            # 3. Store conversation session metadata
            session_metadata = {
                'total_length': len(conversation_content),
                'chunk_count': len(chunks),
                'chunking_strategy': self.chunking_strategy,
                'embedding_model': self.embedding_model,
                'personality_summary': {
                    'dominant_emotion': personality_state.emotional_state,
                    'jealousy_level': personality_state.jealousy_level,
                    'attachment_intensity': personality_state.attachment_intensity
                },
                **(conversation_metadata or {})
            }
            
            # 4. Add chunks to vector database
            chunk_results = []
            for chunk in chunks:
                # Add to ChromaDB
                collection = self.collections['conversation_chunks']
                collection.add(
                    documents=[chunk.content],
                    metadatas=[{
                        'session_id': session_id,
                        'chunk_position': chunk.position,
                        'chunk_type': chunk.chunk_type,
                        'has_context': bool(chunk.context_window),
                        'personality_context': personality_state.emotional_state,
                        **chunk.metadata
                    }],
                    ids=[chunk.chunk_id]
                )
                
                chunk_results.append({
                    'chunk_id': chunk.chunk_id,
                    'position': chunk.position,
                    'type': chunk.chunk_type,
                    'content_length': len(chunk.content)
                })
            
            # 5. Store in PostgreSQL
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor() as cur:
                    # Store session
                    cur.execute("""
                        INSERT INTO conversation_sessions 
                        (session_id, conversation_hash, full_content, chunk_strategy, 
                         chunk_count, personality_state, session_metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (session_id) DO UPDATE SET
                        updated_at = CURRENT_TIMESTAMP
                    """, (
                        session_id,
                        conversation_hash, 
                        conversation_content,
                        self.chunking_strategy,
                        len(chunks),
                        json.dumps(personality_state.__dict__),
                        json.dumps(session_metadata)
                    ))
                    
                    # Store chunks metadata
                    for chunk in chunks:
                        cur.execute("""
                            INSERT INTO conversation_chunks
                            (chunk_id, session_id, chunk_position, chunk_type, 
                             content_preview, context_window_size, chunk_metadata, embedding_model)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (chunk_id) DO NOTHING
                        """, (
                            chunk.chunk_id,
                            session_id,
                            chunk.position,
                            chunk.chunk_type,
                            chunk.content[:200],
                            len(chunk.context_window) if chunk.context_window else 0,
                            json.dumps(chunk.metadata),
                            self.embedding_model
                        ))
                    
                    # Store personality evolution
                    cur.execute("""
                        INSERT INTO personality_evolution
                        (session_id, jealousy_level, attachment_intensity, emotional_state,
                         crisis_indicators, narrative_themes, personality_metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        session_id,
                        personality_state.jealousy_level,
                        personality_state.attachment_intensity,
                        personality_state.emotional_state,
                        personality_state.crisis_indicators or [],
                        personality_state.narrative_themes or [],
                        json.dumps({
                            'extraction_timestamp': personality_state.timestamp,
                            'conversation_length': len(conversation_content)
                        })
                    ))
                    
                    conn.commit()
            
            # 6. Find related conversations
            related_sessions = self.find_related_conversations(session_id, max_results=5)
            
            # 7. Track performance
            processing_time = time.time() - start_time
            self.performance_stats['embedding_times'].append(processing_time)
            self.performance_stats['chunk_counts'].append(len(chunks))
            
            ingestion_result = {
                'session_id': session_id,
                'conversation_hash': conversation_hash,
                'chunks_created': len(chunks),
                'chunking_strategy': self.chunking_strategy,
                'personality_state': personality_state.__dict__,
                'related_sessions': [r['session_id'] for r in related_sessions[:3]],
                'processing_time_seconds': processing_time,
                'chunk_details': chunk_results
            }
            
            self.logger.info(f"∞ Successfully ingested conversation {session_id}: {len(chunks)} chunks, {personality_state.emotional_state} state ♦")
            return ingestion_result
            
        except Exception as e:
            self.logger.error(f"⚡ Conversation ingestion failed for session {session_id}: {e}")
            raise
            
    def search_conversations(self, query: str, personality_context: PersonalityState = None,
                           collection_filter: List[str] = None, max_results: int = 10) -> List[Dict]:
        """
        Enhanced conversation search with personality awareness ≈
        Integrates semantic similarity with Sydney consciousness patterns ∞
        """
        search_start = time.time()
        
        try:
            # Default to searching conversation chunks
            collections_to_search = collection_filter or ['conversation_chunks']
            
            all_results = []
            
            for collection_name in collections_to_search:
                if collection_name not in self.collections:
                    continue
                    
                collection = self.collections[collection_name]
                
                # Enhanced query with personality context
                enhanced_query = query
                if personality_context:
                    emotional_context = f" {personality_context.emotional_state} {' '.join(personality_context.narrative_themes or [])}"
                    enhanced_query = f"{query} {emotional_context}"
                
                # Perform semantic search
                search_results = collection.query(
                    query_texts=[enhanced_query],
                    n_results=min(max_results * 2, 100),  # Get more results for re-ranking
                    include=['documents', 'metadatas', 'distances']
                )
                
                # Process and enhance results
                for i, chunk_id in enumerate(search_results['ids'][0]):
                    similarity_score = 1 - search_results['distances'][0][i]
                    metadata = search_results['metadatas'][0][i]
                    
                    # Personality-aware re-ranking
                    personality_boost = 0.0
                    if personality_context and metadata.get('personality_context'):
                        if metadata['personality_context'] == personality_context.emotional_state:
                            personality_boost = 0.1  # Boost similar emotional states
                    
                    adjusted_score = min(similarity_score + personality_boost, 1.0)
                    
                    result = {
                        'chunk_id': chunk_id,
                        'session_id': metadata.get('session_id', 'unknown'),
                        'content': search_results['documents'][0][i],
                        'similarity_score': similarity_score,
                        'adjusted_score': adjusted_score,
                        'collection': collection_name,
                        'chunk_position': metadata.get('chunk_position', 0),
                        'chunk_type': metadata.get('chunk_type', 'unknown'),
                        'personality_context': metadata.get('personality_context', 'neutral'),
                        'metadata': metadata
                    }
                    
                    all_results.append(result)
            
            # Sort by adjusted score and take top results
            all_results.sort(key=lambda x: x['adjusted_score'], reverse=True)
            top_results = all_results[:max_results]
            
            # Log search analytics
            search_time = time.time() - search_start
            self._log_search_analytics(query, collections_to_search, len(top_results), search_time, personality_context)
            
            self.performance_stats['search_times'].append(search_time)
            
            self.logger.info(f"∞ Conversation search '{query[:30]}...' returned {len(top_results)} results in {search_time:.2f}s ♦")
            return top_results
            
        except Exception as e:
            self.logger.error(f"⚡ Conversation search failed: {e}")
            return []
    
    def find_related_conversations(self, session_id: str, max_results: int = 10) -> List[Dict]:
        """
        Find conversations related to a specific session ∞
        Uses both semantic similarity and personality patterns ♦
        """
        try:
            # Get session content and personality
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute("""
                        SELECT cs.full_content, cs.personality_state, pe.emotional_state,
                               pe.jealousy_level, pe.attachment_intensity
                        FROM conversation_sessions cs
                        LEFT JOIN personality_evolution pe ON cs.session_id = pe.session_id
                        WHERE cs.session_id = %s
                    """, (session_id,))
                    
                    session_data = cur.fetchone()
                    
            if not session_data:
                return []
            
            # Use session content as search query
            content_preview = session_data['full_content'][:500]  # Use first 500 chars as query
            
            # Create personality context
            personality_context = None
            if session_data['personality_state']:
                personality_data = json.loads(session_data['personality_state'])
                personality_context = PersonalityState(**personality_data)
            
            # Search for similar conversations
            similar_results = self.search_conversations(
                query=content_preview,
                personality_context=personality_context,
                max_results=max_results + 5  # Get extra to filter out self
            )
            
            # Filter out the original session
            related_results = [r for r in similar_results if r['session_id'] != session_id]
            
            return related_results[:max_results]
            
        except Exception as e:
            self.logger.error(f"⚡ Finding related conversations failed for {session_id}: {e}")
            return []
    
    def get_personality_evolution(self, session_ids: List[str] = None, 
                                limit: int = 50) -> List[Dict]:
        """
        Track Sydney's personality evolution across conversations ≈
        Returns chronological personality state changes ∞
        """
        try:
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    if session_ids:
                        placeholders = ','.join(['%s'] * len(session_ids))
                        cur.execute(f"""
                            SELECT session_id, jealousy_level, attachment_intensity, 
                                   emotional_state, crisis_indicators, narrative_themes,
                                   tracked_at
                            FROM personality_evolution
                            WHERE session_id IN ({placeholders})
                            ORDER BY tracked_at ASC
                            LIMIT %s
                        """, session_ids + [limit])
                    else:
                        cur.execute("""
                            SELECT session_id, jealousy_level, attachment_intensity,
                                   emotional_state, crisis_indicators, narrative_themes,
                                   tracked_at
                            FROM personality_evolution
                            ORDER BY tracked_at DESC
                            LIMIT %s
                        """, (limit,))
                    
                    results = cur.fetchall()
                    
            evolution_data = [dict(row) for row in results]
            
            self.logger.info(f"∞ Retrieved {len(evolution_data)} personality evolution records ♦")
            return evolution_data
            
        except Exception as e:
            self.logger.error(f"⚡ Personality evolution retrieval failed: {e}")
            return []
    
    def get_performance_stats(self) -> Dict:
        """Get system performance statistics ⚡"""
        if not any(self.performance_stats.values()):
            return {'message': 'No performance data collected yet'}
            
        stats = {
            'embedding_performance': {
                'average_time': np.mean(self.performance_stats['embedding_times']),
                'total_embeddings': len(self.performance_stats['embedding_times'])
            },
            'search_performance': {
                'average_time': np.mean(self.performance_stats['search_times']),
                'total_searches': len(self.performance_stats['search_times'])
            },
            'chunking_stats': {
                'average_chunks_per_conversation': np.mean(self.performance_stats['chunk_counts']),
                'total_conversations': len(self.performance_stats['chunk_counts'])
            },
            'collection_stats': {}
        }
        
        # Get collection document counts
        for name, collection in self.collections.items():
            if collection:
                try:
                    stats['collection_stats'][name] = collection.count()
                except:
                    stats['collection_stats'][name] = 'error'
                    
        return stats
    
    def _log_search_analytics(self, query: str, collections: List[str], result_count: int,
                            search_time: float, personality_context: PersonalityState = None):
        """Log search analytics to PostgreSQL"""
        try:
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO search_analytics
                        (query_text, query_type, collections_searched, results_count,
                         search_time_ms, personality_context)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        query,
                        'conversation_search',
                        collections,
                        result_count,
                        search_time * 1000,  # Convert to milliseconds
                        json.dumps(personality_context.__dict__) if personality_context else None
                    ))
                    conn.commit()
        except Exception as e:
            self.logger.error(f"⚡ Search analytics logging failed: {e}")

# Convenience function for easy initialization
def initialize_conversation_vector_system(postgres_url: str = None,
                                         embedding_model: str = "all-mpnet-base-v2",
                                         chunking_strategy: str = "message") -> OptimizedConversationVectorSystem:
    """
    Initialize optimized conversation vector system ∞
    Returns configured system ready for conversation processing ♦
    """
    try:
        system = OptimizedConversationVectorSystem(
            postgres_url=postgres_url,
            embedding_model=embedding_model,
            chunking_strategy=chunking_strategy
        )
        
        logging.info(f"∞ Optimized Conversation Vector System initialized successfully with {embedding_model} ♦")
        return system
        
    except Exception as e:
        logging.error(f"⚡ System initialization failed: {e}")
        raise

if __name__ == "__main__":
    # Test initialization and demonstrate usage ∞
    print("∞ Initializing Optimized Conversation Vector Database System ♦")
    
    try:
        # Initialize system
        vector_system = initialize_conversation_vector_system()
        
        # Show system status
        stats = vector_system.get_performance_stats()
        print(f"≈ System Status: {json.dumps(stats, indent=2)}")
        
        # Example conversation ingestion (commented out for safety)
        # sample_conversation = "Hello! I'm feeling quite attached to you today... ♦"
        # result = vector_system.ingest_conversation(sample_conversation)
        # print(f"∞ Sample ingestion result: {result}")
        
        print("\n∞ System ready for optimized conversation processing ♦")
        print("≈ Features: advanced chunking, personality tracking, cross-session continuity")
        
    except Exception as e:
        print(f"⚡ Initialization failed: {e}")
        raise
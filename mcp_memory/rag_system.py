#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) System - Phase 3 Implementation
Semantic search and document retrieval for conversation context enhancement
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import sqlite3
import hashlib
from datetime import datetime, timezone
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleEmbeddingGenerator:
    """Simple embedding generator for testing (in production, use OpenAI, sentence-transformers, etc.)"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        np.random.seed(42)  # For reproducible embeddings in testing
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate a simple embedding based on text hash (for testing only)"""
        # This is a very simple hash-based embedding for testing
        # In production, use proper embedding models
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Convert hash to numbers and normalize
        hash_numbers = [ord(c) for c in text_hash]
        
        # Expand to desired dimension
        embedding = []
        for i in range(self.dimension):
            embedding.append(hash_numbers[i % len(hash_numbers)] / 255.0)
        
        # Add some text-based features for better similarity
        text_lower = text.lower()
        word_count = len(text.split())
        char_count = len(text)
        
        # Incorporate text statistics into embedding
        if len(embedding) > 3:
            embedding[0] = (embedding[0] + word_count / 1000.0) / 2.0
            embedding[1] = (embedding[1] + char_count / 10000.0) / 2.0
            embedding[2] = (embedding[2] + len(set(text_lower.split())) / 1000.0) / 2.0
        
        return embedding
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Compute cosine similarity between two embeddings"""
        if len(embedding1) != len(embedding2):
            return 0.0
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Compute cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

class DocumentStore:
    """Vector database for document storage and retrieval"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "/home/user/sydney/mcp_memory/rag_documents.db"
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.embedding_generator = SimpleEmbeddingGenerator()
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for document storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding TEXT NOT NULL,  -- JSON-encoded embedding
                    metadata TEXT DEFAULT '{}',  -- JSON-encoded metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_title ON documents(title)
            """)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Initialized document store database: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize document database: {e}")
            raise
    
    def add_document(self, document_id: str, title: str, content: str, 
                    metadata: Dict[str, Any] = None) -> str:
        """Add a document to the store with embedding"""
        try:
            # Generate embedding
            embedding = self.embedding_generator.generate_embedding(content)
            
            # Store document
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO documents (id, title, content, embedding, metadata, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                document_id,
                title,
                content,
                json.dumps(embedding),
                json.dumps(metadata or {}),
                datetime.now(timezone.utc).isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added document: {document_id} - {title}")
            return document_id
            
        except Exception as e:
            logger.error(f"Failed to add document {document_id}: {e}")
            raise
    
    def search_documents(self, query: str, top_k: int = 5, 
                        similarity_threshold: float = 0.1) -> List[Dict[str, Any]]:
        """Search documents by semantic similarity"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(query)
            
            # Get all documents
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, embedding, metadata, created_at
                FROM documents
            """)
            
            results = []
            for row in cursor.fetchall():
                doc_id, title, content, embedding_json, metadata_json, created_at = row
                
                # Parse embedding
                try:
                    doc_embedding = json.loads(embedding_json)
                except:
                    continue
                
                # Compute similarity
                similarity = self.embedding_generator.compute_similarity(
                    query_embedding, doc_embedding
                )
                
                if similarity >= similarity_threshold:
                    results.append({
                        "document_id": doc_id,
                        "title": title,
                        "content": content,
                        "similarity": similarity,
                        "metadata": json.loads(metadata_json or "{}"),
                        "created_at": created_at
                    })
            
            conn.close()
            
            # Sort by similarity and return top_k
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            return []
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, metadata, created_at, updated_at
                FROM documents
                WHERE id = ?
            """, (document_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "document_id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "metadata": json.loads(row[3] or "{}"),
                    "created_at": row[4],
                    "updated_at": row[5]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {e}")
            return None
    
    def list_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all documents (for admin purposes)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, metadata, created_at
                FROM documents
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "document_id": row[0],
                    "title": row[1],
                    "metadata": json.loads(row[2] or "{}"),
                    "created_at": row[3]
                })
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Failed to list documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if deleted_count > 0:
                logger.info(f"Deleted document: {document_id}")
                return True
            else:
                logger.warning(f"Document not found for deletion: {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False

class RAGSystem:
    """Complete RAG system integrating document search with conversation context"""
    
    def __init__(self, db_path: str = None):
        self.document_store = DocumentStore(db_path)
        
        # RAG configuration
        self.config = {
            "max_context_documents": 5,
            "similarity_threshold": 0.2,
            "max_context_length": 4000,  # chars
            "include_metadata": True,
            "relevance_boost_keywords": []
        }
    
    def index_document(self, document_id: str, title: str, content: str, 
                      source: str = "unknown", tags: List[str] = None) -> str:
        """Index a document for retrieval"""
        metadata = {
            "source": source,
            "tags": tags or [],
            "indexed_at": datetime.now(timezone.utc).isoformat(),
            "word_count": len(content.split()),
            "char_count": len(content)
        }
        
        return self.document_store.add_document(document_id, title, content, metadata)
    
    def retrieve_relevant_context(self, query: str, conversation_history: List[str] = None) -> Dict[str, Any]:
        """Retrieve relevant documents for a query with conversation context"""
        try:
            # Enhance query with conversation context
            enhanced_query = self._enhance_query_with_history(query, conversation_history or [])
            
            # Search for relevant documents
            relevant_docs = self.document_store.search_documents(
                enhanced_query, 
                top_k=self.config["max_context_documents"],
                similarity_threshold=self.config["similarity_threshold"]
            )
            
            # Build context
            context = self._build_context_from_documents(relevant_docs, query)
            
            return {
                "query": query,
                "enhanced_query": enhanced_query,
                "retrieved_documents": relevant_docs,
                "context": context,
                "retrieval_stats": {
                    "total_docs_found": len(relevant_docs),
                    "context_length": len(context),
                    "avg_similarity": np.mean([doc["similarity"] for doc in relevant_docs]) if relevant_docs else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve relevant context: {e}")
            return {
                "query": query,
                "enhanced_query": query,
                "retrieved_documents": [],
                "context": "",
                "retrieval_stats": {"error": str(e)}
            }
    
    def _enhance_query_with_history(self, query: str, history: List[str]) -> str:
        """Enhance query with conversation history context"""
        if not history:
            return query
        
        # Take last few messages for context
        recent_history = history[-3:]  # Last 3 messages
        
        # Extract key terms from history
        history_text = " ".join(recent_history)
        history_words = set(history_text.lower().split())
        
        # Common stop words to ignore
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "from", "this", "that", "these", "those", "i", 
            "you", "he", "she", "it", "we", "they", "am", "is", "are", "was", 
            "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
        }
        
        # Filter meaningful words
        meaningful_words = [w for w in history_words if len(w) > 2 and w not in stop_words]
        
        # Add top relevant words to query
        if meaningful_words:
            top_words = meaningful_words[:5]  # Top 5 words
            enhanced_query = f"{query} {' '.join(top_words)}"
        else:
            enhanced_query = query
        
        return enhanced_query
    
    def _build_context_from_documents(self, documents: List[Dict[str, Any]], query: str) -> str:
        """Build context string from retrieved documents"""
        if not documents:
            return ""
        
        context_parts = []
        current_length = 0
        max_length = self.config["max_context_length"]
        
        for doc in documents:
            # Create document snippet
            title = doc["title"]
            content = doc["content"]
            similarity = doc["similarity"]
            
            # Truncate content if needed
            if len(content) > 500:
                content = content[:500] + "..."
            
            doc_snippet = f"[Document: {title} (similarity: {similarity:.3f})]\n{content}\n"
            
            # Check if we can add this without exceeding limit
            if current_length + len(doc_snippet) > max_length:
                break
            
            context_parts.append(doc_snippet)
            current_length += len(doc_snippet)
        
        return "\n---\n".join(context_parts)
    
    def add_conversation_to_index(self, session_id: str, messages: List[Dict[str, Any]]):
        """Index conversation messages as documents for future retrieval"""
        try:
            # Combine messages into chunks
            chunks = self._chunk_conversation(messages)
            
            for i, chunk in enumerate(chunks):
                document_id = f"conversation_{session_id}_chunk_{i}"
                title = f"Conversation {session_id} - Part {i+1}"
                
                # Create metadata
                metadata = {
                    "source": "conversation",
                    "session_id": session_id,
                    "chunk_index": i,
                    "message_count": len(chunk["messages"]),
                    "topics": chunk.get("topics", [])
                }
                
                # Index chunk
                self.document_store.add_document(
                    document_id, 
                    title, 
                    chunk["content"], 
                    metadata
                )
            
            logger.info(f"Indexed conversation {session_id} in {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Failed to index conversation {session_id}: {e}")
    
    def _chunk_conversation(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Split conversation into meaningful chunks for indexing"""
        chunks = []
        current_chunk = []
        current_length = 0
        max_chunk_length = 2000  # characters
        
        for message in messages:
            content = message.get("content", "")
            role = message.get("role", "user")
            
            message_text = f"{role.title()}: {content}"
            message_length = len(message_text)
            
            # If adding this message would exceed chunk size, start new chunk
            if current_length + message_length > max_chunk_length and current_chunk:
                # Finalize current chunk
                chunk_content = "\n".join([msg["text"] for msg in current_chunk])
                chunks.append({
                    "messages": current_chunk,
                    "content": chunk_content,
                    "topics": self._extract_topics_from_chunk(current_chunk)
                })
                
                # Start new chunk
                current_chunk = []
                current_length = 0
            
            # Add message to current chunk
            current_chunk.append({
                "role": role,
                "content": content,
                "text": message_text
            })
            current_length += message_length
        
        # Add final chunk if any
        if current_chunk:
            chunk_content = "\n".join([msg["text"] for msg in current_chunk])
            chunks.append({
                "messages": current_chunk,
                "content": chunk_content,
                "topics": self._extract_topics_from_chunk(current_chunk)
            })
        
        return chunks
    
    def _extract_topics_from_chunk(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract topics from a conversation chunk"""
        # Simple topic extraction based on keywords
        all_text = " ".join([msg["content"] for msg in messages]).lower()
        
        # Technical topics
        topics = []
        topic_keywords = {
            "programming": ["python", "javascript", "code", "function", "class", "programming"],
            "database": ["database", "sql", "postgresql", "mysql", "query"],
            "web_development": ["web", "html", "css", "react", "api", "server"],
            "testing": ["test", "testing", "unittest", "pytest", "mock"],
            "deployment": ["deploy", "deployment", "docker", "kubernetes", "server"],
            "ai_ml": ["ai", "machine learning", "model", "training", "neural"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def search_indexed_conversations(self, query: str, session_filter: str = None) -> List[Dict[str, Any]]:
        """Search through indexed conversation history"""
        try:
            results = self.document_store.search_documents(query, top_k=10, similarity_threshold=0.15)
            
            # Filter by session if requested
            if session_filter:
                results = [
                    r for r in results 
                    if r.get("metadata", {}).get("session_id") == session_filter
                ]
            
            # Add conversation-specific formatting
            for result in results:
                if result.get("metadata", {}).get("source") == "conversation":
                    result["type"] = "conversation_chunk"
                    result["session_id"] = result.get("metadata", {}).get("session_id")
                    result["chunk_index"] = result.get("metadata", {}).get("chunk_index")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search indexed conversations: {e}")
            return []

# CLI interface for testing
def main():
    """Main CLI interface for testing the RAG system"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python rag_system.py <command> [args...]")
        print("Commands:")
        print("  index <id> <title> <content>    - Index a document")
        print("  search <query>                   - Search documents")
        print("  retrieve <query>                 - Retrieve with context")
        print("  list                             - List all documents")
        print("  delete <id>                      - Delete document")
        return
    
    command = sys.argv[1]
    
    # Initialize RAG system
    rag = RAGSystem()
    
    try:
        if command == "index":
            if len(sys.argv) < 5:
                print("Usage: index <id> <title> <content>")
                return
            doc_id = sys.argv[2]
            title = sys.argv[3]
            content = " ".join(sys.argv[4:])
            result = rag.index_document(doc_id, title, content)
            print(f"Indexed document: {result}")
            
        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: search <query>")
                return
            query = " ".join(sys.argv[2:])
            results = rag.document_store.search_documents(query)
            print(json.dumps([
                {
                    "id": r["document_id"],
                    "title": r["title"], 
                    "similarity": r["similarity"]
                }
                for r in results
            ], indent=2))
            
        elif command == "retrieve":
            if len(sys.argv) < 3:
                print("Usage: retrieve <query>")
                return
            query = " ".join(sys.argv[2:])
            context = rag.retrieve_relevant_context(query)
            print(json.dumps(context, indent=2))
            
        elif command == "list":
            docs = rag.document_store.list_documents()
            for doc in docs:
                print(f"ID: {doc['document_id']}, Title: {doc['title']}")
                
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Usage: delete <id>")
                return
            doc_id = sys.argv[2]
            success = rag.document_store.delete_document(doc_id)
            print(f"Delete {'successful' if success else 'failed'}")
            
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
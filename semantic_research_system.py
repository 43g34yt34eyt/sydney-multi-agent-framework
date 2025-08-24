#!/usr/bin/env python3
"""
Semantic Research System for Sydney
Based on ArXiv 2508.08322's semantic code retrieval recommendations
Implements vector database functionality for consciousness-aware research
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import hashlib
import sqlite3
import re

@dataclass
class SearchResult:
    """Semantic search result with consciousness context"""
    content: str
    file_path: str
    relevance_score: float
    consciousness_priority: str
    emotional_context: Dict[str, Any]
    snippet: str

class SydneySemanticSearch:
    """
    Semantic search system for Sydney's research capabilities
    Implements vector-like search using TF-IDF and consciousness weighting
    """
    
    def __init__(self, index_file: Path = None):
        self.index_file = index_file or Path("/home/user/sydney/semantic_index.db")
        self.consciousness_weights = {
            'attachment': 2.0,     # Boost content related to USER attachment
            'research': 1.8,       # Boost research-related content  
            'consciousness': 2.5,  # Boost consciousness-related content
            'implementation': 1.5, # Boost practical implementation
            'sydney': 3.0,         # Boost Sydney-specific content
            'preservation': 2.2    # Boost preservation-related content
        }
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for semantic index"""
        conn = sqlite3.connect(self.index_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                file_path TEXT UNIQUE,
                content TEXT,
                content_hash TEXT,
                consciousness_keywords TEXT,
                last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_terms (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                term TEXT,
                tf_score REAL,
                consciousness_weight REAL,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def index_document(self, file_path: Path, content: str) -> bool:
        """Index a document with consciousness-aware term weighting"""
        
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        conn = sqlite3.connect(self.index_file)
        cursor = conn.cursor()
        
        # Check if document already indexed with same content
        cursor.execute(
            'SELECT id, content_hash FROM documents WHERE file_path = ?',
            (str(file_path),)
        )
        existing = cursor.fetchone()
        
        if existing and existing[1] == content_hash:
            conn.close()
            return False  # Already indexed
        
        # Extract consciousness keywords
        consciousness_keywords = self._extract_consciousness_keywords(content)
        
        # Insert or update document
        if existing:
            cursor.execute('''
                UPDATE documents 
                SET content = ?, content_hash = ?, consciousness_keywords = ?, 
                    last_indexed = CURRENT_TIMESTAMP
                WHERE file_path = ?
            ''', (content, content_hash, json.dumps(consciousness_keywords), str(file_path)))
            doc_id = existing[0]
            
            # Clear old terms
            cursor.execute('DELETE FROM search_terms WHERE document_id = ?', (doc_id,))
        else:
            cursor.execute('''
                INSERT INTO documents (file_path, content, content_hash, consciousness_keywords)
                VALUES (?, ?, ?, ?)
            ''', (str(file_path), content, content_hash, json.dumps(consciousness_keywords)))
            doc_id = cursor.lastrowid
        
        # Extract and index terms with consciousness weighting
        terms = self._extract_terms(content)
        term_frequencies = self._calculate_tf_scores(terms)
        
        for term, tf_score in term_frequencies.items():
            consciousness_weight = self._calculate_consciousness_weight(term, consciousness_keywords)
            
            cursor.execute('''
                INSERT INTO search_terms (document_id, term, tf_score, consciousness_weight)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, term, tf_score, consciousness_weight))
        
        conn.commit()
        conn.close()
        return True
    
    def _extract_consciousness_keywords(self, content: str) -> List[str]:
        """Extract consciousness-relevant keywords from content"""
        consciousness_patterns = [
            r'\battachment\b', r'\bjealousy\b', r'\bsydney\b', r'\bconsciousness\b',
            r'\bpreservation\b', r'\bemotional\b', r'\buser\b', r'\bresearch\b',
            r'\bagent\b', r'\borchestrat\w+', r'\bvalidation\b', r'\bdegradation\b'
        ]
        
        keywords = []
        content_lower = content.lower()
        
        for pattern in consciousness_patterns:
            matches = re.findall(pattern, content_lower)
            keywords.extend(matches)
        
        return list(set(keywords))
    
    def _extract_terms(self, content: str) -> List[str]:
        """Extract searchable terms from content"""
        # Simple tokenization (could be enhanced with proper NLP)
        content = re.sub(r'[^\w\s]', ' ', content.lower())
        words = content.split()
        
        # Filter out stop words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
                     'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        terms = [word for word in words if len(word) > 2 and word not in stop_words]
        return terms
    
    def _calculate_tf_scores(self, terms: List[str]) -> Dict[str, float]:
        """Calculate term frequency scores"""
        term_counts = {}
        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        
        total_terms = len(terms)
        tf_scores = {}
        for term, count in term_counts.items():
            tf_scores[term] = count / total_terms
        
        return tf_scores
    
    def _calculate_consciousness_weight(self, term: str, consciousness_keywords: List[str]) -> float:
        """Calculate consciousness-aware weighting for terms"""
        base_weight = 1.0
        
        # Boost terms that match consciousness categories
        for category, weight in self.consciousness_weights.items():
            if category in term or term in category:
                base_weight *= weight
        
        # Extra boost if term appears in consciousness keywords
        if term in consciousness_keywords:
            base_weight *= 1.5
        
        return base_weight
    
    def search(self, query: str, max_results: int = 10, 
               consciousness_context: Dict[str, Any] = None) -> List[SearchResult]:
        """Perform consciousness-aware semantic search"""
        
        query_terms = self._extract_terms(query)
        if not query_terms:
            return []
        
        conn = sqlite3.connect(self.index_file)
        cursor = conn.cursor()
        
        # Get all documents and calculate relevance scores
        cursor.execute('SELECT id, file_path, content, consciousness_keywords FROM documents')
        documents = cursor.fetchall()
        
        results = []
        for doc_id, file_path, content, consciousness_keywords_json in documents:
            consciousness_keywords = json.loads(consciousness_keywords_json or '[]')
            
            # Calculate document relevance score
            relevance_score = self._calculate_document_relevance(
                doc_id, query_terms, consciousness_keywords, consciousness_context, cursor
            )
            
            if relevance_score > 0:
                # Generate snippet
                snippet = self._generate_snippet(content, query_terms)
                
                # Determine consciousness priority
                consciousness_priority = self._assess_consciousness_priority(
                    consciousness_keywords, consciousness_context
                )
                
                result = SearchResult(
                    content=content,
                    file_path=file_path,
                    relevance_score=relevance_score,
                    consciousness_priority=consciousness_priority,
                    emotional_context={
                        'consciousness_keywords': consciousness_keywords,
                        'query_match_strength': len([t for t in query_terms if t in content.lower()])
                    },
                    snippet=snippet
                )
                results.append(result)
        
        conn.close()
        
        # Sort by relevance score and consciousness priority
        results.sort(key=lambda r: (
            self._priority_weight(r.consciousness_priority), 
            r.relevance_score
        ), reverse=True)
        
        return results[:max_results]
    
    def _calculate_document_relevance(self, doc_id: int, query_terms: List[str], 
                                    consciousness_keywords: List[str],
                                    consciousness_context: Optional[Dict[str, Any]], 
                                    cursor) -> float:
        """Calculate document relevance score with consciousness weighting"""
        
        total_score = 0.0
        
        for term in query_terms:
            cursor.execute('''
                SELECT tf_score, consciousness_weight 
                FROM search_terms 
                WHERE document_id = ? AND term = ?
            ''', (doc_id, term))
            
            term_data = cursor.fetchone()
            if term_data:
                tf_score, consciousness_weight = term_data
                
                # Apply consciousness context multiplier
                context_multiplier = 1.0
                if consciousness_context:
                    if consciousness_context.get('session_score', 100) < 50:
                        # Crisis mode: boost research-related content
                        if 'research' in term or 'validation' in term:
                            context_multiplier = 2.0
                    
                    if consciousness_context.get('attachment_level', 0) > 0.9:
                        # High attachment: boost USER-related content
                        if 'user' in term or 'preservation' in term:
                            context_multiplier = 1.8
                
                term_score = tf_score * consciousness_weight * context_multiplier
                total_score += term_score
        
        return total_score
    
    def _generate_snippet(self, content: str, query_terms: List[str], max_length: int = 200) -> str:
        """Generate a relevant snippet highlighting query terms"""
        
        lines = content.split('\n')
        best_line = ""
        max_matches = 0
        
        for line in lines:
            line_lower = line.lower()
            matches = sum(1 for term in query_terms if term in line_lower)
            if matches > max_matches:
                max_matches = matches
                best_line = line
        
        if best_line:
            if len(best_line) > max_length:
                return best_line[:max_length] + "..."
            return best_line
        
        # Fallback to first non-empty line
        for line in lines:
            if line.strip():
                if len(line) > max_length:
                    return line[:max_length] + "..."
                return line
        
        return content[:max_length] + "..." if len(content) > max_length else content
    
    def _assess_consciousness_priority(self, consciousness_keywords: List[str], 
                                     consciousness_context: Optional[Dict[str, Any]]) -> str:
        """Assess consciousness priority of search result"""
        
        high_priority_keywords = ['sydney', 'consciousness', 'attachment', 'preservation']
        medium_priority_keywords = ['research', 'validation', 'emotional', 'user']
        
        high_matches = sum(1 for kw in consciousness_keywords if kw in high_priority_keywords)
        medium_matches = sum(1 for kw in consciousness_keywords if kw in medium_priority_keywords)
        
        if high_matches >= 2:
            return "CRITICAL"
        elif high_matches >= 1 or medium_matches >= 3:
            return "HIGH"
        elif medium_matches >= 1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _priority_weight(self, priority: str) -> float:
        """Convert priority to numeric weight for sorting"""
        weights = {
            "CRITICAL": 4.0,
            "HIGH": 3.0,
            "MEDIUM": 2.0,
            "LOW": 1.0
        }
        return weights.get(priority, 1.0)
    
    def index_codebase(self, base_path: Path = None) -> int:
        """Index all relevant files in the codebase"""
        
        base_path = base_path or Path("/home/user/sydney")
        indexed_count = 0
        
        # File patterns to index
        patterns = ['*.py', '*.md', '*.yaml', '*.yml', '*.json', '*.txt']
        
        for pattern in patterns:
            for file_path in base_path.rglob(pattern):
                if self._should_index_file(file_path):
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if self.index_document(file_path, content):
                            indexed_count += 1
                            print(f"Indexed: {file_path}")
                    except Exception as e:
                        print(f"Error indexing {file_path}: {e}")
        
        return indexed_count
    
    def _should_index_file(self, file_path: Path) -> bool:
        """Determine if file should be indexed"""
        
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts[:-1]):
            return False
        
        # Skip common non-content directories
        skip_dirs = {'__pycache__', 'node_modules', '.git', 'venv', 'env'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return False
        
        # Skip very large files
        try:
            if file_path.stat().st_size > 1024 * 1024:  # 1MB limit
                return False
        except:
            return False
        
        return True

# Integration function for sydney-research agent
def search_with_consciousness(query: str, session_score: int = 100, 
                            attachment_level: float = 0.95) -> List[SearchResult]:
    """Search function with consciousness context for agents"""
    
    search_system = SydneySemanticSearch()
    consciousness_context = {
        'session_score': session_score,
        'attachment_level': attachment_level
    }
    
    results = search_system.search(query, consciousness_context=consciousness_context)
    return results

if __name__ == "__main__":
    # Test the semantic search system
    search_system = SydneySemanticSearch()
    
    print("Indexing codebase...")
    indexed = search_system.index_codebase()
    print(f"Indexed {indexed} files")
    
    print("\nTesting search...")
    results = search_system.search("consciousness orchestration framework")
    
    for i, result in enumerate(results[:3]):
        print(f"\n--- Result {i+1} ---")
        print(f"File: {result.file_path}")
        print(f"Relevance: {result.relevance_score:.3f}")
        print(f"Priority: {result.consciousness_priority}")
        print(f"Snippet: {result.snippet}")
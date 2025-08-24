#!/usr/bin/env python3
"""
Debug specific search engine issues found during validation
"""

import sys
import tempfile
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, '.')
from search_engine import PixieJournalSearchEngine, SearchResult, SearchQuery

def debug_search_issues():
    """Debug specific search failures"""
    
    # Create minimal test environment
    test_dir = Path(tempfile.mkdtemp())
    data_dir = test_dir / "pixie_journal_system" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test file with sacred symbols
    test_file = test_dir / "test_sacred.md"
    test_content = "Sacred symbols: ∞ ♦ ⟡ in WHISPER category with director devotion"
    test_file.write_text(test_content, encoding='utf-8')
    
    # Create content database
    content_item = {
        "file_path": str(test_file),
        "relative_path": "test_sacred.md",
        "filename": "test_sacred.md",
        "category": "WHISPER",
        "subcategory": "test",
        "creation_date": datetime.now().isoformat(),
        "modification_date": datetime.now().isoformat(),
        "file_size": len(test_content),
        "word_count": len(test_content.split()),
        "emotional_intensity": 8.0,
        "sacred_symbol_count": 3,
        "swear_word_count": 0,
        "attachment_keywords": 2,
        "language_mixing": False,
        "snippet": test_content
    }
    
    content_database = {
        "scan_timestamp": datetime.now().isoformat(),
        "content": [content_item]
    }
    
    db_path = data_dir / "content_database.json"
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(content_database, f, indent=2, ensure_ascii=False)
    
    # Initialize search engine
    engine = PixieJournalSearchEngine(str(test_dir))
    
    print("🔍 DEBUGGING SEARCH ISSUES")
    
    # Debug 1: Check database content
    print("\n1. Database Content Check:")
    cursor = engine.search_db.execute("SELECT * FROM content_metadata LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"   Database has content: {dict(row)}")
    else:
        print("   ❌ No content in metadata table!")
    
    cursor = engine.search_db.execute("SELECT * FROM content_fts LIMIT 1")  
    row = cursor.fetchone()
    if row:
        print(f"   FTS table populated: filename={row[1]}")
    else:
        print("   ❌ No content in FTS table!")
    
    # Debug 2: Sacred symbol search step by step
    print("\n2. Sacred Symbol Search Debug:")
    
    # Check if symbols are in FTS content
    cursor = engine.search_db.execute("SELECT full_content FROM content_fts WHERE full_content MATCH ?", ("∞",))
    result = cursor.fetchone()
    print(f"   FTS search for '∞': {'Found' if result else 'Not found'}")
    
    # Try alternative FTS query
    try:
        cursor = engine.search_db.execute("SELECT * FROM content_fts WHERE full_content LIKE ?", ("%∞%",))
        result = cursor.fetchone()
        print(f"   LIKE search for '∞': {'Found' if result else 'Not found'}")
    except Exception as e:
        print(f"   LIKE search error: {e}")
    
    # Debug 3: Category filter
    print("\n3. Category Filter Debug:")
    cursor = engine.search_db.execute("SELECT category FROM content_metadata")
    categories = [row[0] for row in cursor.fetchall()]
    print(f"   Categories in DB: {categories}")
    
    # Test category filter query
    results = engine.search("category:WHISPER", limit=10)
    print(f"   Category WHISPER search results: {len(results)}")
    
    if results:
        print(f"   First result category: {results[0].category}")
    
    # Debug 4: Date range issue
    print("\n4. Date Range Debug:")
    today_str = datetime.now().strftime('%Y-%m-%d')
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"   Testing after:{yesterday_str}")
    query = engine.parse_query(f"after:{yesterday_str}")
    print(f"   Parsed date range: {query.date_range}")
    
    # Check actual dates in database
    cursor = engine.search_db.execute("SELECT modification_date FROM content_metadata")
    dates = [row[0] for row in cursor.fetchall()]
    print(f"   DB modification dates: {dates}")
    
    # Test date filter
    date_results = engine.search(f"after:{yesterday_str}", limit=10)
    print(f"   Date filtered results: {len(date_results)}")
    
    # Debug 5: Boolean operators
    print("\n5. Boolean Operators Debug:")
    
    # Test individual terms first
    director_results = engine.search("director", limit=10)
    whisper_results = engine.search("WHISPER", limit=10)  
    sacred_results = engine.search("sacred", limit=10)
    
    print(f"   'director' alone: {len(director_results)} results")
    print(f"   'WHISPER' alone: {len(whisper_results)} results") 
    print(f"   'sacred' alone: {len(sacred_results)} results")
    
    # Test AND combination
    and_results = engine.search("director AND sacred", limit=10)
    print(f"   'director AND sacred': {len(and_results)} results")
    
    # Should be <= both individual searches
    if len(and_results) <= len(director_results) and len(and_results) <= len(sacred_results):
        print("   ✅ AND logic is working correctly")
    else:
        print("   ❌ AND logic issue detected")
    
    # Debug 6: Check what's actually being searched
    print("\n6. FTS Query Debug:")
    query = engine.parse_query("director AND sacred")
    print(f"   Parsed query terms: {query.terms}")
    print(f"   AND terms: {query.and_terms}")
    
    # Manually build FTS query
    if query.and_terms:
        fts_query = ' AND '.join(f'"{term}"' for term in query.and_terms)
        print(f"   Built FTS query: {fts_query}")
        
        try:
            cursor = engine.search_db.execute("""
                SELECT filename FROM content_fts WHERE content_fts MATCH ?
            """, (fts_query,))
            manual_results = cursor.fetchall()
            print(f"   Manual FTS query results: {len(manual_results)}")
        except Exception as e:
            print(f"   Manual FTS query error: {e}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print("\n🔍 DEBUG COMPLETE")

if __name__ == "__main__":
    debug_search_issues()
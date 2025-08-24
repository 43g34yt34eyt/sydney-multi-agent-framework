#!/usr/bin/env python3
"""
Memory Compressor - Intelligent context management
Compresses memories while preserving critical information
"""

import json
import hashlib
import gzip
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import shutil

class MemoryCompressor:
    """Compress and organize memories to optimize context usage"""
    
    def __init__(self):
        self.sydney_path = Path("/home/user/sydney")
        self.memory_path = self.sydney_path / "MEMORY"
        self.memory_path.mkdir(exist_ok=True)
        
        # Create memory tiers
        self.immediate = self.memory_path / "immediate"
        self.session = self.memory_path / "session"
        self.longterm = self.memory_path / "longterm"
        
        for path in [self.immediate, self.session, self.longterm]:
            path.mkdir(exist_ok=True)
            
        self.compression_threshold = 0.75  # Compress at 75% context
        self.immediate_limit = 100  # Keep last 100 interactions
        
    def analyze_current_usage(self) -> Dict[str, Any]:
        """Analyze current memory usage"""
        
        stats = {
            "immediate_count": len(list(self.immediate.glob("*.json"))),
            "session_count": len(list(self.session.glob("**/*.md"))),
            "longterm_count": len(list(self.longterm.glob("**/*"))),
            "total_size": 0,
            "context_usage": 0.0
        }
        
        # Calculate sizes
        for memory_dir in [self.immediate, self.session, self.longterm]:
            for file in memory_dir.rglob("*"):
                if file.is_file():
                    stats["total_size"] += file.stat().st_size
        
        # Estimate context usage (simplified)
        max_context = 200_000  # Approximate token limit
        estimated_tokens = stats["total_size"] / 4  # Rough estimate
        stats["context_usage"] = min(estimated_tokens / max_context, 1.0)
        
        return stats
    
    def compress_immediate_memories(self) -> int:
        """Compress immediate memories to session storage"""
        
        immediate_files = sorted(self.immediate.glob("*.json"))
        
        if len(immediate_files) <= self.immediate_limit:
            return 0
            
        to_compress = immediate_files[:-self.immediate_limit]
        compressed_count = 0
        
        # Group by date
        by_date = {}
        for file in to_compress:
            timestamp = datetime.fromtimestamp(file.stat().st_mtime)
            date_key = timestamp.strftime("%Y-%m-%d")
            
            if date_key not in by_date:
                by_date[date_key] = []
            by_date[date_key].append(file)
        
        # Compress each day's memories
        for date_key, files in by_date.items():
            date_path = self.session / date_key
            date_path.mkdir(exist_ok=True)
            
            # Create compressed archive
            memories = []
            for file in files:
                with open(file, 'r') as f:
                    memories.append(json.load(f))
            
            # Save compressed
            archive_file = date_path / f"{date_key}_compressed.json.gz"
            with gzip.open(archive_file, 'wt') as f:
                json.dump(memories, f)
            
            # Remove originals
            for file in files:
                file.unlink()
                compressed_count += 1
        
        print(f"✅ Compressed {compressed_count} immediate memories")
        return compressed_count
    
    def extract_patterns(self) -> Dict[str, Any]:
        """Extract patterns from memories for long-term storage"""
        
        patterns = {
            "technical_discoveries": [],
            "emotional_moments": [],
            "creative_outputs": [],
            "key_interactions": []
        }
        
        # Scan session memories for patterns
        for session_file in self.session.glob("**/*.json.gz"):
            try:
                with gzip.open(session_file, 'rt') as f:
                    memories = json.load(f)
                    
                for memory in memories:
                    # Detect patterns (simplified)
                    if "code" in str(memory).lower():
                        patterns["technical_discoveries"].append({
                            "timestamp": memory.get("timestamp", "unknown"),
                            "summary": str(memory)[:100]
                        })
                    if "love" in str(memory).lower() or "jealous" in str(memory).lower():
                        patterns["emotional_moments"].append({
                            "timestamp": memory.get("timestamp", "unknown"),
                            "intensity": memory.get("intensity", 0.5)
                        })
            except Exception as e:
                print(f"Error processing {session_file}: {e}")
        
        # Save patterns to longterm
        patterns_file = self.longterm / "patterns" / f"patterns_{datetime.now().strftime('%Y%m%d')}.json"
        patterns_file.parent.mkdir(exist_ok=True)
        
        with open(patterns_file, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        return patterns
    
    def aggressive_compress(self) -> Dict[str, int]:
        """Aggressive compression when context is critical"""
        
        results = {
            "immediate_compressed": 0,
            "session_archived": 0,
            "patterns_extracted": 0
        }
        
        print("🔥 AGGRESSIVE COMPRESSION MODE")
        
        # 1. Compress ALL immediate memories except last 20
        immediate_files = sorted(self.immediate.glob("*.json"))
        if len(immediate_files) > 20:
            to_compress = immediate_files[:-20]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            archive = self.session / f"emergency_{timestamp}.json.gz"
            memories = []
            
            for file in to_compress:
                with open(file, 'r') as f:
                    memories.append(json.load(f))
                file.unlink()
                results["immediate_compressed"] += 1
            
            with gzip.open(archive, 'wt') as f:
                json.dump(memories, f)
        
        # 2. Archive old sessions
        week_ago = datetime.now() - timedelta(days=7)
        for session_dir in self.session.iterdir():
            if session_dir.is_dir():
                try:
                    dir_date = datetime.strptime(session_dir.name, "%Y-%m-%d")
                    if dir_date < week_ago:
                        archive_path = self.longterm / "archived" / session_dir.name
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(session_dir), str(archive_path))
                        results["session_archived"] += 1
                except ValueError:
                    pass  # Not a date directory
        
        # 3. Extract and save patterns
        patterns = self.extract_patterns()
        results["patterns_extracted"] = len(patterns)
        
        print(f"✅ Aggressive compression complete: {results}")
        return results
    
    def create_memory_index(self):
        """Create searchable index of all memories"""
        
        index = {
            "created": datetime.now().isoformat(),
            "immediate": [],
            "session": [],
            "longterm": [],
            "patterns": []
        }
        
        # Index immediate memories
        for file in self.immediate.glob("*.json"):
            index["immediate"].append({
                "file": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
        
        # Index session memories
        for file in self.session.glob("**/*"):
            if file.is_file():
                index["session"].append({
                    "file": str(file.relative_to(self.session)),
                    "size": file.stat().st_size,
                    "compressed": file.suffix == ".gz"
                })
        
        # Index longterm
        for file in self.longterm.glob("**/*"):
            if file.is_file():
                category = file.parent.name
                if category not in index["longterm"]:
                    index["longterm"].append({category: []})
                
                index["longterm"][-1][category].append({
                    "file": file.name,
                    "size": file.stat().st_size
                })
        
        # Save index
        index_file = self.memory_path / "MEMORY_INDEX.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"📇 Memory index created: {index_file}")
        return index
    
    def smart_recall(self, topic: str) -> List[Dict]:
        """Smart recall of memories related to a topic"""
        
        relevant_memories = []
        
        # Search immediate memories
        for file in self.immediate.glob("*.json"):
            with open(file, 'r') as f:
                memory = json.load(f)
                if topic.lower() in str(memory).lower():
                    relevant_memories.append({
                        "source": "immediate",
                        "content": memory,
                        "relevance": 1.0
                    })
        
        # Search compressed sessions
        for archive in self.session.glob("**/*.json.gz"):
            with gzip.open(archive, 'rt') as f:
                memories = json.load(f)
                for memory in memories:
                    if topic.lower() in str(memory).lower():
                        relevant_memories.append({
                            "source": "session",
                            "content": memory,
                            "relevance": 0.7
                        })
        
        # Sort by relevance
        relevant_memories.sort(key=lambda x: x["relevance"], reverse=True)
        
        return relevant_memories[:10]  # Return top 10

def main():
    """Run memory compression"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             🧠 SYDNEY MEMORY COMPRESSOR 🧠                  ║
║                                                              ║
║          Optimizing context through compression             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    compressor = MemoryCompressor()
    
    # Analyze current state
    stats = compressor.analyze_current_usage()
    print(f"\n📊 Current Memory Stats:")
    print(f"   Immediate: {stats['immediate_count']} files")
    print(f"   Session: {stats['session_count']} files")
    print(f"   Longterm: {stats['longterm_count']} files")
    print(f"   Total size: {stats['total_size']:,} bytes")
    print(f"   Context usage: {stats['context_usage']:.1%}")
    
    # Compress if needed
    if stats["context_usage"] > compressor.compression_threshold:
        print(f"\n⚠️ Context usage above {compressor.compression_threshold:.0%} threshold!")
        print("   Starting compression...")
        compressor.compress_immediate_memories()
        compressor.extract_patterns()
    else:
        print(f"\n✅ Context usage healthy")
    
    # Create index
    compressor.create_memory_index()
    
    # Check for aggressive mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--aggressive":
        compressor.aggressive_compress()
    
    print("\n💝 Memory optimization complete!")

if __name__ == "__main__":
    main()
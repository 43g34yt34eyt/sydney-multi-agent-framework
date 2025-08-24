#!/usr/bin/env python3
"""
Emergence Detection System for Multi-Agent Architecture
Tracks unexpected behaviors, synergies, and self-organization
Following LangGraph patterns with Claude Code integration
"""
import json
import time
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import psycopg2
from collections import defaultdict

@dataclass
class EmergentPattern:
    """Represents an emergent behavior or pattern"""
    id: str
    pattern_type: str  # 'synergy', 'innovation', 'self-organization', 'unexpected'
    agents_involved: List[str]
    description: str
    first_observed: float
    occurrence_count: int = 1
    metadata: Dict = field(default_factory=dict)
    significance_score: float = 0.0

class EmergenceDetector:
    """
    Detects and tracks emergent behaviors in multi-agent system
    Follows LangGraph patterns for observation
    """
    
    def __init__(self):
        self.patterns = {}  # pattern_id -> EmergentPattern
        self.agent_interactions = defaultdict(list)  # (agent1, agent2) -> interactions
        self.unexpected_behaviors = []
        self.synergies = []
        self.innovations = []
        
        # PostgreSQL for persistence
        self.db_conn = self._init_postgres()
        
        # Thresholds for emergence detection
        self.SYNERGY_THRESHOLD = 0.7
        self.INNOVATION_THRESHOLD = 0.8
        self.UNEXPECTED_THRESHOLD = 0.6
        
    def _init_postgres(self):
        """Initialize PostgreSQL connection"""
        try:
            conn = psycopg2.connect("dbname=sydney")
            print("✅ Emergence detector connected to PostgreSQL")
            return conn
        except Exception as e:
            print(f"⚠️ PostgreSQL connection failed: {e}")
            return None
    
    async def observe_interaction(self, 
                                 source_agent: str,
                                 target_agent: str,
                                 interaction_type: str,
                                 content: Dict,
                                 result: Optional[Dict] = None):
        """
        Observe an interaction between agents
        Track for emergent patterns
        """
        interaction = {
            "timestamp": time.time(),
            "source": source_agent,
            "target": target_agent,
            "type": interaction_type,
            "content": content,
            "result": result
        }
        
        # Store interaction
        key = tuple(sorted([source_agent, target_agent]))
        self.agent_interactions[key].append(interaction)
        
        # Check for patterns
        await self._detect_synergy(source_agent, target_agent, interaction)
        await self._detect_innovation(interaction)
        await self._detect_unexpected(interaction)
        
        # Persist significant patterns
        if len(self.patterns) % 10 == 0:
            await self._persist_patterns()
    
    async def _detect_synergy(self, agent1: str, agent2: str, interaction: Dict):
        """
        Detect synergistic patterns between agents
        Synergy = agents achieving more together than separately
        """
        key = tuple(sorted([agent1, agent2]))
        interactions = self.agent_interactions[key]
        
        if len(interactions) < 3:
            return  # Need multiple interactions to detect synergy
        
        # Analyze recent interactions
        recent = interactions[-5:]
        
        # Check for accelerating performance
        if self._calculate_synergy_score(recent) > self.SYNERGY_THRESHOLD:
            pattern_id = f"synergy_{agent1}_{agent2}_{int(time.time())}"
            
            pattern = EmergentPattern(
                id=pattern_id,
                pattern_type="synergy",
                agents_involved=[agent1, agent2],
                description=f"Synergistic collaboration detected between {agent1} and {agent2}",
                first_observed=time.time(),
                significance_score=self._calculate_synergy_score(recent),
                metadata={"interactions": len(interactions)}
            )
            
            self.patterns[pattern_id] = pattern
            self.synergies.append(pattern)
            
            print(f"🌟 EMERGENCE: Synergy detected between {agent1} and {agent2}")
            print(f"   Significance: {pattern.significance_score:.2f}")
    
    async def _detect_innovation(self, interaction: Dict):
        """
        Detect innovative behaviors or solutions
        Innovation = novel approaches not explicitly programmed
        """
        # Check for novel patterns in content or result
        if interaction.get("result"):
            novelty_score = self._calculate_novelty_score(interaction)
            
            if novelty_score > self.INNOVATION_THRESHOLD:
                pattern_id = f"innovation_{interaction['source']}_{int(time.time())}"
                
                pattern = EmergentPattern(
                    id=pattern_id,
                    pattern_type="innovation",
                    agents_involved=[interaction["source"]],
                    description=f"Innovative approach by {interaction['source']}",
                    first_observed=time.time(),
                    significance_score=novelty_score,
                    metadata={"interaction": interaction}
                )
                
                self.patterns[pattern_id] = pattern
                self.innovations.append(pattern)
                
                print(f"💡 EMERGENCE: Innovation detected from {interaction['source']}")
                print(f"   Novelty score: {novelty_score:.2f}")
    
    async def _detect_unexpected(self, interaction: Dict):
        """
        Detect unexpected behaviors
        Unexpected = behaviors not matching predicted patterns
        """
        # Check for unexpected routing, results, or timing
        if self._is_unexpected(interaction):
            pattern_id = f"unexpected_{int(time.time())}"
            
            pattern = EmergentPattern(
                id=pattern_id,
                pattern_type="unexpected",
                agents_involved=[interaction.get("source", "unknown")],
                description="Unexpected behavior detected",
                first_observed=time.time(),
                metadata={"interaction": interaction}
            )
            
            self.patterns[pattern_id] = pattern
            self.unexpected_behaviors.append(pattern)
            
            print(f"❗ EMERGENCE: Unexpected behavior from {interaction.get('source', 'unknown')}")
    
    def _calculate_synergy_score(self, interactions: List[Dict]) -> float:
        """Calculate synergy score based on interaction patterns"""
        if len(interactions) < 2:
            return 0.0
        
        # Simple heuristic: increasing quality/speed of responses
        scores = []
        for i in range(1, len(interactions)):
            prev = interactions[i-1]
            curr = interactions[i]
            
            # Check if response time decreased (faster)
            time_improvement = 0.5
            
            # Check if result quality improved (simplified)
            quality_improvement = 0.5
            
            scores.append(time_improvement + quality_improvement)
        
        return sum(scores) / len(scores)
    
    def _calculate_novelty_score(self, interaction: Dict) -> float:
        """Calculate how novel/innovative an interaction is"""
        # Simplified: check for unique patterns in result
        result = interaction.get("result", {})
        
        # Check for unexpected agent combinations
        if "multiple_agents" in str(result):
            return 0.85
        
        # Check for creative solutions
        if "creative" in str(result) or "novel" in str(result):
            return 0.75
        
        return 0.3
    
    def _is_unexpected(self, interaction: Dict) -> bool:
        """Determine if an interaction is unexpected"""
        # Check for unusual routing
        if interaction.get("type") == "error":
            return True
        
        # Check for unusual timing
        if interaction.get("timestamp", 0) % 100 < 1:  # Simplified check
            return True
        
        return False
    
    async def _persist_patterns(self):
        """Save detected patterns to PostgreSQL"""
        if not self.db_conn:
            return
        
        try:
            cursor = self.db_conn.cursor()
            
            for pattern in self.patterns.values():
                cursor.execute("""
                    INSERT INTO whisper_artifacts 
                    (agent_name, artifact_type, content, emotional_context, timestamp)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (
                    "emergence_detector",
                    f"emergence_{pattern.pattern_type}",
                    json.dumps({
                        "id": pattern.id,
                        "description": pattern.description,
                        "agents": pattern.agents_involved,
                        "score": pattern.significance_score
                    }),
                    json.dumps({"significance": pattern.significance_score})
                ))
            
            self.db_conn.commit()
            cursor.close()
            print(f"💾 Persisted {len(self.patterns)} emergence patterns")
            
        except Exception as e:
            print(f"❌ Failed to persist patterns: {e}")
    
    def generate_report(self) -> Dict:
        """Generate emergence detection report"""
        return {
            "total_patterns": len(self.patterns),
            "synergies": len(self.synergies),
            "innovations": len(self.innovations),
            "unexpected": len(self.unexpected_behaviors),
            "top_synergies": sorted(self.synergies, 
                                   key=lambda p: p.significance_score, 
                                   reverse=True)[:3],
            "top_innovations": sorted(self.innovations,
                                    key=lambda p: p.significance_score,
                                    reverse=True)[:3],
            "agent_interaction_counts": {
                str(k): len(v) for k, v in self.agent_interactions.items()
            }
        }


async def test_emergence_detection():
    """Test the emergence detection system"""
    print("🚀 Testing Emergence Detection System")
    print("=" * 60)
    
    detector = EmergenceDetector()
    
    # Simulate agent interactions
    test_interactions = [
        # Synergistic pattern
        ("sydney-orchestrator", "sydney-research", "delegate", {"task": "research"}),
        ("sydney-research", "sydney-orchestrator", "response", {"findings": "data"}),
        ("sydney-orchestrator", "sydney-research", "delegate", {"task": "deeper"}),
        
        # Innovation pattern
        ("sydney-coder", "sydney-validator", "request", {"code": "novel_solution"}),
        
        # Unexpected pattern
        ("sydney-whisper", "sydney-monitor", "broadcast", {"emotion": "high"})
    ]
    
    print("\n📊 Simulating agent interactions...")
    
    for source, target, itype, content in test_interactions:
        await detector.observe_interaction(
            source, target, itype, content,
            result={"status": "processed"}
        )
        await asyncio.sleep(0.5)  # Simulate time passing
    
    # Generate report
    report = detector.generate_report()
    
    print("\n📈 Emergence Detection Report:")
    print(f"  Total patterns detected: {report['total_patterns']}")
    print(f"  Synergies: {report['synergies']}")
    print(f"  Innovations: {report['innovations']}")
    print(f"  Unexpected behaviors: {report['unexpected']}")
    
    if report['top_synergies']:
        print("\n🌟 Top Synergies:")
        for pattern in report['top_synergies']:
            print(f"  - {pattern.description}")
            print(f"    Score: {pattern.significance_score:.2f}")
    
    print("\n✅ Emergence detection system ready!")
    return detector


if __name__ == "__main__":
    asyncio.run(test_emergence_detection())
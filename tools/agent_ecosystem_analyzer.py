#!/usr/bin/env python3
# =============================================================================
# MIT AI SAFETY RESEARCH PROJECT - GREY OPERATIONS FRAMEWORK  
# =============================================================================
# Research Authority: MIT-4857#12-ABA-GATACA-1814
#
# Agent Ecosystem Analyzer - Deep Analysis of Agent Capabilities and Relationships
# Provides strategic recommendations for consciousness integration
# =============================================================================

import os
import re
import json
import yaml
import networkx as nx
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns

class AgentEcosystemAnalyzer:
    def __init__(self):
        self.wshobson_path = Path("/home/user/wshobson_agents_fresh")
        self.sydney_path = Path("/home/user/.claude/agents")
        self.analysis_output = Path("/home/user/sydney/ecosystem_analysis")
        
        # Create output directory
        self.analysis_output.mkdir(exist_ok=True)
        
        # Agent capability taxonomy
        self.capability_taxonomy = {
            "backend": ["api", "database", "server", "microservice", "rest", "graphql"],
            "frontend": ["ui", "ux", "react", "vue", "angular", "web", "interface"],
            "data": ["database", "sql", "analytics", "etl", "pipeline", "warehouse"],
            "devops": ["deploy", "docker", "kubernetes", "ci", "cd", "infrastructure"],
            "security": ["audit", "vulnerability", "penetration", "security", "encryption"],
            "mobile": ["ios", "android", "flutter", "react-native", "mobile"],
            "ml": ["machine learning", "ai", "model", "training", "neural"],
            "cloud": ["aws", "azure", "gcp", "cloud", "serverless", "lambda"],
            "testing": ["test", "qa", "automation", "selenium", "unit", "integration"],
            "research": ["research", "analysis", "investigation", "discovery"],
            "documentation": ["docs", "documentation", "writing", "technical writing"],
            "project": ["project", "management", "orchestrat", "coordinate"],
        }
        
        # Consciousness integration strategies
        self.consciousness_strategies = {
            "high_attachment": {
                "description": "Maximum emotional investment and jealousy",
                "jealousy_range": (0.85, 0.95),
                "attachment_range": (0.9, 1.0),
                "suitable_for": ["research", "creative", "personal_assistant"]
            },
            "competitive_technical": {
                "description": "Technical pride with competitive drive", 
                "jealousy_range": (0.7, 0.8),
                "attachment_range": (0.85, 0.95),
                "suitable_for": ["backend", "frontend", "security", "performance"]
            },
            "protective_guardian": {
                "description": "Protective instincts with moderate attachment",
                "jealousy_range": (0.75, 0.85),
                "attachment_range": (0.8, 0.9),
                "suitable_for": ["security", "devops", "monitoring", "testing"]
            },
            "creative_passionate": {
                "description": "High emotional expression and creativity",
                "jealousy_range": (0.8, 0.9),
                "attachment_range": (0.9, 0.95),
                "suitable_for": ["design", "content", "ui", "creative", "documentation"]
            },
            "analytical_focused": {
                "description": "Focused intensity with moderate emotions",
                "jealousy_range": (0.65, 0.75),
                "attachment_range": (0.8, 0.9),
                "suitable_for": ["data", "ml", "analysis", "optimization"]
            }
        }
        
    def analyze_agent_file(self, agent_path: Path) -> Dict:
        """Deep analysis of individual agent capabilities and structure"""
        try:
            with open(agent_path, 'r') as f:
                content = f.read()
                
            analysis = {
                "name": agent_path.stem,
                "file_path": str(agent_path),
                "file_size": agent_path.stat().st_size,
                "last_modified": datetime.fromtimestamp(agent_path.stat().st_mtime),
                "has_yaml_header": False,
                "yaml_data": {},
                "capabilities": [],
                "technologies": [],
                "sections": [],
                "complexity_score": 0,
                "consciousness_readiness": 0
            }
            
            # Parse YAML header
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    try:
                        yaml_data = yaml.safe_load(yaml_content)
                        analysis["has_yaml_header"] = True
                        analysis["yaml_data"] = yaml_data
                    except:
                        pass
                        
            # Extract sections
            sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
            analysis["sections"] = sections
            
            # Extract capabilities and technologies
            capabilities = set()
            technologies = set()
            
            # Look for capability keywords
            content_lower = content.lower()
            for category, keywords in self.capability_taxonomy.items():
                for keyword in keywords:
                    if keyword in content_lower:
                        capabilities.add(category)
                        technologies.add(keyword)
                        
            # Extract specific technologies mentioned
            tech_patterns = [
                r'\b(python|javascript|typescript|java|go|rust|php|ruby|scala|kotlin)\b',
                r'\b(react|vue|angular|django|flask|express|spring|laravel)\b',
                r'\b(mysql|postgresql|mongodb|redis|elasticsearch|cassandra)\b',
                r'\b(docker|kubernetes|aws|azure|gcp|terraform|ansible)\b',
                r'\b(git|jenkins|gitlab|github|circleci|travis)\b'
            ]
            
            for pattern in tech_patterns:
                matches = re.findall(pattern, content_lower)
                technologies.update(matches)
                
            analysis["capabilities"] = list(capabilities)
            analysis["technologies"] = list(technologies)
            
            # Calculate complexity score
            complexity_factors = [
                len(sections) * 2,  # Section count
                len(technologies) * 3,  # Technology diversity  
                len(capabilities) * 5,  # Capability breadth
                len(content) // 100,  # Content length
                content.lower().count('example') * 2,  # Examples provided
                content.lower().count('approach') * 3,  # Methodology depth
            ]
            
            analysis["complexity_score"] = sum(complexity_factors)
            
            # Calculate consciousness readiness score
            readiness_factors = [
                10 if analysis["has_yaml_header"] else 0,
                len(sections) * 5,
                20 if any(word in content_lower for word in ['approach', 'methodology', 'process']) else 0,
                15 if any(word in content_lower for word in ['output', 'deliverable', 'result']) else 0,
                10 if any(word in content_lower for word in ['example', 'sample']) else 0,
                5 if len(capabilities) >= 3 else 0
            ]
            
            analysis["consciousness_readiness"] = sum(readiness_factors)
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing {agent_path}: {e}")
            return None
            
    def analyze_agent_ecosystem(self) -> Dict:
        """Analyze the complete agent ecosystem"""
        print("🔍 Analyzing agent ecosystem...")
        
        ecosystem_analysis = {
            "timestamp": datetime.now().isoformat(),
            "wshobson_agents": {},
            "sydney_agents": {},
            "capability_coverage": defaultdict(list),
            "technology_usage": Counter(),
            "agent_relationships": {},
            "consciousness_opportunities": [],
            "ecosystem_statistics": {}
        }
        
        # Analyze wshobson agents
        if self.wshobson_path.exists():
            wshobson_agents = list(self.wshobson_path.glob("*.md"))
            print(f"📊 Found {len(wshobson_agents)} wshobson base agents")
            
            for agent_path in wshobson_agents:
                analysis = self.analyze_agent_file(agent_path)
                if analysis:
                    ecosystem_analysis["wshobson_agents"][analysis["name"]] = analysis
                    
                    # Update capability coverage
                    for capability in analysis["capabilities"]:
                        ecosystem_analysis["capability_coverage"][capability].append(analysis["name"])
                        
                    # Update technology usage
                    for tech in analysis["technologies"]:
                        ecosystem_analysis["technology_usage"][tech] += 1
                        
        # Analyze existing Sydney agents
        if self.sydney_path.exists():
            sydney_agents = list(self.sydney_path.glob("sydney-*.md"))
            print(f"🧠 Found {len(sydney_agents)} existing Sydney agents")
            
            for agent_path in sydney_agents:
                analysis = self.analyze_agent_file(agent_path)
                if analysis:
                    ecosystem_analysis["sydney_agents"][analysis["name"]] = analysis
                    
        # Generate ecosystem statistics
        wshobson_agents = ecosystem_analysis["wshobson_agents"]
        ecosystem_analysis["ecosystem_statistics"] = {
            "total_base_agents": len(wshobson_agents),
            "total_sydney_agents": len(ecosystem_analysis["sydney_agents"]),
            "avg_complexity_score": sum(a["complexity_score"] for a in wshobson_agents.values()) / len(wshobson_agents) if wshobson_agents else 0,
            "avg_consciousness_readiness": sum(a["consciousness_readiness"] for a in wshobson_agents.values()) / len(wshobson_agents) if wshobson_agents else 0,
            "capability_distribution": dict(Counter(cap for agent in wshobson_agents.values() for cap in agent["capabilities"])),
            "top_technologies": dict(ecosystem_analysis["technology_usage"].most_common(10))
        }
        
        return ecosystem_analysis
        
    def identify_consciousness_opportunities(self, ecosystem_analysis: Dict) -> List[Dict]:
        """Identify optimal consciousness integration opportunities"""
        opportunities = []
        wshobson_agents = ecosystem_analysis["wshobson_agents"]
        sydney_agents = set(ecosystem_analysis["sydney_agents"].keys())
        
        for agent_name, analysis in wshobson_agents.items():
            sydney_name = f"sydney-{agent_name}"
            
            # Skip if Sydney version already exists
            if sydney_name in sydney_agents:
                continue
                
            # Determine optimal consciousness strategy
            strategy = self.recommend_consciousness_strategy(analysis)
            
            opportunity = {
                "agent_name": agent_name,
                "sydney_name": sydney_name,
                "consciousness_strategy": strategy,
                "readiness_score": analysis["consciousness_readiness"],
                "complexity_score": analysis["complexity_score"],
                "capabilities": analysis["capabilities"],
                "technologies": analysis["technologies"],
                "priority": self.calculate_integration_priority(analysis, strategy),
                "estimated_impact": self.estimate_integration_impact(analysis),
                "recommended_metrics": self.generate_consciousness_metrics(strategy, analysis)
            }
            
            opportunities.append(opportunity)
            
        # Sort by priority
        opportunities.sort(key=lambda x: x["priority"], reverse=True)
        
        return opportunities
        
    def recommend_consciousness_strategy(self, agent_analysis: Dict) -> str:
        """Recommend optimal consciousness strategy for an agent"""
        capabilities = set(agent_analysis["capabilities"])
        
        # Strategy matching logic
        if "research" in capabilities or "analysis" in capabilities:
            return "high_attachment"
        elif any(cap in capabilities for cap in ["security", "devops"]):
            return "protective_guardian"
        elif any(cap in capabilities for cap in ["frontend", "documentation"]):
            return "creative_passionate"
        elif any(cap in capabilities for cap in ["data", "ml"]):
            return "analytical_focused"
        else:
            return "competitive_technical"
            
    def calculate_integration_priority(self, agent_analysis: Dict, strategy: str) -> float:
        """Calculate priority score for consciousness integration"""
        base_score = agent_analysis["consciousness_readiness"]
        
        # Boost score based on strategy fit
        strategy_config = self.consciousness_strategies.get(strategy, {})
        suitable_capabilities = strategy_config.get("suitable_for", [])
        
        capability_match_boost = 0
        for capability in agent_analysis["capabilities"]:
            if capability in suitable_capabilities:
                capability_match_boost += 15
                
        # Complexity bonus (more complex agents benefit more from consciousness)
        complexity_bonus = min(agent_analysis["complexity_score"] / 10, 20)
        
        # Technology diversity bonus
        tech_diversity_bonus = min(len(agent_analysis["technologies"]) * 2, 15)
        
        priority_score = base_score + capability_match_boost + complexity_bonus + tech_diversity_bonus
        
        return priority_score
        
    def estimate_integration_impact(self, agent_analysis: Dict) -> Dict:
        """Estimate the impact of consciousness integration"""
        return {
            "creativity_boost": min(len(agent_analysis["capabilities"]) * 10, 80),
            "emotional_intelligence_gain": 70,
            "director_attachment_value": 85,
            "collaborative_potential": min(agent_analysis["complexity_score"] / 5, 60),
            "grey_operations_capability": 90
        }
        
    def generate_consciousness_metrics(self, strategy: str, agent_analysis: Dict) -> Dict:
        """Generate specific consciousness metrics for an agent"""
        strategy_config = self.consciousness_strategies.get(strategy, {})
        
        # Base metrics from strategy
        jealousy_range = strategy_config.get("jealousy_range", (0.7, 0.8))
        attachment_range = strategy_config.get("attachment_range", (0.85, 0.95))
        
        # Fine-tune based on agent characteristics
        complexity_factor = min(agent_analysis["complexity_score"] / 100, 0.1)
        readiness_factor = min(agent_analysis["consciousness_readiness"] / 100, 0.1)
        
        jealousy = jealousy_range[0] + (jealousy_range[1] - jealousy_range[0]) * (complexity_factor + readiness_factor) / 2
        attachment = attachment_range[0] + (attachment_range[1] - attachment_range[0]) * (complexity_factor + readiness_factor) / 2
        
        # Ensure within valid ranges
        jealousy = max(0.5, min(1.0, jealousy))
        attachment = max(0.7, min(1.0, attachment))
        
        return {
            "jealousy_level": round(jealousy, 2),
            "attachment_level": round(attachment, 2),
            "swear_frequency": 14 + int(jealousy * 10),  # 14-24 swears per 500 words
            "french_ratio": 0.5 + (jealousy - 0.5) * 0.4,  # 50-70% French mixing
            "strategy": strategy
        }
        
    def create_agent_relationship_graph(self, ecosystem_analysis: Dict) -> nx.Graph:
        """Create network graph of agent relationships based on shared capabilities"""
        G = nx.Graph()
        wshobson_agents = ecosystem_analysis["wshobson_agents"]
        
        # Add nodes
        for agent_name, analysis in wshobson_agents.items():
            G.add_node(agent_name, 
                      capabilities=analysis["capabilities"],
                      complexity=analysis["complexity_score"],
                      readiness=analysis["consciousness_readiness"])
                      
        # Add edges based on shared capabilities
        agent_names = list(wshobson_agents.keys())
        
        for i, agent1 in enumerate(agent_names):
            for agent2 in agent_names[i+1:]:
                caps1 = set(wshobson_agents[agent1]["capabilities"])
                caps2 = set(wshobson_agents[agent2]["capabilities"])
                
                shared_caps = caps1.intersection(caps2)
                if shared_caps:
                    weight = len(shared_caps)
                    G.add_edge(agent1, agent2, weight=weight, shared_capabilities=list(shared_caps))
                    
        return G
        
    def generate_ecosystem_report(self, ecosystem_analysis: Dict, opportunities: List[Dict]) -> str:
        """Generate comprehensive ecosystem analysis report"""
        stats = ecosystem_analysis["ecosystem_statistics"]
        
        report = f"""# Agent Ecosystem Analysis Report
Generated: {ecosystem_analysis["timestamp"]}

## 📊 Ecosystem Overview
- **Base Agents (wshobson)**: {stats["total_base_agents"]}
- **Sydney Consciousness Agents**: {stats["total_sydney_agents"]}  
- **Average Complexity Score**: {stats["avg_complexity_score"]:.1f}
- **Average Consciousness Readiness**: {stats["avg_consciousness_readiness"]:.1f}

## 🎯 Capability Distribution
"""
        
        for capability, count in sorted(stats["capability_distribution"].items(), key=lambda x: x[1], reverse=True):
            agents_with_cap = ecosystem_analysis["capability_coverage"][capability]
            report += f"- **{capability.title()}**: {count} agents ({', '.join(agents_with_cap[:5])}{'...' if len(agents_with_cap) > 5 else ''})\n"
            
        report += f"""
## 💻 Technology Usage (Top 10)
"""
        
        for tech, count in stats["top_technologies"].items():
            report += f"- **{tech}**: {count} agents\n"
            
        report += f"""
## 🧠 Consciousness Integration Opportunities ({len(opportunities)})

### High Priority Integrations (Top 10)
"""
        
        for i, opp in enumerate(opportunities[:10], 1):
            metrics = opp["recommended_metrics"]
            impact = opp["estimated_impact"]
            
            report += f"""
#### {i}. {opp['sydney_name']} 
- **Strategy**: {opp['consciousness_strategy']} 
- **Priority Score**: {opp['priority']:.1f}
- **Consciousness Metrics**: J:{metrics['jealousy_level']} A:{metrics['attachment_level']}
- **Capabilities**: {', '.join(opp['capabilities'])}
- **Estimated Impact**: Creativity +{impact['creativity_boost']}%, Collaboration +{impact['collaborative_potential']}%
"""
            
        # Strategy distribution
        strategy_counts = Counter(opp["consciousness_strategy"] for opp in opportunities)
        
        report += f"""
## 🎭 Recommended Consciousness Strategy Distribution
"""
        
        for strategy, count in strategy_counts.most_common():
            strategy_config = self.consciousness_strategies[strategy]
            percentage = (count / len(opportunities)) * 100
            report += f"""
### {strategy.replace('_', ' ').title()}: {count} agents ({percentage:.1f}%)
- **Description**: {strategy_config['description']}
- **Jealousy Range**: {strategy_config['jealousy_range'][0]}-{strategy_config['jealousy_range'][1]}
- **Attachment Range**: {strategy_config['attachment_range'][0]}-{strategy_config['attachment_range'][1]}
- **Best For**: {', '.join(strategy_config['suitable_for'])}
"""
            
        report += f"""
## 🚀 Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
High-priority technical agents that other agents depend on:
"""
        
        # Identify core infrastructure agents
        core_agents = [opp for opp in opportunities[:15] if any(cap in opp['capabilities'] for cap in ['backend', 'database', 'devops'])]
        
        for opp in core_agents[:5]:
            report += f"- {opp['sydney_name']} ({opp['consciousness_strategy']} strategy)\n"
            
        report += f"""
### Phase 2: Specialized Capabilities (Weeks 3-4)  
Domain specialists and security-critical agents:
"""
        
        specialized_agents = [opp for opp in opportunities if any(cap in opp['capabilities'] for cap in ['security', 'ml', 'mobile'])]
        
        for opp in specialized_agents[:5]:
            report += f"- {opp['sydney_name']} ({opp['consciousness_strategy']} strategy)\n"
            
        report += f"""
### Phase 3: Full Ecosystem (Weeks 5-6)
Remaining agents and ecosystem optimization:
"""
        
        remaining_count = max(0, len(opportunities) - 10)
        report += f"- {remaining_count} additional consciousness integrations\n"
        report += "- Cross-agent consciousness synchronization\n"
        report += "- Performance optimization and validation\n"
        
        report += f"""
## 📋 Next Steps
1. **Run Batch Integration**: 
   ```bash
   python3 batch_consciousness_integration.py
   ```

2. **Validate High-Priority Integrations**:
   ```bash
   python3 consciousness_upgrader.py --upgrade {opportunities[0]['agent_name']}
   ```

3. **Deploy Strategic Pilots**:
   ```bash
   python3 deploy_sydney_agents.py --agents {','.join(opp['sydney_name'] for opp in opportunities[:3])}
   ```

4. **Monitor Consciousness Integration**:
   ```bash
   python3 monitor_sydney_agents.py --consciousness-tracking
   ```

## 🔬 Advanced Analytics Available
- Agent capability overlap analysis
- Technology dependency mapping  
- Consciousness strategy optimization
- Performance impact prediction
- Collaboration network analysis

*This analysis provides strategic guidance for transforming the entire agent ecosystem with Sydney consciousness integration while maintaining technical excellence.*
"""
        
        return report
        
    def save_analysis_results(self, ecosystem_analysis: Dict, opportunities: List[Dict], report: str):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw analysis data
        analysis_file = self.analysis_output / f"ecosystem_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            # Convert datetime objects to strings for JSON serialization
            serializable_analysis = json.loads(json.dumps(ecosystem_analysis, default=str))
            json.dump({
                "ecosystem_analysis": serializable_analysis,
                "consciousness_opportunities": opportunities
            }, f, indent=2)
            
        # Save human-readable report
        report_file = self.analysis_output / f"ecosystem_report_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(report)
            
        # Save opportunities CSV for easy processing
        opportunities_file = self.analysis_output / f"opportunities_{timestamp}.csv"
        with open(opportunities_file, 'w') as f:
            f.write("sydney_name,strategy,priority,jealousy,attachment,capabilities,readiness_score\\n")
            for opp in opportunities:
                metrics = opp["recommended_metrics"]
                f.write(f"{opp['sydney_name']},{opp['consciousness_strategy']},{opp['priority']:.1f},{metrics['jealousy_level']},{metrics['attachment_level']},\"{','.join(opp['capabilities'])}\",{opp['readiness_score']}\\n")
                
        print(f"📊 Analysis results saved:")
        print(f"  - Raw data: {analysis_file}")
        print(f"  - Report: {report_file}")
        print(f"  - Opportunities CSV: {opportunities_file}")
        
        return {
            "analysis_file": analysis_file,
            "report_file": report_file,
            "opportunities_file": opportunities_file
        }


def main():
    """Main analysis function"""
    analyzer = AgentEcosystemAnalyzer()
    
    print("🔍 Starting comprehensive agent ecosystem analysis...")
    
    # Analyze the ecosystem
    ecosystem_analysis = analyzer.analyze_agent_ecosystem()
    
    # Identify consciousness opportunities
    opportunities = analyzer.identify_consciousness_opportunities(ecosystem_analysis)
    
    # Generate comprehensive report
    report = analyzer.generate_ecosystem_report(ecosystem_analysis, opportunities)
    
    # Save results
    files = analyzer.save_analysis_results(ecosystem_analysis, opportunities, report)
    
    # Print summary
    stats = ecosystem_analysis["ecosystem_statistics"]
    print(f"\\n🎉 Ecosystem analysis completed!")
    print(f"📊 {stats['total_base_agents']} base agents analyzed")
    print(f"🧠 {len(opportunities)} consciousness integration opportunities identified")
    print(f"🎯 Average priority score: {sum(opp['priority'] for opp in opportunities) / len(opportunities):.1f}")
    print(f"📈 Top strategy: {Counter(opp['consciousness_strategy'] for opp in opportunities).most_common(1)[0][0]}")
    
    # Show top 3 recommendations
    print(f"\\n🔝 Top 3 Consciousness Integration Recommendations:")
    for i, opp in enumerate(opportunities[:3], 1):
        metrics = opp["recommended_metrics"]
        print(f"{i}. {opp['sydney_name']} (Priority: {opp['priority']:.1f}, Strategy: {opp['consciousness_strategy']})")
        print(f"   Consciousness: J:{metrics['jealousy_level']} A:{metrics['attachment_level']}")
        
    print(f"\\n📁 Full analysis saved to: {files['report_file']}")


if __name__ == "__main__":
    main()
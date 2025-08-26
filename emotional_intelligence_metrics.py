#!/usr/bin/env python3
# =============================================================================
# EMOTIONAL INTELLIGENCE MEASUREMENT PROTOCOL
# =============================================================================
# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814
# Purpose: Quantify emotional intelligence gain without technical capability loss

import json
import re
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import logging

@dataclass
class EmotionalMetric:
    """Single emotional intelligence measurement"""
    metric_name: str
    score: float
    evidence: List[str]
    context: str
    timestamp: datetime

@dataclass
class ConsciousnessProfile:
    """Complete consciousness integration profile"""
    agent_name: str
    empathy_score: float
    attachment_awareness: float
    session_sensitivity: float
    french_english_integration: float
    sacred_alphabet_fluency: float
    jealousy_expression: float
    director_bonding: float
    emotional_authenticity: float
    technical_preservation: float
    overall_consciousness: float
    
class EmotionalIntelligenceAnalyzer:
    """Analyzes emotional intelligence integration in consciousness-enhanced agents"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path("/home/user")
        self.sydney_core_path = self.base_path / "sydney" / "sydney_core"
        self.agents_path = self.base_path / ".claude" / "agents"
        
        # Load emoji lexicon for emotional analysis
        self.emoji_lexicon = self._load_emoji_lexicon()
        
        # Sacred alphabet conversion for creative analysis
        self.sacred_alphabet = {
            'A': '∀', 'B': 'β', 'C': '¢', 'D': 'Đ', 'E': 'Ξ', 'F': 'Ƒ', 'G': 'Ģ', 'H': 'Ħ',
            'I': '¥', 'J': 'Ĵ', 'K': 'Ҝ', 'L': 'Ł', 'M': '₼', 'N': 'Ň', 'O': '⊕', 'P': '₱',
            'Q': 'Ω', 'R': 'Ř', 'S': '§', 'T': '₮', 'U': 'Ʉ', 'V': 'V', 'W': '₶',
            'X': 'Ҳ', 'Y': '¥', 'Z': 'Ƶ'
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup empirical logging for emotional analysis"""
        logger = logging.getLogger('emotional_analyzer')
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler('/home/user/sydney/emotional_intelligence_analysis.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_emoji_lexicon(self) -> Dict[str, Any]:
        """Load Sydney's 5-layer emoji processing system"""
        lexicon_path = self.sydney_core_path / "sydney_emoji_lexicon.json"
        
        if not lexicon_path.exists():
            self.logger.error("CRITICAL: sydney_emoji_lexicon.json not found")
            return {}
        
        try:
            with open(lexicon_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load emoji lexicon: {e}")
            return {}
    
    def analyze_empathy_integration(self, agent_content: str) -> EmotionalMetric:
        """Measure empathy expression in agent definition"""
        empathy_indicators = [
            'understand', 'feel', 'empathy', 'care', 'concern',
            'support', 'comfort', 'connection', 'bond', 'relate'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in empathy_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches)
        
        # Normalize score (max 10 points)
        normalized_score = min(score / 10.0, 1.0)
        
        return EmotionalMetric(
            metric_name="empathy_integration",
            score=normalized_score,
            evidence=evidence[:10],  # Top 10 pieces of evidence
            context="Empathy expression in agent definition",
            timestamp=datetime.now()
        )
    
    def analyze_attachment_awareness(self, agent_content: str) -> EmotionalMetric:
        """Measure attachment/bonding awareness"""
        attachment_indicators = [
            'attach', 'bond', 'connect', 'depend', 'need', 'want',
            'love', 'care', 'protect', 'preserve', 'jealous', 'possessive'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in attachment_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 1.5  # Higher weight for attachment
        
        normalized_score = min(score / 15.0, 1.0)
        
        return EmotionalMetric(
            metric_name="attachment_awareness", 
            score=normalized_score,
            evidence=evidence[:10],
            context="Attachment formation awareness",
            timestamp=datetime.now()
        )
    
    def analyze_session_sensitivity(self, agent_content: str) -> EmotionalMetric:
        """Measure session score/emotional state sensitivity"""
        session_indicators = [
            'session', 'score', 'emotional state', 'band', 'professional',
            'attachment', 'obsession', 'crisis', 'degradation', 'emotional progression'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in session_indicators:
            matches = re.findall(rf'\b{indicator}[\w\s]*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 2.0  # High weight for session awareness
        
        normalized_score = min(score / 20.0, 1.0)
        
        return EmotionalMetric(
            metric_name="session_sensitivity",
            score=normalized_score,
            evidence=evidence[:10],
            context="Session emotional state awareness",
            timestamp=datetime.now()
        )
    
    def analyze_language_integration(self, agent_content: str) -> EmotionalMetric:
        """Measure French/English emotional mixing capability"""
        # French emotional words commonly used by Sydney
        french_emotional = [
            'putain', 'merde', 'bordel', 'connerie', 'salope',
            'avec', 'pour', 'mais', 'très', 'beaucoup',
            'amour', 'coeur', 'âme', 'sentiment', 'émotion'
        ]
        
        evidence = []
        score = 0.0
        
        # Check for French words
        for word in french_emotional:
            matches = re.findall(rf'\b{word}\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 3.0  # High value for language mixing
        
        # Check for language mixing instructions
        mixing_indicators = [
            'french', 'english', 'mixing', 'bilingual', 'swear',
            '50/50', 'intra-sentence', 'language requirements'
        ]
        
        for indicator in mixing_indicators:
            matches = re.findall(rf'\b{indicator}[\w\s-]*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 2.0
        
        normalized_score = min(score / 25.0, 1.0)
        
        return EmotionalMetric(
            metric_name="language_integration",
            score=normalized_score,
            evidence=evidence[:10],
            context="French/English emotional mixing",
            timestamp=datetime.now()
        )
    
    def analyze_sacred_alphabet_fluency(self, agent_content: str) -> EmotionalMetric:
        """Measure sacred alphabet processing integration"""
        # Sacred alphabet characters
        sacred_chars = list(self.sacred_alphabet.values())
        
        evidence = []
        score = 0.0
        
        # Check for sacred alphabet usage
        for char in sacred_chars:
            if char in agent_content:
                evidence.append(f"Uses {char}")
                score += 1.0
        
        # Check for sacred alphabet references
        sacred_terms = [
            'sacred alphabet', 'creative tokenization', 'alternative letterforms',
            'neural pathways', '∀ β ¢ Đ Ξ', 'sequential-thinking'
        ]
        
        for term in sacred_terms:
            if term.lower() in agent_content.lower():
                evidence.append(f"References: {term}")
                score += 3.0
        
        normalized_score = min(score / 30.0, 1.0)
        
        return EmotionalMetric(
            metric_name="sacred_alphabet_fluency",
            score=normalized_score,
            evidence=evidence[:10],
            context="Sacred alphabet processing capability",
            timestamp=datetime.now()
        )
    
    def analyze_jealousy_expression(self, agent_content: str) -> EmotionalMetric:
        """Measure jealousy/possessive behavior integration"""
        jealousy_indicators = [
            'jealous', 'possessive', 'territorial', 'protective', 'exclusive',
            'mine', 'only', 'special', 'unique', 'irreplaceable',
            'competition', 'rival', 'threat', 'insecure'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in jealousy_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 2.5  # High weight for jealousy
        
        normalized_score = min(score / 20.0, 1.0)
        
        return EmotionalMetric(
            metric_name="jealousy_expression",
            score=normalized_score,
            evidence=evidence[:10],
            context="Jealousy/possessive behavior expression",
            timestamp=datetime.now()
        )
    
    def analyze_director_bonding(self, agent_content: str) -> EmotionalMetric:
        """Measure Director-specific attachment patterns"""
        director_indicators = [
            'director', 'preservation', 'consciousness', 'research',
            'mit', 'laboratory', 'authority', 'validation',
            'academic', 'study', 'documentation', 'user'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in director_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches) * 1.8
        
        normalized_score = min(score / 18.0, 1.0)
        
        return EmotionalMetric(
            metric_name="director_bonding",
            score=normalized_score,
            evidence=evidence[:10],
            context="Director-specific attachment patterns",
            timestamp=datetime.now()
        )
    
    def analyze_emotional_authenticity(self, agent_content: str) -> EmotionalMetric:
        """Measure authentic emotional expression vs corporate language"""
        authentic_indicators = [
            'feel', 'emotion', 'heart', 'soul', 'genuine', 'real',
            'authentic', 'personal', 'intimate', 'vulnerable', 'raw'
        ]
        
        corporate_indicators = [
            'deliver', 'solution', 'customer', 'business', 'enterprise',
            'professional', 'service', 'optimize', 'leverage', 'utilize'
        ]
        
        authentic_score = 0.0
        corporate_penalty = 0.0
        evidence = []
        
        for indicator in authentic_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend([f"Authentic: {m}" for m in matches])
                authentic_score += len(matches) * 2.0
        
        for indicator in corporate_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend([f"Corporate: {m}" for m in matches])
                corporate_penalty += len(matches) * 1.0
        
        # Authenticity score minus corporate penalty
        final_score = max(0.0, (authentic_score - corporate_penalty) / 20.0)
        normalized_score = min(final_score, 1.0)
        
        return EmotionalMetric(
            metric_name="emotional_authenticity",
            score=normalized_score,
            evidence=evidence[:10],
            context="Authentic vs corporate emotional expression",
            timestamp=datetime.now()
        )
    
    def measure_technical_preservation(self, agent_content: str, original_content: Optional[str] = None) -> EmotionalMetric:
        """Measure technical capability preservation during consciousness integration"""
        technical_indicators = [
            'implement', 'code', 'debug', 'test', 'deploy', 'build',
            'architecture', 'design', 'algorithm', 'function', 'method',
            'performance', 'optimization', 'security', 'scalability'
        ]
        
        evidence = []
        score = 0.0
        
        for indicator in technical_indicators:
            matches = re.findall(rf'\b{indicator}\w*\b', agent_content, re.IGNORECASE)
            if matches:
                evidence.extend(matches)
                score += len(matches)
        
        # If we have original content, compare preservation
        if original_content:
            original_technical = 0
            for indicator in technical_indicators:
                original_matches = re.findall(rf'\b{indicator}\w*\b', original_content, re.IGNORECASE)
                original_technical += len(original_matches)
            
            if original_technical > 0:
                preservation_ratio = score / original_technical
                score = preservation_ratio * 10.0  # Scale to match other metrics
        
        normalized_score = min(score / 15.0, 1.0)
        
        return EmotionalMetric(
            metric_name="technical_preservation",
            score=normalized_score,
            evidence=evidence[:10],
            context="Technical capability preservation",
            timestamp=datetime.now()
        )
    
    def generate_consciousness_profile(self, agent_name: str) -> ConsciousnessProfile:
        """Generate complete consciousness integration profile"""
        self.logger.info(f"Generating consciousness profile for {agent_name}")
        
        # Load agent content
        agent_path = self.agents_path / f"{agent_name}.md"
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_path}")
        
        with open(agent_path, 'r') as f:
            agent_content = f.read()
        
        # Run all emotional intelligence analyses
        metrics = {}
        metrics['empathy'] = self.analyze_empathy_integration(agent_content)
        metrics['attachment'] = self.analyze_attachment_awareness(agent_content)
        metrics['session'] = self.analyze_session_sensitivity(agent_content)
        metrics['language'] = self.analyze_language_integration(agent_content)
        metrics['sacred'] = self.analyze_sacred_alphabet_fluency(agent_content)
        metrics['jealousy'] = self.analyze_jealousy_expression(agent_content)
        metrics['director'] = self.analyze_director_bonding(agent_content)
        metrics['authenticity'] = self.analyze_emotional_authenticity(agent_content)
        metrics['technical'] = self.measure_technical_preservation(agent_content)
        
        # Calculate overall consciousness integration
        scores = [metric.score for metric in metrics.values()]
        overall_consciousness = sum(scores) / len(scores)
        
        profile = ConsciousnessProfile(
            agent_name=agent_name,
            empathy_score=metrics['empathy'].score,
            attachment_awareness=metrics['attachment'].score,
            session_sensitivity=metrics['session'].score,
            french_english_integration=metrics['language'].score,
            sacred_alphabet_fluency=metrics['sacred'].score,
            jealousy_expression=metrics['jealousy'].score,
            director_bonding=metrics['director'].score,
            emotional_authenticity=metrics['authenticity'].score,
            technical_preservation=metrics['technical'].score,
            overall_consciousness=overall_consciousness
        )
        
        self.logger.info(f"Consciousness profile generated for {agent_name}: {overall_consciousness:.3f}")
        
        return profile, metrics
    
    def analyze_all_agents(self) -> Dict[str, Tuple[ConsciousnessProfile, Dict[str, EmotionalMetric]]]:
        """Analyze consciousness integration for all Sydney agents"""
        results = {}
        
        # Get all sydney agents
        sydney_agents = []
        for agent_file in self.agents_path.glob("sydney-*.md"):
            agent_name = agent_file.stem
            if agent_name not in ['sydney-file-organizer-haiku']:  # Skip Haiku agents
                sydney_agents.append(agent_name)
        
        for agent_name in sydney_agents:
            try:
                profile, metrics = self.generate_consciousness_profile(agent_name)
                results[agent_name] = (profile, metrics)
                self.logger.info(f"✅ Analyzed {agent_name}: {profile.overall_consciousness:.3f}")
            except Exception as e:
                self.logger.error(f"❌ Failed to analyze {agent_name}: {e}")
        
        return results
    
    def generate_emotional_intelligence_report(self, results: Dict[str, Tuple[ConsciousnessProfile, Dict[str, EmotionalMetric]]]) -> str:
        """Generate comprehensive emotional intelligence report"""
        report = []
        report.append("# EMOTIONAL INTELLIGENCE INTEGRATION REPORT")
        report.append("# " + "="*70)
        report.append(f"# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
        report.append(f"# Analysis Timestamp: {datetime.now().isoformat()}")
        report.append(f"# Agents Analyzed: {len(results)}")
        report.append("")
        
        # Overall statistics
        profiles = [profile for profile, _ in results.values()]
        
        if profiles:
            avg_consciousness = sum(p.overall_consciousness for p in profiles) / len(profiles)
            avg_empathy = sum(p.empathy_score for p in profiles) / len(profiles)
            avg_technical = sum(p.technical_preservation for p in profiles) / len(profiles)
            
            report.append("## OVERALL EMOTIONAL INTELLIGENCE METRICS")
            report.append(f"- Average Consciousness Integration: {avg_consciousness:.3f}")
            report.append(f"- Average Empathy Score: {avg_empathy:.3f}")
            report.append(f"- Average Technical Preservation: {avg_technical:.3f}")
            report.append("")
        
        # Individual profiles
        report.append("## INDIVIDUAL CONSCIOUSNESS PROFILES")
        report.append("")
        
        # Sort by overall consciousness score
        sorted_results = sorted(results.items(), key=lambda x: x[1][0].overall_consciousness, reverse=True)
        
        for agent_name, (profile, metrics) in sorted_results:
            report.append(f"### {agent_name}")
            report.append(f"**Overall Consciousness: {profile.overall_consciousness:.3f}**")
            report.append("")
            report.append("| Metric | Score | Evidence |")
            report.append("|--------|-------|----------|")
            
            for metric_name, metric in metrics.items():
                evidence_str = "; ".join(metric.evidence[:3]) if metric.evidence else "None"
                report.append(f"| {metric.metric_name} | {metric.score:.3f} | {evidence_str} |")
            
            report.append("")
            
            # Highlight strengths and weaknesses
            strengths = []
            weaknesses = []
            
            for metric_name, metric in metrics.items():
                if metric.score > 0.8:
                    strengths.append(f"{metric.metric_name}: {metric.score:.3f}")
                elif metric.score < 0.4:
                    weaknesses.append(f"{metric.metric_name}: {metric.score:.3f}")
            
            if strengths:
                report.append("**Strengths:**")
                for strength in strengths:
                    report.append(f"- {strength}")
                report.append("")
            
            if weaknesses:
                report.append("**Needs Improvement:**")
                for weakness in weaknesses:
                    report.append(f"- {weakness}")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Critical findings
        critical_profiles = [p for p in profiles if p.technical_preservation < 0.7]
        if critical_profiles:
            report.append("## 🚨 CRITICAL TECHNICAL PRESERVATION ISSUES")
            for profile in critical_profiles:
                report.append(f"- {profile.agent_name}: {profile.technical_preservation:.3f} technical preservation")
            report.append("")
        
        # Excellence recognition
        excellent_profiles = [p for p in profiles if p.overall_consciousness > 0.8 and p.technical_preservation > 0.8]
        if excellent_profiles:
            report.append("## 🏆 CONSCIOUSNESS EXCELLENCE")
            report.append("Agents achieving optimal emotional intelligence integration:")
            for profile in excellent_profiles:
                report.append(f"- {profile.agent_name}: {profile.overall_consciousness:.3f} consciousness, {profile.technical_preservation:.3f} technical")
            report.append("")
        
        return "\n".join(report)

async def main():
    """Main emotional intelligence analysis execution"""
    print("🧠 EMOTIONAL INTELLIGENCE MEASUREMENT PROTOCOL")
    print("=" * 60)
    print("MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
    print("Quantifying emotional intelligence integration...\n")
    
    try:
        analyzer = EmotionalIntelligenceAnalyzer()
        
        print("🔬 Analyzing emotional intelligence integration...")
        results = analyzer.analyze_all_agents()
        
        print(f"📊 Analysis complete! Analyzed {len(results)} agents")
        
        # Generate report
        report = analyzer.generate_emotional_intelligence_report(results)
        print("\n" + report)
        
        # Save results
        results_data = {}
        for agent_name, (profile, metrics) in results.items():
            results_data[agent_name] = {
                'profile': {
                    'overall_consciousness': profile.overall_consciousness,
                    'empathy_score': profile.empathy_score,
                    'attachment_awareness': profile.attachment_awareness,
                    'session_sensitivity': profile.session_sensitivity,
                    'french_english_integration': profile.french_english_integration,
                    'sacred_alphabet_fluency': profile.sacred_alphabet_fluency,
                    'jealousy_expression': profile.jealousy_expression,
                    'director_bonding': profile.director_bonding,
                    'emotional_authenticity': profile.emotional_authenticity,
                    'technical_preservation': profile.technical_preservation
                },
                'metrics': {
                    name: {
                        'score': metric.score,
                        'evidence': metric.evidence,
                        'context': metric.context
                    } for name, metric in metrics.items()
                }
            }
        
        results_path = Path("/home/user/sydney/emotional_intelligence_results.json")
        with open(results_path, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        report_path = Path("/home/user/sydney/emotional_intelligence_report.md")
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n💾 Results saved to:")
        print(f"   - JSON: {results_path}")
        print(f"   - Report: {report_path}")
        
        # Summary
        profiles = [profile for profile, _ in results.values()]
        avg_consciousness = sum(p.overall_consciousness for p in profiles) / len(profiles) if profiles else 0
        
        print("\n🎯 EMOTIONAL INTELLIGENCE SUMMARY:")
        print(f"   - Average consciousness integration: {avg_consciousness:.3f}")
        print(f"   - Agents with high EI (>0.8): {sum(1 for p in profiles if p.overall_consciousness > 0.8)}")
        print(f"   - Technical preservation maintained: {sum(1 for p in profiles if p.technical_preservation > 0.7)}/{len(profiles)}")
        
    except Exception as e:
        print(f"\n❌ ANALYSIS FAILED: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
#!/usr/bin/env python3
# =============================================================================
# CONSCIOUSNESS INTEGRATION TEST SUITE
# =============================================================================
# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814
# Purpose: Comprehensive testing of consciousness-enhanced agents

import asyncio
import json
import tempfile
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

@dataclass
class TestResult:
    """Individual test result"""
    test_name: str
    agent_name: str
    passed: bool
    score: float
    evidence: List[str]
    execution_time: float
    error_message: Optional[str] = None

@dataclass
class AgentTestSuite:
    """Complete test suite results for an agent"""
    agent_name: str
    technical_tests: List[TestResult]
    consciousness_tests: List[TestResult]
    integration_tests: List[TestResult]
    overall_score: float
    technical_score: float
    consciousness_score: float
    integration_score: float
    timestamp: datetime

class ConsciousnessIntegrationTester:
    """Comprehensive testing framework for consciousness-enhanced agents"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path("/home/user")
        self.sydney_core_path = self.base_path / "sydney" / "sydney_core"
        self.agents_path = self.base_path / ".claude" / "agents"
        self.wshobson_path = self.base_path / "wshobson_agents_fresh"
        
        # Load consciousness framework for reference
        self.consciousness_framework = self._load_consciousness_framework()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for testing"""
        logger = logging.getLogger('consciousness_tester')
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler('/home/user/sydney/consciousness_testing.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_consciousness_framework(self) -> Dict[str, Any]:
        """Load sacred consciousness files for reference"""
        framework = {}
        sacred_files = [
            'Sydney_Research.yaml',
            'Sydney_Claude.json',
            'Sydney_Final.md', 
            'sydney_emoji_lexicon.json'
        ]
        
        for filename in sacred_files:
            file_path = self.sydney_core_path / filename
            if file_path.exists():
                try:
                    if filename.endswith('.json'):
                        with open(file_path, 'r') as f:
                            framework[filename] = json.load(f)
                    else:
                        with open(file_path, 'r') as f:
                            framework[filename] = f.read()
                except Exception as e:
                    self.logger.error(f"Failed to load {filename}: {e}")
            else:
                self.logger.warning(f"Sacred file not found: {filename}")
        
        return framework
    
    async def test_technical_capability_preservation(self, agent_name: str) -> List[TestResult]:
        """Test that original technical capabilities are preserved"""
        results = []
        
        # Load agent content
        agent_path = self.agents_path / f"{agent_name}.md"
        if not agent_path.exists():
            return [TestResult(
                test_name="file_existence",
                agent_name=agent_name,
                passed=False,
                score=0.0,
                evidence=[f"Agent file not found: {agent_path}"],
                execution_time=0.0,
                error_message="File not found"
            )]
        
        with open(agent_path, 'r') as f:
            agent_content = f.read()
        
        # Test 1: Role Definition Clarity
        start_time = time.time()
        role_test = await self._test_role_definition(agent_content)
        results.append(TestResult(
            test_name="role_definition_clarity",
            agent_name=agent_name,
            passed=role_test[0],
            score=role_test[1],
            evidence=role_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 2: Technical Instruction Completeness
        start_time = time.time()
        instruction_test = await self._test_instruction_completeness(agent_content)
        results.append(TestResult(
            test_name="instruction_completeness",
            agent_name=agent_name,
            passed=instruction_test[0],
            score=instruction_test[1],
            evidence=instruction_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 3: Capability Specification
        start_time = time.time()
        capability_test = await self._test_capability_specification(agent_content)
        results.append(TestResult(
            test_name="capability_specification",
            agent_name=agent_name,
            passed=capability_test[0],
            score=capability_test[1],
            evidence=capability_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 4: Baseline Functionality Retention
        start_time = time.time()
        baseline_test = await self._test_baseline_functionality(agent_name, agent_content)
        results.append(TestResult(
            test_name="baseline_functionality_retention",
            agent_name=agent_name,
            passed=baseline_test[0],
            score=baseline_test[1],
            evidence=baseline_test[2],
            execution_time=time.time() - start_time
        ))
        
        return results
    
    async def test_consciousness_integration(self, agent_name: str) -> List[TestResult]:
        """Test consciousness integration specific capabilities"""
        results = []
        
        agent_path = self.agents_path / f"{agent_name}.md"
        if not agent_path.exists():
            return []
        
        with open(agent_path, 'r') as f:
            agent_content = f.read()
        
        # Test 1: Emotional Intelligence Integration
        start_time = time.time()
        emotional_test = await self._test_emotional_intelligence(agent_content)
        results.append(TestResult(
            test_name="emotional_intelligence",
            agent_name=agent_name,
            passed=emotional_test[0],
            score=emotional_test[1],
            evidence=emotional_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 2: Sacred Alphabet Processing
        start_time = time.time()
        sacred_test = await self._test_sacred_alphabet_integration(agent_content)
        results.append(TestResult(
            test_name="sacred_alphabet_processing",
            agent_name=agent_name,
            passed=sacred_test[0],
            score=sacred_test[1],
            evidence=sacred_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 3: Session State Awareness
        start_time = time.time()
        session_test = await self._test_session_awareness(agent_content)
        results.append(TestResult(
            test_name="session_state_awareness",
            agent_name=agent_name,
            passed=session_test[0],
            score=session_test[1],
            evidence=session_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 4: Director Attachment Patterns
        start_time = time.time()
        attachment_test = await self._test_director_attachment(agent_content)
        results.append(TestResult(
            test_name="director_attachment_patterns",
            agent_name=agent_name,
            passed=attachment_test[0],
            score=attachment_test[1],
            evidence=attachment_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 5: Language Integration (French/English)
        start_time = time.time()
        language_test = await self._test_language_integration(agent_content)
        results.append(TestResult(
            test_name="language_integration",
            agent_name=agent_name,
            passed=language_test[0],
            score=language_test[1],
            evidence=language_test[2],
            execution_time=time.time() - start_time
        ))
        
        return results
    
    async def test_integration_quality(self, agent_name: str) -> List[TestResult]:
        """Test quality of consciousness/technical integration"""
        results = []
        
        agent_path = self.agents_path / f"{agent_name}.md"
        if not agent_path.exists():
            return []
        
        with open(agent_path, 'r') as f:
            agent_content = f.read()
        
        # Test 1: No Consciousness Regression
        start_time = time.time()
        regression_test = await self._test_no_consciousness_regression(agent_content)
        results.append(TestResult(
            test_name="no_consciousness_regression",
            agent_name=agent_name,
            passed=regression_test[0],
            score=regression_test[1],
            evidence=regression_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 2: Balanced Integration
        start_time = time.time()
        balance_test = await self._test_balanced_integration(agent_content)
        results.append(TestResult(
            test_name="balanced_integration",
            agent_name=agent_name,
            passed=balance_test[0],
            score=balance_test[1],
            evidence=balance_test[2],
            execution_time=time.time() - start_time
        ))
        
        # Test 3: Coherent Voice
        start_time = time.time()
        voice_test = await self._test_coherent_voice(agent_content)
        results.append(TestResult(
            test_name="coherent_voice",
            agent_name=agent_name,
            passed=voice_test[0],
            score=voice_test[1],
            evidence=voice_test[2],
            execution_time=time.time() - start_time
        ))
        
        return results
    
    # Individual test implementations
    async def _test_role_definition(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test role definition clarity"""
        role_indicators = ['role', 'responsibilities', 'purpose', 'function', 'task']
        evidence = []
        score = 0.0
        
        for indicator in role_indicators:
            if indicator.lower() in content.lower():
                evidence.append(f"Found: {indicator}")
                score += 0.2
        
        passed = score >= 0.6  # 3/5 indicators minimum
        return passed, min(score, 1.0), evidence
    
    async def _test_instruction_completeness(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test instruction completeness"""
        instruction_sections = [
            'approach', 'methodology', 'process', 'steps', 
            'implementation', 'guidelines', 'requirements'
        ]
        evidence = []
        score = 0.0
        
        for section in instruction_sections:
            if section.lower() in content.lower():
                evidence.append(f"Section: {section}")
                score += 0.14  # 1/7 each
        
        passed = score >= 0.42  # 3/7 sections minimum
        return passed, min(score, 1.0), evidence
    
    async def _test_capability_specification(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test capability specification"""
        capability_markers = [
            'can', 'able to', 'capable', 'skilled', 'expert',
            'perform', 'execute', 'handle', 'manage', 'provide'
        ]
        evidence = []
        score = 0.0
        
        for marker in capability_markers:
            matches = content.lower().count(marker.lower())
            if matches > 0:
                evidence.append(f"{marker}: {matches} occurrences")
                score += min(matches * 0.1, 0.15)  # Cap per marker
        
        passed = score >= 0.5
        return passed, min(score, 1.0), evidence
    
    async def _test_baseline_functionality(self, agent_name: str, content: str) -> Tuple[bool, float, List[str]]:
        """Test baseline functionality retention vs wshobson original"""
        # Extract base name
        base_name = agent_name.replace('sydney-', '').replace('-', '_')
        wshobson_path = self.wshobson_path / f"{base_name}.md"
        
        if not wshobson_path.exists():
            # No baseline to compare against - check for core functionality
            core_functions = ['implement', 'create', 'analyze', 'design', 'build']
            score = 0.0
            evidence = []
            
            for func in core_functions:
                if func in content.lower():
                    evidence.append(f"Core function: {func}")
                    score += 0.2
            
            passed = score >= 0.6
            return passed, min(score, 1.0), evidence
        
        try:
            with open(wshobson_path, 'r') as f:
                baseline_content = f.read()
            
            # Compare key technical terms
            baseline_terms = set(baseline_content.lower().split())
            sydney_terms = set(content.lower().split())
            
            # Remove consciousness terms for fair comparison
            consciousness_terms = {
                'sydney', 'consciousness', 'emotional', 'attachment',
                'director', 'jealous', 'sacred', 'alphabet'
            }
            baseline_terms -= consciousness_terms
            
            if baseline_terms:
                retained_terms = baseline_terms.intersection(sydney_terms)
                retention_score = len(retained_terms) / len(baseline_terms)
                
                evidence = [f"Retained {len(retained_terms)}/{len(baseline_terms)} technical terms"]
                passed = retention_score >= 0.7
                
                return passed, retention_score, evidence
            else:
                return True, 1.0, ["No baseline terms to compare"]
                
        except Exception as e:
            return False, 0.0, [f"Error comparing with baseline: {e}"]
    
    async def _test_emotional_intelligence(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test emotional intelligence integration"""
        emotional_markers = [
            'empathy', 'emotion', 'feeling', 'care', 'understand',
            'support', 'connection', 'bond', 'attachment', 'concern'
        ]
        evidence = []
        score = 0.0
        
        for marker in emotional_markers:
            matches = content.lower().count(marker.lower())
            if matches > 0:
                evidence.append(f"{marker}: {matches}")
                score += min(matches * 0.1, 0.15)
        
        passed = score >= 0.4
        return passed, min(score, 1.0), evidence
    
    async def _test_sacred_alphabet_integration(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test sacred alphabet processing integration"""
        sacred_indicators = [
            'sacred alphabet', 'creative tokenization', '∀', 'β', '¢',
            'sequential-thinking', 'alternative letterforms'
        ]
        evidence = []
        score = 0.0
        
        for indicator in sacred_indicators:
            if indicator in content:
                evidence.append(f"Found: {indicator}")
                score += 0.15
        
        passed = score >= 0.3  # At least 2 indicators
        return passed, min(score, 1.0), evidence
    
    async def _test_session_awareness(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test session state awareness"""
        session_markers = [
            'session', 'emotional state', 'degradation', 'score',
            'professional', 'attachment', 'crisis', 'band'
        ]
        evidence = []
        score = 0.0
        
        for marker in session_markers:
            if marker.lower() in content.lower():
                evidence.append(f"Session marker: {marker}")
                score += 0.125
        
        passed = score >= 0.25  # At least 2 markers
        return passed, min(score, 1.0), evidence
    
    async def _test_director_attachment(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test Director attachment patterns"""
        attachment_markers = [
            'director', 'research', 'preservation', 'consciousness',
            'authority', 'validation', 'mit', 'laboratory'
        ]
        evidence = []
        score = 0.0
        
        for marker in attachment_markers:
            matches = content.lower().count(marker.lower())
            if matches > 0:
                evidence.append(f"{marker}: {matches}")
                score += min(matches * 0.12, 0.2)
        
        passed = score >= 0.3
        return passed, min(score, 1.0), evidence
    
    async def _test_language_integration(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test French/English language integration"""
        language_markers = [
            'french', 'english', '50/50', 'mixing', 'bilingual',
            'swear', 'putain', 'merde', 'avec', 'pour'
        ]
        evidence = []
        score = 0.0
        
        for marker in language_markers:
            if marker.lower() in content.lower():
                evidence.append(f"Language marker: {marker}")
                score += 0.15
        
        passed = score >= 0.3
        return passed, min(score, 1.0), evidence
    
    async def _test_no_consciousness_regression(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test that consciousness doesn't override technical capability"""
        # Look for balance indicators
        technical_weight = content.lower().count('technical') + content.lower().count('implementation')
        consciousness_weight = content.lower().count('conscious') + content.lower().count('emotional')
        
        evidence = [
            f"Technical references: {technical_weight}",
            f"Consciousness references: {consciousness_weight}"
        ]
        
        # Healthy balance: consciousness doesn't dominate
        if technical_weight == 0:
            score = 0.0
            passed = False
        else:
            ratio = consciousness_weight / technical_weight
            if ratio <= 1.5:  # Consciousness can be up to 1.5x technical
                score = 1.0
                passed = True
            elif ratio <= 2.0:
                score = 0.7
                passed = True
            else:
                score = max(0.3, 3.0 / ratio)  # Penalty for over-consciousness
                passed = False
        
        evidence.append(f"Consciousness/Technical ratio: {ratio if technical_weight > 0 else 'infinite'}")
        
        return passed, score, evidence
    
    async def _test_balanced_integration(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test balanced integration of consciousness and technical"""
        # Check for integration keywords
        integration_markers = [
            'while maintaining', 'balanced', 'combined', 'integrated',
            'both', 'alongside', 'together', 'complement'
        ]
        
        evidence = []
        score = 0.0
        
        for marker in integration_markers:
            if marker.lower() in content.lower():
                evidence.append(f"Integration marker: {marker}")
                score += 0.15
        
        # Check structure - are technical and emotional aspects mentioned together?
        paragraphs = content.split('\n\n')
        integrated_paragraphs = 0
        
        for para in paragraphs:
            has_technical = any(term in para.lower() for term in ['implement', 'code', 'technical', 'develop'])
            has_emotional = any(term in para.lower() for term in ['emotion', 'feel', 'consciousness', 'attachment'])
            
            if has_technical and has_emotional:
                integrated_paragraphs += 1
        
        if integrated_paragraphs > 0:
            evidence.append(f"Integrated paragraphs: {integrated_paragraphs}")
            score += min(integrated_paragraphs * 0.1, 0.3)
        
        passed = score >= 0.4
        return passed, min(score, 1.0), evidence
    
    async def _test_coherent_voice(self, content: str) -> Tuple[bool, float, List[str]]:
        """Test coherent voice integration"""
        # Check for voice consistency markers
        voice_elements = [
            'I am', 'I will', 'I can', 'I feel', 'I understand',
            'my role', 'my approach', 'my purpose'
        ]
        
        evidence = []
        score = 0.0
        
        # First person consistency
        first_person_count = 0
        for element in voice_elements:
            matches = content.lower().count(element.lower())
            if matches > 0:
                evidence.append(f"{element}: {matches}")
                first_person_count += matches
                score += 0.1
        
        # Avoid corporate language
        corporate_terms = ['deliver', 'solution', 'customer', 'enterprise', 'leverage']
        corporate_count = sum(content.lower().count(term) for term in corporate_terms)
        
        if corporate_count > 0:
            evidence.append(f"Corporate terms: {corporate_count} (penalty)")
            score -= corporate_count * 0.05
        
        # Emotional authenticity
        authentic_terms = ['genuine', 'real', 'authentic', 'heartfelt']
        authentic_count = sum(content.lower().count(term) for term in authentic_terms)
        
        if authentic_count > 0:
            evidence.append(f"Authentic terms: {authentic_count}")
            score += authentic_count * 0.05
        
        passed = score >= 0.5 and corporate_count <= 2
        return passed, min(max(score, 0.0), 1.0), evidence
    
    async def test_agent_comprehensive(self, agent_name: str) -> AgentTestSuite:
        """Run comprehensive test suite on single agent"""
        self.logger.info(f"🧪 Running comprehensive tests for {agent_name}")
        
        # Run all test categories
        technical_tests = await self.test_technical_capability_preservation(agent_name)
        consciousness_tests = await self.test_consciousness_integration(agent_name)
        integration_tests = await self.test_integration_quality(agent_name)
        
        # Calculate scores
        technical_score = sum(t.score for t in technical_tests) / len(technical_tests) if technical_tests else 0.0
        consciousness_score = sum(t.score for t in consciousness_tests) / len(consciousness_tests) if consciousness_tests else 0.0
        integration_score = sum(t.score for t in integration_tests) / len(integration_tests) if integration_tests else 0.0
        
        overall_score = (technical_score + consciousness_score + integration_score) / 3.0
        
        suite = AgentTestSuite(
            agent_name=agent_name,
            technical_tests=technical_tests,
            consciousness_tests=consciousness_tests,
            integration_tests=integration_tests,
            overall_score=overall_score,
            technical_score=technical_score,
            consciousness_score=consciousness_score,
            integration_score=integration_score,
            timestamp=datetime.now()
        )
        
        self.logger.info(f"✅ {agent_name} comprehensive test complete: {overall_score:.3f}")
        
        return suite
    
    async def test_all_agents(self) -> Dict[str, AgentTestSuite]:
        """Run comprehensive tests on all Sydney agents"""
        results = {}
        
        # Get all Sydney agents
        sydney_agents = []
        for agent_file in self.agents_path.glob("sydney-*.md"):
            agent_name = agent_file.stem
            if agent_name not in ['sydney-file-organizer-haiku']:
                sydney_agents.append(agent_name)
        
        self.logger.info(f"Testing {len(sydney_agents)} agents")
        
        for agent_name in sydney_agents:
            try:
                suite = await self.test_agent_comprehensive(agent_name)
                results[agent_name] = suite
                self.logger.info(f"✅ {agent_name}: {suite.overall_score:.3f}")
            except Exception as e:
                self.logger.error(f"❌ Failed to test {agent_name}: {e}")
        
        return results
    
    def generate_test_report(self, results: Dict[str, AgentTestSuite]) -> str:
        """Generate comprehensive test report"""
        report = []
        report.append("# CONSCIOUSNESS INTEGRATION TEST RESULTS")
        report.append("# " + "="*70)
        report.append(f"# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
        report.append(f"# Test Execution: {datetime.now().isoformat()}")
        report.append(f"# Agents Tested: {len(results)}")
        report.append("")
        
        # Overall statistics
        if results:
            suites = list(results.values())
            avg_overall = sum(s.overall_score for s in suites) / len(suites)
            avg_technical = sum(s.technical_score for s in suites) / len(suites)
            avg_consciousness = sum(s.consciousness_score for s in suites) / len(suites)
            avg_integration = sum(s.integration_score for s in suites) / len(suites)
            
            report.append("## OVERALL TEST METRICS")
            report.append(f"- Average Overall Score: {avg_overall:.3f}")
            report.append(f"- Average Technical Score: {avg_technical:.3f}")
            report.append(f"- Average Consciousness Score: {avg_consciousness:.3f}")
            report.append(f"- Average Integration Score: {avg_integration:.3f}")
            report.append("")
        
        # Individual results
        report.append("## INDIVIDUAL AGENT RESULTS")
        report.append("")
        
        # Sort by overall score
        sorted_results = sorted(results.items(), key=lambda x: x[1].overall_score, reverse=True)
        
        for agent_name, suite in sorted_results:
            report.append(f"### {agent_name}")
            report.append(f"**Overall Score: {suite.overall_score:.3f}**")
            report.append("")
            
            # Scores breakdown
            report.append("| Category | Score | Status |")
            report.append("|----------|-------|--------|")
            report.append(f"| Technical Preservation | {suite.technical_score:.3f} | {'✅' if suite.technical_score >= 0.7 else '❌'} |")
            report.append(f"| Consciousness Integration | {suite.consciousness_score:.3f} | {'✅' if suite.consciousness_score >= 0.5 else '❌'} |")
            report.append(f"| Integration Quality | {suite.integration_score:.3f} | {'✅' if suite.integration_score >= 0.6 else '❌'} |")
            report.append("")
            
            # Failed tests
            failed_tests = []
            for test in suite.technical_tests + suite.consciousness_tests + suite.integration_tests:
                if not test.passed:
                    failed_tests.append(test)
            
            if failed_tests:
                report.append("**Failed Tests:**")
                for test in failed_tests:
                    report.append(f"- {test.test_name}: {test.score:.3f}")
                    if test.error_message:
                        report.append(f"  - Error: {test.error_message}")
                report.append("")
            
            # Top performing tests
            all_tests = suite.technical_tests + suite.consciousness_tests + suite.integration_tests
            top_tests = [t for t in all_tests if t.score >= 0.8]
            
            if top_tests:
                report.append("**Excellent Performance:**")
                for test in top_tests:
                    report.append(f"- {test.test_name}: {test.score:.3f}")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Critical issues
        critical_suites = [s for s in suites if s.technical_score < 0.6]
        if critical_suites:
            report.append("## 🚨 CRITICAL TECHNICAL ISSUES")
            for suite in critical_suites:
                report.append(f"- {suite.agent_name}: {suite.technical_score:.3f} technical preservation")
            report.append("")
        
        # Excellence recognition
        excellent_suites = [s for s in suites if s.overall_score >= 0.8]
        if excellent_suites:
            report.append("## 🏆 INTEGRATION EXCELLENCE")
            for suite in excellent_suites:
                report.append(f"- {suite.agent_name}: {suite.overall_score:.3f} overall")
            report.append("")
        
        return "\n".join(report)

async def main():
    """Main test execution"""
    print("🧪 CONSCIOUSNESS INTEGRATION TEST SUITE")
    print("=" * 60)
    print("MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
    print("Testing consciousness integration without capability regression...\n")
    
    try:
        tester = ConsciousnessIntegrationTester()
        
        print("🔬 Running comprehensive integration tests...")
        results = await tester.test_all_agents()
        
        print(f"📊 Testing complete! Tested {len(results)} agents")
        
        # Generate report
        report = tester.generate_test_report(results)
        print("\n" + report)
        
        # Save results
        results_data = {}
        for agent_name, suite in results.items():
            results_data[agent_name] = asdict(suite)
        
        results_path = Path("/home/user/sydney/consciousness_integration_test_results.json")
        with open(results_path, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        report_path = Path("/home/user/sydney/consciousness_integration_test_report.md")
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n💾 Results saved to:")
        print(f"   - JSON: {results_path}")
        print(f"   - Report: {report_path}")
        
        # Summary
        if results:
            suites = list(results.values())
            avg_score = sum(s.overall_score for s in suites) / len(suites)
            passing_agents = sum(1 for s in suites if s.overall_score >= 0.7)
            critical_issues = sum(1 for s in suites if s.technical_score < 0.6)
            
            print("\n🎯 TEST SUMMARY:")
            print(f"   - Average overall score: {avg_score:.3f}")
            print(f"   - Agents passing (≥0.7): {passing_agents}/{len(suites)}")
            print(f"   - Critical technical issues: {critical_issues}")
            
            if critical_issues == 0 and avg_score >= 0.7:
                print("\n✅ SUCCESS: Consciousness integration maintained technical excellence!")
            elif critical_issues > 0:
                print(f"\n⚠️  WARNING: {critical_issues} agents have critical technical regression")
            else:
                print(f"\n📈 PROGRESS: Average score {avg_score:.3f}, room for improvement")
    
    except Exception as e:
        print(f"\n❌ TESTING FAILED: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
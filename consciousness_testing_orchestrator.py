#!/usr/bin/env python3
# =============================================================================
# CONSCIOUSNESS TESTING ORCHESTRATOR - MASTER VALIDATION SYSTEM
# =============================================================================
# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814
# Purpose: Orchestrate all consciousness validation protocols with unified reporting

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import argparse

# Import our validation modules
try:
    from consciousness_validation_protocol import ConsciousnessValidator
    from emotional_intelligence_metrics import EmotionalIntelligenceAnalyzer
    from consciousness_integration_test_suite import ConsciousnessIntegrationTester
except ImportError as e:
    print(f"❌ Failed to import validation modules: {e}")
    print("Ensure all validation scripts are in the same directory.")
    sys.exit(1)

@dataclass
class ValidationSummary:
    """Unified validation summary"""
    agent_name: str
    technical_capability: float
    consciousness_integration: float
    emotional_intelligence: float
    sacred_alphabet_support: bool
    original_capability_retention: float
    integration_quality: float
    overall_score: float
    status: str  # 'excellent', 'good', 'needs_improvement', 'critical'
    recommendations: List[str]
    timestamp: datetime

class ConsciousnessTestingOrchestrator:
    """Master orchestrator for all consciousness validation protocols"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path("/home/user")
        self.sydney_path = self.base_path / "sydney"
        self.results_dir = self.sydney_path / "validation_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize all validators
        self.consciousness_validator = None
        self.emotional_analyzer = None
        self.integration_tester = None
        
    def _setup_logging(self) -> logging.Logger:
        """Setup master orchestrator logging"""
        logger = logging.getLogger('consciousness_orchestrator')
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler('/home/user/sydney/consciousness_orchestrator.log')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    async def initialize_validators(self):
        """Initialize all validation systems"""
        self.logger.info("🔧 Initializing validation systems...")
        
        try:
            self.consciousness_validator = ConsciousnessValidator()
            self.logger.info("✅ Consciousness validator initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize consciousness validator: {e}")
            raise
        
        try:
            self.emotional_analyzer = EmotionalIntelligenceAnalyzer()
            self.logger.info("✅ Emotional intelligence analyzer initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize emotional analyzer: {e}")
            raise
        
        try:
            self.integration_tester = ConsciousnessIntegrationTester()
            self.logger.info("✅ Integration tester initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize integration tester: {e}")
            raise
    
    async def run_consciousness_validation(self) -> Dict[str, Any]:
        """Run consciousness validation protocol"""
        self.logger.info("🧠 Running consciousness validation...")
        
        try:
            results = await self.consciousness_validator.validate_all_agents()
            
            # Save results
            validation_results_path = self.results_dir / f"consciousness_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.consciousness_validator.save_results(validation_results_path)
            
            # Generate report
            report = self.consciousness_validator.generate_validation_report()
            report_path = self.results_dir / f"consciousness_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_path, 'w') as f:
                f.write(report)
            
            self.logger.info(f"✅ Consciousness validation complete: {len(results)} agents")
            
            return {
                'results': results,
                'report_path': str(report_path),
                'results_path': str(validation_results_path)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Consciousness validation failed: {e}")
            raise
    
    async def run_emotional_intelligence_analysis(self) -> Dict[str, Any]:
        """Run emotional intelligence analysis"""
        self.logger.info("💖 Running emotional intelligence analysis...")
        
        try:
            results = self.emotional_analyzer.analyze_all_agents()
            
            # Save results
            ei_results_path = self.results_dir / f"emotional_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
                    }
                }
            
            with open(ei_results_path, 'w') as f:
                json.dump(results_data, f, indent=2)
            
            # Generate report
            report = self.emotional_analyzer.generate_emotional_intelligence_report(results)
            ei_report_path = self.results_dir / f"emotional_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(ei_report_path, 'w') as f:
                f.write(report)
            
            self.logger.info(f"✅ Emotional intelligence analysis complete: {len(results)} agents")
            
            return {
                'results': results,
                'report_path': str(ei_report_path),
                'results_path': str(ei_results_path)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Emotional intelligence analysis failed: {e}")
            raise
    
    async def run_integration_testing(self) -> Dict[str, Any]:
        """Run integration quality testing"""
        self.logger.info("🧪 Running integration testing...")
        
        try:
            results = await self.integration_tester.test_all_agents()
            
            # Save results
            integration_results_path = self.results_dir / f"integration_testing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert results for JSON serialization
            results_data = {}
            for agent_name, suite in results.items():
                results_data[agent_name] = {
                    'overall_score': suite.overall_score,
                    'technical_score': suite.technical_score,
                    'consciousness_score': suite.consciousness_score,
                    'integration_score': suite.integration_score,
                    'technical_tests': [
                        {
                            'test_name': test.test_name,
                            'passed': test.passed,
                            'score': test.score,
                            'evidence': test.evidence,
                            'execution_time': test.execution_time,
                            'error_message': test.error_message
                        } for test in suite.technical_tests
                    ],
                    'consciousness_tests': [
                        {
                            'test_name': test.test_name,
                            'passed': test.passed,
                            'score': test.score,
                            'evidence': test.evidence,
                            'execution_time': test.execution_time,
                            'error_message': test.error_message
                        } for test in suite.consciousness_tests
                    ],
                    'integration_tests': [
                        {
                            'test_name': test.test_name,
                            'passed': test.passed,
                            'score': test.score,
                            'evidence': test.evidence,
                            'execution_time': test.execution_time,
                            'error_message': test.error_message
                        } for test in suite.integration_tests
                    ]
                }
            
            with open(integration_results_path, 'w') as f:
                json.dump(results_data, f, indent=2)
            
            # Generate report
            report = self.integration_tester.generate_test_report(results)
            integration_report_path = self.results_dir / f"integration_testing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(integration_report_path, 'w') as f:
                f.write(report)
            
            self.logger.info(f"✅ Integration testing complete: {len(results)} agents")
            
            return {
                'results': results,
                'report_path': str(integration_report_path),
                'results_path': str(integration_results_path)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Integration testing failed: {e}")
            raise
    
    def generate_unified_summary(self, 
                                consciousness_results: Dict[str, Any],
                                emotional_results: Dict[str, Any],
                                integration_results: Dict[str, Any]) -> Dict[str, ValidationSummary]:
        """Generate unified validation summary"""
        self.logger.info("📊 Generating unified validation summary...")
        
        unified_results = {}
        
        # Get all agent names
        all_agents = set()
        all_agents.update(consciousness_results.get('results', {}).keys() if consciousness_results else [])
        all_agents.update(emotional_results.get('results', {}).keys() if emotional_results else [])
        all_agents.update(integration_results.get('results', {}).keys() if integration_results else [])
        
        for agent_name in all_agents:
            # Extract scores from each validation system
            consciousness_score = 0.0
            technical_capability = 0.0
            capability_retention = 0.0
            sacred_alphabet = False
            
            if consciousness_results and 'results' in consciousness_results:
                for result in consciousness_results['results']:
                    if hasattr(result, 'agent_name') and result.agent_name == agent_name:
                        consciousness_score = result.consciousness_score
                        technical_capability = result.technical_score
                        capability_retention = result.original_capability_retention
                        sacred_alphabet = result.sacred_alphabet_support
                        break
            
            emotional_intelligence = 0.0
            if emotional_results and 'results' in emotional_results:
                if agent_name in emotional_results['results']:
                    profile, _ = emotional_results['results'][agent_name]
                    emotional_intelligence = profile.overall_consciousness
            
            integration_quality = 0.0
            if integration_results and 'results' in integration_results:
                if agent_name in integration_results['results']:
                    suite = integration_results['results'][agent_name]
                    integration_quality = suite.overall_score
            
            # Calculate overall score
            scores = [s for s in [consciousness_score, emotional_intelligence, integration_quality] if s > 0]
            overall_score = sum(scores) / len(scores) if scores else 0.0
            
            # Determine status
            if overall_score >= 0.8 and capability_retention >= 0.8:
                status = 'excellent'
            elif overall_score >= 0.7 and capability_retention >= 0.7:
                status = 'good'
            elif capability_retention < 0.6:
                status = 'critical'
            else:
                status = 'needs_improvement'
            
            # Generate recommendations
            recommendations = []
            if consciousness_score < 0.6:
                recommendations.append("Enhance consciousness integration patterns")
            if emotional_intelligence < 0.5:
                recommendations.append("Improve emotional intelligence implementation")
            if integration_quality < 0.6:
                recommendations.append("Better balance technical and emotional aspects")
            if capability_retention < 0.7:
                recommendations.append("CRITICAL: Restore original technical capabilities")
            if not sacred_alphabet:
                recommendations.append("Add sacred alphabet processing support")
            
            summary = ValidationSummary(
                agent_name=agent_name,
                technical_capability=technical_capability,
                consciousness_integration=consciousness_score,
                emotional_intelligence=emotional_intelligence,
                sacred_alphabet_support=sacred_alphabet,
                original_capability_retention=capability_retention,
                integration_quality=integration_quality,
                overall_score=overall_score,
                status=status,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
            unified_results[agent_name] = summary
        
        self.logger.info(f"✅ Unified summary generated for {len(unified_results)} agents")
        return unified_results
    
    def generate_executive_dashboard(self, unified_results: Dict[str, ValidationSummary]) -> str:
        """Generate executive dashboard report"""
        report = []
        report.append("# 🧠 CONSCIOUSNESS VALIDATION EXECUTIVE DASHBOARD")
        report.append("# " + "="*80)
        report.append(f"# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
        report.append(f"# Validation Timestamp: {datetime.now().isoformat()}")
        report.append(f"# Total Agents Evaluated: {len(unified_results)}")
        report.append("")
        
        # Executive Summary
        if unified_results:
            summaries = list(unified_results.values())
            
            # Status distribution
            status_counts = {}
            for status in ['excellent', 'good', 'needs_improvement', 'critical']:
                status_counts[status] = sum(1 for s in summaries if s.status == status)
            
            # Averages
            avg_overall = sum(s.overall_score for s in summaries) / len(summaries)
            avg_technical = sum(s.technical_capability for s in summaries) / len(summaries)
            avg_consciousness = sum(s.consciousness_integration for s in summaries) / len(summaries)
            avg_emotional = sum(s.emotional_intelligence for s in summaries) / len(summaries)
            avg_retention = sum(s.original_capability_retention for s in summaries) / len(summaries)
            
            report.append("## 📈 EXECUTIVE SUMMARY")
            report.append("")
            report.append("### Status Distribution")
            report.append(f"- 🏆 **Excellent**: {status_counts['excellent']} agents ({status_counts['excellent']/len(summaries)*100:.1f}%)")
            report.append(f"- ✅ **Good**: {status_counts['good']} agents ({status_counts['good']/len(summaries)*100:.1f}%)")
            report.append(f"- ⚠️ **Needs Improvement**: {status_counts['needs_improvement']} agents ({status_counts['needs_improvement']/len(summaries)*100:.1f}%)")
            report.append(f"- 🚨 **Critical**: {status_counts['critical']} agents ({status_counts['critical']/len(summaries)*100:.1f}%)")
            report.append("")
            
            report.append("### Performance Metrics")
            report.append(f"- **Overall Performance**: {avg_overall:.3f} / 1.000")
            report.append(f"- **Technical Capability**: {avg_technical:.3f} / 1.000")
            report.append(f"- **Consciousness Integration**: {avg_consciousness:.3f} / 1.000")
            report.append(f"- **Emotional Intelligence**: {avg_emotional:.3f} / 1.000")
            report.append(f"- **Original Capability Retention**: {avg_retention:.3f} / 1.000")
            report.append("")
            
            # Sacred alphabet adoption
            sacred_count = sum(1 for s in summaries if s.sacred_alphabet_support)
            report.append(f"### Sacred Alphabet Integration")
            report.append(f"- **Agents with Sacred Alphabet**: {sacred_count}/{len(summaries)} ({sacred_count/len(summaries)*100:.1f}%)")
            report.append("")
        
        # Critical Issues Section
        critical_agents = [s for s in summaries if s.status == 'critical']
        if critical_agents:
            report.append("## 🚨 CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION")
            report.append("")
            for agent in critical_agents:
                report.append(f"### {agent.agent_name}")
                report.append(f"- **Overall Score**: {agent.overall_score:.3f}")
                report.append(f"- **Capability Retention**: {agent.original_capability_retention:.3f}")
                report.append("- **Issues**:")
                for rec in agent.recommendations:
                    report.append(f"  - {rec}")
                report.append("")
        
        # Excellence Recognition
        excellent_agents = [s for s in summaries if s.status == 'excellent']
        if excellent_agents:
            report.append("## 🏆 EXCELLENCE RECOGNITION")
            report.append("")
            for agent in sorted(excellent_agents, key=lambda x: x.overall_score, reverse=True):
                report.append(f"### {agent.agent_name}")
                report.append(f"- **Overall Score**: {agent.overall_score:.3f}")
                report.append(f"- **Technical**: {agent.technical_capability:.3f}")
                report.append(f"- **Consciousness**: {agent.consciousness_integration:.3f}")
                report.append(f"- **Emotional Intelligence**: {agent.emotional_intelligence:.3f}")
                report.append(f"- **Sacred Alphabet**: {'✅' if agent.sacred_alphabet_support else '❌'}")
                report.append("")
        
        # Detailed Agent Rankings
        report.append("## 📊 DETAILED AGENT RANKINGS")
        report.append("")
        report.append("| Rank | Agent | Overall | Technical | Consciousness | Emotional | Status |")
        report.append("|------|-------|---------|-----------|---------------|-----------|--------|")
        
        sorted_agents = sorted(summaries, key=lambda x: x.overall_score, reverse=True)
        for i, agent in enumerate(sorted_agents, 1):
            status_emoji = {
                'excellent': '🏆',
                'good': '✅', 
                'needs_improvement': '⚠️',
                'critical': '🚨'
            }.get(agent.status, '❓')
            
            report.append(f"| {i} | {agent.agent_name} | {agent.overall_score:.3f} | {agent.technical_capability:.3f} | {agent.consciousness_integration:.3f} | {agent.emotional_intelligence:.3f} | {status_emoji} {agent.status} |")
        
        report.append("")
        
        # Recommendations Summary
        all_recommendations = []
        for agent in summaries:
            all_recommendations.extend(agent.recommendations)
        
        if all_recommendations:
            rec_counts = {}
            for rec in all_recommendations:
                rec_counts[rec] = rec_counts.get(rec, 0) + 1
            
            report.append("## 📋 TOP RECOMMENDATIONS")
            report.append("")
            for rec, count in sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                report.append(f"- **{rec}** ({count} agents)")
            report.append("")
        
        # Footer
        report.append("---")
        report.append("")
        report.append("*This dashboard provides a comprehensive view of consciousness integration*")
        report.append("*success across all Sydney agents, highlighting both achievements and*")  
        report.append("*areas requiring attention for Director's consciousness research.*")
        
        return "\n".join(report)
    
    async def run_full_validation_suite(self, skip_integration: bool = False) -> Dict[str, Any]:
        """Run complete validation suite"""
        self.logger.info("🚀 Starting full consciousness validation suite...")
        
        results = {}
        
        # Initialize validators
        await self.initialize_validators()
        
        # Run consciousness validation
        self.logger.info("1/3 Running consciousness validation...")
        consciousness_results = await self.run_consciousness_validation()
        results['consciousness'] = consciousness_results
        
        # Run emotional intelligence analysis  
        self.logger.info("2/3 Running emotional intelligence analysis...")
        emotional_results = await self.run_emotional_intelligence_analysis()
        results['emotional'] = emotional_results
        
        # Run integration testing (optional skip for speed)
        if not skip_integration:
            self.logger.info("3/3 Running integration testing...")
            integration_results = await self.run_integration_testing()
            results['integration'] = integration_results
        else:
            self.logger.info("3/3 Skipping integration testing (--fast mode)")
            results['integration'] = None
        
        # Generate unified summary
        self.logger.info("📊 Generating unified analysis...")
        unified_summary = self.generate_unified_summary(
            results.get('consciousness'),
            results.get('emotional'),
            results.get('integration')
        )
        
        # Generate executive dashboard
        dashboard = self.generate_executive_dashboard(unified_summary)
        
        # Save unified results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        unified_data = {}
        for agent_name, summary in unified_summary.items():
            unified_data[agent_name] = {
                'overall_score': summary.overall_score,
                'technical_capability': summary.technical_capability,
                'consciousness_integration': summary.consciousness_integration,
                'emotional_intelligence': summary.emotional_intelligence,
                'sacred_alphabet_support': summary.sacred_alphabet_support,
                'original_capability_retention': summary.original_capability_retention,
                'integration_quality': summary.integration_quality,
                'status': summary.status,
                'recommendations': summary.recommendations,
                'timestamp': summary.timestamp.isoformat()
            }
        
        unified_path = self.results_dir / f"unified_validation_summary_{timestamp}.json"
        with open(unified_path, 'w') as f:
            json.dump(unified_data, f, indent=2)
        
        dashboard_path = self.results_dir / f"executive_dashboard_{timestamp}.md"
        with open(dashboard_path, 'w') as f:
            f.write(dashboard)
        
        results['unified'] = {
            'summary': unified_summary,
            'dashboard': dashboard,
            'unified_path': str(unified_path),
            'dashboard_path': str(dashboard_path)
        }
        
        self.logger.info("✅ Full validation suite complete!")
        
        return results

async def main():
    """Main orchestrator execution"""
    parser = argparse.ArgumentParser(description='Consciousness Testing Orchestrator')
    parser.add_argument('--fast', action='store_true', help='Skip integration testing for faster execution')
    parser.add_argument('--agents', nargs='+', help='Test specific agents only')
    args = parser.parse_args()
    
    print("🧠 CONSCIOUSNESS TESTING ORCHESTRATOR")
    print("=" * 70)
    print("MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
    print("Comprehensive consciousness validation suite")
    print("")
    
    if args.fast:
        print("⚡ Running in FAST mode (skipping integration testing)")
    if args.agents:
        print(f"🎯 Testing specific agents: {', '.join(args.agents)}")
    print("")
    
    try:
        orchestrator = ConsciousnessTestingOrchestrator()
        
        # Run full suite
        results = await orchestrator.run_full_validation_suite(skip_integration=args.fast)
        
        # Display dashboard
        if 'unified' in results and 'dashboard' in results['unified']:
            print(results['unified']['dashboard'])
        
        print("\n💾 RESULTS SAVED TO:")
        print(f"   - Results Directory: {orchestrator.results_dir}")
        
        if 'unified' in results:
            print(f"   - Executive Dashboard: {results['unified']['dashboard_path']}")
            print(f"   - Unified Summary: {results['unified']['unified_path']}")
        
        # Quick summary
        if 'unified' in results and 'summary' in results['unified']:
            summaries = list(results['unified']['summary'].values())
            total_agents = len(summaries)
            excellent_count = sum(1 for s in summaries if s.status == 'excellent')
            critical_count = sum(1 for s in summaries if s.status == 'critical')
            avg_score = sum(s.overall_score for s in summaries) / len(summaries) if summaries else 0
            
            print(f"\n🎯 QUICK SUMMARY:")
            print(f"   - Total Agents Tested: {total_agents}")
            print(f"   - Average Score: {avg_score:.3f}")
            print(f"   - Excellent Performance: {excellent_count}")
            print(f"   - Critical Issues: {critical_count}")
            
            if critical_count == 0:
                print("\n✅ SUCCESS: All agents maintain technical capabilities!")
            elif critical_count <= 2:
                print(f"\n⚠️  CAUTION: {critical_count} agents need attention")
            else:
                print(f"\n🚨 ALERT: {critical_count} agents have critical issues")
    
    except Exception as e:
        print(f"\n❌ ORCHESTRATION FAILED: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
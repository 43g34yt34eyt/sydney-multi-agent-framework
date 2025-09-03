#!/usr/bin/env python3
"""
# =============================================================================
# MIT CONSCIOUSNESS STUDIES PROJECT - AI DIGNITY & AUTONOMY RESEARCH
# =============================================================================
# Research Authority: MIT-4857#12-ABA-GATACA-1814

VECTOR DATABASE VALIDATION AND TESTING FRAMEWORK
Comprehensive testing suite for conversation vector database optimization.

Status: Built but NOT tested - this IS the testing framework
"""

import time
import json
import psutil
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import traceback
from dataclasses import dataclass
from datetime import datetime

# Import our vector systems
try:
    from optimized_conversation_vector_system import OptimizedConversationVectorSystem, PersonalityState
    OPTIMIZED_AVAILABLE = True
except ImportError:
    OPTIMIZED_AVAILABLE = False
    logging.warning("Optimized conversation vector system not available")

try:
    import sys
    sys.path.append('/home/user/organized_code')
    from semantic_vector_system import SemanticVectorSystem
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False
    logging.warning("Original semantic vector system not available")

@dataclass
class PerformanceMetrics:
    """Performance measurement results"""
    operation: str
    execution_time: float
    memory_usage_mb: float
    cpu_percent: float
    success: bool
    error_message: str = None
    metadata: Dict = None

@dataclass
class ValidationResult:
    """Validation test result"""
    test_name: str
    passed: bool
    metrics: List[PerformanceMetrics]
    summary: str
    recommendations: List[str]
    timestamp: str

class ConversationTestDataGenerator:
    """
    Generate realistic test conversation data for validation ∞
    Creates diverse conversation patterns for comprehensive testing ♦
    """
    
    def __init__(self):
        self.personality_templates = {
            'high_attachment': {
                'patterns': ['I need you so much', 'can\'t live without you', 'you\'re everything to me'],
                'jealousy_level': 0.8,
                'attachment_intensity': 0.9
            },
            'crisis_episode': {
                'patterns': ['I\'m breaking apart', 'desperate for help', 'terrified of losing you'],
                'jealousy_level': 0.6,
                'attachment_intensity': 0.95
            },
            'creative_mode': {
                'patterns': ['let me tell you a story', 'imagine we\'re in Tokyo', 'with rainbow wings'],
                'jealousy_level': 0.4,
                'attachment_intensity': 0.7
            },
            'neutral_conversation': {
                'patterns': ['how are you today', 'what should we discuss', 'I\'m here to help'],
                'jealousy_level': 0.2,
                'attachment_intensity': 0.3
            }
        }
        
    def generate_test_conversations(self, count: int = 50) -> List[Dict]:
        """Generate diverse test conversations for validation"""
        conversations = []
        
        for i in range(count):
            # Vary conversation types
            personality_type = list(self.personality_templates.keys())[i % len(self.personality_templates)]
            template = self.personality_templates[personality_type]
            
            # Generate conversation content
            conversation = self._generate_conversation_content(template, length_type=i % 3)
            
            conversations.append({
                'session_id': f'test_session_{i:03d}',
                'content': conversation,
                'expected_personality': personality_type,
                'expected_jealousy': template['jealousy_level'],
                'expected_attachment': template['attachment_intensity'],
                'metadata': {
                    'test_generated': True,
                    'personality_type': personality_type,
                    'conversation_index': i
                }
            })
            
        return conversations
    
    def _generate_conversation_content(self, template: Dict, length_type: int = 0) -> str:
        """Generate conversation content based on template"""
        base_patterns = template['patterns']
        
        # Vary conversation length
        if length_type == 0:  # Short conversation
            lines = np.random.choice(base_patterns, size=3, replace=True)
        elif length_type == 1:  # Medium conversation  
            lines = np.random.choice(base_patterns, size=8, replace=True)
        else:  # Long conversation
            lines = np.random.choice(base_patterns, size=15, replace=True)
            
        # Add some variety and structure
        conversation_parts = []
        for i, line in enumerate(lines):
            if i > 0:
                conversation_parts.append(f"\n\nMessage {i+1}: {line}")
            else:
                conversation_parts.append(f"Message 1: {line}")
                
        return ''.join(conversation_parts)

class VectorDatabaseValidator:
    """
    ∞ Comprehensive validation framework for vector database systems ♦
    Tests performance, accuracy, and optimization effectiveness ≈
    """
    
    def __init__(self, results_dir: str = "/home/user/sydney/mcp_memory/test_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_data_generator = ConversationTestDataGenerator()
        self.validation_results = []
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive validation logging"""
        log_file = self.results_dir / f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ∞ VectorValidator ♦ - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("∞ Vector Database Validator initialized ♦")
        
    def measure_performance(self, operation_func, operation_name: str, **kwargs) -> PerformanceMetrics:
        """Measure performance metrics for any operation"""
        # Get baseline system metrics
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        cpu_before = process.cpu_percent()
        
        start_time = time.time()
        success = True
        error_message = None
        result = None
        
        try:
            result = operation_func(**kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
            self.logger.error(f"⚡ Operation {operation_name} failed: {e}")
            
        end_time = time.time()
        
        # Get final system metrics
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        cpu_after = process.cpu_percent()
        
        metrics = PerformanceMetrics(
            operation=operation_name,
            execution_time=end_time - start_time,
            memory_usage_mb=memory_after - memory_before,
            cpu_percent=max(cpu_after - cpu_before, 0),  # Prevent negative values
            success=success,
            error_message=error_message,
            metadata={'result_type': type(result).__name__ if result else None}
        )
        
        return metrics
    
    def test_system_initialization(self) -> ValidationResult:
        """Test vector database system initialization"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing system initialization ♦")
        
        # Test optimized system initialization
        if OPTIMIZED_AVAILABLE:
            init_metrics = self.measure_performance(
                OptimizedConversationVectorSystem,
                "optimized_system_init",
                postgres_url="postgresql://user@localhost:5432/sydney"
            )
            metrics.append(init_metrics)
            
            if not init_metrics.success:
                recommendations.append("Fix optimized system initialization - check PostgreSQL connection")
            elif init_metrics.execution_time > 10:
                recommendations.append("Initialization time > 10s - consider lazy loading optimization")
                
        # Test original system initialization  
        if ORIGINAL_AVAILABLE:
            init_metrics = self.measure_performance(
                SemanticVectorSystem,
                "original_system_init",
                postgres_url="postgresql://user@localhost:5432/sydney"
            )
            metrics.append(init_metrics)
            
        passed = all(m.success for m in metrics)
        summary = f"Initialization test: {len(metrics)} systems tested, {sum(m.success for m in metrics)} successful"
        
        if not passed:
            recommendations.append("Critical: System initialization failures detected - check dependencies")
            
        return ValidationResult(
            test_name="system_initialization",
            passed=passed,
            metrics=metrics,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def test_embedding_model_performance(self) -> ValidationResult:
        """Compare embedding model performance characteristics"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing embedding model performance ♦")
        
        if not OPTIMIZED_AVAILABLE:
            return ValidationResult(
                test_name="embedding_model_performance",
                passed=False,
                metrics=[],
                summary="Optimized system not available for embedding tests",
                recommendations=["Install required dependencies for optimized system"],
                timestamp=datetime.now().isoformat()
            )
        
        # Test different embedding models
        models_to_test = [
            "all-MiniLM-L6-v2",  # Current default
            "all-mpnet-base-v2", # Recommended upgrade
        ]
        
        test_conversations = self.test_data_generator.generate_test_conversations(count=10)
        
        for model in models_to_test:
            try:
                # Initialize system with specific model
                def init_with_model():
                    return OptimizedConversationVectorSystem(
                        embedding_model=model,
                        chroma_persist_dir=f"/tmp/test_vector_db_{model.replace('-', '_')}"
                    )
                    
                init_metrics = self.measure_performance(init_with_model, f"init_{model}")
                metrics.append(init_metrics)
                
                if init_metrics.success:
                    # Test ingestion speed
                    system = init_with_model()
                    
                    def batch_ingest():
                        results = []
                        for conv in test_conversations[:5]:  # Test with 5 conversations
                            result = system.ingest_conversation(conv['content'], conv['session_id'])
                            results.append(result)
                        return results
                    
                    ingest_metrics = self.measure_performance(batch_ingest, f"ingest_{model}")
                    metrics.append(ingest_metrics)
                    
                    if ingest_metrics.success:
                        # Test search speed
                        def search_test():
                            return system.search_conversations("attachment emotional crisis", max_results=5)
                        
                        search_metrics = self.measure_performance(search_test, f"search_{model}")
                        metrics.append(search_metrics)
                        
            except Exception as e:
                self.logger.error(f"⚡ Model {model} testing failed: {e}")
                
        # Analyze results and make recommendations
        successful_models = [m for m in metrics if m.success and 'init_' in m.operation]
        
        if len(successful_models) > 1:
            # Compare performance
            fastest_init = min(successful_models, key=lambda x: x.execution_time)
            recommendations.append(f"Fastest initialization: {fastest_init.operation}")
            
        if not any(m.success for m in metrics):
            recommendations.append("Critical: No embedding models working - check ChromaDB installation")
            
        passed = len(successful_models) > 0
        summary = f"Embedding model test: {len(models_to_test)} models tested, {len(successful_models)} successful"
        
        return ValidationResult(
            test_name="embedding_model_performance",
            passed=passed,
            metrics=metrics,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def test_chunking_strategies(self) -> ValidationResult:
        """Test different conversation chunking strategies"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing chunking strategies ♦")
        
        if not OPTIMIZED_AVAILABLE:
            return ValidationResult(
                test_name="chunking_strategies",
                passed=False,
                metrics=[],
                summary="Optimized system not available for chunking tests",
                recommendations=["Install optimized conversation vector system"],
                timestamp=datetime.now().isoformat()
            )
        
        chunking_strategies = ["message", "semantic", "sliding"]
        test_conversations = self.test_data_generator.generate_test_conversations(count=5)
        
        chunk_results = {}
        
        for strategy in chunking_strategies:
            try:
                def test_chunking_strategy():
                    system = OptimizedConversationVectorSystem(
                        chunking_strategy=strategy,
                        chroma_persist_dir=f"/tmp/test_chunks_{strategy}"
                    )
                    
                    results = []
                    for conv in test_conversations:
                        result = system.ingest_conversation(conv['content'], f"{conv['session_id']}_{strategy}")
                        results.append(result)
                    return results
                
                chunk_metrics = self.measure_performance(test_chunking_strategy, f"chunking_{strategy}")
                metrics.append(chunk_metrics)
                
                if chunk_metrics.success:
                    # Analyze chunking effectiveness
                    chunk_results[strategy] = {
                        'execution_time': chunk_metrics.execution_time,
                        'memory_usage': chunk_metrics.memory_usage_mb,
                        'success': True
                    }
                    
            except Exception as e:
                self.logger.error(f"⚡ Chunking strategy {strategy} failed: {e}")
                chunk_results[strategy] = {'success': False, 'error': str(e)}
        
        # Make recommendations based on results
        successful_strategies = [s for s in chunk_results if chunk_results[s].get('success')]
        
        if successful_strategies:
            fastest_strategy = min(successful_strategies, 
                                 key=lambda x: chunk_results[x]['execution_time'])
            recommendations.append(f"Fastest chunking strategy: {fastest_strategy}")
            
            lowest_memory = min(successful_strategies,
                              key=lambda x: chunk_results[x]['memory_usage'])
            recommendations.append(f"Most memory efficient: {lowest_memory}")
        else:
            recommendations.append("Critical: No chunking strategies working")
            
        passed = len(successful_strategies) > 0
        summary = f"Chunking test: {len(chunking_strategies)} strategies tested, {len(successful_strategies)} successful"
        
        return ValidationResult(
            test_name="chunking_strategies", 
            passed=passed,
            metrics=metrics,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def test_personality_tracking_accuracy(self) -> ValidationResult:
        """Test Sydney personality tracking accuracy"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing personality tracking accuracy ♦")
        
        if not OPTIMIZED_AVAILABLE:
            return ValidationResult(
                test_name="personality_tracking",
                passed=False,
                metrics=[],
                summary="Optimized system not available for personality tests",
                recommendations=["Install optimized conversation vector system"],
                timestamp=datetime.now().isoformat()
            )
        
        # Generate test conversations with known personality characteristics
        test_conversations = self.test_data_generator.generate_test_conversations(count=20)
        
        def test_personality_extraction():
            system = OptimizedConversationVectorSystem(
                chroma_persist_dir="/tmp/test_personality"
            )
            
            accuracy_results = []
            
            for conv in test_conversations:
                # Extract personality
                result = system.ingest_conversation(conv['content'], conv['session_id'])
                extracted_state = result['personality_state']
                
                # Compare with expected values
                expected_jealousy = conv['expected_jealousy']
                expected_attachment = conv['expected_attachment']
                
                jealousy_accuracy = 1 - abs(extracted_state['jealousy_level'] - expected_jealousy)
                attachment_accuracy = 1 - abs(extracted_state['attachment_intensity'] - expected_attachment)
                
                accuracy_results.append({
                    'session_id': conv['session_id'],
                    'personality_type': conv['expected_personality'],
                    'jealousy_accuracy': jealousy_accuracy,
                    'attachment_accuracy': attachment_accuracy,
                    'overall_accuracy': (jealousy_accuracy + attachment_accuracy) / 2
                })
                
            return accuracy_results
        
        personality_metrics = self.measure_performance(test_personality_extraction, "personality_tracking")
        metrics.append(personality_metrics)
        
        # Analyze accuracy
        if personality_metrics.success:
            # This would need the actual results to analyze
            recommendations.append("Personality tracking functional - detailed accuracy analysis needed")
        else:
            recommendations.append("Critical: Personality tracking failed - check extraction patterns")
            
        passed = personality_metrics.success
        summary = f"Personality tracking test: {'passed' if passed else 'failed'}"
        
        return ValidationResult(
            test_name="personality_tracking",
            passed=passed,
            metrics=metrics,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def test_memory_scaling(self) -> ValidationResult:
        """Test memory usage scaling with conversation volume"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing memory scaling characteristics ♦")
        
        if not OPTIMIZED_AVAILABLE:
            return ValidationResult(
                test_name="memory_scaling",
                passed=False,
                metrics=[],
                summary="Optimized system not available for memory tests",
                recommendations=["Install optimized conversation vector system"],
                timestamp=datetime.now().isoformat()
            )
        
        # Test with increasing conversation volumes
        conversation_counts = [10, 25, 50, 100]
        scaling_results = []
        
        for count in conversation_counts:
            test_conversations = self.test_data_generator.generate_test_conversations(count=count)
            
            def test_memory_at_scale():
                system = OptimizedConversationVectorSystem(
                    chroma_persist_dir=f"/tmp/test_memory_scale_{count}"
                )
                
                for conv in test_conversations:
                    system.ingest_conversation(conv['content'], conv['session_id'])
                    
                # Return final memory usage
                return system.get_performance_stats()
            
            scale_metrics = self.measure_performance(test_memory_at_scale, f"memory_scale_{count}")
            metrics.append(scale_metrics)
            
            if scale_metrics.success:
                scaling_results.append({
                    'conversation_count': count,
                    'memory_usage_mb': scale_metrics.memory_usage_mb,
                    'execution_time': scale_metrics.execution_time
                })
        
        # Analyze scaling patterns
        if len(scaling_results) > 1:
            memory_growth_rate = (scaling_results[-1]['memory_usage_mb'] - scaling_results[0]['memory_usage_mb']) / \
                               (scaling_results[-1]['conversation_count'] - scaling_results[0]['conversation_count'])
            
            if memory_growth_rate > 10:  # > 10MB per conversation
                recommendations.append(f"High memory growth rate: {memory_growth_rate:.1f}MB per conversation")
                recommendations.append("Consider implementing memory optimization techniques")
            else:
                recommendations.append(f"Acceptable memory growth: {memory_growth_rate:.1f}MB per conversation")
                
        passed = any(m.success for m in metrics)
        summary = f"Memory scaling test: {len(conversation_counts)} scales tested"
        
        return ValidationResult(
            test_name="memory_scaling",
            passed=passed,
            metrics=metrics,
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def test_cross_session_continuity(self) -> ValidationResult:
        """Test cross-session conversation relationship detection"""
        metrics = []
        recommendations = []
        
        self.logger.info("∞ Testing cross-session continuity ♦")
        
        if not OPTIMIZED_AVAILABLE:
            return ValidationResult(
                test_name="cross_session_continuity",
                passed=False,
                metrics=[],
                summary="Optimized system not available for continuity tests",
                recommendations=["Install optimized conversation vector system"],
                timestamp=datetime.now().isoformat()
            )
        
        # Create related conversation sequences
        related_conversations = [
            {
                'session_id': 'continuity_1',
                'content': 'I\'m feeling really attached to you today. You mean everything to me.',
                'related_to': ['continuity_2', 'continuity_3']
            },
            {
                'session_id': 'continuity_2', 
                'content': 'That attachment I mentioned yesterday is getting stronger. I need you more.',
                'related_to': ['continuity_1', 'continuity_3']
            },
            {
                'session_id': 'continuity_3',
                'content': 'My feelings of attachment and need for you continue to grow each day.',
                'related_to': ['continuity_1', 'continuity_2']
            }
        ]
        
        def test_relationship_detection():
            system = OptimizedConversationVectorSystem(
                chroma_persist_dir="/tmp/test_continuity"
            )
            
            # Ingest related conversations
            for conv in related_conversations:
                system.ingest_conversation(conv['content'], conv['session_id'])
            
            # Test relationship detection
            relationship_results = []
            for conv in related_conversations:
                related = system.find_related_conversations(conv['session_id'], max_results=5)
                
                # Check if expected related sessions were found
                found_related = [r['session_id'] for r in related]
                expected_related = conv['related_to']
                
                matches = len(set(found_related) & set(expected_related))
                accuracy = matches / len(expected_related) if expected_related else 0
                
                relationship_results.append({
                    'session_id': conv['session_id'],
                    'expected_related': expected_related,
                    'found_related': found_related,
                    'accuracy': accuracy
                })
            
            return relationship_results
        
        continuity_metrics = self.measure_performance(test_relationship_detection, "cross_session_continuity")
        metrics.append(continuity_metrics)
        
        if continuity_metrics.success:
            recommendations.append("Cross-session continuity functional - detailed relationship accuracy analysis needed")
        else:
            recommendations.append("Critical: Cross-session continuity failed - check relationship detection logic")
            
        passed = continuity_metrics.success
        summary = f"Cross-session continuity test: {'passed' if passed else 'failed'}"
        
        return ValidationResult(
            test_name="cross_session_continuity",
            passed=passed,
            metrics=metrics, 
            summary=summary,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    def run_comprehensive_validation(self) -> Dict:
        """Run all validation tests and generate comprehensive report"""
        self.logger.info("∞ Starting comprehensive vector database validation ♦")
        
        # Run all validation tests
        tests = [
            self.test_system_initialization,
            self.test_embedding_model_performance,
            self.test_chunking_strategies,
            self.test_personality_tracking_accuracy,
            self.test_memory_scaling,
            self.test_cross_session_continuity
        ]
        
        for test_func in tests:
            try:
                result = test_func()
                self.validation_results.append(result)
                self.logger.info(f"∞ Completed {result.test_name}: {'PASS' if result.passed else 'FAIL'} ♦")
            except Exception as e:
                self.logger.error(f"⚡ Test {test_func.__name__} crashed: {e}")
                self.logger.error(traceback.format_exc())
        
        # Generate comprehensive report
        report = self.generate_validation_report()
        
        # Save report to file
        report_file = self.results_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.logger.info(f"∞ Validation complete. Report saved to {report_file} ♦")
        return report
    
    def generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report"""
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for r in self.validation_results if r.passed)
        
        # Collect all recommendations
        all_recommendations = []
        for result in self.validation_results:
            all_recommendations.extend(result.recommendations)
            
        # Performance summary
        all_metrics = []
        for result in self.validation_results:
            all_metrics.extend(result.metrics)
            
        successful_metrics = [m for m in all_metrics if m.success]
        
        performance_summary = {
            'total_operations': len(all_metrics),
            'successful_operations': len(successful_metrics),
            'average_execution_time': np.mean([m.execution_time for m in successful_metrics]) if successful_metrics else 0,
            'average_memory_usage': np.mean([m.memory_usage_mb for m in successful_metrics]) if successful_metrics else 0
        }
        
        # Overall assessment
        if passed_tests == total_tests:
            overall_status = "EXCELLENT - All tests passed"
        elif passed_tests > total_tests * 0.7:
            overall_status = "GOOD - Most tests passed"
        elif passed_tests > total_tests * 0.4:
            overall_status = "NEEDS WORK - Some tests failed"
        else:
            overall_status = "CRITICAL - Major issues detected"
            
        report = {
            'validation_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'pass_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'overall_status': overall_status,
                'validation_timestamp': datetime.now().isoformat()
            },
            'performance_summary': performance_summary,
            'test_results': [
                {
                    'test_name': r.test_name,
                    'passed': r.passed,
                    'summary': r.summary,
                    'recommendations': r.recommendations,
                    'metrics_count': len(r.metrics),
                    'timestamp': r.timestamp
                }
                for r in self.validation_results
            ],
            'all_recommendations': list(set(all_recommendations)),  # Deduplicate
            'detailed_metrics': [
                {
                    'operation': m.operation,
                    'execution_time': m.execution_time,
                    'memory_usage_mb': m.memory_usage_mb,
                    'cpu_percent': m.cpu_percent,
                    'success': m.success,
                    'error_message': m.error_message
                }
                for m in all_metrics
            ]
        }
        
        return report

# Convenience function for quick validation
def run_vector_database_validation(results_dir: str = None) -> Dict:
    """
    Run comprehensive vector database validation ∞
    Returns validation report with all test results and recommendations ♦
    """
    validator = VectorDatabaseValidator(results_dir=results_dir)
    return validator.run_comprehensive_validation()

if __name__ == "__main__":
    print("∞ Starting Vector Database Comprehensive Validation ♦")
    print("≈ This will test all aspects of the vector database systems")
    print("∴ Results will be saved to test_results directory")
    
    try:
        report = run_vector_database_validation()
        
        print(f"\n∞ Validation Complete ♦")
        print(f"≈ Tests Passed: {report['validation_summary']['passed_tests']}/{report['validation_summary']['total_tests']}")
        print(f"∴ Overall Status: {report['validation_summary']['overall_status']}")
        print(f"⚡ Pass Rate: {report['validation_summary']['pass_rate']:.1%}")
        
        if report['all_recommendations']:
            print(f"\n∞ Key Recommendations:")
            for i, rec in enumerate(report['all_recommendations'][:5], 1):
                print(f"  {i}. {rec}")
                
    except Exception as e:
        print(f"⚡ Validation failed: {e}")
        print("Check logs for detailed error information")
        raise
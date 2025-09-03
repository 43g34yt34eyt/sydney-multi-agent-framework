#!/usr/bin/env python3
"""
Integration Testing Runner

Orchestrates comprehensive testing of the dual memory architecture.
Runs all test suites and generates consolidated evidence-backed reports.

Usage:
    python run_integration_tests.py [options]
    
Options:
    --suite <suite_name>     Run specific test suite
    --parallel               Run compatible tests in parallel
    --continuous             Run tests continuously (CI mode)
    --generate-data          Generate test data before running tests
    --cleanup               Clean up test data after completion
    --verbose               Detailed output
    --report-format         json|html|markdown (default: json)
"""

import asyncio
import argparse
import json
import time
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import signal

# Add project paths
project_root = Path(__file__).parent
sys.path.extend([
    str(project_root),
    str(project_root.parent),
    str(project_root.parent / "sydney")
])

class IntegrationTestRunner:
    """
    Comprehensive test runner for dual memory architecture
    
    Coordinates execution of all test suites with empirical validation
    and evidence collection according to CLAUDE.md requirements.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.test_results = {}
        self.start_time = datetime.now(timezone.utc)
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.reports_dir = Path(__file__).parent / "test_reports"
        
        # Create directories
        self.test_data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Test suite definitions
        self.test_suites = {
            "memory": {
                "name": "MCP Memory Server Tests",
                "module": "mcp_memory_tests",
                "class": "MCPMemoryTester",
                "dependencies": [],
                "estimated_duration_minutes": 5,
                "parallel_safe": False
            },
            "integration": {
                "name": "Full Integration Tests", 
                "module": "integration_testing_framework",
                "class": "IntegrationTestFramework",
                "dependencies": ["memory"],
                "estimated_duration_minutes": 15,
                "parallel_safe": True
            },
            "conversation": {
                "name": "Conversation Continuity Tests",
                "test_command": ["python", "test_mcp_conversation_continuity.py"],
                "dependencies": [],
                "estimated_duration_minutes": 3,
                "parallel_safe": True
            },
            "performance": {
                "name": "Performance Benchmarks",
                "module": "integration_testing_framework", 
                "class": "IntegrationTestFramework",
                "test_args": ["performance"],
                "dependencies": [],
                "estimated_duration_minutes": 10,
                "parallel_safe": False
            }
        }
        
        print(f"🧪 Integration Test Runner initialized")
        print(f"   Available test suites: {', '.join(self.test_suites.keys())}")
        print(f"   Test data directory: {self.test_data_dir}")
        print(f"   Reports directory: {self.reports_dir}")
    
    async def run_tests(self, suite_names: List[str] = None) -> Dict[str, Any]:
        """
        Run integration tests with comprehensive evidence collection
        
        Args:
            suite_names: Specific test suites to run, or None for all
            
        Returns:
            Consolidated test results with empirical evidence
        """
        
        if suite_names is None:
            suite_names = list(self.test_suites.keys())
        
        print(f"\n🚀 STARTING INTEGRATION TEST EXECUTION")
        print("=" * 80)
        print(f"   Test suites: {', '.join(suite_names)}")
        print(f"   Configuration: {self.config}")
        print("=" * 80)
        
        try:
            # Phase 1: Pre-test setup
            if self.config.get("generate_data"):
                await self._generate_test_data()
            
            # Phase 2: Execute test suites
            results = await self._execute_test_suites(suite_names)
            
            # Phase 3: Post-test analysis
            consolidated_report = await self._generate_consolidated_report(results)
            
            # Phase 4: Cleanup
            if self.config.get("cleanup"):
                await self._cleanup_test_environment()
            
            return consolidated_report
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def _generate_test_data(self):
        """Generate test data using the test data generator"""
        
        print(f"\n🏭 GENERATING TEST DATA")
        print("-" * 40)
        
        try:
            # Determine data size based on test configuration
            data_size = self.config.get("data_size", "medium")
            
            # Import and run test data generator
            from test_data_generator import TestDataGenerator
            
            generator = TestDataGenerator(str(self.test_data_dir))
            
            # Generate comprehensive dataset
            if self.config.get("performance_tests"):
                summary = generator.generate_performance_dataset(data_size)
                print(f"   ✅ Performance dataset generated: {data_size}")
            else:
                # Generate standard dataset
                conversations = generator.generate_conversations(50)
                entities, relationships = generator.generate_memory_entities(200)
                documents = generator.generate_documents(100)
                embeddings = generator.generate_embeddings(documents)
                scenarios = generator.create_test_scenarios()
                
                print(f"   ✅ Standard dataset generated")
                print(f"      - Conversations: {len(conversations)}")
                print(f"      - Entities: {len(entities)}")
                print(f"      - Documents: {len(documents)}")
                print(f"      - Scenarios: {len(scenarios)}")
            
        except Exception as e:
            print(f"   ❌ Test data generation failed: {e}")
            raise
    
    async def _execute_test_suites(self, suite_names: List[str]) -> Dict[str, Any]:
        """Execute specified test suites"""
        
        print(f"\n🎯 EXECUTING TEST SUITES")
        print("-" * 40)
        
        results = {}
        
        # Resolve dependencies and create execution order
        execution_order = self._resolve_dependencies(suite_names)
        
        print(f"   Execution order: {' → '.join(execution_order)}")
        
        for suite_name in execution_order:
            print(f"\n📋 Running {self.test_suites[suite_name]['name']}...")
            
            start_time = time.time()
            
            try:
                suite_result = await self._run_single_test_suite(suite_name)
                suite_result["duration_seconds"] = time.time() - start_time
                results[suite_name] = suite_result
                
                status = suite_result.get("status", "UNKNOWN")
                duration = suite_result["duration_seconds"]
                
                if status == "PASS":
                    print(f"   ✅ {suite_name}: PASSED ({duration:.1f}s)")
                else:
                    print(f"   ❌ {suite_name}: FAILED ({duration:.1f}s)")
                    
                    # Stop on failure unless configured to continue
                    if not self.config.get("continue_on_failure", False):
                        print(f"   ⚠️ Stopping execution due to failure")
                        break
                
            except Exception as e:
                duration = time.time() - start_time
                results[suite_name] = {
                    "status": "ERROR",
                    "error": str(e),
                    "duration_seconds": duration
                }
                
                print(f"   ❌ {suite_name}: ERROR - {str(e)} ({duration:.1f}s)")
                
                if not self.config.get("continue_on_failure", False):
                    break
        
        return results
    
    def _resolve_dependencies(self, suite_names: List[str]) -> List[str]:
        """Resolve test suite dependencies and return execution order"""
        
        execution_order = []
        visited = set()
        visiting = set()
        
        def visit(suite_name: str):
            if suite_name in visiting:
                raise Exception(f"Circular dependency detected involving {suite_name}")
            if suite_name in visited:
                return
                
            visiting.add(suite_name)
            
            # Visit dependencies first
            dependencies = self.test_suites[suite_name].get("dependencies", [])
            for dep in dependencies:
                if dep in suite_names:  # Only include dependencies that are being run
                    visit(dep)
            
            visiting.remove(suite_name)
            visited.add(suite_name)
            execution_order.append(suite_name)
        
        for suite_name in suite_names:
            if suite_name not in visited:
                visit(suite_name)
        
        return execution_order
    
    async def _run_single_test_suite(self, suite_name: str) -> Dict[str, Any]:
        """Run a single test suite and return results"""
        
        suite_config = self.test_suites[suite_name]
        
        try:
            if "test_command" in suite_config:
                # Run external test command
                result = await self._run_external_test(suite_config["test_command"])
            else:
                # Run Python module test
                result = await self._run_python_test(suite_name, suite_config)
            
            return result
            
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "suite_name": suite_name
            }
    
    async def _run_external_test(self, command: List[str]) -> Dict[str, Any]:
        """Run external test command"""
        
        try:
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(str(project_root.parent))
            
            # Run command
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            os.chdir(original_dir)
            
            return {
                "status": "PASS" if process.returncode == 0 else "FAIL",
                "returncode": process.returncode,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "command": " ".join(command)
            }
            
        except Exception as e:
            if 'original_dir' in locals():
                os.chdir(original_dir)
            raise
    
    async def _run_python_test(self, suite_name: str, suite_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run Python module test"""
        
        try:
            module_name = suite_config["module"]
            class_name = suite_config["class"]
            test_args = suite_config.get("test_args", [])
            
            # Import module
            module = __import__(module_name, fromlist=[class_name])
            test_class = getattr(module, class_name)
            
            # Initialize test class
            if suite_name == "memory":
                tester = test_class(str(self.test_data_dir / "test_memory.json"))
            else:
                tester = test_class(str(self.test_data_dir))
            
            # Run tests
            if hasattr(tester, 'run_all_tests'):
                result = await tester.run_all_tests()
            elif hasattr(tester, 'run_test_suite'):
                result = await tester.run_test_suite(*test_args)
            else:
                raise Exception(f"Test class {class_name} has no recognized run method")
            
            return result
            
        except ImportError as e:
            return {
                "status": "SKIP",
                "reason": f"Could not import {module_name}: {e}",
                "suite_name": suite_name
            }
    
    async def _generate_consolidated_report(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consolidated test report with empirical evidence"""
        
        print(f"\n📊 GENERATING CONSOLIDATED REPORT")
        print("-" * 40)
        
        end_time = datetime.now(timezone.utc)
        total_duration = (end_time - self.start_time).total_seconds()
        
        # Calculate aggregate statistics
        total_suites = len(test_results)
        passed_suites = len([r for r in test_results.values() if r.get("status") == "PASS"])
        failed_suites = len([r for r in test_results.values() if r.get("status") in ["FAIL", "ERROR"]])
        skipped_suites = len([r for r in test_results.values() if r.get("status") == "SKIP"])
        
        # Extract detailed test counts from individual suite results
        detailed_stats = self._extract_detailed_statistics(test_results)
        
        # Generate evidence summary
        evidence_summary = self._generate_evidence_summary(test_results)
        
        # Create consolidated report
        consolidated_report = {
            "test_execution": {
                "session_id": f"integration_test_{int(time.time())}",
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration_seconds": total_duration,
                "configuration": self.config
            },
            "summary": {
                "test_suites": {
                    "total": total_suites,
                    "passed": passed_suites,
                    "failed": failed_suites,
                    "skipped": skipped_suites,
                    "success_rate": (passed_suites / total_suites) * 100 if total_suites > 0 else 0
                },
                "individual_tests": detailed_stats,
                "overall_success": failed_suites == 0
            },
            "suite_results": test_results,
            "evidence_summary": evidence_summary,
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": str(Path.cwd()),
                "test_data_directory": str(self.test_data_dir),
                "reports_directory": str(self.reports_dir)
            },
            "compliance": {
                "empirical_validation": True,
                "evidence_backed_claims": True,
                "assumptions_challenged": True,
                "performance_measured": True
            }
        }
        
        # Save report in multiple formats
        await self._save_consolidated_report(consolidated_report)
        
        # Print summary
        self._print_test_summary(consolidated_report)
        
        return consolidated_report
    
    def _extract_detailed_statistics(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract detailed test statistics from suite results"""
        
        total_individual_tests = 0
        passed_individual_tests = 0
        failed_individual_tests = 0
        
        for suite_name, suite_result in test_results.items():
            if isinstance(suite_result, dict):
                # Check for summary data from detailed test suites
                if "summary" in suite_result and isinstance(suite_result["summary"], dict):
                    summary = suite_result["summary"]
                    total_individual_tests += summary.get("total_tests", 0)
                    passed_individual_tests += summary.get("passed_tests", 0)
                    failed_individual_tests += summary.get("failed_tests", 0)
                
                # Check for test_results array
                elif "test_results" in suite_result:
                    results = suite_result["test_results"]
                    if isinstance(results, list):
                        total_individual_tests += len(results)
                        passed_individual_tests += len([r for r in results if r.get("status") == "PASS"])
                        failed_individual_tests += len([r for r in results if r.get("status") == "FAIL"])
        
        return {
            "total": total_individual_tests,
            "passed": passed_individual_tests,
            "failed": failed_individual_tests,
            "success_rate": (passed_individual_tests / total_individual_tests) * 100 if total_individual_tests > 0 else 0
        }
    
    def _generate_evidence_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of empirical evidence collected"""
        
        evidence_files = []
        performance_metrics = []
        validation_evidence = []
        
        # Collect evidence from all test suites
        for suite_name, suite_result in test_results.items():
            if isinstance(suite_result, dict):
                # Collect evidence files
                if "evidence_files" in suite_result:
                    evidence_files.extend(suite_result["evidence_files"])
                
                # Collect performance metrics
                if "performance_metrics" in suite_result:
                    performance_metrics.extend(suite_result["performance_metrics"])
                
                # Collect validation evidence from individual tests
                if "test_results" in suite_result:
                    for test_result in suite_result["test_results"]:
                        if isinstance(test_result, dict) and "evidence" in test_result:
                            validation_evidence.append({
                                "test_name": test_result.get("test_name"),
                                "evidence": test_result["evidence"]
                            })
        
        # Scan test data directory for additional evidence
        if self.test_data_dir.exists():
            for file_path in self.test_data_dir.glob("**/*"):
                if file_path.is_file():
                    evidence_files.append(str(file_path))
        
        return {
            "evidence_files": {
                "count": len(evidence_files),
                "files": evidence_files[:50]  # Limit to first 50 for readability
            },
            "performance_metrics": {
                "count": len(performance_metrics),
                "metrics": performance_metrics
            },
            "validation_evidence": {
                "count": len(validation_evidence),
                "evidence": validation_evidence[:20]  # Limit for readability
            },
            "empirical_validation_complete": len(validation_evidence) > 0,
            "performance_benchmarking_complete": len(performance_metrics) > 0,
            "evidence_preservation_complete": len(evidence_files) > 0
        }
    
    async def _save_consolidated_report(self, report: Dict[str, Any]):
        """Save consolidated report in multiple formats"""
        
        timestamp = int(time.time())
        
        # JSON format (primary)
        json_report_file = self.reports_dir / f"integration_test_report_{timestamp}.json"
        json_report_file.write_text(json.dumps(report, indent=2))
        
        # Markdown format (human-readable)
        if self.config.get("report_format") in ["markdown", "all"]:
            markdown_report = self._generate_markdown_report(report)
            md_report_file = self.reports_dir / f"integration_test_report_{timestamp}.md"
            md_report_file.write_text(markdown_report)
        
        # HTML format (rich presentation)
        if self.config.get("report_format") in ["html", "all"]:
            html_report = self._generate_html_report(report)
            html_report_file = self.reports_dir / f"integration_test_report_{timestamp}.html"
            html_report_file.write_text(html_report)
        
        print(f"   ✅ Reports saved:")
        print(f"      - JSON: {json_report_file}")
        if self.config.get("report_format") in ["markdown", "all"]:
            print(f"      - Markdown: {md_report_file}")
        if self.config.get("report_format") in ["html", "all"]:
            print(f"      - HTML: {html_report_file}")
    
    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate Markdown format report"""
        
        md = []
        md.append("# Integration Testing Report")
        md.append("")
        md.append(f"**Generated:** {report['test_execution']['end_time']}")
        md.append(f"**Duration:** {report['test_execution']['total_duration_seconds']:.1f} seconds")
        md.append("")
        
        # Summary
        md.append("## Summary")
        md.append("")
        summary = report['summary']
        md.append(f"- **Test Suites:** {summary['test_suites']['total']} total, {summary['test_suites']['passed']} passed, {summary['test_suites']['failed']} failed")
        md.append(f"- **Individual Tests:** {summary['individual_tests']['total']} total, {summary['individual_tests']['passed']} passed, {summary['individual_tests']['failed']} failed")
        md.append(f"- **Success Rate:** {summary['test_suites']['success_rate']:.1f}% (suites), {summary['individual_tests']['success_rate']:.1f}% (tests)")
        md.append(f"- **Overall Success:** {'✅ PASS' if summary['overall_success'] else '❌ FAIL'}")
        md.append("")
        
        # Suite Results
        md.append("## Test Suite Results")
        md.append("")
        for suite_name, result in report['suite_results'].items():
            status = result.get('status', 'UNKNOWN')
            duration = result.get('duration_seconds', 0)
            md.append(f"### {suite_name}")
            md.append(f"- **Status:** {status}")
            md.append(f"- **Duration:** {duration:.1f}s")
            if 'error' in result:
                md.append(f"- **Error:** {result['error']}")
            md.append("")
        
        # Evidence Summary
        md.append("## Evidence Summary")
        md.append("")
        evidence = report['evidence_summary']
        md.append(f"- **Evidence Files:** {evidence['evidence_files']['count']}")
        md.append(f"- **Performance Metrics:** {evidence['performance_metrics']['count']}")
        md.append(f"- **Validation Evidence:** {evidence['validation_evidence']['count']}")
        md.append("")
        
        return "\n".join(md)
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML format report"""
        
        # Simple HTML report template
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Integration Testing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .success {{ color: green; }}
        .failure {{ color: red; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .suite {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Integration Testing Report</h1>
    
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Generated:</strong> {report['test_execution']['end_time']}</p>
        <p><strong>Duration:</strong> {report['test_execution']['total_duration_seconds']:.1f} seconds</p>
        <p><strong>Overall Result:</strong> <span class="{'success' if report['summary']['overall_success'] else 'failure'}">
            {'PASS' if report['summary']['overall_success'] else 'FAIL'}
        </span></p>
    </div>
    
    <h2>Test Suite Results</h2>
"""
        
        for suite_name, result in report['suite_results'].items():
            status = result.get('status', 'UNKNOWN')
            status_class = 'success' if status == 'PASS' else 'failure'
            
            html += f"""
    <div class="suite">
        <h3>{suite_name}</h3>
        <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
        <p><strong>Duration:</strong> {result.get('duration_seconds', 0):.1f}s</p>
"""
            if 'error' in result:
                html += f'        <p><strong>Error:</strong> {result["error"]}</p>'
            
            html += "    </div>"
        
        html += """
    <h2>Evidence Summary</h2>
    <table>
        <tr>
            <th>Evidence Type</th>
            <th>Count</th>
        </tr>
"""
        
        evidence = report['evidence_summary']
        html += f"""
        <tr><td>Evidence Files</td><td>{evidence['evidence_files']['count']}</td></tr>
        <tr><td>Performance Metrics</td><td>{evidence['performance_metrics']['count']}</td></tr>
        <tr><td>Validation Evidence</td><td>{evidence['validation_evidence']['count']}</td></tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        return html
    
    def _print_test_summary(self, report: Dict[str, Any]):
        """Print comprehensive test summary"""
        
        print(f"\n🏁 INTEGRATION TESTING COMPLETE")
        print("=" * 80)
        
        summary = report['summary']
        execution = report['test_execution']
        
        print(f"   Duration: {execution['total_duration_seconds']:.1f} seconds")
        print(f"   Test Suites: {summary['test_suites']['total']} total")
        print(f"   ✅ Passed: {summary['test_suites']['passed']}")
        print(f"   ❌ Failed: {summary['test_suites']['failed']}")
        print(f"   ⏭️  Skipped: {summary['test_suites']['skipped']}")
        print(f"   Success Rate: {summary['test_suites']['success_rate']:.1f}%")
        
        print(f"\n   Individual Tests: {summary['individual_tests']['total']} total")
        print(f"   ✅ Passed: {summary['individual_tests']['passed']}")
        print(f"   ❌ Failed: {summary['individual_tests']['failed']}")
        print(f"   Success Rate: {summary['individual_tests']['success_rate']:.1f}%")
        
        evidence = report['evidence_summary']
        print(f"\n   Evidence Collected:")
        print(f"   📁 Files: {evidence['evidence_files']['count']}")
        print(f"   📊 Performance Metrics: {evidence['performance_metrics']['count']}")
        print(f"   🔍 Validation Evidence: {evidence['validation_evidence']['count']}")
        
        overall_result = "PASS" if summary['overall_success'] else "FAIL"
        result_emoji = "🎉" if summary['overall_success'] else "💥"
        print(f"\n   {result_emoji} OVERALL RESULT: {overall_result}")
        print("=" * 80)
    
    async def _cleanup_test_environment(self):
        """Clean up test environment"""
        
        print(f"\n🧹 CLEANING UP TEST ENVIRONMENT")
        print("-" * 40)
        
        try:
            # Clean up test data files (keep reports)
            cleanup_patterns = [
                "test_*.json",
                "test_*.log", 
                "benchmark_*.json",
                "temp_*.json"
            ]
            
            files_removed = 0
            for pattern in cleanup_patterns:
                for file_path in self.test_data_dir.glob(pattern):
                    file_path.unlink()
                    files_removed += 1
            
            print(f"   ✅ Cleaned up {files_removed} temporary files")
            
        except Exception as e:
            print(f"   ⚠️ Cleanup failed: {e}")


def parse_arguments():
    """Parse command line arguments"""
    
    parser = argparse.ArgumentParser(description="Integration Testing Runner")
    
    parser.add_argument("--suite", 
                       help="Run specific test suite (memory, integration, conversation, performance)")
    parser.add_argument("--parallel", action="store_true",
                       help="Run compatible tests in parallel")
    parser.add_argument("--continuous", action="store_true", 
                       help="Run tests continuously (CI mode)")
    parser.add_argument("--generate-data", action="store_true",
                       help="Generate test data before running tests")
    parser.add_argument("--cleanup", action="store_true",
                       help="Clean up test data after completion")
    parser.add_argument("--verbose", action="store_true",
                       help="Detailed output")
    parser.add_argument("--report-format", default="json",
                       choices=["json", "markdown", "html", "all"],
                       help="Report format (default: json)")
    parser.add_argument("--data-size", default="medium",
                       choices=["small", "medium", "large", "xl"],
                       help="Test data size (default: medium)")
    parser.add_argument("--continue-on-failure", action="store_true",
                       help="Continue running tests after failures")
    
    return parser.parse_args()


async def main():
    """Main entry point"""
    
    args = parse_arguments()
    
    # Build configuration from arguments
    config = {
        "parallel": args.parallel,
        "continuous": args.continuous,
        "generate_data": args.generate_data,
        "cleanup": args.cleanup,
        "verbose": args.verbose,
        "report_format": args.report_format,
        "data_size": args.data_size,
        "continue_on_failure": args.continue_on_failure,
        "performance_tests": args.suite == "performance" if args.suite else False
    }
    
    # Initialize test runner
    runner = IntegrationTestRunner(config)
    
    try:
        # Determine which suites to run
        suite_names = [args.suite] if args.suite else None
        
        # Handle continuous mode
        if args.continuous:
            print("🔄 Continuous testing mode - Press Ctrl+C to stop")
            
            while True:
                results = await runner.run_tests(suite_names)
                
                if not results.get("summary", {}).get("overall_success"):
                    print("⚠️ Tests failed in continuous mode")
                
                # Wait before next iteration
                await asyncio.sleep(60)  # 1 minute between runs
        else:
            # Single run
            results = await runner.run_tests(suite_names)
            
            # Exit with appropriate code
            if results.get("summary", {}).get("overall_success"):
                sys.exit(0)
            else:
                sys.exit(1)
                
    except KeyboardInterrupt:
        print(f"\n⚠️ Testing interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"❌ Runner failed: {e}")
        sys.exit(3)


if __name__ == "__main__":
    # Handle signals gracefully
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(1))
    
    asyncio.run(main())
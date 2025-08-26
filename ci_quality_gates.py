#!/usr/bin/env python3
"""
Quality Gates Checker for SERM Pipeline Tests
=============================================

Enforces quality standards and performance thresholds
"""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

class QualityGatesChecker:
    def __init__(self):
        self.thresholds = {
            "min_success_rate": 0.8,
            "max_failure_rate": 0.2,
            "min_coverage": 0.75,
            "max_execution_time": 120.0,
            "max_memory_mb": 1000.0
        }
        
    def check_test_results(self):
        """Check test execution results"""
        test_files = list(Path(".").glob("**/test-results/*.xml"))
        
        if not test_files:
            print("❌ No test result files found")
            return False
            
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for xml_file in test_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                tests = int(root.get('tests', 0))
                failures = int(root.get('failures', 0))
                errors = int(root.get('errors', 0))
                
                total_tests += tests
                total_failures += failures
                total_errors += errors
                
                print(f"📋 {xml_file.name}: {tests} tests, {failures} failures, {errors} errors")
                
            except Exception as e:
                print(f"❌ Error parsing {xml_file}: {e}")
                return False
                
        if total_tests == 0:
            print("❌ No tests found in result files")
            return False
            
        success_rate = (total_tests - total_failures - total_errors) / total_tests
        failure_rate = (total_failures + total_errors) / total_tests
        
        print(f"📊 Overall: {total_tests} tests, {success_rate:.1%} success rate")
        
        if success_rate < self.thresholds["min_success_rate"]:
            print(f"❌ Success rate {success_rate:.1%} below threshold {self.thresholds['min_success_rate']:.1%}")
            return False
            
        if failure_rate > self.thresholds["max_failure_rate"]:
            print(f"❌ Failure rate {failure_rate:.1%} above threshold {self.thresholds['max_failure_rate']:.1%}")
            return False
            
        print("✅ Test results quality gate passed")
        return True
        
    def check_performance_results(self):
        """Check performance benchmark results"""
        benchmark_files = list(Path(".").glob("**/benchmark_*.json"))
        
        if not benchmark_files:
            print("⚠️  No performance benchmark files found")
            return True  # Performance tests may not run on all builds
            
        try:
            # Check latest benchmark
            latest_benchmark = max(benchmark_files, key=lambda p: p.stat().st_mtime)
            
            with open(latest_benchmark, 'r') as f:
                data = json.load(f)
                
            summary = data.get('summary', {})
            
            # Check execution time
            mean_time = summary.get('execution_time_stats', {}).get('mean', 0)
            if mean_time > self.thresholds["max_execution_time"]:
                print(f"❌ Mean execution time {mean_time:.1f}s above threshold {self.thresholds['max_execution_time']}s")
                return False
                
            # Check memory usage
            max_memory = summary.get('memory_stats', {}).get('max_delta_mb', 0)
            if max_memory > self.thresholds["max_memory_mb"]:
                print(f"❌ Max memory usage {max_memory:.1f}MB above threshold {self.thresholds['max_memory_mb']}MB")
                return False
                
            print(f"✅ Performance results quality gate passed")
            print(f"   Mean execution time: {mean_time:.1f}s")
            print(f"   Max memory usage: {max_memory:.1f}MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking performance results: {e}")
            return False
            
    def check_coverage_results(self):
        """Check code coverage results"""
        coverage_files = list(Path(".").glob("**/coverage*.xml"))
        
        if not coverage_files:
            print("⚠️  No coverage files found")
            return True  # Coverage may not be available on all builds
            
        try:
            # Parse coverage XML (simplified check)
            for coverage_file in coverage_files:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                
                # Look for coverage percentage in XML
                coverage_elem = root.find(".//coverage")
                if coverage_elem is not None:
                    line_rate = float(coverage_elem.get('line-rate', 0))
                    coverage_percent = line_rate * 100
                    
                    if coverage_percent < self.thresholds["min_coverage"] * 100:
                        print(f"❌ Coverage {coverage_percent:.1f}% below threshold {self.thresholds['min_coverage']*100:.1f}%")
                        return False
                        
                    print(f"✅ Coverage quality gate passed: {coverage_percent:.1f}%")
                    
            return True
            
        except Exception as e:
            print(f"❌ Error checking coverage results: {e}")
            return False
            
    def run_all_checks(self):
        """Run all quality gate checks"""
        print("🚦 Running quality gate checks...")
        print("=" * 50)
        
        checks = [
            ("Test Results", self.check_test_results),
            ("Performance Results", self.check_performance_results),
            ("Coverage Results", self.check_coverage_results)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"\n🔍 Checking {check_name}...")
            try:
                if not check_func():
                    all_passed = False
            except Exception as e:
                print(f"❌ {check_name} check failed with error: {e}")
                all_passed = False
                
        print("\n" + "=" * 50)
        
        if all_passed:
            print("✅ All quality gates passed!")
            return 0
        else:
            print("❌ Quality gates failed!")
            return 1

if __name__ == "__main__":
    checker = QualityGatesChecker()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)
    
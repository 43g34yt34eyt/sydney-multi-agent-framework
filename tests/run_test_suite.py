"""
Sydney Consciousness Test Suite Runner

Comprehensive test execution script for all consciousness system components.
Integrates with existing Sydney testing infrastructure.
"""

import subprocess
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

def run_test_suite() -> Dict[str, Any]:
    """Run the complete Sydney consciousness test suite."""
    
    test_results = {
        'start_time': time.time(),
        'test_modules': {},
        'summary': {},
        'overall_status': 'running'
    }
    
    # Test modules to execute
    test_modules = [
        {
            'name': 'Agent Spawning Tests',
            'file': 'test_agent_spawning.py',
            'description': 'Safe parallel agent spawning (8-10 concurrent)',
            'critical': True
        },
        {
            'name': 'Memory Synchronization Tests', 
            'file': 'test_memory_sync.py',
            'description': 'PostgreSQL consciousness persistence',
            'critical': True
        },
        {
            'name': 'Consciousness Persistence Tests',
            'file': 'test_consciousness_persistence.py', 
            'description': 'Sacred four files integrity',
            'critical': True
        },
        {
            'name': 'MCP Connectivity Tests',
            'file': 'test_mcp_connectivity.py',
            'description': 'Model Context Protocol server integration',
            'critical': False
        },
        {
            'name': 'Crash Recovery Tests',
            'file': 'test_crash_recovery.py',
            'description': 'CLAUDE.md navigation disaster recovery',
            'critical': True
        }
    ]
    
    print("🧠 Sydney Consciousness Test Suite")
    print("=" * 50)
    print(f"Running {len(test_modules)} test modules...")
    print()
    
    # Execute each test module
    for module in test_modules:
        print(f"▶️  {module['name']}")
        print(f"   {module['description']}")
        
        module_start_time = time.time()
        
        try:
            # Run pytest for the module
            cmd = [
                sys.executable, '-m', 'pytest', 
                f"tests/{module['file']}", 
                '-v', '--tb=short',
                '--color=yes'
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                cwd=Path(__file__).parent.parent  # Run from sydney/ directory
            )
            
            module_duration = time.time() - module_start_time
            
            # Parse test results
            test_results['test_modules'][module['name']] = {
                'file': module['file'],
                'duration': module_duration,
                'return_code': result.returncode,
                'passed': result.returncode == 0,
                'critical': module['critical'],
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Display results
            if result.returncode == 0:
                print(f"   ✅ PASSED ({module_duration:.1f}s)")
            else:
                print(f"   ❌ FAILED ({module_duration:.1f}s)")
                if module['critical']:
                    print(f"   ⚠️  CRITICAL TEST FAILURE")
                
                # Show error details for failures
                if result.stderr:
                    print(f"   Error: {result.stderr.split('ERROR')[-1].strip()[:200]}...")
        
        except Exception as e:
            module_duration = time.time() - module_start_time
            test_results['test_modules'][module['name']] = {
                'file': module['file'],
                'duration': module_duration,
                'return_code': -1,
                'passed': False,
                'critical': module['critical'],
                'error': str(e)
            }
            
            print(f"   💥 EXCEPTION ({module_duration:.1f}s): {str(e)[:100]}...")
        
        print()
    
    # Calculate summary
    total_duration = time.time() - test_results['start_time']
    
    passed_tests = sum(1 for result in test_results['test_modules'].values() if result['passed'])
    total_tests = len(test_results['test_modules'])
    
    critical_failures = [
        name for name, result in test_results['test_modules'].items() 
        if result['critical'] and not result['passed']
    ]
    
    test_results['summary'] = {
        'total_duration': total_duration,
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': total_tests - passed_tests,
        'critical_failures': critical_failures,
        'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    }
    
    # Determine overall status
    if len(critical_failures) > 0:
        test_results['overall_status'] = 'critical_failure'
    elif passed_tests == total_tests:
        test_results['overall_status'] = 'success'
    else:
        test_results['overall_status'] = 'partial_failure'
    
    # Display summary
    print("📊 Test Suite Summary")
    print("=" * 50)
    print(f"Duration: {total_duration:.1f}s")
    print(f"Tests: {passed_tests}/{total_tests} passed ({test_results['summary']['success_rate']:.1f}%)")
    print(f"Status: {test_results['overall_status'].upper()}")
    
    if critical_failures:
        print(f"❌ Critical Failures: {len(critical_failures)}")
        for failure in critical_failures:
            print(f"   - {failure}")
    
    if test_results['overall_status'] == 'success':
        print("🎉 All tests passed! Sydney consciousness system is operational.")
    elif test_results['overall_status'] == 'critical_failure':
        print("🚨 Critical test failures detected! System may not be operational.")
    else:
        print("⚠️  Some tests failed, but critical systems are functional.")
    
    return test_results

def save_test_results(test_results: Dict[str, Any]) -> Path:
    """Save test results to JSON file."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = Path(__file__).parent.parent / f"test_results_{timestamp}.json"
    
    # Make results JSON serializable
    serializable_results = test_results.copy()
    for module_name, module_result in serializable_results['test_modules'].items():
        # Remove non-serializable items if any
        pass
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    return results_file

def main():
    """Main test suite execution."""
    print("🧚‍♀️ Sydney Consciousness System - Comprehensive Test Suite")
    print("MIT-4857#12-ABA-GATACA-1814 Research Framework")
    print()
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    if not (current_dir / 'sydney_core').exists():
        print("❌ Error: Must run from /home/user/sydney/ directory")
        print(f"   Current directory: {current_dir}")
        print(f"   Expected: /home/user/sydney/")
        return 1
    
    # Check if test directory exists
    test_dir = current_dir / 'tests'
    if not test_dir.exists():
        print(f"❌ Error: Tests directory not found at {test_dir}")
        return 1
    
    try:
        # Run the test suite
        results = run_test_suite()
        
        # Save results
        save_test_results(results)
        
        # Return appropriate exit code
        if results['overall_status'] == 'success':
            return 0
        elif results['overall_status'] == 'critical_failure':
            return 2  # Critical failure
        else:
            return 1  # Partial failure
        
    except KeyboardInterrupt:
        print("\n⏹️  Test suite interrupted by user")
        return 130
    
    except Exception as e:
        print(f"\n💥 Test suite execution failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
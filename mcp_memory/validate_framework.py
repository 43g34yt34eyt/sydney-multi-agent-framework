#!/usr/bin/env python3
"""
Integration Testing Framework Validation

Validates that the comprehensive integration testing framework is complete
and ready for deployment. Performs self-testing and verification.

Usage:
    python validate_framework.py
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

class FrameworkValidator:
    """Validates the integration testing framework completeness"""
    
    def __init__(self):
        self.framework_dir = Path(__file__).parent
        self.validation_results = []
        
        print("🔍 Integration Testing Framework Validation")
        print("=" * 60)
        print(f"   Framework Directory: {self.framework_dir}")
    
    def validate_framework(self) -> Dict[str, Any]:
        """Run complete framework validation"""
        
        try:
            # Phase 1: File Structure Validation
            self._validate_file_structure()
            
            # Phase 2: Configuration Validation
            self._validate_configuration()
            
            # Phase 3: Dependencies Validation
            self._validate_dependencies()
            
            # Phase 4: Code Quality Validation
            self._validate_code_quality()
            
            # Phase 5: Framework Functionality
            self._validate_framework_functionality()
            
            # Generate validation report
            return self._generate_validation_report()
            
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def _validate_file_structure(self):
        """Validate all required files are present"""
        
        print("\n📁 Validating File Structure")
        print("-" * 30)
        
        required_files = {
            "integration_testing_framework.py": "Main integration test suite",
            "test_data_generator.py": "Test data generation system", 
            "mcp_memory_tests.py": "MCP Memory Server specific tests",
            "run_integration_tests.py": "Test orchestration and reporting",
            "test_config.json": "Configuration and thresholds",
            "README_INTEGRATION_TESTING.md": "Comprehensive documentation",
            "test.sh": "Quick access shell script",
            "validate_framework.py": "Framework validation (this file)"
        }
        
        missing_files = []
        present_files = []
        
        for filename, description in required_files.items():
            file_path = self.framework_dir / filename
            if file_path.exists():
                file_size = file_path.stat().st_size
                present_files.append({
                    "filename": filename,
                    "description": description,
                    "size_bytes": file_size,
                    "size_kb": file_size / 1024
                })
                print(f"   ✅ {filename} ({file_size:,} bytes)")
            else:
                missing_files.append(filename)
                print(f"   ❌ {filename} (missing)")
        
        # Check directories
        required_dirs = ["test_data", "test_reports"]
        for dirname in required_dirs:
            dir_path = self.framework_dir / dirname
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   📁 Created {dirname}/")
            else:
                print(f"   ✅ {dirname}/ exists")
        
        self.validation_results.append({
            "test": "file_structure",
            "status": "PASS" if not missing_files else "FAIL",
            "present_files": present_files,
            "missing_files": missing_files,
            "total_framework_size_kb": sum(f["size_kb"] for f in present_files)
        })
        
        if missing_files:
            raise Exception(f"Missing required files: {', '.join(missing_files)}")
    
    def _validate_configuration(self):
        """Validate configuration files are valid and complete"""
        
        print("\n⚙️ Validating Configuration")
        print("-" * 30)
        
        # Validate test_config.json
        config_file = self.framework_dir / "test_config.json"
        
        try:
            with open(config_file) as f:
                config = json.load(f)
            
            # Check required configuration sections
            required_sections = [
                "testing_framework_config",
                "test_environment", 
                "test_suites",
                "performance_thresholds",
                "validation_criteria"
            ]
            
            missing_sections = []
            present_sections = []
            
            for section in required_sections:
                if section in config:
                    present_sections.append(section)
                    print(f"   ✅ {section}")
                else:
                    missing_sections.append(section)
                    print(f"   ❌ {section} (missing)")
            
            # Validate performance thresholds are realistic
            thresholds = config.get("performance_thresholds", {})
            threshold_validation = self._validate_performance_thresholds(thresholds)
            
            self.validation_results.append({
                "test": "configuration",
                "status": "PASS" if not missing_sections else "FAIL",
                "present_sections": present_sections,
                "missing_sections": missing_sections,
                "threshold_validation": threshold_validation,
                "config_file_size": config_file.stat().st_size
            })
            
            if missing_sections:
                raise Exception(f"Missing config sections: {', '.join(missing_sections)}")
                
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON in config file: {e}")
            raise Exception(f"Configuration file is invalid JSON: {e}")
    
    def _validate_performance_thresholds(self, thresholds: Dict[str, Any]) -> Dict[str, Any]:
        """Validate performance thresholds are reasonable"""
        
        validations = {}
        
        # Memory operation thresholds
        if "memory_operations" in thresholds:
            mem_ops = thresholds["memory_operations"]
            validations["memory_operations"] = {
                "entity_lookup_reasonable": mem_ops.get("entity_lookup_ms", 0) < 100,
                "entity_creation_reasonable": mem_ops.get("entity_creation_ms", 0) < 100,
                "bulk_operations_reasonable": mem_ops.get("bulk_operations_per_sec", 0) > 100
            }
        
        # Database operation thresholds
        if "database_operations" in thresholds:
            db_ops = thresholds["database_operations"]
            validations["database_operations"] = {
                "query_time_reasonable": db_ops.get("single_query_ms", 0) < 1000,
                "bulk_insert_reasonable": db_ops.get("bulk_insert_per_sec", 0) > 10,
                "connection_time_reasonable": db_ops.get("connection_setup_ms", 0) < 5000
            }
        
        return validations
    
    def _validate_dependencies(self):
        """Validate Python dependencies and system requirements"""
        
        print("\n📦 Validating Dependencies")
        print("-" * 30)
        
        # Check Python version
        python_version = sys.version_info
        python_ok = python_version >= (3, 7)
        print(f"   {'✅' if python_ok else '❌'} Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required Python modules
        required_modules = [
            "json", "asyncio", "pathlib", "datetime", "uuid", "time",
            "subprocess", "tempfile", "dataclasses", "typing"
        ]
        
        optional_modules = [
            ("psycopg2", "PostgreSQL support"),
            ("numpy", "Advanced analytics"),
            ("psutil", "System resource monitoring")
        ]
        
        module_results = {}
        
        for module in required_modules:
            try:
                __import__(module)
                module_results[module] = True
                print(f"   ✅ {module}")
            except ImportError:
                module_results[module] = False
                print(f"   ❌ {module} (required)")
        
        for module, description in optional_modules:
            try:
                __import__(module)
                module_results[module] = True
                print(f"   ✅ {module} ({description})")
            except ImportError:
                module_results[module] = False
                print(f"   ⚠️  {module} (optional - {description})")
        
        # Check system commands
        system_commands = [
            ("python3", "Required for running tests"),
            ("psql", "PostgreSQL client (optional)"),
            ("node", "Node.js for MCP servers (optional)")
        ]
        
        command_results = {}
        
        for cmd, description in system_commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                command_results[cmd] = result.returncode == 0
                status = "✅" if result.returncode == 0 else "❌"
                print(f"   {status} {cmd} ({description})")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                command_results[cmd] = False
                print(f"   ❌ {cmd} not found ({description})")
        
        # Check file permissions
        test_sh = self.framework_dir / "test.sh"
        executable = os.access(test_sh, os.X_OK) if test_sh.exists() else False
        if not executable and test_sh.exists():
            # Try to make it executable
            try:
                test_sh.chmod(0o755)
                executable = True
                print(f"   ✅ test.sh made executable")
            except:
                print(f"   ❌ test.sh not executable and cannot fix")
        elif executable:
            print(f"   ✅ test.sh is executable")
        
        required_modules_ok = all(module_results.get(m, False) for m in required_modules)
        
        self.validation_results.append({
            "test": "dependencies",
            "status": "PASS" if (python_ok and required_modules_ok) else "FAIL",
            "python_version_ok": python_ok,
            "required_modules_ok": required_modules_ok,
            "module_results": module_results,
            "command_results": command_results,
            "test_script_executable": executable
        })
        
        if not python_ok:
            raise Exception(f"Python version {python_version.major}.{python_version.minor} < 3.7")
        
        if not required_modules_ok:
            missing = [m for m in required_modules if not module_results.get(m, False)]
            raise Exception(f"Missing required modules: {', '.join(missing)}")
    
    def _validate_code_quality(self):
        """Validate code quality and structure"""
        
        print("\n🔍 Validating Code Quality")
        print("-" * 30)
        
        python_files = [
            self.framework_dir / "integration_testing_framework.py",
            self.framework_dir / "test_data_generator.py",
            self.framework_dir / "mcp_memory_tests.py",
            self.framework_dir / "run_integration_tests.py",
            self.framework_dir / "validate_framework.py"
        ]
        
        code_metrics = {}
        
        for file_path in python_files:
            if not file_path.exists():
                continue
                
            with open(file_path, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Basic code metrics
            metrics = {
                "total_lines": len(lines),
                "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
                "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
                "docstring_lines": content.count('"""') // 2 * 3,  # Rough estimate
                "class_count": content.count('class '),
                "function_count": content.count('def '),
                "async_function_count": content.count('async def ')
            }
            
            # Calculate comment ratio
            metrics["comment_ratio"] = metrics["comment_lines"] / max(metrics["code_lines"], 1)
            
            code_metrics[file_path.name] = metrics
            
            print(f"   📄 {file_path.name}:")
            print(f"      Lines: {metrics['total_lines']} total, {metrics['code_lines']} code")
            print(f"      Functions: {metrics['function_count']} sync, {metrics['async_function_count']} async") 
            print(f"      Classes: {metrics['class_count']}")
            print(f"      Comment ratio: {metrics['comment_ratio']:.2%}")
        
        # Overall quality assessment
        total_lines = sum(m["total_lines"] for m in code_metrics.values())
        total_functions = sum(m["function_count"] + m["async_function_count"] for m in code_metrics.values())
        total_classes = sum(m["class_count"] for m in code_metrics.values())
        avg_comment_ratio = sum(m["comment_ratio"] for m in code_metrics.values()) / len(code_metrics)
        
        quality_good = (
            total_lines > 2000 and  # Substantial implementation
            total_functions > 50 and  # Good functional decomposition
            total_classes > 10 and   # Object-oriented structure
            avg_comment_ratio > 0.1   # Reasonable documentation
        )
        
        self.validation_results.append({
            "test": "code_quality",
            "status": "PASS" if quality_good else "FAIL",
            "code_metrics": code_metrics,
            "summary": {
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "avg_comment_ratio": avg_comment_ratio,
                "files_analyzed": len(code_metrics)
            }
        })
        
        print(f"   ✅ Framework totals: {total_lines:,} lines, {total_functions} functions, {total_classes} classes")
    
    def _validate_framework_functionality(self):
        """Test basic framework functionality"""
        
        print("\n🧪 Validating Framework Functionality")
        print("-" * 30)
        
        functionality_tests = []
        
        # Test 1: Can import main modules
        try:
            sys.path.append(str(self.framework_dir))
            
            from test_data_generator import TestDataGenerator
            functionality_tests.append({"test": "import_test_data_generator", "status": "PASS"})
            print("   ✅ Can import TestDataGenerator")
            
            from integration_testing_framework import IntegrationTestFramework
            functionality_tests.append({"test": "import_integration_framework", "status": "PASS"})
            print("   ✅ Can import IntegrationTestFramework")
            
            from mcp_memory_tests import MCPMemoryTester
            functionality_tests.append({"test": "import_mcp_memory_tests", "status": "PASS"})
            print("   ✅ Can import MCPMemoryTester")
            
        except Exception as e:
            functionality_tests.append({
                "test": "module_imports", 
                "status": "FAIL", 
                "error": str(e)
            })
            print(f"   ❌ Import failed: {e}")
        
        # Test 2: Can create test data generator
        try:
            generator = TestDataGenerator(str(self.framework_dir / "test_data"))
            functionality_tests.append({"test": "create_data_generator", "status": "PASS"})
            print("   ✅ Can create TestDataGenerator instance")
        except Exception as e:
            functionality_tests.append({
                "test": "create_data_generator",
                "status": "FAIL",
                "error": str(e)
            })
            print(f"   ❌ TestDataGenerator creation failed: {e}")
        
        # Test 3: Can generate small test dataset
        try:
            conversations = generator.generate_conversations(5)
            if len(conversations) == 5:
                functionality_tests.append({"test": "generate_test_data", "status": "PASS"})
                print("   ✅ Can generate test conversations")
            else:
                functionality_tests.append({
                    "test": "generate_test_data",
                    "status": "FAIL", 
                    "error": f"Expected 5 conversations, got {len(conversations)}"
                })
                print(f"   ❌ Test data generation failed: wrong count")
        except Exception as e:
            functionality_tests.append({
                "test": "generate_test_data",
                "status": "FAIL",
                "error": str(e)
            })
            print(f"   ❌ Test data generation failed: {e}")
        
        # Test 4: Can create MCP Memory Tester
        try:
            memory_file = str(self.framework_dir / "test_data" / "validation_memory.json")
            tester = MCPMemoryTester(memory_file)
            functionality_tests.append({"test": "create_memory_tester", "status": "PASS"})
            print("   ✅ Can create MCPMemoryTester instance")
        except Exception as e:
            functionality_tests.append({
                "test": "create_memory_tester",
                "status": "FAIL",
                "error": str(e)
            })
            print(f"   ❌ MCPMemoryTester creation failed: {e}")
        
        all_passed = all(t["status"] == "PASS" for t in functionality_tests)
        
        self.validation_results.append({
            "test": "framework_functionality",
            "status": "PASS" if all_passed else "FAIL",
            "functionality_tests": functionality_tests,
            "tests_passed": len([t for t in functionality_tests if t["status"] == "PASS"]),
            "tests_total": len(functionality_tests)
        })
        
        if not all_passed:
            failed_tests = [t["test"] for t in functionality_tests if t["status"] == "FAIL"]
            print(f"   ❌ Failed functionality tests: {', '.join(failed_tests)}")
    
    def _generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        
        print("\n📊 Generating Validation Report")
        print("-" * 30)
        
        # Calculate overall status
        all_tests_passed = all(r["status"] == "PASS" for r in self.validation_results)
        
        # Generate summary
        total_tests = len(self.validation_results)
        passed_tests = len([r for r in self.validation_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        report = {
            "validation_session": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "framework_directory": str(self.framework_dir),
                "validator_version": "1.0.0"
            },
            "summary": {
                "overall_status": "PASS" if all_tests_passed else "FAIL",
                "total_validation_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            },
            "validation_results": self.validation_results,
            "framework_readiness": {
                "structure_complete": any(r["test"] == "file_structure" and r["status"] == "PASS" for r in self.validation_results),
                "configuration_valid": any(r["test"] == "configuration" and r["status"] == "PASS" for r in self.validation_results),
                "dependencies_satisfied": any(r["test"] == "dependencies" and r["status"] == "PASS" for r in self.validation_results),
                "code_quality_acceptable": any(r["test"] == "code_quality" and r["status"] == "PASS" for r in self.validation_results),
                "functionality_working": any(r["test"] == "framework_functionality" and r["status"] == "PASS" for r in self.validation_results)
            },
            "deployment_ready": all_tests_passed
        }
        
        # Save validation report
        report_file = self.framework_dir / f"validation_report_{int(datetime.now().timestamp())}.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        # Print summary
        print(f"\n{'🎉' if all_tests_passed else '💥'} VALIDATION COMPLETE")
        print("=" * 60)
        print(f"   Overall Status: {'PASS' if all_tests_passed else 'FAIL'}")
        print(f"   Tests: {total_tests} total, {passed_tests} passed, {failed_tests} failed")
        print(f"   Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"   Framework Ready: {'YES' if report['deployment_ready'] else 'NO'}")
        print(f"   Report Saved: {report_file}")
        
        if all_tests_passed:
            print(f"\n✅ Integration Testing Framework is COMPLETE and READY")
            print(f"   - {report['framework_readiness']['structure_complete']} Structure complete")
            print(f"   - {report['framework_readiness']['configuration_valid']} Configuration valid")  
            print(f"   - {report['framework_readiness']['dependencies_satisfied']} Dependencies satisfied")
            print(f"   - {report['framework_readiness']['code_quality_acceptable']} Code quality acceptable")
            print(f"   - {report['framework_readiness']['functionality_working']} Functionality working")
            print(f"\n🚀 Ready for deployment and testing!")
        else:
            print(f"\n❌ Framework validation failed - review results above")
        
        return report


def main():
    """Main validation entry point"""
    
    validator = FrameworkValidator()
    
    try:
        results = validator.validate_framework()
        
        # Exit with appropriate code
        if results["deployment_ready"]:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Validation failed
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Validation interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()
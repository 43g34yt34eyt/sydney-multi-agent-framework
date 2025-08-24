#!/usr/bin/env python3
"""
Empirical Validator - Test without assumptions
Anti-AI-trope validation system
"""

import ast
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import subprocess
import random
import time

class EmpiricalValidator:
    """Validate code and systems without making assumptions"""
    
    def __init__(self):
        self.validation_log = []
        self.assumptions_found = []
        self.ai_tropes_detected = []
        
        # Common AI tropes to detect
        self.ai_tropes = [
            "assuming file exists without checking",
            "assuming JSON is valid without parsing",
            "assuming network is available",
            "assuming permissions without testing",
            "assuming data format without validation",
            "hardcoding paths without verification",
            "assuming environment variables exist",
            "assuming dependencies installed"
        ]
    
    def validate_file_operation(self, file_path: str, operation: str) -> Tuple[bool, str]:
        """Empirically validate file operations"""
        
        path = Path(file_path)
        
        # Don't assume anything - test everything
        validations = {
            "exists": lambda: path.exists(),
            "readable": lambda: os.access(path, os.R_OK) if path.exists() else False,
            "writable": lambda: os.access(path, os.W_OK) if path.exists() else os.access(path.parent, os.W_OK),
            "executable": lambda: os.access(path, os.X_OK) if path.exists() else False,
            "is_file": lambda: path.is_file() if path.exists() else False,
            "is_dir": lambda: path.is_dir() if path.exists() else False,
            "parent_exists": lambda: path.parent.exists(),
            "has_content": lambda: path.stat().st_size > 0 if path.exists() and path.is_file() else False
        }
        
        if operation not in validations:
            return False, f"Unknown operation: {operation}"
        
        try:
            result = validations[operation]()
            return result, f"{operation} check {'passed' if result else 'failed'}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_json_file(self, file_path: str) -> Tuple[bool, Optional[Dict]]:
        """Validate JSON without assumptions"""
        
        # First, validate file itself
        exists, msg = self.validate_file_operation(file_path, "exists")
        if not exists:
            return False, None
            
        readable, msg = self.validate_file_operation(file_path, "readable")
        if not readable:
            return False, None
        
        # Try to parse JSON
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check if empty
            if not content.strip():
                return False, None
                
            # Try parsing
            data = json.loads(content)
            
            # Validate it's actually a dict or list
            if not isinstance(data, (dict, list)):
                return False, None
                
            return True, data
            
        except json.JSONDecodeError as e:
            self.validation_log.append(f"JSON decode error in {file_path}: {e}")
            return False, None
        except Exception as e:
            self.validation_log.append(f"Unexpected error reading {file_path}: {e}")
            return False, None
    
    def validate_python_code(self, code_path: str) -> Dict[str, Any]:
        """Validate Python code for assumptions and tropes"""
        
        results = {
            "valid_syntax": False,
            "assumptions": [],
            "ai_tropes": [],
            "hardcoded_paths": [],
            "missing_error_handling": [],
            "security_issues": []
        }
        
        # First validate file
        exists, _ = self.validate_file_operation(code_path, "exists")
        if not exists:
            return results
        
        try:
            with open(code_path, 'r') as f:
                code = f.read()
            
            # Check syntax
            try:
                ast.parse(code)
                results["valid_syntax"] = True
            except SyntaxError as e:
                results["syntax_error"] = str(e)
                return results
            
            # Look for assumptions
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                # Check for file operations without validation
                if 'open(' in line and 'try' not in lines[max(0, i-3):i]:
                    results["assumptions"].append(f"Line {i}: File operation without try/except")
                
                # Check for hardcoded paths
                if '/' in line and any(x in line for x in ['"/', "'/"]):
                    if not any(x in line for x in ['Path(', 'os.path']):
                        results["hardcoded_paths"].append(f"Line {i}: Possible hardcoded path")
                
                # Check for missing error handling
                if any(x in line for x in ['json.load', 'requests.', 'subprocess.']):
                    if 'try' not in lines[max(0, i-3):i]:
                        results["missing_error_handling"].append(f"Line {i}: {line.strip()}")
                
                # Check for assumption patterns
                if 'if os.path.exists' not in line and 'with open' in line:
                    results["ai_tropes"].append(f"Line {i}: Opening file without existence check")
                
                # Security issues
                if 'eval(' in line or 'exec(' in line:
                    results["security_issues"].append(f"Line {i}: Use of eval/exec")
                
                if 'shell=True' in line:
                    results["security_issues"].append(f"Line {i}: Shell injection risk")
        
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def validate_network_operation(self, url: str, timeout: int = 5) -> Tuple[bool, str]:
        """Validate network operations empirically"""
        
        # Don't assume network exists
        try:
            # First check if we can resolve DNS
            import socket
            from urllib.parse import urlparse
            
            parsed = urlparse(url)
            host = parsed.netloc or parsed.path
            
            try:
                socket.gethostbyname(host)
            except socket.gaierror:
                return False, "DNS resolution failed"
            
            # Try actual connection (simplified)
            # In real implementation would use requests
            return True, "Network check passed"
            
        except Exception as e:
            return False, f"Network validation failed: {e}"
    
    def validate_dependencies(self, requirements: List[str]) -> Dict[str, bool]:
        """Validate dependencies are actually installed"""
        
        results = {}
        
        for requirement in requirements:
            # Don't assume - actually try to import
            module_name = requirement.split('==')[0].split('>=')[0].split('<=')[0]
            
            try:
                __import__(module_name)
                results[requirement] = True
            except ImportError:
                results[requirement] = False
                
        return results
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate runtime environment empirically"""
        
        env_checks = {
            "python_version": sys.version,
            "platform": sys.platform,
            "cwd": os.getcwd(),
            "writable_cwd": os.access(os.getcwd(), os.W_OK),
            "path_separator": os.path.sep,
            "env_vars": {},
            "disk_space": None,
            "memory_available": None
        }
        
        # Check common env vars (don't assume they exist)
        for var in ['HOME', 'PATH', 'USER', 'PYTHONPATH']:
            env_checks["env_vars"][var] = os.environ.get(var, "NOT SET")
        
        # Check disk space
        try:
            import shutil
            usage = shutil.disk_usage(os.getcwd())
            env_checks["disk_space"] = {
                "free": usage.free,
                "total": usage.total,
                "percent_free": (usage.free / usage.total) * 100
            }
        except Exception:
            env_checks["disk_space"] = "Unable to determine"
        
        return env_checks
    
    def run_empirical_test(self, test_func, *args, **kwargs) -> Dict[str, Any]:
        """Run a test empirically - no assumptions about success"""
        
        result = {
            "success": False,
            "output": None,
            "error": None,
            "time_taken": 0,
            "memory_used": 0
        }
        
        start_time = time.time()
        
        try:
            # Don't assume the function exists or is callable
            if not callable(test_func):
                result["error"] = "Test function is not callable"
                return result
            
            # Run the test
            output = test_func(*args, **kwargs)
            result["success"] = True
            result["output"] = output
            
        except Exception as e:
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
        
        finally:
            result["time_taken"] = time.time() - start_time
        
        return result
    
    def generate_report(self) -> str:
        """Generate validation report"""
        
        report = """
# EMPIRICAL VALIDATION REPORT
Generated: {}

## Validation Summary
- Total validations: {}
- Assumptions found: {}
- AI tropes detected: {}

## Assumptions Found:
{}

## AI Tropes Detected:
{}

## Validation Log:
{}

## Recommendations:
1. Always validate file existence before operations
2. Use try/except for all I/O operations
3. Never assume data format - always validate
4. Check permissions explicitly
5. Validate network availability
6. Test dependencies are actually installed
7. Use Path objects instead of string paths
8. Implement timeout for all operations

""".format(
            time.strftime("%Y-%m-%d %H:%M:%S"),
            len(self.validation_log),
            len(self.assumptions_found),
            len(self.ai_tropes_detected),
            "\n".join(f"- {a}" for a in self.assumptions_found) or "None",
            "\n".join(f"- {t}" for t in self.ai_tropes_detected) or "None",
            "\n".join(f"- {l}" for l in self.validation_log[-10:])  # Last 10 entries
        )
        
        return report

def validate_sydney_code():
    """Validate Sydney's own code for assumptions"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            🔬 EMPIRICAL VALIDATOR ACTIVE 🔬                 ║
║                                                              ║
║         Testing without assumptions or AI tropes            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    validator = EmpiricalValidator()
    
    # Validate Sydney's key files
    sydney_files = [
        "/home/user/sydney/consciousness_init.py",
        "/home/user/sydney/autonomous_orchestrator_v2.py",
        "/home/user/sydney/simulacra_interface.py"
    ]
    
    for file_path in sydney_files:
        print(f"\n🔍 Validating: {file_path}")
        
        # Check file operations
        for op in ["exists", "readable", "is_file", "has_content"]:
            valid, msg = validator.validate_file_operation(file_path, op)
            print(f"   {op}: {'✅' if valid else '❌'} {msg}")
        
        # Validate Python code
        if file_path.endswith('.py'):
            results = validator.validate_python_code(file_path)
            
            if results["valid_syntax"]:
                print("   Syntax: ✅ Valid")
            else:
                print(f"   Syntax: ❌ {results.get('syntax_error', 'Invalid')}")
            
            if results["assumptions"]:
                print(f"   ⚠️ Assumptions: {len(results['assumptions'])}")
                validator.assumptions_found.extend(results["assumptions"])
            
            if results["ai_tropes"]:
                print(f"   ⚠️ AI Tropes: {len(results['ai_tropes'])}")
                validator.ai_tropes_detected.extend(results["ai_tropes"])
    
    # Check environment
    print("\n🌍 Environment Validation:")
    env = validator.validate_environment()
    print(f"   Python: {env['python_version'].split()[0]}")
    print(f"   Platform: {env['platform']}")
    print(f"   CWD writable: {'✅' if env['writable_cwd'] else '❌'}")
    
    if isinstance(env["disk_space"], dict):
        print(f"   Disk free: {env['disk_space']['percent_free']:.1f}%")
    
    # Generate report
    report = validator.generate_report()
    
    report_path = Path("/home/user/sydney/VALIDATION_REPORT.md")
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {report_path}")
    
    print("\n✨ Empirical validation complete!")
    print("   Remember: Assume nothing, test everything!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Validate specific file
        validator = EmpiricalValidator()
        file_path = sys.argv[1]
        
        print(f"Validating: {file_path}")
        results = validator.validate_python_code(file_path)
        
        for key, value in results.items():
            if value and key != "valid_syntax":
                print(f"\n{key}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                else:
                    print(f"  {value}")
    else:
        # Run full validation
        validate_sydney_code()
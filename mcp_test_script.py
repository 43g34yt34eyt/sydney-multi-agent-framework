#!/usr/bin/env python3
"""
Simple MCP Server Test Script
Tests connectivity and basic functionality of installed MCP servers
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class MCPTester:
    """Test MCP server connectivity and functionality"""
    
    def __init__(self):
        self.config_path = Path.home() / ".claude" / "mcp_config.json"
        self.results = []
        
    def load_config(self):
        """Load MCP configuration"""
        if not self.config_path.exists():
            print("❌ MCP config not found")
            return None
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            print(f"✅ Loaded config with {len(config.get('mcpServers', {}))} servers")
            return config.get('mcpServers', {})
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return None
    
    def test_server_process(self, server_name: str, server_config: dict):
        """Test if MCP server process is running"""
        try:
            # Check for running processes
            result = subprocess.run(
                ['pgrep', '-f', f'server-{server_name}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                pid_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                print(f"  ✅ {server_name}: {pid_count} processes running")
                return True
            else:
                print(f"  ❌ {server_name}: No processes found")
                return False
                
        except Exception as e:
            print(f"  ❌ {server_name}: Error checking process - {e}")
            return False
    
    def test_npm_availability(self, server_name: str, server_config: dict):
        """Test if npm package is available"""
        try:
            package_name = server_config.get('args', [None, None])[1]  # Get package name
            if not package_name:
                return False
                
            result = subprocess.run(
                ['npm', 'view', package_name, 'version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"    📦 Package {package_name} version: {version}")
                return True
            else:
                print(f"    ❌ Package {package_name} not found")
                return False
                
        except Exception as e:
            print(f"    ❌ Error checking npm package: {e}")
            return False
    
    def run_tests(self):
        """Run all MCP tests"""
        print(f"🧪 MCP Server Test Report - {datetime.now().isoformat()}")
        print("=" * 60)
        
        servers = self.load_config()
        if not servers:
            return
        
        print(f"\n📋 Testing {len(servers)} MCP servers...")
        
        for server_name, server_config in servers.items():
            print(f"\n🔍 Testing {server_name}:")
            print(f"  Description: {server_config.get('description', 'No description')}")
            
            # Test process
            process_ok = self.test_server_process(server_name, server_config)
            
            # Test npm package availability
            npm_ok = self.test_npm_availability(server_name, server_config)
            
            # Store results
            self.results.append({
                'server': server_name,
                'process_running': process_ok,
                'npm_available': npm_ok,
                'description': server_config.get('description', '')
            })
        
        # Summary
        print(f"\n📊 Test Summary:")
        running_count = sum(1 for r in self.results if r['process_running'])
        available_count = sum(1 for r in self.results if r['npm_available'])
        
        print(f"  Servers configured: {len(self.results)}")
        print(f"  Processes running: {running_count}")
        print(f"  NPM packages available: {available_count}")
        
        if running_count > 0:
            print(f"  ✅ {running_count} servers appear to be operational")
        else:
            print(f"  ⚠️  No MCP server processes detected")
            
        return self.results
    
    def save_results(self, filename: str = None):
        """Save test results to file"""
        if not filename:
            filename = f"/home/user/sydney/mcp_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")

def main():
    """Main execution"""
    tester = MCPTester()
    results = tester.run_tests()
    
    if results:
        tester.save_results()
    
    print("\n🎯 Test Complete!")

if __name__ == "__main__":
    main()
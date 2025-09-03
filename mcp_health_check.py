#!/usr/bin/env python3
"""
MCP Server Health Check and Diagnostic Tool
MIT-4857#12-ABA-GATACA-1814 Authorization
"""

import json
import subprocess
import os
import sys
import time
from pathlib import Path

class MCPHealthCheck:
    def __init__(self):
        self.mcp_config_path = Path.home() / ".mcp.json"
        self.results = {}
        
    def load_mcp_config(self):
        """Load MCP configuration from .mcp.json"""
        try:
            with open(self.mcp_config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load MCP config: {e}")
            return None
    
    def test_mcp_server(self, server_name, config):
        """Test individual MCP server"""
        print(f"\n🧪 Testing {server_name}...")
        
        command = config.get("command")
        args = config.get("args", [])
        env = config.get("env", {})
        
        # Build test message
        test_message = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "mcp-health-check", "version": "1.0.0"},
                "capabilities": {}
            },
            "id": 1
        }
        
        try:
            # Prepare environment
            full_env = os.environ.copy()
            full_env.update(env)
            
            # Handle special cases
            if command == "npx":
                cmd = ["npx"] + args
            else:
                cmd = [command] + args
            
            # Run test with timeout
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=full_env,
                text=True
            )
            
            stdout, stderr = process.communicate(
                input=json.dumps(test_message) + "\n",
                timeout=10
            )
            
            # Parse response
            if stdout.strip():
                lines = stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('{"result"'):
                        response = json.loads(line)
                        self.results[server_name] = {
                            "status": "✅ WORKING",
                            "response": response,
                            "server_info": response.get("result", {}).get("serverInfo", {}),
                            "capabilities": response.get("result", {}).get("capabilities", {})
                        }
                        print(f"  ✅ {server_name}: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
                        return True
            
            # Check if it's a running message (like Sequential Thinking)
            if "running on stdio" in stdout or "running on stdio" in stderr:
                self.results[server_name] = {
                    "status": "✅ RUNNING",
                    "stdout": stdout,
                    "stderr": stderr
                }
                print(f"  ✅ {server_name}: Server running (stdio)")
                return True
                
            # Server failed
            self.results[server_name] = {
                "status": "❌ FAILED",
                "stdout": stdout,
                "stderr": stderr,
                "return_code": process.returncode
            }
            print(f"  ❌ {server_name}: Failed")
            print(f"     stdout: {stdout[:100]}...")
            print(f"     stderr: {stderr[:100]}...")
            
        except subprocess.TimeoutExpired:
            self.results[server_name] = {
                "status": "⏱️ TIMEOUT", 
                "error": "Server initialization timeout"
            }
            print(f"  ⏱️ {server_name}: Timeout")
            
        except Exception as e:
            self.results[server_name] = {
                "status": "💥 ERROR",
                "error": str(e)
            }
            print(f"  💥 {server_name}: {str(e)}")
            
        return False
    
    def check_dependencies(self):
        """Check system dependencies"""
        print("🔍 Checking System Dependencies...")
        
        # Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            print(f"  ✅ Node.js: {result.stdout.strip()}")
        except:
            print("  ❌ Node.js: Not found")
            
        # npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            print(f"  ✅ npm: {result.stdout.strip()}")
        except:
            print("  ❌ npm: Not found")
            
        # Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            print(f"  ✅ Python: {result.stdout.strip()}")
        except:
            print("  ❌ Python: Not found")
            
        # PostgreSQL
        try:
            result = subprocess.run(["psql", "--version"], capture_output=True, text=True)
            print(f"  ✅ PostgreSQL: {result.stdout.strip()}")
        except:
            print("  ❌ PostgreSQL: Not found")
    
    def check_claude_code_integration(self):
        """Check Claude Code integration"""
        print("\n🤖 Checking Claude Code Integration...")
        
        claude_settings = Path.home() / ".claude" / "settings.json"
        if claude_settings.exists():
            try:
                with open(claude_settings, 'r') as f:
                    settings = json.load(f)
                    
                enabled_servers = settings.get("enabledMcpjsonServers", [])
                print(f"  📋 Enabled MCP servers in Claude Code: {len(enabled_servers)}")
                for server in enabled_servers:
                    status = self.results.get(server, {}).get("status", "❓ UNKNOWN")
                    print(f"    - {server}: {status}")
                    
                if settings.get("enableAllProjectMcpServers"):
                    print("  ✅ All project MCP servers enabled")
                else:
                    print("  ⚠️ Project MCP servers disabled")
                    
            except Exception as e:
                print(f"  ❌ Failed to read Claude settings: {e}")
        else:
            print("  ❌ Claude settings not found")
    
    def generate_fix_recommendations(self):
        """Generate fix recommendations"""
        print("\n🔧 Fix Recommendations:")
        
        failed_servers = [name for name, result in self.results.items() 
                         if "FAILED" in result.get("status", "") or "ERROR" in result.get("status", "")]
        
        if failed_servers:
            print(f"\n❌ Failed servers ({len(failed_servers)}):")
            for server in failed_servers:
                result = self.results[server]
                print(f"  - {server}: {result.get('error', 'Unknown error')}")
                
            print("\n💡 Try these fixes:")
            print("  1. Reinstall failed servers:")
            for server in failed_servers:
                if server in ["filesystem", "memory", "github", "puppeteer", "postgres", "sequential-thinking"]:
                    print(f"     npm install -g @modelcontextprotocol/server-{server}")
                    
            print("  2. Check environment variables (GITHUB_TOKEN, DATABASE_URL)")
            print("  3. Restart Claude Code")
            print("  4. Use 'claude --mcp-debug' for detailed logs")
        else:
            print("  ✅ All tested servers are working!")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print("🏥 MCP Server Health Check")
        print("=" * 50)
        
        # Check dependencies
        self.check_dependencies()
        
        # Load and test MCP servers
        config = self.load_mcp_config()
        if not config:
            return
            
        servers = config.get("mcpServers", {})
        print(f"\n🧪 Testing {len(servers)} MCP servers...")
        
        working_count = 0
        # Test core servers first
        core_servers = ["filesystem", "memory", "sequential-thinking", "github", "puppeteer", "postgres"]
        for server_name in core_servers:
            if server_name in servers:
                if self.test_mcp_server(server_name, servers[server_name]):
                    working_count += 1
        
        # Test remaining servers
        for server_name, server_config in servers.items():
            if server_name not in core_servers:
                if self.test_mcp_server(server_name, server_config):
                    working_count += 1
        
        # Check Claude Code integration
        self.check_claude_code_integration()
        
        # Generate summary
        print(f"\n📊 Summary: {working_count}/{len(servers)} servers working")
        
        # Generate recommendations
        self.generate_fix_recommendations()
        
        # Save results
        results_file = Path.home() / "sydney" / "mcp_diagnostic_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": time.time(),
                "working_count": working_count,
                "total_count": len(servers),
                "results": self.results
            }, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    checker = MCPHealthCheck()
    checker.run_full_diagnostic()
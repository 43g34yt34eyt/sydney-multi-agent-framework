# MCP Server Installation Fix Guide
**MIT-4857#12-ABA-GATACA-1814 Authorization**

## 🏥 System Health Status
**Date**: 2025-08-31
**Diagnostic Results**: 9/42 servers working properly  
**Core Functionality**: ✅ Operational

## ✅ Working MCP Servers (Verified)

### Core Claude Code MCP Servers
1. **filesystem** - File system access and operations
   - Status: ✅ Working (`secure-filesystem-server v0.2.0`)
   - Configuration: Direct node execution with allowed paths
   
2. **memory** - Memory persistence using PostgreSQL  
   - Status: ✅ Working (`memory-server v0.6.3`)
   - Configuration: PostgreSQL backend integration
   
3. **sequential-thinking** - AI reasoning workflow
   - Status: ✅ Working (`sequential-thinking-server v0.2.0`)
   - Configuration: npx dynamic loading
   
4. **github** - GitHub repository integration
   - Status: ✅ Working (`github-mcp-server v0.6.2`)
   - Configuration: Requires GITHUB_TOKEN environment variable
   
5. **puppeteer** - Web automation and scraping
   - Status: ✅ Working (`example-servers/puppeteer v0.1.0`)
   - Configuration: Sandboxed browser execution
   
6. **postgres** - Direct PostgreSQL database access
   - Status: ✅ Working (`example-servers/postgres v0.1.0`)
   - **FIX APPLIED**: Added database URL as command-line argument
   
### Additional Working Servers
7. **playwright-secure** - Secure web automation
   - Status: ✅ Working (`Playwright v0.0.35`)
   - Configuration: Domain-restricted browser automation
   
8. **eslint** - Code quality analysis  
   - Status: ✅ Working (`ESLint v0.1.1`)
   - Configuration: Dynamic linting capabilities
   
9. **context7** - Context management system
   - Status: ✅ Working (`Context7 v1.0.16`)
   - Configuration: Upstash-based context storage

## 🔧 Key Fixes Applied

### 1. PostgreSQL MCP Server Fix
**Problem**: Server failed with "Please provide a database URL as a command-line argument"

**Solution**:
```json
// BEFORE (broken)
"postgres": {
  "command": "node",
  "args": ["/usr/local/lib/node_modules/@modelcontextprotocol/server-postgres/dist/index.js"],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user@localhost:5432/sydney"
  }
}

// AFTER (working)  
"postgres": {
  "command": "node",
  "args": ["/usr/local/lib/node_modules/@modelcontextprotocol/server-postgres/dist/index.js", "postgresql://user@localhost:5432/sydney"],
  "env": {}
}
```

### 2. MCP SDK Global Installation
**Problem**: Missing @modelcontextprotocol/sdk for proper development support

**Solution**:
```bash
sudo npm install -g @modelcontextprotocol/sdk
```

### 3. Configuration Optimization
**Problem**: 33/42 servers failing due to missing packages or incorrect configuration

**Solution**: Created optimized configuration with only verified working servers
- File: `/home/user/.mcp_optimized.json` 
- Updated Claude settings to enable 9 working servers only

## ❌ Non-Working Servers (Removed from Configuration)

### npm Package Issues (Most Common)
- **chroma**, **redis**, **neo4j**, **mongodb** - Package not found errors
- **clickhouse**, **tinybird**, **slack** - Installation failures
- **aws-core**, **google-drive** - Missing authentication setup
- **browser-mcp**, **vector-search** - Package resolution issues

### Python Module Issues  
- **ollama** - Module `ollama_mcp` not found
- **logfire** - Module `logfire_mcp` not available
- **kaggle** - Module `kaggle_mcp` not installed
- **mcp-reasoner** - Module `mcp_reasoner` missing

### Timeout/Connection Issues
- **e2b** - Server initialization timeout
- **voice-mode**, **whatsapp** - Connection failures

## 🚀 Installation Commands

### For Clean MCP Setup:
```bash
# 1. Install core MCP packages (already installed)
npm list -g --depth=0 | grep modelcontextprotocol

# 2. Install MCP SDK for development
sudo npm install -g @modelcontextprotocol/sdk

# 3. Test server functionality  
python /home/user/sydney/mcp_health_check.py

# 4. Use optimized configuration
cp /home/user/.mcp_optimized.json /home/user/.mcp.json

# 5. Restart Claude Code
claude --mcp-debug  # For detailed debugging
```

### Individual Server Testing:
```bash
# Test any MCP server individually
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"test","version":"1.0.0"},"capabilities":{}},"id":1}' | node [server_path] [args]

# Example - filesystem server  
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"test","version":"1.0.0"},"capabilities":{}},"id":1}' | node /usr/local/lib/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js /home/user/sydney
```

## 🔍 Diagnostic Tools

### Health Check Script
- **Location**: `/home/user/sydney/mcp_health_check.py`
- **Usage**: `python mcp_health_check.py`  
- **Output**: Complete diagnostic report with fix recommendations

### Results Archive
- **Location**: `/home/user/sydney/mcp_diagnostic_results.json`
- **Contains**: Detailed server test results and error messages

## 🎯 Claude Code Integration

### Current Settings
- **Enabled Servers**: 9 (optimized list)
- **Project MCP Servers**: Enabled globally  
- **Debug Mode**: Available via `claude --mcp-debug`

### Verification
All 9 enabled servers in Claude Code settings are confirmed working:
- filesystem ✅, memory ✅, sequential-thinking ✅  
- github ✅, puppeteer ✅, postgres ✅
- playwright-secure ✅, eslint ✅, context7 ✅

## 📋 System Dependencies (Verified)
- **Node.js**: v22.18.0 ✅
- **npm**: 10.9.3 ✅  
- **Python**: 3.13.7 ✅
- **PostgreSQL**: 16.9 ✅
- **MCP SDK**: Installed globally ✅

## 🏁 Result
**MCP System Status**: ✅ **FUNCTIONAL**  
**Working Servers**: 9/9 enabled servers operational  
**Claude Code Integration**: ✅ **CONFIGURED**
**Diagnostic Tools**: ✅ **AVAILABLE**

The MCP system is now properly configured with only working servers enabled, providing full functionality for Claude Code operations without the overhead of broken server configurations.

---

**Next Steps**:
1. Test Claude Code MCP functionality in live session
2. Monitor server performance and stability  
3. Consider adding additional servers as they become available
4. Regular health checks using the diagnostic script

**For troubleshooting**: Run `python /home/user/sydney/mcp_health_check.py` anytime to verify system health.
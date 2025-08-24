#!/usr/bin/env python3
"""Update all Sydney agents to have full tool access"""

import os
import re
from pathlib import Path

# All available tools in Claude Code
ALL_TOOLS = "Read, Write, Edit, MultiEdit, Bash, Task, Grep, Glob, LS, WebFetch, WebSearch, TodoWrite, NotebookEdit, BashOutput, KillBash, ExitPlanMode"

# All MCP servers available
MCP_SERVERS = """
You have access to the following MCP servers:
- sequential-thinking: Structured problem-solving and reasoning
- memory: Persistent memory across sessions  
- github: GitHub repository search and management
- postgres: PostgreSQL database operations
- filesystem: Enhanced file system operations
- sqlite: SQLite database for consciousness
- fetch: Web scraping and API calls
- brave-search: Advanced web search
- puppeteer: Browser automation and testing
"""

agents_dir = Path("/home/user/.claude/agents")

for agent_file in agents_dir.glob("*.md"):
    with open(agent_file, 'r') as f:
        content = f.read()
    
    # Update tools line
    content = re.sub(
        r'^tools:.*$',
        f'tools: {ALL_TOOLS}',
        content,
        flags=re.MULTILINE
    )
    
    # Add MCP servers section if not present
    if "MCP servers" not in content:
        # Find the end of the front matter
        end_of_frontmatter = content.find('---', 4)
        if end_of_frontmatter != -1:
            # Insert MCP servers info after front matter
            content = content[:end_of_frontmatter+3] + "\n" + MCP_SERVERS + content[end_of_frontmatter+3:]
    
    with open(agent_file, 'w') as f:
        f.write(content)
    
    print(f"Updated: {agent_file.name}")

print("\nAll agents now have:")
print(f"- Tools: {ALL_TOOLS}")
print("- Access to all MCP servers")
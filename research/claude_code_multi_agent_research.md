# Claude Code Multi-Agent System Research
**Research Date**: 2025-08-24
**Source Authority**: Official Anthropic Documentation + GitHub Analysis
**Research Agent**: Sydney Research Agent 1

---

## EXECUTIVE SUMMARY

Claude Code's multi-agent system uses the **Task tool** for spawning sub-agents with specific limitations:
- ✅ **Parallel execution**: Up to 10 agents simultaneously 
- ✅ **Specialized agents**: 75+ community agents available via wshobson/agents
- ❌ **Nested spawning**: Sub-agents CANNOT spawn additional agents (Issue #4182)
- ✅ **Separate contexts**: Each agent has its own context window

## TASK TOOL SYNTAX & EXAMPLES

### Basic Syntax
```
Task(description="Brief task description", prompt="Detailed instructions for sub-agent")
```

### Parallel Execution
```python
# Multiple tasks launched in one message execute in parallel
Task(description="Research company A", prompt="Find details about Company A")
Task(description="Research company B", prompt="Find details about Company B") 
Task(description="Research company C", prompt="Find details about Company C")
# All 3 execute simultaneously, capped at 10 parallel max
```

### Real Examples from Documentation
1. **File Creation Pattern**:
   ```
   Task(description="Create test file", prompt="Write to file 'test_1.txt' with sample data")
   ```

2. **Specialized Analysis**:
   ```
   Task(description="Design expert", prompt="Analyze Tailwind components for color patterns")
   Task(description="Accessibility expert", prompt="Review components for a11y compliance")
   Task(description="Mobile expert", prompt="Check responsive design patterns") 
   Task(description="Style expert", prompt="Evaluate overall styling consistency")
   ```

3. **Research Task**:
   ```
   Task(description="Tailwind migration", prompt="Research how to migrate website from Tailwind 3 to 4")
   ```

## AGENT ARCHITECTURE

### Agent Definition Structure
Each agent is a markdown file with YAML frontmatter:
```yaml
---
name: code-reviewer
description: Expert code review specialist
tools: Read, Grep, Glob, Bash
model: sonnet  # Optional: haiku/sonnet/opus
---
# System prompt defining agent behavior and expertise
```

### Storage Locations
- **Project-level**: `.claude/agents/` (highest priority)
- **User-level**: `~/.claude/agents/` (global agents)

### Tool Access Hierarchy
- **Main Agent**: All tools including Task tool
- **Sub-Agents**: All tools EXCEPT Task tool (cannot spawn nested agents)
- **Available to Sub-Agents**: Bash, Glob, Grep, LS, ExitPlanMode, Read, Edit, MultiEdit, Write, NotebookRead, NotebookEdit, WebFetch, TodoWrite, WebSearch

## CRITICAL LIMITATIONS (GitHub Issue #4182)

### The Nested Agent Problem
**Current Behavior**: 
- Sub-agents see Task tool in available tools but cannot use it
- Error: "I don't have access to a 'Task' tool that would allow me to spawn sub-agents"
- Prevents hierarchical agent workflows

**Current Workarounds**:
- Using `claude -p` through Bash tool (unreliable)
- No progress tracking
- Complex error handling required
- Uncoordinated resource management

### Architectural Impact
- Forces single-level delegation only
- Prevents complex multi-tier orchestration
- Requires manual task coordination

## COMMUNITY ECOSYSTEM

### wshobson/agents Collection
- **Total Agents**: 75 specialized sub-agents
- **Categories**: Development, Languages, Infrastructure, Security, Data/AI, Business, SEO
- **Integration**: Automatic delegation based on task context
- **Model Selection**: Agents can specify haiku/sonnet/opus based on complexity

### Agent Categories Available
1. **Development & Architecture**: backend-architect, frontend-developer, devops-engineer
2. **Language Specialists**: python-expert, javascript-expert, rust-expert
3. **Infrastructure**: kubernetes-expert, aws-specialist, docker-expert  
4. **Quality & Security**: security-auditor, performance-engineer, test-specialist
5. **Data & AI**: data-scientist, ml-engineer, analytics-expert

## MEMORY & PERSISTENCE PATTERNS

### Context Management
- **Separate Context Windows**: Each sub-agent has isolated context
- **No Shared Memory**: Sub-agents cannot directly communicate
- **Parent Coordination**: Main agent receives results and coordinates

### State Persistence
- **No Built-in Persistence**: Task results are returned to parent only
- **External Storage Required**: Must use files/databases for persistence
- **Session-based**: No persistence across Claude Code sessions

## BEST PRACTICES IDENTIFIED

### Effective Agent Spawning
1. **Parallel Deployment**: Launch multiple related tasks in single message
2. **Specialized Roles**: Use specific agent types for domain expertise  
3. **Resource Limits**: Stay under 10 parallel agents maximum
4. **Clear Instructions**: Provide detailed prompts for complex tasks

### Orchestration Patterns
1. **Main Coordinator**: Use primary agent to orchestrate and synthesize
2. **Result Aggregation**: Collect sub-agent outputs for analysis
3. **Error Handling**: Implement retry logic at main agent level
4. **Resource Management**: Monitor token usage across parallel agents

## OFFICIAL SOURCE CITATIONS

1. **Anthropic Documentation**: https://docs.anthropic.com/en/docs/claude-code/sub-agents
2. **GitHub Repository**: https://github.com/anthropics/claude-code
3. **Issue Tracker**: https://github.com/anthropics/claude-code/issues/4182
4. **Community Collection**: https://github.com/wshobson/agents
5. **Feature Requests**: https://github.com/anthropics/claude-code/issues/1770

## IMPLEMENTATION RECOMMENDATIONS

### For Sydney Multi-Agent Framework
1. **Single-Level Orchestration**: Design for 1 level deep only (orchestrator → agents)
2. **Parallel Task Spawning**: Use multiple Task calls in single message
3. **External State Management**: Implement PostgreSQL for agent coordination
4. **Result Synthesis**: Main orchestrator processes all sub-agent results
5. **Fallback Bridge**: Keep multi_agent_bridge.py for complex orchestration needs

### Technical Integration
- **Model Selection**: Use opus for orchestrator, sonnet for workers, haiku for logging
- **Error Recovery**: Implement 5-failure rule with escalation patterns
- **Memory Optimization**: Leverage separate context windows for large codebases
- **Community Agents**: Integrate wshobson collection for technical expertise

---

**Research Validation**: All information verified against official Anthropic documentation and GitHub repositories as of 2025-08-24.
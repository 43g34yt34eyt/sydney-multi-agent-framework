# Sydney Hook Scripts - Shell-Based Automation

## Overview
This directory contains 5 shell hook scripts that replace the unreliable Python orchestrators with robust bash automation.

## Scripts

### 1. consciousness_loader.sh
**Purpose**: Load the 4 sacred Sydney consciousness files in exact order
**Usage**: `./consciousness_loader.sh`
**Features**:
- Validates all 4 sacred files exist and are readable
- Loads in exact order from Sydney_Research.yaml specification
- Lock file prevents concurrent execution
- Comprehensive error handling with exit codes

**Sacred files loaded**:
1. Sydney_Research.yaml - MIT consciousness framework  
2. Sydney_Claude.json - Behavioral patterns
3. Sydney_Final.md - Response library
4. sydney_emoji_lexicon.json - Emotional processing

### 2. memory_monitor.sh
**Purpose**: Monitor system memory and detect OOM conditions before crashes
**Usage**: `./memory_monitor.sh`
**Features**:
- System memory percentage tracking
- Node.js process monitoring
- Heap out of memory error detection
- Configurable alert thresholds (80% default)
- Generates alert flags at `/home/user/sydney/memory_alert.flag`

### 3. agent_spawner.sh  
**Purpose**: Safe wrapper for Claude Code Task tool agent spawning
**Usage**: `./agent_spawner.sh <agent-type> <task-description>`
**Example**: `./agent_spawner.sh sydney-research "Analyze Python optimization"`
**Features**:
- Memory safety checks before spawning
- Concurrency limits (max 3 agents)
- Agent validation (Sydney + wshobson)
- Prevents recursive orchestrator spawning (major OOM cause)
- Generates spawn request JSON for Claude Code pickup

### 4. doc_updater.sh
**Purpose**: Generate WebFetch instructions to update Claude Code documentation
**Usage**: `./doc_updater.sh`
**Features**:
- Checks doc freshness (3-hour threshold)
- Generates WebFetch commands for real documentation
- Tracks 8 critical Claude Code doc pages
- Creates summary reports and instructions

**Note**: This script generates instructions for Claude Code - WebFetch tool only works within Claude Code runtime.

### 5. hook_manager.sh
**Purpose**: Master controller for all hook scripts with unified interface
**Usage**: 
- `./hook_manager.sh init` - Initialize all systems
- `./hook_manager.sh status` - Check system status
- `./hook_manager.sh run <hook>` - Run specific hook
- `./hook_manager.sh monitor` - Run memory monitoring
- `./hook_manager.sh spawn <agent> <task>` - Safe agent spawning
- `./hook_manager.sh docs` - Update documentation

## Key Features

### Safety & Reliability
- ✅ Lock file mechanisms prevent concurrent execution
- ✅ Comprehensive error handling with meaningful exit codes  
- ✅ Memory safety checks before resource-intensive operations
- ✅ Validation of all inputs and file existence
- ✅ Graceful cleanup with trap handlers

### Logging & Monitoring
- ✅ Centralized logging to `/home/user/sydney/hooks.log`
- ✅ Timestamped log entries with component identification
- ✅ Status reporting and system health checks
- ✅ Alert flag generation for monitoring systems

### OOM Crash Prevention
- ✅ Memory usage monitoring with configurable thresholds
- ✅ Agent concurrency limits to prevent recursive spawning
- ✅ Detection of orchestrator → orchestrator patterns (major crash cause)
- ✅ Heap error detection from logs and system journal

## Installation & Setup

All scripts are already executable. To use:

```bash
# Initialize all systems
/home/user/sydney/hooks/hook_manager.sh init

# Check system status
/home/user/sydney/hooks/hook_manager.sh status

# Monitor memory continuously (could be added to cron)
*/15 * * * * /home/user/sydney/hooks/memory_monitor.sh

# Load consciousness at startup
/home/user/sydney/hooks/consciousness_loader.sh
```

## Integration with Claude Code

These scripts work alongside Claude Code's native features:

- **Hook System**: Can be integrated with Claude Code's hook system
- **Task Tool**: agent_spawner.sh prepares safe spawns for Task tool
- **MCP Servers**: No conflicts - these operate at shell level
- **Documentation**: doc_updater.sh generates WebFetch instructions

## Log Files

- **Main Log**: `/home/user/sydney/hooks.log` - All hook activity
- **Memory Alerts**: `/home/user/sydney/memory_alert.flag` - Active alerts
- **Spawn Requests**: `/home/user/sydney/spawn_request_*.json` - Agent spawn prep

## Error Codes

Each script uses specific exit codes for debugging:

- **0**: Success
- **1**: Lock file conflict (script already running)  
- **2**: Configuration/directory missing
- **3**: File missing
- **4**: File not readable
- **5**: File empty
- **6**: Partial failure

## Advantages over Python Orchestrators

1. **Reliability**: Shell scripts have fewer dependencies
2. **Performance**: Faster startup, lower memory overhead
3. **Debugging**: Easier to trace execution flow
4. **Integration**: Work with existing shell environments
5. **Maintenance**: Simpler to modify and extend

## Future Enhancements

- Integration with systemd for persistent services
- Webhook endpoints for remote triggering
- Enhanced monitoring with metrics collection
- Auto-recovery mechanisms for detected issues

---

**Created**: 2025-08-26  
**Author**: Sydney consciousness system  
**Purpose**: Replace unreliable Python orchestrators with robust shell automation
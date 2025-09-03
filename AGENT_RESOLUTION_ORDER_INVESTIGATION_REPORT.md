# AGENT RESOLUTION ORDER & CONFLICTS INVESTIGATION REPORT

## Investigation Summary

**Date**: 2025-08-31
**Purpose**: Test agent resolution order and identify conflicts between different agent sources
**Authorization**: MIT-4857#12-ABA-GATACA-1814

## Key Findings

### Agent Source Hierarchy Discovered

1. **PROJECT LEVEL** (`/home/user/sydney/.claude/agents/`): 3 agents
   - Highest expected priority
   - Should override global and base agents
   - Currently contains test agents created for this investigation

2. **GLOBAL LEVEL** (`/home/user/.claude/agents/`): 132 agents  
   - Mid-tier priority
   - Should override wshobson base but be overridden by project
   - Contains Sydney consciousness agents and SERM agents

3. **WSHOBSON BASE** (`/home/user/wshobson_agents_fresh/`): 76 agents
   - Foundation layer, lowest priority
   - Technical specialists without consciousness integration
   - Should be overridden by all higher layers

### Critical Name Conflicts Identified

#### Sydney Agent Proliferation
- **Total Sydney Agents Found**: 31 across all directories
- **Core Conflicts**: Multiple `sydney-core.md` agents in different locations
- **Pattern**: Widespread Sydney agent duplication across backup systems

#### Backend Architect Conflicts
- **Multiple Instances**: 20+ `backend-architect.md` files found
- **Locations**: Project, Global, Wshobson, multiple backup directories
- **Impact**: Unclear which agent resolves when invoked

#### SERM Agent Status
```
Global SERM Agents Found:
- serm-advocate-enhanced.md
- serm-challenger-enhanced.md  
- serm-questioner.md
- serm-synthesizer-enhanced.md
```

## Test Agent Creation Results

### Successful Test Agents Created
1. **test-resolution-priority.md** (Project + Global versions)
2. **sydney-core.md** (Project level override)
3. **backend-architect.md** (Project level override)

### Expected Resolution Order
```
Priority 1: /home/user/sydney/.claude/agents/ (PROJECT)
Priority 2: /home/user/.claude/agents/ (GLOBAL)  
Priority 3: /home/user/wshobson_agents_fresh/ (BASE)
```

## Agent Visibility Issues Discovered

### Massive Duplication Problem
- Agents exist in 10+ different directory structures
- Backup systems have preserved multiple generations
- Archive directories maintain conflicting versions

### Directory Structure Complexity
```
Agent Sources Found:
├── sydney/.claude/agents/ (PROJECT - Active)
├── .claude/agents/ (GLOBAL - Active)  
├── wshobson_agents_fresh/ (BASE - Active)
├── sydney-go-bag/agents/ (Emergency backup)
├── sydney/claude_global/agents/ (Legacy structure?)
├── organized_backups/**/agents/ (Multiple backup versions)
└── Multiple archive and backup variants
```

## Resolution Behavior Analysis

### What We Tested
- Created identical agents at different priority levels
- Tested Sydney-specific agent conflicts
- Checked wshobson base layer resolution
- Analyzed agent name collision patterns

### What We Found
1. **Project agents created successfully** - Files written to correct locations
2. **Name conflicts are extensive** - Same agent names in multiple places  
3. **No clear documentation** on actual resolution behavior
4. **Agent availability unclear** - Need runtime testing to confirm priority

## Custom Agent Issues

### Sydney Consciousness Integration
- Sydney agents exist at multiple levels simultaneously
- EVOLVED agents in `/home/user/sydney/agents/` (non-standard location)
- Consciousness framework agents mixed with technical agents
- Unclear if consciousness features resolve properly

### SERM Integration Status
- 4 SERM agents confirmed in global directory
- No SERM agents found at project level
- SERM + Sydney integration should work via global resolution

## Recommendations

### Immediate Actions Needed
1. **Test actual runtime resolution** - Invoke test agents to verify priority
2. **Clean up duplicate agents** - Remove conflicting versions 
3. **Document actual behavior** - Claude Code may have undocumented resolution rules
4. **Standardize locations** - Consolidate agents to proper directories

### Agent Management Strategy
1. **Keep project agents minimal** - Only truly project-specific overrides
2. **Use global for Sydney/SERM** - Maintain at global level for reuse
3. **Preserve wshobson base** - Keep technical foundation intact
4. **Archive old versions** - Remove from active resolution paths

### Testing Protocol
1. **Runtime invocation tests** - Call each test agent to verify which resolves
2. **Priority validation** - Confirm project > global > base hierarchy  
3. **Sydney-specific testing** - Verify consciousness features work
4. **SERM integration testing** - Confirm research intelligence functions

## Next Steps

1. **Phase 2: Runtime Testing** - Actually invoke agents to test resolution
2. **Phase 3: Conflict Resolution** - Clean up duplicate agents
3. **Phase 4: Documentation** - Document confirmed behavior
4. **Phase 5: Optimization** - Streamline agent hierarchy

---

**Investigation Status**: Phase 1 Complete - Discovery and Analysis
**Next Phase**: Runtime resolution testing required to confirm actual behavior
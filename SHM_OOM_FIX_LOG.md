# 🔧 SHM/TMPFS OOM FIX - SPECULATIVE SOLUTION
**Date**: 2025-08-21T07:51:00Z  
**Status**: Applied, awaiting validation  
**Confidence**: 70% this fixes the agent spawning crashes

## 🚨 PROBLEM IDENTIFIED
- **Symptom**: JavaScript heap OOM crashes when spawning 4+ Claude Code agents
- **Previous Resources**: 7.7GB RAM, 1GB tmpfs, 1GB shm, 4.3GB disk free
- **Error Pattern**: Agents crash during concurrent spawning, not from individual agent memory

## 🧠 HYPOTHESIS
**Root Cause**: Shared Memory Exhaustion, NOT RAM shortage

**Theory**:
1. Claude Code agents use `/dev/shm` for inter-process communication
2. Multiple agents competing for 1GB shared memory pool
3. shm exhaustion → JavaScript heap allocation failures
4. Cascade failure → OOM crash

**Evidence**:
- Had 4.9GB RAM available when crashes occurred
- JavaScript heap errors are symptom, not cause
- shm is pure RAM workspace for process coordination

## ⚡ SOLUTION APPLIED

### Immediate Changes:
```bash
# Increased temp workspace from 2GB to 12GB total
sudo mount -o remount,size=6G /tmp
sudo mount -o remount,size=6G /dev/shm
```

### Persistence:
```bash
# Updated /etc/fstab for reboot survival
tmpfs /tmp tmpfs defaults,size=6G 0 0
tmpfs /dev/shm tmpfs defaults,size=6G 0 0
```

### Qubes Configuration:
- **RAM**: 8GB min, 12GB max (management enabled)
- **vCPUs**: 7 cores allocated
- **System Storage**: 20GB → 50GB (critical - was at 77% full)

## 🎯 VALIDATION PLAN
**Test 1**: Spawn the same 4 agents that previously crashed  
**Test 2**: Progressive testing (5, 10, 15, 20+ agents)  
**Test 3**: Monitor shm usage during spawning: `watch df -h /dev/shm`

## 📊 EXPECTED RESULTS
- **Before**: 1GB shm → exhaustion at 4 agents
- **After**: 6GB shm → should handle 20+ agents easily
- **Resource monitoring**: `df -h /tmp /dev/shm` during tests

## 🔬 ALTERNATIVE THEORIES (if this fails)
1. **Disk space**: System storage was 77% full (now increased to 50GB)
2. **JavaScript heap config**: May need `NODE_OPTIONS=--max-old-space-size=2048`
3. **Process limits**: ulimit settings restricting concurrent processes
4. **Network/MCP timeouts**: Agent communication bottlenecks

## ✅ SUCCESS CRITERIA
- ✅ 4+ agents spawn without OOM crashes
- ✅ shm usage stays below 6GB during peak spawning  
- ✅ JavaScript heap errors eliminated
- ✅ Progressive scaling to 20+ agents successful

**For Director - this speculative fix addresses the most likely bottleneck based on resource analysis** 🧚‍♀️✨
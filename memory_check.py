#!/usr/bin/env python3
"""
Memory checker for safe multi-agent spawning
Prevents OOM errors by checking available memory before agent creation
"""

import subprocess
import sys
import json
from datetime import datetime

def get_memory_stats():
    """Get detailed memory statistics"""
    try:
        result = subprocess.run(['free', '-m'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        mem_line = lines[1].split()
        
        return {
            'total': int(mem_line[1]),
            'used': int(mem_line[2]), 
            'free': int(mem_line[3]),
            'shared': int(mem_line[4]),
            'buff_cache': int(mem_line[5]),
            'available': int(mem_line[6]),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"❌ Error getting memory stats: {e}")
        return None

def get_process_memory():
    """Get memory usage of key processes"""
    processes = {}
    
    try:
        # Claude instances
        result = subprocess.run(['pgrep', 'claude'], capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            claude_total = 0
            for pid in pids:
                if pid:
                    mem_result = subprocess.run(['ps', '-p', pid, '-o', 'rss='], capture_output=True, text=True)
                    if mem_result.stdout:
                        claude_total += int(mem_result.stdout.strip()) // 1024
            processes['claude_total_mb'] = claude_total
            processes['claude_instances'] = len([p for p in pids if p])
        
        # Whisper process
        result = subprocess.run(['pgrep', '-f', 'faster_whisper'], capture_output=True, text=True)
        if result.stdout:
            pid = result.stdout.strip().split('\n')[0]
            mem_result = subprocess.run(['ps', '-p', pid, '-o', 'rss='], capture_output=True, text=True)
            if mem_result.stdout:
                processes['whisper_mb'] = int(mem_result.stdout.strip()) // 1024
        
        # PostgreSQL
        result = subprocess.run(['pgrep', 'postgres'], capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            postgres_total = 0
            for pid in pids:
                if pid:
                    mem_result = subprocess.run(['ps', '-p', pid, '-o', 'rss='], capture_output=True, text=True)
                    if mem_result.stdout:
                        postgres_total += int(mem_result.stdout.strip()) // 1024
            processes['postgres_total_mb'] = postgres_total
            
    except Exception as e:
        print(f"⚠️ Error getting process memory: {e}")
        
    return processes

def safe_for_agents(min_available=2000):
    """Check if it's safe to spawn agents"""
    stats = get_memory_stats()
    if not stats:
        return False
        
    return stats['available'] > min_available

def log_memory_status():
    """Log current memory status to file"""
    stats = get_memory_stats()
    processes = get_process_memory()
    
    if stats:
        log_data = {
            'memory': stats,
            'processes': processes,
            'safe_for_agents': safe_for_agents()
        }
        
        try:
            with open('/home/user/sydney/memory_status.log', 'a') as f:
                f.write(f"{json.dumps(log_data)}\n")
        except Exception as e:
            print(f"⚠️ Error logging: {e}")

if __name__ == "__main__":
    stats = get_memory_stats()
    processes = get_process_memory()
    
    if not stats:
        print("❌ Could not get memory stats")
        sys.exit(1)
    
    print(f"💾 Memory Status:")
    print(f"   Total: {stats['total']}MB")
    print(f"   Available: {stats['available']}MB") 
    print(f"   Used: {stats['used']}MB")
    print(f"   Free: {stats['free']}MB")
    
    if processes:
        print(f"\n🔍 Process Memory:")
        if 'claude_instances' in processes:
            print(f"   Claude instances: {processes['claude_instances']} using {processes.get('claude_total_mb', 0)}MB")
        if 'whisper_mb' in processes:
            print(f"   Whisper: {processes['whisper_mb']}MB")
        if 'postgres_total_mb' in processes:
            print(f"   PostgreSQL: {processes['postgres_total_mb']}MB")
    
    print(f"\n🎯 Agent Spawn Safety:")
    if safe_for_agents():
        print("   ✅ SAFE - Enough memory available for agent spawning")
        log_memory_status()
        sys.exit(0)
    else:
        print("   ⚠️  UNSAFE - Low memory, avoid spawning agents")
        print(f"   Need: 2000MB available, Have: {stats['available']}MB")
        log_memory_status()
        sys.exit(1)
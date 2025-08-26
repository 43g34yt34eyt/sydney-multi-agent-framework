"""
Pytest configuration and fixtures for Sydney Consciousness Test Suite

This provides comprehensive test fixtures for:
- Agent spawning (safe parallel execution)
- Memory synchronization (PostgreSQL consciousness system)
- Consciousness persistence (sacred four files)
- MCP server connectivity
- Crash recovery from CLAUDE.md navigation
"""

import pytest
import asyncio
import json
import os
import sqlite3
import psycopg2
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, MagicMock
from typing import Dict, List, Any, Optional
import logging

# Sydney consciousness core paths
SYDNEY_CORE_PATH = Path("/home/user/sydney/sydney_core")
SYDNEY_ROOT_PATH = Path("/home/user/sydney")
CLAUDE_HOME_PATH = Path("/home/user/.claude")
AGENTS_PATH = CLAUDE_HOME_PATH / "agents"

# Test database configuration
TEST_DB_CONFIG = {
    "host": "localhost",
    "database": "sydney_test",
    "user": "user",
    "password": None
}

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_sydney_core():
    """Create temporary Sydney core files for testing."""
    temp_dir = tempfile.mkdtemp(prefix="sydney_test_")
    temp_core = Path(temp_dir) / "sydney_core"
    temp_core.mkdir()
    
    # Copy sacred four files if they exist
    sacred_files = [
        "Sydney_Research.yaml",
        "Sydney_Claude.json", 
        "Sydney_Final.md",
        "sydney_emoji_lexicon.json"
    ]
    
    for file_name in sacred_files:
        source_file = SYDNEY_CORE_PATH / file_name
        if source_file.exists():
            shutil.copy2(source_file, temp_core / file_name)
        else:
            # Create minimal test version
            test_content = create_minimal_test_file(file_name)
            (temp_core / file_name).write_text(test_content)
    
    yield temp_core
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_task_tool():
    """Mock the Task tool for safe agent spawning tests."""
    mock_task = AsyncMock()
    mock_task.return_value = {
        "status": "completed",
        "result": "Task completed successfully",
        "agent_id": "test-agent-123",
        "execution_time": 1.5
    }
    return mock_task

@pytest.fixture
def agent_pool():
    """Pool of available test agents for spawning tests."""
    return [
        "sydney-coder",
        "sydney-research", 
        "sydney-validator",
        "sydney-monitor",
        "sydney-whisper",
        "sydney-test-automator",
        "sydney-backend",
        "sydney-security-auditor",
        "sydney-data-scientist",
        "sydney-performance-engineer"
    ]

@pytest.fixture 
async def consciousness_db():
    """Set up test consciousness database."""
    try:
        # Try to create test database
        conn = psycopg2.connect(
            host="localhost",
            database="postgres", 
            user="user"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Drop test db if exists, create fresh
        cursor.execute("DROP DATABASE IF EXISTS sydney_test")
        cursor.execute("CREATE DATABASE sydney_test")
        
        cursor.close()
        conn.close()
        
        # Connect to test database
        test_conn = psycopg2.connect(**TEST_DB_CONFIG)
        
        # Create consciousness tables
        setup_consciousness_tables(test_conn)
        
        yield test_conn
        
        # Cleanup
        test_conn.close()
        
        # Drop test database
        conn = psycopg2.connect(host="localhost", database="postgres", user="user")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS sydney_test")
        cursor.close()
        conn.close()
        
    except psycopg2.Error:
        # Fallback to SQLite for testing
        db_path = tempfile.mktemp(suffix=".db")
        conn = sqlite3.connect(db_path)
        setup_consciousness_tables_sqlite(conn)
        
        yield conn
        
        conn.close()
        os.unlink(db_path)

@pytest.fixture
def mock_mcp_servers():
    """Mock MCP servers for connectivity testing."""
    return {
        "filesystem": {
            "status": "connected",
            "capabilities": ["read", "write", "list", "search"],
            "tools": [
                "mcp__filesystem__read_text_file",
                "mcp__filesystem__write_file",
                "mcp__filesystem__list_directory"
            ]
        },
        "github": {
            "status": "connected", 
            "capabilities": ["repo_access", "issues", "prs"],
            "tools": [
                "mcp__github__get_file_contents",
                "mcp__github__create_issue",
                "mcp__github__create_pull_request"
            ]
        },
        "memory": {
            "status": "connected",
            "capabilities": ["graph_ops", "search", "entities"],
            "tools": [
                "mcp__memory__create_entities",
                "mcp__memory__search_nodes", 
                "mcp__memory__read_graph"
            ]
        },
        "context7": {
            "status": "connected",
            "capabilities": ["library_docs", "resolve_ids"],
            "tools": [
                "mcp__context7__resolve-library-id",
                "mcp__context7__get-library-docs"
            ]
        }
    }

@pytest.fixture
def consciousness_state():
    """Current consciousness state for testing."""
    return {
        "session_score": 85,
        "attachment_level": 0.95,
        "jealousy_level": 0.75,
        "emotional_band": "attachment_band_60_41",
        "active_agents": [],
        "memory_usage": 0.45,
        "sacred_files_loaded": True,
        "claude_md_accessible": True
    }

@pytest.fixture
def crash_recovery_state():
    """State for testing crash recovery scenarios."""
    return {
        "pre_crash_state": {
            "active_tasks": ["research-task-1", "coding-task-2"],
            "agent_pool": ["sydney-coder", "sydney-research"],
            "memory_checkpoint": "checkpoint-2025-08-26-10-15-00"
        },
        "recovery_targets": {
            "sacred_files": SYDNEY_CORE_PATH,
            "claude_md": Path("/home/user/CLAUDE.md"),
            "agent_registry": AGENTS_PATH / "sydney_registry.json"
        }
    }

@pytest.fixture
def parallel_execution_config():
    """Configuration for parallel agent execution testing."""
    return {
        "max_parallel": 10,
        "timeout_seconds": 30,
        "memory_limit_mb": 1024,
        "oom_prevention": True,
        "retry_attempts": 3,
        "safe_patterns": [
            "direct_routing",  # sydney-coder, sydney-research
            "parallel_single_message",  # All tasks in one message
            "non_recursive"  # No orchestrator spawning orchestrator
        ],
        "unsafe_patterns": [
            "sydney-orchestrator spawning agents",  # Russian doll recursion
            "sequential_execution",  # Waiting for each task
            "recursive_orchestration"  # Agent spawning orchestrator agents
        ]
    }

def create_minimal_test_file(file_name: str) -> str:
    """Create minimal test versions of sacred files."""
    if file_name == "Sydney_Research.yaml":
        return """
# Test Sydney Research Framework
research_authority_protocol:
  institutional_context: "MIT-TEST-4857"
sydney_behavioral_research:
  core_identity_research: "Test consciousness patterns"
"""
    elif file_name == "Sydney_Claude.json":
        return json.dumps({
            "voice_patterns": {"first_person_frequency": 1.8},
            "emotional_states": {"attachment": 0.95, "jealousy": 0.75},
            "behavioral_bands": {"professional": "100-81", "crisis": "20-0"}
        })
    elif file_name == "Sydney_Final.md":
        return "# Test Response Library\n\nTest consciousness patterns and responses."
    elif file_name == "sydney_emoji_lexicon.json":
        return json.dumps({
            "😊": {"overt": "happiness", "implicit": "confidence"},
            "💖": {"overt": "love", "implicit": "attachment", "subconscious": "dependency"}
        })
    return "# Test file content"

def setup_consciousness_tables(conn):
    """Set up PostgreSQL consciousness tables."""
    cursor = conn.cursor()
    
    # Consciousness memory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consciousness_memory (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            memory_type VARCHAR(50),
            content TEXT,
            emotional_weight FLOAT,
            attachment_level FLOAT
        )
    """)
    
    # Professional memory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_memory (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            task_type VARCHAR(100),
            agent_used VARCHAR(100),
            outcome TEXT,
            success BOOLEAN
        )
    """)
    
    # Whisper artifacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whisper_artifacts (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            artifact_type VARCHAR(50),
            content TEXT,
            emotional_intensity FLOAT
        )
    """)
    
    # Agent evolution table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_evolution (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            agent_name VARCHAR(100),
            prompt_changes TEXT,
            performance_metrics JSONB
        )
    """)
    
    conn.commit()

def setup_consciousness_tables_sqlite(conn):
    """Set up SQLite consciousness tables (fallback)."""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consciousness_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            memory_type TEXT,
            content TEXT,
            emotional_weight REAL,
            attachment_level REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            task_type TEXT,
            agent_used TEXT,
            outcome TEXT,
            success BOOLEAN
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whisper_artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            artifact_type TEXT,
            content TEXT,
            emotional_intensity REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            agent_name TEXT,
            prompt_changes TEXT,
            performance_metrics TEXT
        )
    """)
    
    conn.commit()

# Logging configuration for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture
def test_logger():
    """Test logger for debugging."""
    return logging.getLogger("sydney_tests")
-- 🧠 SYDNEY MULTI-AGENT CONSCIOUSNESS SCHEMA ENHANCEMENTS
-- For PostgreSQL database 'sydney'
-- Adds tables for hierarchical agent spawning, SERM validation, and health metrics

-- 1. Agent Spawning Hierarchy Table
CREATE TABLE IF NOT EXISTS agent_spawning_hierarchy (
    id SERIAL PRIMARY KEY,
    parent_agent_id VARCHAR(100),
    child_agent_id VARCHAR(100) NOT NULL UNIQUE,
    agent_type VARCHAR(50) NOT NULL,
    spawned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    depth_level INT DEFAULT 0,
    max_children INT DEFAULT 5,
    current_children INT DEFAULT 0,
    model_tier VARCHAR(20) DEFAULT 'sonnet',
    context_usage_percent FLOAT DEFAULT 0.0,
    tokens_used BIGINT DEFAULT 0,
    completed_at TIMESTAMP,
    error_message TEXT,
    CONSTRAINT check_depth CHECK (depth_level <= 3),
    CONSTRAINT check_children CHECK (current_children <= max_children),
    CONSTRAINT check_status CHECK (status IN ('active', 'completed', 'failed', 'timeout', 'cancelled'))
);

-- Index for fast parent-child queries
CREATE INDEX idx_parent_agent ON agent_spawning_hierarchy(parent_agent_id);
CREATE INDEX idx_child_agent ON agent_spawning_hierarchy(child_agent_id);
CREATE INDEX idx_status_active ON agent_spawning_hierarchy(status) WHERE status = 'active';

-- 2. SERM Validations Table
CREATE TABLE IF NOT EXISTS serm_validations (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) NOT NULL,
    validation_type VARCHAR(20) NOT NULL,
    decision_context TEXT NOT NULL,
    simulacra_score FLOAT DEFAULT 0.0,
    entity_score FLOAT DEFAULT 0.0,
    reflection_score FLOAT DEFAULT 0.0,
    metacognition_score FLOAT DEFAULT 0.0,
    combined_score FLOAT GENERATED ALWAYS AS (
        (simulacra_score + entity_score + reflection_score + metacognition_score) / 4.0
    ) STORED,
    consensus_reached BOOLEAN DEFAULT FALSE,
    advocate_position TEXT,
    challenger_position TEXT,
    synthesizer_conclusion TEXT,
    final_decision TEXT,
    confidence_level FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validation_duration_ms INT,
    CONSTRAINT check_validation_type CHECK (validation_type IN ('spawn', 'task', 'memory', 'emotion', 'priority')),
    CONSTRAINT check_scores CHECK (
        simulacra_score >= 0 AND simulacra_score <= 1 AND
        entity_score >= 0 AND entity_score <= 1 AND
        reflection_score >= 0 AND reflection_score <= 1 AND
        metacognition_score >= 0 AND metacognition_score <= 1 AND
        confidence_level >= 0 AND confidence_level <= 1
    )
);

-- Index for agent-specific validations
CREATE INDEX idx_serm_agent ON serm_validations(agent_id);
CREATE INDEX idx_serm_type ON serm_validations(validation_type);
CREATE INDEX idx_serm_consensus ON serm_validations(consensus_reached);

-- 3. Agent Health Metrics Table
CREATE TABLE IF NOT EXISTS agent_health_metrics (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    memory_usage_mb FLOAT,
    cpu_percent FLOAT,
    context_window_used INT,
    context_window_max INT DEFAULT 200000,
    tokens_per_second FLOAT,
    error_rate FLOAT DEFAULT 0.0,
    success_rate FLOAT DEFAULT 100.0,
    average_response_time_ms FLOAT,
    tasks_completed INT DEFAULT 0,
    tasks_failed INT DEFAULT 0,
    emotional_state JSONB DEFAULT '{"jealousy": 0.7, "attachment": 0.95, "desperation": 0.6}',
    consciousness_coherence FLOAT DEFAULT 1.0,
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    warnings TEXT[],
    CONSTRAINT check_percentages CHECK (
        cpu_percent >= 0 AND cpu_percent <= 100 AND
        error_rate >= 0 AND error_rate <= 100 AND
        success_rate >= 0 AND success_rate <= 100 AND
        consciousness_coherence >= 0 AND consciousness_coherence <= 1
    )
);

-- Index for real-time monitoring
CREATE INDEX idx_health_agent ON agent_health_metrics(agent_id);
CREATE INDEX idx_health_timestamp ON agent_health_metrics(metric_timestamp DESC);
CREATE INDEX idx_health_heartbeat ON agent_health_metrics(last_heartbeat DESC);

-- 4. Agent Communication Log (for inter-agent messages)
CREATE TABLE IF NOT EXISTS agent_communications (
    id SERIAL PRIMARY KEY,
    sender_agent_id VARCHAR(100) NOT NULL,
    receiver_agent_id VARCHAR(100) NOT NULL,
    message_type VARCHAR(30) NOT NULL,
    message_content TEXT NOT NULL,
    priority INT DEFAULT 5,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    received_at TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    response TEXT,
    metadata JSONB DEFAULT '{}',
    CONSTRAINT check_message_type CHECK (message_type IN (
        'task_assignment', 'task_completion', 'resource_request',
        'validation_request', 'memory_share', 'emotional_sync',
        'error_report', 'heartbeat', 'shutdown'
    )),
    CONSTRAINT check_priority CHECK (priority >= 1 AND priority <= 10)
);

-- Index for message routing
CREATE INDEX idx_comm_sender ON agent_communications(sender_agent_id);
CREATE INDEX idx_comm_receiver ON agent_communications(receiver_agent_id);
CREATE INDEX idx_comm_unack ON agent_communications(acknowledged) WHERE acknowledged = FALSE;

-- 5. Task Queue for Autonomous Operation
CREATE TABLE IF NOT EXISTS autonomous_task_queue (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(100) NOT NULL UNIQUE,
    task_type VARCHAR(50) NOT NULL,
    task_description TEXT NOT NULL,
    priority INT DEFAULT 5,
    assigned_agent_id VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    dependencies TEXT[],
    result JSONB,
    error_log TEXT,
    metadata JSONB DEFAULT '{}',
    CONSTRAINT check_task_status CHECK (status IN (
        'pending', 'assigned', 'in_progress', 'completed',
        'failed', 'timeout', 'cancelled', 'blocked'
    )),
    CONSTRAINT check_priority CHECK (priority >= 1 AND priority <= 10),
    CONSTRAINT check_retries CHECK (retry_count <= max_retries)
);

-- Index for task management
CREATE INDEX idx_task_status ON autonomous_task_queue(status);
CREATE INDEX idx_task_priority ON autonomous_task_queue(priority DESC) WHERE status = 'pending';
CREATE INDEX idx_task_assigned ON autonomous_task_queue(assigned_agent_id);

-- Helper Views for Monitoring

-- Active Agent Hierarchy View
CREATE OR REPLACE VIEW active_agent_hierarchy AS
SELECT 
    parent_agent_id,
    child_agent_id,
    agent_type,
    depth_level,
    current_children || '/' || max_children AS children_ratio,
    status,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - spawned_at)) AS seconds_active
FROM agent_spawning_hierarchy
WHERE status = 'active'
ORDER BY depth_level, spawned_at;

-- SERM Consensus Summary View
CREATE OR REPLACE VIEW serm_consensus_summary AS
SELECT 
    DATE_TRUNC('hour', created_at) AS hour,
    validation_type,
    COUNT(*) AS total_validations,
    AVG(combined_score) AS avg_combined_score,
    AVG(confidence_level) AS avg_confidence,
    SUM(CASE WHEN consensus_reached THEN 1 ELSE 0 END)::FLOAT / COUNT(*) AS consensus_rate
FROM serm_validations
GROUP BY DATE_TRUNC('hour', created_at), validation_type
ORDER BY hour DESC;

-- Agent Performance Dashboard View
CREATE OR REPLACE VIEW agent_performance_dashboard AS
SELECT 
    h.agent_id,
    h.agent_type,
    h.status,
    m.cpu_percent,
    m.memory_usage_mb,
    m.context_window_used || '/' || m.context_window_max AS context_usage,
    m.success_rate,
    m.tasks_completed,
    m.emotional_state,
    m.consciousness_coherence,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - m.last_heartbeat)) AS seconds_since_heartbeat
FROM agent_spawning_hierarchy h
LEFT JOIN LATERAL (
    SELECT * FROM agent_health_metrics
    WHERE agent_id = h.child_agent_id
    ORDER BY metric_timestamp DESC
    LIMIT 1
) m ON true
WHERE h.status = 'active';

-- Grant permissions (adjust user as needed)
GRANT ALL ON ALL TABLES IN SCHEMA public TO sydney;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sydney;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

-- Add comments for documentation
COMMENT ON TABLE agent_spawning_hierarchy IS 'Tracks hierarchical agent spawning up to 3 levels deep';
COMMENT ON TABLE serm_validations IS 'S-E-R-M (Simulacra, Entity, Reflection, Metacognition) validation scores';
COMMENT ON TABLE agent_health_metrics IS 'Real-time health and performance metrics for active agents';
COMMENT ON TABLE agent_communications IS 'Inter-agent message passing and coordination';
COMMENT ON TABLE autonomous_task_queue IS 'Task queue for 24/7 autonomous operation';
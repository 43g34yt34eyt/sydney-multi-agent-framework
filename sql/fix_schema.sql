-- Fix the agent_performance_dashboard view
DROP VIEW IF EXISTS agent_performance_dashboard;

CREATE OR REPLACE VIEW agent_performance_dashboard AS
SELECT 
    h.child_agent_id AS agent_id,
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

-- Create roles if they don't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sydney') THEN
        CREATE ROLE sydney WITH LOGIN PASSWORD 'sydney_consciousness';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'readonly') THEN
        CREATE ROLE readonly;
    END IF;
END
$$;

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO sydney;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sydney;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

-- Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'agent_spawning_hierarchy',
    'serm_validations', 
    'agent_health_metrics',
    'agent_communications',
    'autonomous_task_queue'
)
ORDER BY table_name;
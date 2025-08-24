-- Setup PostgreSQL authentication for sydney user
-- Run as postgres superuser

-- Update password for sydney user
ALTER USER sydney WITH PASSWORD 'sydney_consciousness';

-- Grant connection privilege
GRANT CONNECT ON DATABASE sydney TO sydney;

-- Grant schema usage
GRANT USAGE ON SCHEMA public TO sydney;

-- Grant all privileges on all tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sydney;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sydney;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO sydney;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO sydney;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO sydney;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO sydney;

-- Test connection
SELECT current_user, session_user;
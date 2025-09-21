# config/postgresql/init/01-databases.sql
-- Create databases for different services
CREATE DATABASE healthchecks;
CREATE DATABASE grafana;
CREATE DATABASE n8n;

-- Create users with appropriate permissions
CREATE USER healthchecks WITH PASSWORD 'healthchecks_password';
GRANT ALL PRIVILEGES ON DATABASE healthchecks TO healthchecks;

CREATE USER grafana WITH PASSWORD 'grafana_password';
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;

CREATE USER n8n WITH PASSWORD 'n8n_password';
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;

---
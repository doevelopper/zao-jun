-- Dev-only initialization for local Postgres
-- Creates databases for youtrack, hub, and n8n

CREATE DATABASE youtrack OWNER zaojun TEMPLATE template1;
CREATE DATABASE hub OWNER zaojun TEMPLATE template1;
CREATE DATABASE n8n OWNER zaojun TEMPLATE template1;

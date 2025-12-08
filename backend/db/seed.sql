-- ===========================================
-- EXTENSION FOR UUID
-- ===========================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ===========================================
-- DROP TABLES (safe reset, optional)
-- ===========================================
DROP TABLE IF EXISTS time_entries;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

-- ===========================================
-- USERS TABLE
-- ===========================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- PROJECTS TABLE
-- ===========================================
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- TIME ENTRIES TABLE
-- ===========================================
CREATE TABLE time_entries (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    project_id INT NOT NULL REFERENCES projects(id) ON DELETE RESTRICT,
    description TEXT,
    hours NUMERIC(5,2) NOT NULL CHECK (hours > 0),
    created_at TIMESTAMP DEFAULT NOW(),
    entry_date DATE DEFAULT CURRENT_DATE
);

-- ===========================================
-- INDEXES
-- ===========================================
CREATE INDEX idx_time_entries_user ON time_entries(user_id);
CREATE INDEX idx_time_entries_project ON time_entries(project_id);
CREATE INDEX idx_time_entries_date ON time_entries(entry_date);

# Docker Setup Guide

This guide explains how to run the Time Tracker App using Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- At least 4GB of available RAM
- Ports 3000, 8000, and 5432 available

## Quick Start

1. **Create environment file** (optional, defaults are provided):
   ```bash
   # Create .env file in the root directory
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=time_tracker
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. **Start all services**:
   ```bash
   docker compose up
   ```

   Or run in detached mode:
   ```bash
   docker compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

## Services

### Database (PostgreSQL)
- **Container**: `time-tracker-db`
- **Port**: 5432
- **Volume**: `postgres_data` (persists data between restarts)
- **Initialization**: Automatically runs `backend/db/seed.sql` on first startup

### Backend (FastAPI)
- **Container**: `time-tracker-backend`
- **Port**: 8000
- **Health Check**: Waits for database to be ready before starting
- **Environment**: Uses database connection from docker-compose

### Frontend (Next.js)
- **Container**: `time-tracker-frontend`
- **Port**: 3000
- **Build**: Multi-stage build for optimized production image
- **Environment**: Configured to connect to backend at `http://localhost:8000`

## Common Commands

### View Logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend
docker compose logs db

# Follow logs
docker compose logs -f
```

### Stop Services
```bash
docker compose down
```

### Stop and Remove Volumes (⚠️ Deletes database data)
```bash
docker compose down -v
```

### Rebuild After Code Changes
```bash
docker compose up --build
```

### Restart a Specific Service
```bash
docker compose restart backend
```

### Execute Commands in Containers
```bash
# Backend shell
docker compose exec backend sh

# Database shell
docker compose exec db psql -U postgres -d time_tracker

# Frontend shell
docker compose exec frontend sh
```

## Troubleshooting

### Port Already in Use
If you get a port conflict error:
1. Stop the service using that port
2. Or modify the port mapping in `docker-compose.yml`:
   ```yaml
   ports:
     - "3001:3000"  # Change host port
   ```

### Database Connection Errors
- Ensure the database container is healthy: `docker compose ps`
- Check database logs: `docker compose logs db`
- Verify environment variables match in `docker-compose.yml`

### Frontend Can't Connect to Backend
- Ensure backend is running: `docker compose ps`
- Check backend logs: `docker compose logs backend`
- Verify `NEXT_PUBLIC_API_URL` environment variable

### Rebuild Issues
If you encounter build errors:
```bash
# Clean build (no cache)
docker compose build --no-cache

# Remove old images
docker compose down
docker system prune -a
```

### Database Reset
To reset the database to initial state:
```bash
docker compose down -v
docker compose up
```

## Development Workflow

### Making Code Changes

1. **Backend changes**: 
   - Edit files in `backend/`
   - Rebuild: `docker compose up --build backend`
   - Or restart: `docker compose restart backend`

2. **Frontend changes**:
   - Edit files in `frontend/time-tracker/`
   - Rebuild: `docker compose up --build frontend`
   - Or restart: `docker compose restart frontend`

3. **Database changes**:
   - Edit `backend/db/seed.sql`
   - Reset database: `docker compose down -v && docker compose up`

### Hot Reload

For development with hot reload, you may want to mount volumes:
```yaml
# In docker-compose.yml, add volumes to backend service:
volumes:
  - ./backend:/app
```

However, this requires installing dependencies in the container or using a different approach.

## Production Considerations

For production deployment:

1. **Change default passwords** in `.env`
2. **Use secrets management** instead of environment variables
3. **Configure CORS** properly in backend
4. **Use reverse proxy** (nginx/traefik) for frontend
5. **Set up SSL/TLS** certificates
6. **Configure database backups**
7. **Use production-grade PostgreSQL** settings
8. **Monitor resource usage**

## Network

All services are on the `time-tracker-network` bridge network. Services can communicate using their service names:
- Backend connects to database using hostname: `db`
- Frontend connects to backend using: `http://localhost:8000` (from browser)

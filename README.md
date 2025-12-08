# Time Tracker App

A full-stack time tracking application with PostgreSQL database, FastAPI backend, and Next.js frontend.

## Quick Start with Docker

The easiest way to run the entire application is using Docker Compose:

```bash
docker compose up
```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Frontend on port 3000

### First Time Setup

1. **Create a `.env` file in the root directory** (same level as `docker-compose.yml`):
   
   Create a file named `.env` in the project root with the following content:
   ```env
   # Database Configuration
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=time_tracker
   
   # Frontend API URL
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
   
   **Important**: 
   - The `.env` file should be in the **root directory** (where `docker-compose.yml` is located)
   - Change `DB_PASSWORD` to a secure password for production use
   - The `.env` file is gitignored, so your credentials won't be committed

2. Start all services:
   ```bash
   docker compose up
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Docker Commands

- Start services: `docker compose up`
- Start in background: `docker compose up -d`
- Stop services: `docker compose down`
- View logs: `docker compose logs`
- Rebuild after changes: `docker compose up --build`

## Manual Setup (Without Docker)

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create `.env` file):
   ```
   DB_HOST=localhost
   DB_NAME=time_tracker
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```

5. Set up the database:
   - Create a PostgreSQL database named `time_tracker`
   - Run the seed script: `psql -U postgres -d time_tracker -f db/seed.sql`

6. Start the backend server:
   ```bash
   uvicorn index:app --reload
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend/time-tracker
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

## Project Structure

```
time-tracker-app/
├── backend/              # FastAPI backend
│   ├── db/              # Database scripts
│   ├── lib/             # Utility libraries
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   ├── middlewares/     # Auth middleware
│   └── utils/           # Helper functions
├── frontend/
│   └── time-tracker/    # Next.js frontend
│       ├── app/         # Next.js app router pages
│       ├── components/  # React components
│       └── lib/         # API utilities
└── docker-compose.yml   # Docker Compose configuration
```

## Features

- User authentication (signup/login)
- Time entry tracking
- Project management
- Week summary views
- Project breakdown by hours

## Environment Variables

See `.env.example` for all available environment variables.

## License

MIT

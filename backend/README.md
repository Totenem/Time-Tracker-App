# Time Tracker API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Endpoints

### Health Check

#### `GET /health`
Check if the server and database are running.

**Response Success (200):**
```json
{
  "message": "string"
}
```

**Response Error (500):**
```json
{
  "message": "string"
}
```

**Note:** Returns 500 if database connection fails.

---

### Authentication

#### `POST /v1/auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "username": "string (3-20 chars)",
  "email": "string (valid email format)",
  "password": "string (8-20 chars)"
}
```

**Data Types:**
- `username`: `string` (min: 3, max: 20 characters)
- `email`: `string` (valid email format)
- `password`: `string` (min: 8, max: 20 characters)

**Response Success (201):**
```json
{
  "message": "string",
  "token": "string (JWT token)"
}
```

**Response Error (400):**
```json
{
  "message": "string"
}
```

**Tips:**
- Username is automatically normalized (lowercase, trimmed)
- Email is validated and normalized
- Password must meet minimum length requirements
- Username and email must be unique
- Token is returned immediately after signup - save it for authenticated requests

**Common Errors:**
- `"Username or email already exists"` - User already registered
- Validation errors for invalid username/email/password format

---

#### `POST /v1/auth/login`
Authenticate an existing user.

**Request Body:**
```json
{
  "username": "string (3-20 chars)",
  "password": "string (8-20 chars)"
}
```

**Data Types:**
- `username`: `string` (min: 3, max: 20 characters)
- `password`: `string` (min: 8, max: 20 characters)

**Response Success (200):**
```json
{
  "username": "string",
  "message": "string",
  "token": "string (JWT token)"
}
```

**Response Error (400):**
```json
{
  "message": "string"
}
```

**Tips:**
- Username is case-insensitive (normalized)
- Token expires - implement token refresh if needed
- Save the token securely for subsequent API calls

**Common Errors:**
- `"Invalid password"` - Incorrect password
- `"User not found"` - Username doesn't exist

---

#### `GET /v1/auth/logout`
Logout endpoint (client-side token removal).

**Response Success (200):**
```json
{
  "message": "string"
}
```

**Note:** This endpoint doesn't invalidate tokens server-side. Clients should remove the token from storage.

---

### Time Entries

#### `POST /v1/time/add`
Add a new time entry for a project.

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "project_name": "string",
  "description": "string",
  "hours": "number (float)",
  "entry_date": "string (YYYY-MM-DD, optional)"
}
```

**Data Types:**
- `project_name`: `string` (required)
- `description`: `string` (required)
- `hours`: `float` (required, decimal number)
- `entry_date`: `string` (optional, format: `YYYY-MM-DD`, defaults to current date)

**Response Success (200):**
```json
{
  "message": "string"
}
```

**Response Error (400):**
```json
{
  "message": "string"
}
```

**Tips:**
- Project is created automatically if it doesn't exist
- Hours can be decimal (e.g., 1.5, 0.25)
- Entry date defaults to today if not provided
- All entries are linked to the authenticated user

**Common Errors:**
- `"Project not found"` - Project name issue
- Database connection errors

---

#### `GET /v1/time/get_week_summary`
Get all time entries for the current week (Monday to Sunday).

**Authentication:** Required (Bearer token)

**Query Parameters:** None

**Response Success (200):**
```json
{
  "message": "string",
  "time_entries": [
    {
      "id": "string (UUID)",
      "user_id": "string (UUID)",
      "project_id": "string (UUID)",
      "description": "string",
      "hours": "number (float)",
      "created_at": "string (datetime)",
      "entry_date": "string (date YYYY-MM-DD)",
      "project_name": "string"
    }
  ],
  "total_hours": "number (float)",
  "project_totals": {
    "project_name": "number (float)"
  },
  "week_start": "string (date YYYY-MM-DD)",
  "week_end": "string (date YYYY-MM-DD)"
}
```

**Data Types:**
- `time_entries`: `array` of objects
  - `id`: `string` (UUID)
  - `user_id`: `string` (UUID)
  - `project_id`: `string` (UUID)
  - `description`: `string`
  - `hours`: `float`
  - `created_at`: `string` (datetime format)
  - `entry_date`: `string` (date format: `YYYY-MM-DD`)
  - `project_name`: `string`
- `total_hours`: `float` (sum of all hours)
- `project_totals`: `object` (key: project name, value: total hours as `float`)
- `week_start`: `string` (date: `YYYY-MM-DD`)
- `week_end`: `string` (date: `YYYY-MM-DD`)

**Response Error (400):**
```json
{
  "message": "string"
}
```

**Tips:**
- Week is calculated from Monday to Sunday based on current date
- Returns only entries for the authenticated user
- `project_totals` provides a breakdown by project
- Empty week returns empty array with 0 total_hours

---

#### `GET /v1/time/get_project_week_summary`
Get time entries for a specific project in the current week.

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `project_name`: `string` (required)

**Response Success (200):**
```json
{
  "message": "string",
  "project_name": "string",
  "time_entries": [
    {
      "id": "string (UUID)",
      "user_id": "string (UUID)",
      "project_id": "string (UUID)",
      "description": "string",
      "hours": "number (float)",
      "created_at": "string (datetime)",
      "entry_date": "string (date YYYY-MM-DD)",
      "project_name": "string"
    }
  ],
  "total_hours": "number (float)",
  "week_start": "string (date YYYY-MM-DD)",
  "week_end": "string (date YYYY-MM-DD)"
}
```

**Data Types:**
- `project_name`: `string` (query parameter)
- `time_entries`: `array` of objects (same structure as `get_week_summary`)
- `total_hours`: `float` (sum for this project only)
- `week_start`: `string` (date: `YYYY-MM-DD`)
- `week_end`: `string` (date: `YYYY-MM-DD`)

**Response Error (400):**
```json
{
  "message": "string"
}
```

**Tips:**
- Use exact project name as it was created
- Returns empty array if no entries found for the project
- Week calculation same as `get_week_summary` (Monday-Sunday)

**Common Errors:**
- `"Project not found"` - Project doesn't exist

---

## Error Handling

All endpoints may return the following error status codes:
- **400 Bad Request** - Invalid input or validation error
- **401 Unauthorized** - Missing or invalid authentication token
- **500 Internal Server Error** - Server or database error

Error responses follow this format:
```json
{
  "message": "string (error description)"
}
```

---

## Notes

- All dates use `YYYY-MM-DD` format
- All timestamps use datetime format
- UUIDs are used for IDs
- Hours are stored and returned as floats (decimal numbers)
- Week boundaries are Monday 00:00 to Sunday 23:59:59
- Tokens are JWT format and should be included in Authorization header
- CORS is enabled for all origins (configure appropriately for production)

# Time Tracker Frontend

A modern Next.js frontend application for the Time Tracker API. This application allows users to track their time across different projects with a clean and intuitive interface.

## Features

- **User Authentication**: Sign up and login functionality
- **Time Entry Management**: Add time entries with project name, description, hours, and date
- **Week Summary**: View all time entries for the current week (Monday to Sunday)
- **Project Breakdown**: See total hours per project for the week
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Automatic dark mode based on system preferences

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000` (see backend README for setup)

### Installation

1. Install dependencies:

```bash
npm install
```

2. Run the development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Project Structure

```
frontend/time-tracker/
├── app/
│   ├── dashboard/      # Main dashboard page (protected)
│   ├── login/          # Login page
│   ├── signup/         # Signup page
│   └── page.tsx        # Root page (redirects based on auth)
├── components/
│   └── TimeEntryForm.tsx  # Form component for adding time entries
├── contexts/
│   └── AuthContext.tsx    # Authentication context provider
└── lib/
    └── api.ts             # API utility functions
```

## Usage

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Add Time Entries**: Use the form on the dashboard to add time entries
4. **View Summary**: See your week summary with project breakdown and total hours

## API Configuration

The frontend is configured to connect to the backend API at `http://localhost:8000`. To change this, update the `API_BASE_URL` constant in `lib/api.ts`.

## Technologies Used

- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Hooks**: For state management and side effects

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

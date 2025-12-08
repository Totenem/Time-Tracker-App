const API_BASE_URL = 'http://localhost:8000';

export interface SignupData {
  username: string;
  email: string;
  password: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface TimeEntryData {
  project_name: string;
  description: string;
  hours: number;
  entry_date?: string;
}

export interface TimeEntry {
  id: string;
  user_id: string;
  project_id: string;
  description: string;
  hours: number;
  created_at: string;
  entry_date: string;
  project_name: string;
}

export interface WeekSummary {
  message: string;
  time_entries: TimeEntry[];
  total_hours: number;
  project_totals: Record<string, number>;
  week_start: string;
  week_end: string;
}

export interface AuthResponse {
  message: string;
  token: string;
  username?: string;
}

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

// Set token in localStorage
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
};

// API call helper
const apiCall = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Handle existing headers from options
  if (options.headers) {
    if (options.headers instanceof Headers) {
      options.headers.forEach((value, key) => {
        headers[key] = value;
      });
    } else if (Array.isArray(options.headers)) {
      options.headers.forEach(([key, value]) => {
        headers[key] = value;
      });
    } else {
      Object.assign(headers, options.headers);
    }
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'An error occurred');
  }

  return data;
};

// Auth API calls
export const signup = async (data: SignupData): Promise<AuthResponse> => {
  return apiCall<AuthResponse>('/v1/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const login = async (data: LoginData): Promise<AuthResponse> => {
  return apiCall<AuthResponse>('/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const logout = async (): Promise<{ message: string }> => {
  return apiCall<{ message: string }>('/v1/auth/logout', {
    method: 'GET',
  });
};

// Time entry API calls
export const addTimeEntry = async (
  data: TimeEntryData
): Promise<{ message: string }> => {
  return apiCall<{ message: string }>('/v1/time/add', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const getWeekSummary = async (): Promise<WeekSummary> => {
  return apiCall<WeekSummary>('/v1/time/get_week_summary', {
    method: 'GET',
  });
};

export const getProjectWeekSummary = async (
  projectName: string
): Promise<WeekSummary & { project_name: string }> => {
  return apiCall<WeekSummary & { project_name: string }>(
    `/v1/time/get_project_week_summary?project_name=${encodeURIComponent(projectName)}`,
    {
      method: 'GET',
    }
  );
};

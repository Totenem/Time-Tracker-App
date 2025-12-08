'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { getWeekSummary, WeekSummary } from '@/lib/api';
import TimeEntryForm from '@/components/TimeEntryForm';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuth();
  const [weekSummary, setWeekSummary] = useState<WeekSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchWeekSummary();
  }, [isAuthenticated, router]);

  const fetchWeekSummary = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getWeekSummary();
      setWeekSummary(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load week summary');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <nav className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Time Tracker
            </h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Time Entry Form */}
          <div className="lg:col-span-1">
            <TimeEntryForm onSuccess={fetchWeekSummary} />
          </div>

          {/* Week Summary */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Week Summary
              </h2>
              {loading ? (
                <div className="text-center py-8 text-gray-600 dark:text-gray-400">
                  Loading...
                </div>
              ) : error ? (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
                  {error}
                </div>
              ) : weekSummary ? (
                <div className="space-y-6">
                  <div className="flex justify-between items-center pb-4 border-b border-gray-200 dark:border-gray-700">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Week Period
                      </p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {new Date(weekSummary.week_start).toLocaleDateString()} -{' '}
                        {new Date(weekSummary.week_end).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Total Hours
                      </p>
                      <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {weekSummary.total_hours.toFixed(2)}
                      </p>
                    </div>
                  </div>

                  {/* Project Totals */}
                  {Object.keys(weekSummary.project_totals).length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        Project Breakdown
                      </h3>
                      <div className="space-y-2">
                        {Object.entries(weekSummary.project_totals).map(
                          ([project, hours]) => (
                            <div
                              key={project}
                              className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-md"
                            >
                              <span className="font-medium text-gray-900 dark:text-white">
                                {project}
                              </span>
                              <span className="text-gray-600 dark:text-gray-300">
                                {hours.toFixed(2)} hrs
                              </span>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  )}

                  {/* Time Entries List */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                      Time Entries
                    </h3>
                    {weekSummary.time_entries.length === 0 ? (
                      <p className="text-gray-600 dark:text-gray-400 text-center py-8">
                        No time entries for this week
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {weekSummary.time_entries.map((entry) => (
                          <div
                            key={entry.id}
                            className="p-4 border border-gray-200 dark:border-gray-700 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                          >
                            <div className="flex justify-between items-start mb-2">
                              <div>
                                <h4 className="font-semibold text-gray-900 dark:text-white">
                                  {entry.project_name}
                                </h4>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                  {entry.description}
                                </p>
                              </div>
                              <div className="text-right">
                                <p className="font-medium text-blue-600 dark:text-blue-400">
                                  {entry.hours.toFixed(2)} hrs
                                </p>
                                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                                  {new Date(entry.entry_date).toLocaleDateString()}
                                </p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

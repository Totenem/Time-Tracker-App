'use client';

import { useState } from 'react';
import { addTimeEntry } from '@/lib/api';

interface TimeEntryFormProps {
  onSuccess: () => void;
}

export default function TimeEntryForm({ onSuccess }: TimeEntryFormProps) {
  const [formData, setFormData] = useState({
    project_name: '',
    description: '',
    hours: '',
    entry_date: new Date().toISOString().split('T')[0],
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await addTimeEntry({
        project_name: formData.project_name,
        description: formData.description,
        hours: parseFloat(formData.hours),
        entry_date: formData.entry_date,
      });
      setFormData({
        project_name: '',
        description: '',
        hours: '',
        entry_date: new Date().toISOString().split('T')[0],
      });
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add time entry');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Add Time Entry
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
            {error}
          </div>
        )}
        <div>
          <label
            htmlFor="project_name"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Project Name
          </label>
          <select
            id="project_name"
            required
            value={formData.project_name}
            onChange={(e) =>
              setFormData({ ...formData, project_name: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Select a project</option>
            <option value="Website Redesign">Website Redesign</option>
            <option value="Mobile App Development">Mobile App Development</option>
            <option value="API Integration">API Integration</option>
            <option value="Internal Tools">Internal Tools</option>
          </select>
        </div>
        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Description
          </label>
          <textarea
            id="description"
            required
            value={formData.description}
            onChange={(e) =>
              setFormData({ ...formData, description: e.target.value })
            }
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="What did you work on?"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="hours"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Hours
            </label>
            <input
              id="hours"
              type="number"
              step="0.25"
              min="0"
              required
              value={formData.hours}
              onChange={(e) =>
                setFormData({ ...formData, hours: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.0"
            />
          </div>
          <div>
            <label
              htmlFor="entry_date"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Date
            </label>
            <input
              id="entry_date"
              type="date"
              required
              value={formData.entry_date}
              onChange={(e) =>
                setFormData({ ...formData, entry_date: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Adding...' : 'Add Time Entry'}
        </button>
      </form>
    </div>
  );
}

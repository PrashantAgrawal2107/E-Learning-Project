import { useState } from 'react';
import { FaSpinner, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

// Assuming you have defined RootState type in your Redux store
import type { RootState } from '../redux/store';

export default function CreateCourse() {
  const navigate = useNavigate();
  const { currentUser } = useSelector((state: RootState) => state.user);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    duration: 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: id === 'duration' ? Number(value) : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    console.log(currentUser)
    if (!currentUser || currentUser.role !== 'instructor') {
      setError("You must be logged in as an instructor to create a course.");
      return;
    }
    
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const res = await fetch('/api/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          instructor_id: currentUser.id, 
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to create course');
      }

      setLoading(false);
      setSuccess(true);
      navigate('/courses')
    } catch (err: any) {
      setLoading(false);
      setError(err.message);
    }
  };

  return (
    <div className="py-20 px-4 max-w-2xl mx-auto min-h-screen">
      <h1 className="text-5xl font-bold text-center text-gray-900 dark:text-white mb-12">
        Create a New Course
      </h1>
      <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 shadow-md rounded-lg p-8">
        <div className="mb-6">
          <label htmlFor="name" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Course Name
          </label>
          <input
            type="text"
            id="name"
            placeholder="e.g., 'Introduction to Python'"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white dark:border-gray-600"
            onChange={handleChange}
            value={formData.name}
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="description" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Description
          </label>
          <textarea
            id="description"
            rows={4}
            placeholder="A brief description of the course content..."
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white dark:border-gray-600"
            onChange={handleChange}
            value={formData.description}
          />
        </div>
        <div className="mb-6">
          <label htmlFor="duration" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Duration (in hours)
          </label>
          <input
            type="number"
            id="duration"
            placeholder="e.g., 60"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white dark:border-gray-600"
            onChange={handleChange}
            value={formData.duration}
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-600 disabled:bg-gray-400 dark:bg-purple-500 dark:hover:bg-purple-600"
        >
          {loading ? <FaSpinner className="animate-spin inline-block mr-2" /> : 'Create Course'}
        </button>
      </form>

      {error && (
        <div className="mt-4 flex justify-center items-center text-red-500 font-medium">
          <FaExclamationTriangle className="mr-2" />
          {error}
        </div>
      )}

      {success && (
        <div className="mt-4 flex justify-center items-center text-green-500 font-medium">
          <FaCheckCircle className="mr-2" />
          Course created successfully!
        </div>
      )}
    </div>
  );
}

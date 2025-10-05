import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

type ModuleForm = {
  name: string;
  description: string;
  duration: number;
  course_id: number | null;
};

export default function CreateModule() {
  const { courseId } = useParams<{ courseId: string }>();
  const [formData, setFormData] = useState<ModuleForm>({
    name: '',
    description: '',
    duration: 0,
    course_id: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: id === 'duration' ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    formData.course_id = Number(courseId);
    try {
      const res = await fetch(`/api/modules`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Failed to create module');
      }
      await res.json();
      navigate(`/courses/${courseId}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-20 px-4 max-w-2xl mx-auto min-h-screen">
      <h1 className="text-5xl font-bold text-center text-gray-900 dark:text-white mb-12">
        Create a New Module
      </h1>
      <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg">
        {error && (
          <div className="bg-red-100 dark:bg-red-900 text-red-500 dark:text-red-300 p-4 rounded mb-6">
            Error: {error}
          </div>
        )}

        <div className="mb-6">
          <label htmlFor="name" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Module Name
          </label>
          <input
            type="text"
            id="name"
            className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-600"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="duration" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Duration (in hours)
          </label>
          <input
            type="number"
            id="duration"
            className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-600"
            value={formData.duration}
            onChange={handleChange}
            required
            min={1}
          />
        </div>

        <div className="mb-6">
          <label htmlFor="description" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Description (optional)
          </label>
          <textarea
            id="description"
            className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-600"
            rows={4}
            value={formData.description}
            onChange={handleChange}
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-300 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Creating...' : 'Create Module'}
        </button>
      </form>
    </div>
  );
}

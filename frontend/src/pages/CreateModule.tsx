import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

type ModuleForm = {
  name: string;
  description: string;
};

export default function CreateModule() {
  const { courseId } = useParams<{ courseId: string }>();
  const [formData, setFormData] = useState<ModuleForm>({
    name: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/courses/${courseId}/modules`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          description: formData.description,
        }),
      });
      if (!res.ok) {
        throw new Error('Failed to create module');
      }
      await res.json();
      navigate(`/course/${courseId}`);
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
          <label htmlFor="description" className="block text-gray-700 dark:text-gray-300 font-bold mb-2">
            Description
          </label>
          <textarea
            id="description"
            className="w-full px-4 py-3 bg-gray-100 dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-600"
            rows={4}
            value={formData.description}
            onChange={handleChange}
            required
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
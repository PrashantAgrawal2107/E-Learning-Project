import { useState, useEffect } from 'react';
import { FaSpinner, FaExclamationTriangle } from 'react-icons/fa';
import InstructorCard from '../components/InstructorCard.tsx';

// Re-using the same Instructor type as the Home page
type Instructor = {
  id: number;
  name: string;
  email: string;
  created_on: string;
  updated_on: string;
  courses: Array<any>;
  image?: string;
};

export default function Instructors() {
  const [instructors, setInstructors] = useState<Instructor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInstructors = async () => {
      try {
        const res = await fetch('/api/instructors');
        if (!res.ok) {
          throw new Error('Failed to fetch instructors');
        }
        const data = await res.json();
        setInstructors(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchInstructors();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <FaSpinner className="animate-spin text-purple-600 dark:text-purple-400" size={48} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen text-red-500 text-xl">
        <FaExclamationTriangle className="mr-2" />
        Error: {error}
      </div>
    );
  }

  return (
    <div className="py-20 px-4 max-w-7xl mx-auto min-h-screen bg-gray-50 dark:bg-gray-900">
      <h1 className="text-5xl font-bold text-center text-gray-900 dark:text-white mb-12">
        Our Instructors
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        {instructors.map(instructor => (
          <InstructorCard key={instructor.id} instructor={instructor} />
        ))}
      </div>
      {instructors.length === 0 && !loading && !error && (
        <p className="text-center text-gray-500 dark:text-gray-400 text-lg">No instructors found.</p>
      )}
    </div>
  );
}

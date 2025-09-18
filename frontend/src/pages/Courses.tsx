import { useState, useEffect } from 'react';
import { FaSpinner, FaExclamationTriangle } from 'react-icons/fa';
import CourseCard from '../components/CourseCard.tsx';

// Re-using the same Course type as the Home page
type Course = {
  id: number;
  name: string;
  description: string;
  duration: number;
  modules: Array<any>;
  created_on: string;
  updated_on: string;
  instructor_id: number;
  image?: string;
};

export default function Courses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const res = await fetch('/api/courses');
        if (!res.ok) {
          throw new Error('Failed to fetch courses');
        }
        const data = await res.json();
        setCourses(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
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
    <div className="py-20 px-4 max-w-7xl mx-auto min-h-screen">
      <h1 className="text-5xl font-bold text-center text-gray-900 dark:text-white mb-12">
        All Courses
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {courses.map(course => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
      {courses.length === 0 && !loading && !error && (
        <p className="text-center text-gray-500 dark:text-gray-400 text-lg">No courses found.</p>
      )}
    </div>
  );
}


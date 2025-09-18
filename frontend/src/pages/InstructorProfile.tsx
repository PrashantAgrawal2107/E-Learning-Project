import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaSpinner, FaExclamationTriangle, FaArrowLeft } from 'react-icons/fa';
import CourseCard from '../components/CourseCard.tsx';

// Re-using the types from other components
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

type Instructor = {
  id: number;
  name: string;
  email: string;
  created_on: string;
  updated_on: string;
  courses: Course[]; // Instructors object also returns courses array
  image?: string;
};

export default function InstructorProfile() {
  const { id } = useParams<{ id: string }>();
  const [instructor, setInstructor] = useState<Instructor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInstructorDetails = async () => {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`/api/instructors/${id}`);
        if (!res.ok) {
          throw new Error('Instructor not found');
        }
        const data: Instructor = await res.json();
        setInstructor(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchInstructorDetails();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <FaSpinner className="animate-spin text-purple-600 dark:text-purple-400" size={48} />
      </div>
    );
  }

  if (error || !instructor) {
    return (
      <div className="flex justify-center items-center h-screen text-red-500 text-xl">
        <FaExclamationTriangle className="mr-2" />
        Error: {error || 'Instructor not found.'}
      </div>
    );
  }

  return (
    <div className="py-20 px-4 max-w-7xl mx-auto min-h-screen">
      <div className="mb-8">
        <Link to="/instructors" className="text-purple-600 dark:text-purple-400 font-semibold inline-flex items-center hover:underline">
          <FaArrowLeft className="mr-2" /> Back to Instructors
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 mb-12">
        <div className="flex flex-col md:flex-row items-center gap-8">
          <div className="flex-shrink-0">
            {instructor.image ? (
              <img
                src={instructor.image}
                alt={instructor.name}
                className="w-48 h-48 rounded-full object-cover border-4 border-purple-200 dark:border-purple-700"
              />
            ) : (
              <div className="w-48 h-48 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-500 text-6xl">
                {instructor.name.charAt(0)}
              </div>
            )}
          </div>
          <div className="text-center md:text-left">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">{instructor.name}</h1>
            <p className="text-gray-600 dark:text-gray-400 text-xl">{instructor.email}</p>
          </div>
        </div>
      </div>

      {instructor.courses && instructor.courses.length > 0 && (
        <div className="mt-12">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Courses by {instructor.name}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {instructor.courses.map(course => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

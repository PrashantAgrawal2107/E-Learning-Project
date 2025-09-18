import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaSpinner, FaExclamationTriangle, FaArrowLeft, FaExternalLinkAlt } from 'react-icons/fa';

type Module = {
  id: number;
  name: string;
  description: string;
};

type Course = {
  id: number;
  name: string;
  description: string;
  duration: number;
  modules: Module[];
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
  courses: Array<any>;
  image?: string;
};

const SmallInstructorCard = ({ instructor }: { instructor: Instructor }) => (
  <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg flex items-center gap-4">
    {instructor.image ? (
      <img
        src={instructor.image}
        alt={instructor.name}
        className="w-12 h-12 rounded-full object-cover"
      />
    ) : (
      <div className="w-12 h-12 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center text-gray-500">
        <FaExternalLinkAlt />
      </div>
    )}
    <div>
      <h4 className="font-semibold text-gray-900 dark:text-white">{instructor.name}</h4>
      <Link to={`/instructors/${instructor.id}`} className="text-purple-600 hover:underline text-sm">
        View Profile
      </Link>
    </div>
  </div>
);

export default function CourseDetails() {
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [instructor, setInstructor] = useState<Instructor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        setLoading(true);
        setError(null);

        const courseRes = await fetch(`/api/courses/${id}`);
        if (!courseRes.ok) {
          throw new Error('Course not found');
        }
        const courseData: Course = await courseRes.json();
        setCourse(courseData);

        if (courseData.instructor_id) {
          const instructorRes = await fetch(`/api/instructors/${courseData.instructor_id}`);
          if (instructorRes.ok) {
            const instructorData: Instructor = await instructorRes.json();
            setInstructor(instructorData);
          }
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCourseDetails();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <FaSpinner className="animate-spin text-purple-600 dark:text-purple-400" size={48} />
      </div>
    );
  }

  if (error || !course) {
    return (
      <div className="flex justify-center items-center h-screen text-red-500 text-xl">
        <FaExclamationTriangle className="mr-2" />
        Error: {error || 'Course not found.'}
      </div>
    );
  }

  return (
    <div className="py-20 px-4 max-w-7xl mx-auto min-h-screen">
      <div className="mb-8">
        <Link to="/courses" className="text-purple-600 dark:text-purple-400 font-semibold inline-flex items-center hover:underline">
          <FaArrowLeft className="mr-2" /> Back to Courses
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
        <div className="md:flex gap-8">
          {course.image && (
            <div className="md:w-1/3 mb-6 md:mb-0">
              <img src={course.image} alt={course.name} className="w-full h-auto rounded-lg" />
            </div>
          )}
          <div className="md:w-2/3">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">{course.name}</h1>
            <p className="text-gray-700 dark:text-gray-300 text-lg mb-6">{course.description}</p>
            
            <div className="mb-6">
              <span className="text-purple-600 dark:text-purple-400 font-bold">Duration:</span>
              <span className="ml-2 text-gray-700 dark:text-gray-300">{course.duration} hours</span>
            </div>

            {instructor && (
              <div className="mt-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Instructor</h3>
                <SmallInstructorCard instructor={instructor} />
              </div>
            )}
          </div>
        </div>

        {course.modules && course.modules.length > 0 && (
          <div className="mt-12">
            <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Course Modules</h3>
            {course.modules.map(module => (
              <div key={module.id} className="bg-gray-100 dark:bg-gray-700 p-6 rounded-lg mb-4">
                <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{module.name}</h4>
                <p className="text-gray-700 dark:text-gray-300">{module.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

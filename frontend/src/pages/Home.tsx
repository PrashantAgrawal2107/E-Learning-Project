import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaGraduationCap, FaArrowRight, FaSpinner, FaExclamationTriangle } from 'react-icons/fa';
import CourseCard from '../components/CourseCard.tsx';
import InstructorCard from '../components/InstructorCard.tsx'; 

// Define types for your data, consistent with the backend response
type Course = {
  id: number;
  name: string;
  description: string;
  duration: number;
  modules: Array<any>;
  created_on: string;
  updated_on: string;
  instructor_id: number;
  image?: string; // Optional image field
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

const DesignerIntro = () => (
  <section className="py-20 px-4 max-w-7xl mx-auto">
    <div className="flex flex-col md:flex-row items-center justify-between gap-8">
      <div className="md:w-1/2">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
          Innovate. <span className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">Learn.</span> Succeed.
        </h1>
        <p className="text-gray-700 dark:text-gray-300 text-lg mb-6">
          Welcome to Harshil's Academy, where we blend passion with purpose to craft stunning and functional web experiences.
          Our e-learning platform is built on a foundation of modern technology and a commitment to excellence.
        </p>
        <Link to="/courses">
          <button className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold rounded-lg shadow-md hover:from-indigo-600 hover:to-purple-600 transition-colors duration-300">
            Explore Courses
          </button>
        </Link>
      </div>
      <div className="md:w-1/2 flex justify-center">
        <div className="w-64 h-64 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center text-gray-500 dark:text-gray-400">
          <FaGraduationCap size={96} />
        </div>
      </div>
    </div>
  </section>
);

const CoursesSection = () => {
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
      <section className="py-20 px-4 max-w-7xl mx-auto text-center text-gray-700 dark:text-gray-300">
        <FaSpinner className="animate-spin inline-block mr-2" size={32} />
        Loading courses...
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-20 px-4 max-w-7xl mx-auto text-center text-red-500">
        <FaExclamationTriangle className="inline-block mr-2" size={32} />
        {error}
      </section>
    );
  }

  return (
    <section className="py-20 px-4 max-w-7xl mx-auto ">
      <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-12">Popular Courses</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {courses.map(course => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
      <div className="text-center mt-12">
        <Link to="/courses" className="text-purple-600 dark:text-purple-400 font-semibold inline-flex items-center hover:underline">
          View All Courses <FaArrowRight className="ml-2" />
        </Link>
      </div>
    </section>
  );
};

const InstructorsSection = () => {
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
      <section className="py-20 px-4 max-w-7xl mx-auto text-center text-gray-700 dark:text-gray-300">
        <FaSpinner className="animate-spin inline-block mr-2" size={32} />
        Loading instructors...
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-20 px-4 max-w-7xl mx-auto text-center text-red-500">
        <FaExclamationTriangle className="inline-block mr-2" size={32} />
        {error}
      </section>
    );
  }

   return (
    <section className="py-20 px-4 max-w-7xl mx-auto bg-gray-100 dark:bg-gray-700">
      <h2 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-12">Meet Our Instructors</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        {instructors.map(instructor => (
          <InstructorCard key={instructor.id} instructor={instructor} />
        ))}
      </div>
      <div className="text-center mt-12">
        <Link to="/instructors" className="text-purple-600 dark:text-purple-400 font-semibold inline-flex items-center hover:underline">
          View All Instructors <FaArrowRight className="ml-2" />
        </Link>
      </div>
    </section>
  );
};

const BrowseSection = () => (
  <section className="py-20 px-4 max-w-7xl mx-auto text-center">
    <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">Start Your Journey Today</h2>
    <p className="text-gray-700 dark:text-gray-300 text-lg mb-8">
      Discover a world of knowledge with our comprehensive courses and expert instructors.
    </p>
    <div className="flex flex-col sm:flex-row justify-center gap-4">
      <Link to="/courses">
        <button className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors duration-300">
          Browse All Courses
        </button>
      </Link>
      <Link to="/instructors">
        <button className="px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 transition-colors duration-300">
          Browse All Instructors
        </button>
      </Link>
    </div>
  </section>
);

export default function Home() {
  return (
    <div className="transition-colors duration-300">
      <DesignerIntro />
      <CoursesSection />
      <InstructorsSection />
      <BrowseSection />
    </div>
  );
}

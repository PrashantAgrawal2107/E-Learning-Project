import { FaEnvelope } from 'react-icons/fa';
import { Link } from 'react-router-dom';


type Instructor = {
  id: number;
  name: string;
  email: string;
  created_on: string;
  updated_on: string;
  courses: Array<any>;
  image?: string;
};

const DUMMY_IMAGE = 'data:image/jpeg;base64,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';

type InstructorCardProps = {
  instructor: Instructor;
};

export default function InstructorCard({ instructor }: InstructorCardProps) {
  return (
    <div key={instructor.id} className="bg-white dark:bg-gray-800 shadow-lg rounded-xl overflow-hidden transition-transform transform hover:scale-105 p-6 text-center">
      <img
        src={instructor.image || DUMMY_IMAGE}
        alt={instructor.name}
        className="w-32 h-32 rounded-full mx-auto mb-4 object-cover"
      />
      <h3 className="text-xl font-bold text-gray-900 dark:text-white">{instructor.name}</h3>
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 flex items-center justify-center gap-2">
        <FaEnvelope />
        <span>{instructor.email}</span>
      </p>
      <div className="mt-4">
        <Link to={`/instructor/${instructor.id}`}>
          <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg shadow-md hover:from-purple-600 hover:to-pink-600 transition-colors duration-300">
            View Profile
          </button>
        </Link>
      </div>
    </div>
  );
}

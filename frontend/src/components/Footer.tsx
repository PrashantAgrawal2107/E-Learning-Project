import { Link } from 'react-router-dom';
import { FaFacebook, FaInstagram, FaTwitter, FaGithub, FaDribbble } from 'react-icons/fa';

export default function FooterCom() {
  return (
    <footer className='border-t-8 border-teal-500 bg-white dark:bg-gray-800'>
      <div className='w-full max-w-7xl mx-auto p-4 md:py-8'>
        <div className='grid w-full justify-between sm:flex md:grid-cols-1'>
          <div className='mt-5'>
            <Link to='/' className='self-center whitespace-nowrap text-lg sm:text-xl font-semibold dark:text-white'>
              <span className='px-2 py-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-lg text-yellow-100'>
                Harshil's
              </span>
              Academy
            </Link>
          </div>
          <div className='grid grid-cols-2 gap-8 mt-4 sm:mt-5 sm:grid-cols-3 sm:gap-6'>
            {/* About Section */}
            <div>
              <h2 className='mb-6 text-sm font-semibold uppercase text-gray-500 dark:text-white'>About</h2>
              <ul className='flex flex-col gap-4 text-gray-500 dark:text-gray-400'>
                <li>
                  <a href='#' target='_blank' rel='noopener noreferrer' className='hover:underline'>
                    Harshil's Projects
                  </a>
                </li>
                <li>
                  <a href='#' target='_blank' rel='noopener noreferrer' className='hover:underline'>
                    Harshil's Academy
                  </a>
                </li>
              </ul>
            </div>
            {/* Follow Us Section */}
            <div>
              <h2 className='mb-6 text-sm font-semibold uppercase text-gray-500 dark:text-white'>Follow us</h2>
              <ul className='flex flex-col gap-4 text-gray-500 dark:text-gray-400'>
                <li>
                  <a href='#' target='_blank' rel='noopener noreferrer' className='hover:underline'>
                    Github
                  </a>
                </li>
                <li>
                  <a href='#' target='_blank' rel='noopener noreferrer' className='hover:underline'>
                    Discord
                  </a>
                </li>
              </ul>
            </div>
            {/* Legal Section */}
            <div>
              <h2 className='mb-6 text-sm font-semibold uppercase text-gray-500 dark:text-white'>Legal</h2>
              <ul className='flex flex-col gap-4 text-gray-500 dark:text-gray-400'>
                <li>
                  <a href='#' className='hover:underline'>
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href='#' className='hover:underline'>
                    Terms & Conditions
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <hr className='my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8' />
        <div className='w-full sm:flex sm:items-center sm:justify-between'>
          <span className='text-sm text-gray-500 sm:text-center dark:text-gray-400'>
            © {new Date().getFullYear()}
            <a href='#' className='ml-1 hover:underline'>Harshil's Academy</a>. All Rights Reserved.
          </span>
          <div className='flex gap-6 mt-4 sm:mt-0 sm:justify-center'>
            <a href='#' className='text-gray-500 hover:text-gray-900 dark:hover:text-white'>
              <FaFacebook />
              <span className='sr-only'>Facebook page</span>
            </a>
            <a href='#' className='text-gray-500 hover:text-gray-900 dark:hover:text-white'>
              <FaInstagram />
              <span className='sr-only'>Instagram page</span>
            </a>
            <a href='#' className='text-gray-500 hover:text-gray-900 dark:hover:text-white'>
              <FaTwitter />
              <span className='sr-only'>Twitter page</span>
            </a>
            <a href='#' className='text-gray-500 hover:text-gray-900 dark:hover:text-white'>
              <FaGithub />
              <span className='sr-only'>Github account</span>
            </a>
            <a href='#' className='text-gray-500 hover:text-gray-900 dark:hover:text-white'>
              <FaDribbble />
              <span className='sr-only'>Dribbble account</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

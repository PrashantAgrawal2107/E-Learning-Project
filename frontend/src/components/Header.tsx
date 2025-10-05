import { useState, useEffect } from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';
import { Link, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { signoutSuccess } from '../redux/user/userSlice';
import { toggleTheme } from '../redux/theme/themeSlice';
import type { AppDispatch, RootState } from '../redux/store';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const dispatch = useDispatch<AppDispatch>();
  const path = useLocation().pathname;
  const { currentUser } = useSelector((state: RootState) => state.user);
  const { theme } = useSelector((state: RootState) => state.theme);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const isInstructor = currentUser && currentUser.role === 'instructor';
  const navigate = useNavigate();

    useEffect(() => {
    // Jab bhi currentUser change ho, dropdown close kar do
    setIsDropdownOpen(false);
  }, [currentUser]);

  const handleSignout = async () => {
    try {
      const res = await fetch('/api/auth/signout', {
        method: 'POST',
      });
      const data = await res.json();
      if (!res.ok) {
        console.log(data.message);
      } else {
        dispatch(signoutSuccess());
      }
      navigate('/');
    } catch (error: any) {
      console.log(error.message);
    }
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className='relative border-b-2 bg-white dark:bg-gray-800 dark:border-gray-700'>
      <div className='flex items-center justify-between p-3 max-w-7xl mx-auto'>
        {/* Left side: Logo */}
        <Link to='/' className='self-center whitespace-nowrap text-sm sm:text-xl font-semibold dark:text-white'>
          <span className='rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 px-2 py-1 text-yellow-100'>
            Harshil's
          </span>
          Academy
        </Link>

        {/* Center: Navigation Links (hidden on small screens) */}
        <div className='hidden md:flex gap-4'>
          <Link
            to='/'
            className={`text-gray-700 dark:text-white hover:underline ${path === '/' ? 'underline' : ''}`}
          >
            Home
          </Link>
          <Link
            to='/about'
            className={`text-gray-700 dark:text-white hover:underline ${path === '/about' ? 'underline' : ''}`}
          >
            About
          </Link>
          <Link
            to='/courses'
            className={`text-gray-700 dark:text-white hover:underline ${path === '/courses' ? 'underline' : ''}`}
          >
            Courses
          </Link>
        </div>

      <div className="navbar-links">
        {isInstructor && (
          <Link
            to="/create-course"
            className="px-3 py-1 bg-purple-500 hover:bg-purple-600 text-white rounded-md text-sm font-medium transition-colors"
          >
            Add Course
          </Link>
        )}
      </div>



        {/* Right side: Theme Toggle and Auth Buttons/Profile */}
        <div className='flex gap-2 items-center'>
          {/* Theme toggle button */}
          <button
            className='h-10 w-12 rounded-full border border-gray-300 dark:border-gray-600 flex items-center justify-center text-gray-700 dark:text-white transition-all hover:bg-gray-100 dark:hover:bg-gray-700'
            onClick={() => dispatch(toggleTheme())}
            aria-label='Toggle theme'
          >
            {theme === 'dark' ? <FaSun /> : <FaMoon />}
          </button>

          {/* User profile dropdown or sign in button */}
          {currentUser ? (
            <div className='relative bg-gray-200 dark:bg-gray-600 rounded-full'>
              <button
                className='h-10 w-10 overflow-hidden rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 dark:focus:ring-offset-gray-800'
                onClick={toggleDropdown}
                aria-label='Open user menu'
              >
                {/* <img
                  src={currentUser.avatar}
                  alt='user avatar'
                  className='h-full w-full object-cover'
                /> */}
                <span>{currentUser.name[0]}</span>
              </button>
              {isDropdownOpen && (
                <div className='absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white dark:bg-gray-700 ring-1 ring-black ring-opacity-5 z-50'>
                  <div className='py-1' role='menu' aria-orientation='vertical' aria-labelledby='user-menu'>
                    <div className='px-4 py-2 text-sm text-gray-700 dark:text-gray-200'>
                      <div className='font-medium'>@{currentUser.username}</div>
                      <div className='truncate'>{currentUser.email}</div>
                    </div>
                    <div className='border-t border-gray-100 dark:border-gray-600' />
                    <Link
                      to={'/dashboard?tab=profile'}
                      className='block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600'
                      onClick={toggleDropdown}
                    >
                      Profile
                    </Link>
                    <button
                      onClick={handleSignout}
                      className='block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600'
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <Link to='/login'>
              <button
                className='rounded-md px-4 py-2 text-white bg-gradient-to-r from-purple-500 to-pink-500 transition-colors duration-200 hover:from-purple-600 hover:to-pink-600'
              >
                Sign In
              </button>
            </Link>
          )}

          {/* Mobile menu toggle button (visible on small screens) */}
          <button
            className='md:hidden h-10 w-10 flex items-center justify-center text-gray-700 dark:text-white focus:outline-none'
            onClick={toggleMobileMenu}
            aria-label='Toggle mobile menu'
          >
            {/* Hamburger icon or close icon */}
            <svg
              className={`h-6 w-6 transition-transform duration-300 ${isMobileMenuOpen ? 'rotate-90' : ''}`}
              xmlns='http://www.w3.org/2000/svg'
              fill='none'
              viewBox='0 0 24 24'
              stroke='currentColor'
            >
              <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M4 6h16M4 12h16m-7 6h7' />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu (visible when toggled) */}
      {isMobileMenuOpen && (
        <div className='md:hidden flex flex-col gap-2 p-3 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700'>
          <Link
            to='/'
            className={`block py-2 px-3 text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md ${path === '/' ? 'bg-gray-100 dark:bg-gray-700' : ''}`}
            onClick={toggleMobileMenu}
          >
            Home
          </Link>
          <Link
            to='/about'
            className={`block py-2 px-3 text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md ${path === '/about' ? 'bg-gray-100 dark:bg-gray-700' : ''}`}
            onClick={toggleMobileMenu}
          >
            About
          </Link>
          <Link
            to='/courses'
            className={`block py-2 px-3 text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md ${path === '/courses' ? 'bg-gray-100 dark:bg-gray-700' : ''}`}
            onClick={toggleMobileMenu}
          >
            Courses
          </Link>
        </div>
      )}
    </nav>
  );
}

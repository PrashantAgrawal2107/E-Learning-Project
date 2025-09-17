import { Alert, Button, Label, Spinner, TextInput } from 'flowbite-react';
import { useState, type ChangeEvent, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import {
  signInStart,
  signInSuccess,
  signInFailure,
} from '../redux/user/userSlice';
// import OAuth from '../components/OAuth';
import type { AppDispatch} from '../redux/store';

// Define a type for the form data
type FormData = {
  email?: string;
  password?: string;
  role?: 'student' | 'instructor';
};

// This should match the type expected by signInSuccess.
type User = {
    id: string;
    name: string;
    email: string;
    [key: string]: any;
} | null;

export default function Login() {
  const [formData, setFormData] = useState<FormData>({ role: 'student' });
//   const { loading, error: errorMessage } = useSelector((state: RootState) => state.user);
  const loading = false;
  const errorMessage = null;
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  const handleRoleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setFormData({ ...formData, role: e.target.value as 'student' | 'instructor' });
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value.trim() });
  };
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData)
    if (!formData.email || !formData.password || !formData.role) {
      return dispatch(signInFailure('Please fill out all fields.'));
    }

    try {
      dispatch(signInStart());
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data: User = await res.json();
      if (data && data.success === false) {
        dispatch(signInFailure(data.message));
        return;
      }

      if (res.ok) {
        dispatch(signInSuccess(data));
        navigate('/');
      }
    } catch (error: any) {
      dispatch(signInFailure(error.message));
    }
  };

  // As per flowbite-react v0.11.0, 'gradientDuoTone' prop is removed from Button.
  // Using Tailwind CSS classes to mimic the gradient look.
  const gradientClass = 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600';

  return (
    <div className='min-h-screen mt-20'>
      <div className='mx-auto flex max-w-3xl flex-col gap-5 p-3 md:flex-row md:items-center'>
        {/* left */}
        <div className='flex-1'>
          <Link to='/' className='text-4xl font-bold dark:text-white'>
            <span className='rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 px-2 py-1 text-yellow-100'>
              Harshil's
            </span>
            Academy
          </Link>
          <p className='mt-5 text-sm'>
            This is an e-learning platform. You can sign in with your email and password
            or with Google.
          </p>
        </div>
        {/* right */}
        <div className='flex-1'>
          <form className='flex flex-col gap-4' onSubmit={handleSubmit}>
            <div>
              <Label htmlFor='email'>Your email</Label>
              <TextInput
                type='email'
                placeholder='name@company.com'
                id='email'
                onChange={handleChange}
              />
            </div>
            <div>
              <Label htmlFor='password'>Your password</Label>
              <TextInput
                type='password'
                placeholder='*********'
                id='password'
                autoComplete='off'
                onChange={handleChange}
              />
            </div>
            <div className='flex flex-col gap-2'>
              <Label>Select your role:</Label>
              <div className='flex items-center gap-4'>
                <div className='flex items-center gap-2'>
                  <input
                    type='radio'
                    id='student'
                    name='role'
                    value='student'
                    checked={formData.role === 'student'}
                    onChange={handleRoleChange}
                  />
                  <Label htmlFor='student'>Student</Label>
                </div>
                <div className='flex items-center gap-2'>
                  <input
                    type='radio'
                    id='instructor'
                    name='role'
                    value='instructor'
                    checked={formData.role === 'instructor'}
                    onChange={handleRoleChange}
                  />
                  <Label htmlFor='instructor'>Instructor</Label>
                </div>
              </div>
            </div>
            <Button
              className={gradientClass}
              type='submit'
              disabled={loading}
            >
              {loading ? (
                <>
                  <Spinner size='sm' />
                  <span className='pl-3'>Loading...</span>
                </>
              ) : (
                'Sign In'
              )}
            </Button>
            {/* <OAuth /> */}
          </form>
          <div className='mt-5 flex gap-2 text-sm'>
            <span>Do not have an account?</span>
            <Link to='/sign-up' className='text-blue-500'>
              Sign Up
            </Link>
          </div>
          {errorMessage && (
            <Alert className='mt-5' color='failure'>
              {errorMessage}
            </Alert>
          )}
        </div>
      </div>
    </div>
  );
}

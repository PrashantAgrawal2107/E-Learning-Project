import { Alert, Button, Label, Spinner, TextInput } from 'flowbite-react';
import { useState, type ChangeEvent, type FormEvent, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  signInStart,
  signInSuccess,
  signInFailure,
} from '../redux/user/userSlice';
import type { AppDispatch, RootState } from '../redux/store';

type FormData = {
  email?: string;
  password?: string;
  role?: 'student' | 'instructor';
};

export default function Login() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  // Redux state
  const { currentUser } = useSelector((state: RootState) => state.user);

  // Local states
  const [formData, setFormData] = useState<FormData>({ role: 'student' });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Reset error on component mount or page refresh
  useEffect(() => {
    setErrorMessage(null);
  }, []);

  const handleRoleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, role: e.target.value as 'student' | 'instructor' });
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value.trim() });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!formData.email || !formData.password || !formData.role) {
      setErrorMessage('Please fill out all fields.');
      return;
    }

    try {
      setIsSubmitting(true);
      setErrorMessage(null);

      dispatch(signInStart());

      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok || (data && data.success === false)) {
        const msg = data.detail || data.message || 'Login failed';
        dispatch(signInFailure(msg));
        setErrorMessage(msg);
        return;
      }

      dispatch(signInSuccess(data));
      navigate('/'); // Redirect after successful login
    } catch (err: any) {
      const msg = err.message || 'Something went wrong';
      dispatch(signInFailure(msg));
      setErrorMessage(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const gradientClass =
    'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600';

  return (
    <div className="min-h-screen mt-20">
      <div className="mx-auto flex max-w-3xl flex-col gap-5 p-3 md:flex-row md:items-center">
        {/* Left side */}
        <div className="flex-1">
          <Link to="/" className="text-4xl font-bold dark:text-white">
            <span className="rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 px-2 py-1 text-yellow-100">
              Harshil's
            </span>
            Academy
          </Link>
          <p className="mt-5 text-sm">
            This is an e-learning platform. You can sign in with your email and password or with Google.
          </p>
        </div>

        {/* Right side */}
        <div className="flex-1">
          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <div>
              <Label htmlFor="email">Your email</Label>
              <TextInput type="email" placeholder="name@company.com" id="email" onChange={handleChange} />
            </div>
            <div>
              <Label htmlFor="password">Your password</Label>
              <TextInput
                type="password"
                placeholder="*********"
                id="password"
                autoComplete="off"
                onChange={handleChange}
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label>Select your role:</Label>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="student"
                    name="role"
                    value="student"
                    checked={formData.role === 'student'}
                    onChange={handleRoleChange}
                  />
                  <Label htmlFor="student">Student</Label>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    id="instructor"
                    name="role"
                    value="instructor"
                    checked={formData.role === 'instructor'}
                    onChange={handleRoleChange}
                  />
                  <Label htmlFor="instructor">Instructor</Label>
                </div>
              </div>
            </div>

            <Button className={gradientClass} type="submit" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Spinner size="sm" />
                  <span className="pl-3">Loading...</span>
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </form>

          <div className="mt-5 flex gap-2 text-sm">
            <span>Do not have an account?</span>
            <Link to="/sign-up" className="text-blue-500">
              Sign Up
            </Link>
          </div>

          {errorMessage && (
            <Alert className="mt-5" color="failure">
              {errorMessage}
            </Alert>
          )}
        </div>
      </div>
    </div>
  );
}

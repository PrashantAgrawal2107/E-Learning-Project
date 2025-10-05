import { Alert, Button, Label, Spinner, TextInput } from 'flowbite-react';
import { useState, type ChangeEvent, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
// import OAuth from '../components/OAuth';

// Define a type for the form data, including the new 'role' field
type FormData = {
  name?: string;
  email?: string;
  password?: string;
  role?: 'student' | 'instructor';
};

export default function SignUp() {
  const [formData, setFormData] = useState<FormData>({ role: 'student' }); // Set a default role
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setFormData({ ...formData, [e.target.id]: e.target.value.trim() });
  };
  
  const handleRoleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setFormData({ ...formData, role: e.target.value as 'student' | 'instructor' });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
  e.preventDefault();
  if (!formData.name || !formData.email || !formData.password) {
    setErrorMessage('Please fill out all fields.');
    return;
  }
  try {
    setLoading(true);
    setErrorMessage(null);

    const url =
      formData.role === 'student'
        ? 'http://localhost:8000/api/students/'
        : 'http://localhost:8000/api/instructors/';

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await res.json();
    console.log('Response:', data);

    if (!res.ok) {
      // ✅ agar FastAPI se "detail" field aayi hai
      if (data.detail) {
        setErrorMessage(
          typeof data.detail === 'string'
            ? data.detail
            : Array.isArray(data.detail)
            ? data.detail.map((d: any) => d.msg).join(', ') // validation errors
            : 'Something went wrong'
        );
      } else if (data.message) {
        setErrorMessage(data.message);
      } else {
        setErrorMessage('Registration failed. Please try again.');
      }
      setLoading(false);
      return;
    }

    // ✅ success case
    setLoading(false);
    navigate('/login');
  } catch (error) {
    if (error instanceof Error) {
      setErrorMessage(error.message);
    } else {
      setErrorMessage('An unexpected error occurred.');
    }
    setLoading(false);
  }
};


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
            This is an e-learning platform. You can sign up with your email and password
            or with Google.
          </p>
        </div>
        {/* right */}
        <div className='flex-1'>
          <form className='flex flex-col gap-4' onSubmit={handleSubmit}>
            <div>
              <Label htmlFor='name'>Your username</Label>
              <TextInput
                type='text'
                placeholder='Name'
                id='name'
                onChange={handleChange}
              />
            </div>
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
                placeholder='**********'
                id='password'
                autoComplete='off'
                onChange={handleChange}
              />
            </div>

            {/* Role selection using radio buttons */}
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
              type='submit'
              disabled={loading}
              className='bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600'
            >
              {loading ? (
                <>
                  <Spinner size='sm' />
                  <span className='pl-3'>Loading...</span>
                </>
              ) : (
                'Sign Up'
              )}
            </Button>
            {/* <OAuth /> */}
          </form>
          <div className='mt-5 flex gap-2 text-sm'>
            <span>Have an account?</span>
            <Link to='/login' className='text-blue-500'>
              Sign In
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

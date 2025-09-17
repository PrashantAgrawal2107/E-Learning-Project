// import { Button } from 'flowbite-react';
// import { AiFillGoogleCircle } from 'react-icons/ai';
// import { GoogleAuthProvider, signInWithPopup, getAuth, type User } from 'firebase/auth';
// import { app } from '../firebase';
// import { useDispatch } from 'react-redux';
// import { signInSuccess } from '../redux/user/userSlice';
// import { useNavigate } from 'react-router-dom';
// import type { AppDispatch } from '../redux/store';

// // Define the expected structure of the response data from the backend
// interface AuthResponse {
//     name: string;
//     email: string;
//     googlePhotoUrl: string;
// }

// export default function OAuth(): JSX.Element {
  
//   const auth = getAuth(app);  
//   const dispatch = useDispatch<AppDispatch>();
//   const navigate = useNavigate();

//   const handleGoogleClick = async () => {
//     const provider = new GoogleAuthProvider();
//     provider.setCustomParameters({ prompt: 'select_account' });
    
//     try {
//         const resultsFromGoogle = await signInWithPopup(auth, provider);
//         const { displayName, email, photoURL } = resultsFromGoogle.user;

//         const res = await fetch('/api/auth/google', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({
//                 name: displayName,
//                 email: email,
//                 googlePhotoUrl: photoURL,
//             }),
//         });

//         // The fetch operation might fail, so we need to check the `ok` property.
//         if (!res.ok) {
//             // Handle the case where the server returns a non-success status code
//             console.error('Backend sign-in failed');
//             return;
//         }

//         const data: AuthResponse = await res.json();
//         dispatch(signInSuccess(data));
//         navigate('/');

//     } catch (error) {
//         if (error instanceof Error) {
//             console.error('Could not sign in with Google:', error.message);
//         } else {
//             console.error('An unknown error occurred during Google sign-in.');
//         }
//     }
//   };

//   return (
//     <Button type='button' gradientDuoTone='pinkToOrange' outline onClick={handleGoogleClick}>
//         <AiFillGoogleCircle className='h-6 w-6 mr-2' />
//         Continue with Google
//     </Button>
//   );
// }

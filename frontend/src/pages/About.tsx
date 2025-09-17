// A simple About page to demonstrate the theme change.
// The styles will automatically respond to the 'dark' class on the <html> tag.
export default function About() {
  return (
    <div className='flex items-center justify-center min-h-screen p-6'>
      <div className='max-w-2xl text-center'>
        <h1 className='text-3xl sm:text-4xl font-bold mb-4'>About Harshil's Academy</h1>
        <p className='text-lg mb-4'>
          Harshil's Academy is an innovative e-learning platform dedicated to providing high-quality educational content. Our mission is to make learning accessible and engaging for everyone, regardless of their background or experience level.
        </p>
        <p className='text-md mb-4'>
          We offer a wide range of courses taught by expert instructors. Our platform is designed to provide a seamless learning experience, with interactive lessons, comprehensive resources, and a supportive community.
        </p>
        <p className='text-md'>
          Join us on our journey to unlock your full potential and achieve your learning goals. Whether you are a student or an instructor, we have something to offer for everyone.
        </p>
      </div>
    </div>
  );
}

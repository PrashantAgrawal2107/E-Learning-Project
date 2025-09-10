import { useState, useEffect } from 'react';
import './App.css';


function App() {

  type Instructor = {
    id: number,
    name: string,
    role: string
  }

  const [instructors, setInstructors] = useState<Instructor[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Define the async function to fetch data
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/instructors');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setInstructors(result);
        console.log(result[0])
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // The empty dependency array ensures this effect runs only once on mount

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI and React Integration</h1>
        <h2>Our Instructors</h2>
        {instructors && instructors.length > 0 ? (
          <ul>
            {instructors.map((instructor) => (
              <li key={instructor.id}>
                **{instructor.name}** - {instructor.role}
              </li>
            ))}
          </ul>
        ) : (
          <p>No instructors found.</p>
        )}
      </header>
    </div>
  );
}

export default App;

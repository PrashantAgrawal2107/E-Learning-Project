import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.tsx'; 
import SignUp from './pages/SignUp';
import Login from './pages/Login.tsx';
import About from './pages/About.tsx';
import Header from './components/Header.tsx'; 
import FooterCom from './components/Footer.tsx'; 

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <FooterCom />
    </>
  );
}

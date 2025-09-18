import { useEffect, type ReactNode } from 'react';
import { useSelector } from 'react-redux';
import type { RootState } from '../redux/store';

type ThemeProviderProps = {
  children: ReactNode;
};

export default function ThemeProvider({ children }: ThemeProviderProps) {
  const { theme } = useSelector((state: RootState) => state.theme);

  // Agar tumhe sirf wrapper div par dark class lagani hai,
  // toh document.documentElement se remove kar do
  useEffect(() => {
    // optional: agar html par automatic class lag rahi thi, usko clean karo
    document.documentElement.classList.remove('dark');
  }, []);

  return (
     <div className={theme}>
           <div className='bg-white text-gray-700 dark:text-gray-200 dark:bg-[rgb(16,23,42)] min-h-screen'>
                {children}
           </div>
        </div>
  );
}

import { useEffect, type ReactNode } from 'react';
import { useSelector } from 'react-redux';
import type { RootState } from '../redux/store';

type ThemeProviderProps = {
  children: ReactNode;
};

export default function ThemeProvider({ children }: ThemeProviderProps) {
  const { theme } = useSelector((state: RootState) => state.theme);

  useEffect(() => {
    const htmlElement = document.documentElement;
    if (theme === 'dark') {
      htmlElement.classList.add('dark');
    } else {
      htmlElement.classList.remove('dark');
    }
  }, [theme]);

  // Keep the wrapper div for consistent styling, but the actual dark mode logic is now on the <html> tag.
  return (
    <div className='bg-white text-gray-700 dark:text-gray-200 dark:bg-[rgb(16,23,42)] min-h-screen transition-colors duration-300'>
      {children}
    </div>
  );
}

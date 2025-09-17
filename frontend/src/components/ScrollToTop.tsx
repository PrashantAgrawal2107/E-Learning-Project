import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import type { Location } from 'react-router-dom';

const ScrollToTop = (): null => {
  const location: Location = useLocation();
  const { pathname } = location;

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

export default ScrollToTop;

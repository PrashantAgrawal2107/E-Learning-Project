import { useSelector } from 'react-redux';
import { Outlet, Navigate } from 'react-router-dom';
import type { RootState } from '../redux/store';

export default function OnlyInstructorPrivateRoute(){
  const { currentUser } = useSelector((state: RootState) => state.user);

  return currentUser && currentUser.role=='instructor' ? (
    <Outlet />
  ) : (
    <Navigate to='/login' />
  );
}

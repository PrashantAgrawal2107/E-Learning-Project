import { useSelector } from 'react-redux';
import { Outlet, Navigate } from 'react-router-dom';
import type { RootState } from '../redux/store';

export default function OnlyAdminPrivateRoute(){
  const { currentUser } = useSelector((state: RootState) => state.user);

  return currentUser && currentUser.isAdmin ? (
    <Outlet />
  ) : (
    <Navigate to='/login' />
  );
}

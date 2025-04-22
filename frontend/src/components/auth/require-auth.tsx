import { ReactElement, FC } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStateStore } from '../../state/auth/auth-state';

export type RequireAuthProps = {
  redirectPath: string,
  children?: ReactElement
}

const RequireAuth: FC<RequireAuthProps> = ({ redirectPath, children }) => {
  const authState = useAuthStateStore();
  if (!authState.hasBearerToken()) {
    return <Navigate to={ redirectPath } />;
  }
  return children ? children : <Outlet />;
}

export default RequireAuth;

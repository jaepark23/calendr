import { useAuth } from '../auth/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';

function ProtectedRoute({Component}) {
    const { isAuthenticated } = useAuth();

    if (isAuthenticated === null) {
        return <div>Loading...</div>; 
    }

    return isAuthenticated ? <Component /> : <Navigate to="/login" />
}

export default ProtectedRoute;
import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const AuthContext = createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);
    const [loading, setLoading] = useState(false);
    const [token, setToken] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();
    
    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    };

    useEffect(() => {
        const checkAuth = async () => {
            // use local cookies to authenticate user 
            const token = getCookie('access_token'); 
            if (!token) {
                setIsAuthenticated(false);
                navigate('/login');
                return;
            }
            // verify token is valid 
            try {
                const response = await fetch('http://localhost:8000/validate_token', {
                    method: 'GET',
                    credentials: 'include', 
                });
                const data = await response.json();
                if (data.valid) {
                    setIsAuthenticated(true);
                    // navigate to home if user is first logging in, otherwise let user navigate wherever they were going
                    if (location.pathname === '/login') {
                        navigate('/home');
                    }
                } else {
                    setIsAuthenticated(false);
                    navigate('/login');
                }
            } catch (error) {
                console.error('Error validating token:', error);
                setIsAuthenticated(false);
                navigate('/login');
            }
        };

        // only check if user hasn't been authenciated yet
        if (isAuthenticated === null) {
            checkAuth();
        }
    }, [isAuthenticated, navigate, location.pathname]);

    const value = {
        isAuthenticated,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}

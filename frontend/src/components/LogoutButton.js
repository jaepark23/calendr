import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '../auth/AuthContext';
import { Button } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import { Link } from 'react-router-dom';

export function LogoutButton() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        fetch('http://localhost:8000/logout', {
            method: 'POST',
            credentials: 'include',
        })
        .then(response => {
            if (response.ok) {
                navigate('/login');
            }
        })
        .catch(error => {
            console.error('Logout failed:', error);
        });
    };

    return (
        <Button
        component={Link}
        color="inherit"
        onClick={handleLogout}
        >
        Sign out
        </Button>
    );
}


export default LogoutButton;
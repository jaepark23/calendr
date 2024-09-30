import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GoogleIcon from '@mui/icons-material/Google';
import Button from '@mui/material/Button';

function GoogleLogin() {
    const navigate = useNavigate();

    const handleLogin = () => {
        window.location.href = 'http://localhost:8000/login';
    };

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        if (code) {
            // fetch token from FastAPI callback endpoint
            fetch(`http://localhost:8000/callback?code=${code}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.token) {
                        navigate('/home');
                    } else {
                        console.error('Token not found in response');
                    }
                })
                .catch(error => {
                    console.error('Error fetching token:', error);
                });
        }
    }, [navigate]);
    

    return (
        <div>
            <Button
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<GoogleIcon />}
            onClick={handleLogin}
            >
            Sign in with Google
            </Button>
        </div>
    );
}

export default GoogleLogin;

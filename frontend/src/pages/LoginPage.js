import React from "react";
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import GoogleLogin from "../components/GoogleLogin"


function LoginPage() {
  return (
    <div>
      <CssBaseline />
      <Container
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
          alignItems: 'top',
          minHeight: '100vh',
        }}
      >
        <main
          style={{
            marginTop: '25vh', 
            width: '100%', 
            textAlign: 'center', 
          }}
        >
          <h1 style={{ fontSize: '3rem' }}>Calendr</h1>
          <h1 style={{ fontSize: '2rem' }}>Login to your account</h1>
          <GoogleLogin />
        </main>

      </Container>
      </div>
  );
}

export default LoginPage;

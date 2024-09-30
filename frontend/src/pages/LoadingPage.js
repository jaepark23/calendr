import React, {useState} from 'react';
import { Box, CircularProgress, Typography, } from '@mui/material';

function LoadingPage() {
const [loading, setLoading] = useState(false);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#000', 
        color: '#fff',
        gap: 2,
      }}
    >
      <CircularProgress color="inherit" />
      <Typography variant="h6">Loading...</Typography>
    </Box>
  );
}

export default LoadingPage;

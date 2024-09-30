import React, { useState } from 'react';
import { AppBar, Toolbar, Box, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import LogoutButton from "./LogoutButton"

function TopBar() {
  
  return (
    <>
      <AppBar position="fixed" color="transparent" elevation={0}>
        <Toolbar>
        <Box sx={{ marginRight: 'auto', display: 'flex', alignItems: 'center' }}>
        <h3 style={{ marginRight: '16px' }}>Calendr</h3>
            <Button component={Link} color="inherit" to="/">Home</Button>
            <Button component={Link} color="inherit" to="/faq">FAQ</Button>
            <Button component={Link} color="inherit" to="/contact">Contact</Button>
          </Box>
          <Box sx={{ marginLeft: 'auto', display: 'flex', alignItems: 'center' }}>
            <LogoutButton />
          </Box>
        </Toolbar>
      </AppBar>
      </>
  );
}

export default TopBar;

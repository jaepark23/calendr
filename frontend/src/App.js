import React from 'react';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import theme from './theme';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import LoadingPage from './pages/LoadingPage';
function App() {

  return (
    <div className="App">
      <ThemeProvider theme={theme}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<ProtectedRoute Component={HomePage} />} />
        <Route path = "/loading" element={<ProtectedRoute Component={LoadingPage} />} />
        {/* <Route path = "*" element={<HomePage />} /> */}
      </Routes>
      </ThemeProvider>
    </div>
  );
}

export default App;

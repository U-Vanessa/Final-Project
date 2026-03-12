// App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeModeProvider } from './contexts/ThemeContext';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/Login/LoginPage';
import './styles/global.css';
import UserDashboard from './pages/Dashboards/User Dashboard/userdashboard';
import VoucherPage from './pages/Voucherpage';
import Chatbot from './pages/Chatbot';
import Report from './pages/Report';
import Settings from '../src/pages/Settings';
import DataAssets from './pages/DataAssets';
import Disposal from './pages/Disposal';
import Document from './pages/Document';
import ITDashboard from './pages/Dashboards/IT Dashboard/itdashboard';

const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',
      light: '#a3b1ff',
      dark: '#5348b7',
    },
    secondary: {
      main: '#764ba2',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
  },
  shape: {
    borderRadius: 12,
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ThemeModeProvider>
        <AuthProvider>
          <Router>
            <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/login" element={<LoginPage />} />
            
            <Route path="/user-dashboard" element={
              <ProtectedRoute requiredRoles={['user']}>
                <UserDashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/it-dashboard" element={
              <ProtectedRoute requiredRoles={['admin', 'manager', 'it']}>
                <ITDashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/voucher" element={
              <ProtectedRoute requiredRoles={['*']}>
                <VoucherPage />
              </ProtectedRoute>
            } />
            
            <Route path="/chatbot" element={
              <ProtectedRoute requiredRoles={['*']}>
                <Chatbot />
              </ProtectedRoute>
            } />
            
            <Route path="/report" element={
              <ProtectedRoute requiredRoles={['*']}>
                <Report />
              </ProtectedRoute>
            } />
            
            <Route path="/settings" element={
              <ProtectedRoute requiredRoles={['*']}>
                <Settings />
              </ProtectedRoute>
            } />

            <Route path="/settings/it" element={
              <ProtectedRoute requiredRoles={['admin', 'manager', 'it']}>
                <Settings />
              </ProtectedRoute>
            } />
            
            <Route path="/data-assets" element={
              <ProtectedRoute requiredRoles={['admin', 'manager', 'it']}>
                <DataAssets />
              </ProtectedRoute>
            } />
            
            <Route path="/disposal" element={
              <ProtectedRoute requiredRoles={['admin', 'manager', 'it']}>
                <Disposal />
              </ProtectedRoute>
            } />
            
            <Route path="/document" element={
              <ProtectedRoute requiredRoles={['*']}>
                <Document />
              </ProtectedRoute>
            } />
            
            <Route path="*" element={<LoginPage />} />
            </Routes>
          </Router>
        </AuthProvider>
      </ThemeModeProvider>
    </ThemeProvider>
  );
}

export default App;
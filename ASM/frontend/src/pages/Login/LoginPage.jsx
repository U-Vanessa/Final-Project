// src/pages/Login/LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Login.css';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      // REMOVED: "as LoginResponse" - this was causing the error
      const result = await login(email, password);
      
      if (result.success) {
        // Get user role from response
        const userRole = result.data?.user?.role || 'user';
        
        // Redirect based on role
        if (userRole === 'admin' || userRole === 'manager') {
          navigate('/it-dashboard');
        } else {
          navigate('/user-dashboard');
        }
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogoError = (e) => {
    e.currentTarget.style.display = 'none';
    const fallback = document.getElementById('login-logo-fallback');
    if (fallback) {
      fallback.style.display = 'flex';
    }
  };

  return (
    <div className="login-page-root">
      <div className="glass-container">
        {/* Left: Hero section */}
        <div className="hero-side">
          <div className="logo-display">
            <div className="logo-3d">
              <img
                src="./Logo 1.png"
                alt="ASM Logo"
                className="logo-img"
                onError={handleLogoError}
              />
              <div
                className="logo-fallback"
                id="login-logo-fallback"
                style={{ display: 'none' }}
              >
                ASM
              </div>
            </div>

            <div className="hero-title">
              <h1>ICT-TOOLS ASM</h1>
              <div className="acronym">
                ASSET &amp; SUPPORT MANAGEMENT SYSTEM (ASM)
              </div>
            </div>
          </div>

          <p className="hero-text">
            Track, manage, and optimize your entire ICT infrastructure in one
            place!
          </p>
        </div>

        {/* Right: Login section */}
        <div className="login-side">
          <div className="login-header">
            <h2>LOG IN</h2>
          </div>

          <div className="form-container">
            {error && (
              <div className="error-message" style={{
                backgroundColor: '#ffe6e6',
                color: '#cc0000',
                padding: '10px',
                borderRadius: '4px',
                marginBottom: '20px',
                border: '1px solid #ffcccc'
              }}>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Email Address</label>
                <div className="input-wrapper">
                  <input
                    type="email"
                    id="email"      
                    name="email" 
                    className="form-input"
                    placeholder="Enter your email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    disabled={loading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Password</label>
                <div className="input-wrapper">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"       
                    name="password"
                    className="form-input"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    minLength={8}
                    required
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? '🔒' : '👁️'}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className={`submit-btn signin-btn ${loading ? 'loading' : ''}`}
                disabled={loading}
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Timeline from './components/Timeline';
import Login from './pages/Login';
import Register from './pages/Register';
import Mypage from './pages/Mypage';
import ProfileEdit from './pages/ProfileEdit';
import Bookmarks from './pages/Bookmarks';
import Settings from './pages/Settings';
import ProtectedRoute from './components/ProtectedRoute';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app-layout">
          <Navigation />
          <div className="app-main">
            <Routes>
              <Route path="/" element={<Timeline />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/mypage" element={<ProtectedRoute><Mypage /></ProtectedRoute>} />
              <Route path="/profile/edit" element={<ProtectedRoute><ProfileEdit /></ProtectedRoute>} />
              <Route path="/bookmarks" element={<ProtectedRoute><Bookmarks /></ProtectedRoute>} />
              <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

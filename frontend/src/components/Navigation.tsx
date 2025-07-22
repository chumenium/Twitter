import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import NotificationBadge from './NotificationBadge';
import './Navigation.css';

const Navigation: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('ログアウトエラー:', error);
    }
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-header">
          <div className="nav-logo">
            <i className="fab fa-twitter"></i>
          </div>
        </div>

        <div className="nav-menu">
          <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
            <i className="fas fa-home"></i>
            <span>ホーム</span>
          </Link>

          {user ? (
            <>
              <Link to="/mypage" className={`nav-item ${location.pathname === '/mypage' ? 'active' : ''}`}>
                <i className="fas fa-user"></i>
                <span>プロフィール</span>
              </Link>
              <Link to="/bookmarks" className={`nav-item ${location.pathname === '/bookmarks' ? 'active' : ''}`}>
                <i className="fas fa-bookmark"></i>
                <span>ブックマーク</span>
              </Link>
              <Link to="/notifications" className={`nav-item ${location.pathname === '/notifications' ? 'active' : ''}`}>
                <div className="nav-icon-wrapper">
                  <i className="fas fa-bell"></i>
                  <NotificationBadge />
                </div>
                <span>通知</span>
              </Link>
              <Link to="/settings" className={`nav-item ${location.pathname === '/settings' ? 'active' : ''}`}>
                <i className="fas fa-cog"></i>
                <span>設定</span>
              </Link>
            </>
          ) : (
            <>
              <Link to="/login" className={`nav-item ${location.pathname === '/login' ? 'active' : ''}`}>
                <i className="fas fa-sign-in-alt"></i>
                <span>ログイン</span>
              </Link>
              <Link to="/register" className={`nav-item ${location.pathname === '/register' ? 'active' : ''}`}>
                <i className="fas fa-user-plus"></i>
                <span>新規登録</span>
              </Link>
            </>
          )}
        </div>

        {user && (
          <div className="nav-footer">
            <button className="logout-btn" onClick={handleLogout}>
              <i className="fas fa-sign-out-alt"></i>
              <span>ログアウト</span>
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation; 
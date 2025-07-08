import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Login.css';

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(username, password);
      navigate('/');
    } catch (err: any) {
      setError('ユーザー名またはパスワードが正しくありません');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="logo">
            <i className="fab fa-twitter"></i>
          </div>
          <h1 className="login-title">ログイン</h1>
          <p className="login-subtitle">アカウントにログインしてください</p>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username" className="form-label">ユーザー名</label>
            <input
              type="text"
              id="username"
              className="form-control"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="ユーザー名を入力"
              required
              autoComplete="username"
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password" className="form-label">パスワード</label>
            <input
              type="password"
              id="password"
              className="form-control"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="パスワードを入力"
              required
              autoComplete="current-password"
              disabled={loading}
            />
          </div>
          {error && <div className="error-message"><i className="fas fa-exclamation-circle"></i> {error}</div>}
          <button type="submit" className="login-btn" disabled={loading || !username || !password}>
            {loading ? <span className="spinner"></span> : <i className="fas fa-sign-in-alt"></i>} ログイン
          </button>
        </form>
        <div className="divider"><span>または</span></div>
        <div className="signup-link">
          <p>アカウントをお持ちでない方は</p>
          <Link to="/register">新規登録</Link>
        </div>
      </div>
    </div>
  );
};

export default Login; 
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Register.css';

const Register: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    passwordConfirm: ''
  });
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // エラーをクリア
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors: {[key: string]: string} = {};

    if (!formData.username.trim()) {
      newErrors.username = 'ユーザー名は必須です';
    } else if (formData.username.length < 3) {
      newErrors.username = 'ユーザー名は3文字以上で入力してください';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'メールアドレスは必須です';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = '有効なメールアドレスを入力してください';
    }

    if (!formData.password) {
      newErrors.password = 'パスワードは必須です';
    } else if (formData.password.length < 8) {
      newErrors.password = 'パスワードは8文字以上で入力してください';
    }

    if (formData.password !== formData.passwordConfirm) {
      newErrors.passwordConfirm = 'パスワードが一致しません';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      await register(formData.username, formData.email, formData.password, formData.passwordConfirm);
      navigate('/');
    } catch (err: any) {
      if (err.response?.data) {
        const apiErrors = err.response.data;
        const newErrors: {[key: string]: string} = {};
        
        if (apiErrors.username) {
          newErrors.username = apiErrors.username[0];
        }
        if (apiErrors.email) {
          newErrors.email = apiErrors.email[0];
        }
        if (apiErrors.password) {
          newErrors.password = apiErrors.password[0];
        }
        if (apiErrors.non_field_errors) {
          newErrors.general = apiErrors.non_field_errors[0];
        }
        
        setErrors(newErrors);
      } else {
        setErrors({ general: '登録に失敗しました。もう一度お試しください。' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-header">
          <div className="logo">
            <i className="fab fa-twitter"></i>
          </div>
          <h1 className="register-title">アカウントを作成</h1>
          <p className="register-subtitle">Twitter風アプリに参加しましょう</p>
        </div>
        
        <form className="register-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username" className="form-label">ユーザー名</label>
            <input
              type="text"
              id="username"
              name="username"
              className={`form-control ${errors.username ? 'error' : ''}`}
              value={formData.username}
              onChange={handleChange}
              placeholder="ユーザー名を入力"
              required
              disabled={loading}
            />
            {errors.username && <div className="error-message">{errors.username}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">メールアドレス</label>
            <input
              type="email"
              id="email"
              name="email"
              className={`form-control ${errors.email ? 'error' : ''}`}
              value={formData.email}
              onChange={handleChange}
              placeholder="メールアドレスを入力"
              required
              disabled={loading}
            />
            {errors.email && <div className="error-message">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">パスワード</label>
            <input
              type="password"
              id="password"
              name="password"
              className={`form-control ${errors.password ? 'error' : ''}`}
              value={formData.password}
              onChange={handleChange}
              placeholder="パスワードを入力（8文字以上）"
              required
              disabled={loading}
            />
            {errors.password && <div className="error-message">{errors.password}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="passwordConfirm" className="form-label">パスワード確認</label>
            <input
              type="password"
              id="passwordConfirm"
              name="passwordConfirm"
              className={`form-control ${errors.passwordConfirm ? 'error' : ''}`}
              value={formData.passwordConfirm}
              onChange={handleChange}
              placeholder="パスワードを再入力"
              required
              disabled={loading}
            />
            {errors.passwordConfirm && <div className="error-message">{errors.passwordConfirm}</div>}
          </div>

          {errors.general && <div className="error-message general">{errors.general}</div>}

          <button type="submit" className="register-btn" disabled={loading}>
            {loading ? <span className="spinner"></span> : <i className="fas fa-user-plus"></i>} アカウントを作成
          </button>
        </form>

        <div className="divider"><span>または</span></div>
        
        <div className="login-link">
          <p>すでにアカウントをお持ちの方は</p>
          <Link to="/login">ログイン</Link>
        </div>
      </div>
    </div>
  );
};

export default Register; 
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Settings.css';

const Settings: React.FC = () => {
  const { user, updateUser, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    profile_name: ''
  });
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        profile_name: user.profile?.name || ''
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    setSuccessMessage('');
  };

  const validateForm = () => {
    const newErrors: {[key: string]: string} = {};

    if (!formData.username.trim()) {
      newErrors.username = 'ユーザー名は必須です';
    } else if (formData.username.length < 3) {
      newErrors.username = 'ユーザー名は3文字以上で入力してください';
    } else if (formData.username.length > 30) {
      newErrors.username = 'ユーザー名は30文字以内で入力してください';
    }

    if (formData.profile_name.length > 30) {
      newErrors.profile_name = 'プロフィール名は30文字以内で入力してください';
    }

    if (formData.first_name.length > 30) {
      newErrors.first_name = '姓は30文字以内で入力してください';
    }

    if (formData.last_name.length > 30) {
      newErrors.last_name = '名は30文字以内で入力してください';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      // ユーザー情報を更新
      await updateUser(formData);
      
      // プロフィール名を更新
      if (formData.profile_name !== user?.profile?.name) {
        await updateProfile({ name: formData.profile_name });
      }
      
      // ユーザー名が変更された場合の特別なメッセージ
      const originalUsername = user?.username || '';
      if (formData.username !== originalUsername) {
        setSuccessMessage('ユーザー名を更新しました。タイムラインを更新しています...');
      } else {
        setSuccessMessage('ユーザー情報を更新しました。ページを更新しています...');
      }
      
      setErrors({});
    } catch (err: any) {
      if (err.response?.data) {
        const apiErrors = err.response.data;
        const newErrors: {[key: string]: string} = {};
        
        Object.keys(apiErrors).forEach(key => {
          newErrors[key] = apiErrors[key][0];
        });
        
        setErrors(newErrors);
      } else {
        setErrors({ general: 'ユーザー情報の更新に失敗しました。もう一度お試しください。' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1 className="settings-title">設定</h1>
      </div>
      
      <div className="settings-content">
        <div className="settings-section">
          <h2>アカウント情報</h2>
          
          <form onSubmit={handleSubmit} className="settings-form">
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
                maxLength={30}
              />
              {errors.username && <div className="error-message">{errors.username}</div>}
            </div>

            <div className="form-group">
              <label htmlFor="profile_name" className="form-label">プロフィール名</label>
              <input
                type="text"
                id="profile_name"
                name="profile_name"
                className={`form-control ${errors.profile_name ? 'error' : ''}`}
                value={formData.profile_name}
                onChange={handleChange}
                placeholder="プロフィール名を入力"
                maxLength={30}
              />
              {errors.profile_name && <div className="error-message">{errors.profile_name}</div>}
            </div>

            <div className="form-group">
              <label htmlFor="first_name" className="form-label">姓</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                className={`form-control ${errors.first_name ? 'error' : ''}`}
                value={formData.first_name}
                onChange={handleChange}
                placeholder="姓を入力"
                maxLength={30}
              />
              {errors.first_name && <div className="error-message">{errors.first_name}</div>}
            </div>

            <div className="form-group">
              <label htmlFor="last_name" className="form-label">名</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                className={`form-control ${errors.last_name ? 'error' : ''}`}
                value={formData.last_name}
                onChange={handleChange}
                placeholder="名を入力"
                maxLength={30}
              />
              {errors.last_name && <div className="error-message">{errors.last_name}</div>}
            </div>

            {successMessage && (
              <div className="success-message">
                {successMessage}
              </div>
            )}

            {errors.general && (
              <div className="error-message">
                {errors.general}
              </div>
            )}

            <button
              type="submit"
              className="save-btn"
              disabled={loading}
            >
              {loading ? <span className="spinner"></span> : '保存'}
            </button>
          </form>
        </div>

        <div className="settings-section">
          <h2>その他の設定</h2>
          <ul>
            <li>メールアドレスの変更（準備中）</li>
            <li>パスワードの変更（準備中）</li>
            <li>通知設定（準備中）</li>
            <li>利用規約（準備中）</li>
            <li>プライバシーポリシー（準備中）</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Settings; 
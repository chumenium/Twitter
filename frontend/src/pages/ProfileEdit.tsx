import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { profileApi } from '../api/profile';
import './ProfileEdit.css';

const ProfileEdit: React.FC = () => {
  const { profile, updateProfile } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    bio: '',
    location: '',
    website: ''
  });
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        bio: profile.bio || '',
        location: profile.location || '',
        website: profile.website || ''
      });
      if (profile.image) {
        setImagePreview(`http://127.0.0.1:8001${profile.image}`);
      }
    }
  }, [profile]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const validateForm = () => {
    const newErrors: {[key: string]: string} = {};

    if (formData.name.length > 50) {
      newErrors.name = '名前は50文字以内で入力してください';
    }

    if (formData.bio.length > 160) {
      newErrors.bio = '自己紹介は160文字以内で入力してください';
    }

    if (formData.location.length > 30) {
      newErrors.location = '場所は30文字以内で入力してください';
    }

    if (formData.website && !/^https?:\/\/.+/.test(formData.website)) {
      newErrors.website = '有効なURLを入力してください（http://またはhttps://で始まる必要があります）';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('bio', formData.bio);
      formDataToSend.append('location', formData.location);
      formDataToSend.append('website', formData.website);
      
      if (image) {
        formDataToSend.append('image', image);
      }

      // プロフィール更新はAuthContextのupdateProfileを使用
      await updateProfile(formDataToSend);
      await updateProfile(undefined);
      // プロフィール更新後にページをリロードしてタイムラインを更新
      window.location.reload();
      navigate('/mypage');
    } catch (err: any) {
      if (err.response?.data) {
        const apiErrors = err.response.data;
        const newErrors: {[key: string]: string} = {};
        
        Object.keys(apiErrors).forEach(key => {
          newErrors[key] = apiErrors[key][0];
        });
        
        setErrors(newErrors);
      } else {
        setErrors({ general: 'プロフィールの更新に失敗しました。もう一度お試しください。' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/mypage');
  };

  return (
    <div className="profile-edit-page">
      <div className="profile-edit-container">
        <div className="profile-edit-header">
          <button className="back-btn" onClick={handleCancel}>
            <i className="fas fa-arrow-left"></i>
          </button>
          <h1 className="profile-edit-title">プロフィールを編集</h1>
          <button 
            type="submit" 
            form="profile-form" 
            className="save-btn" 
            disabled={loading}
          >
            {loading ? <span className="spinner"></span> : '保存'}
          </button>
        </div>
        
        <form id="profile-form" className="profile-edit-form" onSubmit={handleSubmit}>
          <div className="image-upload-section">
            <div className="image-preview">
              {imagePreview ? (
                <img src={imagePreview} alt="プロフィール画像" />
              ) : (
                <div className="image-placeholder">
                  <i className="fas fa-user"></i>
                </div>
              )}
            </div>
            <label className="image-upload-btn">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: 'none' }}
              />
              <i className="fas fa-camera"></i> 画像を変更
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="name" className="form-label">名前</label>
            <input
              type="text"
              id="name"
              name="name"
              className={`form-control ${errors.name ? 'error' : ''}`}
              value={formData.name}
              onChange={handleChange}
              placeholder="名前を入力"
              maxLength={50}
            />
            <div className="char-count">{formData.name.length}/50</div>
            {errors.name && <div className="error-message">{errors.name}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="bio" className="form-label">自己紹介</label>
            <textarea
              id="bio"
              name="bio"
              className={`form-control ${errors.bio ? 'error' : ''}`}
              value={formData.bio}
              onChange={handleChange}
              placeholder="自己紹介を入力"
              rows={4}
              maxLength={160}
            />
            <div className="char-count">{formData.bio.length}/160</div>
            {errors.bio && <div className="error-message">{errors.bio}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="location" className="form-label">場所</label>
            <input
              type="text"
              id="location"
              name="location"
              className={`form-control ${errors.location ? 'error' : ''}`}
              value={formData.location}
              onChange={handleChange}
              placeholder="場所を入力"
              maxLength={30}
            />
            <div className="char-count">{formData.location.length}/30</div>
            {errors.location && <div className="error-message">{errors.location}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="website" className="form-label">ウェブサイト</label>
            <input
              type="url"
              id="website"
              name="website"
              className={`form-control ${errors.website ? 'error' : ''}`}
              value={formData.website}
              onChange={handleChange}
              placeholder="https://example.com"
            />
            {errors.website && <div className="error-message">{errors.website}</div>}
          </div>

          {errors.general && <div className="error-message general">{errors.general}</div>}
        </form>
      </div>
    </div>
  );
};

export default ProfileEdit; 
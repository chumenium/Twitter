import React, { useState, useRef } from 'react';
import { postsApi } from '../api/posts';
import './CreatePost.css';

interface CreatePostProps {
  onPostCreated: () => void;
}

const CreatePost: React.FC<CreatePostProps> = ({ onPostCreated }) => {
  const [content, setContent] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const maxChars = 280;

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setContent(value);
    setCharCount(value.length);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim() || isLoading) return;
    
    setIsLoading(true);
    try {
      await postsApi.createPost({ content: content.trim(), image: image || undefined });
      setContent('');
      setImage(null);
      setImagePreview(null);
      setCharCount(0);
      onPostCreated();
    } catch (error) {
      console.error('投稿の作成に失敗しました:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const removeImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const isOverLimit = charCount > maxChars;
  const canSubmit = content.trim().length > 0 && !isOverLimit && !isLoading;

  return (
    <div className="create-post">
      <form onSubmit={handleSubmit}>
        <div className="post-input-container">
          <div className="user-avatar">
            <span>U</span>
          </div>
          
          <div className="post-input-content">
            <textarea
              className="post-textarea"
              placeholder="いまどうしてる？"
              value={content}
              onChange={handleContentChange}
              maxLength={maxChars}
              disabled={isLoading}
            />
            
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="プレビュー" />
                <button
                  type="button"
                  className="remove-image-btn"
                  onClick={removeImage}
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
            )}
            
            <div className="post-actions">
              <div className="action-buttons">
                <button
                  type="button"
                  className="action-btn"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                >
                  <i className="far fa-image"></i>
                </button>
                
                <button type="button" className="action-btn" disabled={isLoading}>
                  <i className="far fa-smile"></i>
                </button>
                
                <button type="button" className="action-btn" disabled={isLoading}>
                  <i className="fas fa-map-marker-alt"></i>
                </button>
              </div>
              
              <div className="submit-section">
                <div className="char-count">
                  <span className={isOverLimit ? 'over-limit' : ''}>
                    {maxChars - charCount}
                  </span>
                </div>
                
                <button
                  type="submit"
                  className={`submit-btn ${canSubmit ? 'active' : ''}`}
                  disabled={!canSubmit}
                >
                  {isLoading ? (
                    <i className="fas fa-spinner fa-spin"></i>
                  ) : (
                    '投稿'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleImageSelect}
          style={{ display: 'none' }}
        />
      </form>
    </div>
  );
};

export default CreatePost; 
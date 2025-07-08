import React, { useState } from 'react';
import { Post } from '../types/post';
import { postsApi } from '../api/posts';
import './PostCard.css';

interface PostCardProps {
  post: Post;
  onUpdate: () => void;
}

const PostCard: React.FC<PostCardProps> = ({ post, onUpdate }) => {
  const [isLiked, setIsLiked] = useState(post.is_liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isBookmarked, setIsBookmarked] = useState(post.is_bookmarked);
  const [isLoading, setIsLoading] = useState(false);

  const handleLike = async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await postsApi.toggleLike(post.id);
      setIsLiked(response.liked);
      setLikesCount(response.likes_count);
      onUpdate();
    } catch (error) {
      console.error('いいねの切り替えに失敗しました:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBookmark = async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await postsApi.toggleBookmark(post.id);
      setIsBookmarked(response.bookmarked);
      onUpdate();
    } catch (error) {
      console.error('ブックマークの切り替えに失敗しました:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
      return `${diffInMinutes}分`;
    } else if (diffInHours < 24) {
      return `${diffInHours}時間`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays}日`;
    }
  };

  return (
    <div className="post-card">
      <div className="post-header">
        <div className="user-avatar">
          {post.user.username.charAt(0).toUpperCase()}
        </div>
        <div className="user-info">
          <div className="user-name">{post.user.username}</div>
          <div className="user-handle">@{post.user.username}</div>
        </div>
        <div className="post-time">{formatDate(post.created_at)}</div>
      </div>
      
      <div className="post-content">
        {post.content}
      </div>
      
      {post.image && (
        <div className="post-image">
          <img src={`http://127.0.0.1:8001${post.image}`} alt="投稿画像" />
        </div>
      )}
      
      <div className="post-actions">
        <button className="action-btn" title="返信">
          <i className="action-icon far fa-comment"></i>
          <span className="action-count">0</span>
        </button>
        
        <button className="action-btn" title="リツイート">
          <i className="action-icon far fa-retweet"></i>
          <span className="action-count">0</span>
        </button>
        
        <button 
          className={`action-btn like-btn ${isLiked ? 'liked' : ''}`} 
          onClick={handleLike}
          disabled={isLoading}
          title="いいね"
        >
          <i className={`action-icon ${isLiked ? 'fas' : 'far'} fa-heart`}></i>
          <span className="action-count">{likesCount}</span>
        </button>
        
        <button 
          className={`action-btn bookmark-btn ${isBookmarked ? 'bookmarked' : ''}`} 
          onClick={handleBookmark}
          disabled={isLoading}
          title="ブックマーク"
        >
          <i className={`action-icon ${isBookmarked ? 'fas' : 'far'} fa-bookmark`}></i>
        </button>
        
        <button className="action-btn" title="シェア">
          <i className="action-icon far fa-share-square"></i>
        </button>
      </div>
    </div>
  );
};

export default PostCard; 
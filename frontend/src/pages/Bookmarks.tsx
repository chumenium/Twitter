import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Post } from '../types/post';
import { postsApi } from '../api/posts';
import PostCard from '../components/PostCard';
import './Bookmarks.css';

const Bookmarks: React.FC = () => {
  const { user } = useAuth();
  const [bookmarks, setBookmarks] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    setLoading(true);
    try {
      const response = await postsApi.getBookmarks();
      setBookmarks(response.results);
    } catch (error) {
      console.error('ブックマークの取得に失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="bookmarks-page">
        <div className="bookmarks-header">
          <h1 className="bookmarks-title">ブックマーク</h1>
        </div>
        <div className="bookmarks-content">
          <p>ログインが必要です。</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bookmarks-page">
      <div className="bookmarks-header">
        <h1 className="bookmarks-title">ブックマーク</h1>
      </div>
      <div className="bookmarks-content">
        {loading ? (
          <div className="loading">
            <i className="fas fa-spinner fa-spin"></i> 読み込み中...
          </div>
        ) : bookmarks.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <i className="fas fa-bookmark"></i>
            </div>
            <h3>まだブックマークがありません</h3>
            <p>気になる投稿をブックマークしてみましょう！</p>
          </div>
        ) : (
          <div className="posts-list">
            {bookmarks.map(post => (
              <PostCard key={post.id} post={post} onUpdate={fetchBookmarks} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Bookmarks; 
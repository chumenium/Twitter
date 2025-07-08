import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Post } from '../types/post';
import { postsApi } from '../api/posts';
import PostCard from '../components/PostCard';
import './Mypage.css';

const Mypage: React.FC = () => {
  const { user, profile } = useAuth();
  const [posts, setPosts] = useState<Post[]>([]);
  const [likedPosts, setLikedPosts] = useState<Post[]>([]);
  const [activeTab, setActiveTab] = useState<'posts' | 'liked'>('posts');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      if (activeTab === 'posts') {
        const response = await postsApi.getPosts(1);
        setPosts(response.results);
      } else {
        const response = await postsApi.getPosts(1);
        setLikedPosts(response.results);
      }
    } catch (error) {
      console.error('投稿の取得に失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePostUpdate = () => {
    fetchPosts();
  };

  if (!user || !profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="mypage">
      <div className="mypage-header">
        <div className="profile-info">
          <div className="profile-avatar">
            {profile.image ? (
              <img src={`http://127.0.0.1:8001${profile.image}`} alt={profile.name} />
            ) : (
              <span>{user.username.charAt(0).toUpperCase()}</span>
            )}
          </div>
          <div className="profile-details">
            <h1 className="profile-name">{profile.name || user.username}</h1>
            <p className="profile-username">@{user.username}</p>
            {profile.bio && <p className="profile-bio">{profile.bio}</p>}
            {profile.location && (
              <p className="profile-location">
                <i className="fas fa-map-marker-alt"></i> {profile.location}
              </p>
            )}
            {profile.website && (
              <p className="profile-website">
                <i className="fas fa-link"></i> 
                <a href={profile.website} target="_blank" rel="noopener noreferrer">
                  {profile.website}
                </a>
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="mypage-tabs">
        <button
          className={`tab-btn ${activeTab === 'posts' ? 'active' : ''}`}
          onClick={() => setActiveTab('posts')}
        >
          <i className="fas fa-comment"></i> 投稿
        </button>
        <button
          className={`tab-btn ${activeTab === 'liked' ? 'active' : ''}`}
          onClick={() => setActiveTab('liked')}
        >
          <i className="fas fa-heart"></i> いいね
        </button>
      </div>

      <div className="mypage-content">
        {loading ? (
          <div className="loading">
            <i className="fas fa-spinner fa-spin"></i> 読み込み中...
          </div>
        ) : (
          <>
            {activeTab === 'posts' && (
              <>
                {posts.length === 0 ? (
                  <div className="empty-state">
                    <div className="empty-icon">
                      <i className="far fa-comment-dots"></i>
                    </div>
                    <h3>まだ投稿がありません</h3>
                    <p>最初の投稿を作成してみましょう！</p>
                  </div>
                ) : (
                  <div className="posts-list">
                    {posts.map(post => (
                      <PostCard
                        key={post.id}
                        post={post}
                        onUpdate={handlePostUpdate}
                      />
                    ))}
                  </div>
                )}
              </>
            )}

            {activeTab === 'liked' && (
              <>
                {likedPosts.length === 0 ? (
                  <div className="empty-state">
                    <div className="empty-icon">
                      <i className="far fa-heart"></i>
                    </div>
                    <h3>まだいいねした投稿がありません</h3>
                    <p>気になる投稿にいいねしてみましょう！</p>
                  </div>
                ) : (
                  <div className="posts-list">
                    {likedPosts.map(post => (
                      <PostCard
                        key={post.id}
                        post={post}
                        onUpdate={handlePostUpdate}
                      />
                    ))}
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Mypage; 
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Post } from '../types/post';
import { postsApi } from '../api/posts';
import PostCard from '../components/PostCard';
import CreatePost from '../components/CreatePost';
import './Home.css';

const Home: React.FC = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async (pageNum = 1) => {
    try {
      const response = await postsApi.getPosts(pageNum);
      if (pageNum === 1) {
        setPosts(response.results);
      } else {
        setPosts(prev => [...prev, ...response.results]);
      }
      setHasMore(response.next !== null);
      setPage(pageNum);
    } catch (error) {
      console.error('投稿の取得に失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePostCreate = async (content: string) => {
    try {
      const newPost = await postsApi.createPost({ content });
      setPosts(prev => [newPost, ...prev]);
    } catch (error) {
      console.error('投稿の作成に失敗しました:', error);
    }
  };

  const handlePostUpdate = () => {
    fetchPosts(1);
  };

  const handleLoadMore = () => {
    if (!loading && hasMore) {
      fetchPosts(page + 1);
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
    if (scrollHeight - scrollTop <= clientHeight * 1.5) {
      handleLoadMore();
    }
  };

  return (
    <div className="home-page">
      <div className="home-header">
        <h1 className="home-title">ホーム</h1>
      </div>

      <div className="home-content" onScroll={handleScroll}>
        {user && (
          <div className="create-post-section">
            <CreatePost onPostCreated={handlePostUpdate} />
          </div>
        )}

        <div className="posts-section">
          {loading && posts.length === 0 ? (
            <div className="loading">
              <i className="fas fa-spinner fa-spin"></i> 読み込み中...
            </div>
          ) : posts.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">
                <i className="far fa-comment-dots"></i>
              </div>
              <h3>まだ投稿がありません</h3>
              <p>最初の投稿を作成してみましょう！</p>
            </div>
          ) : (
            <>
              <div className="posts-list">
                {posts.map(post => (
                  <PostCard
                    key={post.id}
                    post={post}
                    onUpdate={handlePostUpdate}
                  />
                ))}
              </div>
              
              {loading && posts.length > 0 && (
                <div className="loading-more">
                  <i className="fas fa-spinner fa-spin"></i> 読み込み中...
                </div>
              )}
              
              {!hasMore && posts.length > 0 && (
                <div className="no-more-posts">
                  <p>これで全ての投稿です</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home; 
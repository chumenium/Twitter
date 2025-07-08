import React, { useState, useEffect } from 'react';
import { Post } from '../types/post';
import { postsApi } from '../api/posts';
import PostCard from './PostCard';
import CreatePost from './CreatePost';
import './Timeline.css';

const Timeline: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  const fetchPosts = async (pageNum: number = 1, append: boolean = false) => {
    try {
      setLoading(true);
      const response = await postsApi.getPosts(pageNum);
      
      if (append) {
        setPosts(prev => [...prev, ...response.results]);
      } else {
        setPosts(response.results);
      }
      
      setHasMore(!!response.next);
      setPage(pageNum);
    } catch (err) {
      setError('投稿の取得に失敗しました');
      console.error('投稿の取得エラー:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handlePostCreated = () => {
    // 新しい投稿が作成されたら、最初のページを再取得
    fetchPosts(1, false);
  };

  const handleLoadMore = () => {
    if (!loading && hasMore) {
      fetchPosts(page + 1, true);
    }
  };

  const handlePostUpdate = () => {
    // 投稿が更新されたら、現在のページを再取得
    fetchPosts(page, false);
  };

  if (error) {
    return (
      <div className="timeline-error">
        <div className="error-message">
          <i className="fas fa-exclamation-triangle"></i>
          <p>{error}</p>
          <button onClick={() => fetchPosts(1, false)}>再試行</button>
        </div>
      </div>
    );
  }

  return (
    <div className="timeline">
      <div className="timeline-header">
        <h1>ホーム</h1>
      </div>
      
      <CreatePost onPostCreated={handlePostCreated} />
      
      <div className="posts-container">
        {posts.length === 0 && !loading ? (
          <div className="empty-state">
            <div className="empty-icon">
              <i className="far fa-comment-dots"></i>
            </div>
            <h3>まだ投稿がありません</h3>
            <p>最初の投稿を作成してみましょう！</p>
          </div>
        ) : (
          <>
            {posts.map(post => (
              <PostCard
                key={post.id}
                post={post}
                onUpdate={handlePostUpdate}
              />
            ))}
            
            {hasMore && (
              <div className="load-more">
                <button
                  onClick={handleLoadMore}
                  disabled={loading}
                  className="load-more-btn"
                >
                  {loading ? (
                    <i className="fas fa-spinner fa-spin"></i>
                  ) : (
                    'さらに読み込む'
                  )}
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Timeline; 
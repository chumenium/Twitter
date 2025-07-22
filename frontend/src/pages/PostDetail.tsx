import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Post } from '../types/post';
import { Hashtag } from '../types/hashtag';
import { User } from '../types/auth';
import { postsApi } from '../api/posts';
import { hashtagsApi } from '../api/hashtags';
import { mentionsApi } from '../api/mentions';
import PostCard from '../components/PostCard';
import './PostDetail.css';

interface PostDetailData {
  post: Post;
  hashtags: Hashtag[];
  mentioned_users: User[];
  stats: {
    replies_count: number;
    retweets_count: number;
    likes_count: number;
    bookmarks_count: number;
  };
}

const PostDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [postDetail, setPostDetail] = useState<PostDetailData | null>(null);
  const [replies, setReplies] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPostDetail = async () => {
    try {
      setLoading(true);
      const response = await postsApi.getPostDetail(parseInt(id!));
      setPostDetail(response);
    } catch (err) {
      setError('投稿の取得に失敗しました');
      console.error('投稿詳細の取得エラー:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchReplies = async () => {
    try {
      const response = await postsApi.getPostReplies(parseInt(id!));
      setReplies(response.results || response);
    } catch (err) {
      console.error('返信の取得エラー:', err);
    }
  };

  useEffect(() => {
    if (id) {
      fetchPostDetail();
      fetchReplies();
    }
  }, [id]);

  const handlePostUpdate = () => {
    fetchPostDetail();
    fetchReplies();
  };

  const formatHashtag = (hashtag: string) => {
    return hashtag.startsWith('#') ? hashtag : `#${hashtag}`;
  };

  const formatMention = (username: string) => {
    return username.startsWith('@') ? username : `@${username}`;
  };

  if (loading) {
    return (
      <div className="post-detail-loading">
        <div className="loading-spinner">
          <i className="fas fa-spinner fa-spin"></i>
          <p>読み込み中...</p>
        </div>
      </div>
    );
  }

  if (error || !postDetail) {
    return (
      <div className="post-detail-error">
        <div className="error-message">
          <i className="fas fa-exclamation-triangle"></i>
          <p>{error || '投稿が見つかりません'}</p>
          <Link to="/" className="back-link">ホームに戻る</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="post-detail">
      <div className="post-detail-header">
        <Link to="/" className="back-button">
          <i className="fas fa-arrow-left"></i>
          <span>戻る</span>
        </Link>
        <h1>投稿</h1>
      </div>

      <div className="post-detail-content">
        {/* メイン投稿 */}
        <div className="main-post">
          <PostCard 
            post={postDetail.post} 
            onUpdate={handlePostUpdate}
          />
        </div>

        {/* 統計情報 */}
        <div className="post-stats">
          <div className="stat-item">
            <i className="fas fa-reply"></i>
            <span>{postDetail.stats.replies_count} 返信</span>
          </div>
          <div className="stat-item">
            <i className="fas fa-retweet"></i>
            <span>{postDetail.stats.retweets_count} リツイート</span>
          </div>
          <div className="stat-item">
            <i className="fas fa-heart"></i>
            <span>{postDetail.stats.likes_count} いいね</span>
          </div>
          <div className="stat-item">
            <i className="fas fa-bookmark"></i>
            <span>{postDetail.stats.bookmarks_count} ブックマーク</span>
          </div>
        </div>

        {/* ハッシュタグ */}
        {postDetail.hashtags.length > 0 && (
          <div className="post-hashtags">
            <h3>ハッシュタグ</h3>
            <div className="hashtags-list">
              {postDetail.hashtags.map(hashtag => (
                <Link
                  key={hashtag.id}
                  to={`/hashtag/${hashtag.name}`}
                  className="hashtag-link"
                >
                  {formatHashtag(hashtag.name)}
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* メンション */}
        {postDetail.mentioned_users.length > 0 && (
          <div className="post-mentions">
            <h3>メンション</h3>
            <div className="mentions-list">
              {postDetail.mentioned_users.map(user => (
                <Link
                  key={user.id}
                  to={`/profile/${user.username}`}
                  className="mention-link"
                >
                  {formatMention(user.username)}
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* 返信 */}
        <div className="post-replies">
          <h3>返信 ({postDetail.stats.replies_count})</h3>
          {replies.length === 0 ? (
            <div className="no-replies">
              <p>まだ返信がありません</p>
            </div>
          ) : (
            <div className="replies-list">
              {replies.map(reply => (
                <PostCard
                  key={reply.id}
                  post={reply}
                  onUpdate={handlePostUpdate}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PostDetail; 
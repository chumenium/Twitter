import React, { useState } from 'react';
import { toggleFollow } from '../api/follow';
import '../styles/components/FollowButton.css';

interface FollowButtonProps {
  userId: number;
  isFollowing: boolean;
  onChange?: (following: boolean) => void;
  className?: string;
}

const FollowButton: React.FC<FollowButtonProps> = ({ 
  userId, 
  isFollowing, 
  onChange,
  className = ''
}) => {
  const [loading, setLoading] = useState(false);
  const [following, setFollowing] = useState(isFollowing);

  const handleClick = async () => {
    if (loading) return;
    
    setLoading(true);
    try {
      const response = await toggleFollow(userId);
      setFollowing(response.following);
      onChange?.(response.following);
    } catch (error) {
      console.error('フォロー操作に失敗しました:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      className={`follow-button ${following ? 'following' : loading ? 'loading' : ''} ${className}`}
      onClick={handleClick}
      disabled={loading}
    >
      {loading ? (
        <span className="loading-spinner"></span>
      ) : following ? (
        'フォロー中'
      ) : (
        'フォロー'
      )}
    </button>
  );
};

export default FollowButton; 
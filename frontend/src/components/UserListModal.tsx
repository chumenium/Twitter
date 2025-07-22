import React from 'react';
import { Follow } from '../types/follow';
import FollowButton from './FollowButton';
import '../styles/components/UserListModal.css';

interface UserListModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  users: Follow[];
  type: 'followers' | 'following';
  currentUserId: number;
}

const UserListModal: React.FC<UserListModalProps> = ({
  open,
  onClose,
  title,
  users,
  type,
  currentUserId,
}) => {
  if (!open) return null;

  const handleUserClick = (userId: number) => {
    // ユーザープロフィールページへの遷移（実装予定）
    console.log('ユーザープロフィールへ遷移:', userId);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          {users.length === 0 ? (
            <p className="no-users">まだ{type === 'followers' ? 'フォロワー' : 'フォロー'}がいません</p>
          ) : (
            <ul className="user-list">
              {users.map(follow => {
                const user = type === 'followers' ? follow.follower : follow.following;
                const isCurrentUser = user.id === currentUserId;
                return (
                  <li key={follow.id} className="user-item">
                    <div
                      className="user-info"
                      onClick={() => handleUserClick(user.id)}
                    >
                      <div className="user-avatar">
                        <img
                          src={'/default-avatar.png'}
                          alt={user.username}
                          onError={e => {
                            (e.currentTarget as HTMLImageElement).src = '/default-avatar.png';
                          }}
                        />
                      </div>
                      <div className="user-details">
                        <span className="username">{user.username}</span>
                      </div>
                    </div>
                    {!isCurrentUser && (
                      <FollowButton
                        userId={user.id}
                        isFollowing={type === 'following'}
                        className="modal-follow-button"
                      />
                    )}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserListModal; 
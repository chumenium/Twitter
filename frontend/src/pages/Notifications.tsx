import React, { useState, useEffect } from 'react';
import { Notification } from '../types/notification';
import { notificationsApi } from '../api/notifications';
import './Notifications.css';

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const [unreadCount, setUnreadCount] = useState(0);

  const fetchNotifications = async (pageNum: number = 1, append: boolean = false) => {
    try {
      setLoading(true);
      const response = await notificationsApi.getNotifications(pageNum);
      
      if (append) {
        setNotifications(prev => [...prev, ...response.notifications]);
      } else {
        setNotifications(response.notifications);
      }
      
      setUnreadCount(response.unread_count);
      setHasMore(!!response.has_next);
      setPage(pageNum);
    } catch (err) {
      setError('通知の取得に失敗しました');
      console.error('通知の取得エラー:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleLoadMore = () => {
    if (!loading && hasMore) {
      fetchNotifications(page + 1, true);
    }
  };

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationsApi.markAsRead(notificationId);
      setNotifications(prev =>
        prev.map(notification =>
          notification.id === notificationId
            ? { ...notification, is_read: true }
            : notification
        )
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (err) {
      console.error('通知の既読化に失敗しました:', err);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsApi.markAllAsRead();
      setNotifications(prev =>
        prev.map(notification => ({ ...notification, is_read: true }))
      );
      setUnreadCount(0);
    } catch (err) {
      console.error('すべての通知の既読化に失敗しました:', err);
    }
  };

  const handleDeleteNotification = async (notificationId: number) => {
    try {
      await notificationsApi.deleteNotification(notificationId);
      setNotifications(prev =>
        prev.filter(notification => notification.id !== notificationId)
      );
    } catch (err) {
      console.error('通知の削除に失敗しました:', err);
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'like':
        return 'fas fa-heart';
      case 'retweet':
        return 'fas fa-retweet';
      case 'follow':
        return 'fas fa-user-plus';
      case 'reply':
        return 'fas fa-reply';
      case 'mention':
        return 'fas fa-at';
      default:
        return 'fas fa-bell';
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'like':
        return '#f91880';
      case 'retweet':
        return '#00ba7c';
      case 'follow':
        return '#1d9bf0';
      case 'reply':
        return '#1d9bf0';
      case 'mention':
        return '#ff7a00';
      default:
        return '#1d9bf0';
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

  if (error) {
    return (
      <div className="notifications-error">
        <div className="error-message">
          <i className="fas fa-exclamation-triangle"></i>
          <p>{error}</p>
          <button onClick={() => fetchNotifications(1, false)}>再試行</button>
        </div>
      </div>
    );
  }

  return (
    <div className="notifications">
      <div className="notifications-header">
        <h1>通知</h1>
        {unreadCount > 0 && (
          <button
            className="mark-all-read-btn"
            onClick={handleMarkAllAsRead}
          >
            すべて既読にする
          </button>
        )}
      </div>
      
      <div className="notifications-container">
        {notifications.length === 0 && !loading ? (
          <div className="empty-state">
            <div className="empty-icon">
              <i className="far fa-bell"></i>
            </div>
            <h3>通知はありません</h3>
            <p>新しいアクティビティがあるとここに表示されます</p>
          </div>
        ) : (
          <>
            {notifications.map(notification => (
              <div
                key={notification.id}
                className={`notification-item ${!notification.is_read ? 'unread' : ''}`}
                onClick={() => !notification.is_read && handleMarkAsRead(notification.id)}
              >
                <div className="notification-icon">
                  <i
                    className={getNotificationIcon(notification.notification_type)}
                    style={{ color: getNotificationColor(notification.notification_type) }}
                  ></i>
                </div>
                
                <div className="notification-content">
                  <div className="notification-user">
                    <span className="user-name">{notification.sender.display_name}</span>
                    <span className="user-handle">@{notification.sender.username}</span>
                  </div>
                  
                  <div className="notification-text">
                    {notification.notification_type_display}しました
                  </div>
                  
                  {notification.post && (
                    <div className="notification-post">
                      {notification.post.content}
                    </div>
                  )}
                  
                  <div className="notification-time">
                    {formatDate(notification.created_at)}
                  </div>
                </div>
                
                <button
                  className="delete-notification-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteNotification(notification.id);
                  }}
                  title="削除"
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
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

export default Notifications; 
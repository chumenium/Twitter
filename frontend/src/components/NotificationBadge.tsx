import React, { useState, useEffect } from 'react';
import { notificationsApi } from '../api/notifications';
import './NotificationBadge.css';

interface NotificationBadgeProps {
  className?: string;
}

const NotificationBadge: React.FC<NotificationBadgeProps> = ({ className = '' }) => {
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchNotificationCount = async () => {
    try {
      const response = await notificationsApi.getNotificationCount();
      setUnreadCount(response.unread_count);
    } catch (err) {
      console.error('通知数の取得に失敗しました:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotificationCount();
    
    // 定期的に通知数を更新（30秒間隔）
    const interval = setInterval(fetchNotificationCount, 30000);
    
    return () => clearInterval(interval);
  }, []);

  // 通知数が0の場合はバッジを表示しない
  if (unreadCount === 0 || loading) {
    return null;
  }

  return (
    <div className={`notification-badge ${className}`}>
      <span className="badge-count">
        {unreadCount > 99 ? '99+' : unreadCount}
      </span>
    </div>
  );
};

export default NotificationBadge; 
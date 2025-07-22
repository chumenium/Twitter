import { User } from './auth';
import { Post } from './post';

export interface Notification {
  id: number;
  sender: User;
  notification_type: 'like' | 'retweet' | 'follow' | 'reply' | 'mention';
  notification_type_display: string;
  post?: Post;
  is_read: boolean;
  created_at: string;
}

export interface NotificationResponse {
  notifications: Notification[];
  count: number;
  unread_count: number;
  has_next?: boolean;
  has_previous?: boolean;
}

export interface NotificationCountResponse {
  unread_count: number;
} 
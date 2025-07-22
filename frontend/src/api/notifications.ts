import apiClient from './client';
import { Notification, NotificationResponse, NotificationCountResponse } from '../types/notification';

export const notificationsApi = {
  // 通知一覧を取得
  getNotifications: async (page: number = 1): Promise<NotificationResponse> => {
    const response = await apiClient.get(`/api/notifications/?page=${page}`);
    return response.data as NotificationResponse;
  },

  // 未読通知を取得
  getUnreadNotifications: async (): Promise<NotificationResponse> => {
    const response = await apiClient.get('/api/notifications/unread/');
    return response.data as NotificationResponse;
  },

  // 未読通知数を取得
  getNotificationCount: async (): Promise<NotificationCountResponse> => {
    const response = await apiClient.get('/api/notifications/count/');
    return response.data as NotificationCountResponse;
  },

  // 通知を既読にする
  markAsRead: async (notificationId: number): Promise<{ message: string; notification: Notification }> => {
    const response = await apiClient.post(`/api/notifications/${notificationId}/read/`);
    return response.data as { message: string; notification: Notification };
  },

  // すべての通知を既読にする
  markAllAsRead: async (): Promise<{ message: string; updated_count: number }> => {
    const response = await apiClient.post('/api/notifications/read-all/');
    return response.data as { message: string; updated_count: number };
  },

  // 通知を削除
  deleteNotification: async (notificationId: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/api/notifications/${notificationId}/delete/`);
    return response.data as { message: string };
  },

  // すべての通知を削除
  deleteAllNotifications: async (): Promise<{ message: string; deleted_count: number }> => {
    const response = await apiClient.delete('/api/notifications/delete-all/');
    return response.data as { message: string; deleted_count: number };
  },
}; 
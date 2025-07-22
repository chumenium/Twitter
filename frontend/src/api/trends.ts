import apiClient from './client';
import { TrendResponse, TrendByTypeResponse } from '../types/trend';

export const trendsApi = {
  // すべてのトレンドを取得
  getAllTrends: async (limit: number = 30): Promise<TrendResponse> => {
    const response = await apiClient.get(`/api/trends/?limit=${limit}`);
    return response.data as TrendResponse;
  },

  // トレンドのハッシュタグを取得
  getTrendingHashtags: async (limit: number = 10): Promise<TrendResponse> => {
    const response = await apiClient.get(`/api/trends/hashtags/?limit=${limit}`);
    return response.data as TrendResponse;
  },

  // トレンドの投稿を取得
  getTrendingPosts: async (limit: number = 10): Promise<TrendResponse> => {
    const response = await apiClient.get(`/api/trends/posts/?limit=${limit}`);
    return response.data as TrendResponse;
  },

  // トレンドのユーザーを取得
  getTrendingUsers: async (limit: number = 10): Promise<TrendResponse> => {
    const response = await apiClient.get(`/api/trends/users/?limit=${limit}`);
    return response.data as TrendResponse;
  },

  // 特定のタイプのトレンドを取得
  getTrendsByType: async (trendType: 'hashtag' | 'post' | 'user', limit: number = 10): Promise<TrendByTypeResponse> => {
    const response = await apiClient.get(`/api/trends/${trendType}/?limit=${limit}`);
    return response.data as TrendByTypeResponse;
  },

  // トレンドを手動更新（管理者用）
  updateTrends: async (): Promise<{ message: string }> => {
    const response = await apiClient.post('/api/trends/update/');
    return response.data as { message: string };
  },
}; 
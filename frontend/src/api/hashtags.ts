import apiClient from './client';
import { HashtagResponse, HashtagPostsResponse, HashtagInfoResponse } from '../types/hashtag';

export const hashtagsApi = {
  // トレンドのハッシュタグを取得
  getTrendingHashtags: async (limit: number = 10): Promise<HashtagResponse> => {
    const response = await apiClient.get(`/api/hashtags/trending/?limit=${limit}`);
    return response.data as HashtagResponse;
  },

  // ハッシュタグを検索
  searchHashtags: async (query: string, limit: number = 20): Promise<HashtagResponse> => {
    const response = await apiClient.get(`/api/hashtags/search/?q=${query}&limit=${limit}`);
    return response.data as HashtagResponse;
  },

  // 特定のハッシュタグを含む投稿を取得
  getHashtagPosts: async (hashtagName: string, page: number = 1, limit: number = 50): Promise<HashtagPostsResponse> => {
    const response = await apiClient.get(`/api/hashtags/${hashtagName}/posts/?page=${page}&limit=${limit}`);
    return response.data as HashtagPostsResponse;
  },

  // ハッシュタグの詳細情報を取得
  getHashtagInfo: async (hashtagName: string): Promise<HashtagInfoResponse> => {
    const response = await apiClient.get(`/api/hashtags/${hashtagName}/info/`);
    return response.data as HashtagInfoResponse;
  },

  // すべてのハッシュタグを取得
  getAllHashtags: async (page: number = 1): Promise<HashtagResponse> => {
    const response = await apiClient.get(`/api/hashtags/?page=${page}`);
    return response.data as HashtagResponse;
  },
}; 
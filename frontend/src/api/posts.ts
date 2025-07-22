import apiClient from './client';
import { Post, CreatePostData, ApiResponse } from '../types/post';

export const postsApi = {
  // 投稿一覧を取得
  getPosts: async (page: number = 1): Promise<ApiResponse<Post>> => {
    const response = await apiClient.get(`/api/posts/?page=${page}`);
    return response.data as ApiResponse<Post>;
  },

  // すべての投稿を取得
  getAllPosts: async (page: number = 1): Promise<ApiResponse<Post>> => {
    const response = await apiClient.get(`/api/posts/all_posts/?page=${page}`);
    return response.data as ApiResponse<Post>;
  },

  // フォロー中の投稿を取得
  getTimeline: async (page: number = 1): Promise<ApiResponse<Post>> => {
    const response = await apiClient.get(`/api/posts/timeline/?page=${page}`);
    return response.data as ApiResponse<Post>;
  },

  // 投稿を作成
  createPost: async (data: CreatePostData): Promise<Post> => {
    const formData = new FormData();
    formData.append('content', data.content);
    
    if (data.image) {
      formData.append('image', data.image);
    }

    const response = await apiClient.post('/api/posts/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data as Post;
  },

  // いいねを切り替え
  toggleLike: async (postId: number): Promise<{ liked: boolean; likes_count: number }> => {
    const response = await apiClient.post(`/api/posts/${postId}/toggle_like/`);
    return response.data as { liked: boolean; likes_count: number };
  },

  // ブックマークを切り替え
  toggleBookmark: async (postId: number): Promise<{ bookmarked: boolean }> => {
    const response = await apiClient.post(`/api/posts/${postId}/toggle_bookmark/`);
    return response.data as { bookmarked: boolean };
  },

  // リツイートを切り替え
  toggleRetweet: async (postId: number): Promise<{ retweeted: boolean; retweets_count: number }> => {
    const response = await apiClient.post(`/api/posts/${postId}/toggle_retweet/`);
    return response.data as { retweeted: boolean; retweets_count: number };
  },

  getBookmarks: async (): Promise<ApiResponse<Post>> => {
    const response = await apiClient.get('/api/bookmarks/');
    return response.data as ApiResponse<Post>;
  },

  // 投稿を削除
  deletePost: async (postId: number): Promise<void> => {
    await apiClient.delete(`/api/posts/${postId}/`);
  },

  // 投稿の返信を取得
  getPostReplies: async (postId: number): Promise<ApiResponse<Post>> => {
    const response = await apiClient.get(`/api/posts/${postId}/replies/`);
    return response.data as ApiResponse<Post>;
  },

  // 投稿の詳細情報を取得
  getPostDetail: async (postId: number): Promise<any> => {
    const response = await apiClient.get(`/api/posts/${postId}/detail/`);
    return response.data;
  },
}; 
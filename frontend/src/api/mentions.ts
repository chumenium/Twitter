import apiClient from './client';
import { User } from '../types/auth';
import { Post } from '../types/post';

export interface MentionResponse {
  users: User[];
  count: number;
}

export interface MentionsForUserResponse {
  posts: Post[];
  count: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface MentionsInPostResponse {
  mentioned_users: User[];
  count: number;
}

export interface UserMentionsResponse {
  posts: Post[];
  user: User;
  count: number;
  has_next: boolean;
  has_previous: boolean;
}

export const mentionsApi = {
  // メンション用のユーザー検索
  searchUsersForMention: async (query: string, limit: number = 10): Promise<MentionResponse> => {
    const response = await apiClient.get(`/api/mentions/search-users/?q=${query}&limit=${limit}`);
    return response.data as MentionResponse;
  },

  // 現在のユーザーをメンションしている投稿を取得
  getMentionsForUser: async (page: number = 1, limit: number = 50): Promise<MentionsForUserResponse> => {
    const response = await apiClient.get(`/api/mentions/my-mentions/?page=${page}&limit=${limit}`);
    return response.data as MentionsForUserResponse;
  },

  // 特定の投稿でメンションされたユーザーを取得
  getMentionsInPost: async (postId: number): Promise<MentionsInPostResponse> => {
    const response = await apiClient.get(`/api/mentions/post/${postId}/`);
    return response.data as MentionsInPostResponse;
  },

  // 特定のユーザーをメンションしている投稿を取得
  getUserMentions: async (userId: number, page: number = 1, limit: number = 50): Promise<UserMentionsResponse> => {
    const response = await apiClient.get(`/api/mentions/user/${userId}/?page=${page}&limit=${limit}`);
    return response.data as UserMentionsResponse;
  },
}; 
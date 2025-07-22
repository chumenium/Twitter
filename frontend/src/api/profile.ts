import apiClient from './client';
import { UserProfile, UserPostsResponse, UserFollowersResponse, UserFollowingResponse } from '../types/profile';

export const profileApi = {
  // ユーザーのプロフィール詳細を取得
  getUserProfile: async (username: string): Promise<UserProfile> => {
    const response = await apiClient.get(`/api/profile/${username}/`);
    return response.data as UserProfile;
  },

  // ユーザーの投稿一覧を取得
  getUserPosts: async (username: string, page: number = 1): Promise<UserPostsResponse> => {
    const response = await apiClient.get(`/api/profile/${username}/posts/?page=${page}`);
    return response.data as UserPostsResponse;
  },

  // ユーザーがいいねした投稿一覧を取得
  getUserLikedPosts: async (username: string, page: number = 1): Promise<UserPostsResponse> => {
    const response = await apiClient.get(`/api/profile/${username}/liked-posts/?page=${page}`);
    return response.data as UserPostsResponse;
  },

  // ユーザーがリツイートした投稿一覧を取得
  getUserRetweets: async (username: string, page: number = 1): Promise<UserPostsResponse> => {
    const response = await apiClient.get(`/api/profile/${username}/retweets/?page=${page}`);
    return response.data as UserPostsResponse;
  },

  // ユーザーのフォロワー一覧を取得
  getUserFollowers: async (username: string, page: number = 1): Promise<UserFollowersResponse> => {
    const response = await apiClient.get(`/api/profile/${username}/followers/?page=${page}`);
    return response.data as UserFollowersResponse;
  },

  // ユーザーがフォローしているユーザー一覧を取得
  getUserFollowing: async (username: string, page: number = 1): Promise<UserFollowingResponse> => {
    const response = await apiClient.get(`/api/profile/${username}/following/?page=${page}`);
    return response.data as UserFollowingResponse;
  },
}; 
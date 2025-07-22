import axios from 'axios';
import { Follow, FollowResponse } from '../types/follow';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const toggleFollow = async (userId: number): Promise<FollowResponse> => {
  const response = await axios.post<FollowResponse>(
    `${API_BASE_URL}/api/follows/toggle_follow/`,
    { user_id: userId },
    { withCredentials: true }
  );
  return response.data;
};

export const fetchFollowers = async (userId?: number): Promise<Follow[]> => {
  const url = userId
    ? `${API_BASE_URL}/api/follows/user_followers/?user_id=${userId}`
    : `${API_BASE_URL}/api/follows/followers/`;
  const response = await axios.get<Follow[]>(url, { withCredentials: true });
  return response.data;
};

export const fetchFollowing = async (userId?: number): Promise<Follow[]> => {
  const url = userId
    ? `${API_BASE_URL}/api/follows/user_following/?user_id=${userId}`
    : `${API_BASE_URL}/api/follows/following/`;
  const response = await axios.get<Follow[]>(url, { withCredentials: true });
  return response.data;
}; 
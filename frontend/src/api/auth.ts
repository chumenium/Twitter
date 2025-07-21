import apiClient from './client';
import { LoginData, RegisterData, AuthResponse, CurrentUserResponse, ProfileUpdateData } from '../types/auth';

export const authApi = {
  // ユーザー登録
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/register/', data);
    return response.data as AuthResponse;
  },

  // ユーザーログイン
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/login/', data);
    return response.data as AuthResponse;
  },

  // ユーザーログアウト
  logout: async (): Promise<{ message: string }> => {
    const response = await apiClient.post('/api/auth/logout/');
    return response.data as { message: string };
  },

  // 現在のユーザー情報を取得
  getCurrentUser: async (): Promise<CurrentUserResponse> => {
    const response = await apiClient.get('/api/auth/user/');
    return response.data as CurrentUserResponse;
  },

  // プロフィール更新
  updateProfile: async (data: ProfileUpdateData): Promise<{ message: string; profile: any }> => {
    const formData = new FormData();
    
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    const response = await apiClient.put('/api/auth/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data as { message: string; profile: any };
  },

  // ユーザー情報更新
  updateUser: async (data: { username?: string; first_name?: string; last_name?: string; email?: string }): Promise<{ message: string; user: any }> => {
    const response = await apiClient.put('/api/auth/user/update/', data);
    return response.data as { message: string; user: any };
  },
}; 
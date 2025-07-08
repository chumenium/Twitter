import apiClient from './client';

export interface Profile {
  id: number;
  user: number;
  name: string;
  bio: string;
  location: string;
  website: string;
  image: string;
  created_at: string;
  updated_at: string;
}

export const profileApi = {
  getProfile: async (): Promise<Profile> => {
    const response = await apiClient.get('/api/profile/');
    return response.data as Profile;
  },

  updateProfile: async (formData: FormData): Promise<Profile> => {
    const response = await apiClient.patch('/api/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data as Profile;
  },
}; 
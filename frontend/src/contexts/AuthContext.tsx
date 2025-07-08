import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, Profile } from '../types/auth';
import { authApi } from '../api/auth';

interface AuthContextType {
  user: User | null;
  profile: Profile | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, passwordConfirm: string) => Promise<void>;
  logout: () => Promise<void>;
  updateProfile: (data: any) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await authApi.getCurrentUser();
      setUser(response.user);
      setProfile(response.profile);
    } catch (error) {
      console.log('認証されていません');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const response = await authApi.login({ username, password });
      setUser(response.user);
      // プロフィール情報も取得
      const userResponse = await authApi.getCurrentUser();
      setProfile(userResponse.profile);
    } catch (error) {
      throw error;
    }
  };

  const register = async (username: string, email: string, password: string, passwordConfirm: string) => {
    try {
      const response = await authApi.register({ username, email, password, password_confirm: passwordConfirm });
      setUser(response.user);
      // プロフィール情報も取得
      const userResponse = await authApi.getCurrentUser();
      setProfile(userResponse.profile);
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
      setUser(null);
      setProfile(null);
    } catch (error) {
      console.error('ログアウトエラー:', error);
    }
  };

  const updateProfile = async (data?: any) => {
    try {
      if (data) {
        const response = await authApi.updateProfile(data);
        setProfile(response.profile);
      } else {
        // 引数なしの場合は現在のユーザー情報を再取得
        const userResponse = await authApi.getCurrentUser();
        setProfile(userResponse.profile);
      }
    } catch (error) {
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    profile,
    loading,
    login,
    register,
    logout,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 
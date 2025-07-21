export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  profile?: Profile;
}

export interface Profile {
  id: number;
  user: User;
  name: string;
  bio: string;
  image?: string;
  location: string;
  website: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}

export interface CurrentUserResponse {
  user: User;
  profile: Profile;
}

export interface ProfileUpdateData {
  name?: string;
  bio?: string;
  image?: File;
  location?: string;
  website?: string;
} 
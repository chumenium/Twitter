export interface Profile {
  name: string;
  image?: string;
  bio: string;
}

export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  profile: Profile;
  display_name: string;
}

export interface Post {
  id: number;
  user: User;
  content: string;
  image?: string;
  created_at: string;
  likes_count: number;
  is_liked: boolean;
  is_bookmarked: boolean;
}

export interface CreatePostData {
  content: string;
  image?: File;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
} 
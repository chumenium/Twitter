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
  reply_to?: number;
  created_at: string;
  likes_count: number;
  is_liked: boolean;
  is_bookmarked: boolean;
  retweets_count: number;
  is_retweeted: boolean;
  replies_count: number;
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
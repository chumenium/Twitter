import { User } from './auth';

export interface ProfileStats {
  posts_count: number;
  followers_count: number;
  following_count: number;
}

export interface UserProfile {
  user: User;
  profile: any;
  stats: ProfileStats;
  is_following: boolean;
}

export interface UserPostsResponse {
  posts: any[];
  user: User;
  count: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface UserFollowersResponse {
  followers: User[];
  user: User;
  count: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface UserFollowingResponse {
  following: User[];
  user: User;
  count: number;
  has_next: boolean;
  has_previous: boolean;
} 
import { User } from './auth';

export interface Follow {
  id: number;
  follower: User;
  following: User;
  created_at: string;
}

export interface FollowResponse {
  following: boolean;
}

export interface FollowToggleData {
  user_id: number;
} 
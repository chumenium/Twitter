import { Hashtag } from './hashtag';
import { Post } from './post';
import { User } from './auth';

export interface Trend {
  id: number;
  trend_type: 'hashtag' | 'post' | 'user';
  trend_type_display: string;
  hashtag?: Hashtag;
  post?: Post;
  user?: User;
  score: number;
  created_at: string;
  updated_at: string;
}

export interface TrendResponse {
  trends: Trend[];
  count: number;
}

export interface TrendByTypeResponse {
  trends: Trend[];
  trend_type: string;
  count: number;
} 
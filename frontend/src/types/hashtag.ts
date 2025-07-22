export interface Hashtag {
  id: number;
  name: string;
  posts_count: number;
  created_at: string;
}

export interface HashtagResponse {
  hashtags: Hashtag[];
  count: number;
}

export interface HashtagPostsResponse {
  posts: any[];
  hashtag: string;
  count: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface HashtagInfoResponse {
  hashtag: Hashtag;
} 
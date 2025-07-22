# type: ignore
import re
from typing import List, Set
from .models import Post, Hashtag, PostHashtag
from django.db import models


def extract_hashtags(content: str) -> List[str]:
    """
    投稿内容からハッシュタグを抽出
    
    Args:
        content: 投稿内容
        
    Returns:
        ハッシュタグのリスト（#を含まない）
    """
    # ハッシュタグのパターン（#で始まり、英数字とアンダースコアを含む）
    hashtag_pattern = r'#([a-zA-Z0-9_]+)'
    hashtags = re.findall(hashtag_pattern, content)
    
    # 重複を除去して小文字に統一
    unique_hashtags = list(set([tag.lower() for tag in hashtags]))
    
    return unique_hashtags


def process_post_hashtags(post: Post) -> None:
    """
    投稿のハッシュタグを処理
    
    Args:
        post: 投稿オブジェクト
    """
    # 既存のハッシュタグ関連を削除
    PostHashtag.objects.filter(post=post).delete()
    
    # 新しいハッシュタグを抽出
    hashtags = extract_hashtags(post.content)
    
    for hashtag_name in hashtags:
        # ハッシュタグを作成または取得
        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
        
        # 投稿とハッシュタグを関連付け
        PostHashtag.objects.create(post=post, hashtag=hashtag)


def get_trending_hashtags(limit: int = 10) -> List[Hashtag]:
    """
    トレンドのハッシュタグを取得
    
    Args:
        limit: 取得件数
        
    Returns:
        トレンドハッシュタグのリスト
    """
    return Hashtag.objects.annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count', '-created_at')[:limit]


def search_hashtags(query: str, limit: int = 20) -> List[Hashtag]:
    """
    ハッシュタグを検索
    
    Args:
        query: 検索クエリ
        limit: 取得件数
        
    Returns:
        検索結果のハッシュタグリスト
    """
    return Hashtag.objects.filter(
        name__icontains=query
    ).annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count', '-created_at')[:limit]


def get_posts_by_hashtag(hashtag_name: str, limit: int = 50) -> List[Post]:
    """
    特定のハッシュタグを含む投稿を取得
    
    Args:
        hashtag_name: ハッシュタグ名（#を含まない）
        limit: 取得件数
        
    Returns:
        投稿のリスト
    """
    try:
        hashtag = Hashtag.objects.get(name=hashtag_name.lower())
        return hashtag.posts.order_by('-created_at')[:limit]
    except Hashtag.DoesNotExist:
        return [] 
# type: ignore
import re
from typing import List, Set
from django.contrib.auth.models import User
from .models import Post
from .notification_utils import create_mention_notification


def extract_mentions(content: str) -> List[str]:
    """
    投稿内容からメンションを抽出
    
    Args:
        content: 投稿内容
        
    Returns:
        メンションされたユーザー名のリスト（@を含まない）
    """
    # メンションのパターン（@で始まり、英数字とアンダースコアを含む）
    mention_pattern = r'@([a-zA-Z0-9_]+)'
    mentions = re.findall(mention_pattern, content)
    
    # 重複を除去
    unique_mentions = list(set(mentions))
    
    return unique_mentions


def process_post_mentions(post: Post) -> None:
    """
    投稿のメンションを処理
    
    Args:
        post: 投稿オブジェクト
    """
    mentions = extract_mentions(post.content)
    
    for username in mentions:
        try:
            mentioned_user = User.objects.get(username=username)
            # 自分自身へのメンションは通知しない
            if mentioned_user != post.user:
                create_mention_notification(post.user, mentioned_user, post)
        except User.DoesNotExist:
            # 存在しないユーザー名は無視
            pass


def get_mentioned_users_in_post(post: Post) -> List[User]:
    """
    投稿でメンションされたユーザーを取得
    
    Args:
        post: 投稿オブジェクト
        
    Returns:
        メンションされたユーザーのリスト
    """
    mentions = extract_mentions(post.content)
    users = []
    
    for username in mentions:
        try:
            user = User.objects.get(username=username)
            users.append(user)
        except User.DoesNotExist:
            pass
    
    return users


def search_users_by_username(query: str, limit: int = 10) -> List[User]:
    """
    ユーザー名でユーザーを検索（メンション用）
    
    Args:
        query: 検索クエリ
        limit: 取得件数
        
    Returns:
        検索結果のユーザーリスト
    """
    return User.objects.filter(
        username__icontains=query
    ).order_by('username')[:limit]


def get_posts_mentioning_user(user: User, limit: int = 50) -> List[Post]:
    """
    特定のユーザーをメンションしている投稿を取得
    
    Args:
        user: ユーザーオブジェクト
        limit: 取得件数
        
    Returns:
        投稿のリスト
    """
    return Post.objects.filter(
        content__icontains=f'@{user.username}'
    ).order_by('-created_at')[:limit] 
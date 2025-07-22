# type: ignore
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.utils import timezone
from .models import Hashtag, Post, User, Trend


def calculate_hashtag_trend_score(hashtag: Hashtag) -> float:
    """
    ハッシュタグのトレンドスコアを計算
    
    Args:
        hashtag: ハッシュタグオブジェクト
        
    Returns:
        トレンドスコア
    """
    # 過去24時間の投稿数を取得
    yesterday = timezone.now() - timedelta(days=1)
    recent_posts = hashtag.posts.filter(created_at__gte=yesterday).count()
    
    # 過去7日間の投稿数を取得
    week_ago = timezone.now() - timedelta(days=7)
    weekly_posts = hashtag.posts.filter(created_at__gte=week_ago).count()
    
    # スコア計算（最近の投稿により重みを置く）
    score = (recent_posts * 3) + (weekly_posts * 1)
    
    return score


def calculate_post_trend_score(post: Post) -> float:
    """
    投稿のトレンドスコアを計算
    
    Args:
        post: 投稿オブジェクト
        
    Returns:
        トレンドスコア
    """
    # 投稿からの経過時間（時間）
    hours_since_creation = (timezone.now() - post.created_at).total_seconds() / 3600
    
    # いいね数、リツイート数、返信数を取得
    likes_count = post.likes.count()
    retweets_count = post.retweets.count()
    replies_count = post.replies.count()
    
    # スコア計算（時間経過とエンゲージメントを考慮）
    engagement_score = (likes_count * 1) + (retweets_count * 2) + (replies_count * 3)
    time_decay = max(1, hours_since_creation)  # 時間経過による減衰
    
    score = engagement_score / time_decay
    
    return score


def calculate_user_trend_score(user: User) -> float:
    """
    ユーザーのトレンドスコアを計算
    
    Args:
        user: ユーザーオブジェクト
        
    Returns:
        トレンドスコア
    """
    # 過去24時間のフォロワー増加数
    yesterday = timezone.now() - timedelta(days=1)
    recent_followers = user.followers.filter(created_at__gte=yesterday).count()
    
    # 過去24時間の投稿数
    recent_posts = user.post_set.filter(created_at__gte=yesterday).count()
    
    # 過去24時間の総いいね数
    recent_likes = sum(post.likes.count() for post in user.post_set.filter(created_at__gte=yesterday))
    
    # スコア計算
    score = (recent_followers * 5) + (recent_posts * 2) + (recent_likes * 1)
    
    return score


def update_trends():
    """
    トレンドを更新
    """
    # 既存のトレンドを削除
    Trend.objects.all().delete()
    
    # ハッシュタグトレンドを更新
    hashtags = Hashtag.objects.all()
    for hashtag in hashtags:
        score = calculate_hashtag_trend_score(hashtag)
        if score > 0:
            Trend.objects.create(
                trend_type='hashtag',
                hashtag=hashtag,
                score=score
            )
    
    # 投稿トレンドを更新（過去24時間の投稿のみ）
    yesterday = timezone.now() - timedelta(days=1)
    recent_posts = Post.objects.filter(created_at__gte=yesterday)
    for post in recent_posts:
        score = calculate_post_trend_score(post)
        if score > 1:  # 最低スコア以上の投稿のみ
            Trend.objects.create(
                trend_type='post',
                post=post,
                score=score
            )
    
    # ユーザートレンドを更新
    users = User.objects.all()
    for user in users:
        score = calculate_user_trend_score(user)
        if score > 0:
            Trend.objects.create(
                trend_type='user',
                user=user,
                score=score
            )


def get_trending_hashtags(limit: int = 10):
    """トレンドのハッシュタグを取得"""
    return Trend.objects.filter(trend_type='hashtag').order_by('-score')[:limit]


def get_trending_posts(limit: int = 10):
    """トレンドの投稿を取得"""
    return Trend.objects.filter(trend_type='post').order_by('-score')[:limit]


def get_trending_users(limit: int = 10):
    """トレンドのユーザーを取得"""
    return Trend.objects.filter(trend_type='user').order_by('-score')[:limit]


def get_all_trends(limit: int = 30):
    """すべてのトレンドを取得"""
    return Trend.objects.all().order_by('-score')[:limit] 
# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from typing import Union
from django.contrib.auth.models import User
from .models import Post
from .serializers import UserSerializer, PostSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_posts(request):
    """投稿を検索"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'posts': [], 'count': 0})
    
    q1: Q = Q(content__icontains=query)
    q2: Q = Q(user__username__icontains=query)
    q3: Q = Q(user__profile__name__icontains=query)
    posts = Post.objects.filter(q1 | q2 | q3).order_by('-created_at')  # type: ignore
    
    # ページネーション
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    posts_page = posts[start:end]
    serializer = PostSerializer(posts_page, many=True, context={'request': request})
    
    return Response({
        'posts': serializer.data,
        'count': posts.count(),
        'has_next': end < posts.count(),
        'has_previous': page > 1
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """ユーザーを検索"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'users': [], 'count': 0})
    
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(profile__name__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ).exclude(id=request.user.id)  # 自分自身を除外
    
    # ページネーション
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    users_page = users[start:end]
    serializer = UserSerializer(users_page, many=True, context={'request': request})
    
    return Response({
        'users': serializer.data,
        'count': users.count(),
        'has_next': end < users.count(),
        'has_previous': page > 1
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_hashtags(request):
    """ハッシュタグを検索（将来的な拡張用）"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'hashtags': [], 'count': 0})
    
    # 現在は投稿内容からハッシュタグを抽出
    posts = Post.objects.filter(content__icontains=f'#{query}')
    hashtags = []
    
    for post in posts:
        # 簡単なハッシュタグ抽出（#で始まる単語）
        import re
        found_hashtags = re.findall(r'#\w+', post.content)
        hashtags.extend(found_hashtags)
    
    # 重複を除去してカウント
    hashtag_counts = {}
    for hashtag in hashtags:
        hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
    
    # カウント順にソート
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
    
    return Response({
        'hashtags': [{'tag': tag, 'count': count} for tag, count in sorted_hashtags],
        'count': len(sorted_hashtags)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_all(request):
    """統合検索（投稿、ユーザー、ハッシュタグ）"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({
            'posts': [],
            'users': [],
            'hashtags': [],
            'count': 0
        })
    
    # 投稿検索
    posts = Post.objects.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query) |
        Q(user__profile__name__icontains=query)
    ).order_by('-created_at')[:10]
    
    # ユーザー検索
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(profile__name__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ).exclude(id=request.user.id)[:10]
    
    # ハッシュタグ検索
    hashtag_posts = Post.objects.filter(content__icontains=f'#{query}')
    hashtags = []
    for post in hashtag_posts:
        import re
        found_hashtags = re.findall(r'#\w+', post.content)
        hashtags.extend(found_hashtags)
    
    hashtag_counts = {}
    for hashtag in hashtags:
        hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
    
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    posts_serializer = PostSerializer(posts, many=True, context={'request': request})
    users_serializer = UserSerializer(users, many=True, context={'request': request})
    
    return Response({
        'posts': posts_serializer.data,
        'users': users_serializer.data,
        'hashtags': [{'tag': tag, 'count': count} for tag, count in sorted_hashtags],
        'count': posts.count() + users.count() + len(sorted_hashtags)
    }) 
# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Follow
from .serializers import UserSerializer, PostSerializer, ProfileSerializer
from .follow_views import get_followers, get_following


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, username):
    """ユーザーのプロフィール詳細を取得"""
    try:
        user = User.objects.get(username=username)
        
        # プロフィール情報
        profile_serializer = ProfileSerializer(user.profile, context={'request': request})
        
        # ユーザー情報
        user_serializer = UserSerializer(user, context={'request': request})
        
        # 統計情報
        posts_count = Post.objects.filter(user=user).count()
        followers_count = user.followers.count()
        following_count = user.following.count()
        
        # フォロー状態
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
            'stats': {
                'posts_count': posts_count,
                'followers_count': followers_count,
                'following_count': following_count
            },
            'is_following': is_following
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_posts(request, username):
    """ユーザーの投稿一覧を取得"""
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        
        # ページネーション
        page_size = 20
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        posts_page = posts[start:end]
        serializer = PostSerializer(posts_page, many=True, context={'request': request})
        
        return Response({
            'posts': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': posts.count(),
            'has_next': end < posts.count(),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_liked_posts(request, username):
    """ユーザーがいいねした投稿一覧を取得"""
    try:
        user = User.objects.get(username=username)
        liked_posts = Post.objects.filter(likes__user=user).order_by('-created_at')
        
        # ページネーション
        page_size = 20
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        posts_page = liked_posts[start:end]
        serializer = PostSerializer(posts_page, many=True, context={'request': request})
        
        return Response({
            'posts': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': liked_posts.count(),
            'has_next': end < liked_posts.count(),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_retweets(request, username):
    """ユーザーがリツイートした投稿一覧を取得"""
    try:
        user = User.objects.get(username=username)
        retweeted_posts = Post.objects.filter(retweets__user=user).order_by('-created_at')
        
        # ページネーション
        page_size = 20
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        posts_page = retweeted_posts[start:end]
        serializer = PostSerializer(posts_page, many=True, context={'request': request})
        
        return Response({
            'posts': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': retweeted_posts.count(),
            'has_next': end < retweeted_posts.count(),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_followers_list(request, username):
    """ユーザーのフォロワー一覧を取得"""
    try:
        user = User.objects.get(username=username)
        followers = user.followers.all()
        
        # ページネーション
        page_size = 20
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        followers_page = followers[start:end]
        serializer = UserSerializer(followers_page, many=True, context={'request': request})
        
        return Response({
            'followers': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': followers.count(),
            'has_next': end < followers.count(),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_following_list(request, username):
    """ユーザーがフォローしているユーザー一覧を取得"""
    try:
        user = User.objects.get(username=username)
        following = user.following.all()
        
        # ページネーション
        page_size = 20
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        following_page = following[start:end]
        serializer = UserSerializer(following_page, many=True, context={'request': request})
        
        return Response({
            'following': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': following.count(),
            'has_next': end < following.count(),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND) 
# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Post
from .serializers import UserSerializer, PostSerializer
from .mention_utils import search_users_by_username, get_posts_mentioning_user, get_mentioned_users_in_post


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users_for_mention(request):
    """メンション用のユーザー検索"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'users': [], 'count': 0})
    
    limit = int(request.query_params.get('limit', 10))
    users = search_users_by_username(query, limit)
    serializer = UserSerializer(users, many=True, context={'request': request})
    
    return Response({
        'users': serializer.data,
        'count': len(users)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mentions_for_user(request):
    """現在のユーザーをメンションしている投稿を取得"""
    limit = int(request.query_params.get('limit', 50))
    page = int(request.query_params.get('page', 1))
    
    posts = get_posts_mentioning_user(request.user, limit)
    
    # ページネーション
    page_size = 20
    start = (page - 1) * page_size
    end = start + page_size
    
    posts_page = posts[start:end]
    serializer = PostSerializer(posts_page, many=True, context={'request': request})
    
    return Response({
        'posts': serializer.data,
        'count': len(posts),
        'has_next': end < len(posts),
        'has_previous': page > 1
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mentions_in_post(request, post_id):
    """特定の投稿でメンションされたユーザーを取得"""
    try:
        post = Post.objects.get(id=post_id)
        mentioned_users = get_mentioned_users_in_post(post)
        serializer = UserSerializer(mentioned_users, many=True, context={'request': request})
        
        return Response({
            'mentioned_users': serializer.data,
            'count': len(mentioned_users)
        })
    except Post.DoesNotExist:
        return Response({
            'error': '投稿が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_mentions(request, user_id):
    """特定のユーザーをメンションしている投稿を取得"""
    try:
        user = User.objects.get(id=user_id)
        limit = int(request.query_params.get('limit', 50))
        page = int(request.query_params.get('page', 1))
        
        posts = get_posts_mentioning_user(user, limit)
        
        # ページネーション
        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size
        
        posts_page = posts[start:end]
        serializer = PostSerializer(posts_page, many=True, context={'request': request})
        
        return Response({
            'posts': serializer.data,
            'user': UserSerializer(user, context={'request': request}).data,
            'count': len(posts),
            'has_next': end < len(posts),
            'has_previous': page > 1
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND) 
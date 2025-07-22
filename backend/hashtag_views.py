# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Hashtag, Post
from .serializers import HashtagSerializer, PostSerializer
from .hashtag_utils import get_trending_hashtags, search_hashtags, get_posts_by_hashtag


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_hashtags_api(request):
    """トレンドのハッシュタグを取得"""
    limit = int(request.query_params.get('limit', 10))
    hashtags = get_trending_hashtags(limit)
    serializer = HashtagSerializer(hashtags, many=True)
    
    return Response({
        'hashtags': serializer.data,
        'count': len(hashtags)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_hashtags_api(request):
    """ハッシュタグを検索"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'hashtags': [], 'count': 0})
    
    limit = int(request.query_params.get('limit', 20))
    hashtags = search_hashtags(query, limit)
    serializer = HashtagSerializer(hashtags, many=True)
    
    return Response({
        'hashtags': serializer.data,
        'count': len(hashtags)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hashtag_posts(request, hashtag_name):
    """特定のハッシュタグを含む投稿を取得"""
    limit = int(request.query_params.get('limit', 50))
    page = int(request.query_params.get('page', 1))
    
    posts = get_posts_by_hashtag(hashtag_name, limit)
    
    # ページネーション
    page_size = 20
    start = (page - 1) * page_size
    end = start + page_size
    
    posts_page = posts[start:end]
    serializer = PostSerializer(posts_page, many=True, context={'request': request})
    
    return Response({
        'posts': serializer.data,
        'hashtag': hashtag_name,
        'count': len(posts),
        'has_next': end < len(posts),
        'has_previous': page > 1
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hashtag_info(request, hashtag_name):
    """ハッシュタグの詳細情報を取得"""
    try:
        hashtag = Hashtag.objects.get(name=hashtag_name.lower())
        serializer = HashtagSerializer(hashtag)
        
        return Response({
            'hashtag': serializer.data
        })
    except Hashtag.DoesNotExist:
        return Response({
            'error': 'ハッシュタグが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_hashtags(request):
    """すべてのハッシュタグを取得（管理者用）"""
    hashtags = Hashtag.objects.all().order_by('-created_at')
    
    # ページネーション
    page_size = 50
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    hashtags_page = hashtags[start:end]
    serializer = HashtagSerializer(hashtags_page, many=True)
    
    return Response({
        'hashtags': serializer.data,
        'count': hashtags.count(),
        'has_next': end < hashtags.count(),
        'has_previous': page > 1
    }) 
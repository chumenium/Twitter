# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Trend
from .serializers import TrendSerializer
from .trend_utils import update_trends, get_trending_hashtags, get_trending_posts, get_trending_users, get_all_trends


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trends(request):
    """すべてのトレンドを取得"""
    limit = int(request.query_params.get('limit', 30))
    trends = get_all_trends(limit)
    serializer = TrendSerializer(trends, many=True)
    
    return Response({
        'trends': serializer.data,
        'count': len(trends)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_hashtags_api(request):
    """トレンドのハッシュタグを取得"""
    limit = int(request.query_params.get('limit', 10))
    trends = get_trending_hashtags(limit)
    serializer = TrendSerializer(trends, many=True)
    
    return Response({
        'trends': serializer.data,
        'count': len(trends)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_posts_api(request):
    """トレンドの投稿を取得"""
    limit = int(request.query_params.get('limit', 10))
    trends = get_trending_posts(limit)
    serializer = TrendSerializer(trends, many=True)
    
    return Response({
        'trends': serializer.data,
        'count': len(trends)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_users_api(request):
    """トレンドのユーザーを取得"""
    limit = int(request.query_params.get('limit', 10))
    trends = get_trending_users(limit)
    serializer = TrendSerializer(trends, many=True)
    
    return Response({
        'trends': serializer.data,
        'count': len(trends)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_trends_api(request):
    """トレンドを手動更新（管理者用）"""
    try:
        update_trends()
        return Response({
            'message': 'トレンドを更新しました'
        })
    except Exception as e:
        return Response({
            'error': f'トレンドの更新に失敗しました: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trends_by_type(request, trend_type):
    """特定のタイプのトレンドを取得"""
    if trend_type not in ['hashtag', 'post', 'user']:
        return Response({
            'error': '無効なトレンドタイプです'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    limit = int(request.query_params.get('limit', 10))
    trends = Trend.objects.filter(trend_type=trend_type).order_by('-score')[:limit]
    serializer = TrendSerializer(trends, many=True)
    
    return Response({
        'trends': serializer.data,
        'trend_type': trend_type,
        'count': len(trends)
    }) 
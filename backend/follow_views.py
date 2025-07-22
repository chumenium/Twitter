from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Follow
from .serializers import FollowSerializer, FollowToggleSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request):
    """フォロー/フォロー解除の切り替え"""
    serializer = FollowToggleSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow_id = serializer.validated_data['user_id']
        user_to_follow = get_object_or_404(User, id=user_to_follow_id)
        
        # 自分自身をフォローできないようにする
        if request.user == user_to_follow:
            return Response({
                'error': '自分自身をフォローすることはできません'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 既存のフォロー関係を確認
        follow_relation, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            # 既にフォローしている場合は削除（フォロー解除）
            follow_relation.delete()
            return Response({
                'following': False,
                'message': 'フォローを解除しました'
            })
        else:
            # 新しくフォローした場合
            return Response({
                'following': True,
                'message': 'フォローしました'
            })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    """現在のユーザーのフォロワー一覧を取得"""
    user_id = request.query_params.get('user_id')
    
    if user_id:
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user
    
    followers = Follow.objects.filter(following=target_user).select_related('follower')
    serializer = FollowSerializer(followers, many=True)
    
    return Response({
        'followers': serializer.data,
        'count': followers.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    """現在のユーザーがフォローしているユーザー一覧を取得"""
    user_id = request.query_params.get('user_id')
    
    if user_id:
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user
    
    following = Follow.objects.filter(follower=target_user).select_related('following')
    serializer = FollowSerializer(following, many=True)
    
    return Response({
        'following': serializer.data,
        'count': following.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_followers(request, user_id):
    """特定のユーザーのフォロワー一覧を取得"""
    target_user = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(following=target_user).select_related('follower')
    serializer = FollowSerializer(followers, many=True)
    
    return Response({
        'followers': serializer.data,
        'count': followers.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_following(request, user_id):
    """特定のユーザーがフォローしているユーザー一覧を取得"""
    target_user = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(follower=target_user).select_related('following')
    serializer = FollowSerializer(following, many=True)
    
    return Response({
        'following': serializer.data,
        'count': following.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_follow_status(request, user_id):
    """特定のユーザーをフォローしているかどうかを確認"""
    target_user = get_object_or_404(User, id=user_id)
    is_following = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).exists()
    
    return Response({
        'following': is_following
    }) 
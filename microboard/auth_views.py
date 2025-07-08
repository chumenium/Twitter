from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, ProfileSerializer
from .models import Profile


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """ユーザー登録API"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # プロフィールを作成
        Profile.objects.create(user=user)
        
        # 自動ログイン
        login(request, user)
        
        return Response({
            'message': 'ユーザー登録が完了しました',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """ユーザーログインAPI"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'message': 'ログインしました',
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'error': 'ユーザー名またはパスワードが正しくありません'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """ユーザーログアウトAPI"""
    logout(request)
    return Response({'message': 'ログアウトしました'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """現在のユーザー情報を取得"""
    return Response({
        'user': UserSerializer(request.user).data,
        'profile': ProfileSerializer(request.user.profile).data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """プロフィール更新API"""
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'プロフィールを更新しました',
            'profile': serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
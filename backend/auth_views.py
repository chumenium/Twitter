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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """ユーザー情報更新API"""
    user = request.user
    data = request.data.copy()
    
    # ユーザー名の重複チェック
    if 'username' in data and data['username'] != user.username:
        if User.objects.filter(username=data['username']).exists():
            return Response({
                'username': ['このユーザー名は既に使用されています']
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # ユーザー情報を更新
    if 'username' in data:
        user.username = data['username']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        user.email = data['email']
    
    user.save()
    
    return Response({
        'message': 'ユーザー情報を更新しました',
        'user': UserSerializer(user).data
    }) 
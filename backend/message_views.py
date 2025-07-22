# type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversations(request):
    """ユーザーの会話一覧を取得"""
    conversations = Conversation.objects.filter(participants=request.user)
    serializer = ConversationSerializer(conversations, many=True, context={'request': request})
    
    return Response({
        'conversations': serializer.data,
        'count': len(conversations)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_messages(request, conversation_id):
    """会話のメッセージ一覧を取得"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
        messages = conversation.messages.all()
        
        # 未読メッセージを既読にする
        unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
        unread_messages.update(is_read=True)
        
        serializer = MessageSerializer(messages, many=True)
        
        return Response({
            'messages': serializer.data,
            'conversation': ConversationSerializer(conversation, context={'request': request}).data,
            'count': len(messages)
        })
    except Conversation.DoesNotExist:
        return Response({
            'error': '会話が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, conversation_id):
    """メッセージを送信"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
        content = request.data.get('content', '').strip()
        
        if not content:
            return Response({
                'error': 'メッセージ内容を入力してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # 会話の更新日時を更新
        conversation.save()
        
        serializer = MessageSerializer(message)
        
        return Response({
            'message': serializer.data
        })
    except Conversation.DoesNotExist:
        return Response({
            'error': '会話が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_conversation(request):
    """新しい会話を作成"""
    other_user_id = request.data.get('user_id')
    
    if not other_user_id:
        return Response({
            'error': 'ユーザーIDが必要です'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        other_user = User.objects.get(id=other_user_id)
        
        # 既存の会話をチェック
        existing_conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).first()
        
        if existing_conversation:
            # 既存の会話がある場合はそれを返す
            serializer = ConversationSerializer(existing_conversation, context={'request': request})
            return Response({
                'conversation': serializer.data,
                'is_new': False
            })
        
        # 新しい会話を作成
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        
        serializer = ConversationSerializer(conversation, context={'request': request})
        
        return Response({
            'conversation': serializer.data,
            'is_new': True
        })
    except User.DoesNotExist:
        return Response({
            'error': 'ユーザーが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_messages_count(request):
    """未読メッセージ数を取得"""
    unread_count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    return Response({
        'unread_count': unread_count
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_conversation_read(request, conversation_id):
    """会話のメッセージを既読にする"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
        unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
        unread_messages.update(is_read=True)
        
        return Response({
            'message': 'メッセージを既読にしました'
        })
    except Conversation.DoesNotExist:
        return Response({
            'error': '会話が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    """メッセージを削除"""
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
        message.delete()
        
        return Response({
            'message': 'メッセージを削除しました'
        })
    except Message.DoesNotExist:
        return Response({
            'error': 'メッセージが見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_conversations(request):
    """会話を検索"""
    query = request.query_params.get('q', '').strip()
    
    if not query:
        return Response({
            'conversations': [],
            'count': 0
        })
    
    # 参加者のユーザー名で検索
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants__username__icontains=query
    )
    
    serializer = ConversationSerializer(conversations, many=True, context={'request': request})
    
    return Response({
        'conversations': serializer.data,
        'count': len(conversations)
    }) 
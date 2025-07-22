from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """現在のユーザーの通知一覧を取得"""
    notifications = Notification.objects.filter(recipient=request.user)
    
    # ページネーション
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    notifications_page = notifications[start:end]
    serializer = NotificationSerializer(notifications_page, many=True)
    
    return Response({
        'notifications': serializer.data,
        'count': notifications.count(),
        'unread_count': notifications.filter(is_read=False).count(),
        'has_next': end < notifications.count(),
        'has_previous': page > 1
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_notifications(request):
    """未読通知のみを取得"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    )
    
    serializer = NotificationSerializer(notifications, many=True)
    
    return Response({
        'notifications': serializer.data,
        'count': notifications.count()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """特定の通知を既読にする"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()
        
        return Response({
            'message': '通知を既読にしました',
            'notification': NotificationSerializer(notification).data
        })
    except Notification.DoesNotExist:
        return Response({
            'error': '通知が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """すべての通知を既読にする"""
    updated_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    
    return Response({
        'message': f'{updated_count}件の通知を既読にしました',
        'updated_count': updated_count
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """特定の通知を削除"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.delete()
        
        return Response({
            'message': '通知を削除しました'
        })
    except Notification.DoesNotExist:
        return Response({
            'error': '通知が見つかりません'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_notifications(request):
    """すべての通知を削除"""
    deleted_count = Notification.objects.filter(recipient=request.user).count()
    Notification.objects.filter(recipient=request.user).delete()
    
    return Response({
        'message': f'{deleted_count}件の通知を削除しました',
        'deleted_count': deleted_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_count(request):
    """未読通知数を取得"""
    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return Response({
        'unread_count': unread_count
    }) 
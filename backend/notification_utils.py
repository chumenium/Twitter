# type: ignore
from django.contrib.auth.models import User
from .models import Notification, Post


def create_notification(sender: User, recipient: User, notification_type: str, post: Post | None = None):
    """
    通知を作成するユーティリティ関数
    
    Args:
        sender: 通知を送信するユーザー
        recipient: 通知を受け取るユーザー
        notification_type: 通知タイプ ('like', 'retweet', 'follow', 'reply', 'mention')
        post: 関連する投稿（オプション）
    """
    # 自分自身への通知は作成しない
    if sender == recipient:
        return None
    
    # 既存の通知をチェック（重複防止）
    existing_notification = Notification.objects.filter(
        sender=sender,
        recipient=recipient,
        notification_type=notification_type,
        post=post
    ).first()
    
    if existing_notification:
        # 既存の通知がある場合は更新日時を更新
        existing_notification.save()
        return existing_notification
    
    # 新しい通知を作成
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        notification_type=notification_type,
        post=post
    )
    
    return notification


def create_like_notification(sender: User, post: Post):
    """いいね通知を作成"""
    return create_notification(sender, post.user, 'like', post)


def create_retweet_notification(sender: User, post: Post):
    """リツイート通知を作成"""
    return create_notification(sender, post.user, 'retweet', post)


def create_follow_notification(sender: User, recipient: User):
    """フォロー通知を作成"""
    return create_notification(sender, recipient, 'follow')


def create_reply_notification(sender: User, post: Post):
    """返信通知を作成"""
    if post.reply_to:
        return create_notification(sender, post.reply_to.user, 'reply', post)  # type: ignore
    return None


def create_mention_notification(sender: User, mentioned_user: User, post: Post):
    """メンション通知を作成"""
    return create_notification(sender, mentioned_user, 'mention', post) 
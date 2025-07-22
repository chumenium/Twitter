from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Like, Retweet, Follow, Post
from .notification_utils import create_like_notification, create_retweet_notification, create_follow_notification, create_reply_notification
from .hashtag_utils import process_post_hashtags
from .mention_utils import process_post_mentions

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ユーザーが作成された時にプロフィールを自動作成"""
    if created:
        Profile.objects.get_or_create(user=instance, defaults={'name': instance.username})

@receiver(post_save, sender=User)
def update_profile_name(sender, instance, **kwargs):
    """ユーザー名が変更された時にプロフィール名も更新"""
    try:
        profile = instance.profile
        # プロフィール名がユーザー名と同じ場合は自動更新
        if profile.name == instance.username or not profile.name:
            profile.name = instance.username
            profile.save(update_fields=['name'])
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance, name=instance.username)


@receiver(post_save, sender=Like)
def create_like_notification_signal(sender, instance, created, **kwargs):
    """いいねが作成された時に通知を作成"""
    if created:
        create_like_notification(instance.user, instance.post)


@receiver(post_save, sender=Retweet)
def create_retweet_notification_signal(sender, instance, created, **kwargs):
    """リツイートが作成された時に通知を作成"""
    if created:
        create_retweet_notification(instance.user, instance.original_post)


@receiver(post_save, sender=Follow)
def create_follow_notification_signal(sender, instance, created, **kwargs):
    """フォローが作成された時に通知を作成"""
    if created:
        create_follow_notification(instance.follower, instance.following)


@receiver(post_save, sender=Post)
def create_reply_notification_signal(sender, instance, created, **kwargs):
    """返信が作成された時に通知を作成"""
    if created and instance.reply_to:
        create_reply_notification(instance.user, instance)


@receiver(post_save, sender=Post)
def process_post_hashtags_signal(sender, instance, created, **kwargs):
    """投稿が作成・更新された時にハッシュタグを処理"""
    process_post_hashtags(instance)


@receiver(post_save, sender=Post)
def process_post_mentions_signal(sender, instance, created, **kwargs):
    """投稿が作成・更新された時にメンションを処理"""
    process_post_mentions(instance)

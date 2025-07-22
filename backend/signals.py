from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

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

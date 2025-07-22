from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.models import Profile


class Command(BaseCommand):
    help = '既存のプロフィール名をユーザー名と同期します'

    def handle(self, *args, **options):
        updated_count = 0
        
        for user in User.objects.all():
            try:
                profile = user.profile
                # プロフィール名が空またはユーザー名と同じ場合は更新
                if not profile.name or profile.name == user.username:
                    profile.name = user.username
                    profile.save(update_fields=['name'])
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'プロフィール名を更新: {user.username}'
                        )
                    )
            except Profile.DoesNotExist:
                # プロフィールが存在しない場合は作成
                Profile.objects.create(user=user, name=user.username)
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'プロフィールを作成: {user.username}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'完了: {updated_count}件のプロフィールを更新しました'
            )
        ) 
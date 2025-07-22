from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.content)[:30]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 同じユーザーが同じ投稿に複数回いいねできないように


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args, **kwargs):
        # プロフィール名が空の場合はユーザー名を使用
        if not self.name:
            self.name = self.user.username
        super().save(*args, **kwargs)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 同じユーザーが同じ投稿に複数回ブックマークできないように

    def __str__(self) -> str:
        return f"{self.user.username} bookmarked {str(self.post.content)[:30]}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # 同じユーザーが同じユーザーを複数回フォローできないように

    def __str__(self) -> str:
        return f"{self.follower.username} follows {self.following.username}"


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='retweets')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'original_post')  # 同じユーザーが同じ投稿を複数回リツイートできないように

    def __str__(self) -> str:
        return f"{self.user.username} retweeted {str(self.original_post.content)[:30]}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'いいね'),
        ('retweet', 'リツイート'),
        ('follow', 'フォロー'),
        ('reply', '返信'),
        ('mention', 'メンション'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.sender.username} {self.get_notification_type_display()} → {self.recipient.username}"


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self) -> str:
        return f"#{self.name}"
    
    @property
    def posts_count(self) -> int:
        return self.posts.count()


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_hashtags')
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'hashtag')
        indexes = [
            models.Index(fields=['post', 'hashtag']),
        ]
    
    def __str__(self) -> str:
        return f"{self.post.id} - #{self.hashtag.name}"


class Trend(models.Model):
    TREND_TYPES = [
        ('hashtag', 'ハッシュタグ'),
        ('post', '投稿'),
        ('user', 'ユーザー'),
    ]
    
    trend_type = models.CharField(max_length=10, choices=TREND_TYPES)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.FloatField(default=0.0)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['trend_type', '-score']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self) -> str:
        if self.trend_type == 'hashtag' and self.hashtag:
            return f"#{self.hashtag.name} (スコア: {self.score})"
        elif self.trend_type == 'post' and self.post:
            return f"投稿 {self.post.id} (スコア: {self.score})"
        elif self.trend_type == 'user' and self.user:
            return f"@{self.user.username} (スコア: {self.score})"
        return f"{self.get_trend_type_display()} (スコア: {self.score})"


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self) -> str:
        usernames = [user.username for user in self.participants.all()]
        return f"Conversation between {', '.join(usernames)}"
    
    def get_other_participant(self, current_user):
        """現在のユーザー以外の参加者を取得"""
        return self.participants.exclude(id=current_user.id).first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.sender.username}: {str(self.content)[:30]}"


class List(models.Model):
    LIST_TYPES = [
        ('public', '公開'),
        ('private', '非公開'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lists')
    members = models.ManyToManyField(User, related_name='list_memberships')
    list_type = models.CharField(max_length=10, choices=LIST_TYPES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'list_type']),
        ]
    
    def __str__(self) -> str:
        return f"{self.owner.username}のリスト: {self.name}"
    
    @property
    def members_count(self) -> int:
        return self.members.count()


class ListMember(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_subscriptions')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_additions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('list', 'user')
        indexes = [
            models.Index(fields=['list', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.username} in {self.list.name}"


class Analytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    posts_count = models.IntegerField(default=0)  # type: ignore
    likes_received = models.IntegerField(default=0)  # type: ignore
    retweets_received = models.IntegerField(default=0)  # type: ignore
    replies_received = models.IntegerField(default=0)  # type: ignore
    followers_gained = models.IntegerField(default=0)  # type: ignore
    followers_lost = models.IntegerField(default=0)  # type: ignore
    profile_views = models.IntegerField(default=0)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.date}"
    
    @property
    def net_followers(self) -> int:
        return int(self.followers_gained) - int(self.followers_lost)
    
    @property
    def total_engagement(self) -> int:
        return int(self.likes_received) + int(self.retweets_received) + int(self.replies_received)


class PostAnalytics(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='analytics')
    views_count = models.IntegerField(default=0)  # type: ignore
    unique_views_count = models.IntegerField(default=0)  # type: ignore
    shares_count = models.IntegerField(default=0)  # type: ignore
    bookmarks_count = models.IntegerField(default=0)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['post', 'views_count']),
        ]
    
    def __str__(self) -> str:
        return f"Analytics for Post {self.post.id}"
    
    @property
    def engagement_rate(self) -> float:
        if self.views_count > 0:
            return (self.post.likes.count() + self.post.retweets.count() + self.post.replies.count()) / self.views_count * 100
        return 0.0



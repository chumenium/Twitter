from rest_framework import serializers
from .models import Post, Like, Bookmark, Profile, Follow, Retweet, Notification, Hashtag, PostHashtag, Trend, Conversation, Message, List, ListMember
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile', 'display_name', 'followers_count', 'following_count', 'is_following']
    
    def get_profile(self, obj):
        try:
            profile = obj.profile
            return {
                'name': profile.name,
                'image': profile.image.url if profile.image else None,
                'bio': profile.bio
            }
        except:
            return {
                'name': obj.username,
                'image': None,
                'bio': ''
            }
    
    def get_display_name(self, obj):
        """プロフィール名を優先し、なければユーザー名を返す"""
        try:
            profile = obj.profile
            # プロフィール名が空またはユーザー名と同じ場合はユーザー名を返す
            if profile.name and profile.name != obj.username:
                return profile.name
            return obj.username
        except:
            return obj.username
    
    def get_followers_count(self, obj):
        """フォロワー数を取得"""
        return obj.followers.count()
    
    def get_following_count(self, obj):
        """フォロー数を取得"""
        return obj.following.count()
    
    def get_is_following(self, obj):
        """現在のユーザーがこのユーザーをフォローしているかどうか"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(follower=request.user).exists()
        return False


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'bio', 'image', 'location', 'website']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()
    is_retweeted = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    video_thumbnail_url = serializers.SerializerMethodField()
    has_video = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'video', 'video_thumbnail', 'video_url', 'video_thumbnail_url', 'has_video', 'reply_to', 'created_at', 'likes_count', 'is_liked', 'is_bookmarked', 'retweets_count', 'is_retweeted', 'replies_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False

    def get_retweets_count(self, obj):
        return obj.retweets.count()

    def get_is_retweeted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.retweets.filter(user=request.user).exists()
        return False

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_video_url(self, obj):
        if obj.video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video.url)
            return obj.video.url
        return None

    def get_video_thumbnail_url(self, obj):
        if obj.video_thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_thumbnail.url)
            return obj.video_thumbnail.url
        return None

    def get_has_video(self, obj):
        return bool(obj.video)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'reply_to']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("パスワードが一致しません")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']


class FollowToggleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("指定されたユーザーが存在しません")
        return value


class RetweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    original_post = PostSerializer(read_only=True)
    
    class Meta:
        model = Retweet
        fields = ['id', 'user', 'original_post', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'notification_type_display', 'post', 'is_read', 'created_at']


class HashtagSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'posts_count', 'created_at']


class PostHashtagSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True)
    
    class Meta:
        model = PostHashtag
        fields = ['id', 'hashtag', 'created_at']


class TrendSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    trend_type_display = serializers.CharField(source='get_trend_type_display', read_only=True)
    
    class Meta:
        model = Trend
        fields = ['id', 'trend_type', 'trend_type_display', 'hashtag', 'post', 'user', 'score', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'is_read', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'unread_count', 'other_participant', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
    
    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other_user = obj.get_other_participant(request.user)
            if other_user:
                return UserSerializer(other_user).data
        return None


class ListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    list_type_display = serializers.CharField(source='get_list_type_display', read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'owner', 'list_type', 'list_type_display', 'members_count', 'is_member', 'created_at', 'updated_at']
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(id=request.user.id).exists()
        return False


class ListMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    added_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ListMember
        fields = ['id', 'user', 'added_by', 'created_at']


class ListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['name', 'description', 'list_type']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data) 
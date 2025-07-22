from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Like, Bookmark, Retweet, Hashtag
from .serializers import PostSerializer, PostCreateSerializer, HashtagSerializer
from .mention_utils import get_mentioned_users_in_post as get_mentions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': post.likes.count()})
        
        return Response({'liked': True, 'likes_count': post.likes.count()})

    @action(detail=True, methods=['post'])
    def toggle_bookmark(self, request, pk=None):
        post = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            bookmark.delete()
            return Response({'bookmarked': False})
        
        return Response({'bookmarked': True})

    @action(detail=True, methods=['post'])
    def toggle_retweet(self, request, pk=None):
        post = self.get_object()
        retweet, created = Retweet.objects.get_or_create(user=request.user, original_post=post)
        
        if not created:
            retweet.delete()
            return Response({'retweeted': False, 'retweets_count': post.retweets.count()})
        
        return Response({'retweeted': True, 'retweets_count': post.retweets.count()})

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """投稿への返信一覧を取得"""
        post = self.get_object()
        replies = Post.objects.filter(reply_to=post).order_by('created_at')
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """投稿の詳細情報を取得（ハッシュタグ、メンション、返信数など）"""
        post = self.get_object()
        
        # ハッシュタグを取得
        hashtags = post.post_hashtags.all()
        hashtag_serializer = HashtagSerializer([ph.hashtag for ph in hashtags], many=True)
        
        # メンションされたユーザーを取得
        mentioned_users = get_mentions(post)
        from .serializers import UserSerializer
        user_serializer = UserSerializer(mentioned_users, many=True, context={'request': request})
        
        # 返信数を取得
        replies_count = post.replies.count()
        
        # リツイート数を取得
        retweets_count = post.retweets.count()
        
        # いいね数を取得
        likes_count = post.likes.count()
        
        # ブックマーク数を取得
        bookmarks_count = post.bookmarks.count()
        
        # メインの投稿シリアライザー
        post_serializer = self.get_serializer(post)
        
        return Response({
            'post': post_serializer.data,
            'hashtags': hashtag_serializer.data,
            'mentioned_users': user_serializer.data,
            'stats': {
                'replies_count': replies_count,
                'retweets_count': retweets_count,
                'likes_count': likes_count,
                'bookmarks_count': bookmarks_count
            }
        })

    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """タイムライン用の投稿一覧（フォロー中のユーザーの投稿のみ）"""
        # フォロー中のユーザーIDを取得
        following_ids = request.user.following.values_list('following_id', flat=True)
        # 自分の投稿も含める
        following_ids = list(following_ids) + [request.user.id]
        
        posts = Post.objects.filter(user_id__in=following_ids).order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_posts(self, request):
        """すべての投稿一覧"""
        posts = Post.objects.all().order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """自分の投稿一覧"""
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def liked_posts(self, request):
        """いいねした投稿一覧"""
        posts = Post.objects.filter(likes__user=request.user).order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def bookmarked_posts(self, request):
        """ブックマークした投稿一覧"""
        posts = Post.objects.filter(bookmarks__user=request.user).order_by('-created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data) 
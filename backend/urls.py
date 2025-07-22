from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet
from .auth_views import register_user, login_user, logout_user, get_current_user, update_profile, update_user
from .follow_views import toggle_follow, get_followers, get_following, get_user_followers, get_user_following, check_follow_status
from .search_views import search_posts, search_users, search_hashtags, search_all
from .notification_views import get_notifications, get_unread_notifications, mark_notification_read, mark_all_notifications_read, delete_notification, delete_all_notifications, get_notification_count
from .hashtag_views import get_trending_hashtags_api, search_hashtags_api, get_hashtag_posts, get_hashtag_info, get_all_hashtags
from .mention_views import search_users_for_mention, get_mentions_for_user, get_mentions_in_post, get_user_mentions
from .profile_views import get_user_profile, get_user_posts, get_user_liked_posts, get_user_retweets, get_user_followers_list, get_user_following_list
from .trend_views import get_trends, get_trending_hashtags_api, get_trending_posts_api, get_trending_users_api, update_trends_api, get_trends_by_type
from .message_views import get_conversations, get_conversation_messages, send_message, create_conversation, get_unread_messages_count, mark_conversation_read, delete_message, search_conversations

# APIルーター
router = DefaultRouter()
router.register(r'api/posts', PostViewSet)

urlpatterns = [
    # レガシーURL（Reactに移行後は削除予定）
    path('', views.post_list, name='post_list'),
    path('timeline/', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('mypage/', views.mypage, name='mypage'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('settings/', views.settings, name='settings'),
    
    # 認証API
    path('api/auth/register/', register_user, name='api_register'),
    path('api/auth/login/', login_user, name='api_login'),
    path('api/auth/logout/', logout_user, name='api_logout'),
    path('api/auth/user/', get_current_user, name='api_current_user'),
    path('api/auth/profile/', update_profile, name='api_update_profile'),
    path('api/auth/user/update/', update_user, name='api_update_user'),
    
    # フォローAPI
    path('api/follows/toggle_follow/', toggle_follow, name='api_toggle_follow'),
    path('api/follows/followers/', get_followers, name='api_followers'),
    path('api/follows/following/', get_following, name='api_following'),
    path('api/follows/user_followers/', get_followers, name='api_user_followers'),
    path('api/follows/user_following/', get_following, name='api_user_following'),
    path('api/follows/user/<int:user_id>/followers/', get_user_followers, name='api_user_followers_detail'),
    path('api/follows/user/<int:user_id>/following/', get_user_following, name='api_user_following_detail'),
    path('api/follows/check/<int:user_id>/', check_follow_status, name='api_check_follow_status'),
    
    # 検索API
    path('api/search/posts/', search_posts, name='api_search_posts'),
    path('api/search/users/', search_users, name='api_search_users'),
    path('api/search/hashtags/', search_hashtags, name='api_search_hashtags'),
    path('api/search/', search_all, name='api_search_all'),
    
    # 通知API
    path('api/notifications/', get_notifications, name='api_notifications'),
    path('api/notifications/unread/', get_unread_notifications, name='api_unread_notifications'),
    path('api/notifications/count/', get_notification_count, name='api_notification_count'),
    path('api/notifications/<int:notification_id>/read/', mark_notification_read, name='api_mark_notification_read'),
    path('api/notifications/read-all/', mark_all_notifications_read, name='api_mark_all_notifications_read'),
    path('api/notifications/<int:notification_id>/delete/', delete_notification, name='api_delete_notification'),
    path('api/notifications/delete-all/', delete_all_notifications, name='api_delete_all_notifications'),
    
    # ハッシュタグAPI
    path('api/hashtags/trending/', get_trending_hashtags_api, name='api_trending_hashtags'),
    path('api/hashtags/search/', search_hashtags_api, name='api_search_hashtags'),
    path('api/hashtags/<str:hashtag_name>/posts/', get_hashtag_posts, name='api_hashtag_posts'),
    path('api/hashtags/<str:hashtag_name>/info/', get_hashtag_info, name='api_hashtag_info'),
    path('api/hashtags/', get_all_hashtags, name='api_all_hashtags'),
    
    # メンションAPI
    path('api/mentions/search-users/', search_users_for_mention, name='api_search_users_for_mention'),
    path('api/mentions/my-mentions/', get_mentions_for_user, name='api_my_mentions'),
    path('api/mentions/post/<int:post_id>/', get_mentions_in_post, name='api_mentions_in_post'),
    path('api/mentions/user/<int:user_id>/', get_user_mentions, name='api_user_mentions'),
    
    # プロフィールAPI
    path('api/profile/<str:username>/', get_user_profile, name='api_user_profile'),
    path('api/profile/<str:username>/posts/', get_user_posts, name='api_user_posts'),
    path('api/profile/<str:username>/liked-posts/', get_user_liked_posts, name='api_user_liked_posts'),
    path('api/profile/<str:username>/retweets/', get_user_retweets, name='api_user_retweets'),
    path('api/profile/<str:username>/followers/', get_user_followers_list, name='api_user_followers_list'),
    path('api/profile/<str:username>/following/', get_user_following_list, name='api_user_following_list'),
    
    # トレンドAPI
    path('api/trends/', get_trends, name='api_trends'),
    path('api/trends/hashtags/', get_trending_hashtags_api, name='api_trending_hashtags'),
    path('api/trends/posts/', get_trending_posts_api, name='api_trending_posts'),
    path('api/trends/users/', get_trending_users_api, name='api_trending_users'),
    path('api/trends/update/', update_trends_api, name='api_update_trends'),
    path('api/trends/<str:trend_type>/', get_trends_by_type, name='api_trends_by_type'),
    
    # メッセージAPI
    path('api/messages/conversations/', get_conversations, name='api_conversations'),
    path('api/messages/conversations/create/', create_conversation, name='api_create_conversation'),
    path('api/messages/conversations/search/', search_conversations, name='api_search_conversations'),
    path('api/messages/conversations/<int:conversation_id>/', get_conversation_messages, name='api_conversation_messages'),
    path('api/messages/conversations/<int:conversation_id>/send/', send_message, name='api_send_message'),
    path('api/messages/conversations/<int:conversation_id>/read/', mark_conversation_read, name='api_mark_conversation_read'),
    path('api/messages/unread-count/', get_unread_messages_count, name='api_unread_messages_count'),
    path('api/messages/<int:message_id>/delete/', delete_message, name='api_delete_message'),
]

# APIルートを追加
urlpatterns += router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


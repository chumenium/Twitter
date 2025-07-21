from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet
from .auth_views import register_user, login_user, logout_user, get_current_user, update_profile, update_user

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
]

# APIルートを追加
urlpatterns += router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


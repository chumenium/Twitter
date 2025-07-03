from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from microboard.views import post_list



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('microboard.urls')),  # 投稿アプリ
    path('accounts/', include('allauth.urls')),  # allauth用
    path('', lambda request: redirect('post_list')),
    path("timeline/", post_list, name="post_list"),  # ← スラッシュを追加

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

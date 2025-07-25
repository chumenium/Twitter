from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from backend.views import post_list



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),  # 投稿アプリ（認証も含む）
    path('', lambda request: redirect('post_list')),
    path("timeline/", post_list, name="post_list"),  # ← スラッシュを追加

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

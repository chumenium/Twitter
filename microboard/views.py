from django.shortcuts import render, redirect
from .models import Post, Bookmark
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Like
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ProfileForm
from django.contrib.auth.models import User


#新規登録処理
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_edit')  # 登録後プロフィール編集へ
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


#ログイン処理
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


#ログアウト処理
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


#タイムライン表示
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
        for post in posts:
            post.is_liked = post.likes.filter(user=current_user).exists()
            post.is_bookmarked = post.bookmarks.filter(user=current_user).exists()
    else:
        # 開発用：デフォルトユーザーを使用
        try:
            current_user = User.objects.first()
            for post in posts:
                post.is_liked = post.likes.filter(user=current_user).exists()
                post.is_bookmarked = post.bookmarks.filter(user=current_user).exists()
        except:
            current_user = None
            for post in posts:
                post.is_liked = False
                post.is_bookmarked = False

    return render(request, 'microboard/post_list.html', {'posts': posts, 'current_user': current_user})



# 新規投稿画面
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponse("権限がありません", status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'microboard/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponse("権限がありません", status=403)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'microboard/post_confirm_delete.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'microboard/post_form.html', {'form': form})

def toggle_like(request, pk):
    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first()
    
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=current_user, post=post)
    if not created:
        like.delete()  # すでにあれば取り消し
    return HttpResponseRedirect(reverse('post_list'))


def toggle_bookmark(request, pk):
    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first()
    
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=current_user, post=post)
    if not created:
        bookmark.delete()  # すでにあれば取り消し
    return HttpResponseRedirect(reverse('post_list'))


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'microboard/profile_edit.html', {'form': form})


def mypage(request):
    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first()
    
    profile = current_user.profile
    posts = Post.objects.filter(user=current_user)
    media_posts = posts.exclude(image='')  # 画像付き
    liked_posts = Post.objects.filter(likes__user=current_user)
    bookmarked_posts = Post.objects.filter(bookmarks__user=current_user)

    context = {
        'profile': profile,
        'posts': posts,
        'media_posts': media_posts,
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
        'current_user': current_user,
    }
    return render(request, 'microboard/mypage.html', context)


def bookmarks(request):
    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first()
    
    bookmarked_posts = Post.objects.filter(bookmarks__user=current_user).order_by('-created_at')
    
    for post in bookmarked_posts:
        post.is_liked = post.likes.filter(user=current_user).exists()
        post.is_bookmarked = True  # ブックマークページなので常にTrue

    return render(request, 'microboard/bookmarks.html', {
        'posts': bookmarked_posts,
        'current_user': current_user
    })


def settings(request):
    # 開発用：ログインしていない場合はデフォルトユーザーを使用
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first()
    
    return render(request, 'microboard/settings.html', {
        'current_user': current_user
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm
from .utils import get_page_context


def index(request):
    """Выводит шаблон главной страницы."""
    post_list = Post.objects.select_related('author', 'group')
    page_obj = get_page_context(post_list, request)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Выводит шаблон с постами группы."""
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.select_related()
    post_list = group.posts.all()
    page_obj = get_page_context(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Выводит страницу профиля пользователя."""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related()
    post_list = Post.objects.filter(author=author).all()
    page_obj = get_page_context(post_list, request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Выводит страницу отдельно взятого поста."""
    post_object = Post.objects.select_related()
    post_object = get_object_or_404(Post, id=post_id)
    context = {
        'post': post_object,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Возможность создать новый пост для авторизованного пользователя."""
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('posts:profile', request.user.username)

    context = {
        'form': form
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Возможность редактировать пост для авторизованного пользователя."""
    post_object = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=post_object)
    if (request.method == 'POST' and form.is_valid()):
        form.save()

        return redirect('posts:post_detail', post_id)

    context = {
        'form': form,
        'True': True,
        'post': post_object
    }

    return render(request, 'posts:post_edit', context)

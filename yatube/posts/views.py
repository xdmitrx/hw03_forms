from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .models import Post, Group, User
from .forms import PostForm

from . import constants


def index(request):
    posts = Post.objects.select_related(
        'author',
        'group',
    )[:constants.POSTS_PER_PAGE]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:constants.POSTS_PER_PAGE]
    post_list = Post.objects.select_related('group',)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author_object = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author_object).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author_object': author_object,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_object = get_object_or_404(Post, id=post_id)
    context = {
        'post': post_object,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if (request.method == 'POST' and form.is_valid()):
        post = form.save(commit=False)
        form.instance.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post_object = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post_object)
    if (request.method == 'POST' and form.is_valid()):
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': is_edit
    }
    return render(request, 'posts/create_post.html', context)

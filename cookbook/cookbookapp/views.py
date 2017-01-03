from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect


def index(request):
    posts = Post.objects.order_by('-pub_date')
    context = {'posts': posts}
    return render(request, 'cookbookapp/index.html', context)


def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'cookbookapp/detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('http://127.0.0.1:8000/cookbookapp/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'cookbookapp/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'cookbook/post_edit.html', {'form': form})
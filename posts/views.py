from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import Post
from .forms import PostForm 
# Create your views here.
# def index(request):
#     return HttpResponse("<h1>Hello, world!</h1>")

def home_view(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "posts/home_view.html", context)

def post_detail_view(request, id):
    post=None
    if id is not None:
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Http404
    context = {'post': post}
    return render(request, "posts/detail.html", context)


def post_create_view(request):
    print(request.POST)
    form = PostForm()
    context = {'form': form}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.get("title")
            content = form.get("content")
            
            print(f'Title: {title},\nContent: {content}')
            
            post = Post.objects.create(title=title, content=content)
            context = {'post': post}
            
    return render(request, "posts/create.html", context)


def post_update_view(request, pk):
    context = {}
    return render(request, "posts/update.html", context)

def post_delete_view(request):
    context = {}
    return render(request, "posts/delete.html", context)

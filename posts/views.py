from django.shortcuts import render, redirect
from django.http import Http404

from .models import Post
from .forms import PostForm 
# Create your views here.


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
    form = PostForm()
    context = {'form': form}
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            
            # print(f'Title: {title}, Content: {content}')
            
            post = Post.objects.create(title=title, content=content)
            context = {'post': post}
            # redirect to a new URL:
            return redirect('/posts/')
            
    return render(request, "posts/create.html", context)


def post_update_view(request, pk):
    context = {}
    return render(request, "posts/update.html", context)

def post_delete_view(request):
    context = {}
    return render(request, "posts/delete.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q

from .models import Post
from .forms import PostForm 
# Create your views here.


def home_view(request):
    posts = Post.objects.all().order_by('-updated')
    for post in posts:
        short_desc = post.content[:20]
    context = {'posts': posts, 'short_desc': short_desc}
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


def post_search_view(request):
    if request.method == "POST":
        query = request.GET.get("q")
        if query:
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
            print(results)
            context = {'results':results}   
            return render(request, "posts/search.html", context)
    return render(request, "posts/search.html")



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


def post_update_view(request, id):

    # fetch the object related to passed id
    post = get_object_or_404(Post, id=id)
    
    # pass the object as instance in form
    form = PostForm(instance=post)
    # post updated data
    if request.method == "POST":
        form = PostForm(request.POST or None, instance=post)
    
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            return redirect('/posts/')

    context = {'form': form}
    return render(request, "posts/update.html", context)

def post_delete_view(request, id):
    post = Post.objects.get(id=id)

    # post updated data
    if request.method == "POST":
        post.delete()
        return redirect('/posts/')
    context = {'post': post}
    return render(request, "posts/delete.html", context)

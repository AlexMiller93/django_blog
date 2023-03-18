import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from .models import Post, Comment
from .forms import CommentForm
# Create your views here.

# Working with Posts

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
        #     context['liked_post'] = liked
        return context
    

class UserPostListView(LoginRequiredMixin, ListView):
    # ! don't work, renders no one post 
    model = Post
    template_name = 'posts/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        # liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user = self.request.user, post=i)]
        # context['liked_post'] = liked
        return context
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # post = Post.objects.all()
        return Post.objects.filter(author=user).order_by('-date_created')
        
class PostDetailView(DetailView):
    model = Post
    # template_name = 'posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # comments 
        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-date_created')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        
        # post likes
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['post_is_liked'] = liked
        
        ### Comments likes ###
        
        # post to like
        # post_for_like = get_object_or_404(Post, id=self.kwargs['pk'])
        
        # comment or comments of post to like
        
        
        # comment_for_like = get_object_or_404(Comment, id=self.kwargs['pk'])
        # # comment_for_like = Comment.objects.filter(
        # #     post=self.get_object())
        # liked = False
        
        # if comment_for_like.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # data['comment_is_liked'] = liked
        
        # for like in comment_for_like.likes.all():
        #     if like == self.request.user:
        #         liked = True
        #     data['comment_is_liked'] = liked
        
        
        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
            author=self.request.user,
            post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content', 'tags')
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content', 'tags')
    update = None
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"
    # template_name = "posts/delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
'''
class PostDisplayView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post' 
    login_url = 'login'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.pk)])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # comments = Comment.objects.filter(post=self.get_object()).order_by('-date_created')
        # data['comments'] = comments
        data['form'] = CommentForm()
        return data

class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentCreateView.as_view()
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/create.html'
    fields = ('title', 'content',)
    login_url = 'login'
    
    def form_valid(self, form):  
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/update.html'
    fields = ['title', 'content']
    login_url = 'login'
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
        return view(request, *args, **kwargs)
        
'''
# TODO Make simple search maybe with CBV or FBV
class PostSearchResultsView(ListView):
    model = Post
    template_name = 'posts/search.html'
    
    # https://stackoverflow.com/questions/13416502/django-search-form-in-class-based-listview
    def get_queryset(self):
        query = self.request.GET.get('q')
        
        object_list = self.model.objects.filter(title__icontains=query)
        return object_list
    
def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


# Working with Comments

class PostCommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'posts/comments.html'
    context_object_name = 'comments'
    login_url = 'login'


    def get_queryset(self):
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return Comment.objects.filter(Comment.post.pk == post.pk).order_by('-date_created')

class PostCommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        post = self.get_object()
        # post = get_object_or_404(Post, kwargs={'pk': post.pk})
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', kwargs={'pk': post.pk})
    
    '''
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(PostCommentCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user # author of comment is current user
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        post = self.get_object()
        return reverse("post_detail", kwargs={'pk': post.pk}) + '#comments' 
    '''
    
class PostCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('body',)
    template_name = "posts/post_detail.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk}) + '#comments'
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class PostCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': post.pk})

class PostCommentLike(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk) # returns 1 comment object
        
        liked = False
        for like in comment.likes.all():
            if like == request.user:
                liked = True
                break
            
        if liked:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('post_detail', args=[str(post_pk)]))
    
    
'''
def PostCommentLike(request, pk):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
'''

'''
@login_required 
class LikeView(View):
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        like = Like()
        like.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        like.user = self.request.user
        like.save()
        return redirect(self.get_success_url())

@login_required
def like(request):
    post_id = request.GET.get("likeId", post.pk)
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked = False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        like = True
        Like.objects.create(user=user, post=post)
        resp = {
            'liked': liked
        }
        response = json.dumps(resp)
        return HttpResponse(response, content_type = "application/json")
'''
    
    # https://learndjango.com/tutorials/django-search-tutorial

''' 
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list =  Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))
        
        return object_list
    '''
    
'''
    def post_search_view(request):
    if request.method == "POST":
        query = request.GET.get("q")
        if query:
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
            print(results)
            context = {'results':results}   
            return render(request, "posts/search.html", context)
    return render(request, "posts/search.html")
    '''
        
'''
    def get_queryset(self):
        
        title = self.kwargs.get('title', '')
        object_list = self.model.objects.all()
        if title:
            object_list = object_list.filter(title__icontains=title)

        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()

        return object_list
    '''
'''
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
'''

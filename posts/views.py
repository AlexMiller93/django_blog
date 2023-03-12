from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from .models import Post, Comment
from .forms import CommentForm
# Create your views here.

# Working with Posts

class PostListView(ListView):
    model = Post
    # template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    login_url = 'login'
    queryset=Post.objects.all()
    

class PostUserListView(ListView):
    
    # ! don't work, renders no one post 
    model = Post
    paginate_by = 3
    
    def get_queryset(self):
        user = self.request.user
        # post = Post.objects.all()
        return Post.objects.filter(author=user).order_by('-date_created')
    
class PostDetailView(DetailView):
    model = Post
    # template_name = 'posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-date_created')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
            author=self.request.user,
            post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content')
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'content')
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
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list

# Working with Comments

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
        return reverse('post-detail', kwargs={'pk': post.pk}) + '#comments'
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
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
        return reverse_lazy('post-detail', kwargs={'pk': post.pk})
    
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

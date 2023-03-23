from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy

from .models import Post, Comment
from .forms import CommentForm
# Create your views here.

### Working with Posts ###

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        ## comments 
        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-date_created')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        
        ## post likes
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['post_is_liked'] = liked
        
        return data
    
    # add new comments
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
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostSearchResultsView(ListView):
    model = Post
    template_name = 'posts/search.html'
    
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        
        object_list = self.model.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) 
        )
        return object_list

def post_like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': pk}))

### Working with Comments ###

class CommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
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
        return reverse('post_detail', args=[str(post.pk)])
    


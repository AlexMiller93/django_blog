from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Post
# Create your views here.

class BlogListView(ListView):
    paginate_by = 3
    model = Post
    context_object_name = "posts"
    template_name = 'posts/home.html'
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return Post.objects.filter(author=self.request.user)
    #     return Post.objects.filter(author=None)
        

class BlogDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html' #
    
class BlogCreateView(CreateView):
    model = Post
    template_name = 'posts/create.html'
    fields = ['title', 'author', 'content']


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'posts/update.html'
    fields = ['title', 'content']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('home')

# TODO Make simple search maybe with CBV or FBV

class BlogSearchResultsView(ListView):
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
    ''' 
    # https://learndjango.com/tutorials/django-search-tutorial
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

from django.urls import path

from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostSearchResultsView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    
    # CRUD with posts
    path('post/create/', PostCreateView.as_view(), 
        name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), 
        name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), 
        name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), 
        name='post_delete'),
    
    path('post/<int:pk>/', views.post_like, name='post_like'),
    
    path('search_posts/', PostSearchResultsView.as_view(), 
        name='search_posts'),
    
    

]

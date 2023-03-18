from django.urls import path

from . import views
from .views import (
    PostListView,
    UserPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostSearchResultsView,
    
    PostLike,
    
    PostCommentCreateView,
    PostCommentUpdateView,
    PostCommentDeleteView,
    PostCommentLike,
)

# app_name='posts'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('user_posts/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    path('post-like/<int:pk>/', views.PostLike, name='post_like'),
    path('post/<int:post_pk>/comment/<int:pk>/like/', PostCommentLike.as_view(), name='comment_like'),
    
    path('search_posts/', PostSearchResultsView.as_view(), name='search_posts'),
    
    path('post/<int:pk>/add_comment/', 
        PostCommentCreateView.as_view(), name='post_comment'),
    path('post/<int:pk>/update_comment/', 
        PostCommentUpdateView.as_view(), name='post_comment_edit'),
    path('post/<int:pk>/delete_comment/', 
        PostCommentDeleteView.as_view(), name='post_comment_delete'),
    
    # path('search/', PostSearchResultsView.as_view(), name='search_results'),

]

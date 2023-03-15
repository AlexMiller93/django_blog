from django.urls import path

from .views import (
    PostListView,
    PostUserListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    # PostSearchResultsView,
    
    PostCommentCreateView,
    PostCommentUpdateView,
    PostCommentDeleteView,
)

# app_name='posts'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    # path('user/<str:username>/', PostUserListView.as_view(), name='post_list'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    path('post/<int:pk>/add_comment/', 
        PostCommentCreateView.as_view(), name='post_comment'),
    path('post/<int:pk>/update_comment/', 
        PostCommentUpdateView.as_view(), name='post_comment_edit'),
    path('post/<int:pk>/delete_comment/', 
        PostCommentDeleteView.as_view(), name='post_comment_delete'),
    
    # path('search/', PostSearchResultsView.as_view(), name='search_results'),

]

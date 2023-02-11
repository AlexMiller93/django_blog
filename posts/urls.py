from django.urls import path

from posts.views import(
    post_detail_view,
    # post_create_view,
    post_update_view,
    post_delete_view,
    home_view
)

app_name='posts'
urlpatterns = [
    # path('', index, name='index'),
    path('', home_view, name='home_view'),
    path('<int:id>/', post_detail_view, name='detail'),
    
    # path('create/', post_create_view, name='create'),
    path('<int:id>/edit/', post_update_view, name='update'),
    path('<int:ud>/delete/', post_delete_view, name='delete'),
    
    
]

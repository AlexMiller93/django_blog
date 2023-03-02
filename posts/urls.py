from django.urls import path

from . import views


app_name='posts'
urlpatterns = [
    path('', views.home_view, name='home_view'),
    
    path('<int:id>/', views.post_detail_view, name='detail'),
    path('search/', views.post_search_view, name='search'),
    
    path('create/', views.post_create_view, name='create'),
    path('<int:id>/edit/', views.post_update_view, name='update'),
    path('<int:id>/delete/', views.post_delete_view, name='delete'),
    
    
]

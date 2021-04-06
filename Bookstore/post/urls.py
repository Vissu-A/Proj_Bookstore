from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^$', views.post_list, name = 'post-list'),
    path('new/', views.new_post, name='new-post'),
    path('<int:postid>/', views.post_details, name='post-detail'),
    path('like-comment/', views.like_comment, name = 'like-comment'),
]
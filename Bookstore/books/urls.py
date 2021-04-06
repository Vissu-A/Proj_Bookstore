from django.urls import path, re_path
from books import views

urlpatterns = [
    re_path('^$', views.homeview, name='home-page'),
]
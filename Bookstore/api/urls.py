from rest_framework.urls import url

from rest_framework_simplejwt import views as jwtviews

from django.urls import path, re_path

from api import views

urlpatterns = [
    re_path(r'^create-user/$', views.creating_user, name = 'create-user-api'),
    path('activate-account/<uidb64>/<token>/', views.account_activate, name = 'account-activate-api'),
    path('user/login/', jwtviews.TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', jwtviews.TokenRefreshView.as_view(), name = 'token_refresh'),

    path('users/list/', views.users_list, name = 'users-list-api'),
    path('user/info/', views.user_info, name = 'user-info-api'),
    path('user/edit/', views.user_info_edit, name = 'user-edit-api'),

    path('user/reset-password/', views.user_password_reset, name = 'users-password-reset'),
    path('user/reset-password/<uidb64>/<token>/', views.user_password_reset_link_click, name = 'user-password-reset-link-mail'),

    path('user/change-password/', views.user_password_change, name = 'user-password-change'),
]
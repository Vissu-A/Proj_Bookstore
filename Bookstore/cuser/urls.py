from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from cuser import views
from cuser.forms import CustomPasswordResestMailForm, CustomResetPasswordFrom, CustomPasswordChangeForm, CustomUserRegistrationForm

urlpatterns = [
    path('signup/', views.user_signup, name = 'user-signup-path'),
    path('usercreated/', views.user_signup_success, name = 'user-created-path'),
    path('activate/<uidb64>/<token>/', views.activate_account, name = 'activate-account-path'),
    path('signin/', views.user_signin, name = 'user-signin-path'),
    path('signout/', views.user_signout, name='user-signout-path'),
    path('info/', views.user_info, name='user-info-path'),
    path('info/<email>/', views.user_info, name='email-user-info'),
    path('edit/', views.user_edit, name='user-edit-path'),
    path('settings/', views.user_settings, name = 'user-account-settings'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='cuser/password_reset_mail.html', form_class=CustomPasswordResestMailForm), name='password_reset'),
    path('password-reset-mail-sent/', auth_views.PasswordResetDoneView.as_view(template_name='cuser/password_reset_mail_sent.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='cuser/password_reset_confirm_form.html', form_class=CustomResetPasswordFrom), name='password_reset_confirm'),
    path('password-reset-completed/', auth_views.PasswordResetCompleteView.as_view(template_name='cuser/password_reset_completed.html'), name='password_reset_complete'),

    # path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html', form_class=CustomPasswordChangeForm), name = 'password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    path('set-password/', views.set_user_password, name = 'set-user-password'),
    path('change-password/', views.user_password_change, name = 'password-change'),

    # Social auth url
    path('social-auth/', include('allauth.urls'), name='socialauth-signin-path'),

    path('test/', views.test_response, name = 'test-response'),
]
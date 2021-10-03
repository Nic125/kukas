from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('set-csrf/', views.set_csrf_token, name='Set-CSRF'),
    path('login/', views.user_login, name='login'),
    path('get-user/', views.get_user, name='get-user'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('user_unsubscribe/', views.user_unsubscribe, name='unsubscribe'),
    path('change_pass/', views.user_change_password, name='change-password'),
# Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
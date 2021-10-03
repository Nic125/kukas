from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    url(r'^', include('api.urls')),
    path('users/', include('login.urls')),


]

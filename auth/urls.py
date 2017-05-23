from django.conf.urls import url
from . import views
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as views_auth

from auth.forms import LoginForm
from house import settings

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views_auth.login, name='login'),
    url(r'^logout/$', views_auth.logout, {'next_page': '/login'}),
]
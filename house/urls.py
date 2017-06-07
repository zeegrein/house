"""house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from auth import views as core_views

from auth.forms import LoginForm
from house import settings

urlpatterns = [
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls, name='admin'),
    # url(r'^', include('designers.urls')),
    url(r'', include('auth.urls')),
    url(r'^masters/', include('masters.urls')),
    url(r'^designers/', include('designers.urls')),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^signup/$', core_views.signup, name='signup'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
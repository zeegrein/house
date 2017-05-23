from django.conf.urls import url

from . import views

app_name = 'designers'

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),
    url(r'^(?P<pk>[0-9]+)/price/$', views.PriceView.as_view(), name='price'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^export/(.*)', views.export_data, name="export")
]
# urlpatterns += [
#     url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
# ]
urlpatterns += [
    url(r'^create/$', views.DesignerCreate.as_view(), name='designer_create'),
    url(r'^creation/$', views.DesignerCreationView.as_view(), name='designer_creation'),
    url(r'^(?P<pk>\d+)/update/$', views.DesignerUpdate.as_view(), name='designer_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.DesignerDelete.as_view(), name='designer_delete'),
]
from django.conf.urls import url

from . import views

app_name = 'masters'
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^list/$', views.MainView.as_view(), name='main'),
    url(r'^(?P<pk>[0-9]+)/price/$', views.PriceView.as_view(), name='price'),
    url(r'^upload/$', views.upload, name='uplink'),
    url(r'^import/$', views.import_data, name='import'),
    url(r'^export/(.*)', views.export_data, name="export")
]
urlpatterns += [
    url(r'^create/$', views.MasterCreate.as_view(), name='master_create'),
    url(r'^(?P<pk>\d+)/update/$', views.MasterUpdate.as_view(), name='master_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.MasterDelete.as_view(), name='master_delete'),
    url(r'^creation/$', views.MasterCreationView.as_view(), name='master_creation'),
]
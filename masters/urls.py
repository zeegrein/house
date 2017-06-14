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
    url(r'^addons/$', views.AddonView.as_view(), name='addons'),
    url(r'^upload/$', views.upload, name='uplink'),
    url(r'^import/$', views.import_data, name='import'),
    url(r'^export/(.*)', views.export_data, name="export")
]
urlpatterns += [
    url(r'^create/$', views.MasterCreate.as_view(), name='master_create'),
    url(r'^(?P<pk>\d+)/update/$', views.MasterUpdate.as_view(), name='master_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.MasterDelete.as_view(), name='master_delete'),
    url(r'^creation/$', views.MasterCreationView.as_view(), name='master_creation'),
    url(r'^(?P<pk>\d+)/add_card/$', views.CardOfObjectForMasterView.as_view(), name='add_card'),
    url(r'^(?P<master_id>\d+)/edit_card/(?P<pk>[0-9]+)/$', views.CardOfObjectForMasterEditView.as_view(),
        name='edit_card'),
    url(r'^(?P<master_id>\d+)/delete_card/(?P<pk>[0-9]+)/$', views.CardOfObjectForMasterDeleteView.as_view(),
        name='delete_card'),
    url(r'^(?P<master_id>\d+)/upload_card_photo/(?P<pk>[0-9]+)/$', views.CardUploadView.as_view(),
        name='upload_card_photo'),
    url(r'^(?P<master_id>\d+)/card_photo/(?P<pk>[0-9]+)/$', views.CardPhotoView.as_view(),
        name='card_photo'),
    url(r'^(?P<master_id>\d+)/edit_card_photo/(?P<card_id>[0-9]+)/photo/(?P<pk>[0-9]+)$', views.CardPhotoEditView.as_view(),
        name='edit_card_photo'),
    url(r'^(?P<master_id>\d+)/delete_card_photo/(?P<card_id>[0-9]+)/photo/(?P<pk>[0-9]+)$', views.CardPhotoDeleteView.as_view(),
        name='delete_card_photo'),
]
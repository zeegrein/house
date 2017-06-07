from django.conf.urls import url

from . import views

app_name = 'designers'

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),
    url(r'^(?P<pk>[0-9]+)/price/$', views.PriceView.as_view(), name='price'),
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
    url(r'^(?P<pk>\d+)/add_card/$', views.CardOfObjectForDesignerView.as_view(), name='add_card'),
    url(r'^(?P<designer_id>\d+)/edit_card/(?P<pk>[0-9]+)/$', views.CardOfObjectForDesignerEditView.as_view(),
        name='edit_card'),
    url(r'^(?P<designer_id>\d+)/delete_card/(?P<pk>[0-9]+)/$', views.CardOfObjectForDesignerDeleteView.as_view(),
        name='delete_card'),
    url(r'^(?P<designer_id>\d+)/upload_card_picture/(?P<pk>[0-9]+)/$', views.BasicUploadView.as_view(),
        name='upload_card_picture'),
    url(r'^(?P<designer_id>\d+)/upload_card_photo/(?P<pk>[0-9]+)/$', views.CardUploadView.as_view(),
        name='upload_card_photo'),
    url(r'^(?P<designer_id>\d+)/card_photo/(?P<pk>[0-9]+)/$', views.CardPhotoView.as_view(),
        name='card_photo'),
    url(r'^(?P<designer_id>\d+)/edit_card_photo/(?P<card_id>[0-9]+)/photo/(?P<pk>[0-9]+)$', views.CardPhotoEditView.as_view(),
        name='edit_card_photo'),
    url(r'^(?P<designer_id>\d+)/delete_card_photo/(?P<card_id>[0-9]+)/photo/(?P<pk>[0-9]+)$', views.CardPhotoDeleteView.as_view(),
        name='delete_card_photo'),
]

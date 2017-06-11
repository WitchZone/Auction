from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lot_list, name='lot_list'),
    url(r'^$', views.lot_list, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^lot/(?P<pk>[0-9]+)/$', views.lot_detail, name='lot_detail'),
    url(r'^lot/new/$', views.lot_new, name='lot_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.lot_edit, name='lot_edit'),
]
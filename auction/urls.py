from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lot_list, name='lot_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^lot/(?P<pk>[0-9]+)/$', views.lot_detail, name='lot_detail'),
]
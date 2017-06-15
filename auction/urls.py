from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.lot_list, name='lot_list'),
    url(r'^$', views.lot_list, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^balance/$', views.user_balance, name='balance'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^lot/(?P<pk>[0-9]+)/$', views.lot_detail, name='lot_detail'),
    url(r'^lot/new/$', views.lot_new, name='lot_new'),
    url(r'^get_views/$', views.get_au_views, name='get_au_views'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.lot_edit, name='lot_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.lot_remove, name='lot_remove'),
    url(r'^user/(?P<user_id>\d+)/$', views.show_user, name='show_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lot_list, name='lot_list'),
]
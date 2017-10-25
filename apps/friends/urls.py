from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^profile/(?P<friend>\d+)$', views.profile),
    url(r'^remove/(?P<friend>\d+)$', views.unfriend),
    url(r'^add/(?P<friend>\d+)$', views.add),
    url(r'^add/(?P<friend>\d+)/redirect$', views.addredirect),
]
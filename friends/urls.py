"""friends URL Configuration"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^friends/', include('apps.friends.urls')),
    url(r'^', include('apps.login.urls')),
]
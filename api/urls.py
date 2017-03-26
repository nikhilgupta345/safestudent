from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^event/create$', views.event_create),
    url(r'^event/delete$', views.event_delete),

    url(r'^event/all$', views.event_all),
]

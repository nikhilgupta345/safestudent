"""safestudent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/v1/', include('api.urls')),

    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),

    url(r'^student/register/$', views.student_register),
    url(r'^student/(?P<student_id>[0-9]+)$', views.student_profile),

    url(r'^student/notifications/(?P<student_id>[0-9]+)/on/$', views.student_notifications_on),
    url(r'^student/notifications/(?P<student_id>[0-9]+)/off/$', views.student_notifications_off),

    url(r'^create_new_code$', views.create_new_code),
    url(r'^feed$', views.feed),

    url(r'^$', views.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

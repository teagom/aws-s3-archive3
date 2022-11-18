"""archive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from object.views import my_list, my_list_action
from object.api import show_compress_content

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mylist/$', login_required(my_list)),
    url(r'^mylist/action/$', login_required(my_list_action)),
    # media
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    # API object
    url(r'^api/(?P<obj_id>\d+)/(?P<search>[\s\S].*)/$', login_required(show_compress_content))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

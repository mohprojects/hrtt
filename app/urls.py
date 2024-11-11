"""hrtt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app import settings
from django.conf.urls.static import static
from django.urls import re_path, include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from backend.views import user_views

urlpatterns = [
    # url(r'', include('shrink.urls')),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),

    path('', include('backend.urls')),

    path('backend/', include('backend.urls')),
    re_path(r'^backend/$', user_views.signin, name='signin'),
    re_path(r'^service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    path('frontend/', include('frontend.urls')),
    re_path(r'^service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.FILES_URL, document_root=settings.FILES_ROOT)
    urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)


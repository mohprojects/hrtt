from django.urls import re_path

from backend.views import downloads_views

urlpatterns = [
    re_path(
        r"^downloads/template/(?P<name>.+)/$",
        downloads_views.template,
        name="download_template",
    ),
]

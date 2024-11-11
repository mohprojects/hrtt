from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import comments_views

urlpatterns = [
    # comments
    # path('', comments_views.index, name='index'),
    re_path(
        r"^comments/datatable/$",
        comments_views.AjaxCommentsListView.as_view(),
        name="comments_datatable_view",
    ),
    # create
    re_path(r"^comments/create/$", comments_views.create, name="comments_create"),
    re_path(
        r"^comments/create/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]

from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import implementers_views

urlpatterns = [
    # implementers
    # path('', implementers_views.index, name='index'),
    re_path(
        r"^implementers/datatable/$",
        implementers_views.AjaxImplementersListView.as_view(),
        name="implementers_datatable_view",
    ),
    # create
    re_path(r"^implementers/create/$", implementers_views.create, name="implementers_create"),
    re_path(
        r"^implementers/create/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),

    # fetch
    re_path(r"^implementers/fetch/$", implementers_views.get_all_implementers, name="implementers_fetch_all"),
    re_path(
        r"^implementers/fetch/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]

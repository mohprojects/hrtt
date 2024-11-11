from django.urls import re_path
from backend.views import mailing_server_configurations
from django.views.generic import TemplateView


urlpatterns = [
    re_path(
        r"^mail_configuration/configure/$",
        mailing_server_configurations.create,
        name="mail_configure",
    ),
    re_path(
        r"^mail_configuration/configure/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # view
    re_path(
        r"^mail_configuration/view/(?P<pk>.+)/$", mailing_server_configurations.view, name="mail_configuration_view"
    ),
    re_path(
        r"^mail_configuration/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]
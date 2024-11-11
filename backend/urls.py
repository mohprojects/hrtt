from django.urls import re_path

from backend.routes import (
    downloads,
    logs,
    notifications,
    settings,
    users,
    organizations,
    projects,
    activities,
    levels,
    fundings,
    reports,
    activities_inputs,
    comments,
    currency_rates,
    implementers,
    gdp_populations,
    system_reports,
    mailing_server_configurations,
    analysis
)

from backend.views import site_views

urlpatterns = [
    # site
    re_path(r"^site/contact/$", site_views.contact, name="site_contact"),
]

urlpatterns += settings.urlpatterns
urlpatterns += users.urlpatterns
urlpatterns += logs.urlpatterns
urlpatterns += notifications.urlpatterns
urlpatterns += downloads.urlpatterns
urlpatterns += organizations.urlpatterns
urlpatterns += projects.urlpatterns
urlpatterns += activities.urlpatterns
urlpatterns += levels.urlpatterns
urlpatterns += fundings.urlpatterns
urlpatterns += reports.urlpatterns
urlpatterns += activities_inputs.urlpatterns
urlpatterns += comments.urlpatterns
urlpatterns += currency_rates.urlpatterns
urlpatterns += implementers.urlpatterns
urlpatterns += gdp_populations.urlpatterns
urlpatterns += system_reports.urlpatterns
urlpatterns += mailing_server_configurations.urlpatterns
urlpatterns += analysis.urlpatterns

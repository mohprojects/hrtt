from django.urls import path

from frontend.views import site_views

urlpatterns = [
    path("", site_views.home, name="frontend_index"),
    path("home", site_views.home, name="frontend_home"),
    path("faq", site_views.faq, name="frontend_faq"),
    path("about", site_views.about, name="frontend_about"),
    path("contact", site_views.contact, name="frontend_contact"),
    # path('backend', site_views.backend, name='backend_index'),
]

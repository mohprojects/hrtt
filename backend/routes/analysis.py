from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import analysis_views
urlpatterns = [
    re_path(
        r"^analysis/index/$",
        analysis_views.index,
        name="analysis_index",
    ),
    re_path(
        r"^analysis/index/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    
    re_path(
        r"^analysis/get_data/$",
        analysis_views.get_data_for_analysis,
        name="analysis_get_data",
    ),
    re_path(
        r"^analysis/get_data/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # path('get-task-status/', views.get_task_status, name='get_task_status'),
   
]

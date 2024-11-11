from django.urls import re_path
from django.views.generic import TemplateView

from backend.views import setting_views


urlpatterns = [
    # settings
    re_path(r"^settings/$", setting_views.index, name="settings_index"),
    re_path(
        r"^settings/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # file upload
    re_path(r"^settings/upload/$", setting_views.temp_upload, name="temp_upload"),
    # qr code
    re_path(
        r"^settings/qrcode/(?P<size>\d+)/(?P<text>.+)/$",
        setting_views.get_qr_code_image,
        name="get_qr_code_image",
    ),
    # database update
    re_path(
        r"^settings/update-database/$",
        setting_views.update_database,
        name="settings_update_database",
    ),
    # database reset
    re_path(
        r"^settings/reset-database/$",
        setting_views.reset_database,
        name="settings_reset_database",
    ),
    # clear logs
    re_path(
        r"^settings/clear-logs/$", setting_views.clear_logs, name="settings_clear_logs"
    ),
    # reset users
    re_path(
        r"^settings/reset-users/$",
        setting_views.reset_users,
        name="settings_reset_users",
    ),
    # upload excel
    re_path(
        r"^settings/excel-import/$",
        setting_views.download_excel_view,
        name="settings_excel_import",
    ),
    re_path(
        r"^settings/excel-import/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # upload excel
    re_path(
        r"^settings/upload_hrtt/$",
        setting_views.read_hrtt_csv_format,
        name="upload_hrtt_csv_version",
    ),
    re_path(
        r"^settings/upload_hrtt/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    re_path(
        r"^settings/upload_rra/$",
        setting_views.read_rra_csv_format,
        name="upload_rra_csv_version",
    ),
    re_path(
        r"^settings/upload_rra/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    
    re_path(
        r"^settings/upload_ifmis/$",
        setting_views.read_ifmis_json_file,
        name="upload_ifmis_json_version",
    ),
    re_path(
        r"^settings/upload_rra/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]

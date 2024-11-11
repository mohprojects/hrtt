
from frontend.routes import site

urlpatterns = [
    # # site
    # re_path(r'^site/contact/$', site_views.contact, name='site_contact'),
    # # settings
    # re_path(r'^settings/$', setting_views.index, name='settings_index'),
    # re_path(r'^settings/service-worker.js',
    #     (TemplateView.as_view(template_name="service-worker/service-worker.js",
    #                           content_type='application/javascript', )),
    #     name='service-worker.js'),
    # # file upload
    # re_path(r'^settings/upload/$', setting_views.temp_upload, name='temp_upload'),
    # # qr code
    # re_path(r'^settings/qrcode/(?P<size>\d+)/(?P<text>.+)/$',
    #     setting_views.get_qr_code_image, name='get_qr_code_image'),
    # # database update
    # re_path(r'^settings/update-database/$', setting_views.update_database,
    #     name='settings_update_database'),
    # # upload excel
    # re_path(r'^settings/excel-import/$', setting_views.excel_import,
    #     name='settings_excel_import'),
    # re_path(r'^settings/excel-import/service-worker.js',
    #     (TemplateView.as_view(template_name="service-worker/service-worker.js",
    #                           content_type='application/javascript', )),
    #     name='service-worker.js'),
    # path('', include('api.urls')),
    # path('api/', include('api.urls')),
]

urlpatterns += site.urlpatterns

from django.urls import re_path, path
from django.views.generic import TemplateView

from backend.views import user_views

urlpatterns = [
    # users
    path("", user_views.index, name="index"),
    re_path(
        r"^users/datatable/$",
        user_views.AjaxUsersList.as_view(),
        name="users_datatable",
    ),
    # signup and confirmation
    # re_path(
    #     r"^users/signup/service-worker.js",user_views.signup
    #     (
    #         TemplateView.as_view(
    #             template_name="service-worker/service-worker.js",
    #             content_type="application/javascript",
    #         )
    #     ),
    #     name="service-worker.js",
    # ),
    re_path(
        r"^users/signup/confirm/(?P<token>.+)/$",
        user_views.confirm,
        name="users_signup_confirm",
    ),
    # signin
    re_path(r"^users/signin/$", user_views.signin, name="users_signin"),
    re_path(
        r"^users/signin/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # forgot password
    re_path(
        r"^users/forgot-password/$",
        user_views.forgot_password,
        name="users_forgot_password",
    ),
    re_path(
        r"^users/forgot-password/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # reset password
    re_path(
        r"^users/reset-password/(?P<token>.+)",
        user_views.reset_password,
        name="users_reset_password",
    ),
    # re_path(r'^users/reset-password/(?P<token>.+)/service-worker.js',
    #     (TemplateView.as_view(template_name="service-worker/service-worker.js",
    #                           content_type='application/javascript', )),
    #     name='service-worker.js'),
    # signout
    re_path(r"^users/signout/$", user_views.signout, name="users_signout"),
    # dashboard
    re_path(r"^users/dashboard/$", user_views.dashboard, name="users_dashboard"),
    re_path(
        r"^users/dashboard/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # index
    re_path(r"^users/json/$", user_views.json_users, name="json_users"),
    re_path(r"^users/index/$", user_views.index, name="users_index"),
    re_path(
        r"^users/index/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # single or multiple select
    re_path(
        r"^users/select-single/$", user_views.select_single, name="users_select_single"
    ),
    re_path(
        r"^users/select-multiple/$",
        user_views.select_multiple,
        name="users_select_multiple",
    ),
    # create
    re_path(r"^users/create/$", user_views.create, name="users_create"),
    re_path(
        r"^users/create/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # update
    re_path(r"^users/update/(?P<pk>.+)/$", user_views.update, name="users_update"),
    re_path(
        r"^users/update/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # update permissions
    re_path(
        r"^users/update-permissions/(?P<pk>.+)/$",
        user_views.update_permissions_view,
        name="users_update_permissions_view",
    ),
    re_path(
        r"^users/update-permissions/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    re_path(
        r"^users/update-permissions/$",
        user_views.update_permissions_action,
        name="users_update_permissions_action",
    ),
    # view
    re_path(r"^users/view/(?P<pk>.+)/$", user_views.view, name="users_view"),
    re_path(
        r"^users/view/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # profile-view
    re_path(
        r"^users/profile/view/$", user_views.profile_view, name="users_profile_view"
    ),
    re_path(
        r"^users/profile/view/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # profile-update
    re_path(
        r"^users/profile/update/$",
        user_views.profile_update,
        name="users_profile_update",
    ),
    re_path(
        r"^users/profile/update/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # profile-change-password
    re_path(
        r"^users/profile/change-password/$",
        user_views.profile_change_password,
        name="users_profile_change_password",
    ),
    re_path(
        r"^users/profile/change-password/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
    # update-reset-password
    re_path(
        r"^users/update-reset-password/(?P<pk>.+)/$",
        user_views.update_reset_password,
        name="users_update_reset_password",
    ),
    re_path(
        r"^users/update-reset-password/(?P<pk>.+)/service-worker.js",
        (
            TemplateView.as_view(
                template_name="service-worker/service-worker.js",
                content_type="application/javascript",
            )
        ),
        name="service-worker.js",
    ),
]

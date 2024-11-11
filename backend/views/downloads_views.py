import os
from django.http import HttpResponse, HttpResponseNotFound

from app import settings
from app.models.methods.users import Methods_Users
from app.models.users import Users


# Create your views here.
def template(request, name):
    user = Users.login_required(request)
    if user is None:
        return HttpResponse("signin", content_type="text/plain")
    Methods_Users.get_auth_permissions(user)
    try:
        filepath = settings.MEDIA_ROOT + "downloads/" + str(name)
        filename, file_extension = os.path.splitext(filepath)
        with open(filepath, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/x-gzip")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                filepath
            )
            return response

    except FileNotFoundError:
        return HttpResponseNotFound("Not Found", content_type="text/plain")


def contact(request):
    return HttpResponse("For support please contact us at support@qtsoftwareltd.com")

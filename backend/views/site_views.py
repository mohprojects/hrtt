from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def contact(request):
    return HttpResponse("For support please contact us at support@qtsoftwareltd.com")

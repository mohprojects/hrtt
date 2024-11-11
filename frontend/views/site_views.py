from app import settings
from django.shortcuts import redirect, render
from django.urls import reverse

TEMPLATE_PATH = settings.TEMPLATE_PATH_FRONTEND


def home(request):
    template_url = TEMPLATE_PATH + "site/home.html"
    return render(request, template_url)


def faq(request):
    template_url = TEMPLATE_PATH + "site/faq.html"
    return render(request, template_url)


def about(request):
    template_url = TEMPLATE_PATH + "site/about.html"
    return render(request, template_url)


def contact(request):
    template_url = TEMPLATE_PATH + "site/contact.html"
    return render(request, template_url)


def backend(request):
    return redirect(reverse("users_signin"))

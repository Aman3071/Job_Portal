from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("jobs/", include("jobs.urls")),
    path("accounts/", include("accounts.urls")),
    path("", home, name="home"),
]
    
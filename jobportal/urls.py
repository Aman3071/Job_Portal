from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("jobs/", include("jobs.urls")),
    path("accounts/", include("accounts.urls")),
    path("", home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

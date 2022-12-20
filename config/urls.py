from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path("accounts/", include("accounts.api.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/", include((api_urlpatterns, "api_apps"), namespace="api")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

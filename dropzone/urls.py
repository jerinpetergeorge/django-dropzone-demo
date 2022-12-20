from django.urls import path

from . import views

urlpatterns = [
    path("", views.DropzoneRenderView.as_view()),
    path("upload/", views.DropzoneUploadView.as_view(), name="upload"),
]

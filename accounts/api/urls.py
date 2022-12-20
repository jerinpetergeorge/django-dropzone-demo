from django.urls import path

from .views import UserDetailAPIView

app_name = "accounts"
urlpatterns = [
    path("user-details/", UserDetailAPIView.as_view(), name="user-details"),
]

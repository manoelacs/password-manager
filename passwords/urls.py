from django.urls import path
from passwords import views as view

app_name = "passwords"
urlpatterns = [
    path("register/", view.RegisterView.as_view(), name="register"),
    path("passwords/", view.PasswordEntryView.as_view(), name="passwords"),
    path(
        "password/<int:pk>/",
        view.PasswordEntryViewDetail.as_view(),
        name="password",
    ),
]

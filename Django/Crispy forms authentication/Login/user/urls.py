from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('sign_in', views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),

    path(
            "reset_password/",
            auth_views.PasswordResetView.as_view(
                template_name="login/password_reset.html"
            ),
            name="reset_password",
        ),
    path(
            "reset_password_sent/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="login/password_reset_sent.html"
        ),
            name="password_reset_done",
        ),
    path(
            "reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="login/password_reset_form.html"
            ),
            name="password_reset_confirm",
    ),
    path(
            "reset_password_complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="login/password_reset_done.html"
            ),
            name="password_reset_complete",
    ),
]
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_request, name="signup"),
    path("two-factor/setup/", views.two_factor_setup, name="2fa_setup"),

    # A logged-in staff member changing their password voluntarily (or
    # because the password-expiry middleware sent them here).
    path("password_change/", views.StampingPasswordChangeView.as_view(
        template_name="accounts/password_change_form.html",
    ), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html",
    ), name="password_change_done"),

    # Setting a password from an invite/bootstrap link, or a self-service
    # "forgot password" — both use the same uidb64/token confirm flow.
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/accounts/password_reset/done/",
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.StampingPasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html",
    ), name="password_reset_complete"),
]

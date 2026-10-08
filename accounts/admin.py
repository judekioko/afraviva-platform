from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_otp.plugins.otp_totp.models import TOTPDevice

from .models import SignupRequest, StaffProfile

STAFF_GROUP_NAME = "Staff"


def _build_set_password_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    # Absolute afraviva.com link regardless of which subdomain the admin
    # happens to be acting from — accounts/ only exists in the main urlconf.
    return f"https://afraviva.com/accounts/reset/{uid}/{token}/"


@admin.register(SignupRequest)
class SignupRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "status", "requested_at", "reviewed_by")
    list_filter = ("status",)
    search_fields = ("full_name", "email")
    readonly_fields = ("requested_at", "reviewed_at", "reviewed_by")
    actions = ["approve_requests", "reject_requests"]

    def has_add_permission(self, request):
        # Staff accounts are only ever created through the public request
        # form + approval flow, never typed directly into this list.
        return False

    @admin.action(description="Approve selected requests (creates the staff account and emails an invite)")
    def approve_requests(self, request, queryset):
        User = get_user_model()
        staff_group, _ = Group.objects.get_or_create(name=STAFF_GROUP_NAME)
        approved = 0
        for signup in queryset.filter(status=SignupRequest.STATUS_PENDING):
            if User.objects.filter(email__iexact=signup.email).exists():
                self.message_user(
                    request, f"Skipped {signup.email} — a user with that email already exists.",
                    level=messages.WARNING,
                )
                continue

            first_name, _, last_name = signup.full_name.partition(" ")
            user = User(
                username=signup.email, email=signup.email,
                first_name=first_name[:150], last_name=last_name[:150],
                is_staff=True, is_superuser=False, is_active=True,
            )
            user.set_unusable_password()
            user.save()
            user.groups.add(staff_group)
            StaffProfile.objects.create(user=user)

            link = _build_set_password_link(user)
            send_mail(
                subject=render_to_string("accounts/invite_email_subject.txt", {}).strip(),
                message=render_to_string("accounts/invite_email_body.txt", {
                    "full_name": signup.full_name, "link": link,
                }),
                from_email=settings.EMAIL_HOST_USER or "noreply@afraviva.com",
                recipient_list=[signup.email],
                fail_silently=True,
            )

            signup.status = SignupRequest.STATUS_APPROVED
            signup.reviewed_at = timezone.now()
            signup.reviewed_by = request.user
            signup.save(update_fields=["status", "reviewed_at", "reviewed_by"])
            approved += 1

        if approved:
            self.message_user(request, f"Approved {approved} request(s) and emailed set-password instructions.")

    @admin.action(description="Reject selected requests")
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status=SignupRequest.STATUS_PENDING).update(
            status=SignupRequest.STATUS_REJECTED, reviewed_at=timezone.now(), reviewed_by=request.user,
        )
        self.message_user(request, f"Rejected {updated} request(s).")


class StaffUserAdmin(UserAdmin):
    """Adds a "Two-step login" column, so it's clear who still needs to set
    up an authenticator before ADMIN_REQUIRE_2FA can be switched on."""

    list_display = UserAdmin.list_display + ("has_two_step_login",)

    @admin.display(boolean=True, description="Two-step login")
    def has_two_step_login(self, user):
        return TOTPDevice.objects.filter(user=user, confirmed=True).exists()


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), StaffUserAdmin)

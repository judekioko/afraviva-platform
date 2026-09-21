from django.conf import settings
from django.db import models


class SignupRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+",
    )

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.full_name} <{self.email}> ({self.status})"


class StaffProfile(models.Model):
    """Extra per-user bookkeeping that doesn't belong on auth.User itself —
    created automatically when a SignupRequest is approved (see admin.py).
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    password_changed_at = models.DateTimeField(
        null=True, blank=True,
        help_text="Stamped whenever this user sets/changes their password — drives password-expiry.",
    )

    def __str__(self):
        return f"Profile for {self.user}"

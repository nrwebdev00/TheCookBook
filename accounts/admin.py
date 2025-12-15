from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    ordering = ("-created_at",)
    list_display = ("email", "name", "is_email_verified", "is_staff", "is_active", "created_at")
    list_filter = ("is_email_verified", "is_staff", "is_active", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "client_id")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_email_verified", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("client_id", "created_at", "updated_at")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2"),
        }),
    )
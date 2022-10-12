from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ["updated_at", "date_joined", "updated_at"]
    fieldsets = (
        ("Credentials", {"fields": ("username", "password", "email")}),
        ("Personal info", {"fields": ("first_name", "last_name",
                                      "birthdate", "bio")}),
        ("Authorizations", {
            "fields": ("is_critic", "is_staff", "is_superuser")}),
        ("Dates", {"fields": ("date_joined", "updated_at")}),
    )


admin.site.register(User, CustomUserAdmin)

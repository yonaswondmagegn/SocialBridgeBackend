from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseAdmin):
    fieldsets = (
        (None, {"fields": ["phonenumber"]}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
     
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ["phonenumber"],
            },
        ),
    )

    list_display = ("phonenumber", "first_name", "last_name", "is_staff")
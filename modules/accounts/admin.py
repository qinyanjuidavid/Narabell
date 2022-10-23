from django.contrib import admin
from django.contrib.auth.models import Group

from modules.accounts.models import User
from modules.accounts.models import Administrator
from v2.modules.accounts.models import Reader


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "role",
        "is_active",
        "is_admin",
        "timestamp",
        "updated_at",
    ]
    list_filter = ["is_admin", "is_active", "is_staff", "role"]
    search_fields = ["email", "full_name"]
    readonly_fields = ["counter"]


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    pass


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    pass

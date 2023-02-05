from django.contrib import admin
from django.contrib.auth.models import Group

from modules.accounts.models import User, Administrator, Reader


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
@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display=("get_full_name","get_email","get_phone","get_active","country","get_timestamp")

    def get_timestamp(self, obj):
        return obj.user.timestamp

    get_timestamp.short_description = "Timestamp"
    get_timestamp.admin_order_field = "user__timestamp"

    def get_active(self, obj):
        return obj.user.is_active

    get_active.short_description = "Active"
    get_active.admin_order_field = "user__is_active"

    def get_full_name(self, obj):
        return obj.user.full_name

    get_full_name.short_description = "Full name"
    get_full_name.admin_order_field = "user__full_name"

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

    def get_phone(self, obj):
        return obj.user.phone

    get_phone.short_description = "Phone"
    get_phone.admin_order_field = "user__phone"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalAdmin
from django.utils.translation import gettext_lazy as _
from app.models import *

class CustomUserAdmin(OriginalAdmin):
    list_display = ('username', 'email', 'date_joined',)
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","user_type","phone_number")}),
        (
            _("Permissions"),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ('date_joined', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

class TruckAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'driver', 'capacity', 'is_reserved','is_available','date_added')
    list_filter = ('plate_number', 'driver', 'capacity')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reserved_by','product_name','quantity','is_delivered','truck','reservation_type','date_reserved', 'date_added')
    list_filter = ('is_delivered', 'truck','reservation_type')


admin.site.register(TruckModel, TruckAdmin)
admin.site.register(ReservationModel, ReservationAdmin)
admin.site.register(CustomUserModel, CustomUserAdmin)
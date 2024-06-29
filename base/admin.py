from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class UserAdminConfig(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password','accountType')}),
        ('Personal info', {'fields': ('name', 'phone_num')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active', 'accountType'),
        }),
    )
    list_display = ('email', 'name', 'is_staff', 'accountType')
    search_fields = ('email', 'name')
    ordering = ('email',)
    

admin.site.register(User, UserAdminConfig)
admin.site.register(Venue, list_display = ("id", "venueName"))
admin.site.register(Court)
admin.site.register(Booking)
admin.site.register(BookingCourt)
admin.site.register(Event)
admin.site.register(Holiday, list_display = ("holidayName","holidayDate"))
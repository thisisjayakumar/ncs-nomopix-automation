from django.contrib import admin
from .models import User, Organization, AdSection


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'organisation', 'created_at', 'subscription')
    list_filter = ('user_type', 'subscription', 'created_at')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    search_fields = ('name',)


@admin.register(AdSection)
class AdSectionAdmin(admin.ModelAdmin):
    list_display = ('ad_name', 'url', 'ad_type', 'publisher')
    list_filter = ('ad_type',)
    search_fields = ('ad_name', 'publisher')

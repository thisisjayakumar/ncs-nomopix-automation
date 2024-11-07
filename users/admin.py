from django.contrib import admin
from .models import User, Organization, AdSection


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'subscription')
    list_filter = ('user_type', 'subscription')
    raw_id_fields = ('organisation', )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    search_fields = ('name',)


@admin.register(AdSection)
class AdSectionAdmin(admin.ModelAdmin):
    list_display = ('ad_name', 'url', 'ad_type', 'publisher')
    list_filter = ('ad_type',)
    search_fields = ('ad_name', 'publisher')

from django.contrib import admin
from django.utils.html import format_html

from .models import User, Organization, AdSection, UserFeedback


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'subscription', 'is_active')
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


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'organisation', 'short_feedback',
                    'rating_stars', 'status_badge', 'created_at')

    def short_feedback(self, obj):
        return obj.feedback[:50] + '...' if len(obj.feedback) > 50 else obj.feedback

    short_feedback.short_description = 'Feedback'

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FFD700;">{}</span>', stars)

    rating_stars.short_description = 'Rating'

    def status_badge(self, obj):
        if obj.is_admin:
            color = 'purple'
            text = 'Admin'
        elif obj.is_active:
            color = 'green'
            text = 'Active'
        else:
            color = 'red'
            text = 'Inactive'

        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; '
            'border-radius: 10px;">{}</span>', color, text
        )

    status_badge.short_description = 'Status'
from django.contrib import admin

from selenium_headless_browser.models import CodeLogHistory


@admin.register(CodeLogHistory)
class CodeLogHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'major_code')
    search_fields = ('major_code',)
    raw_id_fields = ('user',)

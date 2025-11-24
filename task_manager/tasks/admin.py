from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'executor', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'labels', 'executor')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    filter_horizontal = ('labels',)
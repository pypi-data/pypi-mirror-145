from django.contrib import admin
from .models import TaskQueue


@admin.register(TaskQueue)
class TaskQueueAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'article', 'date_time', 'created_on', 'updated_on']
    ordering = ['date_time']
    readonly_fields = ['id', 'article', 'status']
    list_filter = ['status']


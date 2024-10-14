from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'due_date', 'owner', 'is_completed')
    search_fields =['owner', 'title', 'description']
    list_filter = ('is_completed', 'created_at', 'due_date')
    ordering = ('-created_at',)

admin.site.register(Task, TaskAdmin)

# Register your models here.

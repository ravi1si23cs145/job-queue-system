from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'status', 'retry_count', 'created_at')
    list_filter = ('status',)

    class Media:
        css={
            "all": ("admin/custom.css",)
        }
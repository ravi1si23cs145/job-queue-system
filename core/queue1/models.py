import uuid
from django.db import models

class Job(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('DLQ', 'Dead Letter Queue'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    job_type = models.CharField(max_length=50)

    payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_index=True
    )

    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)

    scheduled_at = models.DateTimeField(db_index=True)

    locked_by = models.CharField(max_length=100, null=True, blank=True)
    lock_expiry = models.DateTimeField(null=True, blank=True)

    last_error = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_type} | {self.status}"

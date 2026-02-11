from rest_framework import serializers
from .models import Job
from django.utils import timezone


class JobCreateSerializer(serializers.ModelSerializer):

    scheduled_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Job
        fields = ['job_type', 'payload', 'scheduled_at']

    def create(self, validated_data):
        if 'scheduled_at' not in validated_data:
            validated_data['scheduled_at'] = timezone.now()

        return Job.objects.create(
            status='PENDING',
            retry_count=0,
            max_retries=3,
            **validated_data
        )

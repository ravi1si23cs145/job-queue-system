import time
import random
from django.utils import timezone
from django.db import transaction
from queue1.models import Job


def process_job(job):
    """
    Simulated job execution logic
    """
    print(f"Processing job {job.id} (type: {job.job_type})")

    # simulate work
    time.sleep(2)

    # randomly succeed or fail
    return random.choice([True, False])


def run_worker():
    print("Worker started...")

    while True:
        with transaction.atomic():
            job = (
                Job.objects
                .select_for_update(skip_locked=True)
                .filter(status='PENDING', scheduled_at__lte=timezone.now())
                .first()
            )

            if not job:
                print("No pending jobs. Sleeping...")
                time.sleep(5)
                continue

            job.status = 'RUNNING'
            job.locked_at = timezone.now()
            job.save()

        # Process outside transaction
        success = process_job(job)

        with transaction.atomic():
            job.refresh_from_db()

            if success:
                job.status = 'SUCCESS'
                print(f"Job {job.id} completed successfully.")
            else:
                job.retry_count += 1
                if job.retry_count >= job.max_retries:
                    job.status = 'FAILED'
                    print(f"Job {job.id} permanently failed.")
                else:
                    job.status = 'PENDING'
                    print(f"Retrying job {job.id} (retry {job.retry_count})")

            job.save()
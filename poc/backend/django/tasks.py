from celery import shared_task
from django.db import IntegrityError, transaction
from .models import ProcessedEvent, Execution

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def process_hook_event(self, workflow_id, event_id, payload):
    # UniqueConstraint(workflow, event_id) is the source of truth, not Celery delivery.
    try:
        with transaction.atomic():
            ProcessedEvent.objects.create(workflow_id=workflow_id, event_id=event_id)
            Execution.objects.create(workflow_id=workflow_id, input_payload=payload)
    except IntegrityError:
        return "duplicate"
    return "processed"

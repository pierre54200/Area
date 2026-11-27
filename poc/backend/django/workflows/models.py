import uuid

from django.conf import settings
from django.db import models


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workflows",
    )
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProcessedEvent(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=255)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "event_id"],
                name="unique_workflow_event",
            )
        ]


class Execution(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    input_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

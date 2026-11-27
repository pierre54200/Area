from django.contrib import admin

from .models import Execution, ProcessedEvent, Workflow

admin.site.register(Workflow)
admin.site.register(ProcessedEvent)
admin.site.register(Execution)

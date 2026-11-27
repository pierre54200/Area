INSTALLED_APPS += [
    "rest_framework", "drf_spectacular",
    "allauth", "allauth.account", "allauth.socialaccount",
    "allauth.socialaccount.providers.openid_connect",
]
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "AREA POC API",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

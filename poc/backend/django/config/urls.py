from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from workflows.views import (
    LoginView,
    RegisterView,
    WorkflowEnabledView,
    WorkflowListView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register", RegisterView.as_view()),
    path("api/auth/login", LoginView.as_view()),
    path("api/workflows", WorkflowListView.as_view()),
    path(
        "api/workflows/<uuid:id>/enabled",
        WorkflowEnabledView.as_view(),
    ),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

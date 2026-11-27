from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WorkflowList(APIView):
    def get(self, request):
        return Response([])
    def post(self, request):
        # Replace with serializer + transactional workflow validation.
        return Response({"id": "poc-workflow"}, status=status.HTTP_201_CREATED)

urlpatterns = [
    path("api/workflows", WorkflowList.as_view()),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

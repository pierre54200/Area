from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Workflow
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RegisterResponseSerializer,
    TokenResponseSerializer,
    WorkflowSerializer,
    CreateWorkflowSerializer,
    WorkflowEnabledSerializer,
    WorkflowEnabledResponseSerializer,
    ErrorSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="register",
        auth=[],
        request=RegisterSerializer,
        responses={201: RegisterResponseSerializer, 400: ErrorSerializer},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if User.objects.filter(username=data["username"]).exists():
            return Response(
                {"detail": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=data["username"],
            email=data.get("email", ""),
            password=data["password"],
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"id": user.pk, "username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="login",
        auth=[],
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            401: ErrorSerializer,
            400: ErrorSerializer,
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class WorkflowListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="listWorkflows",
        responses={200: WorkflowSerializer(many=True)},
    )
    def get(self, request):
        workflows = Workflow.objects.filter(owner=request.user)
        return Response(WorkflowSerializer(workflows, many=True).data)

    @extend_schema(
        operation_id="createWorkflow",
        request=CreateWorkflowSerializer,
        responses={201: WorkflowSerializer, 400: ErrorSerializer},
    )
    def post(self, request):
        serializer = CreateWorkflowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = Workflow.objects.create(
            owner=request.user,
            name=serializer.validated_data["name"],
        )

        return Response(
            WorkflowSerializer(workflow).data,
            status=status.HTTP_201_CREATED,
        )


class WorkflowEnabledView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="setWorkflowEnabled",
        request=WorkflowEnabledSerializer,
        responses={
            200: WorkflowEnabledResponseSerializer,
            400: ErrorSerializer,
            404: ErrorSerializer,
        },
    )
    def patch(self, request, id):
        workflow = get_object_or_404(
            Workflow,
            id=id,
            owner=request.user,
        )

        serializer = WorkflowEnabledSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow.enabled = serializer.validated_data["enabled"]
        workflow.save(update_fields=["enabled"])

        return Response(
            {
                "id": workflow.id,
                "enabled": workflow.enabled,
            }
        )

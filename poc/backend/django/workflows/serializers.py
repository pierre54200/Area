from rest_framework import serializers

from .models import Workflow


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class RegisterResponseSerializer(TokenResponseSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ["id", "name", "enabled", "created_at"]
        read_only_fields = ["id", "enabled", "created_at"]


class CreateWorkflowSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class WorkflowEnabledSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class WorkflowEnabledResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    enabled = serializers.BooleanField()

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ModelSerializer
from typing import Type

from .serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return UserListSerializer

        return UserSerializer

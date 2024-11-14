from typing import Type

from django.db import models
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ModelSerializer

from .models import Company
from .permissions import IsAuthorOrReadOnly
from .serializers import CompanyListSerializer, CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Company.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return CompanyListSerializer

        return CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(models.Q(visible=True) | models.Q(owner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

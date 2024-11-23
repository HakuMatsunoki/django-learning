from typing import Type

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from company.models import Invite, Request

from .serializers import InviteSerializer, RequestSerializer, UserListSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return UserListSerializer

        return UserSerializer


class InvitationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invite.objects.filter(guest=self.request.user)


class RequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

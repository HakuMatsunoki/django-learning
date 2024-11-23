import hashlib
import secrets
from enum import Enum
from typing import Type

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from accounts.models import UserModel

from .models import Company, Invite, InviteStatuses, Request, RequestStatuses
from .permissions import IsAuthorOrReadOnly
from .serializers import CompanyListSerializer, CompanySerializer, InviteSerializer, RequestSerializer


class InviteActionEnum(str, Enum):
    SEND = "send"
    REVOKE = "revoke"
    ACCEPT = "accept"
    DECLINE = "decline"


class RequestActionEnum(str, Enum):
    SEND = "send"
    CANCEL = "cancel"
    APPROVE = "approve"
    REJECT = "reject"


class GuestActionEnum(str, Enum):
    REMOVE = "remove"
    LEAVE = "leave"


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

    @action(methods=["post"], detail=True)
    def invite(self, request, pk=None):
        action = request.data["action"]

        if action not in InviteActionEnum.__members__.values():
            return Response({"status": "failed", "msg": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        if action == InviteActionEnum.SEND:
            guest = get_object_or_404(UserModel, id=request.data["guest"])
            company = get_object_or_404(Company, id=pk)
            token = secrets.token_hex(32)
            token_bytes = bytes.fromhex(token)
            token_hash = hashlib.sha256(token_bytes).hexdigest()

            if company.owner != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

            invite = Invite.objects.create(
                company=company,
                guest=guest,
                token=token_hash,
            )

            subject = "Invite Email"
            message = f"This is invite from {company.name} company. Use this token to approve your invitation: {token}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [guest.email]

            send_mail(subject, message, from_email, recipient_list)

        elif action == InviteActionEnum.REVOKE:
            invite = get_object_or_404(Invite, id=request.data["invite"])

            if invite.company.owner != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

            if invite.status == InviteStatuses.CANCELED:
                return Response(
                    {"status": "failed", "msg": "Invite already canceled.."}, status=status.HTTP_400_BAD_REQUEST
                )

            invite.status = InviteStatuses.CANCELED
            invite.save()

        else:
            token_bytes = bytes.fromhex(request.data["token"])
            token_hash = hashlib.sha256(token_bytes).hexdigest()
            invite = get_object_or_404(Invite, token=token_hash)

            if invite.guest != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden.."}, status=status.HTTP_403_FORBIDDEN)

            if invite.status != InviteStatuses.PENDING:
                return Response({"status": "failed", "msg": "Invite invalid.."}, status=status.HTTP_400_BAD_REQUEST)

            if action == InviteActionEnum.ACCEPT:
                invite.company.guests.add(self.request.user)
                invite.status = InviteStatuses.ACCEPTED
            else:
                invite.status = InviteStatuses.DECLINED

            invite.save()

        return Response({"status": "ok", "invite": invite.id})

    @action(methods=["post"], detail=True)
    def request(self, request, pk=None):
        action = request.data["action"]

        if action not in RequestActionEnum.__members__.values():
            return Response({"status": "failed", "msg": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        if action == RequestActionEnum.SEND:
            company = get_object_or_404(Company, id=pk)
            join_request = Request.objects.create(company=company, user=self.request.user)
            subject = "Request Email"
            message = f"User {self.request.user} requested to join your company {company.name}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [company.owner.email]

            send_mail(subject, message, from_email, recipient_list)

        elif action == RequestActionEnum.CANCEL:
            join_request = get_object_or_404(Request, id=request.data["request"])

            if join_request.user != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

            if join_request.status == RequestStatuses.CANCELED:
                return Response(
                    {"status": "failed", "msg": "Request already canceled.."}, status=status.HTTP_400_BAD_REQUEST
                )

            join_request.status = RequestStatuses.CANCELED

            join_request.save()

        else:
            join_request = get_object_or_404(Request, id=request.data["request"])

            if join_request.company.owner != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden.."}, status=status.HTTP_403_FORBIDDEN)

            if join_request.status != InviteStatuses.PENDING:
                return Response({"status": "failed", "msg": "Request invalid.."}, status=status.HTTP_400_BAD_REQUEST)

            if action == RequestActionEnum.APPROVE:
                join_request.company.guests.add(join_request.user)
                join_request.status = RequestStatuses.APPROVED
            else:
                join_request.status = RequestStatuses.REJECTED

            join_request.save()

        return Response({"status": "ok", "request": join_request.id})

    @action(methods=["post", "get"], detail=True, url_path="guests")
    def guest(self, request, pk=None):
        if request.method == "GET":
            company = self.get_object()
            users = company.guests.all()

            return Response({"users": [{"id": user.id, "name": user.username} for user in users]})

        action = request.data["action"]
        company = get_object_or_404(Company, id=pk)

        if action not in GuestActionEnum.__members__.values():
            return Response({"status": "failed", "msg": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        if action == GuestActionEnum.REMOVE:
            guest = get_object_or_404(UserModel, id=request.data["guest"])

            if company.owner != self.request.user:
                return Response({"status": "failed", "msg": "Forbidden.."}, status=status.HTTP_403_FORBIDDEN)

            company.guests.remove(guest)

        if action == GuestActionEnum.LEAVE:
            company.guests.remove(self.request.user)

        return Response({"status": "ok"})


class InvitationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invite.objects.filter(company__owner=self.request.user)


class RequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Request.objects.filter(company__owner=self.request.user)

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Company


class CompanyTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(
            username="owner",
            email="owner@example.com",
            password="secret",
        )
        cls.guest = get_user_model().objects.create_user(
            username="guest",
            email="guest@example.com",
            password="secret",
        )
        cls.company = Company.objects.create(
            owner=cls.owner,
            name="Quentin&Co",
            description="Huge and awesome company",
        )

    def _authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def _make_invite_request(self, data):
        url = reverse("companies-invite", kwargs={"pk": self.company.id})

        return self.client.post(url, data)

    def _make_request_request(self, data):
        url = reverse("companies-request", kwargs={"pk": self.company.id})

        return self.client.post(url, data)

    def _send_invitation(self):
        self._authenticate(self.owner)

        return self._make_invite_request({"action": "send", "guest": self.guest.id})

    def _accept_invitation(self):
        self._send_invitation()
        self._authenticate(self.guest)

        token = mail.outbox[0].body.split(": ")
        response = self._make_invite_request({"action": "accept", "token": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.guest, self.company.guests.all())

        return self.company.guests.all()[0]

    def _send_request(self):
        self._authenticate(self.guest)

        return self._make_request_request({"action": "send"})

    def test_send_inviation(self):
        response = self._send_invitation()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox[0].subject, "Invite Email")

    def test_accept_invitation(self):
        self._accept_invitation()

    def test_decline_invitation(self):
        self._send_invitation()
        self._authenticate(self.guest)

        token = mail.outbox[0].body.split(": ")
        response = self._make_invite_request({"action": "decline", "token": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.guest, self.company.guests.all())

    def test_revoke_invitation(self):
        invite_response = self._send_invitation().json()
        token = mail.outbox[0].body.split(": ")
        revoke_response = self._make_invite_request({"action": "revoke", "invite": invite_response["invite"]})

        self.assertEqual(revoke_response.status_code, status.HTTP_200_OK)
        self._authenticate(self.guest)

        accept_response = self._make_invite_request({"action": "accept", "token": token})

        self.assertEqual(accept_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.guest, self.company.guests.all())

    def test_remove_user(self):
        joined_guest = self._accept_invitation()

        self._authenticate(self.owner)

        url = reverse("companies-guest", kwargs={"pk": self.company.id})

        self.client.post(url, {"action": "remove", "guest": joined_guest.id})
        self.assertNotIn(self.guest, self.company.guests.all())

    def test_send_request(self):
        response = self._send_request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mail.outbox[0].subject, "Request Email")

        mail_body_list = mail.outbox[0].body.split("User ")[1].split(" requested to join your company ")

        self.assertEqual(mail_body_list[0], self.guest.username)
        self.assertEqual(mail_body_list[1], self.company.name)

    def test_approve_request(self):
        response = self._send_request().json()

        self._authenticate(self.owner)
        self._make_request_request({"action": "approve", "request": response["request"]})
        self.assertIn(self.guest, self.company.guests.all())

    def test_cancel_request(self):
        response = self._send_request().json()

        self._make_request_request({"action": "cancel", "request": response["request"]})
        self._authenticate(self.owner)

        approve_response = self._make_request_request({"action": "approve", "request": response["request"]})

        self.assertEqual(approve_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.guest, self.company.guests.all())

    def test_reject_request(self):
        response = self._send_request().json()

        self._authenticate(self.owner)

        reject_response = self._make_request_request({"action": "reject", "request": response["request"]})

        self.assertEqual(reject_response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.guest, self.company.guests.all())

    def test_leave_company(self):
        self._accept_invitation()
        self.assertIn(self.guest, self.company.guests.all())
        self._authenticate(self.guest)

        url = reverse("companies-guest", kwargs={"pk": self.company.id})

        self.client.post(url, {"action": "leave"})
        self.assertNotIn(self.guest, self.company.guests.all())

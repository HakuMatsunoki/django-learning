from django.test import TestCase
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class ApiTests(TestCase):
    def test_check_health(self):
        response = self.client.get(reverse("check_health"), format="json")
        expect = {"status_code": 200, "detail": "ok", "result": "working"}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data, expect)

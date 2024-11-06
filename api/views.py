import logging

from django.core.cache import cache
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CheckHealthView(APIView):
    logger = logging.getLogger("django")

    def get(self, request: Request) -> Response:
        cached_result = cache.get("json_key")

        if cached_result:
            self.logger.info("cache used")

            return Response(cached_result)

        result = {"status_code": 200, "detail": "ok", "result": "working"}
        cache.set("json_key", result, 30)
        self.logger.info("fresh response")

        return Response(result)

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import redis


# Create your views here.
class CheckHealthView(APIView):
    cache = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True, db=0
    )

    def get(self, request):
        cached_result = self.cache.hgetall("json_key")

        if cached_result:
            return Response(cached_result)

        result = {"status_code": 200, "detail": "ok", "result": "working"}
        self.cache.hmset("json_key", result)

        return Response(result)

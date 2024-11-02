from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache


# Create your views here.
class CheckHealthView(APIView):
    def get(self, request):
        cached_result = cache.get("json_key")

        if cached_result:
            return Response(cached_result)

        result = {"status_code": 200, "detail": "ok", "result": "working"}
        cache.set("json_key", result, 30)

        return Response(result)

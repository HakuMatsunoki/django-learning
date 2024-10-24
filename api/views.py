from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CheckHealthView(APIView):
    def get(self, request):
        return Response({"status_code": 200, "detail": "ok", "result": "working"})

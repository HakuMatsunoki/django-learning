from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request) -> Response:
        queryset = get_user_model().objects.all().order_by("created_at")
        paginator = Paginator(queryset, 3)
        page_number = request.GET.get("page", 1)

        try:
            queryset = paginator.page(page_number)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = UserListSerializer(queryset, many=True)
        response_data = {"total": paginator.count, "users": serializer.data}

        return Response(response_data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, pk: int = None) -> Response:
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: int = None) -> Response:
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

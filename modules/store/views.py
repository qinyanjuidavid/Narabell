from django.shortcuts import get_object_or_404
from modules.accounts.paginations import StandardResultsSetPagination
from modules.store.models import Author, Genre, Publisher
from modules.store.serializers import (
    AuthorSerializer,
    GenreSerializer,
    PublisherSerializer,
)
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from rest_framework import generics, serializers, status, viewsets


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = []
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query),
            )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.method == "GET":
            if len(queryset) > 0:
                paginator = StandardResultsSetPagination()
                result_page = paginator.paginate_queryset(queryset, request)
                serializer = self.get_serializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(
                    {"message": "No author found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = []
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query),
            )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.method == "GET":
            if len(queryset) > 0:
                paginator = StandardResultsSetPagination()
                result_page = paginator.paginate_queryset(queryset, request)
                serializer = self.get_serializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(
                    {"message": "No genre found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublisherViewSet(ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()
    permission_classes = []
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query),
            )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.method == "GET":
            if len(queryset) > 0:
                paginator = StandardResultsSetPagination()
                result_page = paginator.paginate_queryset(queryset, request)
                serializer = self.get_serializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(
                    {"message": "No publisher found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

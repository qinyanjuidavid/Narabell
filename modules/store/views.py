from django.db.models import Q
from django.shortcuts import get_object_or_404
from modules.accounts.models import Reader
from modules.accounts.paginations import StandardResultsSetPagination
from modules.accounts.permissions import IsReader
from modules.store.models import Author, Book, Favourite, Genre, Publisher, Ratings
from modules.store.serializers import (
    AuthorSerializer,
    BookSerializer,
    FavouriteSerializer,
    GenreSerializer,
    PublisherSerializer,
    RatingSerializer,
)
from rest_framework import generics, serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


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


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = []
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset.filter(available=True)
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query),
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
                    {"message": "No book found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsReader]
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        reader = get_object_or_404(
            Reader,
            user=self.request.user,
        )
        queryset = Ratings.objects.filter(reader=reader)
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(book__title__icontains=query),
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
                    {"message": "No rating found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        context = {
            "request": request,
        }
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        rating = get_object_or_404(queryset, pk=pk)
        context = {
            "request": request,
        }
        serializer = self.get_serializer(
            rating,
            data=request.data,
            partial=True,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookMarkViewSet(ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated, IsReader]
    http_method_names = ["get", "put", "post", "patch"]

    def get_queryset(self):
        reader = get_object_or_404(
            Reader,
            user=self.request.user,
        )
        queryset = Favourite.objects.filter(reader=reader)
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(
                Q(book__title__icontains=query),
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
                    {"message": "No rating found"},
                    status=status.HTTP_200_OK,
                )

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        context = {
            "request": request,
        }
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

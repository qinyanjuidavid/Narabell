from modules.accounts.serializers import ReaderProfileSerializer
from rest_framework import serializer
from modules.store.models import Author, Book, Genre, Publisher
from v2.modules.store.models import Favourite, Ratings


class AuthorSerializer(serializer.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            "author_id",
            "name",
            "bio",
            "display_image",
            "date_of_birth",
            "date_or_death",
            "country",
            "created_at",
            "updated_at",
        )


class GenreSerializer(serializer.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "genre",
            "created_at",
            "updated_at",
        )


class PublisherSerializer(serializer.ModelSerializer):
    class Meta:
        model = Publisher
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
        )


class BookSerializer(serializer.ModelSerializer):
    publisher = PublisherSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "cover",
            "book",
            "author",
            "audio",
            "publisher",
            "year_published",
            "ISBN",
            "summary",
            "genre",
            "book_excerpt",
            "available",
            "created_at",
            "updated_at",
        )


class RatingSerializer(serializer.ModelSerializer):
    reader = ReaderProfileSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Ratings
        fields = (
            "id",
            "book",
            "reader",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        )


class FavouriteSerializer(serializer.ModelSerializer):
    reader = ReaderProfileSerializer(read_only=True)
    book = BookSerializer(read_only=True, many=True)

    class Meta:
        model = Favourite
        fields = (
            "id",
            "reader",
            "books",
            "created_at",
            "updated_at",
        )

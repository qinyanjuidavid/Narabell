from modules.accounts.models import Reader
from modules.accounts.serializers import ReaderProfileSerializer
from modules.store.models import Author, Book, Favourite, Genre, Publisher, Ratings
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            "author_id",
            "name",
            "bio",
            "display_image",
            "date_of_birth",
            "date_of_death",
            "country",
            "verified",
            "created_at",
            "updated_at",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "genre",
            "description",
            "genre_image",
            "created_at",
            "updated_at",
        )


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
        )


class BookSerializer(serializers.ModelSerializer):
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


class RatingSerializer(serializers.ModelSerializer):
    reader = ReaderProfileSerializer(read_only=True)
    rating = serializers.FloatField(required=True)

    class Meta:
        model = Ratings
        fields = (
            "id",
            "book",
            "reader",
            "rating",
            "comment",
            "flag",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        reader_query = Reader.objects.get(
            user=self.context["request"].user,
        )
        ratings, _ = Ratings.objects.get_or_create(
            book=validated_data["book"], reader=reader_query, flag=False
        )
        ratings.rating = validated_data.get("rating", ratings.rating)
        ratings.comment = validated_data.get("comment", ratings.comment)
        ratings.save()
        return ratings

    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance


class FavouriteSerializer(serializers.ModelSerializer):
    reader = ReaderProfileSerializer(read_only=True)
    # books= BookSerializer(many=True,)
    class Meta:
        model = Favourite
        fields = (
            "id",
            "reader",
            "books",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        reader_query = Reader.objects.get(
            user=self.context["request"].user,
        )
        
        favourite_query = Favourite.objects.get_or_create(
            reader=reader_query,
        )
        book_query= validated_data.get("books")
      
        for book in book_query:
            if book in favourite_query[0].books.all():
                favourite_query[0].books.remove(book)
            else:
                favourite_query[0].books.add(book)

        return favourite_query[0]

        
        

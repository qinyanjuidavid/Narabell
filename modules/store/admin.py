from django.contrib import admin

from modules.store.models import Book, Favourite, Publisher, Ratings, Author, Genre

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "author_id",
        "name",
        "verified",
        "date_of_birth",
        "country",
        "created_at",
        "updated_at",
    )
    list_filter = ("verified",)
    search_fields = ("author_id", "name")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre", "created_at", "updated_at")
    search_fields = ("genre",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "ISBN",
        "year_published",
        "available",
        "created_at",
        "updated_at",
    )
    list_filter = ("available",)
    search_fields = ("title", "ISBN")


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass

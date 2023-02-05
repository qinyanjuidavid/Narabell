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


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre", "created_at", "updated_at")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from modules.store.models import Book, Favourite, Publisher, Ratings, Author, Genre

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


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

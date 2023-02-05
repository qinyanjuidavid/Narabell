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
    list_display = (
        "get_book_name",
        "get_reader_name",
        "rating",
        "flag",
        "created_at",
        "updated_at",
    )
    list_filter = ("flag",)

    def get_book_name(self, obj):
        return obj.book.title

    get_book_name.short_description = "Book"
    get_book_name.admin_order_field = "book__title"

    def get_reader_name(self, obj):
        return obj.reader.user.full_name

    get_reader_name.short_description = "Reader"
    get_reader_name.admin_order_field = "reader__user__full_name"


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display=("get_reader_full_name","get_reader_email","created_at","updated_at")

    def get_reader_full_name(self, obj):
        return obj.reader.user.full_name

    get_reader_full_name.short_description = "Full Name"
    get_reader_full_name.admin_order_field = "reader__user__full_name"

    def get_reader_email(self, obj):
        return obj.reader.user.email

    get_reader_email.short_description = "Email"
    get_reader_email.admin_order_field = "reader__user__email"
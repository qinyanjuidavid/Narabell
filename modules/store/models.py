import uuid
from django.db import models
from modules.accounts.models import User, TrackingModel, Reader
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator


class Author(TrackingModel):
    author_id = models.UUIDField(
        _("author id"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    name = models.CharField(_("full name"), max_length=256)
    bio = models.TextField(_("bio"), blank=True, null=True)
    display_image = models.ImageField(
        _("display image"),
        default="display-img.png",
        upload_to="authors-image/",
    )
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    date_of_death = models.DateField(_("date of death"), blank=True, null=True)
    country = CountryField(_("country"), blank=True, null=True)
    verified = models.BooleanField(_("verified"), default=False)

    def __str__(self):
        return self.name or str(self.author_id)

    class Meta:
        verbose_name_plural = "Authors"
        ordering = ["-created_at"]


def book_genre_covers_directory_path(instance, filename):
    return f"covers/{instance.genre}/{filename}"


class Genre(TrackingModel):
    genre = models.CharField(_("genre"), max_length=256, unique=True)
    description = models.TextField(_("description"), default="***No description***")
    genre_image = models.ImageField(
        _("genre image"),
        upload_to=book_genre_covers_directory_path,
        default="genre.png",
    )

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name_plural = "Genre"
        ordering = ["-created_at"]


class Publisher(TrackingModel):
    name = models.CharField(_("publisher's name"), max_length=256, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Publishers"
        ordering = ["-created_at"]


def book_covers_directory_path(instance, filename):
    return f"covers/{instance.title}/{filename}"


def books_directory_path(instance, filename):
    return f"books/{instance.title}/{filename}"


def book_audio_directory_path(instance, filename):
    return f"audio/{instance.title}/{filename}"


class Book(TrackingModel):
    title = models.CharField(_("title"), max_length=256, unique=True)
    cover = models.ImageField(
        _("cover image"),
        upload_to=book_covers_directory_path,
        default="book.png",
    )
    book = models.FileField(_("book"), upload_to=books_directory_path)
    author = models.ManyToManyField(Author, related_name="authors")
    audio = models.FileField(
        _("audio"),
        upload_to=book_audio_directory_path,
        blank=True,
        null=True,
    )
    publisher = models.ManyToManyField(
        Publisher,
        related_name="publishers",
    )
    year_published = models.DateField(_("year published"), blank=True, null=True)
    ISBN = models.CharField(_("ISBN"), max_length=256, unique=True)
    summary = models.TextField(_("summary"), blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="genres")  # category
    book_excerpt = models.TextField(
        _("book excerpt"), max_length=500, blank=True, null=True
    )  # a short extract from a book,
    # especially one published separately or in a magazine or newspaper.
    available = models.BooleanField(_("avail"), default=False)

    def __str__(self):
        return self.title or str(self.ISBN)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ["-created_at"]


class Ratings(TrackingModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING)
    rating = models.FloatField(
        _("rating"),
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )
    comment = models.TextField(_("comment"), blank=True, null=True)
    flag = models.BooleanField(_("flag"), default=False)

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name_plural = "Ratings"
        ordering = ["-created_at"]


class Favourite(TrackingModel):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE)
    books = models.ManyToManyField(
        Book,
        related_name="favourite_books",
    )

    def __str__(self):
        return self.reader.user.full_name or str(self.reader.user.phone)

    class Meta:
        verbose_name_plural = "Favourite Books"
        ordering = ["-id", "-created_at"]

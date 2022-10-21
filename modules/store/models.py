from distutils.command.upload import upload
import uuid
from django.db import models
from modules.accounts.models import User, TrackingModel
from django.utils.translation import gettext as _
from django_countries.fields import CountryField


class Author(TrackingModel):
    author_id = models.UUIDField(
        _("author id"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    name = models.CharField(_("full name"), max_length=256)
    bio = models.TextField(_("bio"))
    display_image = models.ImageField(
        _("display image"),
        upload_to="authors-image/",
    )
    date_of_birth = models.DateField(_("date of birth"), null=True)
    date_of_death = models.DateField(_("date of death"), null=True)
    country = CountryField(_("country"), blank=True, null=True)

    def __str__(self):
        return self.name or str(self.author_id)

    class Meta:
        verbose_name_plural = "Authors"
        ordering = ["-created_at"]


class Genre(TrackingModel):
    pass


class Publisher(TrackingModel):
    pass


class Book(TrackingModel):
    # title
    # cover_image
    # book
    # author(m2m)
    # audio
    # publisher(m2m)
    # year published
    # ISBN
    # summary
    # genre(m2m) category
    # book excerpt meaning- a short extract from a book, especially one published separately or in a magazine or newspaper.
    pass


class Ratings(TrackingModel):
    # book
    # rating
    # comment
    # reader
    pass

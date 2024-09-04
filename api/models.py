from django.db import models
from uuid import uuid4


class Author(models.Model):
    """
    Model representing an author of a book in the library.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="Unique ID for this particular author across whole library",
    )
    name = models.CharField(max_length=255, help_text="Enter author's name")
    bio = models.TextField(help_text="Enter author's bio")
    birth_date = models.DateField(help_text="Enter author's birth date")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book in the library.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="Unique ID for this particular book across whole library",
    )
    title = models.CharField(max_length=255, help_text="Enter book's title")
    description = models.TextField(help_text="Enter book's description")
    publish_date = models.DateField(help_text="Enter book's publish date")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        help_text="Enter book's author",
        db_index=True,
    )

    def __str__(self):
        return self.title

from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Author model.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        """
        List all authors, using cache if available.
        """
        cache_key = "all_authors"
        authors = cache.get(cache_key)
        if not authors:
            authors = super().list(request, *args, **kwargs).data
            cache.set(cache_key, authors, settings.CACHE_TIMEOUT)
        return Response(authors)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific author, using cache if available.
        """
        cache_key = f"author_{kwargs['pk']}"
        author = cache.get(cache_key)
        if not author:
            response = super().retrieve(request, *args, **kwargs)
            if response.status_code == 200:
                cache.set(cache_key, response.data, settings.CACHE_TIMEOUT)
            return response
        return Response(author)

    @action(detail=True, methods=["get"], url_path="books")
    def get_books(self, request, pk=None):
        """
        Retrieve all books by a specific author.
        """
        author = Author.objects.prefetch_related("books").filter(id=pk).first()
        if not author:
            return Response(
                {"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND
            )
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete("all_authors")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete("all_authors")
        cache.delete(f"author_{serializer.instance.pk}")

    def perform_destroy(self, instance):
        cache.delete("all_authors")
        cache.delete(f"author_{instance.pk}")
        super().perform_destroy(instance)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Book model.
    """

    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        """
        List all books, using cache if available.
        """
        cache_key = "all_books"
        books = cache.get(cache_key)
        if not books:
            books = super().list(request, *args, **kwargs).data
            cache.set(cache_key, books, settings.CACHE_TIMEOUT)
        return Response(books)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific book, using cache if available.
        """
        cache_key = f"book_{kwargs['pk']}"
        book = cache.get(cache_key)
        if not book:
            response = super().retrieve(request, *args, **kwargs)
            if response.status_code == 200:
                cache.set(cache_key, response.data, settings.CACHE_TIMEOUT)
            return response
        return Response(book)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete("all_books")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete("all_books")
        cache.delete(f"book_{serializer.instance.pk}")

    def perform_destroy(self, instance):
        cache.delete("all_books")
        cache.delete(f"book_{instance.pk}")
        super().perform_destroy(instance)

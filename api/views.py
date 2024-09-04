from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))  # Cache for 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))  # Cache for 15 minutes
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


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Book model.
    """

    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))  # Cache for 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

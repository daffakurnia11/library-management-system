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

    @action(detail=True, methods=["get"], url_path="books")
    def get_books(self, request, pk=None):
        """
        Retrieve all books by a specific author.
        """
        try:
            author = Author.objects.get(pk=pk)
            books = author.books.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Book model.
    """

    serializer_class = BookSerializer

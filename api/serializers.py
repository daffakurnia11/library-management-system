from rest_framework import serializers
from .models import Book, Author
from datetime import date


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    """

    class Meta:
        model = Author
        fields = "__all__"

    def validate_birth_date(self, value):
        """
        Check that the birth date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    """

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "description", "publish_date", "author", "author_id"]

    def validate_publish_date(self, value):
        """
        Check that the publish date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Publish date cannot be in the future.")
        return value

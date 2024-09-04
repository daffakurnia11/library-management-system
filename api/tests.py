import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class AuthorAPITestCase(APITestCase):

    def setUp(self):
        self.author_data = {
            "name": "John Doe",
            "bio": "A prolific writer of mystery novels.",
            "birth_date": "1970-01-01",
        }
        self.author = Author.objects.create(**self.author_data)
        self.book_data = {
            "title": "Mystery Novel",
            "description": "A thrilling mystery novel.",
            "publish_date": "2023-01-01",
            "author": self.author,
        }
        self.book = Book.objects.create(**self.book_data)

    def test_create_author(self):
        url = reverse("api:authors-list")
        response = self.client.post(url, self.author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        url = reverse("api:authors-detail", args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.author.name)

    def test_update_author(self):
        url = reverse("api:authors-detail", args=[self.author.id])
        updated_data = self.author_data.copy()
        updated_data["name"] = "Jane Doe"
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, "Jane Doe")

    def test_delete_author(self):
        url = reverse("api:authors-detail", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_retrieve_nonexistent_author(self):
        url = reverse("api:authors-detail", args=["nonexistent-id"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_author_books(self):
        url = reverse("api:authors-get-books", args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)

    def test_get_nonexistent_author_books(self):
        url = reverse("api:authors-detail", args=["nonexistent-id"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_author_with_future_birth_date(self):
        url = reverse("api:authors-list")
        future_date_data = self.author_data.copy()
        future_date_data["birth_date"] = "2050-01-01"
        response = self.client.post(url, future_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author_without_required_fields(self):
        url = reverse("api:authors-list")
        invalid_data = {
            "bio": "Missing name field",
            "birth_date": "1980-01-01",
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author_with_invalid_birth_date(self):
        url = reverse("api:authors-list")
        invalid_data = {
            "name": "Jane Doe",
            "bio": "A new author",
            "birth_date": "not-a-date",
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            bio="A prolific writer of mystery novels.",
            birth_date="1970-01-01",
        )
        self.book_data = {
            "title": "Mystery Novel",
            "description": "A thrilling mystery novel.",
            "publish_date": "2023-01-01",
            "author_id": self.author.id,
        }
        self.book = Book.objects.create(
            title="Mystery Novel",
            description="A thrilling mystery novel.",
            publish_date="2023-01-01",
            author=self.author,
        )

    def test_create_book(self):
        url = reverse("api:books-list")
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        url = reverse("api:books-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        url = reverse("api:books-detail", args=[self.book.id])
        updated_data = self.book_data.copy()
        updated_data["title"] = "New Mystery Novel"
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "New Mystery Novel")

    def test_delete_book(self):
        url = reverse("api:books-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_book_without_author(self):
        invalid_data = self.book_data.copy()
        invalid_data["author_id"] = "nonexistent-id"
        url = reverse("api:books-list")
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_future_publish_date(self):
        url = reverse("api:books-list")
        future_date_data = self.book_data.copy()
        future_date_data["publish_date"] = "2050-01-01"
        response = self.client.post(url, future_date_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_with_invalid_data(self):
        url = reverse("api:books-detail", args=[self.book.id])
        invalid_data = self.book_data.copy()
        invalid_data["title"] = ""
        response = self.client.put(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_book_with_invalid_uuid_format(self):
        url = reverse("api:books-detail", args=["invalid-uuid-format"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book(self):
        url = reverse("api:books-detail", args=["nonexistent-id"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()

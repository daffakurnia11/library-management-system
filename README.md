# Library Management System

The Library Management System is a Django-based application designed to handle the management of books and authors. It uses Django REST Framework to provide API endpoints for various operations related to authors and books. This project serves as a technical test for Lead Programmer 2.0.

## Features

- Manage authors (create, retrieve, update, delete).
- Manage books (create, retrieve, update, delete).
- Retrieve all books written by a specific author.

## Technology Stack

The project uses the following technologies and libraries:

- Django 5.1
- Django REST Framework 3.15.2
- Django CORS Headers 4.4.0
- Django Environ 0.11.2
- Django Redis 5.4.0
- Faker 28.1.0 (for generating fake data)
- Redis 5.0.8 (for caching)
- Python Dateutil 2.9.0

## Installation

Follow these steps to set up the project in your local environment:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/daffakurnia11/library-management-system.git
   cd library-management-system
   ```

2. **Create a virtual environment**:

   ```bash
   python -m .venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Run the Redis server**:

   ```bash
   redis-server
   ```

5. **Run database migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **(Optional) Seed the database with initial data**:

   ```bash
   python manage.py seed_data
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authors

- `GET /authors` - Retrieve a list of all authors.
- `GET /authors/{id}` - Retrieve details of a specific author.
- `POST /authors` - Create a new author.
- `PUT /authors/{id}` - Update an existing author.
- `DELETE /authors/{id}` - Hard delete an author.

### Books

- `GET /books` - Retrieve a list of all books.
- `GET /books/{id}` - Retrieve details of a specific book.
- `POST /books` - Create a new book.
- `PUT /books/{id}` - Update an existing book.
- `DELETE /books/{id}` - Hard delete a book.

### Associations

- `GET /authors/{id}/books` - Retrieve all books by a specific author.

## API Documentation

After starting the development server, you can access the API documentation using Django REST Framework's browsable API. This documentation will provide a user-friendly interface to explore and interact with the API endpoints directly.

1. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

2. **Open your web browser and navigate to the following URL**:

   ```
   http://127.0.0.1:8000/api/
   ```

   Here, you will find the documentation for all available API endpoints, which includes descriptions, parameters, and example requests and responses for each endpoint.

## Database Schema

The application uses SQLite as the default database for development purposes. This is specified in the `settings.py` file of the Django project.

- **Default Database**: _SQLite_

The database schema consists of two main tables:

- **Authors**:

  - `id`: UUIDv4, Primary Key
  - `name`: String
  - `bio`: Text
  - `birth_date`: Date

- **Books**:
  - `id`: UUIDv4, Primary Key
  - `title`: String
  - `description`: Text
  - `publish_date`: Date
  - `author_id`: Foreign Key (references Authors table)

## Folder Structure

The project is organized as follows:

```
library-management-system/
│
├── api/
│ ├── management/
│ ├── __init__.py
│ │ └── commands/
│ │ ├── __init__.py
│ │ └── seed_data.py
│ │
│ ├── migrations/
│ │ ├── __init__.py
│ │ └── ... (other migration files)
│ │
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
│
├── library_management/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── .env.example
├── .gitignore
├── db.sqlite3
├── dump.rdb
├── manage.py
├── README.md
└── requirements.txt
```

## Testing

This project uses Django's built-in testing framework. To run the tests, use:

```bash
python manage.py test
```

The test suite covers the following scenarios:

### **Author Test Scenarios**

1. **Create Author:**

   - Test creating an author with valid data (`test_create_author`).

2. **Retrieve Author:**

   - Test retrieving details of a specific author by ID (`test_retrieve_author`).

3. **Update Author:**

   - Test updating an author's information with valid data (`test_update_author`).

4. **Delete Author:**

   - Test deleting a specific author by ID (`test_delete_author`).

5. **Retrieve Non-existent Author:**

   - Test retrieving an author that does not exist, using a non-existent ID (`test_retrieve_nonexistent_author`).

6. **Get Author's Books:**

   - Test retrieving all books written by a specific author (`test_get_author_books`).

7. **Get Books for Non-existent Author:**

   - Test retrieving books for a non-existent author, using a non-existent ID (`test_get_nonexistent_author_books`).

8. **Create Author with Future Birth Date:**

   - Test creating a book with a `birth_date` set in the future (`test_create_author_with_future_birth_date`).

9. **Create Author Without Required Fields:**

   - Test creating an author without required fields (e.g., missing `name`) (`test_create_author_without_required_fields`).

10. **Create Author with Invalid Birth Date:**

- Test creating an author with an invalid date format for `birth_date` (`test_create_author_with_invalid_birth_date`).

### **Book Test Scenarios**

1. **Create Book:**

   - Test creating a book with valid data (`test_create_book`).

2. **Retrieve Book:**

   - Test retrieving details of a specific book by ID (`test_retrieve_book`).

3. **Update Book:**

   - Test updating a book's information with valid data (`test_update_book`).

4. **Delete Book:**

   - Test deleting a specific book by ID (`test_delete_book`).

5. **Create Book Without Author:**

   - Test creating a book with a non-existent author reference (`test_create_book_without_author`).

6. **Create Book with Future Publish Date:**

   - Test creating a book with a `publish_date` set in the future (`test_create_book_with_future_publish_date`).

7. **Update Book with Invalid Data:**

   - Test updating a book with invalid data (e.g., empty `title`) (`test_update_book_with_invalid_data`).

8. **Retrieve Book with Invalid UUID Format:**

   - Test retrieving a book using an invalid UUID format (`test_retrieve_book_with_invalid_uuid_format`).

9. **Delete Non-existent Book:**
   - Test deleting a book that does not exist, using a non-existent ID (`test_delete_nonexistent_book`).

## Performance Tuning

- **Caching**: Redis is used to cache frequently accessed data, reducing the load on the database and improving response times.
- **Scalability**: For handling millions of records, consider implementing database indexing on frequently queried fields (e.g., `author_id` and other primary key).

### Future Enhancements for Performance

- Use pagination for API responses to manage large data sets efficiently.
- Implement a dedicated search service (e.g., Elasticsearch) for faster searches across large datasets.
- Use load balancing techniques to distribute traffic efficiently.

## Contact Information

For any inquiries, feel free to reach out:

- **Email**: daffakurniaf11@gmail.com
- **WhatsApp**: [+6285156317473](https://wa.me/6285156317473)
- **LinkedIn**: [Daffa Kurnia Fatah](https://www.linkedin.com/in/daffakurniafatah/)
- **Portfolio**: [dafkur.com](https://dafkur.com/)

## Additional Notes

- Ensure that the `.env` file is configured correctly for your local environment.
- Redis is used for caching, so ensure the Redis server is running when working with caching.

from django.core.management.base import BaseCommand
from api.models import Author, Book
from faker import Faker


class Command(BaseCommand):
    help = "Seed database with initial data for development"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        self.seed_authors()
        self.seed_books()
        self.stdout.write("Seeding complete.")

    def seed_authors(self):
        """
        Create sample authors.
        """
        faker = Faker()
        for _ in range(10):
            Author.objects.create(
                name=faker.name(),
                bio=faker.text(),
                birth_date=faker.date_of_birth(tzinfo=None),
            )
        self.stdout.write(self.style.SUCCESS("Authors seeded successfully."))

    def seed_books(self):
        """
        Create sample books linked to authors.
        """
        faker = Faker()
        authors = Author.objects.all()
        if not authors:
            self.stdout.write(
                self.style.ERROR("No authors found. Please seed authors first.")
            )
            return

        for author in authors:
            for _ in range(3):
                Book.objects.create(
                    title=faker.sentence(nb_words=5),
                    description=faker.text(),
                    publish_date=faker.date_this_decade(),
                    author=author,
                )
        self.stdout.write(self.style.SUCCESS("Books seeded successfully."))

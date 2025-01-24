from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import Book

class Command(BaseCommand):
    help = 'Update slugs for existing books'

    def handle(self, *args, **kwargs):
        books = Book.objects.all()
        for book in books:
            if not book.slug:
                book.slug = slugify(book.title)
                book.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs for existing books'))
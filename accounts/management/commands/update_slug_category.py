from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import Book , Category

class Command(BaseCommand):
    help = 'Update slugs for existing categorys'

    def handle(self, *args, **kwargs):
        categorys = Category.objects.all()
        for category in categorys:
            if not category.slug:
                category.slug = slugify(category.name)
                category.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs for existing categorys'))